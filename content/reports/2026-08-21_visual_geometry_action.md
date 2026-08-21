# Visual Action / Geometry Action：以视觉与几何形式统一跨本体动作

**报告标签**：visual action, geometry action, world model, cross-embodiment, embodied AI

检索日期：2026-08-21。范围：2024-01-01 至检索日，优先 2025–2026 新作。检索从 arXiv、CVF、作者项目页与代码仓库获得线索，并以论文正文、正式出版页和官方资源为准。FlowWAM（2607.13017）与 Masked Visual Actions（2607.19343）虽已由其他报告入库，但作为本专题的核心坐标仍在下文完整纳入；数据层按 arXiv ID 合并，不会产生重复论文记录。

本专题所说的 action representation 不是“给策略额外加入深度输入”，而是把动作本身或动作引起的变化改写为视频模型原生、跨本体可共享的视觉/几何接口。当前形成四条路线：

- **光流与 latent motion**：FlowWAM 把光流作为显式 flow video，Motus 与 Latent Policy Steering 则将无标签视频中的光流压缩为 latent action。
- **实体轨迹、骨架与视觉场**：Masked Visual Actions、VAP、OSCAR、EA-WM、GeniWorld、iMaC、RoFacto 把动作表示为实体 mask，或把关节动作经运动学投影为图像、骨架、深度与接触距离场。
- **3D point / trace**：PointAction、TraceGen、μ₀ 预测像素对齐点图或语义交互轨迹，再由本体专属模块解码。
- **粒子位移**：Scaling Cross-Embodiment World Models 直接把人手、机器人手和物体写成粒子，以粒子位移统一不同关节空间。

下文按与“ego human video、embodied video、不同 embodiment 的统一动作接口”的相关度排序：先讨论视频原生的显式 flow / masked entity action，再讨论人手—机器人共享的骨架和 3D trace，随后是需要本体适配的 point/latent 接口，最后是更依赖 URDF、标定或特定评测任务的视觉条件。

证据审计后的共同判断是：相机对齐、空间显式的动作条件通常优于低维数值条件，但“接口跨本体”不等于“无需标定、数据或解码器即可零样本控制”。遮挡、相机运动、深度误差、接触力学缺失、生成延迟和训练成本仍是主要瓶颈。

## 1. FlowWAM: Optical Flow as a Unified Action Representation for World Action Models

