# Galaxea G0.5 与 FlowWAM：自回归 VLA 与光流动作表征整理

**报告标签**：World Action Model, VLA, 机器人学习  
**检索与核对日期：2026-08-21**  
**阅读范围：** 两篇均核对其 arXiv HTML 全文（含方法、实验、附录要点）、项目页和官方 GitHub；不是仅依据标题或摘要。二者均为 2026 年 arXiv 预印本，尚未见正式会议/期刊版本。

> 两篇工作同属机器人控制，但接口不同：G0.5 让 VLM 在同一自回归流中同时生成推理与动作 token；FlowWAM 把光流视频当作 WAM 的统一动作表征，同时服务策略解码与动作条件世界建模。二者都不是结构因果或反事实识别工作。

---

## 1. Galaxea G0.5: One Autoregressive Stream for Robot Reasoning and Action

**作者：** Yicheng Liu, Zibin Dong, Baijun Ye, Tianyuan Yuan, Tao Jiang, Anqi Yang, Shicheng Cao, Haonan Liu, Yue Sun, Zihan Guo, Xiao Liu, Ke Dong, Changxun Pan, Chenru Wu, Tailai Cheng, Xiaoshu Ren, Xinlei Zhang, Jianning Cui, Zijie Zhao, Haoyu Zhang, Kaiming Xu, Haodong Yang, Bowen Zhang, Jiahui Niu, Shaoting Zhu, Shiduo Zhang, Hang Zhao  
**年份与发表：** 2026，arXiv preprint（v1，cs.RO）；arXiv HTML 署名 Galaxea Team，项目负责 Yicheng Liu，PI Hang Zhao。GitHub 新闻记论文于 2026-08-12 上线。尚无 DOI / 正式出版页。  
**可靠入口：** [arXiv](https://arxiv.org/abs/2608.11739)｜[HTML 全文](https://arxiv.org/html/2608.11739)｜[项目页](https://opengalaxea.github.io/G05/)｜[代码](https://github.com/OpenGalaxea/GalaxeaVLA)｜[模型](https://huggingface.co/OpenGalaxea/G05)｜[AlphaXiv](https://alphaxiv.org/abs/2608.11739)  
**代表图：** Galaxea G0.5，Fig. 1，reasoning and action in one autoregressive stream。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2608.11739v1/teaser.png)

