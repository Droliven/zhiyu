# R1 / GRPO / 奖励优化专题：从视频几何一致性到机器人策略

**报告标签**：R1, GRPO, Flow-GRPO, 强化学习, Reward Optimization, 3D/4D, video generation, Robot Policy

> 严格收录知域中直接使用 R1-style、GRPO、RL post-training 或显式奖励优化的 6 篇工作；不因标题、机器人型号或 on-policy 字样做表面匹配。

## 专题结论

这 6 篇形成两条路线：World-R1、GeoFlow、VGGRPO、Stream4D 用 3D/4D foundation model 或运动先验构造视频奖励；Discrete-WAM 与 Galaxea G0.5 则把可计算 log-prob 的离散视觉/动作 token 接入策略强化学习。共同难点不是“有没有 reward”，而是 reward 是否覆盖真实动态、是否造成静态化等投机行为，以及 rollout/reward server 的成本是否可承受。

| 路线 | 工作 | 奖励或优化对象 | 主要风险 |
|---|---|---|---|
| RGB 几何奖励 | GeoFlow | 刚性背景 flow + 动态语义保持 | 遮挡、拓扑变化与采样间隔漏检 |
| 4D latent 奖励 | VGGRPO | latent geometry / scene flow | 奖励模型偏差与 HOI 细节缺失 |
| R1 复合奖励 | World-R1 | 3D 重建、相机轨迹、VLM 质量 | reward hacking 与视频静态化 |
| 动态 4D 奖励 | Stream4D | 4D 重建 + 运动先验 | 4D 重建器偏差和计算成本 |
| World-policy RL | Discrete-WAM | 离散视觉—动作 token 策略 | 离散化误差与闭环安全 |
| Robot GRPO | Galaxea G0.5 | 自回归动作 token policy | 真机样本成本与奖励设计 |

## 纳入与排除边界

- **纳入**：论文方法或正式实验明确包含 GRPO、Flow-GRPO、RL post-training、RLHF/奖励反馈或策略强化学习。
- **不纳入 WAM-OPD**：它虽然 on-policy 收集数据，但目标是教师蒸馏，并明确强调不依赖稀疏奖励 RL。
- **不纳入 Riemann-1.0**：名称含“1.0”，并非 R1-style 强化学习。
- **不因 R1-Pro 纳入其他论文**：R1-Pro 是机器人平台名称，不是奖励优化方法。

## 对 HOI / 世界模型的直接启发

R1 路线若迁移到手—物交互，奖励不能只检查静态 3D 重建；至少需要联合 hand pose、object pose、持续 correspondence、contact timing、动作后的 object response 与运动幅度，避免模型通过减少接触、冻结物体或降低运动来骗取几何一致性分数。

---

## 1. World-R1: Reinforcing 3D Constraints for Text-to-Video Generation

