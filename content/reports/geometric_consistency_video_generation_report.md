# 3D/4D 几何一致性视频生成论文梳理：GeoFlow / VGGRPO / World-R1

> 检索与整理日期：2026-08-18  
> 阅读范围：arXiv 摘要页、arXiv HTML 正文/附录中的方法与实验部分、项目页/代码页。  
> 主题定位：这 3 篇并不是 hand-object interaction 专文，而是 **通用 text-to-video / video generation 的 3D/4D 几何一致性后训练与奖励设计**。它们对 HOI world model 的价值主要在于：几何奖励、4D latent reward、3D foundation model critic、camera consistency、failure diagnosis。

---

## 0. 总体判断

这三篇工作的共同问题是：

> 大规模视频生成模型视觉质量已经很强，但它们仍容易出现 object deformation、texture drift、background wobble、camera jitter、scene layout shift 等几何不一致问题。

共同解决思路是：

- 不从头训练一个显式 3D/4D generator；
- 不一定在推理时加入昂贵 3D 控制模块；
- 而是用 **3D/4D 几何 foundation model + reward / RL post-training**，把几何一致性变成优化目标。

和 hand-object interaction world model 的关系：

- **直接相关性：中等**。三篇都不是手物交互任务，也没有显式 hand/object/contact state。
- **方法价值：高**。如果你做 HOI world model，可以把它们作为 3D/4D consistency reward、camera/scene consistency evaluator、RL alignment 方法参考。
- **关键不足**：它们主要约束“场景几何一致”，尚未解决 HOI 中更核心的 **action -> hand motion -> contact -> object response** 因果链。

---

# 1. GeoFlow: Enforcing Implicit Geometric Consistency in Video Generation