![Galaxea G0.5 Fig. 1: reasoning and action in one autoregressive stream](https://arxiv.org/html/2608.11739v1/teaser.png)

### 当前挑战

领域长期问题是：通用机器人策略既要继承大规模 VLM 的语言/感知能力，又要在高频、跨本体、长时程控制上可部署。本文针对的具体缺口是当前主流 VLA 配方把这两件事拆开了。

- **作者明确指出的失败模式：** 早期 RT-2 / OpenVLA 式自回归动作离散化，在控制频率、动作时域和动作维度上升后，逐步 token 数量爆炸，推理变慢、变贵。随后 \(\pi_0\) / \(\pi_{0.5}\) / GR00T 等把预训练 VLM 降为条件编码器，另训 flow-matching / diffusion action expert。VLM 不再是 actor，chain-of-thought、in-context learning 和 prompt 级动作调节只能穿过压缩条件瓶颈间接影响动作分布。
- **知识隔离信号：** 当 expert 梯度回传到 VLM 时，会出现 anti-forgetting；Knowledge Insulation 干脆切断梯度，再用 AR 动作预测作辅助目标。作者把它读成：AR 动作监督恰恰是保护 VLM 能力的信号，而不是该被丢掉的瓶颈。
- **分词缺口：** FAST 等对每个本体单独做固定 DCT pipeline；多数方法把整段动作压成一个向量再离散化，token 与形态结构不对齐，空闲关节仍占 token，语义相近动作的 Hamming 距离也大。
- **记忆缺口：** 单帧观测在遮挡和失败重试时不够；直接堆历史视觉 token 则二次方变贵，且未见过的时间轨迹容易漂移。

这些是架构与表征缺口，不是“再做一个更强的视频预测器”就能自动解决的问题。

### 研究动机

核心 Insight：**不要把越来越复杂的 action expert 架在被降级的 VLM 上，而应让 VLM 继续做它被预训练成的自回归推理器，同时在同一 token 流里行动。**

方法选择因此改变了三个接口：

1. **动作接口：** 学习式、跨本体的 ActionCodec / RVQ，把异构连续动作压成共享离散词表，并用 active-part tokenization 丢掉空闲控制组。
2. **推理接口：** Subtask / BBox / Trace / ActionHint 四种自描述 CoT 目标与动作码共用 decoder、上下文和 next-token 损失，而不是 bolt-on 规划模块。
3. **记忆接口：** 在 ViT 中插入分解的时空注意力，把数秒视觉历史注入视觉编码器，而不是在 LLM 侧无限堆图像 token。

与本知识库课题的关系：**强相关于机器人 VLA / 通用操作，与 World Action Model 是相邻对照而非同类。** G0.5 主实验把 Fast-WAM、LingBot-VA 等 WAM 当作成功率 baseline，但它本身不生成未来 RGB 世界，也不做 \(do(\cdot)\) 或反事实。可借鉴点是：跨本体动作分词、原生 CoT 与动作共用目标、以及“VLM 应否继续当 actor”这一接口争论。

### 技术方案

- **输入：** 多视角 RGB 短时窗、本体标识 \(e\)、自然语言指令 \(\ell\)、本体感觉 \(s_t\)；可选外部裁剪目标图或坐标 token。
- **过程：** 从 Qwen3.5-2B 初始化；全部序列化为一段 chat：条件段（图像 / 本体 / 任务 / 状态）+ 生成段（可选 CoT + 动作码）。单一 next-token 交叉熵只加在生成段，联合监督 CoT 与动作。动作码经冻结的跨本体 ActionCodec 解码到统一 27 维动作空间：left control 9 + gripper 1 + right control 9 + gripper 1 + lower body 7；空闲槽用 noop。CoT 从 8 种模板中采样（含 no-CoT），评估默认 no-CoT。视觉记忆每四层做分解时空注意力，训练时随机丢掉历史帧；可选附加 \(\pi_{0.5}\) 式 flow-matching 头作推理加速，主文默认仍是 AR。
- **输出：** 结构化离散动作码 → 连续电机指令；需要时同时输出子任务文本、物体框、2D gripper trace、动作提示。

与最近 baseline 的实质差异：相对 \(\pi_{0.5}\) / GR00T，VLM 不是条件编码器而是 actor；相对 OpenVLA / FAST，分词是学习式、按运动部件分组、只预测激活组；相对 ECoT，四种推理原语进入同一共享词表且可按 prompt 开关。预训练是单阶段混合：14 个本体的机器人数据 + web/embodied VQA；DROID 不进 foundation mix，评估时再 post-train。CoT 语言标注来自 Gemini 3 / Doubao 等自动标注，视觉框来自 MLLM + SAM3。

### 实验结果

**作者主张：** AR 主干在 7 个独立设定上匹配或超过最强 VLM-as-encoder、AR 和 WAM baseline；语言跟随和多阶段执行上优势更结构性。

实验实际支持（数字均来自原文表格/正文）：

- **真机 fine-tune（R1-Lite / R1-Pro，6 个 task–embodiment，各 15 episode，对齐 16×H20 墙钟）：** 平均成功率 **76.7%** vs \(\pi_{0.5}\) 53.3%、GR00T-N1.7 24.4%；process score 129.2 vs 105.2 / 68.9。R1-Pro 搬箱堆叠是例外：\(\pi_{0.5}\) 93.3% vs G0.5 80.0%。
- **2025 BEHAVIOR Challenge（50 长时程家务，单 checkpoint）：** Task Success Score，G0.5 1 epoch **0.2904**、4 epoch **0.3136**；\(\pi_{0.5}\) 4 epoch 0.2626；冠军 RLC 四 checkpoint 0.2605。作者强调这是单策略 vs 多 checkpoint 的不对等对照。
- **DROID post-train 后环境/物体 zero-shot（10 任务×10 trial）：** 平均 **82.5%** vs \(\pi_{0.5}\)-DROID 57.5%、MolmoAct2-DROID 52.0%。抽屉任务上，半透明柜体无高对比标记时 G0.5 仅 60%，贴橙色标记后到 100%；作者承认对低对比半透明表面更敏感。
- **仿真：** LIBERO 平均 **98.9%**（Long 98.6）；RoboTwin 2.0 Clean/Rand/Avg **93.7 / 92.8 / 93.3**；SimplerEnv-Bridge 平均 **87.3%**（部分 baseline 数字编译自既有论文，不是全部同代码重跑）。
- **PP Bench（64 次真机 trial）：** zero-shot 语言跟随 65.6%、任务成功 59.4%；50H post-train 分别为 84.4% / 75.0%，同设置下仍高于 \(\pi_{0.5}\) 的 68.8% / 65.6%。单阶段任务上 CoT 几乎无增益；五阶段 Air Fryer / Cook Bacon 零样本探测中，AR+CoT 的 progress 从 2.4→3.8 与 1.5→3.4。作者把 prompt 措辞能改变 rollout 写成定性探针，**不是**定量结论。
- **GRPO：** 每任务 1 条演示后，AR 比可选 FM 头收敛更快、终值更高、方差更低（Fig. 12）。这支持“AR 提供可直接用的 token log-prob”，不支持“FM 不能做 RL”。

**证据未支持：** 提示词即可零样本控制系统性地调节粒度/时域/OOD；lower-body 被单独评测；AR 消除了感知失败。

### 总结讨论

G0.5 把当代 VLA 的主分歧写清楚了：VLM-as-encoder 换来连续高频动作，却把推理能力隔在 expert 之外；G0.5 用压缩动作码把 AR 路线重新做大规模。真机、长时程家务和语言跟随上的数字支持“同一套权重同时推理和行动”这一工程主张。适用边界是操作式 VLA，不是世界模型，更不是因果识别。失败案例集中在抽屉/半透明柜、预训练偏 pick-and-place 导致的容器/电器交互偏弱、以及数秒级视觉记忆。阅读判断：适合作为跨本体 AR-VLA 和 LingBot-VA / Fast-WAM 的对照基线；引用时不要把 CoT 增益外推到单阶段任务，也不要把 BEHAVIOR 的单 checkpoint 优势直接写成击败了多策略冠军系统。

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

---

## 2. FlowWAM: Optical Flow as a Unified Action Representation for World Action Models

**作者：** Yixiang Chen, Peiyan Li, Yuan Xu, Qisen Ma, Jiabing Yang, Kai Wang, Jianhua Yang, Dong An, He Guan, Gaoteng Liu, Jianlou Si, Jun Huang, Jing Liu, Nianfeng Liu, Yan Huang, Liang Wang  
**年份与发表：** 2026，arXiv preprint（v1，cs.RO，2026-07-14）。通讯作者 Yan Huang、Liang Wang。尚无 DOI / 正式出版页。  
**可靠入口：** [arXiv](https://arxiv.org/abs/2607.13017)｜[HTML 全文](https://arxiv.org/html/2607.13017)｜[项目页](https://flow-wam.github.io/)｜[代码](https://github.com/YixiangChen515/FlowWAM)｜[模型](https://huggingface.co/YixiangChen/FlowWAM)｜[数据](https://huggingface.co/datasets/YixiangChen/FlowWAM_RoboTwin)｜[AlphaXiv](https://alphaxiv.org/abs/2607.13017)  
**代表图：** FlowWAM，Fig. 2，dual-stream RGB–flow diffusion overview。来源：[Fig. 2 原图 PNG](https://arxiv.org/html/2607.13017v1/method.png)

![FlowWAM Fig. 2: dual-stream RGB and optical flow generation](https://arxiv.org/html/2607.13017v1/method.png)

### 当前挑战

WAM 想借用预训练视频生成器的运动先验做控制，但动作必须同时满足两件事：格式贴合视频生成器，以及跨帧运动线索足够解码成可执行控制。本文针对的是这个表征缺口，而不是“视频生成还不够像真”。

- **数值动作 token**（DreamZero、Cosmos Policy、UWM、Fast-WAM 等）精确，但动作空间随本体变化，和像素先验不在同一模态。
- **学习 latent action**（Motus、LAPO 等）可跨本体，却往往丢掉稠密、空间对齐的运动。
- **图像空间动作**（ray map、mask、多视角 action image）把控制画进视觉域，但多是静态“在哪里动”，不是“每一可见部分如何随帧移动”，因此仍是帧级条件，而不是与未来视频一起演化的时间稠密动作流。
- 先前光流工作多把 flow 当 VLA 辅助监督、规划中间量或模块桥，**没有**把它放进视频生成器的生成 latent，同时充当策略目标和世界模型条件。

### 研究动机

核心 Insight：**把光流编码成与 RGB 同格式的视频，就可以作为 WAM 的统一动作表征——策略模式生成 flow 再解码动作，世界模型模式固定目标 flow 来引导未来 RGB，并且可以从无动作标签的自我中心视频里预训练。**

这改变的是动作/视频接口，不是再加一个更重的 RGB rollout 头：flow 与 RGB 共享冻结 VAE 和 DiT 主体，只保留轻量 stream-specific patch embedding 与输出头。与本知识库课题 **直接相关**：它明确站在 WAM 动作表征谱系上，对照数值 token、latent action 和静态图像动作，并在 RoboTwin / WorldArena 上同时测策略与世界模型。它建模的是像素位移场，**不是**结构因果或反事实。

### 技术方案

- **输入：** 参考 RGB \(I_0\)、语言指令 \(\tau\)；策略模式还要本体感觉。RoboTwin 阶段把头/左腕/右腕拼成 \(320\times 384\) 的 T 形拼图。
- **过程：** RAFT 提取光流，HSV 色轮编码 \(\phi\)（色相=方向，饱和度=幅度，\(m\) 为幅度归一化；在该归一化下可逆）。同一冻结 VAE 分别编码 RGB 与 flow latent；各 self-attention 层把两路 token 拼接做联合注意力再拆回，RoPE 分路施加。策略模式：两路后续帧从噪声联合去噪，action expert（约 780M AdaLN DiT，30 层）交叉注意各层 RGB+flow hidden state，用 flow matching 预测 \(N\) 步动作块；训练时以 \(p=0.5\) 向 expert 所见 latent 混噪声，以对齐推理时的残差去噪误差。世界模型模式：flow latent 固定为所需轨迹的干净 VAE 编码，只去噪 RGB。\(\mathcal{L}_{\text{video}}=(1-\lambda_f)\mathcal{L}_{\text{RGB}}+\lambda_f\mathcal{L}_{\text{flow}}\)，并对 flow 做 motion-aware 重加权以免背景主导。有动作标签时再加 \(\lambda_a\mathcal{L}_{\text{action}}\)。两阶段：EgoDex 无标签只训双流 DiT；再在 RoboTwin 上接入 action expert 联合训练。backbone 为 Wan2.2-TI2V-5B。
- **输出：** 策略模式 → 未来 RGB + flow 视频 + 可执行动作块；世界模型模式 → 与指定运动一致的未来 RGB。

与最近 baseline 的实质差异：Motus 用光流衍生的 **latent action**，FlowWAM 生成显式 flow **视频**；Fast-WAM 训练期有视频、测试期跳过 imagination 并走数值动作；X-WAM 用数值投影的动作/状态 latent 而非稠密图像空间 flow。RoboTwin 的 flow 监督来自 SAPIEN 中只重放机器人、去掉背景/物体运动后的 robot-only 渲染，腕部 flow 区域用占位常量，因为腕部 robot-only flow 不可用。

### 实验结果

**作者主张：** 同一套 flow 表征在策略、世界模型和无标签预训练三侧都带来增益，且策略增益可追溯到 flow 预测质量而非 decoder 捷径。

实验实际支持：

- **RoboTwin 2.0（50 任务，Clean 50 demo + Random 500 demo 合训，每任务 100 rollout）：** FlowWAM w/ PT 平均成功 **92.94% Clean / 92.14% Random**，高于表中 \(\pi_{0.5}\)、X-VLA、Motus、GigaWorld Policy、X-WAM、Fast-WAM；无 EgoDex 预训练仍有 82.40 / 80.80，说明 flow 流本身贡献大部分，预训练是放大器。Hanging Mug 等难任务仍明显低于均值（65/68）。这些数字与 G0.5 文中的 93.7/92.8 **不是同一套训练/评估脚本**，不宜直接排序成 SOTA 竞赛。
- **WorldArena（121 帧、24 fps）：** 总 EWMScore **63.71**，Trajectory Accuracy **64.26**（相对第二名约 +10 分，作者称轨迹精度相对提升 18.4%）。外观类 Subject/Background Consistency 接近但不全面领先。消融用自定义 validation split，与主表数字不一致，作者已注明。
- **真机（Franka 单臂 4 任务 + ARX 双臂 3 任务，各 100 条演示、10 trial）：** 平均 **75.7%** vs \(\pi_{0.5}\) 61.4%、Motus 57.1%；双臂任务差距更大。
- **消融（RoboTwin 子集）：** 数值动作 69.8，原始 \((u,v)\) 72.3，去掉 flow 重加权 83.9，去掉 stochastic AE 条件 82.1，完整 89.8。世界模型侧：text 49.31，数值动作 54.18，原始 flow 56.72，mask 图像动作 57.84，完整 65.23。
- **可解码性：** 50 个 RoboTwin 任务上，预测 flow 相对 RAFT 伪 GT 的误差与成功率 Pearson **\(r=-0.81\)**。这支持“flow 质量与控制成功相关”，不是因果识别。

### 总结讨论

FlowWAM 把 WAM 的动作表征问题收束成一句可检验的话：动作应是视频原生、跨帧稠密、且能解码成关节指令的运动场。RoboTwin、WorldArena 轨迹轴和真机双臂任务支持这一主张；相关工作里最接近的是 Motus，但表征层级不同。适用边界是操作式短中程 WAM，不是 HOI 接触力学，也不是 Pearl 式因果。失败与开放问题包括：腕部 flow 缺失、robot-only 伪标签丢掉物体被推动后的 scene flow、HSV 幅度截断、5B 级视频骨干的算力，以及未来工作自己列出的互联网级无动作预训练和更长时域。阅读判断：若课题关心 WAM 里“动作该长成什么样”，这篇比再堆一个 RGB imagination 头更直接；不要把光流一致性写成世界的因果结构，也不要和 G0.5 的 RoboTwin 数字做未经对齐的榜首比较。

### 代码与数据

- **代码：** [YixiangChen515/FlowWAM](https://github.com/YixiangChen515/FlowWAM) 含 `training/`、`inference/`、`data_generation/`、`diffsynth/`。LICENSE 为 Apache-2.0（文件末尾仍留有 diffsynth 来源的 Zhongjie Duan 版权样板，以仓库实际 NOTICE 为准）。
- **模型 / 数据：** README 指向 Hugging Face `YixiangChen/FlowWAM` 与 `YixiangChen/FlowWAM_RoboTwin`；本次未逐文件核验权重是否已全部上传。
- **依赖数据：** EgoDex（无机器人动作标签）、RoboTwin 2.0、RAFT 伪标签；完整复现仍依赖这些外部语料和 32×H100 级训练设置。

### 局限、失败案例与开放问题

- 腕部视角没有 robot-only flow 监督，拼图里用常量占位。
- RoboTwin flow 目标去掉了物体/背景运动，接触后的 object response 不在动作表征里。
- WorldArena 消融 split 与官方远程评测不一致，不能把 65.23 与主表 63.71 混比。
- Hanging Mug 等任务成功率仍低；真机每任务仅 10 trial。
- 光流是像素位移，不是可干预因果变量；RAFT 误差会进入训练目标。
- 未来工作承认尚未做 internet-scale 无动作预训练和更长时域 flow planning。
