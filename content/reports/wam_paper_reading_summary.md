# World Action Model / Predictive Representation 论文梳理

> 说明：本文按“标题、发表情况、链接、核心概括 / Insight、Pipeline、实验概括、代表图”的标准整理。内容依据原论文 arXiv / CVF 页面和论文 HTML 图表信息重写。图片使用论文 HTML 中的原图链接；若 Markdown 预览器不显示远程图片，可点击论文链接查看。

## 总览

这批论文高度集中在一个主题：**World Action Model (WAM) 正在从“推理时生成未来 RGB 视频”，转向“用未来预测训练 action-relevant predictive representation”。**

可以粗分为四类：

- **Structured Future Supervision**：MECo-WAM、GeoSem-WAM、DreamWAM、GWM-VLA。
- **Inference-Efficient / No-Rollout WAM**：Efficient-WAM、SG-WAM、GigaWorld-Policy-0.5、SLIM、Vid2WAM。
- **Representation / Tokenizer 重设计**：EmbodiedVAE、Discrete-WAM、SLIM。
- **4D Geometry 与评测诊断**：DynamicVGGT、WorldSimProbe。

---

## 1. Learning 4D Geometric Priors for Inference-Efficient World Action Models

- **方法名**：MECo-WAM
- **发表情况**：arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2607.05468)
- **代表图**：MECo-WAM 训练/推理总览

![MECo-WAM overview](https://arxiv.org/html/2607.05468v1/overview.png)

**核心概括 / Insight**  
传统 WAM 用 future RGB / video prediction 为 action 学习提供密集监督，但 video latent 更偏 appearance，不一定显式编码 manipulation 所需的时变 3D / 4D geometry。MECo-WAM 的关键观点是：**4D geometry 不必成为推理阶段的输入或输出，更适合作为 training-time representation constraint**，把几何知识蒸馏进最终部署的 video-action representation。

**Pipeline**

- **输入**：当前 RGB observation、proprioception、language instruction。
- **训练期**：Video Expert 预测 future video latent；Action Expert 预测 future action chunk；额外 4D Expert 使用 frozen VGGT 提取 current/future geometry feature；Decayed 4D Read-Mask 早期允许有限读取当前几何，随后逐渐关闭；Action-Aware Temporal Geometric Distillation 对齐几何关系及其时间变化，并强调 action-relevant region。
- **推理期输出**：直接输出 action chunk；VGGT、4D Expert、alignment module 全部删除。

**实验概括**  
LIBERO 平均成功率 98.2%，RoboTwin 2.0 达 92.6%，真机任务减少 correction、缩短完成时间。实验说明：单独挂 geometry branch 帮助有限，关键在于把 4D knowledge 迁移进部署时仍保留的 policy representation。

---

## 2. Efficient-WAM: A 1B-Parameter World-Action Model with Low-Cost Future Imagination

- **发表情况**：arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2606.10040)
- **代表图**：Efficient-WAM 架构

![Efficient-WAM architecture](https://arxiv.org/html/2606.10040v2/architecture.png)

**核心概括 / Insight**  
Efficient-WAM 直接挑战一个默认假设：**control 是否真的需要 photorealistic future video？** 作者认为 action 主要需要物体运动、接触、空间变化等 dynamics cue，而不是纹理、光照等视觉细节。因此 future prediction 应被看作 action guidance signal，而不是 video generation task 本身。

**Pipeline**

- **输入**：当前 observation、language、robot state。
- **过程**：从 WAN2.2-5B 蒸馏/压缩 Compact Video Expert 到约 1B；使用 sparse / low-resolution video tokens；video 分支使用比 action 分支更少的 denoising steps；训练分为 video dynamics 蒸馏、冻结 video expert 训练 action expert、video/action 联合 refinement。
- **输出**：future latent + action chunk；部署时实现低延迟 action generation。

**实验概括**  
RoboTwin 2.0 上 1B Efficient-WAM 达 86.7% clean / 85.7% random；真机 Efficient-WAM-RT 平均 66.25%，接近或超过更重模型。每 action chunk 约 98 ms，显著快于传统重型 WAM。结论：低分辨率、低成本、少步 future imagination 已足以提供有效 dynamics supervision。

---

## 3. GeoSem-WAM: Geometry- and Semantic-Aware World Action Models

- **发表情况**：arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2606.03188)
- **代表图**：GeoSem-WAM 架构