- **作者**：Weijie Wang, Xiaoxuan He, Youping Gu, Yifan Yang, Zeyu Zhang, Yefei He, Yanbo Ding, Xirui Hu, Donny Y. Chen, Zhiyuan He, Yuqing Yang, Bohan Zhuang
- **年份与发表**：2026
- **arXiv ID**：2604.24764
- **DOI**：10.48550/arXiv.2604.24764
- **可靠入口**：[论文](https://arxiv.org/abs/2604.24764) · [项目](https://microsoft.github.io/World-R1/) · [代码](https://github.com/microsoft/World-R1) · [数据](https://huggingface.co/datasets/microsoft/World-R1) · [AlphaXiv](https://alphaxiv.org/abs/2604.24764)
- **类别标签**：R1, Flow-GRPO, 3D Reward, Text-to-Video, 几何一致性
- **证据边界**：沿用知域既有来源报告的论文核验；本专题重新分类，不声称完成独立复现。

- **代表图**：World-R1，Fig. 2 / Pipeline Overview，。来源：[原图](https://microsoft.github.io/World-R1/tech.html)

![World-R1 Fig. 2: pipeline overview](https://microsoft.github.io/World-R1/assets/pipeline.jpg)

### 核心内容与 Insight

World-R1 的出发点与 GeoFlow/VGGRPO 接近：video foundation model 已有强视觉合成能力，但缺内在 3D 几何约束。它反对在推理时加重型 3D control modules，主张通过 RL 后训练把几何一致性“内化”到模型中。

核心 insight：

> 用 3D foundation model 和 VLM 作为 reward providers，通过 Flow-GRPO 对 text-to-video 模型做后训练，可以在不改架构、不加推理期 3D 模块的情况下强化 3D consistency。

它还引入 implicit camera conditioning：从 text 中解析 camera motion，将轨迹先验写入 initial latent noise，而不是增加额外控制网络。

### Pipeline

- **输入**：pure text world-simulation prompt；其中可包含 camera push / pull / pan / orbit 等运动描述。
- **Camera conditioning**：
  - 解析文本中的 camera motion tokens；
  - 转为 deterministic camera extrinsics；
  - 投影成 dense optical flow；
  - 用 trajectory-guided noise wrapping 注入初始 latent noise。
- **Policy rollout**：Wan2.1 T2V backbone 生成 grouped candidate videos。
- **Reward design**：
  - Depth Anything 3 / DA3 将视频 lifted 到 3DGS；
  - meta-view score：用 Qwen3-VL 判断 novel/meta views 是否合理；
  - rendering score：用 LPIPS 等衡量重渲染一致性；
  - trajectory score：评估 camera trajectory adherence；
  - general reward：HPSv3 约束视觉质量。
- **Training strategy**：Flow-GRPO-Fast；周期性 decoupled training，每 100 steps 暂时关闭 3D reward，只用 general reward 在 dynamic prompts 上训练，避免过度刚性化。
- **输出**：World-R1-Small / World-R1-Large 这类 3D-consistent T2V 模型。

### 实验与证据

- World-R1-Small / Large 在 3D consistency benchmark 上显著优于 Wan2.1 / Wan2.2 / CogVideoX 等 baseline。
- 官方技术页报告 World-R1-Large 达 27.67 PSNR / 0.865 SSIM / 0.162 LPIPS；World-R1-Small 相对 Wan2.1-1.3B 有 +10.23 dB PSNR 改善。
- User study 中，World-R1 相对 Wan2.1 在 geometry/control/overall preference 上有优势。
- 121-frame long-video evaluation 中，World-R1-Large 将 PSNR 从 18.32 提升到 26.32。

需要注意：这些实验支持的是 **3D consistency / camera control / visual quality preservation**，不是严格意义上的物理仿真或可交互因果 world model。

### 代码与数据

- **代码**：GitHub 已公开，MIT license。仓库包含 `flow_grpo`、`reward_server`、`scripts`、`dataset` 等目录，并给出单机/多机训练、reward server、inference 脚本。
- **数据**：Hugging Face `microsoft/World-R1` 已公开 prompt-only dataset，包含 `final` 与 `enhanced` 两个 config。数据卡明确说明不包含生成视频、reward annotations、human preference labels 或 model checkpoints。
- **模型权重**：公开页面主要提供代码和 prompt dataset；是否发布完整 LoRA/model checkpoint 需以官方仓库后续说明为准。

### 局限、失败案例与开放问题

作者明确指出两点局限：

- RL 用于视频生成仍成本高，因为需要重复 rollout 和 reward evaluation。
- World-R1 受基础视频模型生成能力限制；dense multi-object composition、fine-grained non-rigid motion、detailed hand dynamics、very long-horizon scene evolution 仍可能继承 base model artifacts。

作者还分析了 reward hacking 风险：如果只优化窄 3D metric，模型可能生成 near-static clips 来方便重建但不遵循 camera motion。World-R1 用 composite reward、trajectory term、periodic dynamic-only training 来缓解，但这不等于完全消除。

### 与知域的关系

R1-style 视频后训练的核心条目：以 3D foundation model 和 VLM 提供复合奖励，用 Flow-GRPO 将几何一致性内化到生成模型。

## 2. GeoFlow: Enforcing Implicit Geometric Consistency in Video Generation

- **作者**：Jan Ackermann, Shengqu Cai, Boyang Deng, Zhengfei Kuang, Songyou Peng, Gordon Wetzstein
- **年份与发表**：2026
- **arXiv ID**：2605.18365
- **DOI**：10.48550/arXiv.2605.18365
- **可靠入口**：[论文](https://arxiv.org/abs/2605.18365) · [项目](https://geometryflow.github.io/) · [代码](https://github.com/geometryflow/GeoFlow) · [模型](https://huggingface.co/ackermannj/geoflow) · [AlphaXiv](https://alphaxiv.org/abs/2605.18365)
- **类别标签**：Flow-GRPO, RL Post-training, Geometry Reward, Video Generation
- **证据边界**：沿用知域既有来源报告的论文核验；本专题重新分类，不声称完成独立复现。

- **代表图**：GeoFlow，Fig. 2 "GeoFlow method overview"，。来源：[原图](https://geometryflow.github.io/)

![GeoFlow Fig. 2: method overview](https://geometryflow.github.io/assets/images/method.png)

### 核心内容与 Insight

作者明确声称的问题：通用 text-to-video diffusion model 在 camera motion 和 object motion 下常出现对象形变、纹理漂移、背景非刚性抖动。GeoFlow 的核心 insight 是：

> 几何一致的视频应满足两类近似条件：静态背景运动应能被相机运动诱导的刚性 flow 解释；独立运动物体沿其运动轨迹应保持语义/外观身份。

因此 GeoFlow 不直接要求有 3D/4D ground truth，而是从生成视频自身出发，用 monocular depth/pose、optical flow、DINO feature correspondence 构造一个 geometry-consistency reward，再用 Flow-GRPO 对 video generator 做 RL fine-tuning。

### Pipeline

- **输入**：text prompt；基础视频模型为 Wan2.1-T2V-1.3B。
- **视频采样**：对每个 prompt 采样一组 candidate videos，并同步初始噪声以降低 group comparison 方差。
- **几何奖励**：
  - Depth Anything 3 预测 depth、camera intrinsics / extrinsics；
  - WAFT / optical flow 估计相邻帧 observed flow；
  - 由 depth + relative camera pose 计算 rigid camera-induced flow；
  - 比较 observed flow 与 rigid flow，得到 background / structural consistency；
  - 用 DINOv2 feature 在 flow-warped frame 与目标帧间比较，约束 dynamic object identity。
- **优化**：用 Flow-GRPO 做 RL post-training；仅对早期 denoising steps 做 truncated backpropagation，以控制显存和计算。
- **输出**：几何一致性更好的 text-to-video generator / LoRA adapter。

### 实验与证据

- GeoFlow 在 static / dynamic、simple / complex 四类设置下整体降低几何错误。
- 它并非简单提升画质，而是针对几何与时序一致性有针对性改善。
- 消融显示：几何结构奖励与 DINO semantic consistency reward 互补；只做 SFT 不足以稳定提升几何一致性。

### 代码与数据

- **代码**：GitHub 已公开，包含 sampler、evaluation scripts、reward server、tests、第三方子模块说明。
- **模型**：Hugging Face 发布 GeoFlow LoRA adapter；模型卡显示是基于 `wan-ai/Wan2.1-T2V-1.3B-Diffusers` 的 PEFT LoRA。
- **数据**：论文说明 evaluation prompts 来自 OpenVid-1M / DL3DV 并经 Gemini 标准化；仓库含 `eval_data`，但训练 prompt 全量细节需要以仓库实际发布为准。

### 局限、失败案例与开放问题

作者在附录和项目页明确提到：

- 对严重拓扑变化不稳，例如大遮挡、打开抽屉露出新内容等，因为 pixel persistence 假设被破坏。
- 快速瞬时错误如果发生在 reward sampling interval 之外，可能无法惩罚。
- RL alignment 受基础模型能力上限约束；若 base model 对 OOD prompt 已经完全混乱，reward 可能过稀疏。
- 静态/动态区域边界模糊时，reward 可能误伤合理动态，例如布料/帐篷摆动。
- 仍可能只部分改善一致性，不能消除所有 artifacts。

### 与知域的关系

提供无需 3D/4D ground truth 的几何奖励构造，并以 Flow-GRPO 优化视频模型；适合作为 World-R1 的近邻方法和 HOI reward 设计参考。

## 3. VGGRPO: Towards World-Consistent Video Generation with 4D Latent Reward

- **作者**：Zhaochong An, Orest Kupyn, Theo Uscidda, Andrea Colaco, Karan Ahuja, Serge Belongie, Mar Gonzalez-Franco, Marta Tintore Gazulla
- **年份与发表**：2026
- **arXiv ID**：2603.26599
- **DOI**：10.48550/arXiv.2603.26599
- **可靠入口**：[论文](https://arxiv.org/abs/2603.26599) · [项目](https://zhaochongan.github.io/projects/VGGRPO/) · [AlphaXiv](https://alphaxiv.org/abs/2603.26599)
- **类别标签**：GRPO, 4D Latent Reward, Video Generation, 几何一致性
- **证据边界**：沿用知域既有来源报告的论文核验；本专题重新分类，不声称完成独立复现。

- **代表图**：VGGRPO，Fig. 2 "Method Overview"，。来源：[原图](https://zhaochongan.github.io/projects/VGGRPO/)

![VGGRPO Fig. 2: method overview](https://zhaochongan.github.io/projects/VGGRPO/VGGRPO_files/pipeline.png)

### 核心内容与 Insight

VGGRPO 针对的是 RGB-space geometry reward 的成本和鲁棒性问题。作者认为：已有 alignment 方法常在 RGB 解码后再跑几何模型，导致反复 VAE decoding，计算贵；而 RGB-based reward 还容易受生成图像分布偏移影响。

核心 insight：

> 如果 video diffusion latent 已包含足够视觉信息，可以训练一个 Latent Geometry Model，把 diffusion latent 直接接到 4D geometry foundation model，从 latent 中解码 camera pose、depth、point map、scene flow，再在 latent space 做 GRPO reward。

这使几何奖励不必每次回到 RGB pixel space，也能利用 4D reconstruction model 支持 dynamic scenes。

### Pipeline

- **输入**：text prompt、video diffusion latents。
- **Latent Geometry Model (LGM)**：
  - 用 VAE encoder 得到 video latents；
  - 通过 lightweight connector / transformer layers 接到 geometry foundation model；
  - 预测 camera pose、point map、depth map、scene flow 等 4D geometry outputs；
  - 用 alignment loss 保留几何 foundation model 的 4D prior。
- **VGGRPO post-training**：
  - video diffusion model 采样 grouped rollouts；
  - LGM 直接从 denoised latents 预测几何；
  - 计算 camera motion smoothness reward 与 geometry reprojection consistency reward；
  - 在 latent space 中执行 GRPO 更新。
- **输出**：更 world-consistent 的 video diffusion model；论文还给出 training-free latent reward guidance 伪代码。

### 实验与证据

- VGGRPO 在 static/dynamic scenes 中都改善 camera smoothness、geometry consistency 和整体质量。
- LGM 相比“latent -> RGB -> geometry model”的路径更抗 latent perturbation，说明 latent-space reward 减少了 RGB decoding domain gap。
- 附录中的 VBench 表显示，VGGRPO 相比 baseline / SFT / Epipolar-DPO / VideoGPA 在 subject/background consistency、motion smoothness、image quality 等维度整体更稳。

### 代码与数据

- **项目页**：提供 arXiv paper 和大量 qualitative comparisons。
- **代码/模型**：截至本次检索，项目页未显示公开 GitHub / model weights 链接；arXiv 摘要页也未声明代码开放。置信度：中等，以作者后续更新为准。
- **数据**：未发现单独开放的训练/评测数据链接；论文使用 RealEstate10K 等 benchmark 做分析。

### 局限、失败案例与开放问题

论文没有像 GeoFlow 那样集中列出详细 failure cases，但根据方法假设和实验范围，可明确区分：

- **作者明确覆盖**：static + dynamic scene geometry consistency、camera smoothness、latent reward efficiency。
- **实验未充分证明**：对细粒度物理交互、手物接触、物体可操作状态变化的建模能力。
- **潜在局限**：
  - 奖励质量受 LGM 和背后 geometry foundation model 上限影响；
  - 对严重拓扑变化、细粒度非刚性接触、透明/反光物体等可能仍难；
  - 不是 action-conditioned world model，不能直接证明“动作导致世界变化”的因果一致性。

### 与知域的关系

把 4D geometry reward 移到 diffusion latent，减少反复 RGB 解码；它回答的是奖励如何高效计算，而不是 hand-object interaction 本身。

## 4. Stream4D: 4D-Consistency for Streaming Autoregressive Diffusion Video Models

- **作者**：Yuanhao Ban, Jiaqi Feng, Hengguang Zhou, Xiaohuan Pei, Justin Cui, Cho-Jui Hsieh
- **年份与发表**：2026，arXiv 预印本（Under review）
- **arXiv ID**：2608.19556
- **DOI**：10.48550/arXiv.2608.19556
- **可靠入口**：[论文](https://arxiv.org/abs/2608.19556) · [项目](https://banyuanhao.github.io/Stream4D/) · [AlphaXiv](https://alphaxiv.org/abs/2608.19556)
- **类别标签**：4D Reward, Streaming Video, RLHF, Motion Preservation
- **证据边界**：沿用知域既有来源报告的论文核验；本专题重新分类，不声称完成独立复现。

- **代表图**：Stream4D，Fig. 1，静态 3D 奖励导致场景冻结，而动态 4D 奖励保留运动并改善长程一致性。。来源：[原图](https://arxiv.org/html/2608.19556v1/figure1_teaser.png)

![Stream4D Fig. 1：静态 3D 奖励与动态 4D 奖励对比](https://arxiv.org/html/2608.19556v1/figure1_teaser.png)

### 核心内容与 Insight

Stream4D 解决流式自回归视频生成中的长程几何漂移和运动退化问题。核心 insight 是：**用静态 3D 高斯泼溅重建作为一致性奖励会惩罚真实运动**——因为动态物体无法被单个刚性 3D 重建解释，奖励最大化的捷径是冻结画面。在自回归设置下，每个 chunk 会传播前一个 chunk 的错误，这种"冻结捷径"尤其有害。

Stream4D 用前馈 4D 重建（MoVieS）替代静态 3D 重建，使得能够被一致动态 4D 场景解释的视频获得高奖励。附加运动先验奖励自然场景流幅度并惩罚抖动和非刚性伪影，加上轻量感知锚点稳定外观。

### Pipeline

**输入**：自回归扩散骨干生成的视频 rollout

**过程**：MoVieS 将 rollout 重建为动态 4D 高斯场景，在估计相机下重渲染，4D PSNR 作为一致性奖励；场景流幅度的峰值高斯目标 + 平滑/刚性正则作为运动先验；HPSv2 作为感知锚点；三项 z 归一化后求和作为总奖励。

**输出**：奖励信号反馈给自回归扩散策略，用于 RLHF 或蒸馏微调

### 实验与证据

- **骨干**：Self-Forcing, Causal-Forcing, LongLive
- **指标**：MoVieS 4D-PSNR, Gemini Consistency win%, VideoReward Overall win%
- **定量结果**：4D-PSNR 提升 +3.46/+5.53/+6.76 dB；Gemini Consistency win% 82.2%/73.9%/74.2%；VideoReward Overall win% 66.2%/76.0%/84.4%
- **消融**：项目页对比了 World-R1 和 VideoGPA（静态 3D 奖励基线），Stream4D 在运动保持上一致更优
- **实验直接支持的结论**：4D 重建奖励有效替代静态 3D 奖励，避免运动退化；跨骨干泛化；人类偏好更高
- **尚未被实验支持的主张**：运动先验的"自然运动量级"假设是否跨场景泛化

### 代码与数据

代码和模型在项目页标注 "Under review"，暂未公开。

### 局限、失败案例与开放问题

- MoVieS 自身的重建误差和偏差会传递到奖励信号中，失败模式未讨论
- 运动先验对"自然运动量级"的假设可能不适用于所有场景
- 评估在 500 个运动突出提示词上进行，低运动/静态场景覆盖不明
- 依赖 MoVieS 做 4D 重建，计算开销未报告

### 与知域的关系

针对 World-R1 类静态 3D 奖励的冻结捷径，以动态 4D 重建奖励保留真实运动，是流式视频奖励设计的重要修正。

## 5. Discrete-WAM: Unified Discrete Vision-Action Token Editing for World-Policy Learning

- **作者**：Ziyang Yao, Haochen Liu, Yuncheng Jiang, Zeyu Zhu, Zibin Guo, Jingru Wang, Tianle Liu, Jianwei Cui, Kuiyuan Yang, Hongwei Xie, Jingwei Zhao, Guang Chen, Hangjun Ye
- **年份与发表**：arXiv 2026
- **arXiv ID**：2606.05645
- **DOI**：10.48550/arXiv.2606.05645
- **可靠入口**：[论文](https://arxiv.org/abs/2606.05645) · [AlphaXiv](https://alphaxiv.org/abs/2606.05645)
- **类别标签**：RL Post-training, Discrete Vision-Action Tokens, World-Policy Learning
- **证据边界**：沿用知域既有来源报告的论文核验；本专题重新分类，不声称完成独立复现。

- **代表图**：Discrete-WAM 模型架构。来源：[原图](https://arxiv.org/html/2606.05645v2/pic1_v5.png)

![Discrete-WAM architecture](https://arxiv.org/html/2606.05645v2/pic1_v5.png)

### 核心内容与 Insight

Discrete-WAM 认为 continuous world latent 与 continuous action 分处不同表示空间，使 world generation、policy learning、counterfactual reasoning 难以统一。因此它提出：**把 future vision 和 ego action 都离散成 token，在同一个 discrete generative / editing framework 中建模**。这样“换一组 action token 后世界如何变化”天然成为可编辑、可组合的问题。

### Pipeline

- **输入**：camera observations、driving context / ego state / navigation。
- **离散化**：image 转 discrete visual tokens；trajectory/action 转 discrete action tokens；高层行为转 decision token。
- **统一 Transformer 任务**：World Modeling，即 action 到 future vision；World-Policy Modeling，即交错预测 action / vision token；Decision-conditioned Policy，即 decision 到 action trajectory。
- **推理期输出**：先得到 high-level decision，再通过 confidence-guided parallel token editing 迭代 refinement action trajectory。

### 实验与证据

NAVSIM v2 达 90.4 EPDMS；world generation 达 FID 6.6 / FVD 80.0；SFT 89.1，decision-conditioned 90.0，RL post-training 90.4。结论：统一 discrete vision-action space 不只用于视频生成，也能支撑 planning、counterfactual generation 和 RL refinement。

### 代码与数据

截至来源报告核验时，未记录可确认的官方代码、数据或模型入口；这表示开放状态待核验，不代表资源确定不存在。

### 局限、失败案例与开放问题

来源报告未单列可核验的局限、失败案例或开放问题；在补充原论文正文核验前，不对该工作的泛化性、因果性、复现性或 SOTA 结论作扩大解释。

### 与知域的关系

统一离散视觉与动作 token 后再做 RL refinement，把 R1/GRPO 路线从纯视频生成延伸到 world-policy learning。

## 6. Galaxea G0.5: One Autoregressive Stream for Robot Reasoning and Action

- **作者**：Yicheng Liu, Zibin Dong, Baijun Ye, Tianyuan Yuan, Tao Jiang, Anqi Yang, Shicheng Cao, Haonan Liu, Yue Sun, Zihan Guo, Xiao Liu, Ke Dong, Changxun Pan, Chenru Wu, Tailai Cheng, Xiaoshu Ren, Xinlei Zhang, Jianning Cui, Zijie Zhao, Haoyu Zhang, Kaiming Xu, Haodong Yang, Bowen Zhang, Jiahui Niu, Shaoting Zhu, Shiduo Zhang, Hang Zhao
- **年份与发表**：2026，arXiv preprint（v1，cs.RO）；arXiv HTML 署名 Galaxea Team，项目负责 Yicheng Liu，PI Hang Zhao。GitHub 新闻记论文于 2026-08-12 上线。尚无 DOI / 正式出版页。
- **arXiv ID**：2608.11739
- **DOI**：10.48550/arXiv.2608.11739
- **可靠入口**：[论文](https://arxiv.org/abs/2608.11739) · [项目](https://opengalaxea.github.io/G05/) · [代码](https://github.com/OpenGalaxea/GalaxeaVLA) · [模型](https://huggingface.co/OpenGalaxea/G05) · [AlphaXiv](https://alphaxiv.org/abs/2608.11739)
- **类别标签**：GRPO, Robot Policy, Autoregressive VLA, Reasoning and Action
- **证据边界**：沿用知域既有来源报告的论文核验；本专题重新分类，不声称完成独立复现。

- **代表图**：Galaxea G0.5，Fig. 1，reasoning and action in one autoregressive stream。。来源：[原图](https://arxiv.org/html/2608.11739v1/teaser.png)

![Galaxea G0.5 Fig. 1: reasoning and action in one autoregressive stream](https://arxiv.org/html/2608.11739v1/teaser.png)

### 核心内容与 Insight

核心 Insight：**不要把越来越复杂的 action expert 架在被降级的 VLM 上，而应让 VLM 继续做它被预训练成的自回归推理器，同时在同一 token 流里行动。**

方法选择因此改变了三个接口：

1. **动作接口：** 学习式、跨本体的 ActionCodec / RVQ，把异构连续动作压成共享离散词表，并用 active-part tokenization 丢掉空闲控制组。
2. **推理接口：** Subtask / BBox / Trace / ActionHint 四种自描述 CoT 目标与动作码共用 decoder、上下文和 next-token 损失，而不是 bolt-on 规划模块。
3. **记忆接口：** 在 ViT 中插入分解的时空注意力，把数秒视觉历史注入视觉编码器，而不是在 LLM 侧无限堆图像 token。

与本知识库课题的关系：**强相关于机器人 VLA / 通用操作，与 World Action Model 是相邻对照而非同类。** G0.5 主实验把 Fast-WAM、LingBot-VA 等 WAM 当作成功率 baseline，但它本身不生成未来 RGB 世界，也不做 \(do(\cdot)\) 或反事实。可借鉴点是：跨本体动作分词、原生 CoT 与动作共用目标、以及“VLM 应否继续当 actor”这一接口争论。

### Pipeline

- **输入：** 多视角 RGB 短时窗、本体标识 \(e\)、自然语言指令 \(\ell\)、本体感觉 \(s_t\)；可选外部裁剪目标图或坐标 token。
- **过程：** 从 Qwen3.5-2B 初始化；全部序列化为一段 chat：条件段（图像 / 本体 / 任务 / 状态）+ 生成段（可选 CoT + 动作码）。单一 next-token 交叉熵只加在生成段，联合监督 CoT 与动作。动作码经冻结的跨本体 ActionCodec 解码到统一 27 维动作空间：left control 9 + gripper 1 + right control 9 + gripper 1 + lower body 7；空闲槽用 noop。CoT 从 8 种模板中采样（含 no-CoT），评估默认 no-CoT。视觉记忆每四层做分解时空注意力，训练时随机丢掉历史帧；可选附加 \(\pi_{0.5}\) 式 flow-matching 头作推理加速，主文默认仍是 AR。
- **输出：** 结构化离散动作码 → 连续电机指令；需要时同时输出子任务文本、物体框、2D gripper trace、动作提示。

与最近 baseline 的实质差异：相对 \(\pi_{0.5}\) / GR00T，VLM 不是条件编码器而是 actor；相对 OpenVLA / FAST，分词是学习式、按运动部件分组、只预测激活组；相对 ECoT，四种推理原语进入同一共享词表且可按 prompt 开关。预训练是单阶段混合：14 个本体的机器人数据 + web/embodied VQA；DROID 不进 foundation mix，评估时再 post-train。CoT 语言标注来自 Gemini 3 / Doubao 等自动标注，视觉框来自 MLLM + SAM3。

### 实验与证据

**作者主张：** AR 主干在 7 个独立设定上匹配或超过最强 VLM-as-encoder、AR 和 WAM baseline；语言跟随和多阶段执行上优势更结构性。

实验实际支持（数字均来自原文表格/正文）：

- **真机 fine-tune（R1-Lite / R1-Pro，6 个 task–embodiment，各 15 episode，对齐 16×H20 墙钟）：** 平均成功率 **76.7%** vs \(\pi_{0.5}\) 53.3%、GR00T-N1.7 24.4%；process score 129.2 vs 105.2 / 68.9。R1-Pro 搬箱堆叠是例外：\(\pi_{0.5}\) 93.3% vs G0.5 80.0%。
- **2025 BEHAVIOR Challenge（50 长时程家务，单 checkpoint）：** Task Success Score，G0.5 1 epoch **0.2904**、4 epoch **0.3136**；\(\pi_{0.5}\) 4 epoch 0.2626；冠军 RLC 四 checkpoint 0.2605。作者强调这是单策略 vs 多 checkpoint 的不对等对照。
- **DROID post-train 后环境/物体 zero-shot（10 任务×10 trial）：** 平均 **82.5%** vs \(\pi_{0.5}\)-DROID 57.5%、MolmoAct2-DROID 52.0%。抽屉任务上，半透明柜体无高对比标记时 G0.5 仅 60%，贴橙色标记后到 100%；作者承认对低对比半透明表面更敏感。
- **仿真：** LIBERO 平均 **98.9%**（Long 98.6）；RoboTwin 2.0 Clean/Rand/Avg **93.7 / 92.8 / 93.3**；SimplerEnv-Bridge 平均 **87.3%**（部分 baseline 数字编译自既有论文，不是全部同代码重跑）。
- **PP Bench（64 次真机 trial）：** zero-shot 语言跟随 65.6%、任务成功 59.4%；50H post-train 分别为 84.4% / 75.0%，同设置下仍高于 \(\pi_{0.5}\) 的 68.8% / 65.6%。单阶段任务上 CoT 几乎无增益；五阶段 Air Fryer / Cook Bacon 零样本探测中，AR+CoT 的 progress 从 2.4→3.8 与 1.5→3.4。作者把 prompt 措辞能改变 rollout 写成定性探针，**不是**定量结论。
- **GRPO：** 每任务 1 条演示后，AR 比可选 FM 头收敛更快、终值更高、方差更低（Fig. 12）。这支持“AR 提供可直接用的 token log-prob”，不支持“FM 不能做 RL”。

**证据未支持：** 提示词即可零样本控制系统性地调节粒度/时域/OOD；lower-body 被单独评测；AR 消除了感知失败。

### 代码与数据

- **代码：** [OpenGalaxea/GalaxeaVLA](https://github.com/OpenGalaxea/GalaxeaVLA) 含推理、fine-tune、LIBERO / DROID / RoboTwin / R1 部署入口。
- **权重：** Hugging Face `OpenGalaxea/G05` 提供 g05-base、libero、droid、so101、robotwin20 及对应 ActionCodec。
- **许可：** `LICENSE-G0.5` 为 **非商业 + 有限专利** 社区协议；Qwen3.5 另有独立许可。商业用途需另签协议。
- **数据：** 预训练含内部多本体数据与自动标注；完整语料不能仅凭公开 checkpoint 复现。Galaxea Open-World Dataset 另有 HF 条目，但是否覆盖 G0.5 全文预训练 mix 需按数据卡核对。

### 局限、失败案例与开放问题

- 抽屉插入和半透明柜体是作者承认的感知失败，AR 本身不消除。
- 视觉记忆只有数秒；lower-body 在统一动作空间里有槽位，但本文未单独评测。
- 预训练长尾偏 pick-and-place，BEHAVIOR 上微波炉/热狗等容器交互弱于 \(\pi_{0.5}\)。
- Prompt 级动作调节目前只是定性探针，不是系统实验。
- SimplerEnv 部分 baseline 来自文献汇编；BEHAVIOR 对照混有单/多 checkpoint。
- 社区许可禁止商业使用；自动标注 CoT 质量依赖闭源 MLLM。

### 与知域的关系

展示自回归动作 token 可直接提供策略 log-prob，并以 GRPO 做机器人策略优化；属于机器人 R1/GRPO 侧，而非未来 RGB 世界生成模型。
