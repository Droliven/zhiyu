# Hand-Object Interaction World Model：2D 视频结合 3D/4D 的最新工作梳理

> 检索日期：2026-08-15  
> 关注方向：egocentric hand-object interaction world model，尤其是 **2D 视频生成 + 3D/4D 几何、手部动作、相机运动、物体状态、接触动力学** 的结合。  
> 说明：很多最新工作标题里都写 world model / egocentric interaction，但实际 3D/4D grounding 强度差异很大。因此本文先做分级，再逐篇介绍。

## 0. 先给结论

如果你的目标是往 **hand-object interaction world model，2D video + 3D/4D** 方向走，我建议优先关注这几条线：

1. **强相关主线：3D/4D-grounded egocentric HOI world model**
   - HandsOnWorld
   - Hand2World
   - EgoHOI
   - EgoSim
   - Dexterous World Models
   - DexWM
   - EgoGrasp

2. **中等相关：2D 视频生成 + contact/depth/structure 等弱 3D/2.5D 监督**
   - SCAR / Open-world HOI Video Generation
   - MEgoHand
   - VideoAfford

3. **外围相关：3D/4D HOI motion prior 或 4D geometry prior，不是直接 video world model**
   - HO-Flow
   - OpenHOI
   - DynamicVGGT

4. **不建议作为核心对标但可放 related work 的偏 2D 方法**
   - InterDyn、CosHand、Mask2IV、Wan2.1-Control 等。这些多用 2D mask / video control，缺少显式 3D/4D hand-object-world state。

一句话判断：

> 现在真正值得做的 gap 不是“再做一个手控视频生成器”，而是 **让 egocentric HOI video generation 具有显式 3D/4D state：hand geometry、camera geometry、object pose/state、contact、scene memory，并能随 action 更新。**

---

# 1. HandsOnWorld: Unconstrained Egocentric Video Generation with Camera-Disentangled Hand Control