![GeoSem-WAM architecture](https://arxiv.org/html/2606.03188v1/figures/architecture.png)

**核心概括 / Insight**  
GeoSem-WAM 关注 WAM 收益究竟来自 test-time imagination，还是 predictive training 学到的 representation。论文倾向后者，并进一步指出：如果 future prediction 主要是 representation learning objective，那么 RGB 不应是唯一监督，应该显式加入 **geometry + semantics**。

**Pipeline**

- **输入**：RGB observation、language、action trajectory。
- **训练期监督**：future RGB、future geometry、future semantic segmentation、future action。
- **实现方式**：基于 Wan2.2-5B + Action DiT；geometry / semantic 使用 DPT-style auxiliary heads，从 VideoDiT 中间 feature 解码。
- **推理期输出**：只输入当前 observation，single forward 直接预测 action；不生成 future video，geometry / semantic heads 删除。

**实验概括**  
LIBERO ablation 中，RGB-only 97.6，加入 Geometry 为 98.2，加入 Semantic 为 98.1，Geometry + Semantic 为 98.6。真机平均成功率从 Fast-WAM 的 88.9 提升到 95.4。结论：geometry 和 semantic 是互补的 structured supervision；future modeling 的价值主要在训练期塑造 representation。

---

## 4. SG-WAM: Self-Guided World Modeling in Geometry-Aware Policy Space

- **发表情况**：arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2608.01397)
- **代表图**：SG-WAM 框架