**作者：** Yixiang Chen, Peiyan Li, Yuan Xu, Qisen Ma, Jiabing Yang, Kai Wang, Jianhua Yang, Dong An, He Guan, Gaoteng Liu, Jianlou Si, Jun Huang, Jing Liu, Nianfeng Liu, Yan Huang, Liang Wang
**年份与发表：** 2026，arXiv preprint（v1，cs.RO，2026-07-14）。通讯作者 Yan Huang、Liang Wang。尚无 DOI / 正式出版页。
**可靠入口：** [arXiv](https://arxiv.org/abs/2607.13017)｜[HTML 全文](https://arxiv.org/html/2607.13017)｜[项目页](https://flow-wam.github.io/)｜[代码](https://github.com/YixiangChen515/FlowWAM)｜[模型](https://huggingface.co/YixiangChen/FlowWAM)｜[数据](https://huggingface.co/datasets/YixiangChen/FlowWAM_RoboTwin)｜[AlphaXiv](https://alphaxiv.org/abs/2607.13017)
**代表图：** FlowWAM，Fig. 2，dual-stream RGB–flow diffusion overview。来源：[Fig. 2 原图 PNG](https://arxiv.org/html/2607.13017v1/method.png)

![FlowWAM Fig. 2: dual-stream RGB and optical flow generation](https://arxiv.org/html/2607.13017v1/method.png)

### 当前挑战

WAM 想借用预训练视频生成器的运动先验做控制，但动作必须同时满足两件事：格式贴合视频生成器，以及跨帧运动线索足够解码成可执行控制。本文针对的是这个表征缺口，而不是“视频生成还不够像真”。

- **数值动作 token** 精确，但动作空间随本体变化，和像素先验不在同一模态。
- **学习 latent action** 可跨本体，却往往丢掉稠密、空间对齐的运动。
- **图像空间动作** 多是静态“在哪里动”，不是“每一可见部分如何随帧移动”。
- 先前光流工作没有把 flow 放进视频生成器的生成 latent，同时充当策略目标和世界模型条件。

### 研究动机

核心 Insight：**把光流编码成与 RGB 同格式的视频，就可以作为 WAM 的统一动作表征——策略模式生成 flow 再解码动作，世界模型模式固定目标 flow 来引导未来 RGB，并且可以从无动作标签的自我中心视频里预训练。**

这改变的是动作/视频接口，不是再加一个更重的 RGB rollout 头。与本专题直接相关：它对照数值 token、latent action 和静态图像动作，并在 RoboTwin / WorldArena 上同时测策略与世界模型。它建模的是像素位移场，不是结构因果或反事实。

### 技术方案

- **输入：** 参考 RGB \(I_0\)、语言指令 \(\tau\)；策略模式还要本体感觉。RoboTwin 阶段把头/左腕/右腕拼成 \(320\times384\) 的 T 形拼图。
- **过程：** RAFT 提取光流，HSV 色轮编码方向和幅度。同一冻结 VAE 分别编码 RGB 与 flow latent，各 self-attention 层联合注意两路 token。策略模式联合去噪 RGB/flow，约 780M action expert 交叉注意其 hidden states 并用 flow matching 预测动作块；世界模型模式固定目标 flow latent，只去噪 RGB。两阶段先用 EgoDex 无动作标签视频训练双流 DiT，再在 RoboTwin 接入 action expert。
- **输出：** 策略模式输出未来 RGB、flow 视频与可执行动作块；世界模型模式输出与指定运动一致的未来 RGB。

相对 Motus，FlowWAM 生成显式 flow 视频而非只提取低维 latent action；相对数值动作 WAM，它让动作成为视频生成器原生模态。RoboTwin 的 flow 监督来自 robot-only 渲染，因此不包含接触后的物体 scene flow。

### 实验结果

- **RoboTwin 2.0（50 任务，Clean 50 demo + Random 500 demo 合训，每任务 100 rollout）：** 预训练 FlowWAM 为 **92.94% Clean / 92.14% Random**；无 EgoDex 预训练为 82.40/80.80。Hanging Mug 等难任务仍只有 65/68。
- **WorldArena：** EWMScore **63.71**，Trajectory Accuracy **64.26**；轨迹轴优势明显，外观一致性并非全面领先。
- **真机：** Franka 四任务与 ARX 双臂三任务各 100 条演示、10 trial，平均 **75.7%**，π0.5 为 61.4%、Motus 57.1%。
- **消融：** 数值动作 69.8，原始 \((u,v)\) 72.3，去掉 flow 重加权 83.9，完整 89.8。预测 flow 误差与成功率 Pearson \(r=-0.81\)，支持相关性而非因果性。

### 总结讨论

FlowWAM 把动作定义为视频原生、跨帧稠密且可解码的运动场，是连接 ego human video、embodied video 与机器人动作的核心工作。边界包括腕部 flow 缺失、robot-only 目标丢失物体响应、HSV 幅度截断和 5B 视频骨干成本；RoboTwin 数字也不能与使用不同脚本的工作直接排榜。

### 代码与数据

代码仓库含训练、推理与数据生成模块，许可证为 Apache-2.0。模型和 RoboTwin 数据入口已公开；完整复现仍依赖 EgoDex、RoboTwin、RAFT 伪标签及约 32×H100 训练设置。

### 局限、失败案例与开放问题

- 腕部视角没有 robot-only flow 监督，使用常量占位。
- flow 目标不包含接触后的物体/背景运动。
- WorldArena 消融 split 与官方远程评测不同。
- 真机每任务仅 10 trial，难任务仍明显较低。
- 光流是像素位移，不是可干预因果变量。
- 尚未完成互联网规模无动作预训练与长时 flow planning。

## 2. Masked Visual Actions for Unified World Modeling

**作者：** Hadi Alzayer, Wenlong Huang, Haonan Chen, Christopher Luey, Lvmin Zhang, Maneesh Agrawala, Gordon Wetzstein, Li Fei-Fei, Yilun Du, Jiajun Wu, Jia-Bin Huang
**年份与发表：** 2026，arXiv preprint（v1，cs.CV，2026-07-21）
**可靠入口：** [arXiv](https://arxiv.org/abs/2607.19343)｜[HTML 全文](https://arxiv.org/html/2607.19343)｜[项目页](https://masked-visual-actions.github.io/)｜[代码](https://github.com/HadiZayer/masked-visual-actions)｜[权重](https://huggingface.co/HadiZayer/masked-visual-actions)｜[AlphaXiv](https://alphaxiv.org/abs/2607.19343)
**代表图：** Masked Visual Actions，Fig. 1，同一 checkpoint 用遮罩机器人轨迹做正向动力学、用遮罩物体运动做逆向合成。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2607.19343v1/teaser.png)

![Masked Visual Actions Fig. 1: forward and inverse queries via masked trajectories](https://arxiv.org/html/2607.19343v1/teaser.png)

### 当前挑战

视频模型已有运动、接触和形变先验，却缺少与像素预训练空间一致的动作入口。文本太欠定，tracks/关键点过稀疏，关节角和末端位姿又绑定本体。把动作简单画成 skeleton 或 end-effector 也不充分：域内结果接近，但未见夹爪和双臂上会幻觉训练集机器人或扭曲本体。

### 研究动机

核心做法是把动作表示成视频中任意实体的部分可见时空轨迹：露出机器人运动，模型补全物体与场景响应；露出期望物体运动，同一模型补全机器人行为。主动与被动不再是两套架构，而是对同一交互先验的不同 masked-video 查询。它与 FlowWAM 一起构成本专题最直接的两个端点：显式 flow field 与实体 masked trajectory。

### 技术方案

- **输入：** 参考帧、masked 条件视频（未露出区域填灰）和文本 prompt；正向时 mask 是机器人轨迹，逆向时是物体/期望运动。
- **过程：** Wan-Fun-Control 2.2 14B 双 expert MoE；条件经同一 VAE 后与视频 latent 拼接。LoRA rank 256，batch 4，8×H200，约 10k steps/4 天。约 15 小时数据混合 DROID、RoboCasa 成功与失败轨迹；条件来自机器人分割或 URDF 渲染。
- **输出：** 正向模式输出场景对机器人运动的响应；逆向模式输出与目标物体运动一致的机器人视频，再由单独 IDM 转成控制。规划时对 Diffusion Policy 候选 rollout，并由 Gemini 3.1 Pro 排序。

与 Ctrl-World 的原始动作向量、Wan-Move 的 GT tracks、skeleton/EE 稀疏可视化相比，masked entity trajectory 更稠密且与像素对齐。实现是 DiffSynth-Studio 上的 LoRA 薄层，没有修改视频骨干。

### 实验结果

- **DROID（LPIPS/SSIM/PSNR）：** 0.0945/0.887/23.74；Ctrl-World 0.362/0.708/18.15。Ctrl-World 见过全部 DROID，公平性对其有利。
- **BEHAVIOR 未见双臂：** 0.123/0.843/22.90；Ctrl-World 0.196/0.837/18.39。
- **条件消融：** DROID 域内 EE/skeleton/masked 接近；自定义夹爪 LPIPS 为 0.183/0.169/0.148，BEHAVIOR 为 0.171/0.162/0.123。
- **策略评估：** 视频模型成功率与 GT 环境相关 \(r=0.982\)，但存在系统性成功正偏差。
- **逆向动作：** RoboCasa CoffeeServeMug、20 trials，本方法报告 90%；视频模型未见任务，但 IDM 使用 100 条示范。

### 总结讨论

Masked Visual Actions 直接展示了像素级实体轨迹如何统一正向世界建模、逆向机器人行为、人手/机器人视频与未见本体。它最贴近用户关心的“把 action 变成视觉形式”；但生成保真不自动等于可靠规划，模型学到的是交互相关而不是因果。

### 代码与数据

代码和高/低噪两套 LoRA 权重已公开，Apache-2.0。训练使用 DROID 与 RoboCasa；完整 15 小时 masked 语料和 URDF 渲染工具是否已全部发布仍待核验。规划依赖闭源 Gemini 3.1 Pro。

### 局限、失败案例与开放问题

- 14B 骨干带来高延迟与算力成本。
- 分割条件可能从遮挡泄漏原视频动态；渲染条件需要标定。
- 视频内评估对成功有正偏差，不能视为无偏模拟器。
- 规划排序依赖闭源 VLM。
- 逆向视频仍需单独 IDM 才能落地动作。
- 学到的是相关性，不是可识别的接触因果。

## 3. Motus: A Unified Latent Action World Model

**作者：** Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Yao Feng, Chendong Xiang, Yinze Rong, Hongyan Zhao, Hanyu Liu, Zhizhong Su, Lei Ma, Hang Su, Jun Zhu
**年份与发表：** 2026，CVPR 2026（arXiv 初稿 2025）
**arXiv / DOI：** 2512.13030；10.48550/arXiv.2512.13030
**类别标签：** optical flow, latent action, unified world-action model, cross-embodiment
**可靠入口：** [CVPR](https://openaccess.thecvf.com/content/CVPR2026/html/Bi_Motus_A_Unified_Latent_Action_World_Model_CVPR_2026_paper.html)｜[arXiv](https://arxiv.org/abs/2512.13030)｜[项目](https://motus-robotics.github.io/motus)｜[模型](https://huggingface.co/motus-robotics/Motus)｜[AlphaXiv](https://www.alphaxiv.org/abs/2512.13030)
**代表图：** Motus，Fig. 1，三专家架构与统一生成模式。来源：[Fig. 1 原图](https://arxiv.org/html/2512.13030v2/x1.png)

![Motus Fig. 1](https://arxiv.org/html/2512.13030v2/x1.png)

### 当前挑战

VLA、视频世界模型、逆动力学和视频—动作联合预测通常由不同系统承担，难共享理解、生成和控制先验。更根本的缺口是不同机器人的动作维度与语义不兼容，人类第一视角视频又没有机器人动作标签；直接联合视频与动作 token 还会因视频 token 数量占优而削弱控制学习。

### 研究动机

作者把光流视为像素级“delta action”：它不要求关节空间一致，可从人类、模拟和多机器人视频自动提取。核心 Insight 是同时建立模型接口（三专家 MoT）与数据接口（低维光流 latent），让同一模型切换 VLA、WM、IDM、视频生成和联合预测。与本专题直接相关，但光流 latent 仍需目标本体动作监督才能成为可执行控制。

### 技术方案

- **输入：** 当前观测、语言、可选本体状态，以及按模式提供的未来动作、视频或 DPFlow 光流。
- **过程：** Wan2.2-5B 视频专家、Qwen3-VL 理解专家和 641.5M action expert 通过联合注意力交互；UniDiffuser 式双时间步控制不同条件/生成模式。DC-AE 把 RGB 光流压成 4×512 特征，再映射为 14 维 latent action；90% 无标签流重建与 10% 有动作对齐混训。三阶段数据金字塔依次适配视频模型、训练 latent action 与三专家、最后做目标机器人动作 SFT。
- **输出：** 可执行动作块、未来视频、逆动力学动作，或视频—动作联合序列。

相对只做单一 VLA/WAM 的 baseline，Motus 的实质差异是同一 checkpoint 的多条件生成，以及用光流先在 action-free 视频上预训练 action expert；动作 48 步/30 Hz、视频 8 帧/5 Hz，以降低模态失衡。

### 实验结果

RoboTwin 2.0 使用 50 任务，Clean 每任务 50 条、Randomized 每任务 500 条训练轨迹，每任务 100 次执行。Motus 为 88.66% / 87.02%，X-VLA 为 72.80% / 72.84%，π0.5 为 42.98% / 43.84%；摘要中的“+15%/+45%”接近百分点差，不是严格相对提升率。无预训练为 77.56% / 77.00%，仅 Stage 1 为 82.26% / 81.86%，支持完整预训练有效；但 Place Dual Shoes、Scan Object 等单任务不总领先。

真实 AC-One 和 Agilex-Aloha-2 每任务 100 条轨迹，采用 partial success：Motus 平均 63.22 与 59.30，π0.5 为 14.79 与 48.60；个别任务 Motus 仍低于基线。LIBERO-Long 为 97.6，与 X-VLA 持平。模型约 8B、推理 10 个 flow-matching steps；未报告训练 GPU、时长或 FLOPs。组件未逐项消融，不能把平均增益单独归因于光流。

### 总结讨论

Motus 最强证据是多模式统一与预训练阶段消融，而非摘要中的单个提升数字。它展示了光流可把无标签视频接入 action learning，但 14 维瓶颈是启发式设计，遮挡和相机运动鲁棒性未被充分验证，也没有证明 latent 对任意本体都具有稳定语义。

### 代码与数据

Stage-2 权重已公开；未核验到官方代码仓库或整理后的六层混合数据。训练依赖 EgoDex、RoboTwin、AgiBot World、RoboMIND、AnyPos 等外部资源。

### 局限、失败案例与开放问题

- 8B 模型训练与部署成本高，算力披露不足。
- 光流受遮挡、低纹理和相机运动影响，缺少专项鲁棒性实验。
- 14 维 latent action 未证明对更多形态最优。
- 关键架构与数据组件缺少正交消融。
- partial success 不等同完整任务成功，且部分任务出现负迁移。

## 4. Precise Action-to-Video Generation Through Visual Action Prompts

**作者：** Yuang Wang, Chao Wen, Haoyu Guo, Sida Peng, Minghan Qin, Hujun Bao, Xiaowei Zhou, Ruizhen Hu
**年份与发表：** 2025，ICCV 2025，pp. 12713–12724
**arXiv / DOI：** 2508.13104；未核验独立 DOI
**类别标签：** visual action prompt, skeleton, human-object interaction, action-to-video
**可靠入口：** [ICCV](https://openaccess.thecvf.com/content/ICCV2025/html/Wang_Precise_Action-to-Video_Generation_Through_Visual_Action_Prompts_ICCV_2025_paper.html)｜[arXiv](https://arxiv.org/abs/2508.13104)｜[项目](https://zju3dv.github.io/VAP/)
**代表图：** Precise Action-to-Video Generation Through Visual Action Prompts，Fig. 1，骨架 visual action prompt 统一人手与机器人动作。来源：[Fig. 1 原图](https://arxiv.org/html/2508.13104/x1.png)

![Precise Action-to-Video Generation Through Visual Action Prompts Fig. 1](https://arxiv.org/html/2508.13104/x1.png)

### 当前挑战

action-to-video 存在精度—通用性权衡：文本和 primitive 通用但控制粗糙；末端位姿精确却绑定机器人和坐标系；mask 受遮挡影响，mesh 又难从野外视频规模化恢复。长期挑战是高自由度交互生成，本文具体缺口是缺少可同时处理人手和机器人数据的统一动作条件。

### 研究动机

作者把动作“渲染”为相机平面中的主体结构，选择 2D 骨架作为获取成本与几何精度的折中。机器人关节状态和人类 MANO 手部姿态都能被转成同格式视频条件，从而联合学习 ego human video 与 robotic video 的交互动力学。

### 技术方案

- **输入：** 初始图像、动作序列、scene caption 和目标视频；机器人侧使用关节/相机参数，人类侧使用手部视频。
- **过程：** HOI 视频经 WiLoR、SAMURAI 和 OneEuro filter 得到平滑手部骨架；机器人轨迹在模拟器重放并渲染，经 MatchAnything 与 homography 校正。骨架视频由 3D 卷积编码；CogVideoX 前 14 个 block 复制为 ControlNet，零初始化注入控制，并以 LoRA 微调主 DiT。
- **输出：** 25 帧、720×480 的动作条件视频；单模型覆盖 EgoVid、RT-1 和 DROID。

### 实验结果

训练使用 EgoVid 200k、DROID 47k、RT-1 57k clips。DROID 上 text/raw state/skeleton 单域/skeleton 联合的 FVD 为 248.3/151.2/141.8/124.4，ST-IoU 为 0.239/0.365/0.450/0.478；novel lab 的 J&F 为 26.9/33.4/52.5/54.9。RT-1 联合训练的 FVD 优于单域（258.1 vs 288.6），但 PSNR、SSIM、LPIPS、ST-IoU 均略差，因此联合训练并非全面领先。

表示消融中 DROID skeleton/mesh/depth 的 FVD 为 141.8/120.4/119.7，说明骨架不是最精确条件，其优势是易获取和可扩展。去掉 ControlNet 后 FVD 165.2，去掉主分支注入为 146.9，完整为 141.8。EgoVid 测试仅人工选 32 clips；论文未报告 GPU、训练步数或时长，也没有真实机器人闭环成功率。

### 总结讨论

最可靠结论是“相机对齐的视觉动作条件优于抽象动作条件”，不是“骨架永远最佳”。VAP 提供了连接人手与机器人视频的实用接口，但 2D 结构缺少深度和接触力学，预处理误差也会直接污染条件。

### 代码与数据

论文与项目页公开；未核验到官方训练代码、权重或处理后骨架标注下载。原始 EgoVid、RT-1、DROID 的开放状态不能替代本文处理资产。

### 局限、失败案例与开放问题

- 2D prompt 的三维与接触信息有限。
- 手部恢复、跟踪、标定和 homography 误差会级联。
- EgoVid 测试集仅 32 clips，存在选择偏差风险。
- 未报告算力与关键训练超参数。
- 只验证离线视频指标，没有闭环控制证据。

## 5. OSCAR: Omni-Embodiment Action-Conditioned World Model for Robotics

**作者：** Zhuoyuan Wu, Jun Gao
**年份与发表：** 2026，arXiv preprint
**arXiv / DOI：** 2606.04463；未核验独立 DOI
**类别标签：** skeleton action, omni-embodiment, policy evaluation, human-robot video
**可靠入口：** [arXiv](https://arxiv.org/abs/2606.04463)｜[项目](https://wuzy2115.github.io/oscar-project-page/)｜[代码](https://github.com/wuzy2115/oscar-public)｜[模型](https://huggingface.co/zywu2115/OSCAR-2B)｜[数据](https://huggingface.co/datasets/zywu2115/OSCAR_robot)
**代表图：** OSCAR，Fig. 1，生成 rollout 与真实 RoboArena 策略评估的对应关系。来源：[Fig. 1 原图](https://arxiv.org/html/2606.04463/x1.png)

![OSCAR Fig. 1](https://arxiv.org/html/2606.04463/x1.png)

### 当前挑战

动作条件视频模型面临帧级动作跟随不准、机器人数据场景有限、动作条件绑定具体本体三类问题。latent action 会压缩掉空间定位，密集 mesh 易绑定外观，仅画末端又缺少整臂运动。本文针对的缺口是同时统一机器人和人手，并为真实策略评估提供足够稳定的 rollout。

### 研究动机

二维运动学骨架只依赖拓扑与相机投影，不携带纹理；改变 URDF/MANO 拓扑即可表示不同机器人或人手。作者再通过大规模清洗和去重缓解数据覆盖问题。与 VAP 相邻且直接相关：VAP 强调跨域 action-to-video，OSCAR 更强调数据工程与策略排序。

### 技术方案

- **输入：** 首帧、caption、机器人关节或 MANO 姿态、运动学树、相机参数和目标视频。
- **过程：** 前向运动学投影 link 原点并绘制关节、父子边与夹爪状态；骨架和视频经 Wan VAE 编码，latent patch embedding 后相加，Cosmos-Predict2.5-2B 用 rectified flow 训练。数据经过长度、静态相机、动作、可见性过滤，再用 SigLIP 与轨迹 RMS 去重；先机器人训练 15k iterations，再 warm-start 混入人类数据。
- **输出：** 81 帧未来视频；策略评估时由 GPT-5 判断成功与进度。

### 实验结果

2,165,359 原始 episodes 过滤为 180,657（机器人 94,830、人类 85,827），涵盖四种机器人及多个 ego 数据源。200-clips 测试中 OSCAR 的 PSNR 24.24、LPIPS 0.094、FVD 7.08、FPS 2.214；Genie Envisioner 为 23.29/0.140/15.37，但其 tLPIPS 更优（0.007 vs 0.015），OSCAR 在 AIROA-MoMa 子集也非最佳。

条件消融中 latent action/mesh/skeleton 的 FVD 为 12.03/7.89/7.69；骨架与 mesh 像素指标接近，主要优势是跨本体兼容。RoboArena 65 sessions×7 policies：骨架的 Spearman 0.750、Pearson 0.852、成功率绝对误差 1.73 pp；latent action Pearson 0.867 略高，不能写成骨架所有指标最佳。GPT-5 与 100 个真人标注的一致率 78%，recall 仅 0.66。训练为单张 GH200，未报告 wall-clock。

### 总结讨论

OSCAR 证明清洗后的混合人类—机器人数据和无纹理骨架可形成可迁移条件，并给出较强策略排序证据。但它依赖准确标定，评估器又依赖 GPT-5；生成世界尚不能完全替代真实评测。

### 代码与数据

代码、OSCAR-2B 权重和机器人数据已公开。混合数据包含多种 CC 许可证，不能统一视为可商业使用；人类数据应以实际下载页及许可证为准。

### 局限、失败案例与开放问题

- 依赖准确相机参数和运动学标注。
- 主要筛选静态相机，不覆盖普遍 ego camera motion。
- GPT-5 成功判定 recall 仅 0.66。
- 测试仅 200 clips、四种机器人，覆盖仍有限。
- RoboArena 只保留标定较好的 sessions，可能有选择偏差。

## 6. TraceGen: World Modeling in 3D Trace Space Enables Learning from Cross-Embodiment Videos

**作者：** Seungjae Lee, Yoonkyo Jung, Inkook Chun, Yao-Chih Lee, Zikui Cai, Hongjia Huang, Aayush Talreja, Tan Dat Dao, Yongyuan Liang, Jia-Bin Huang, Furong Huang
**年份与发表：** 2026，CVPR 2026（arXiv 2025）
**arXiv / DOI：** 2511.21690；未核验独立 DOI
**类别标签：** 3D trace, cross-embodiment video, geometric world model, few-shot adaptation
**可靠入口：** [arXiv](https://arxiv.org/abs/2511.21690)｜[项目](https://tracegen.github.io/)
**代表图：** TraceGen，Fig. 1，TraceForge 数据引擎、3D trace 世界模型与人机迁移。来源：[Fig. 1 原图](https://arxiv.org/html/2511.21690/x1.png)

![TraceGen Fig. 1](https://arxiv.org/html/2511.21690/x1.png)

### 当前挑战

人类和异构机器人视频丰富，却有本体、相机、尺度、速度与环境差异；像素世界模型昂贵且可能产生几何幻觉，VLM token 又缺精细时空分辨率。既有 trace 方法常停留在 2D、静态相机或依赖检测器的目标中心轨迹。

### 研究动机

不同本体不可共享关节动作，但被操作物体、末端和工具的场景级 3D 运动具有共同结构。TraceGen 因此预测“世界中什么点怎样移动”，而非主体外观或关节命令；这是把 geometry action 扩展到 ego human、robot 和不同环境的直接方案。

### 技术方案

- **输入：** 单帧 RGB、深度与语言；TraceForge 接收未标定人类/机器人视频。
- **过程：** TraceForge 用 CoTracker3、TAPIP3D、VGGT/SpatialTrackerV2 将 20×20 点轨迹变换到参考相机，补偿相机运动并按弧长重采样。TraceGen 冻结 DINOv3、SigLIP、T5，以 CogVideoX 风格 3D Transformer 和 flow matching 生成 400×32×3 trace increments，100 步 ODE；逆运动学转为执行命令。
- **输出：** 未来 32 时刻、覆盖机器人/物体/工具的 3D traces，以及经 IK 得到的目标机器人动作。

### 实验结果

TraceForge-123K 含 123k 视频、约 1.8M observation–trace–language triplets。Franka 四任务每设置每任务 10 trials：只用 5 个目标机器人视频 warm-up 时从头训练 25%，TraceGen 80%；15 视频为 30% vs 82.5%。只用 5 个未标定手机人类视频时 67.5%，从头训练 0%。预训练来源消融在 Ball/Block 上 scratch/SSV2/Agibot/完整为 0/25/45/70%。

9 episodes 的 3D sanity check 平均运动 70.96 cm，终点绝对误差 x/y/z 为 1.66/1.79/2.26 cm。0.67B 模型比 trace baseline 快 3.8×、比大型视频模型快 50×以上；Wan2.2 超过 600×。训练 GPU 与总成本未报告。长时抓取包含 scripted component，不应归因于 TraceGen。

### 总结讨论

TraceGen 强力支持“场景级 3D 运动是跨本体中间语言”，且少样本与速度优势明确；但执行依赖深度校正、坐标变换、IK 与 scripted grasping，不是完全端到端。真实试验每格仅 10 次，置信度有限。

### 代码与数据

项目页公开并描述 TraceForge-123K；未核验到代码、权重或数据下载入口，不能写成已开源。

### 局限、失败案例与开放问题

- 自动处理仍保留失败、纠错与低效动作噪声。
- 新本体可能生成视觉合理但不可执行的轨迹。
- trace 对精细接触可能过粗，未显式建模力。
- 评估形态有限，执行依赖 IK 与 scripted grasp。
- 未研究多模态轨迹模式选择及更多生成 schedule。

## 7. μ₀: A Scalable 3D Interaction-Trace World Model

**作者：** Seungjae Lee, Yoonkyo Jung, Jusuk Lee, Jonghun Shin, Amir Hossein Shahidzadeh, Yao-Chih Lee, H. Jin Kim, Jia-Bin Huang, Furong Huang
**年份与发表：** 2026，arXiv preprint
**arXiv / DOI：** 2606.13769；未核验独立 DOI
**类别标签：** semantic 3D trace, video-only pretraining, action expert, cross-embodiment
**可靠入口：** [arXiv](https://arxiv.org/abs/2606.13769)｜[项目](https://mu0-wm.github.io/)
**代表图：** μ₀，Fig. 1，从异构视频提取语义 3D interaction traces 并复用于 action expert。来源：[Fig. 1 原图](https://arxiv.org/html/2606.13769/x1.png)

![μ₀ Fig. 1](https://arxiv.org/html/2606.13769/x1.png)

### 当前挑战

固定网格 trace 浪费预算在背景并漏掉接触点；局部/2D 轨迹混淆相机和物体运动，episode caption 又不能描述局部子目标。原始 waypoint 噪声大，且世界模型视频预训练需要与本体动作监督解耦。

### 研究动机

μ₀ 将 TraceGen 的固定网格升级为语义交互点，把 episode caption 改为事件级语言，并让 action expert 直接消费 trace-denoising features。目标是从无动作视频学可复用运动先验，再以小型本体模块解码动作；与本专题直接相关。

### 技术方案

- **输入：** RGB、语言、1–256 个无序 keypoint query，可选深度和 8 步历史 trace。
- **过程：** TraceExtract 用 DINOv2 聚类实体，VGGT+TAPIP3D 做全局 3D 对齐，以运动事件切分并生成层级 caption。SmolVLM2-2.2B 前 20 层与 20 层 Trace Expert 联合条件化；每条未来 32 步 trace 用 10 个三次 B-spline 控制点，经 semantic flow matching、validity 与 rigidity loss 生成，4 步 Euler 解码。冻结 μ₀ 后，action expert 读取一次部分去噪特征并用 flow matching 输出 action chunk。
- **输出：** 平滑、可变查询的未来 3D traces，或目标本体动作块。

### 实验结果

3D trace、T=32 的 top-5 ADE/FDE/DTW：μ₀ 0.239/0.305/0.223，TraceGen 0.325/0.370/0.299，Dream2Flow 0.336/0.403/0.329。单 A6000 推理 0.29 s，TraceGen 1.20 s、Dream2Flow 106.8 s；μ₀ 为 2.59B。

RoboCasa365 8 任务，每任务 100 demos、50 eval：μ₀ 30.25%，Diffusion Policy 22.75、π0 25.25、π0.5 42、TraceGen+expert 23。真实 UR3 三任务分别 90/80/50 demos、每任务 20 次，μ₀ 平均 91.7%，但仅同一双指夹爪。B-spline 消融的 T=32 top-5 DTW 0.223 vs 0.258；模型 342M→568M→2.59B 为 0.240→0.227→0.223。数据 scaling 并非每个时域严格单调。预训练 2 张未注明型号 GPU、200k steps；RoboCasa expert 为 4×L40S、50k steps。

### 总结讨论

μ₀ 在表示、速度与 action-feature interface 上系统升级 TraceGen，但 RoboCasa 绝对成功率仅 30.25%，显著低于 π0.5。真实结果强但本体单一，因此支持视频预训练迁移运动结构，不足以证明广泛跨本体动作泛化。

### 代码与数据

项目页与论文公开；未核验代码、checkpoint 或 TraceExtract 数据入口，绝对训练数据规模也未披露。

### 局限、失败案例与开放问题

- 聚类、3D 重建、跟踪和 caption 存在级联伪标签误差。
- trace 没有显式力、触觉与接触模式。
- 下游集中于桌面操作，移动机器人与灵巧手未验证。
- RoboCasa 成功率仍低于 π0.5。
- 真实实验仅 UR3 双指夹爪，跨本体结论有限。
## 8. Latent Policy Steering with Embodiment-Agnostic Pretrained World Models

**作者：** Yiqi Wang, Mrinal Verghese, Jeff Schneider
**年份与发表：** 2025，arXiv preprint（项目页标记 under review）
**arXiv / DOI：** 2507.13340；10.48550/arXiv.2507.13340
**类别标签：** optical flow, embodiment-agnostic action, world model, policy steering
**可靠入口：** [arXiv](https://arxiv.org/abs/2507.13340)｜[项目](https://yiqiwang8177.github.io/LatentPolicySteering/)｜[AlphaXiv](https://www.alphaxiv.org/abs/2507.13340)
**代表图：** Latent Policy Steering，Fig. 1，光流世界模型预训练与候选策略 steering。来源：[Fig. 1 原图](https://arxiv.org/html/2507.13340v1/x1.png)

![Latent Policy Steering Fig. 1](https://arxiv.org/html/2507.13340v1/x1.png)

### 当前挑战

目标机器人专家示范昂贵，跨机器人和人类视频又因动作/本体状态不兼容而难以共享。普通 policy steering 的价值函数只在专家状态训练，却要给策略偏离分布后的 imagined states 打分，容易外推过度乐观。

### 研究动机

作者观察到不同本体执行相似技能时会产生相似视觉运动，因此用光流取代本体专属动作来预训练世界模型；目标本体只需少量数据把同一接口替换成归一化机器人动作。与 FlowWAM 的“预测 flow 再解码动作”不同，本工作把 flow 用作预训练期世界模型的输入动作，并在部署时通过世界模型给 BC 候选排序。

### 技术方案

- **输入：** 跨本体机器人/人类视频、小规模目标机器人专家集，以及 diffusion policy 生成的多个候选动作块。
- **过程：** 卷积编码器把相邻帧光流压成与目标动作维数相同的向量，与 Dreamer v3 RSSM 联训；适配时移除光流编码器，直接输入目标动作。价值函数在专家状态及世界模型模拟的 OOD 状态上训练，并以策略轨迹和专家 latent 的余弦偏离作为惩罚。推理对多个候选 rollout，执行价值最高者。
- **输出：** 被选中的目标机器人动作计划；世界模型不直接生成动作。

### 实验结果

Robomimic 的 30/50-demo 设置覆盖 Lift、Can、Square、Transport、3 seeds。50-demo 时 BC 平均 57.3，LPS-mix 63.4；Transport 25.8→34.6。30-demo 时平均仅 33.2→35.5，部分方法下降，说明 base policy 候选缺乏多样性会限制 steering。100-demo 价值消融中 BC 62.9、vanilla 65.2、bootstrap 64.3、完整 LPS 68.7；正文声称两种消融低于 BC 与表格矛盾，应以表为准。

真实 Franka 四任务、每设置 20 次，作者报告 30–50 条示范相对提升 70%、60–100 条提升 44%；可解析表格列有错位，不能可靠重建逐任务数字。Flow 预训练在 50-demo 平均 62.4，EEF 为 59.1。horizon 24 时低于 BC，显示长 rollout 噪声。未报告 GPU、参数规模或实时频率。

### 总结讨论

证据支持“跨本体世界模型预训练 + 候选筛选”在中等数据量下有效，但没有证明光流形成通用动作语义。真实实验样本小，模拟方差较大，推理还需多候选 rollout；适合作为低数据 policy enhancement，而非直接替代控制器。

### 代码与数据

项目页公开，代码仅承诺后续发布；未核验到官方仓库、权重、过滤后的 Open X-Embodiment 子集、人类 play 或 Franka 示范。名称相近的其他 LPS 仓库不是本文实现。

### 局限、失败案例与开放问题

- 遮挡、视角变化和移动相机破坏光流动作的一致性。
- 多候选 imagined rollout 增加推理延迟，未报告频率。
- horizon 过长时价值与偏离奖励变噪。
- 低数据 BC 可能近似单峰，使 steering 无候选可选。
- 真实试验次数有限，缺少置信区间。

## 9. PointAction: 3D Points as Universal Action Representations for Robot Control

**作者：** Mutian Tong, Han Jiang, Qiao Feng, Lingjie Liu, Jiatao Gu
**年份与发表：** 2026，arXiv preprint
**arXiv / DOI：** 2606.03943；未核验独立 DOI
**类别标签：** 3D point action, 4D generation, robot control, cross-embodiment
**可靠入口：** [arXiv](https://arxiv.org/abs/2606.03943)｜[项目](https://oriontmt.github.io/pointaction/)｜[代码](https://github.com/GMLR-Penn/PointAction)
**代表图：** PointAction，Fig. 1，RGB 与动态 3D pointmap 联合生成并解码动作。来源：[Fig. 1 原图](https://arxiv.org/html/2606.03943/x1.png)

![PointAction Fig. 1](https://arxiv.org/html/2606.03943/x1.png)

### 当前挑战

RGB rollout 无法唯一确定 metric 3D motion、接触几何与精细空间约束，因而难直接落地成动作；跨任务/本体收集 action supervision 又昂贵。本文针对的是“视频未来怎样变”与“目标机器人具体怎样动”之间的 grounding gap。

### 研究动机

作者把动态、像素对齐的 XYZ pointmap 作为通用中间动作：大型模型负责预测场景与机器人 4D 运动，小型本体专属 decoder 再映射低层动作。与纯几何输入 VLA 不同，这里的 3D points 是预测输出和控制接口，直接属于 geometry action。

### 技术方案

- **输入：** 当前 RGB 和语言；动作解码器另接生成视频中的机器人 XYZ 轨迹与当前本体状态。
- **过程：** 从 LVP 初始化，冻结 VAE 分别编码 RGB/XYZ，并在 latent 宽度拼接，以 LoRA+flow matching 联合生成。SAM 3 用“robot”提示分割生成 RGB，保留机器人表面 XYZ，每帧 FPS 采 512 点；PointNet 风格特征和 6-block DiT 以 DDIM 生成动作。
- **输出：** 49 帧 RGB、像素对齐 XYZ pointmap、目标机器人 49 步动作。

### 实验结果

预训练约 75k 轨迹（DROID 50k、BridgeData V2 25k）。RoboCasa365 的 ID/OOD-Env/OOD-Task 成功率为 47.7/44.1/17.0，Cosmos Policy 为 45.2/42.9/14.0；每单元 100 rollout。xArm7 三任务各 50 demos、100 tests，PointAction 平均 43.0%，π0.5 为 22.7%；YAM 各 20 demos/20 tests 也领先。

RGB-only 为 25.1/20.3，机器人 XYZ 37.2/30.9，联合生成机器人 XYZ 47.7/44.1；DA3 后处理 XYZ 仅 28.4/21.7，支持联合动态几何的重要性。公平性风险是 PointAction 使用额外深度、分割和 4D supervision，主表/附录的 GR00T 与 π 版本还有不一致。单次 49 帧生成在一张 B200 上约 6 分钟、40-step UniPC，不是实时闭环；未报告预训练总算力。

### 总结讨论

PointAction 对“3D 中间动作有助于控制”提供本专题最直接的真实机器人证据，但“universal”需要限定：每个新本体仍需专属 decoder 与数据。OOD-Task 绝对成功率仅 17%，CoffeeServeMug 甚至只有 2%，跨任务问题远未解决。

### 代码与数据

GitHub 已建立，但核验时 README 仍称代码整理中，不能视为完整开源。DROID、BridgeData V2 可获得；处理后的 75k 语料、真实数据和 checkpoint 未核验公开。

### 局限、失败案例与开放问题

- 单次推理约 6 分钟且 49 步开环，无法在线纠错。
- SAM 3 分割和自遮挡会破坏点轨迹。
- 深度伪标签可能有系统偏差。
- 新本体仍需数据、decoder 与后训练。
- OOD 任务成功率低，缺少统计显著性。

## 10. GeniWorld: A Generalizable Interactive World Model for Robotic Manipulation via Visual Actions

**作者：** Chenghao Gu, Hanyang Yu, Jingbo Zhang, Haitao Lin, Wenyao Zhang, Jinghe Wang, Hanglei Jin, Shuzhao Xie, Jingyan Jiang, Zhi Wang
**年份与发表：** 2026，arXiv preprint
**arXiv / DOI：** 2608.06332；未核验独立 DOI
**类别标签：** visual action, URDF rendering, interactive world model, synthetic data
**可靠入口：** [arXiv](https://arxiv.org/abs/2608.06332)｜[项目](https://chenghaogu.github.io/GeniWorld/)
**代表图：** GeniWorld，Fig. 1，视觉动作条件与闭环交互总览。来源：[Fig. 1 原图](https://arxiv.org/html/2608.06332/x1.png)

![GeniWorld Fig. 1](https://arxiv.org/html/2608.06332/x1.png)

### 当前挑战

数值动作缺乏像素空间锚定，视频模型需同时学习机器人运动学和环境响应，容易在新背景、物体与布局中过拟合。现实中扩展训练/评估环境昂贵，传统图像增强又不能产生新的可交互行为。

### 研究动机

GeniWorld 用 URDF 渲染把实施体运动学显式移出环境动力学学习：模型看到“机器人将在图像中怎样运动”，只需预测环境如何响应。目标是让少量固定场景数据训练的模型支持 OOD rollout、闭环人机交互、策略评估与合成轨迹。

### 技术方案

- **输入：** 初始/历史观测、数值动作、URDF、运动学与相机参数、语言和训练期未来视频。
- **过程：** 数值动作经正向运动学渲染为不含物体/背景的视觉动作；视频和动作由 causal 3D VAE 编码并按通道拼成 96-channel latent。Wan2.2-TI2V-5B causal DiT 仅对视频 latent 加噪，以 flow matching 预测；训练逐渐以生成帧替换真实上下文，推理用 KV cache 闭环。
- **输出：** 与动作一致的未来 RGB、可反馈给策略的交互环境，以及合成 observation–action trajectories。

### 实验结果

RoboTwin2.0 50 任务，Clean 每任务 45 train/5 test；Clean-to-Random 零适配使用 250 Random episodes。Clean-to-Random 的数值动作与 GeniWorld 分别为 LPIPS 0.3659/0.144、FID 40.91/13.08、FVD 53.69/20.15、EWMScore 51.49/63.54；ControlNet-style 视觉条件 FVD 59.95，说明表示与 latent 拼接方式都重要。

5-step、单 H20、480×640 闭环约 8 Hz；作者称相对 50-step 约 10× 加速且 FVD 只退化约 2%。世界模型训练用 4×H20，但未报告总步数/GPU-hours。合成数据实验每任务 25 real + 65 spatial + 65 diverse；四任务、五设置、共 1,200 次物理试验。仅真实数据 overall 40.8%，加入两类生成数据为 69.0%；但初始图像编辑与世界模型 rollout 同时变化，归因没有完全隔离。策略评估未报告相关系数和置信区间。

### 总结讨论

GeniWorld 对视觉动作的生成质量与合成数据价值给出较强证据，尤其是 Clean-to-Random 和真实策略改进；但“generalizable”目前主要指场景 OOD，不是跨机器人零样本。输出仍是视觉状态，没有力、触觉或碰撞保证。

### 代码与数据

论文与项目页公开；未核验到代码、权重、真实数据或完整训练配置。RoboTwin、Wan2.2 和 OpenPI 是外部资源，不等于 GeniWorld 已开源。

### 局限、失败案例与开放问题

- 真实实验仅双臂 Xtrainer，跨本体未验证。
- 依赖 URDF、正向运动学和相机标定。
- 策略评估没有公开相关系数与统计区间。
- 合成数据收益未隔离图像编辑和世界模型 rollout。
- 真实任务与视角覆盖有限，缺少力学状态。

## 11. iMaC: Translating Actions into Motion and Contact Images for Embodied World Models

**作者：** Zhenyu Wu, Xiuwei Xu, Yukun Zhou, Yifan Li, Qiuping Deng, Xiaofeng Wang, Zheng Zhu, Bingyao Yu, Ziwei Wang, Jiwen Lu, Haibin Yan
**年份与发表：** 2026，arXiv preprint
**arXiv / DOI：** 2606.09813；未核验独立 DOI
**类别标签：** motion image, contact image, embodied world model, policy evaluation
**可靠入口：** [arXiv](https://arxiv.org/abs/2606.09813)｜[项目](https://imac-wm.github.io/)
**代表图：** iMaC，Fig. 1，动作转换为 motion images 与 contact images 的整体流程。来源：[Fig. 1 原图](https://arxiv.org/html/2606.09813/x1.png)

![iMaC Fig. 1](https://arxiv.org/html/2606.09813/x1.png)

### 当前挑战

离线策略评估要求世界模型区分厘米级动作差异导致的抓住、错过或碰撞。低维动作没有直接指明机器人将出现在哪里、与物体多远；仅渲染机器人运动仍无法消除 2D 重叠下的深度和接触歧义。

### 研究动机

iMaC 把动作翻译成两类图像：motion image 给出未来机器人外观/位置，双向 contact image 给出未来机器人与当前场景的 3D 距离。核心 Insight 是让视频生成器显式读取“谁移动到哪里”和“哪里可能接触”，用于分钟级 rollout 与策略 checkpoint 排序。

### 技术方案

- **输入：** 头部与双腕 RGB、语言、未来关节动作、URDF、关节状态、相机参数和 DA3 初始深度。
- **过程：** 三视角拼 mosaic；控制器与正向运动学渲染未来机器人 motion images。移除当前机器人并构造场景点云，再计算 robot→scene 与 scene→gripper 最近距离场，投影为两路 contact images。三类控制 latent 注入 Wan2.2；模型联合预测 RGB/彩色深度，并以训练期生成参考缓解分块 rollout 的 exposure bias。
- **输出：** 多视角 RGB/深度长视频，以及由 rollout 得到的策略成功分数与排序。

### 实验结果

八项真实长时任务混合成功/失败数据，π0.5 与 GigaBrain-0.5 各取早中晚 checkpoint，每评估组 30 episodes；先联合训练再逐任务微调，最终不是单一通用模型。iMaC 的 MSE/FID/PSNR/SSIM/FVD 为 0.028/36.96/16.39/0.735/489.51，Ctrl-World 为 0.030/48.64/16.22/0.730/591.47；去掉 contact images 的 FVD 523.94，说明接触场主要改善时序质量。

世界模型分数与真实成功率的八任务 Pearson 为 0.956、0.931、0.678、0.915、0.428、0.870、0.856、0.833；两项涉及相机难观察的高度关系，明确暴露观测盲区。相关性只来自两个策略族×三个 checkpoint，且没有 CI、p 值或 Spearman。论文未披露数据规模、GPU、时延与训练成本。

### 总结讨论

iMaC 展示了接触几何条件对策略评估的潜力，但相机看不到关键高度时相关性会降至 0.428。它只能补充而不能替代真实评测；逐任务微调和未披露算力也限制规模化。

### 代码与数据

论文与项目页公开；未核验到完整代码、权重、训练数据或评测脚本。

### 局限、失败案例与开放问题

- 依赖 URDF、精确标定和深度；DA3 误差会改变接触时序。
- 相机盲区会生成视觉合理但物理错误的结果。
- 分块生成仍会累积模糊与动作漂移。
- 每任务单独微调，不是通用单模型。
- 仅两个策略族，相关性的泛化与统计稳定性不足。

## 12. Robot-Factored World Models via Robot Rendering

**作者：** Byungjun Kim, Taeksoo Kim, Hyunsoo Cha, Hanbyul Joo
**年份与发表：** 2026，arXiv preprint
**arXiv / DOI：** 2607.22535；未核验独立 DOI
**类别标签：** robot rendering, nominal trajectory, leakage audit, cross-embodiment
**可靠入口：** [arXiv](https://arxiv.org/abs/2607.22535)｜[项目](https://bjkim95.github.io/rofacto/)｜[代码](https://github.com/bjkim95/rofacto)
**代表图：** Robot-Factored World Models，Fig. 1，静态场景上下文与名义机器人渲染组成视觉动作接口。来源：[Fig. 1 原图](https://arxiv.org/html/2607.22535/x1.png)

![Robot-Factored World Models Fig. 1](https://arxiv.org/html/2607.22535/x1.png)

### 当前挑战

直接条件化原始命令要求世界模型同时学习控制器如何实现动作；条件化日志中的未来关节状态则泄漏接触、延迟和纠错结果。长期挑战是动作条件视频的可部署性，本文具体缺口是缺少既反映机器人运动、又不偷看未来结果的中间变量。

### 研究动机

作者提出“名义轨迹”：在无场景交互时，用部署可用的控制器与运动学把动作实现成轨迹，再渲染成相机对齐机器人几何。它将 action realization 和 embodiment geometry 移出网络，让模型专门预测环境响应，并首次清晰审计 logged future state leakage。

### 技术方案

- **输入：** 当前场景 RGB/深度、动作、初始关节状态、控制器、URDF、相机轨迹和不泄漏结果的文本。
- **过程：** 在无碰撞环境中重放动作得到名义关节轨迹，渲染机器人 RGB mesh 与末端深度；静态场景 RGB/深度和机器人几何经 VAE 后与噪声视频拼接。Wan2.1-Fun 14B inpainting 模型以 LoRA+flow matching 训练。
- **输出：** 给定名义机器人运动后的交互视频；可组合未见机器人几何与重定向的人类动作。

### 实验结果

DROID 41,642 clips、RoboCasa-GR1 9,380 clips；测试 256/128 clips。Wan backbone 下 AdaLN 状态向量与 mesh+EEF/场景深度在 DROID 的 PSNR/LPIPS 为 18.57/0.224 vs 21.87/0.178，RoboCasa 为 17.67/0.194 vs 24.61/0.131。名义 mesh 相对原始动作 mesh 的 DROID PSNR 21.57→22.44，加入深度到 23.08。

泄漏审计中 DROID nominal→nominal、logged→logged oracle、logged train→nominal test 的 LPIPS 为 0.179/0.174/0.187；RoboCasa 为 0.120/0.112/0.126。oracle 条件最好但不可部署，训练/部署错配最差，支持名义条件定义。跨 xArm6、双 Franka 与人手重定向仅定性。论文未报告 GPU、训练步数或延迟。

### 总结讨论

RoFacto 最重要的贡献不是更高 PSNR，而是区分动作命令、部署可用名义轨迹和泄漏未来结果的 logged state。结果证明条件一致性重要；但名义轨迹仍忽略接触后的顺应性与执行误差，跨本体只证明接口可组合，未证明物理预测准确。

### 代码与数据

项目页和仓库公开，但核验时仓库仍标记 “Code coming soon”。基础数据公开；处理 clips、名义轨迹缓存和渲染资产未核验发布。

### 局限、失败案例与开放问题

- 每个机器人都需 URDF、控制器和相机—机器人标定。
- 名义轨迹不表达接触后的真实顺应与偏差。
- 仅报告重建指标，缺少任务成功与接触准确率。
- 跨本体与人类重定向只有定性证据。
- 失败、滑落和卡住等尾部数据不足。

## 13. Scaling Cross-Embodiment World Models for Dexterous Manipulation

**作者：** Zihao He, Bo Ai, Tongzhou Mu, Yulin Liu, Weikang Wan, Jiawei Fu, Yilun Du, Henrik I. Christensen, Hao Su
**年份与发表：** 2025，arXiv preprint
**arXiv / DOI：** 2511.01177；未核验独立 DOI
**类别标签：** particle displacement action, dexterous manipulation, cross-embodiment, MPC
**可靠入口：** [arXiv](https://arxiv.org/abs/2511.01177)｜[项目](https://alan-heoooh.github.io/dexwm.html)
**代表图：** Scaling Cross-Embodiment World Models for Dexterous Manipulation，Fig. 1，粒子状态与末端粒子位移统一不同手型。来源：[Fig. 1 原图](https://arxiv.org/html/2511.01177/x1.png)

![Scaling Cross-Embodiment World Models for Dexterous Manipulation Fig. 1](https://arxiv.org/html/2511.01177/x1.png)

### 当前挑战

多指手的自由度、关节定义与控制空间不同，动作标签不能直接合并；接触丰富的刚体/可变形体操作还叠加高维控制与 sim-to-real gap。本文针对既有跨本体工作多局限于抓取、重定向或平行夹爪，缺少真正共享的状态—动作空间。

### 研究动机

作者主张跨本体可共享的不是关节动作，而是对环境产生的物理交互。将人手、机器人手和物体统一成 3D 粒子，动作定义为末端粒子位移，就能把不同 DoF 的控制映射到同一几何接口，并用一个图世界模型加 MPC 部署。

### 技术方案

- **输入：** 手与物体 3D 粒子、候选关节动作、目标物体点云。
- **过程：** 前向运动学把动作变为粒子位移；DPI-Net 半径图进行局部消息传播并预测下一粒子状态，仿真用 MSE、无对应真实点云用 Chamfer/EMD。MPC 每次采样 500 个 horizon-4 序列、优化 10 次，执行 2 步后重规划。
- **输出：** 物体粒子未来和目标机器人原生关节空间中的控制动作。

### 实验结果

六种模拟手、两类刚体/塑形任务，每手每任务 100 条随机轨迹；真实人类 ThumbPinch/FingersPinch/PalmPress 各 30 分钟。论文以均值和 95% CI 显示训练本体越多，未见手 MSE 与组合方差总体下降，但图中没有精确点值，不宜编造 scaling law 数表。

真实塑形每手 4 字母×5 trials。Ability Hand co-train 18/20、human-only 10/20；XHand 17/20 vs 9/20。平衡约 1:1 sim/human 最好，simulation-only 最差，支持仿真是正则而非真实替代。RTX 4090 每次 MPC 更新约 60 秒，不适合高频闭环；系统还依赖四相机与人工动作原语。

### 总结讨论

这篇不依赖视频生成，直接证明粒子位移可作为跨手型共享 action abstraction。本体多样性和 sim-real 共训结果有价值，但证据集中在塑形、两种真机手与四个目标，且在线规划极慢；它是“geometry action”的强概念验证，而非通用实时策略。

### 代码与数据

项目页与论文公开；未核验代码、权重、随机交互数据或 90 分钟人类数据下载。

### 局限、失败案例与开放问题

- 半径图对手尺寸与粒子密度敏感。
- sim-only 表现差，接触参数 reality gap 未解决。
- MPC 每次约 60 秒，无法实时。
- 依赖四相机、网格/点云重建和 FoundationPose。
- 真实任务和手型有限，并依赖人工动作原语。

## 14. EA-WM: Event-Aware Generative World Model with Structured Kinematic-to-Visual Action Fields

**作者：** Zhaoyang Yang, Yurun Jin, Lizhe Qi, Kai Chen, Cong Huang
**年份与发表：** 2026，arXiv preprint
**arXiv / DOI：** 2605.06192；未核验独立 DOI
**类别标签：** kinematic visual action field, event-aware world model, robot video
**可靠入口：** [arXiv](https://arxiv.org/abs/2605.06192)

### 当前挑战

低维动作 token 缺少目标视角中的机器人几何、深度和接触位置；即使增设动作分支，普通融合也可能忽略物体真正发生变化的交互事件。本文具体针对“动作空间—视频空间错位”和“双流只交换一般特征而不聚焦事件”。

### 研究动机

作者把关节动作与运动学状态投影成 Structured Kinematic-to-Visual Action Fields（KVAF），再用帧差监督 event gate。核心 Insight 是同时对齐表示空间和信息交换时机；与本专题直接相关，但 KVAF 是高带宽生成条件，不是数值动作的无损编码。

### 技术方案

- **输入：** 首帧、语言、双臂关节/夹爪/末端位姿、URDF、相机参数和目标视频。
- **过程：** 前向运动学与投影生成深度骨架、landmark、夹爪几何、末端热图和 RGB 位姿轴；RGB/KVAF 用同一 Wan2.2 VAE。两个 full-depth DiT 流在稀疏层双向 cross-attention；共享 event MLP 用相邻 RGB 绝对帧差 latent 监督门控。两阶段先训 LoRA/KVAF head，再解冻 fusion。
- **输出：** 未来 RGB 与可解释 KVAF 序列；启发式动作恢复仅是附加分析。

### 实验结果

WorldArena/RoboTwin 的六项 P3CScore 上 EA-WM 为 76.60，最强总体基线 CogVideoX 为 71.08。EA-WM 的 Interaction/Trajectory/Depth/Perspectivity/Instruction 为 0.682/0.430/0.959/0.838/0.792，均领先；Semantic 0.895 略低于 CogVideoX 0.898，所以不是六项全胜。Wan2.2、无 KVAF、无 EAF、完整模型为 60.83/70.97/74.80/76.60，支持 KVAF 是主要增益来源。

动作恢复中 raw-action baseline 的 translation/rotation/gripper 误差为 0.004/0.009/0.013，KVAF recovery 为 0.0155/0.110/0.039，检测率约 0.45，说明视觉场不适合精确反演控制。训练使用 32×H100、LoRA rank 32、batch 32；未报告步数和 GPU-hours，也无真机闭环实验。

### 总结讨论

EA-WM 的受控结果支持相机对齐视觉场改善轨迹与几何、事件融合进一步改善综合一致性。证据局限于模拟视频评测；高算力、完整标定和双 DiT 流使其更像高成本视觉模拟器，而非已验证的实时控制接口。

### 代码与数据

未核验到官方代码、权重或 KVAF 处理数据。实验依赖 WorldArena/RoboTwin，不代表本文实现已经开放。

### 局限、失败案例与开放问题

- 依赖 URDF、同步状态日志和准确相机标定。
- KVAF 只显式编码机器人，对象接触仍由模型隐式学习。
- 动作恢复检测率约 0.45，不能替代原始控制量。
- 仅模拟基准，无真实闭环策略验证。
- 32×H100 且缺少训练时长，复现成本不透明。
