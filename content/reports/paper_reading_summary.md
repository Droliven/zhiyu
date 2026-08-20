# 交互世界模型与人体/手物交互生成论文梳理

> 说明：每篇均基于原论文 arXiv / 项目页整理。代表图优先选论文中的方法总览图或最能说明问题设定的图；若本地 Markdown 预览器屏蔽远程图片，请点击对应论文链接或图片链接查看。

## 1. Learning Interactive World Model for Object-Centric Reinforcement Learning

- **发表情况**：NeurIPS 2025
- **链接**：[arXiv](https://arxiv.org/abs/2511.02225)
- **代表图**：FIOC-WM 整体 pipeline

![FIOC-WM pipeline](https://arxiv.org/html/2511.02225v1/fig2.png)

**核心概括 / Insight**  
提出 **Factored Interactive Object-Centric World Model (FIOC-WM)**。多数 object-centric RL 只把状态拆成对象，但交互关系仍是隐式的；本文进一步显式学习对象间 interaction graph，并把每个对象状态拆为动态属性与静态属性。关键 insight：长时程任务可以被分解成一串“对象交互 primitive”，高层策略选择交互图，低层策略执行交互。

**Pipeline**

- **输入**：像素观测、动作、奖励。
- **过程**：DINO/R3M 等预训练视觉特征 + Slot Attention 得到对象表示；VAE 学 object latents；拆分 static / dynamic factors；学习 interaction graph、transition、reward；再训练层级策略。
- **输出**：可用于规划和策略学习的 object-centric interactive world model，以及高低层策略。

**实验概括**  
在 SpritesWorld、Fetch、Franka Kitchen、iGibson、Libero 上比较 DreamerV3、TD-MPC2、DINO-WM、EIT。结果显示 FIOC-WM 在单任务、属性泛化、组合泛化、skill 泛化上整体更优。消融表明 interaction modeling 和 hierarchical policy 是最关键组件。

---

## 2. MEgoHand: Multimodal Egocentric Hand-Object Interaction Motion Generation

- **发表情况**：arXiv 2025
- **链接**：[arXiv](https://arxiv.org/abs/2505.16602) / [Project](https://beingbeyond.github.io/MEgoHand/)
- **代表图**：MEgoHand 多模态运动生成框架

![MEgoHand pipeline](https://arxiv.org/html/2505.16602v1/pipeline.png)

**核心概括 / Insight**  
MEgoHand 解决第一视角手-物交互运动生成。核心 insight：只用文本或 RGB 不够，第一视角 HOI 需要同时利用 **语义理解、3D 深度、初始手姿态**。它把 VLM 当作高层 “cerebrum”，用深度估计补 3D 空间信息，再用 DiT / flow matching 生成细粒度 MANO 手部轨迹。

**Pipeline**

- **输入**：任务文本、egocentric RGB、预测/真实深度、初始 MANO 手参数。
- **过程**：RGB 经 VLM 视觉编码，RGB 估计 metric depth 并编码；文本/RGB/depth 融合；DiT-based motion generator 预测未来 MANO 参数；Temporal Orthogonal Filtering 平滑旋转。
- **输出**：未来一段 hand-object interaction 的 MANO 手部运动序列。

**实验概括**  
整合 3.35M RGB-D frames、24K interactions、1.2K objects。训练集包括 TACO、HOI4D、H2O、HOT3D、OakInk2 等，跨域测试 ARCTIC、HOLO。相比 LatentAct / LatentAct-Diff，in-domain 与 cross-domain 指标均明显更好；消融证明 depth supervision、文本+图像+深度融合、初始手姿态都有效。

---

## 3. Dexterous World Models

- **发表情况**：arXiv 2025
- **链接**：[arXiv](https://arxiv.org/abs/2512.17907) / [Project](https://snuvclab.github.io/dwm/)
- **代表图**：scene-action-conditioned video diffusion

![Dexterous World Models overview](https://arxiv.org/html/2512.17907v1/overview_v2_fix.png)

**核心概括 / Insight**  
DWM 把静态 3D digital twin 变成可交互世界模型。核心 insight：不要让视频模型从零 hallucinate 整个场景，而是给定静态场景渲染，让模型只学习 **手部动作造成的 residual dynamics**。

**Pipeline**

- **输入**：静态 3D 场景沿相机轨迹渲染的视频、egocentric hand mesh video、文本 prompt。
- **过程**：用 inpainting video diffusion 初始化；静态场景 latent 与手部 mesh latent 作为条件；DiT 在 latent video space 学习动作导致的残差变化。
- **输出**：第一视角交互视频，如抓取、打开、移动物体。

**实验概括**  
构建 synthetic + real hybrid dataset：TRUMANS 提供精确对齐，TASTE-Rob 等真实视频提供真实动力学。测试集包含 synthetic dynamic、real static、real dynamic。相比 SDEdit、CogVideoX-Fun finetune、InterDyn，DWM 在 PSNR/SSIM/LPIPS/DreamSim 上整体最好，并展示可用于 action evaluation：生成候选动作后用 VideoCLIP/LPIPS 选最匹配目标的视频结果。

---

## 4. Hand2World: Autoregressive Egocentric Interaction Generation via Free-Space Hand Gestures

- **发表情况**：arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2602.09600) / [Project](https://hand2world.github.io/)
- **代表图**：Hand2World 方法框架

![Hand2World pipeline](https://arxiv.org/html/2602.09600v2/method_pipeline.png)

**核心概括 / Insight**  
Hand2World 从单张场景图 + 空中手势生成第一视角交互视频。核心 insight：free-space gesture 与真实接触训练数据存在遮挡分布差异，不能直接用手 mask 控制；应使用 **projected 3D hand mesh** 作为 occlusion-invariant control，并显式注入 camera geometry 防止背景漂移。

**Pipeline**

- **输入**：单张 egocentric scene image、free-space hand gesture sequence、可选 camera control。
- **过程**：重建/投影 3D MANO hand mesh，形成 silhouette + wireframe 控制；Pluecker-ray embedding 注入相机几何；双向 diffusion teacher 蒸馏为 causal AR generator。
- **输出**：任意长度、可流式生成的第一视角手-物交互视频。

**实验概括**  
在三个 egocentric interaction benchmark 上评估 perceptual quality、3D/viewpoint consistency、long-horizon rollout。论文报告 FVD 降低约 76%，camera trajectory error 降低约 42%。对比 InterDyn、Mask2IV、CosHand、PlayerOne、Wan2.1-Control 等，Hand2World 在自由手势、相机控制、长时程稳定性上更强。

---

## 5. EgoForge: Goal-Directed Egocentric World Simulator

- **发表情况**：arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2603.20169) / [Project](https://plan-lab.github.io/projects/egoforge/)
- **代表图**：EgoForge 总览

![EgoForge overview](https://arxiv.org/html/2603.20169v1/concept_video_yifan.png)

**核心概括 / Insight**  
EgoForge 关注“目标导向”的第一视角世界模拟：给一张 egocentric image、高层指令、可选 exocentric view，生成完成目标的第一视角 rollout。核心 insight：长程 egocentric video 不仅要像，还要满足目标完成、时序因果、场景稳定和几何一致。

**Pipeline**

- **输入**：单张第一视角图像、自然语言目标/指令、可选第三视角参考图。
- **过程**：DiT backbone；引入 geometry-level grounding，与 VGGT 几何特征对齐；VideoDiffusionNFT 用 trajectory-level reward 细化采样。
- **输出**：目标导向的第一视角视频 rollout。

**实验概括**  
构建 X-Ego benchmark，评估 goal alignment、temporal coherence、physical consistency。相对强基线，DINO-Score、CLIP-Score、FVD、Flow MSE、SSIM、LPIPS、PSNR 等指标均有提升。结论是 reward-guided diffusion refinement 能显著提升长程目标一致性和稳定性。

---

## 6. HOI-Dyn: Learning Interaction Dynamics for Human-Object Motion Diffusion

- **发表情况**：NeurIPS 2025
- **链接**：[arXiv](https://arxiv.org/abs/2507.01737) / [Project](https://wulin97.github.io/hoi-dyn/)
- **代表图**：driver-responder interaction dynamics framework

![HOI-Dyn framework](https://arxiv.org/html/2507.01737v3/framework_main.png)

**核心概括 / Insight**  
HOI-Dyn 把 HOI 生成建模为 **driver-responder system**：人体动作是 driver，物体运动是 responder。关键 insight：只联合生成 human motion 和 object motion 不够，必须显式约束“物体应如何响应人体动作”，否则会出现物体提前移动、漂浮、反应夸张等因果错误。

**Pipeline**

- **输入**：文本/条件、物体几何、初始状态、稀疏 waypoint/contact context。
- **过程**：conditional motion diffusion 生成 human-object trajectory；训练时加入轻量 Transformer interaction dynamics model，预测物体对人体相对运动的响应；residual dynamics loss 约束生成。
- **输出**：3D human motion、object motion、interaction context。

**实验概括**  
在 FullBodyManipulation / 3D-FUTURE 等设置上比较 InterDiff、MDM、OMOMO、CHOIS。HOI-Dyn 在 FID、foot sliding、contact F1、MPJPE、object translation/rotation error 等指标整体更优。定性结果显示它减少物体提前移动、浮空、滑动等问题。作者还把 dynamics loss 作为评估交互因果一致性的 proxy metric。

---

## 7. InterPrior: Scaling Generative Control for Physics-Based Human-Object Interactions

- **发表情况**：arXiv 2026；IPA 2026 Best Poster
- **链接**：[arXiv](https://arxiv.org/abs/2602.06035) / [Project](https://sirui-xu.github.io/InterPrior)
- **代表图**：InterPrior 三阶段框架

![InterPrior framework](https://arxiv.org/html/2602.06035v1/method2.png)

**核心概括 / Insight**  
InterPrior 学的是 physics simulator 中的 HOI controller，而不只是离线生成轨迹。核心 insight：大规模 imitation distillation 可以提供自然动作先验，但单靠蒸馏泛化差；单靠 RL 容易 reward hacking。因此先蒸馏 imitation expert，再用 RL post-training 把策略推到更鲁棒的可行流形。

**Pipeline**

- **输入**：当前人-物状态、历史状态、高层目标，如 snapshot、trajectory、contact、稀疏目标。
- **过程**：训练 full-reference imitation expert；蒸馏成 goal-conditioned variational policy，latent 表示 skill；对 latent/observation 做 bounding；RL finetuning 增强 OOD 鲁棒性。
- **输出**：可在物理仿真中执行的 full-body HOI control policy。

**实验概括**  
在 snapshot、trajectory、contact、long-horizon chain、random initialization 等任务评估。完整 InterPrior 在多个 in-distribution goal-conditioned tasks 上成功率高；随机初始化 object lifting success 明显提升。BEHAVE/HODome 新对象和新交互适配中，InterPrior + finetuning 明显优于 InterMimic + finetuning，说明它是可复用的 HOI prior。

---

## 8. VideoAfford: Grounding 3D Affordance from Human-Object-Interaction Videos via Multimodal Large Language Model

- **发表情况**：arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2602.09638)
- **代表图**：VideoAfford 框架

![VideoAfford pipeline](https://arxiv.org/html/2602.09638v1/pipeline.png)

**核心概括 / Insight**  
VideoAfford 研究从 HOI 视频中学习 3D affordance grounding。核心 insight：静态图片/语言难以解释“哪里可操作”，视频中的 pre-contact/contact/post-contact 动态过程能提供因果交互线索。

**Pipeline**

- **输入**：HOI 视频、文本 instruction、3D point cloud。
- **过程**：构建 VIDA 数据集；LanguageBind 编码视频；latent action encoder 提取交互动作先验；3D encoder 提取点云特征；video MLLM 输出 affordance token；affordance decoder 生成点云 affordance mask；spatial-aware loss 增强 3D 空间一致性。
- **输出**：3D object affordance mask。

**实验概括**  
VIDA 含约 38K HOI videos、16 affordance types、38 object categories、22K point clouds。实验包含 seen/unseen 设置，与 3D AffordanceNet、LASO、GREAT、AGPIL 等静态方法对比。结果显示 VideoAfford 在 in-distribution 和 open-world / unseen 泛化中均更强；消融证明 latent action encoder 和 spatial-aware loss 都有效。

---

## 9. MotionGPT3: Human Motion as a Second Modality

- **发表情况**：arXiv 2025
- **链接**：[arXiv](https://arxiv.org/abs/2506.24086) / [Project](https://motiongpt3.github.io/)
- **代表图**：dual-stream motion-language architecture

![MotionGPT3 architecture](https://arxiv.org/html/2506.24086v3/architure-v1.png)

**核心概括 / Insight**  
MotionGPT3 把 human motion 当成和 text 并列的第二模态，而不是把 motion 强行离散成 token。核心 insight：motion tokenization 会带来量化误差，single-stream text-motion 混训会产生跨模态干扰；因此用连续 VAE latent + 双流 Transformer + shared attention 更适合 motion-language unified modeling。

**Pipeline**

- **输入**：文本序列或 motion sequence。
- **过程**：motion VAE 编码连续 latent；文本分支保留预训练 LLM 参数；motion branch 用 diffusion head 预测 motion latent；双分支通过 shared attention 交互；三阶段 generate-then-align training。
- **输出**：text-to-motion、motion-to-text，以及混合 motion-language 任务输出。

**实验概括**  
在 motion generation 与 motion understanding benchmark 上达到 SOTA 或竞争性能。训练收敛显著更快：论文报告 training loss 约 2x faster，validation 最多 4x faster。实验结论是连续 motion latent + 双流结构能同时保留动作质量和语言能力。

---

## 10. InfiniteDance: Scalable 3D Dance Generation Towards in-the-wild Generalization

- **发表情况**：arXiv 2026
- **链接**：[arXiv](https://arxiv.org/abs/2603.13375) / [Project](https://infinitedance.github.io/) / [Hugging Face](https://huggingface.co/huuuuuuuuu/InfiniteDance)
- **代表图**：ChoreoLLaMA 框架

![ChoreoLLaMA](https://arxiv.org/html/2603.13375v1/ChoreoLLaMA.png)

**核心概括 / Insight**  
InfiniteDance 解决 3D dance generation 的野外泛化问题。核心 insight：泛化差主要来自数据规模和模型容量不足，因此同时 scale data 和 model：从野外单目视频自动重建大规模 3D 舞蹈数据，并用 LLaMA-style architecture 学音乐到舞蹈。

**Pipeline**

- **输入**：音乐音频，可选检索到的参考舞蹈 prompt。
- **过程**：自动单目视频重建 3D dance；Foot Restoration Diffusion Model 修复脚滑、浮空、穿透；构建 100.69h、30 genres、SMPL-X 数据集；ChoreoLLaMA 用 RAG 注入参考舞蹈，并用 slow/fast-cadence MoE 适配不同节奏。
- **输出**：与音乐同步、长时程、跨舞种泛化的 3D dance motion。

**实验概括**  
数据集比既有 3D dance 数据规模更大，含 1000+ dancers、55 joints、手部和面部信息、30 个舞种。实验跨多舞种音乐评估，定量和定性均超过现有方法；RAG 提升陌生音乐下的结构性，Cadence-MoE 改善不同速度音乐的节奏适配，FRDM 提升脚部物理合理性。

---

# 分类梳理与趋势分析

## A. Egocentric Interactive World Model：从“看视频”到“模拟可交互世界”

相关论文：**Dexterous World Models、Hand2World、EgoForge**

这一类论文的共同目标是让生成模型具备第一视角交互模拟能力。DWM 关注“静态 3D 场景 + 手部动作 -> 动态交互视频”；Hand2World 进一步强调 free-space hand gesture、显式相机控制和自回归长视频；EgoForge 则把目标指令和 reward-guided refinement 加入世界模拟，强调 goal completion。

**趋势**：从 image-to-video 的视觉合成，转向 action-conditioned、camera-aware、goal-directed 的 world simulator。

## B. Human/Object Interaction Motion：从“轨迹合理”到“因果与物理一致”

相关论文：**MEgoHand、HOI-Dyn、InterPrior**

MEgoHand 生成第一视角手部 MANO 轨迹，重点是多模态理解和 3D 空间推理；HOI-Dyn 显式建模 human driver -> object responder 的交互动力学；InterPrior 则进入 physics-based controller，要求动作不仅可生成，还能在物理仿真中执行并完成目标。

**趋势**：从离线 motion generation，走向 dynamics-aware generation，再走向可闭环执行的 physics-based generative control。

## C. Affordance / Interaction Understanding：从静态语义到动态交互证据

相关论文：**VideoAfford**

VideoAfford 的位置很关键：它不是直接生成视频或动作，而是从 HOI 视频中抽取 3D affordance。它说明当前领域正在把“人如何和物体互动”的视频证据，转化为机器人可用的 3D 操作区域。

**趋势**：affordance learning 正从 image/text prior 转向 video-demonstration prior，强调时序、接触、因果。

## D. Motion Foundation Model / Data Scaling：动作作为大模型模态

相关论文：**MotionGPT3、InfiniteDance**

MotionGPT3 代表“把 motion 纳入 LLM 多模态体系”的方向，重点解决连续动作与离散文本之间的表示冲突；InfiniteDance 则展示了动作数据和模型规模化的重要性，用大规模野外数据 + LLaMA-style 模型提升音乐舞蹈泛化。

**趋势**：动作生成开始拥抱 foundation model 思路：连续 latent、多分支架构、大规模数据、RAG/MoE 等机制会越来越常见。

## 总结判断

这组论文共同指向一个方向：**Embodied generative modeling 正在从“生成好看的动作/视频”，走向“生成可控、可交互、物理一致、可长程执行的世界演化”。**

更具体地说：

- 控制信号从文本扩展到手势、相机、目标、接触、轨迹、affordance。
- 表示方式从 2D mask / text prompt 走向 3D mesh、depth、point cloud、geometry embedding。
- 训练目标从感知质量扩展到 interaction causality、goal completion、physics robustness。
- 模型形态从 diffusion generator 走向 autoregressive simulator、reward-refined simulator、physics-based controller、motion-language foundation model。

如果后续继续追这个方向，建议重点关注三类关键词：**egocentric world model、interaction dynamics、physics-based generative control**。