- **作者**：Jan Ackermann, Shengqu Cai, Boyang Deng, Zhengfei Kuang, Songyou Peng, Gordon Wetzstein
- **年份**：2026
- **发表情况**：arXiv preprint，提交日期 2026-05-18
- **可靠链接**：[arXiv](https://arxiv.org/abs/2605.18365) / [Project](https://geometryflow.github.io/) / [Code](https://github.com/geometryflow/GeoFlow) / [Model](https://huggingface.co/ackermannj/geoflow)
- **主题相关度**：**3D/4D 视频几何一致性：强；HOI world model：间接相关**
- **代表图**：GeoFlow，Fig. 2 "GeoFlow method overview"，来源：[项目页](https://geometryflow.github.io/) / arXiv HTML

![GeoFlow Fig. 2: method overview](https://geometryflow.github.io/assets/images/method.png)

## 核心概括 / Insight

作者明确声称的问题：通用 text-to-video diffusion model 在 camera motion 和 object motion 下常出现对象形变、纹理漂移、背景非刚性抖动。GeoFlow 的核心 insight 是：

> 几何一致的视频应满足两类近似条件：静态背景运动应能被相机运动诱导的刚性 flow 解释；独立运动物体沿其运动轨迹应保持语义/外观身份。

因此 GeoFlow 不直接要求有 3D/4D ground truth，而是从生成视频自身出发，用 monocular depth/pose、optical flow、DINO feature correspondence 构造一个 geometry-consistency reward，再用 Flow-GRPO 对 video generator 做 RL fine-tuning。

## Pipeline

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

## 实验概括

作者构建了 110 个 evaluation prompts，覆盖 static/dynamic、simple/complex motion regimes；每个 prompt 用 5 个随机种子采样，共 550 videos/config。训练分辨率 480x832，33 frames；使用 16 张 H100 做 LoRA fine-tuning。

主要 baseline 包括 CogVideoX-1.5、VideoGPA、GeoVideo、VideoRepa、Wan2.1、SFT。评价指标包括：

- **MEt3R**：multi-view / geometric consistency；
- **Sampson distance**：epipolar consistency；
- **Gemini judge**：语义/视觉一致性；
- **VBench**：background consistency、aesthetic quality、temporal flickering、motion smoothness。

实验支持的结论：

- GeoFlow 在 static / dynamic、simple / complex 四类设置下整体降低几何错误。
- 它并非简单提升画质，而是针对几何与时序一致性有针对性改善。
- 消融显示：几何结构奖励与 DINO semantic consistency reward 互补；只做 SFT 不足以稳定提升几何一致性。

## 代码与数据开放情况

- **代码**：GitHub 已公开，包含 sampler、evaluation scripts、reward server、tests、第三方子模块说明。
- **模型**：Hugging Face 发布 GeoFlow LoRA adapter；模型卡显示是基于 `wan-ai/Wan2.1-T2V-1.3B-Diffusers` 的 PEFT LoRA。
- **数据**：论文说明 evaluation prompts 来自 OpenVid-1M / DL3DV 并经 Gemini 标准化；仓库含 `eval_data`，但训练 prompt 全量细节需要以仓库实际发布为准。

## 局限与失败案例

作者在附录和项目页明确提到：

- 对严重拓扑变化不稳，例如大遮挡、打开抽屉露出新内容等，因为 pixel persistence 假设被破坏。
- 快速瞬时错误如果发生在 reward sampling interval 之外，可能无法惩罚。
- RL alignment 受基础模型能力上限约束；若 base model 对 OOD prompt 已经完全混乱，reward 可能过稀疏。
- 静态/动态区域边界模糊时，reward 可能误伤合理动态，例如布料/帐篷摆动。
- 仍可能只部分改善一致性，不能消除所有 artifacts。

## 对 HOI world model 的启发

GeoFlow 适合作为 **HOI 视频生成的几何一致性 reward/evaluator**。但它没有显式建模 hand mesh、object pose、contact、force-like object response。若直接用于手物交互，建议把 reward 从“background rigid + dynamic identity”扩展为：

- hand kinematics consistency；
- hand-object contact timing；
- object pose / shape persistence；
- contact 后 object motion 是否由 hand motion 合理导致。

---

# 2. VGGRPO: Towards World-Consistent Video Generation with 4D Latent Reward

- **作者**：Zhaochong An, Orest Kupyn, Theo Uscidda, Andrea Colaco, Karan Ahuja, Serge Belongie, Mar Gonzalez-Franco, Marta Tintore Gazulla
- **年份**：2026
- **发表情况**：ECCV 2026；arXiv v1 2026-03-27，v2 2026-07-11
- **可靠链接**：[arXiv](https://arxiv.org/abs/2603.26599) / [Project](https://zhaochongan.github.io/projects/VGGRPO/)
- **主题相关度**：**4D latent geometry reward：强；HOI world model：间接相关**
- **代表图**：VGGRPO，Fig. 2 "Method Overview"，来源：[项目页](https://zhaochongan.github.io/projects/VGGRPO/) / arXiv HTML

![VGGRPO Fig. 2: method overview](https://zhaochongan.github.io/projects/VGGRPO/VGGRPO_files/pipeline.png)

## 核心概括 / Insight

VGGRPO 针对的是 RGB-space geometry reward 的成本和鲁棒性问题。作者认为：已有 alignment 方法常在 RGB 解码后再跑几何模型，导致反复 VAE decoding，计算贵；而 RGB-based reward 还容易受生成图像分布偏移影响。

核心 insight：

> 如果 video diffusion latent 已包含足够视觉信息，可以训练一个 Latent Geometry Model，把 diffusion latent 直接接到 4D geometry foundation model，从 latent 中解码 camera pose、depth、point map、scene flow，再在 latent space 做 GRPO reward。

这使几何奖励不必每次回到 RGB pixel space，也能利用 4D reconstruction model 支持 dynamic scenes。

## Pipeline

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

## 实验概括

论文在 static 和 dynamic benchmarks 上比较 baseline、SFT、Epipolar-DPO、VideoGPA 等方法，评价 camera stability、geometry consistency、VBench general quality。作者还做了 latent geometry model 的鲁棒性分析：在 RealEstate10K test sequences 上给 video latent 加扰动，比较 LGM 与 RGB-decoded geometry model 的 camera pose estimation 稳定性。

实验支持的结论：

- VGGRPO 在 static/dynamic scenes 中都改善 camera smoothness、geometry consistency 和整体质量。
- LGM 相比“latent -> RGB -> geometry model”的路径更抗 latent perturbation，说明 latent-space reward 减少了 RGB decoding domain gap。
- 附录中的 VBench 表显示，VGGRPO 相比 baseline / SFT / Epipolar-DPO / VideoGPA 在 subject/background consistency、motion smoothness、image quality 等维度整体更稳。

## 代码与数据开放情况

- **项目页**：提供 arXiv paper 和大量 qualitative comparisons。
- **代码/模型**：截至本次检索，项目页未显示公开 GitHub / model weights 链接；arXiv 摘要页也未声明代码开放。置信度：中等，以作者后续更新为准。
- **数据**：未发现单独开放的训练/评测数据链接；论文使用 RealEstate10K 等 benchmark 做分析。

## 局限与失败案例

论文没有像 GeoFlow 那样集中列出详细 failure cases，但根据方法假设和实验范围，可明确区分：

- **作者明确覆盖**：static + dynamic scene geometry consistency、camera smoothness、latent reward efficiency。
- **实验未充分证明**：对细粒度物理交互、手物接触、物体可操作状态变化的建模能力。
- **潜在局限**：
  - 奖励质量受 LGM 和背后 geometry foundation model 上限影响；
  - 对严重拓扑变化、细粒度非刚性接触、透明/反光物体等可能仍难；
  - 不是 action-conditioned world model，不能直接证明“动作导致世界变化”的因果一致性。

## 对 HOI world model 的启发

VGGRPO 对你方向最有价值的是 **latent 4D reward**。如果你做 hand-object interaction，可以借鉴：

- 不必每次 decode RGB 再算 3D reward；
- 可训练一个 HOI Latent Geometry Model，从 video/action latents 解码 hand pose、object pose、contact map、scene flow；
- 用 latent reward 对 video world model 做 post-training。

换句话说，VGGRPO 是“4D 几何奖励怎么高效算”的参考，而不是 HOI 任务本身的解决方案。

---

# 3. World-R1: Reinforcing 3D Constraints for Text-to-Video Generation

- **作者**：Weijie Wang, Xiaoxuan He, Youping Gu, Yifan Yang, Zeyu Zhang, Yefei He, Yanbo Ding, Xirui Hu, Donny Y. Chen, Zhiyuan He, Yuqing Yang, Bohan Zhuang
- **年份**：2026
- **发表情况**：ICML 2026；arXiv v1 2026-04-27，v4 2026-05-26
- **可靠链接**：[arXiv](https://arxiv.org/abs/2604.24764) / [Project](https://microsoft.github.io/World-R1/) / [Technical Report](https://microsoft.github.io/World-R1/tech.html) / [Code](https://github.com/microsoft/World-R1) / [Dataset](https://huggingface.co/datasets/microsoft/World-R1)
- **主题相关度**：**3D constraints + RL video post-training：强；HOI world model：间接相关**
- **代表图**：World-R1，Fig. 2 / Pipeline Overview，来源：[官方技术页](https://microsoft.github.io/World-R1/tech.html)

![World-R1 Fig. 2: pipeline overview](https://microsoft.github.io/World-R1/assets/pipeline.jpg)

## 核心概括 / Insight

World-R1 的出发点与 GeoFlow/VGGRPO 接近：video foundation model 已有强视觉合成能力，但缺内在 3D 几何约束。它反对在推理时加重型 3D control modules，主张通过 RL 后训练把几何一致性“内化”到模型中。

核心 insight：

> 用 3D foundation model 和 VLM 作为 reward providers，通过 Flow-GRPO 对 text-to-video 模型做后训练，可以在不改架构、不加推理期 3D 模块的情况下强化 3D consistency。

它还引入 implicit camera conditioning：从 text 中解析 camera motion，将轨迹先验写入 initial latent noise，而不是增加额外控制网络。

## Pipeline

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

## 实验概括

数据方面，World-R1 构建 prompt-only world simulation dataset：官方技术页称约 3,000 pure-text prompts，含约 500 high-entropy dynamic prompts；Hugging Face 数据集显示 `final` 和 `enhanced` 两个 config，总计 6,476 rows。

评价包括：

- 3D reconstruction consistency：PSNR / SSIM / LPIPS；
- MVCS：reconstruction-independent multi-view consistency；
- VBench：general video quality；
- user study：几何、控制、整体偏好；
- long-video generalization：121-frame videos；
- scene-complexity breakdown：static、single-object dynamic、multi-object dynamic、non-rigid、long-horizon dynamics。

实验支持的结论：

- World-R1-Small / Large 在 3D consistency benchmark 上显著优于 Wan2.1 / Wan2.2 / CogVideoX 等 baseline。
- 官方技术页报告 World-R1-Large 达 27.67 PSNR / 0.865 SSIM / 0.162 LPIPS；World-R1-Small 相对 Wan2.1-1.3B 有 +10.23 dB PSNR 改善。
- User study 中，World-R1 相对 Wan2.1 在 geometry/control/overall preference 上有优势。
- 121-frame long-video evaluation 中，World-R1-Large 将 PSNR 从 18.32 提升到 26.32。

需要注意：这些实验支持的是 **3D consistency / camera control / visual quality preservation**，不是严格意义上的物理仿真或可交互因果 world model。

## 代码与数据开放情况

- **代码**：GitHub 已公开，MIT license。仓库包含 `flow_grpo`、`reward_server`、`scripts`、`dataset` 等目录，并给出单机/多机训练、reward server、inference 脚本。
- **数据**：Hugging Face `microsoft/World-R1` 已公开 prompt-only dataset，包含 `final` 与 `enhanced` 两个 config。数据卡明确说明不包含生成视频、reward annotations、human preference labels 或 model checkpoints。
- **模型权重**：公开页面主要提供代码和 prompt dataset；是否发布完整 LoRA/model checkpoint 需以官方仓库后续说明为准。

## 局限与失败案例

作者明确指出两点局限：

- RL 用于视频生成仍成本高，因为需要重复 rollout 和 reward evaluation。
- World-R1 受基础视频模型生成能力限制；dense multi-object composition、fine-grained non-rigid motion、detailed hand dynamics、very long-horizon scene evolution 仍可能继承 base model artifacts。

作者还分析了 reward hacking 风险：如果只优化窄 3D metric，模型可能生成 near-static clips 来方便重建但不遵循 camera motion。World-R1 用 composite reward、trajectory term、periodic dynamic-only training 来缓解，但这不等于完全消除。

## 对 HOI world model 的启发

World-R1 特别适合借鉴到 HOI 的后训练框架：

- 用 3D / 4D foundation model 给生成视频打分；
- 加入 camera trajectory / viewpoint consistency reward；
- 用 VLM 评估 novel view 或 meta-view plausibility；
- 通过 periodic dynamic training 避免 reward 过度鼓励“静态化”。

但它对 HOI 最关键的 hand-object contact 没有直接处理。若迁移到 HOI，需要把 reward 改为：

- hand pose / MANO consistency；
- object 6DoF / articulated state consistency；
- contact map / affordance alignment；
- action-conditioned object response；
- first-person camera 与手部运动解耦。

---

# 4. 三篇横向比较

| 维度 | GeoFlow | VGGRPO | World-R1 |
|---|---|---|---|
| 核心目标 | 减少视频几何/时序 artifacts | latent-space 4D geometry reward | 用 RL 强化 T2V 的 3D consistency |
| 是否改模型架构 | 主要 LoRA / RL fine-tune | 构建 LGM；post-training 可不大改生成器 | 不改基础生成架构 |
| 奖励位置 | 生成视频/RGB 后计算 | diffusion latent space 直接计算 | 视频 lifted 到 3DGS 后计算 |
| 几何来源 | Depth Anything 3 + optical flow + DINOv2 | 4D geometry foundation model + LGM | DA3 / 3DGS + Qwen3-VL + HPSv3 |
| 是否支持 dynamic scenes | 支持，但依赖 static/dynamic 分解假设 | 强调支持 dynamic 4D | 支持动态 prompt，但仍受 base model 限制 |
| 是否 action-conditioned | 否 | 否 | 否 |
| 是否 HOI 专用 | 否 | 否 | 否 |
| 代码开放 | 是 | 暂未发现 | 是 |
| 数据开放 | eval/prompt 相关内容部分可见 | 暂未发现 | prompt-only dataset 开放 |

---

# 5. 对“2D 视频 + 3D/4D HOI world model”的启发

这三篇论文的共同启发不是“直接拿来做 hand-object interaction”，而是给 HOI world model 提供一套后训练思想：

## A. 3D/4D consistency reward 可以不需要真实 3D GT

GeoFlow 和 World-R1 都说明，可以用 pretrained depth / 3D foundation models 从生成视频本身构造 reward。对 HOI 来说，这意味着可以用：

- HaMeR / MANO / WHAM 类 hand/body estimator；
- VGGT / DA3 / DynamicVGGT 类 geometry estimator；
- SAM2 / tracking / optical flow；
- object pose estimator / point tracker；

构造弱监督的 hand-object-world consistency reward。

## B. HOI 不能只奖励“场景几何一致”

对通用 T2V，背景不抖、物体不变形已经很关键。对 HOI，真正难的是：

> action -> hand motion -> contact -> object response

所以需要额外评估：

- 手是否按 action/control 运动；
- 接触是否发生在合理 affordance region；
- 物体是否在接触之后而不是之前响应；
- 物体运动是否与手的方向、速度、接触点一致；
- 相机运动和手部运动是否解耦。

## C. Latent reward 对 HOI 很有潜力

VGGRPO 的 LGM 很适合改成 HOI-LGM：从 video/action latent 直接预测 hand pose、object pose、scene flow、contact map。这样可以避免每次 decode RGB 再跑 3D estimator，训练效率会高很多。

## D. 需要警惕 reward hacking

World-R1 的 reward hacking 分析对 HOI 尤其重要。若只奖励 3D 重建一致，模型可能学会生成“更静态、更少接触、更少物体运动”的视频。HOI reward 必须同时包含：

- contact/action completion；
- dynamic degree；
- object displacement correctness；
- visual quality；
- 3D consistency。

---

# 6. 额外推荐的相关工作

> 检索日期：2026-08-18。以下推荐用于补全脉络，不替代对三篇主论文的阅读。

## World-consistent Video Diffusion with Explicit 3D Modeling (WVD)

- **发表情况**：CVPR 2025 Highlight
- **链接**：[CVF](https://openaccess.thecvf.com/content/CVPR2025/html/Zhang_World-consistent_Video_Diffusion_with_Explicit_3D_Modeling_CVPR_2025_paper.html) / [Project](https://zqh0253.github.io/wvd/)
- **推荐理由**：它不是 reward alignment，而是显式联合生成 RGB + XYZ / NCS frames，是“2D video + explicit 3D modeling”的代表性工作。适合作为 GeoFlow/VGGRPO/World-R1 的前置脉络。

## Geometry Forcing: Marrying Video Diffusion and 3D Representation for Consistent World Modeling

- **发表情况**：ICLR 2026；arXiv 2025
- **链接**：[arXiv](https://arxiv.org/abs/2507.07982)
- **推荐理由**：将 video diffusion intermediate features 与 VGGT 等 geometric representation 对齐，强调 training-time geometry alignment。和 GeoFlow/World-R1 的 RL reward 路线互补。

## VideoGPA: Distilling Geometry Priors for 3D-Consistent Video Generation

- **发表情况**：arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2601.23286) / [Project](https://hongyang-du.github.io/VideoGPA-Website/) / [Code](https://github.com/Hongyang-Du/VideoGPA)
- **推荐理由**：使用 geometry foundation model 自动构造 preference pairs，再用 DPO 做 3D consistency alignment。它是 GeoFlow/VGGRPO 重要 baseline，也代表“preference alignment for geometry”的路线。

## GeCo: Evaluating Geometric Consistency for Video Generation via Motion and Structure

- **链接**：[Project](https://geco-geoconsistency.github.io/)
- **推荐理由**：更偏 metric / benchmark。用 residual motion 和 depth reprojection error 检测 deformation 与 occlusion inconsistency。适合做 HOI world model 的几何评估模块参考。

## VMem: Consistent Interactive Video Scene Generation with Surfel-Indexed View Memory

- **发表情况**：ICCV 2025 Highlight
- **链接**：[Project](https://v-mem.github.io/)
- **推荐理由**：用 surfel-indexed view memory 支持长程 interactive scene generation。它不解决手物交互，但对“persistent 3D memory / revisiting consistency”非常有启发。

## WorldMem: Long-term Consistent World Simulation with Memory

- **链接**：[arXiv](https://arxiv.org/abs/2504.12369) / [Project](https://spmem.github.io/)
- **推荐理由**：关注长期空间记忆，解决 autoregressive video world model 在重访场景时遗忘的问题。对 HOI 的多阶段操作、场景状态持续更新有参考价值。

---

# 7. 给 hand-object interaction 方向的落点

如果要把这组工作转化成你的研究方向，我建议这样表述：

> GeoFlow、VGGRPO、World-R1 说明，通用视频模型可以通过 3D/4D geometry reward 和 RL post-training 获得更强世界一致性。但它们仍主要解决 camera/scene geometry consistency，不处理 hand-object interaction 的接触因果。因此我的方向可以是：面向 egocentric hand-object interaction，构建 3D/4D-grounded video world model，用 hand pose、object pose、scene flow、contact map 和 camera trajectory 组成 HOI-specific latent reward，使模型不仅保持几何一致，还能学习 action -> contact -> object response 的动态关系。

可以对应三个技术问题：

1. **HOI-Latent Geometry Model**：从 video/action latents 解码 hand pose、object state、contact、scene flow。
2. **HOI-specific Reward**：奖励 hand kinematics、contact timing、object response、camera consistency，而不只是背景稳定。
3. **Scalable Pseudo-4D Data**：用 2D ego videos 自动抽取 depth、flow、hand mesh、object tracks、contact regions，避免依赖昂贵 4D 标注。