- **作者**：Yushuo Chen, Xiaoyu Shi, Xiaoshi Wu, Xintao Wang, Pengfei Wan, Yebin Liu
- **发表情况**：arXiv 2026；v2 更新于 2026-08-13
- **链接**：[arXiv](https://arxiv.org/abs/2607.02075)
- **3D/4D 相关度**：**强 3D hand + camera geometry，但 object 3D/4D state 较弱**
- **代表图**：HandsOnWorld 生成示例

![HandsOnWorld](https://arxiv.org/html/2607.02075v2/showcases.png)

**核心概括 / Insight**  
HandsOnWorld 解决的是 unconstrained monocular egocentric video 下的 hand-controlled generation。关键 insight 是：实验室多视角/动捕数据太窄，真实 ego video 又缺干净 3D hand annotation；因此它构建 EgoVid-Pro，用 protagonist-centered annotation pipeline 从大规模单目视频中过滤出干净 3D hand trajectories。另一个关键点是 **Pluecker Hand Map**：把手部表面也放进与相机同一世界坐标下的 Pluecker-style representation，缓解 camera motion 和 hand motion 的纠缠。

**Pipeline**

- **输入**：首帧图像、目标 3D camera trajectory、目标 3D hand trajectory。
- **过程**：从 EgoVid-5M 中筛选出动作语义、图像质量、3D 几何都可靠的 EgoVid-Pro；用 Pluecker Hand Map 表达 3D-aware hand control；训练 egocentric video generator。
- **输出**：手部动作可控、相机-手部运动解耦的第一视角视频。

**实验概括**  
论文报告其在视觉保真度、手部控制精度、跨真实日常场景泛化方面优于 prior hand-controlled generators。它的强项是 **unconstrained data scale + camera-hand disentanglement**。

**对你方向的启发**

- 适合作为出发点和 baseline。
- 但它更偏 **hand-controlled video generation**，不是完整 HOI simulator。
- 可扩展方向：加入 **object-centric 3D/4D state、contact dynamics、persistent world memory**。

---

# 2. Hand2World: Autoregressive Egocentric Interaction Generation via Free-Space Hand Gestures

- **发表情况**：arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2602.09600) / [Project](https://hand2world.github.io/)
- **3D/4D 相关度**：**强 3D hand + camera geometry；object dynamics 仍主要隐式在视频里**
- **代表图**：Hand2World pipeline

![Hand2World pipeline](https://arxiv.org/html/2602.09600v2/method_pipeline.png)

**核心概括 / Insight**  
Hand2World 从单张 scene image 和 free-space hand gesture 生成第一视角交互视频。它指出 mask-based hand conditioning 会把“手几何”和“可见性/遮挡”混在一起：训练视频中手常被物体遮挡，而推理时 free-space gesture 是完整可见的手，导致分布偏移。因此它用 **projected 3D MANO hand mesh 的 silhouette + wireframe** 作为 occlusion-invariant control，并用 per-pixel Pluecker-ray embedding 显式建模相机运动。

**Pipeline**

- **输入**：单张 egocentric scene image、free-space hand gesture sequence、可选 camera control。
- **过程**：重建/投影 3D hand mesh；生成 silhouette + wireframe 控制信号；注入 Pluecker-ray camera geometry；将 bidirectional diffusion distill 成 causal autoregressive generator。
- **输出**：可长时程、可流式生成的第一视角手-物交互视频。

**实验概括**  
在三个 egocentric interaction benchmark 上，论文报告其在 perceptual quality、3D consistency、camera control、long-horizon generation 上显著优于 InterDyn、Mask2IV、CosHand、PlayerOne、Wan2.1-Control 等。

**对你方向的启发**

- 它非常适合和 HandsOnWorld 放一起对比：二者都强调 **3D hand + camera disentanglement**。
- 但 Hand2World 的 object response 仍是 video diffusion 隐式学习出来的；缺少显式 object state / 4D object dynamics。
- 可扩展方向：把 hand mesh control 扩为 **hand-object-contact-object-state control**。

---

# 3. EgoHOI: Egocentric World Model for Photorealistic Hand-Object Interaction Synthesis

- **发表情况**：arXiv 2026；作者主页标注 ECCV 2026
- **链接**：[arXiv](https://arxiv.org/abs/2603.13615) / [Project](https://egohoi.github.io/)
- **3D/4D 相关度**：**强 3D priors + HOI world model；非常相关**
- **代表图**：EgoHOI pipeline

![EgoHOI pipeline](https://arxiv.org/html/2603.13615v1/pipeline.png)

**核心概括 / Insight**  
EgoHOI 明确反对“给未来物体轨迹等 privileged future state，再做条件视频生成”的捷径。它认为真正的 egocentric HOI world model 应该从 action signals 推断 hand-object dynamics。为此，它从 3D estimates 中蒸馏 **physics-informed embeddings**：hand kinematic embeddings、ego-motion embeddings、object entity embeddings，用来约束 latent rollout 的物理合理性、手部运动学一致性、物体身份稳定性。

**Pipeline**

- **输入**：第一帧、action signals、估计出的 3D hand/camera/object priors。
- **过程**：DiT backbone 做 latent-space state transition；HKE 约束高自由度手部运动；EME 用 Pluecker camera geometry 约束 ego-motion；OEE 用首帧物体实体特征维护 object identity；这些 embedding 通过 lightweight adapters 融入生成模型。
- **输出**：photorealistic、contact-consistent 的 egocentric HOI rollout。

**实验概括**  
在 HOT3D 上，与 Wan、Cosmos 2B/14B、Uni3C 等强基线比较，在视觉预测、ego-motion consistency、kinematic fidelity、object consistency 等方面取得提升。消融验证 physics-informed embeddings 对手部稳定、相机一致、物体保持都有效。

**对你方向的启发**

- 这是目前最贴近“HOI world model”的工作之一。
- 它强在 **3D prior distillation into video world model**。
- 仍可继续做的点：显式 object pose/state update、contact state transition、4D object representation，而不是只作为 embedding regularizer。

---

# 4. EgoSim: Egocentric World Simulator for Embodied Interaction Generation

- **发表情况**：arXiv 2026；v2 更新于 2026-07
- **链接**：[arXiv](https://arxiv.org/abs/2604.01001) / [Project](https://egosimulator.github.io/)
- **3D/4D 相关度**：**强 3D scene state + persistent update；极相关**
- **代表图**：EgoSim overview

![EgoSim overview](https://arxiv.org/html/2604.01001v2/Network04011416.png)

**核心概括 / Insight**  
EgoSim 把问题从“生成一段视频”推进到“维护并更新 3D scene state”。它指出现有 egocentric simulators 要么缺显式 3D grounding，视角变化时结构漂移；要么把场景当静态，无法支持多阶段交互后的世界状态变化。因此 EgoSim 建模 **updatable world state**，让交互视频生成和 3D 状态更新互相约束。

**Pipeline**

- **输入**：scene image / scene video、action sequence、相机轨迹/动作估计。
- **过程**：Geometry-action-aware Observation Simulation 生成 action-conditioned egocentric observation；Interaction-aware State Updating 维护并更新 3D scene state；数据管线从 in-the-wild monocular ego videos 中抽取 static point cloud、camera trajectory、embodiment actions；EgoCap 用手机低成本扫描真实场景并采集交互。
- **输出**：空间一致的第一视角交互视频，以及随交互持续更新的 3D world state。

**实验概括**  
论文在视觉质量、空间一致性、复杂场景泛化、in-the-wild dexterous interaction 上优于现有方法，并展示 cross-embodiment transfer 到 robot manipulation。

**对你方向的启发**

- 如果你要强调 3D/4D，EgoSim 比纯视频生成更重要。
- 它提供了一个可讲的核心卖点：**persistent 3D state update**。
- 可扩展方向：把 state update 细化到 object-centric 4D state、contact state、hand-object relation graph。

---

# 5. Dexterous World Models

- **发表情况**：CVPR 2026
- **链接**：[CVF](https://openaccess.thecvf.com/content/CVPR2026/html/Kim_Dexterous_World_Models_CVPR_2026_paper.html) / [arXiv](https://arxiv.org/abs/2512.17907) / [Project](https://snuvclab.github.io/dwm/)
- **3D/4D 相关度**：**强 3D scene rendering + 3D hand mesh；object dynamics 隐式**
- **代表图**：DWM overview

![DWM overview](https://arxiv.org/html/2512.17907v1/overview_v2_fix.png)

**核心概括 / Insight**  
DWM 关注如何让静态 3D digital twin 具备可交互性。它不是让视频模型从零生成整个场景，而是先给定静态 3D scene rendering，再让模型学习 hand action 导致的 residual dynamics。关键是把 **static scene renderings** 和 **egocentric hand mesh renderings** 同时作为 video diffusion 条件。

**Pipeline**

- **输入**：静态 3D scene rendering、camera trajectory、egocentric hand mesh motion、文本 prompt。
- **过程**：渲染静态场景以保证空间一致；渲染手部 mesh 表达动作几何和运动；video diffusion 学习 action-induced visual dynamics。
- **输出**：抓取、打开、移动物体等第一视角交互视频。

**实验概括**  
构建 synthetic + real hybrid interaction dataset。实验显示 DWM 在 synthetic / real、static / dynamic view 设置下，相比 SDEdit、CogVideoX-Fun、InterDyn 等具有更好的视觉质量、物理合理性和场景一致性。

**对你方向的启发**

- 强项是 **3D scene prior + 2D video dynamics**。
- 弱点是没有显式更新 object state；更像“3D-conditioned video world model”。
- 可扩展方向：把 static 3D scene 改成 **dynamic 4D scene state**，做可累计交互。

---

# 6. DexWM: World Models for Learning Dexterous Hand-Object Interactions from Human Videos

- **发表情况**：ECCV 2026
- **链接**：[arXiv](https://arxiv.org/abs/2512.13644) / [Project](https://raktimgg.github.io/dexwm/) / [Code](https://github.com/facebookresearch/dexwm)
- **3D/4D 相关度**：**强 3D hand action + latent world model；偏 robotics**
- **代表图**：DexWM architecture

![DexWM architecture](https://arxiv.org/html/2512.13644v2/Figs/flow.png)

**核心概括 / Insight**  
DexWM 认为现有 world models 的 action space 太粗，无法建模 dexterous hand-object interaction。它用从 egocentric videos 中提取的 **3D finger keypoints** 表示细粒度 dexterous actions，并学习 past latent state + hand action -> future latent state 的 dynamics。另一个 insight 是：只预测视觉 latent 不够，需要 auxiliary hand consistency loss 来约束精细手部构型。

**Pipeline**

- **输入**：过去图像 latent、3D hand keypoint action、camera motion。
- **过程**：DINOv2 编码图像为 latent state；DexWM predictor 根据 hand keypoints 和 camera motion 预测未来 latent state；用 hand consistency loss 约束 dexterity；训练数据包括 EgoDex 和 DROID。
- **输出**：未来 latent state；可用于 planning，并能迁移到 Franka + Allegro gripper。

**实验概括**  
训练使用 900+ 小时 human / robot data。DexWM 在 future-state prediction 上超过 text、navigation、full-body action-conditioned world models；在 Franka Panda + Allegro gripper 零样本技能迁移中，在 grasping、placing、reaching 等任务上平均超过 Diffusion Policy 50% 以上。

**对你方向的启发**

- 它很适合连接 human ego video 和 robot dexterous manipulation。
- 但它不是 photorealistic video generator，而是 latent world model / planning model。
- 可扩展方向：把 DexWM 的 3D hand action latent 与 EgoSim / EgoHOI 的 video simulator 结合。

---

# 7. EgoGrasp: World-Space Hand-Object Interaction Estimation from Egocentric Videos

- **发表情况**：arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2601.01050) / [Project](https://mint-sjtu.github.io/EgoGrasp.io/)
- **3D/4D 相关度**：**强 4D reconstruction / W-HOI；不是生成模型但非常重要**
- **代表图**：EgoGrasp pipeline

![EgoGrasp pipeline](https://arxiv.org/html/2601.01050v2/pipelinev2.png)

**核心概括 / Insight**  
EgoGrasp 解决从动态 egocentric monocular videos 中恢复 world-space hand-object interaction 的问题。它指出多数 HOI 方法停留在 camera coordinate 或单帧层面，缺少全局世界坐标下的时间一致 hand/object trajectory。EgoGrasp 通过 foundation models + body prior + HOI diffusion，实现 open-vocabulary object 的 world-space HOI reconstruction。

**Pipeline**

- **输入**：动态相机下的 egocentric monocular video。
- **过程**：用 spatial perception models 提取 3D scene、hand、object attributes；用 body-guided diffusion 重建 upper-body / hand pose；用 HOI-prior-informed diffusion 对离散 object 6DoF 序列做 infilling，保证空间、时间、接触一致性。
- **输出**：world-space hand poses、object 6DoF trajectories、temporally consistent W-HOI。

**实验概括**  
在 H2O、HOI4D 等数据上，EgoGrasp 在 world-space hand/object reconstruction 上达到 SOTA 或竞争性能，并能处理多个 open-vocabulary objects。

**对你方向的启发**

- 它可以作为 3D/4D pseudo-label generator。
- 如果你要用真实 ego video 训练 world model，EgoGrasp 这类方法可提供 object pose / contact / hand trajectory 标注。

---

# 8. SCAR: Open-world Hand-Object Interaction Video Generation Based on Structure and Contact-aware Representation

- **发表情况**：CVPR 2026
- **链接**：[arXiv](https://arxiv.org/abs/2512.01677) / [Project](https://hgzn258.github.io/SCAR/)
- **3D/4D 相关度**：**中等；主要是 2D/2.5D contact + depth，不是真 3D/4D state**
- **代表图**：SCAR joint generation

![SCAR pipeline](https://arxiv.org/html/2512.01677v1/pipeline_i2v.png)

**核心概括 / Insight**  
SCAR 指出 HOI video generation 面临 2D 与 3D 表示的两难：3D mesh/pose 保真但难规模化，2D mask/flow 易规模化但缺接触与结构。它提出 **structure and contact-aware representation**：用 hand-object contour、contact region、depth map 等形成可规模化的交互监督，不依赖 3D annotation。

**Pipeline**

- **输入**：observed image、task description。
- **训练表示构建**：VLM + SAM2 得到 hand/object masks；估计 contact region；估计 video depth；将 contact-augmented contours 与 depth 融合为 HOI representation。
- **生成模型**：jointly generate RGB video 和 HOI representation；Hierarchical Joint Denoiser 在统一 latent space 中 co-denoise visual tokens 和 interaction tokens。
- **输出**：HOI video 及对应的结构/接触表示。

**实验概括**  
在 TASTE-Rob、TACO 等真实数据上，SCAR 相比 CogVideoX、Wan2.1、FLOVD 等在物理合理性、时序一致性、任务对齐上更好，并展示对 unseen non-rigid / transparent / distractor objects 的 open-world 泛化。

**对你方向的启发**

- 你说得对：它不是严格 3D/4D。
- 但它提供了一个很实用的路线：**用可规模化的 2.5D/contact supervision 替代昂贵 3D annotation**。
- 可扩展方向：把 SCAR 表示升级成 object-centric 3D point/pose/contact state。

---

# 9. MEgoHand: Multimodal Egocentric Hand-Object Interaction Motion Generation

- **发表情况**：NeurIPS 2025；arXiv 2025
- **链接**：[arXiv](https://arxiv.org/abs/2505.16602) / [Project](https://beingbeyond.github.io/MEgoHand/)
- **3D/4D 相关度**：**中强；生成 3D hand motion，但不生成 world video / object state**
- **代表图**：MEgoHand pipeline

![MEgoHand pipeline](https://arxiv.org/html/2505.16602v1/pipeline.png)

**核心概括 / Insight**  
MEgoHand 生成的是 egocentric hand-object interaction 中的 hand motion，而不是完整视频 world model。它认为单靠文本或 RGB 不足以恢复第一视角 HOI motion，需要结合 VLM 语义理解、monocular depth 的 3D 空间推理、初始 MANO hand pose。

**Pipeline**

- **输入**：egocentric RGB、text instruction、initial MANO hand parameters。
- **过程**：VLM 编码语义；depth estimator 提供 object-agnostic spatial reasoning；DiT-based flow-matching policy 生成 fine-grained MANO hand trajectory；Temporal Orthogonal Filtering 提升稳定性。
- **输出**：未来 hand-object interaction 的 3D MANO hand motion sequence。

**实验概括**  
构建 3.35M RGB-D frames、24K interactions、1.2K objects 的统一数据。跨 H2O、HOI4D、HOT3D、OakInk2、TACO 等数据训练，并在 ARCTIC、HOLO 跨域评估，显著降低 wrist translation 和 joint rotation error。

**对你方向的启发**

- 它适合作为 hand action prior，而不是完整 world model。
- 可与 EgoHOI / Hand2World 结合：先生成/估计 MANO trajectory，再驱动 video world model。

---

# 10. HO-Flow: Generalizable Hand-Object Interaction Generation with Latent Flow Matching

- **发表情况**：ECCV 2026
- **链接**：[arXiv](https://arxiv.org/abs/2604.10836) / [Project](https://zerchen.github.io/projects/hoflow.html)
- **3D/4D 相关度**：**强 3D/4D motion；不是 video world model**
- **代表图**：HO-Flow overview

![HO-Flow overview](https://arxiv.org/html/2604.10836v1/overview.png)

**核心概括 / Insight**  
HO-Flow 生成 text-conditioned 3D hand-object interaction motion sequence。它的重点是把 hand 和 object motion 编进统一 latent manifold，并用 masked flow matching 做时间推理和连续 latent generation。关键 insight 是：要同时建模 hand kinematics、object motion、contact-rich coordination，才能得到物理合理且多样的 4D interaction sequence。

**Pipeline**

- **输入**：text prompt、object geometry / point cloud、上下文 motion tokens。
- **过程**：Interaction-aware VAE 编码 hand/object motion；masked auto-regressive flow matching 逐步生成 latent；object motion 用相对初始帧表示以增强泛化。
- **输出**：3D hand-object interaction motion sequence。

**实验概括**  
在 GRAB、OakInk、DexYCB 上，HO-Flow 在物理合理性、运动多样性、接触保持方面超过 prior methods。

**对你方向的启发**

- 适合作为 4D HOI motion prior。
- 不做 RGB video，但可作为 video world model 的 3D latent supervision。

---

# 11. OpenHOI: Open-World Hand-Object Interaction Synthesis with Multimodal Large Language Model

- **发表情况**：NeurIPS 2025
- **链接**：[NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2025/hash/f376f5dff6f6ec6364aea7a46ab49574-Abstract-Conference.html) / [arXiv](https://arxiv.org/abs/2505.18947) / [Project](https://openhoi.github.io/)
- **3D/4D 相关度**：**强 3D HOI synthesis + affordance；非视频 world model**
- **代表图**：OpenHOI，Fig. 2，3D MLLM 任务分解、affordance grounding、HOI diffusion 与物理优化的整体流程。来源：[Fig. 2 原图 PNG](https://arxiv.org/html/2505.18947v2/pipeline.png)

![OpenHOI Fig. 2：开放世界 3D HOI 合成流程](https://arxiv.org/html/2505.18947v2/pipeline.png)

**核心概括 / Insight**  
OpenHOI 面向 open-world 3D hand-object interaction synthesis，解决 closed-set object 和 predefined task 泛化差的问题。它用 3D MLLM 同时做 affordance grounding 和 semantic task decomposition，把复杂语言任务拆成可执行子任务，再用 affordance-driven diffusion 生成 HOI，并用 physics refinement 减少穿透、优化 affordance alignment。

**Pipeline**

- **输入**：自由语言指令、novel object / 3D object information。
- **过程**：3D MLLM 定位可交互区域并做任务分解；affordance-driven diffusion 生成 hand-object interaction；training-free physics refinement 优化物理合理性。
- **输出**：长程、多阶段、open-world 的 3D HOI sequence。

**实验概括**  
论文报告其在 novel object categories、multi-stage tasks、complex language instructions 下优于 SOTA 3D HOI synthesis 方法。

**对你方向的启发**

- 如果你的 world model 要接语言目标、任务分解、affordance，这篇很重要。
- 它不是视频生成，但可以作为 “language -> 3D affordance/contact plan” 模块。

---

# 12. VideoAfford: Grounding 3D Affordance from Human-Object-Interaction Videos via MLLM

- **发表情况**：arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2602.09638)
- **3D/4D 相关度**：**中强；从 HOI video 到 3D affordance，不是生成 world model**
- **代表图**：VideoAfford pipeline

![VideoAfford pipeline](https://arxiv.org/html/2602.09638v1/pipeline.png)

**核心概括 / Insight**  
VideoAfford 关注从 HOI videos 中学习 3D affordance grounding。它认为静态图片/语言缺少交互因果线索，而视频中的 pre-contact、contact、post-contact 能揭示物体哪里可操作、如何被操作。

**Pipeline**

- **输入**：HOI video、text instruction、3D point cloud。
- **过程**：LanguageBind 编码视频；latent action encoder 提取动作先验；3D encoder 提取 point features；video MLLM 输出 affordance token；decoder 生成 3D affordance mask；spatial-aware loss 增强空间一致性。
- **输出**：3D object affordance mask。

**实验概括**  
构建 VIDA：38K HOI videos、16 affordance types、38 object categories、22K point clouds。与 3D AffordanceNet、LASO、GREAT、AGPIL 等相比，在 seen/unseen 和 open-world 泛化上更好。

**对你方向的启发**

- 可作为 object affordance prior，为 HOI world model 提供 action-relevant regions。
- 但它不预测未来视频，也不维护动态世界状态。

---

# 13. DynamicVGGT: Learning Dynamic Point Maps for 4D Scene Reconstruction in Autonomous Driving

- **发表情况**：CVPR 2026
- **链接**：[CVF](https://openaccess.thecvf.com/content/CVPR2026/html/He_DynamicVGGT_Learning_Dynamic_Point_Maps_for_4D_Scene_Reconstruction_in_CVPR_2026_paper.html) / [arXiv](https://arxiv.org/abs/2603.08254)
- **3D/4D 相关度**：**强 4D geometry；非 HOI，但方法论很值得借鉴**
- **代表图**：DynamicVGGT pipeline

![DynamicVGGT pipeline](https://arxiv.org/html/2603.08254v1/totalpipelinev4.png)

**核心概括 / Insight**  
DynamicVGGT 把 static VGGT 扩展到 dynamic 4D reconstruction。它不是逐帧独立重建，而是在统一坐标表示中预测 current / future point maps，并通过时序对应和 Gaussian velocity 建模动态点运动。

**Pipeline**

- **输入**：monocular / multi-camera image sequences。
- **过程**：DINOv2 / VGGT backbone 提取几何 token；Motion-aware Temporal Attention 建模时间依赖；Future Point Head 预测 current / future point map；Dynamic Gaussian Head 用 motion tokens 预测 Gaussian velocity。
- **输出**：dynamic point maps、dynamic 3D Gaussians / velocities。

**实验概括**  
在 KITTI、Waymo 上验证 dynamic point-map reconstruction 和 4D scene reconstruction。相较静态 VGGT，动态区域重建和时序一致性明显提升。

**对你方向的启发**

- 它不是 HOI，但可以给你一个 4D 表示灵感：**把 HOI world state 表示成 dynamic point map / Gaussian state，而不是只用 video latent**。
- 很适合借来做“object 4D state update”的几何 backbone。

---

# 14. 关键数据集和资源

## HOT3D

- **链接**：[HOT3D](https://facebookresearch.github.io/hot3d/)
- **发表情况**：CVPR 2025 highlight
- **价值**：833 分钟 multi-view egocentric hand-object interaction，19 subjects、33 rigid objects，准确 3D hand/object pose 和 shape。适合高质量 3D HOI tracking / world model evaluation。
- **适合用途**：评估 egocentric HOI world model 的 hand kinematics、object consistency、camera consistency。

## EgoDex

- **链接**：[Apple Research](https://machinelearning.apple.com/research/egodex-learning-dexterous-manipulation) / [GitHub](https://github.com/apple/ml-egodex)
- **发表情况**：ICLR 2025
- **价值**：829 小时 Apple Vision Pro egocentric video，带 3D hand / upper-body pose 和语言标注，194 tabletop tasks。
- **适合用途**：大规模 dexterous hand action prior、human-to-robot transfer、world model pretraining。

## HOI4D

- **链接**：[HOI4D](https://hoi4d.github.io/)
- **发表情况**：CVPR 2022
- **价值**：2.4M RGB-D ego frames、4K sequences、3D hand pose、category-level object pose、scene point cloud、CAD / articulated annotations。
- **适合用途**：4D HOI reconstruction、object pose tracking、RGB-D world model 训练/评估。

---

# 15. 横向比较：哪些是真 3D/4D，哪些只是 2D？

| 工作 | 视频生成 | 显式 3D hand | 显式 camera geometry | 显式 object 3D/state | 4D / state update | 评价 |
|---|---:|---:|---:|---:|---:|---|
| HandsOnWorld | 是 | 强 | 强 | 弱 | 弱 | 强 3D hand-control，但 object dynamics 仍弱 |
| Hand2World | 是 | 强 | 强 | 弱 | 弱/中 | 很接近，但 object state 隐式 |
| EgoHOI | 是 | 强 | 强 | 中 | 中 | 最像 HOI world model |
| EgoSim | 是 | 中 | 强 | 强 | 强 | 最接近 3D/4D simulator |
| DWM | 是 | 强 | 强 | 中 | 弱/中 | 3D scene-conditioned video dynamics |
| DexWM | 否/latent | 强 | 中 | 隐式 | 中 | robotics latent world model |
| EgoGrasp | 否/重建 | 强 | 强 | 强 | 强 | 4D W-HOI reconstruction，可做标注器 |
| SCAR | 是 | 弱/2D | 弱 | 弱 | 弱 | 2.5D/contact supervision，非真 3D |
| MEgoHand | 否/手部 motion | 强 | 弱/中 | 弱 | 中 | 3D hand motion prior |
| HO-Flow | 否/3D motion | 强 | 不强调 | 强 | 强 | 3D/4D motion prior |
| OpenHOI | 否/3D synthesis | 强 | 不强调 | 强 | 中/强 | language + affordance + 3D HOI |
| VideoAfford | 否/理解 | 否 | 不强调 | 强 | 中 | 从 HOI video 学 3D affordance |
| DynamicVGGT | 否/重建 | 无 | 强 | 强 | 强 | 4D geometry prior，非 HOI |

结论：你感觉“很多还是 2D 视频”是对的。真正和 **2D+3D/4D HOI world model** 强相关的，主要是：

- **EgoSim**：persistent 3D scene state update。
- **EgoHOI**：3D physics-informed embeddings for HOI rollout。
- **DWM**：static 3D scene + hand mesh -> interactive video。
- **Hand2World / HandsOnWorld**：3D hand + camera disentanglement。
- **EgoGrasp**：world-space 4D HOI reconstruction，可作为训练标注器。
- **DexWM**：3D hand action latent world model，可连接 robot transfer。

---

# 16. 建议的研究切入点

## 方向 A：Object-Centric 4D HOI World Model

**问题**：现有 HandsOnWorld / Hand2World 主要控制手和相机，物体响应多是视频模型隐式生成。  
**切入**：显式建模 object state：

- object 6DoF pose / articulated joint state；
- contact state；
- object-centric point map / Gaussian state；
- hand-object relation graph。

**一句话 pitch**：  
从 hand-controlled egocentric video generation 走向 **object-state-aware HOI world simulation**。

## 方向 B：Scalable 2D Video -> 3D/4D Pseudo State

**问题**：真实 ego videos 多，但 3D/4D 标注贵。  
**切入**：结合 EgoGrasp、VGGT / DynamicVGGT、SAM2、Depth Anything、HaMeR/MANO，从 2D ego video 自动抽取：

- 3D hand trajectory；
- object pose / point map；
- depth / flow；
- contact heatmap；
- camera trajectory。

**一句话 pitch**：  
用可规模化伪 4D 标注，把 in-the-wild HOI video 变成 world model training data。

## 方向 C：Contact-Aware Video World Model

**问题**：视频生成容易“手碰到了但物体没动”或“物体自己动”。  
**切入**：引入 contact event / contact region / force-like interaction tokens：

- pre-contact / contact / post-contact phase；
- hand-object proximity；
- object response delay；
- contact-conditioned object motion。

**一句话 pitch**：  
让 HOI world model 学到 **action -> contact -> object response** 的因果链。

## 方向 D：Human Ego Video to Robot Dexterous World Model

**问题**：人手视频丰富，但机器人可执行动作少。  
**切入**：借鉴 DexWM / EgoDex：

- human 3D hand action -> robot gripper / dexterous hand action；
- world model 预测未来 state；
- 用 planning / inverse dynamics 迁移到机器人。

**一句话 pitch**：  
从 human egocentric HOI videos 中学习可迁移到 robot 的 dexterous interaction dynamics。

---

# 17. 推荐阅读顺序

如果你要准备组会，我建议按这个顺序读：

1. **HandsOnWorld**：导师已经提到，作为 anchor。
2. **Hand2World**：同类最近方法，重点比较 hand/camera control。
3. **EgoHOI**：从 hand-controlled generation 走向 HOI world model。
4. **EgoSim**：从 video rollout 走向 persistent 3D world state。
5. **DWM**：3D scene + hand mesh conditioned video dynamics。
6. **DexWM**：human video -> dexterous robot world model。
7. **EgoGrasp**：4D W-HOI reconstruction，作为伪标注和状态估计工具。
8. **SCAR / MEgoHand / HO-Flow**：补充 contact supervision、3D hand motion、3D HOI motion prior。

---

# 18. 最适合你在周会上说的一段话

我建议把方向表述成：

> 我想沿着 HandsOnWorld 的方向继续做，但不只停留在 3D hand-controlled egocentric video generation。当前很多方法虽然能生成第一视角手物交互视频，但物体状态和接触动力学大多还是隐式藏在 2D video latent 里。更有价值的方向是构建 **3D/4D-grounded hand-object interaction world model**：从大规模 2D egocentric videos 中自动抽取 hand trajectory、camera trajectory、object pose / point map、contact state 等伪 4D supervision，让模型不仅生成看起来合理的视频，还能维护和更新 object-centric world state，学习 action -> contact -> object response 的因果动态。