![SG-WAM overview](https://arxiv.org/html/2608.01397v1/overview.png)

**核心概括 / Insight**  
SG-WAM 认为好的 future latent 必须同时满足两点：与 policy/action representation 对齐，并包含足够 geometry。外部 V-JEPA / VGGT latent 虽然强，但未必 policy-aligned；RGB 又太重。因此它提出：**直接在 policy 自己的 representation space 中预测 future，并用 geometry teacher 塑造该 policy space**。

**Pipeline**

- **输入**：当前 visual observation、language。
- **过程**：Qwen3.5-based policy 内部引入 learnable Dynamics Tokens；SGWP 根据当前 dynamics tokens 与 intervening action 预测 future dynamics tokens；future target 来自同一 policy 的 EMA copy；frozen VGGT 对 visual tokens 施加 geometry supervision；Action Expert 用 flow matching 输出 action。
- **推理期输出**：EMA target、VGGT、SGWP 全部删除，只保留 policy 到 action。

**实验概括**  
仅 0.9B、无大规模 embodied pretraining，LIBERO 达 98.5%，LIBERO-Plus 达 73.0%。UR5e 真机 Pick&Place、Towel Folding、Toolbox Organization 中，ID 和背景、光照、新物体 OOD 均优于 VPP、VLA-JEPA。结论：future representation 与 policy 使用同一 representation family 很重要，geometry grounding 防止 latent dynamics 只学习 appearance correlation。

---

## 5. DynamicVGGT: Learning Dynamic Point Maps for 4D Scene Reconstruction in Autonomous Driving

- **发表情况**：CVPR 2026
- **链接**：[CVF Open Access](https://openaccess.thecvf.com/content/CVPR2026/html/He_DynamicVGGT_Learning_Dynamic_Point_Maps_for_4D_Scene_Reconstruction_in_CVPR_2026_paper.html) / [arXiv](https://arxiv.org/abs/2603.08254)
- **定位**：不是 WAM / policy，而是 feed-forward 4D reconstruction。
- **代表图**：DynamicVGGT 训练框架

![DynamicVGGT pipeline](https://arxiv.org/html/2603.08254v1/totalpipelinev4.png)

**核心概括 / Insight**  
VGGT 擅长 static 3D reconstruction，但 dynamic scene 的关键不是独立重建每一帧，而是在统一坐标表示中显式建模 point 随时间如何运动。DynamicVGGT 将 static point map 扩展为 **Dynamic Point Map (DPM)**，同时学习 implicit temporal correspondence 和 explicit motion。

**Pipeline**

- **输入**：时间序列 monocular / multi-camera images。
- **过程**：VGGT backbone 提取 geometry；Motion-aware Temporal Attention 建模时序；Future Point Head 预测 current/future point maps，并在统一 reference 中通过差值得到 implicit motion；Dynamic Gaussian Head 将 points 转为 3D Gaussians，并用 motion tokens 预测 Gaussian velocity，受 scene-flow supervision 约束。
- **输出**：dynamic point maps、dynamic 3D Gaussians / velocities，可用于 4D reconstruction / rendering。

**实验概括**  
在 KITTI、Waymo 上评估 point-map reconstruction 和 4D scene reconstruction。Waymo dynamic regions 达到 18.07 PSNR / 0.376 SSIM，full frame 为 24.07 / 0.676。结论：VGGT 的 feed-forward geometry prior 可以从 static 3D 扩展到 dynamic 4D，关键是把 temporal point correspondence 与 explicit scene motion 纳入统一几何表示。

---

## 6. DreamWAM: Beyond RGB Future Prediction for World Action Models

- **发表情况**：arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2608.04996)
- **代表图**：DreamWAM 框架

![DreamWAM overview](https://arxiv.org/html/2608.04996v1/DreamWAM.png)

**核心概括 / Insight**  
DreamWAM 对 RGB foresight 的批判更彻底：RGB future 混合了 action-relevant dynamics 与 texture、background、lighting、viewpoint 等 nuisance factors。因此 WAM 应预测的不是“未来长什么样”，而是未来有哪些对 action 有意义的状态变化。它将 future 拆为 **appearance + motion + geometry + semantics**。

**Pipeline**

- **输入**：当前 RGB observation、language、action trajectory。
- **训练 future targets**：RGB 使用 Wan VAE latent；Motion 使用 RAFT optical flow 后接 VAE；Geometry 使用 Depth Anything V3 feature；Semantic 使用 DINOv2 feature。
- **建模方式**：RGB + optical flow 做 joint latent denoising；geometry / semantic 通过 gated residual branches 注入 VideoDiT；VideoDiT 与 ActionDiT shared attention。
- **推理期输出**：beyond-RGB branches 删除；支持 no-rollout 当前帧到 action，也支持 joint RGB future + action 联合生成。

**实验概括**  
LIBERO-Plus no-rollout 从 Fast-WAM 51.36 提升到 63.44，joint rollout 从 69.16 提升到 75.47；真机 unseen visual perturbation 从 55.6 提升到 74.4。关键证据是 no-rollout 也显著提升，说明 beyond-RGB future 的主要价值在训练期塑造 action representation，而不只是 test-time imagination。

---

## 7. GigaWorld-Policy-0.5: A Faster and Stronger WAM Empowered by AutoResearch

- **发表情况**：arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2607.13960) / [Project](https://open-gigaai.github.io)
- **代表图**：GigaWorld-Policy-0.5 框架

![GigaWorld-Policy-0.5 framework](https://arxiv.org/html/2607.13960v3/framework.png)

**核心概括 / Insight**  
延续 GigaWorld-Policy 的 Action-Centered World Modeling：future RGB 是 action 的密集监督，但不应成为 action 推理时的前置依赖。核心是让 **Action -> Future RGB**，而不是让 action 依赖 future RGB；训练获得 dense video supervision，推理可完全关闭 video generation。

**Pipeline**

- **输入**：left / front / right cameras、proprioception、language；三视角先 compose 成一张 image。
- **训练期**：Visual Expert 预测 future visual observations；Action Expert 预测 action chunk；causal attention mask 允许 future visual 读取 action，但 action 不能读取 future visual；混合 AC-WM + WAM pretraining；MoT 分离大 Visual Expert 与小 Action Expert；AutoResearch 自动搜索 LR、warmup 等配置。
- **推理期输出**：关闭 future visual tokens，只运行 action pathway。

**实验概括**  
Fruit Picking 平均 graded SR 0.85；三个 long-horizon task 平均成功率 0.77，优于约 0.47-0.57 的基线；mixed AC-WM + WAM pretraining 收敛更快、最终性能更高；本地 RTX 4090 上 action inference 约 85 ms。结论：video prediction 最合理的角色可以是 action 的训练监督者，而不是推理计算前置条件。

---

## 8. Discrete-WAM: Unified Discrete Vision-Action Token Editing for World-Policy Learning

- **发表情况**：arXiv 2026
- **任务领域**：自动驾驶
- **链接**：[arXiv](https://arxiv.org/abs/2606.05645)
- **代表图**：Discrete-WAM 模型架构

![Discrete-WAM architecture](https://arxiv.org/html/2606.05645v2/pic1_v5.png)

**核心概括 / Insight**  
Discrete-WAM 认为 continuous world latent 与 continuous action 分处不同表示空间，使 world generation、policy learning、counterfactual reasoning 难以统一。因此它提出：**把 future vision 和 ego action 都离散成 token，在同一个 discrete generative / editing framework 中建模**。这样“换一组 action token 后世界如何变化”天然成为可编辑、可组合的问题。

**Pipeline**

- **输入**：camera observations、driving context / ego state / navigation。
- **离散化**：image 转 discrete visual tokens；trajectory/action 转 discrete action tokens；高层行为转 decision token。
- **统一 Transformer 任务**：World Modeling，即 action 到 future vision；World-Policy Modeling，即交错预测 action / vision token；Decision-conditioned Policy，即 decision 到 action trajectory。
- **推理期输出**：先得到 high-level decision，再通过 confidence-guided parallel token editing 迭代 refinement action trajectory。

**实验概括**  
NAVSIM v2 达 90.4 EPDMS；world generation 达 FID 6.6 / FVD 80.0；SFT 89.1，decision-conditioned 90.0，RL post-training 90.4。结论：统一 discrete vision-action space 不只用于视频生成，也能支撑 planning、counterfactual generation 和 RL refinement。

---

## 9. EmbodiedVAE: Disentangled Video VAE for Efficient and Controllable Embodied Manipulation

- **发表情况**：ECCV 2026；arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2608.02990)
- **代表图**：EmbodiedVAE 架构

![EmbodiedVAE framework](https://arxiv.org/html/2608.02990v1/framework.png)

**核心概括 / Insight**  
EmbodiedVAE 关注更底层的 tokenizer / VAE 问题：WAM 常用 Video VAE 原本面向 natural video，其 latent 未必适合机器人。机器人视频具有明显结构：robot arm 运动丰富、需要 controllability；environment/background 时序冗余大。因此不应对整段视频使用统一 compression rate，而应做 **robot / environment disentanglement + asymmetric compression**。

**Pipeline**

- **输入**：robot manipulation video；arm mask 仅训练时使用。
- **结构**：双 Encoder + 单 Decoder。Arm Encoder 使用较弱 temporal compression 以保留 motion；Environment Encoder 使用更强 temporal compression 以压缩静态背景；OT-based motion consistency 约束 arm latent 跨帧 correspondence；Unified Decoder 合并两种 latent 重建完整视频。
- **输出**：更紧凑、可控的 embodied video latent，可供下游 action-conditioned world model 使用。

**实验概括**  
约 100 万机器人 manipulation videos 训练；compression rate 仅 0.39%；Agibot-2025 reconstruction PSNR 31.67；在 IRASim-L action-conditioned generation 中，同样 0.39% latent 下取得最优或接近最优 reconstruction / generation 指标。消融显示去掉 mask 或 OT motion loss 后 reconstruction 和 manipulation generation 均下降。结论：WAM efficiency 不只来自 DiT 压缩，embodied-specific tokenizer / VAE 本身也是关键方向。

---

## 10. SLIM-0.5B: Learning Action-Grounded Predictive Latents for Robot Manipulation

- **发表情况**：arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2608.09771)
- **代表图**：action-grounded masked trajectory prediction

![SLIM masked trajectory prediction](https://arxiv.org/html/2608.09771v1/IDM_FDM.png)

**核心概括 / Insight**  
SLIM 同时质疑 VLA 与 WAM：大 VLM 中许多容量用于 open-domain semantics，pixel-level WAM 又花大量计算预测 control-irrelevant details。作者认为 manipulation 真正需要的是一个紧凑的 observation-action-transition latent space。关键是 predictive latent 必须 **action-grounded**：既能由 action 推断 future，也能从 state transition 反推出 action。

**Pipeline**

- **输入**：current observation latent、future observation latent、proprioception、action tokens、language。
- **Stage 1**：Masked Trajectory Prediction，包括 inverse dynamics grounding：current latent + future latent 重建 action；forward dynamics grounding：current latent + action 预测 future latent。future target 来自 EMA encoder，防止 latent collapse。
- **Stage 2**：current observation + proprioception + language 通过 flow matching 输出 action chunk。
- **推理期输出**：不显式预测 future observation，直接生成 action chunk。

**实验概括**  
0.47B MoT，无额外 embodied pretraining；LIBERO 97.5，LIBERO-Plus 77.45，CALVIN ABC->D 平均 sequence length 4.556/5。真机 5 tasks / 750 demos 中，多数 nominal / distractor / lighting 设置表现最好；极端 background shift 下略低于 pi_0.5，但显著高于 Fast-WAM。结论：不需要 RGB foresight，也不一定需要大 VLM；action-grounded predictive latent 本身可以成为 compact policy backbone。

---

## 11. WorldSimProbe: Diagnosing Simulator Faithfulness in Action-Conditioned World Models for Embodied Manipulation

- **发表情况**：arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2608.09298) / [Code & Data](https://evophys.com)
- **定位**：Benchmark / diagnosis，不是新 WAM policy。
- **代表图**：WorldSimProbe 操作化评测框架

![WorldSimProbe operational diagram](https://arxiv.org/html/2608.09298v1/operational_diagram.png)

**核心概括 / Insight**  
WorldSimProbe 指出现有 world model benchmark 的核心问题：生成视频看起来合理、task outcome 正确，并不代表模型真的执行了给定 action。例如机器人动作没有按 action 走，但物体却“自己”到了目标位置，传统 video metric 仍可能给高分。因此它提出 **Observable Simulator Contract**：supplied action 必须导致对应 robot motion；environment response 必须由实际 motion/contact 导致。

**Pipeline / Benchmark**

- **输入**：当前状态 x_t 与 action sequence a_{t:t+H}。
- **被测对象**：ACWM 输出 future rollout。
- **五组测试**：Local Action Calibration；Global Trajectory Coverage；Action-Source Behavior Preservation；Interaction Grounding；Interaction Dynamics。
- **覆盖范围**：RoboTwin、ManiSkill、LIBERO，约 18K+ instances，测试 6 个开源 ACWM。

**实验概括**  
发现 action trajectory 越偏离训练 task distribution，6 个模型的 action-realization fidelity 普遍越差；trajectory mismatch 与 fidelity 平均 Spearman rho 为 -0.433；存在大量 false contact、unsupported interaction、inconsistent dynamics；普通 VLM 对 OOD action-following 判断过于乐观。WorldSimProbe 指标与人工判断及 downstream synthetic rollout policy performance 更一致。结论：world model 是否像真实 simulator，不能只看 FVD、视觉合理性或最终 task success，必须检查 action -> motion -> interaction -> environment response 的因果链。

---

## 12. GWM-VLA: Geometry-Aware Latent World Modeling for Vision-Language-Action Learning

- **发表情况**：arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2608.07619)
- **代表图**：GWM-VLA 架构

![GWM-VLA architecture](https://arxiv.org/html/2608.07619v1/architecture.png)

**核心概括 / Insight**  
GWM-VLA 针对 VLA-JEPA 类 latent world model 的问题：多相机分别编码再 concat，虽然能预测 future latent，但跨视角 geometry relationship 没有被显式编码。它使用 **VGGT-Omega jointly encode multi-view**，把带 cross-view geometry 的 representation 直接作为 world-model state。

**Pipeline**

- **输入**：multi-view images、language、proprioception。
- **过程**：Frozen VGGT-Omega 联合同一 timestep 所有视角，得到 geometry-aware multi-view state；不预测完整 multi-view future，只预测 target wrist-view patch tokens；wrist-view register tokens 提供 global geometric context；Qwen3-VL-2B 产生 latent-action tokens；同一组 latent-action 同时 condition latent world model 与 flow-matching action head。
- **推理期输出**：current observations -> latent action -> continuous action chunk；world-model loss 只是训练辅助目标。

**实验概括**  
LIBERO 97.1%，LIBERO-Plus 76.9%，相比 robot-only VLA-JEPA 的 62.9% 提升 14.0 points。SO-101 真机少量数据实验中，对 novel layout 很强；但 held-out object-receptacle composition 上 GWM-VLA 53.3%，低于 pi_0.5 的 60%。结论：显式 multi-view geometry 对视觉变化、相机变化、layout OOD 尤其有效，但它解决的是 spatial robustness，不等价于更强 semantic compositional generalization。

---

## 13. Vid2WAM: Distilling Video Diffusion Priors into World Action Models

- **发表情况**：arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2608.08558) / [Project](https://qch-fa.github.io)
- **代表图**：Vid2WAM 蒸馏框架

![Vid2WAM method](https://arxiv.org/html/2608.08558v1/method.png)

**核心概括 / Insight**  
Vid2WAM 进一步追问：WAM 的 future supervision 是否一定要来自昂贵的 target-task robot expert trajectories？大型 video diffusion model 已经包含大量 world / dynamics prior。Vid2WAM 让 video foundation model 离线“想象 future”，再用 inverse dynamics model 把 visual transition 翻译成 embodiment-specific pseudo action，最后蒸馏给小 WAM。核心是 **world knowledge acquisition 与 robot expert collection 解耦**。

**Pipeline**

- **离线输入**：当前 observation + language instruction。
- **过程**：large video diffusion teacher 生成 task-conditioned future rollout；future rollout 直接监督 student future-video branch；同一 rollout 输入 IDM 得到 pseudo action；real demos + synthetic rollout 联合训练 student；Source-Aware Residual Action Adapter 分离 real / pseudo action distribution，降低 noisy IDM action 干扰。
- **推理期输出**：video teacher + IDM 全部删除，只保留 compact WAM student。

**实验概括**  
RoboTwin novel subset：Vid2WAM 54.7 clean / 55.3 random，Fast-WAM 为 45.0 / 42.8。LIBERO low-data robustness average：Fast-WAM 33.6，Vid2WAM 39.0。真机 3 个完全没有 real expert trajectory 的 novel tasks 上取得非零成功率，并优于或匹配 VLA/WAM baselines。消融显示 future latent supervision 单独有效，pseudo action 进一步提供互补收益；在线直接组合 teacher + IDM 反而更差。结论：大型 video model 最有价值的角色未必是部署时在线 rollout，而可以作为离线 world-dynamics teacher。

---

# 横向脉络与趋势

## A. Future Prediction 的角色被重新定义

早期 WAM 直觉是“先想象未来 RGB，再据此行动”。这批工作普遍把 future prediction 改写为训练期 representation learning objective：

- MECo-WAM：4D geometry 只做训练期约束，推理删除。
- GeoSem-WAM / DreamWAM：future 不只 RGB，而是 geometry、semantic、motion 等结构化状态。
- GigaWorld-Policy-0.5 / SG-WAM / SLIM：推理时不 rollout future，只保留 action pathway。
- Vid2WAM：future 甚至可以来自外部 video diffusion teacher，用于离线蒸馏。

**趋势判断**：WAM 的核心竞争点不再是“生成多像真的视频”，而是“训练出多 action-relevant 的 predictive latent”。

## B. RGB Future 被认为信息过重，Structured Supervision 变成主线

RGB 同时包含任务相关状态变化与大量干扰因素。MECo-WAM、GeoSem-WAM、DreamWAM、GWM-VLA 都在往结构化监督走：

- geometry：深度、点云、4D 几何、cross-view 几何。
- semantics：DINOv2 / semantic segmentation 类 feature。
- motion：optical flow、dynamic point map、scene flow。
- policy-space future：让 future target 与 policy representation 同源。

**趋势判断**：未来 WAM 很可能会从“video latent model”演化为“multi-view / multi-modal state transition model”。

## C. 推理效率成为硬约束

Efficient-WAM、GigaWorld-Policy-0.5、SG-WAM、SLIM 都强调低延迟、少参数、无推理期 world branch。机器人控制不是离线视频生成，部署时要闭环、稳定、低 latency。

**趋势判断**：推理时显式生成 future video 会越来越像训练/诊断工具，而不是主流部署路径。

## D. Representation 本身开始被重做

EmbodiedVAE 从 tokenizer / VAE 层面重做 embodied latent；Discrete-WAM 把视觉和动作都离散化，统一编辑；SLIM 直接学习 observation-action-transition latent，不走 RGB foresight。

**趋势判断**：WAM 的瓶颈不只在 DiT 或 policy head，而在“什么 latent 最适合 action”。Embodied-specific VAE、离散 vision-action token、action-grounded latent 会成为重要分支。

## E. 评测从“像不像”转向“因果对不对”

WorldSimProbe 强调 action-conditioned world model 必须满足 simulator contract：action 要导致 robot motion，motion/contact 要导致 environment response。它补上了现有 FVD、task success、VLM judge 的盲区。

**趋势判断**：未来 ACWM / WAM 评测会更关注 action fidelity、contact grounding、interaction dynamics，而不是只看视频质量。

## 总结

这 13 篇论文共同指向一个清晰变化：

> **World Action Model 正从“推理时生成未来视频的模型”，转向“用结构化未来监督学习动作相关世界表征的模型”。**

更凝练地说：

- 训练期：可以大胆使用 video、geometry、semantics、motion、4D teacher、video diffusion teacher。
- 推理期：尽量删除 auxiliary branch，只保留快速 action pathway。
- 表征目标：不是 photorealistic future，而是 action-grounded、geometry-aware、causally faithful 的 predictive latent。

后续建议重点跟踪关键词：**structured future supervision、no-rollout WAM、action-grounded predictive latent、embodied tokenizer、simulator faithfulness**。
