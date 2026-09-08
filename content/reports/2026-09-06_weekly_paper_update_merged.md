# 知域论文合并更新：2026-09-06

**报告标签**：周报, World Action Model, world model, Embodied In-context Learning, cross-embodiment, HOI, egocentric vision, 3D/4D Reconstruction, Streaming Generation, Causal Modeling, Physical Reasoning

- **检索日期**：2026-09-06
- **合并检索窗口**：2026-08-26 至 2026-09-06
- **检索方向**：Hand-Object Interaction、3D/4D HOI、具身 In-context Learning、Egocentric World Model、World Action Model、跨具身泛化、前馈重建与生成、因果世界模型、流式生成、物理一致性评测及相关机器人学习。
- **来源文档数量**：2
- **来源文档正式条目数量**：27
- **跨文档重复数量**：5
- **馆藏既有正式条目数量**：1
- **用户补充指定论文数量**：1
- **最终唯一新增论文数量**：22

## 馆藏检查

- **知域论文数据**：读取成功
- **知域报告索引**：读取成功
- **检查时馆藏论文数量**：135
- **检查时专题报告数量**：21
- **合并入库检查时间**：2026-09-08，Asia/Shanghai
- **去重状态**：已与最新 `origin/main`、本地论文数据和两份来源文档交叉比较
- **补充说明**：入库前论文库为 135 篇、报告库为 21 份。两份来源文档共有 27 个正式条目，其中 Zeva、Motus2、IMPACT、Streaming4D、Facet-0 重复出现；MILO（arXiv:2608.27407）已由 2026-08-30 周报收录，不重复生成新卡片。用户指定补充 AnyWorld（arXiv:2608.29242），最终得到 22 篇唯一新论文。Motus2 与已收录的 Motus 是后续工作，不是同一论文。

## 检索方法

两份来源检索覆盖 arXiv 的 `cs.CV`、`cs.RO`、`cs.AI`、`cs.LG`、`cs.GR` 和 `cs.MM` 分类，合并窗口为 2026-08-26 至 2026-09-06；同时核验 arXiv 摘要页、论文 HTML/正文、论文 comments、官方项目页、GitHub 和 Hugging Face 链接。AnyWorld 由用户补充指定，并额外核验 arXiv v2、官方项目页和官方代码仓库。

检索关键词包括：

- `world model`、`world action model`、`WAM`
- `egocentric`、`hand-object`、`dexterous manipulation`
- `in-context learning`、`causal interaction`
- `3D reconstruction`、`4D world model`、`streaming generation`
- `video prediction`、`interactive video`、`physical reasoning`
- `JEPA`、`counterfactual`、`action-conditioned video`
- `Gaussian Splatting`、`feed-forward reconstruction`

纳入标准：

1. 在本期时间窗口内首次发布，或在窗口内发生可核验的重要版本变化；
2. 与知域关注方向直接相关；
3. 至少存在 arXiv、OpenReview、正式会议或期刊页面之一；
4. 能从原始论文摘要、论文 comments 或官方项目页核验基本事实。

排除标准：

- 仅与通用机器人、自动驾驶或视频生成弱相关；
- 只有二手线索且无法找到原论文；
- 与知域已有论文完全重复且无实质版本变化；
- 论文主题与 HOI、世界模型、具身学习、3D/4D 表征关系过弱。

合并报告优先保留两份来源中证据更完整的条目：9 月 2 日文档已全文核验的重复论文不会被 9 月 6 日摘要级条目降级覆盖。多数其余论文仍主要依据 arXiv 元数据、摘要和官方项目资料；涉及具体数值时，仅记录原论文或官方页面明确给出的结果。AnyWorld 已核验 arXiv v2 正文、项目页与官方代码仓库。

## 本周概览

本期最明显的技术趋势是 **World Action Model 从"预测未来视频"向"可决策、可验证、可执行的闭环系统"演化**。

第一条主线是跨具身和数据规模扩展。ZimaBlue、Motus2、SolarWM、RoboTok 与 AnyWorld 分别从大规模第一视角视频、机器人轨迹、失败交互、互联网人类示范、统一数据管线和可因子化经验重组等角度，试图降低动作标注和机器人数据采集成本。AnyWorld 进一步把动作、相机和目标 embodiment/context 分开控制，将同一人类交互重组为机器人域视频—动作经验；但其跨具身证据仍限于 EgoDex、RoboCasa GR1 与 IRON 三类 embodiment。

第二条主线是 WAM 的几何与空间建模。SA-WAM 将 RGB、深度和动作置于同一扩散骨干中；Temporal Forcing 用 4D foundation model 对齐 VLA 历史表征；RESELF 联合重建场景与穿戴者自身运动；Puffin-World 将物理、几何和外观作为统一世界状态；Streaming4D 则把视频生成与增量 3D 重建同步化。GeoNeXt 展示视频扩散先验也可反向迁移到深度与法线估计。这些工作说明，单纯 RGB 预测正在被几何、深度、相机状态和身体状态等结构化信号补充。

第三条主线是推理阶段的可靠性。World-Coherent Decoding 用多候选未来和执行后反馈进行测试时选择；VeriPhy 将物理约束编译成可审计的证据链；Principia 通过关系物理而非单一视觉质量分数评测视频模型；Can Video World Models Track Unobserved World States? 则直接检验模型是否维护了不可见的隐状态。这些工作共同削弱了"视频看起来合理就代表世界模型可靠"的假设。

第四条主线是交互视频的长期一致性。Matrix-Game 3.5 使用 3D patch memory 和静态—动态解耦维持长时交互世界；SolarWM 通过统一数据合同和多骨干适配支持长时视频世界模型；World-State Reasoning 和隐状态追踪工作则把"记住历史画面"与"维护可用于下一步决策的世界状态"区分开来。

## 分类与研究脉络

### 1. World Action Model 与具身控制

| 工作 | 输入 | 核心表示 | 输出 | 主要贡献 |
|---|---|---|---|---|
| ZimaBlue | 人类/机器人第一视角视频、机器人轨迹 | 视频动态、统一动作表示 | 机器人动作与未来视频 | 三阶段视频预训练、视频—动作中训练、目标机器人适配 |
| Motus2 | 单目/双目人类视频、机器人轨迹、失败交互 | 共享策略—模拟器—评估器 | 动作块、未来视觉后果、价值评估 | 将 WAM、世界模型和价值模型置于闭环 |
| SA-WAM | RGB、深度、动作 | 几何潜变量与视频扩散表示 | 动作、RGB 和深度未来 | 将 3D 信息引入 WAM |
| World-Coherent Decoding | 当前观测、WAM 采样未来 | 视觉 surprisal、动作路径稳定性 | 经过筛选的动作候选 | 测试时选择可靠未来，而非简单增加采样数 |
| Zeva | 机器人交互轨迹 | 因果交互信号、双时间尺度记忆 | 冻结策略的上下文输入 | 不更新策略参数的具身 In-context Learning |
| AnyWorld | 人类第一视角交互、动作骨架、相机轨迹、目标首帧 | 动作—相机—embodiment/context 因子化条件 | 机器人域视频—动作经验 | 无配对人机演示的跨具身经验重组与定向策略补强 |

该方向的共同瓶颈是动作可执行性。视频中观察到的动作、光流或接触变化，并不自动等价于目标机器人的关节动作。未来实验需要严格区分视觉预测质量、动作预测质量和真实执行成功率。

### 2. Egocentric World Model、HOI 与操作数据

RoboTok 从互联网人类视频中检索操作示范，使用以手轨迹为中心的 3D 表示提升跨视角和遮挡条件下的检索。AnyWorld 把第一视角人类交互拆成图像平面动作骨架、Plücker 相机轨迹与目标 embodiment/context，再重组为机器人域经验。RESELF 联合恢复环境场景与拍摄者自身运动，补足了传统场景重建忽略身体、人体运动估计缺少场景几何的问题。Motus2 和 ZimaBlue 则把第一视角人类视频视为具身经验来源。

这些工作与知域已有的 HandsOnWorld、DreamHand、EgoForge、EgoSim、HO-Flow 等形成连续脉络：研究重点从单纯生成手部或手—物交互，逐步转向把第一视角视频转换为可泛化的动作、几何和世界状态监督。

### 3. 3D/4D 重建与流式生成

Streaming4D 直接耦合分块视频生成和增量 3D 重建，减少视频生成完成后再统一重建的延迟。Temporal Forcing 用 4D 教师监督轻量历史路径，RoboPhys-3D 用同构重建流程分离生成误差与重建器误差，GeoNeXt 则把视频扩散时序先验用于单图深度—法线联合估计。Puffin-World 在统一模型中同时处理物理、深度、图像和相机表示。RESELF 则利用确定性的场景几何约束生成被遮挡的身体运动。

这类工作适合影响知域后续关于 VGGT、DynamicVGGT、4DGS-WAM 和流式生成的研究路线，但需要进一步核验：

- 增量重建是否会累积几何漂移；
- 生成视频的视觉一致性是否真正对应 3D 一致性；
- 实时性是否只在单卡、短序列或低分辨率条件下成立；
- 评测是否使用了生成过程中的真实未来信息。

### 4. 交互世界模型与长期记忆

Matrix-Game 3.5 引入 patch memory、投影相机位置编码和静态—动态解耦，目标是维持长时场景几何、动态主体和相机控制的一致性。SolarWM 将多数据源转换为包含视觉、相机几何、字幕、质量和 provenance 的统一数据合同。Statebench 则关注视频续接是否真正反映历史动作导致的世界状态，而不是简单复制历史帧。

这里最值得关注的研究问题是：**记忆模块存储的是画面证据，还是可被后续动作条件化更新的世界状态？**

### 5. 因果、物理与可靠性评测

Zeva 使用"动作—状态变化"构造因果交互信号，但摘要尚不足以证明其实现了严格的因果识别。它更接近 action-conditioned interaction memory，而不是结构因果模型。

Can Video World Models Track Unobserved World States? 使用 Shell Game 式隐状态任务检验模型能否追踪不可见状态；Principia 用关系物理约束评估视频模型；VeriPhy 将物理义务、测量和证据来源结构化。它们共同提示：像素似然、VBench 或视觉流畅度不能替代隐状态、干预一致性和物理可验证性。

## 证据审计

- **实验直接支持的结论**：
  - WCD 摘要明确报告 RoboTwin 2.0 Hard success 从 55.80% 提升到 60.90%。
  - Streaming4D 摘要报告单张 RTX 4090 上约 \(1.24\times\) 的运行速度提升。
  - DemoMimic 摘要报告在 16 个物体、4 个任务和 2 种机械手上的 71% 真实世界成功率。
  - LEAP 摘要报告在匹配协议下相较 LeWM+CEM 将平均成功率从 77.5% 提升到 94.8%。
  - Principia 摘要报告多个视频生成模型在关系物理测试上最高分不超过 0.42，而 VBench 约为 0.8。
  - AnyWorld 正文报告 ActionAlign、CameraAlign、EmbodAcc 的平均可控性为 0.778，高于 WAN Fun-Control 的 0.609；加入重组经验后，RoboCasa GR1 18 项任务成功率从 49.8% 提至 54.6%，IRON 20 次抓取从 20.0% 提至 55.0%。
  - RESELF、SolarWM、Puffin-World、Matrix-Game 3.5 和 OctWorld 均有项目页或代码/模型链接，但完整复现边界仍需阅读全文确认。

- **仅能视为作者主张的内容**：
  - "可泛化""可扩展""实时控制""物理一致""零样本泛化"等表述，目前主要来自标题和摘要。
  - ZimaBlue、Motus2、SolarWM 的大规模数据扩展效果需要检查数据混合比例、跨本体划分和是否存在目标任务泄漏。
  - AnyWorld 的“保留底层交互动力学”主要由代理可控性指标、视频质量和下游策略收益支持；它不能替代真实接触力、触觉或完整 3D 物理状态验证。
  - Zeva 使用"causal"命名，但目前摘要只证明其编码动作导致的状态变化；尚不能据此认定实现了 causal identification、结构因果模型或可靠反事实推理。
  - SA-WAM 的 "state-of-the-art" 表述需要核验 benchmark 版本、比较模型、训练数据和是否使用额外深度监督。

- **需要重点检查的公平性问题**：
  - WAM 之间可能使用不同的视频骨干、动作空间、数据规模和推理预算。
  - 机器人成功率比较需要确认是否使用相同本体、随机化范围、任务初始化和失败重试规则。
  - 生成视频物理评测需要区分真实视频、生成视频和后处理视频的分布差异。
  - 互联网视频数据工作需要检查测试集是否被预训练数据覆盖。
  - AnyWorld 的真实机器人结果只有 20 次 IRON 抓取，且比较的是同一 UniT 系策略适配前后；不能据此推出对任意机器人形态或长时任务的普遍泛化。

- **因果结论边界**：
  - action-conditioned prediction 不等于 intervention。
  - temporal causal attention 不等于 causal identification。
  - 物理或几何 inductive bias 不等于结构因果模型。
  - 反事实视频生成若没有明确干预变量、可识别假设和反事实一致性评测，不应扩大解释为反事实推理。
  - AnyWorld 的“counterfactual”实验是固定视觉状态下构造左右指令—动作配对，并比较 action-only 与视觉—动作联合重组；它支持定向数据干预机制，不构成 SCM、因果识别或一般反事实推断证明。

## 对研究选题的影响

1. **如果研究 WAM 的泛化**，不能只增加模型规模。ZimaBlue、Motus2、SolarWM、RoboTok 和 AnyWorld 表明，数据来源、跨具身对齐、动作表示、视角因子化和失败数据的价值可能与参数规模同等重要。AnyWorld 尤其提供了可证伪的接口：固定动作、相机或目标 context 中两项，只改变第三项，分别测量控制忠实度和下游策略收益。
2. **如果研究具身 In-context Learning**，Zeva 提供了"动作导致的状态变化 + 双时间尺度记忆"的路线，但需要设计更严格的干预式评测，证明记忆不仅是在做相似轨迹检索。
3. **如果研究 3D/4D 世界模型**，SA-WAM、RESELF、Puffin-World 和 Streaming4D 都支持引入深度、相机、身体状态或增量几何，而不是仅预测 RGB。
4. **如果研究实时交互视频**，Matrix-Game 3.5 和 Streaming4D 将记忆、分块生成、低延迟重建作为系统级问题，适合与知域已有的 Causal Forcing++、minWM 和流式生成工作对比。
5. **如果研究世界模型的因果性**，隐状态追踪、关系物理和可审计验证比单纯提升视频质量更能形成清晰的 novelty。
6. **如果研究实验设计**，建议同时报告：视觉质量、几何一致性、动作可执行性、长时状态保持、干预/反事实测试、计算成本和失败案例。

## 已收录且无重要变化

以下工作在本期候选或相关检索中出现，但知域已经收录，本周期未发现新的 arXiv 版本、正式出版状态、官方代码/数据/模型首次公开或项目页重大变化：

- **4DGS-WAM: Bridging Past and Future with an Object-Centric World Action Model based on 4D Gaussian Splatting**，知域 ID：`arxiv-2608-25956`；排除原因：知域已收录，本周期无实质更新。
- **Causal-JEPA: Learning World Models through Object-Level Latent Masking**，知域 ID：`arxiv-2602-11389`；排除原因：知域已收录，本周期无实质更新。
- **FlowWAM: Optical Flow as a Unified Action Representation for World Action Models**，知域 ID：`arxiv-2607-13017`；排除原因：知域已收录，本周期无实质更新。
- **HandsOnWorld: Unconstrained Egocentric Video Generation with Camera-Disentangled Hand Control**，知域 ID：`arxiv-2607-02075`；排除原因：知域已收录，本周期无实质更新。
- **DreamHand: Repurposing Video Diffusion Models for Occlusion-Robust Egocentric 3D Hand Motion Recovery**，知域 ID：`arxiv-2608-20308`；排除原因：知域已收录，本周期无实质更新。
- **FACT: Failure-Aware Causal Training for World-Action Models**，知域 ID：`arxiv-2608-10232`；排除原因：知域已收录，本周期无实质更新。
- **GeniWorld: A Generalizable Interactive World Model for Robotic Manipulation via Visual Actions**，知域 ID：`arxiv-2608-06332`；排除原因：知域已收录，本周期无实质更新。
- **WorldEcho & WorldSync: Do Robotic World Models Really Follow Actions?**，知域 ID：`arxiv-2608-24885`；排除原因：知域已收录，本周期无实质更新。
- **WorldSimProbe: Diagnosing Simulator Faithfulness in Action-Conditioned World Models for Embodied Manipulation**，知域 ID：`arxiv-2608-09298`；排除原因：知域已收录，本周期无实质更新。
- **Zero-WAM: In-Context World-Action Modeling from Human Videos for Open-Ended Task Generalization**，知域 ID：`arxiv-2608-26103`；排除原因：知域已收录，本周期无实质更新。
- **LAWA: Latent Action as Intention Enables Efficient Future Imagination for World Action Models**，知域 ID：`arxiv-2608-24882`；排除原因：知域已收录，本周期无实质更新。
- **LD4WAM: Learning Latent Dynamics from Human Videos for World Action Models**，知域 ID：`arxiv-2608-22403`；排除原因：知域已收录，本周期无实质更新。
- **WAM-OPD: On-Policy Distillation for World Action Models**，知域 ID：`arxiv-2608-22364`；排除原因：知域已收录，本周期无实质更新。
- **R2M-Bench: Evaluating Revisit Memory via Relative Consistency in Interactive Video World Models**，知域 ID：`arxiv-2608-27328`；排除原因：知域已收录，本周期无实质更新。
- **ReWorld: An Interactive World Model with Long-Horizon Memory**，知域 ID：`arxiv-2608-23565`；排除原因：知域已收录，本周期无实质更新。
- **EchoWM: Open and Enterable Omnimodal World Models**，知域 ID：`arxiv-2608-23189`；排除原因：知域已收录，本周期无实质更新。
- **MILO: Reconstructing Humans and Objects in Interaction using Large Reconstruction Models**，知域 ID：`arxiv-2608-27407`；排除原因：已由 2026-08-30 周报收录，本次合并不重复生成新卡片。
- **4DGS-WAM、GeoWAM、GaussianWAM、GWM-VLA** 等几何增强 WAM 工作；排除原因：均已在知域馆藏中，未发现本周期新的版本变化。
- **Causal Forcing++、minWM、Causal-JEPA** 等流式生成和因果世界模型工作；排除原因：已在近期专题报告和论文馆藏中覆盖。

## 待人工核验线索

- **HarmoHOI 相关新版本或项目页更新**：本期未找到可明确归属于 HarmoHOI 的新 arXiv 记录，需要人工确认是否存在仅在项目页、社交媒体或会议页面发布的更新。
- **DWM、HandsOnWorld、X-WAM、Flow WAM 的官方代码状态**：部分工作在知域已有馆藏，但本期检索未能确认是否在 2026-08-30 至 2026-09-06 首次开放新代码或模型。
- **Puffin-World 的 Hugging Face 模型页面**：项目页已确认代码、模型和数据链接，但本次网络环境无法直接访问 Hugging Face 页面，模型文件和许可证状态待人工核验。
- **OctWorld 的代码仓库**：论文 comments 和项目页确认项目页面，项目页可访问；未能在本次检索中确认公开 GitHub 仓库地址。
- **若干仅有摘要级线索的机器人操作论文**，包括 AdaRoboVLG、XR-2、Blind Dexterity 和 One Demonstration, Many Objects：与 HOI/具身操作高度相关，但本期未对全文实验、代码、数据和失败案例完成核验。

## 1. ZimaBlue: Evolving Generalizable World Action Models through Scalable Video Pre-training

- **作者**：Xionghao Wu, Yijun Yang, Shiyang Zhou, Haoze Sun, Jianhui Liu, Songsong Yu, Jiyao Zhang, Wenbo Li, Bo Wang, Guoqing Ma, Lin Song, Renjie Liao, Shenghe Zheng, Wei Tang, Xiaojuan Qi, Yanwei Li, Yuan Zhang, Zhuotao Tian, Haoyang Huang, Nan Duan
- **年份与发表**：2026，arXiv
- **arXiv ID**：2609.00188
- **DOI**：暂无
- **论文**：[arXiv](https://arxiv.org/abs/2609.00188)
- **正式出版**：暂无
- **项目**：未在 arXiv comments 中提供
- **代码**：未在 arXiv comments 中提供
- **数据**：未在 arXiv comments 中提供
- **模型**：未在 arXiv comments 中提供
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.00188)
- **代表图**：ZimaBlue 跨具身世界动作模型概览；来源：[论文原图](https://arxiv.org/html/2609.00188v1/teaser.svg)
- **类别标签**：World Action Model, Egocentric Video, cross-embodiment, Robot Learning, Video Pretraining
- **证据等级**：仅摘要与 arXiv 元数据核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![ZimaBlue 跨具身世界动作模型概览](https://arxiv.org/html/2609.00188v1/teaser.svg)

### 核心内容与 Insight

ZimaBlue 试图利用大规模人类和机器人第一视角视频学习可泛化的 World Action Model。摘要描述了三阶段训练流程：

1. 因果具身视频预训练；
2. 视频—动作中训练，将视觉动态与异构机器人轨迹对齐；
3. 针对目标机器人进行部署适配。

论文还提出 Slow–Fast 双系统：Slow 分支提供高容量世界模型表示，Fast 分支负责实时动作预测。摘要声称 Fast 分支可在 RTX 4090 上达到 30 Hz，但具体动作空间、预测延迟和成功率需要全文核验。

### Pipeline

**输入**：人类第一视角视频、机器人第一视角视频、异构机器人轨迹、目标机器人数据。

**过程**：先学习大规模视觉动态，再通过统一动作表示将视觉动态对齐到机器人轨迹，最后针对目标机器人进行适配；推理阶段由高容量 Slow 模型和轻量 Fast 动作分支协同工作。

**输出**：面向目标机器人的动作预测和未来视觉动态表示。

### 实验与证据

摘要明确声称进行了真实机器人零样本评估，并比较了仅使用目标机器人数据与加入大规模视频预训练的方案。但当前尚未核验：

- 使用了哪些机器人、本体和任务；
- 零样本的具体定义；
- 是否存在目标任务或场景泄漏；
- 与哪些 WAM/VLA baseline 比较；
- 30 Hz 是否包含视觉编码、采样和动作后处理时间。

因此，目前只能确认其研究方向和系统设计，不能据摘要扩大为全面的跨本体泛化结论。

### 代码与数据

arXiv 页面未提供明确代码、数据或模型链接，开放状态待人工核验。

### 局限、失败案例与开放问题

- 人类视频中的视觉变化如何被转化为可执行动作仍是核心难点。
- 统一动作表示可能牺牲不同机器人本体的精细控制能力。
- Slow–Fast 架构的实时性可能依赖硬件、分辨率和缓存策略。
- 需要检查长时任务、遮挡、接触失败和分布外物体上的表现。

### 与知域的关系

该工作直接连接知域中的 Zero-WAM、FlowWAM、Motus、DreamWAM、LD4WAM 和跨具身世界模型路线，尤其适合用于研究"人类视频预训练如何转化为机器人动作监督"。

## 2. Spatially Aware World Action Model via Geometric Latent Diffusion

- **作者**：Javier Alejandro Lopetegui Gonzalez, Paul Pacaud, Cordelia Schmid
- **年份与发表**：2026，arXiv
- **arXiv ID**：2609.02531
- **DOI**：暂无
- **论文**：[arXiv](https://arxiv.org/abs/2609.02531)
- **正式出版**：暂无
- **项目**：未提供
- **代码**：未提供
- **数据**：使用 RoboCasa、LIBERO-Plus，具体数据链接待核验
- **模型**：未提供
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.02531)
- **代表图**：SA-WAM 几何潜变量与空间感知对比；来源：[论文原图](https://arxiv.org/html/2609.02531v1/ep_vs_sr_teaser_a200.svg)
- **类别标签**：World Action Model, Geometric Latent Diffusion, Depth Prediction, Robot Manipulation
- **证据等级**：仅摘要与 arXiv 元数据核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![SA-WAM 几何潜变量与空间感知对比](https://arxiv.org/html/2609.02531v1/ep_vs_sr_teaser_a200.svg)

### 核心内容与 Insight

SA-WAM 将动作、RGB 和深度预测放入同一个视频扩散骨干。论文的关键工程设计是把无界深度信号映射到冻结 VAE tokenizer 可以接受的有界输入域，从而不必重新训练 3D 专用 tokenizer。

作者声称在 RoboCasa、LIBERO-Plus 和真实 UR5 实验中取得较强结果，并观察到未来状态预测质量与 rollout 成功率之间存在关联。

### Pipeline

**输入**：RGB 观测、深度信息、机器人动作条件。

**过程**：使用预训练视频模型作为扩散骨干，将深度经过非线性编码后送入冻结 VAE tokenizer；模型联合预测 RGB、深度和动作相关未来状态。

**输出**：未来 RGB、未来深度和机器人动作。

### 实验与证据

摘要提到 RoboCasa、LIBERO-Plus 和 UR5 真实机器人实验，并声称相较强 baseline 有提升。尚未核验：

- 深度是训练输入、辅助监督还是推理时可用输入；
- benchmark 的具体版本和训练划分；
- "state-of-the-art" 的比较范围；
- 未来深度预测与真实控制成功率之间的统计关系；
- 真实 UR5 中是否使用额外标定或环境先验。

### 代码与数据

未在摘要 comments 中发现代码、数据或模型链接。

### 局限、失败案例与开放问题

- 深度编码可能丢失绝对尺度或精细几何。
- RGB、深度和动作联合生成的训练目标可能存在监督不平衡。
- 3D 信息是否真正带来跨视角、遮挡和新物体泛化，需要消融验证。

### 与知域的关系

该工作直接补充知域已有 DreamWAM、GaussianWAM、GeoWAM、GWM-VLA 和 4DGS-WAM，将几何信息从额外模块提升为 WAM 内部预测目标。

## 3. World-Coherent Decoding: Self-Verifying Test-Time Planning for World Action Models

- **作者**：Chuhan Zhang, Seiji Ito, Kenta Hoshino, Satoshi Ikehata, Ikuro Sato
- **年份与发表**：2026，arXiv
- **arXiv ID**：2609.02159
- **DOI**：暂无
- **论文**：[arXiv](https://arxiv.org/abs/2609.02159)
- **正式出版**：暂无
- **项目**：未提供
- **代码**：未提供
- **数据**：RoboTwin 2.0，具体链接待核验
- **模型**：基于冻结 WAM
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.02159)
- **代表图**：World-Coherent Decoding 测试时规划示例；来源：[论文原图](https://arxiv.org/html/2609.02159v1/hook_pilot.png)
- **类别标签**：World Action Model, Test-Time Planning, Self-Verification, Robot Control
- **证据等级**：仅摘要与 arXiv 元数据核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![World-Coherent Decoding 测试时规划示例](https://arxiv.org/html/2609.02159v1/hook_pilot.png)

### 核心内容与 Insight

WCD 将 WAM 生成的未来视为可证伪的"未来—动作假设"，不直接采用单个采样结果，而是：

- 采样多个候选未来；
- 使用视觉 surprisal 评价未来的生成可信度；
- 使用动作路径代价评价动作稳定性；
- 执行后比较想象与真实观测；
- 在线训练轻量预测器，改进下一次候选选择。

核心观点是：WAM 的测试时扩展不一定是采样更多未来，而是选择更可靠的未来。

### Pipeline

**输入**：当前观测、冻结 WAM、候选动作和未来视频样本。

**过程**：多候选采样、视觉 plausibility 评分、动作路径评分、执行后误差审计、在线候选选择器更新。

**输出**：被选择并执行的动作序列。

### 实验与证据

摘要报告 RoboTwin 2.0 Hard success 从 55.80% 提升到 60.90%，Horizon-3 任务提升 16.43 个百分点，并在真实 Franka 视觉变化测试中展示定性鲁棒性。

尚未核验：

- 是否使用了额外的真实执行数据；
- 在线 predictor 的训练预算；
- 与单纯增加采样数、CEM、reranking baseline 的公平比较；
- 真实机器人结果是否有统计重复。

### 代码与数据

未在 arXiv comments 中发现明确代码或模型链接。

### 局限、失败案例与开放问题

- 视觉 surprisal 可能偏好"像训练分布"的未来，而不一定是正确未来。
- 动作路径代价不等价于任务成功概率。
- 执行后审计存在延迟，失败动作可能已经造成不可逆后果。
- 在线选择器是否能跨任务和跨本体迁移尚不清楚。

### 与知域的关系

该工作对知域的 WAM 研究提供了重要的测试时推理路线，可与 GlanceWAM、WAM-OPD、FACT 和 WorldSimProbe 形成互补。

## 4. Motus2: A Self-Evolving General World Model for Dexterous Manipulation

- **作者**：Hongzhe Bi, Zihao Zhou, Yihang Tang, Jingrui Pang, Shuhe Huang, Haitian Liu, Runqing Wang, Shuai Huang, Yichen Wang, Yiming Cheng, Ruowen Zhao, Zhenghua Li, Hengkai Tan, Xiaolong Liu, Jinhui Wan, Jiabao Liu, Min Zhao, Fan Bao, Jun Zhu
- **年份与发表**：2026，arXiv
- **arXiv ID**：2608.30237
- **DOI**：[10.48550/arXiv.2608.30237](https://doi.org/10.48550/arXiv.2608.30237)
- **论文**：[arXiv](https://arxiv.org/abs/2608.30237)
- **正式出版**：暂无
- **项目**：[Motus2 官方项目页](https://motus-robotics.github.io/motus2/)
- **代码**：未提供
- **数据**：未提供
- **模型**：未提供
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2608.30237)
- **代表图**：策略—模拟器—价值模型统一框架；来源：[论文原图](https://arxiv.org/html/2608.30237v1/motus2_overview.png)
- **类别标签**：Dexterous Manipulation, world model, World Action Model, Value Model, Egocentric Video
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：与 Motus 为同团队后续工作，但不是重复记录
- **现有知域 ID**：`arxiv-2512-13030` 为前作 Motus

![Motus2 策略—模拟器—价值模型统一框架](https://arxiv.org/html/2608.30237v1/motus2_overview.png)

### 核心内容与 Insight

Motus2 将单一共享权重模型暴露为三个控制接口：

1. policy：提出动作候选；
2. simulator：预测动作后果；
3. evaluator：评价预测结果。

三者形成闭环，用于策略改进。论文还强调失败和次优交互对动力学建模与价值学习的作用，并从单目第一视角视频扩展到同步双目视频和机器人轨迹。

### Pipeline

**输入**：人类第一视角视频、双目第一视角视频、机器人轨迹、专家示范、失败交互。

**过程**：统一模型分别承担动作提议、视觉后果预测和价值评估；通过候选动作—模拟—评估闭环进行决策和学习。

**输出**：动作块、视觉未来、价值评估和策略更新信号。

### 实验与证据

摘要强调模型规模、数据规模和失败数据利用，但没有在摘要中给出足够的定量结果。需要阅读全文核验：

- 三个接口是否完全共享权重；
- 失败交互如何标注和使用；
- 与 Motus、WAM、VLA 的比较；
- 双目视频对性能的独立贡献；
- 自我改进是否来自模型更新、上下文记忆或搜索策略。

### 代码与数据

arXiv comments 未提供明确开放链接。

### 局限、失败案例与开放问题

- policy、simulator 和 evaluator 共享权重可能造成目标冲突。
- 预测视觉后果不代表价值评估可靠。
- 失败数据的分布可能与真实部署失败分布不同。
- "self-evolving"需要区分持续训练、在线适应和测试时搜索。

### 与知域的关系

Motus2 是知域已收录 Motus 的直接后续，值得作为"统一 WAM—世界模型—价值模型"路线的重点更新对象。

## 5. RoboTok: An Internet-Scale Data Engine for Human Demonstration Retrieval and Dexterous Manipulation Learning

- **作者**：Howard Qian, Yiting Chen, Yunfei Xie, Kejia Ren, Podshara Chanrungmaneekul, Gaotian Wang, Bowen Wen, Chen Wei, Kaiyu Hang
- **年份与发表**：2026，arXiv
- **arXiv ID**：2609.03199
- **DOI**：暂无
- **论文**：[arXiv](https://arxiv.org/abs/2609.03199)
- **正式出版**：暂无
- **项目**：未提供
- **代码**：未提供
- **数据**：互联网操作视频，具体数据开放状态待核验
- **模型**：未提供
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.03199)
- **代表图**：RoboTok 人类示范活动、关键点与轨迹表示；来源：[论文原图](https://arxiv.org/html/2609.03199v1/fig_qualitative_activities_keypoints_traj.png)
- **类别标签**：Human Demonstration Retrieval, Dexterous Manipulation, 3D Hand Trajectory, Robot Learning
- **证据等级**：仅摘要与 arXiv 元数据核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![RoboTok 人类示范活动、关键点与轨迹表示](https://arxiv.org/html/2609.03199v1/fig_qualitative_activities_keypoints_traj.png)

### 核心内容与 Insight

RoboTok 将互联网人类操作视频视为可持续增长的机器人学习数据源。其核心表示是以演员为中心坐标系表达的 3D 手部轨迹，用于跨视角、场景外观和遮挡条件下的操作示范检索。

### Pipeline

**输入**：查询人类操作视频、互联网人类操作视频集合、估计的 3D 手部轨迹。

**过程**：将手轨迹转换到 actor-centered reference frame，学习潜在运动空间，建立大规模检索索引，再将相关示范用于机器人策略学习。

**输出**：相关人类示范及下游机器人策略监督。

### 实验与证据

摘要声称在检索 benchmark 和下游机器人策略成功率上优于已有机器人数据检索方法。尚未核验：

- 3D 手部轨迹的估计误差；
- 视频检索数据规模；
- 互联网视频与测试任务之间的数据泄漏；
- 机器人策略是否真正使用了检索视频，还是只使用了筛选后的标签；
- 遮挡和非人手操作场景的失败率。

### 代码与数据

当前未确认代码、索引或数据是否开放。

### 局限、失败案例与开放问题

- 人类手部轨迹不一定包含接触力、摩擦和机器人执行约束。
- 互联网视频的镜头剪辑可能破坏时间因果关系。
- 检索相关性与可执行性之间仍存在明显鸿沟。

### 与知域的关系

该工作直接连接 HOI、Egocentric World Model 和跨具身学习，可能影响知域的数据设计路线：从"收集更多机器人轨迹"转向"检索并筛选高价值人类交互视频"。

## 6. Zeva: In-Context Causal Learning for Generalizable Embodied Manipulation

- **作者**：Fu Chen, Xin Ding, Bingjia Huang, Xiangyu Li, Mingju Wang, Jiawei He, Kun Li, Wei Sun, Yunxin Liu, Hao Wu, Ting Cao
- **年份与发表**：2026，arXiv
- **arXiv ID**：2608.30880
- **DOI**：[10.48550/arXiv.2608.30880](https://doi.org/10.48550/arXiv.2608.30880)
- **论文**：[arXiv](https://arxiv.org/abs/2608.30880)
- **正式出版**：暂无
- **项目**：[Zeva 官方项目页](https://air-embodied-brain.github.io/Zeva/)
- **代码**：[GitHub](https://github.com/air-embodied-brain/Zeva)
- **数据**：依赖 RoboCasa365；未发现新增独立数据集
- **模型**：[Hugging Face](https://huggingface.co/chen123fu/zeva-robocasa)
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2608.30880)
- **代表图**：Zeva 总体框架与交互记忆流程；来源：[论文原图](https://arxiv.org/html/2608.30880v1/zeva_v2.png)
- **类别标签**：Embodied In-context Learning, Causal Interaction, Robot Memory, Test-Time Adaptation
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![Zeva 总体框架与交互记忆流程](https://arxiv.org/html/2608.30880v1/zeva_v2.png)

### 核心内容与 Insight

Zeva 让机器人从自身交互中在线学习，同时保持策略模型冻结。它使用 Causal Interaction Extractor 将执行动作及其诱导的状态变化编码成因果交互信号，并存储在双时间尺度记忆中。后续动作通过检索相关交互信号，将经验作为上下文注入冻结策略。

### Pipeline

**输入**：机器人观测、执行动作、动作后的状态变化、历史交互记忆。

**过程**：提取动作—状态变化关系，写入短期和长期记忆；根据当前任务检索相关经验，并作为上下文提供给冻结策略。

**输出**：经过交互经验调节的机器人动作。

### 实验与证据

摘要声称在仿真和真实机器人操作中优于若干 VLA 和 WAM baseline，并且成功率随交互经验增加而提升。尚未核验：

- 记忆检索是否优于普通轨迹检索；
- "causal"信号是否经过干预实验验证；
- 在线经验是否跨任务泛化；
- 真实机器人实验的任务数量、重复次数和失败案例。

### 代码与数据

未在 arXiv comments 中发现公开链接。

### 局限、失败案例与开放问题

该方法的"causal"命名需要谨慎解释。目前摘要支持的是动作导致状态变化的记忆建模，不足以证明结构因果模型、因果识别或反事实推理。

### 与知域的关系

该工作与知域已有 Zero-WAM、S1、VLA-JEPA、Causal World Modeling for Robot Control 和 What-If World 直接相关，适合作为具身 ICL 与因果交互记忆的重点新线索。

## 7. SolarWM: Open Data and Scalable Training for Long-Horizon Video World Models

- **作者**：Junchao Huang, Guian Fang, Shengju Qian, Xianghao Kong, Zhuoran Zhao, Wei Huang, Yihua Du, Zixin Zhang, Justin Cui, Yuchao Gu, Yukang Chen, Xinting Hu, Tianyu He, Shaoshuai Shi, Zhuotao Tian, Xin Wang, Mike Zheng Shou, Li Jiang
- **年份与发表**：2026，arXiv
- **arXiv ID**：2609.02886
- **DOI**：暂无
- **论文**：[arXiv](https://arxiv.org/abs/2609.02886)
- **正式出版**：暂无
- **项目**：[SolarWM 项目页](https://junchao-cs.github.io/SolarWM-Web/)
- **代码**：[GitHub](https://github.com/Junchao-cs/SolarWM)
- **数据**：[Hugging Face 数据集](https://huggingface.co/datasets/junchaoh-cs/SolarWM-Data)；[ModelScope 数据集](https://modelscope.cn/datasets/junchao2003/SolarWM-Data)
- **模型**：项目页提供模型集合链接
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.02886)
- **代表图**：SolarWM 长时世界模型数据与训练流程；来源：[论文原图](https://arxiv.org/html/2609.02886v1/pipeline_2.png)
- **类别标签**：Long-Horizon World Model, Open Data, Video Generation, Camera Conditioning
- **证据等级**：摘要、arXiv comments、项目页和代码仓库已核验；正文待阅读全文
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![SolarWM 长时世界模型数据与训练流程](https://arxiv.org/html/2609.02886v1/pipeline_2.png)

### 核心内容与 Insight

SolarWM 关注世界模型训练中的数据异构问题。论文构建统一数据合同，将 10 个数据集、约 143 万个 canonical clips 转换为包含视觉观测、相机几何、字幕、质量元数据、筛选决策和 provenance 的统一格式。

其训练框架适配 Wan2.2、LTX-2.5 和 MiniMax-H3 等不同视频骨干，并使用多阶段训练和蒸馏支持长时、因果、可交互视频生成。

### Pipeline

**输入**：多来源视频、相机几何、字幕、质量和 provenance 信息。

**过程**：统一数据预处理、相机条件化、骨干原生适配、教师强制自回归初始化、分布匹配蒸馏。

**输出**：支持长时 rollout 的多个视频世界模型。

### 实验与证据

摘要明确给出 143 万 clips、10 个数据集、4 个 5B–33B 模型的信息，并声称支持分钟级实时交互 rollout。需要全文核验：

- 各数据集在训练与测试中的比例；
- 训练数据是否包含 benchmark 测试视频；
- "real-time"具体硬件和帧率；
- 不同骨干之间的比较协议；
- 长时一致性的评价指标和失败率。

### 代码与数据

代码、数据集和项目页已公开链接。Hugging Face 页面本次网络环境无法直接打开，但项目页确认其存在；许可证、完整数据可下载性和模型权重待人工核验。

### 局限、失败案例与开放问题

- 统一数据合同可能掩盖不同数据源的相机、运动和标注偏差。
- 长时视频生成的视觉一致性不一定等于状态一致性。
- 多骨干适配可能导致不同模型的训练目标和计算成本不可直接比较。

### 与知域的关系

SolarWM 对知域的流式生成、长时记忆、Causal Forcing++、minWM 和 ReWorld 路线具有直接参考价值，尤其是数据工程和可复现训练接口。

## 8. Streaming4D: Accelerate 4D World Models via Block-wise Video Generation and Incremental Reconstruction

- **作者**：Xiaoyan Liu, Jiaxin Liu, Kangrui Li, Sifan Zhou
- **年份与发表**：2026，arXiv
- **arXiv ID**：2609.00610
- **DOI**：[10.48550/arXiv.2609.00610](https://doi.org/10.48550/arXiv.2609.00610)
- **论文**：[arXiv](https://arxiv.org/abs/2609.00610)
- **正式出版**：暂无
- **项目**：未提供
- **代码**：未提供
- **数据**：未提供
- **模型**：未提供
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.00610)
- **代表图**：分块视频生成与增量 4D 重建流水线；来源：[论文原图](https://arxiv.org/html/2609.00610v1/pipeline.png)
- **类别标签**：Streaming Generation, 4D Reconstruction, Incremental Reconstruction, world model
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![Streaming4D 分块生成与增量重建流水线](https://arxiv.org/html/2609.00610v1/pipeline.png)

### 核心内容与 Insight

Streaming4D 将分块自回归视频生成和增量 3D 重建紧密耦合。每个视频块完成后立即触发重建，使生成和几何更新并行，而不是等整段视频生成完成后再重建。

### Pipeline

**输入**：初始观测、生成条件、相机或时序信息。

**过程**：按视频块进行自回归生成；每个块完成后送入增量重建后端；视频生成和几何更新并行执行。

**输出**：持续更新的 4D 世界表示和视频流。

### 实验与证据

摘要报告在单张 RTX 4090 上约 \(1.24\times\) 的速度提升，并保持较高 4D 几何和多视角一致性。尚未核验：

- 与哪些 sequential baseline 比较；
- 视频块长度和分辨率；
- 重建误差是否随序列长度增加；
- 并行执行是否引入时序错位；
- 速度提升是否包含 I/O 和模型加载成本。

### 代码与数据

未发现公开代码、数据或模型链接。

### 局限、失败案例与开放问题

增量重建可能出现漂移、错误累积和局部几何不可逆。对于快速运动、遮挡和新区域进入场景的情况，需要额外失败分析。

### 与知域的关系

该工作直接连接知域的 StreamingHOI、4DGS-WAM、DynamicVGGT 和流式生成专题，是本期前馈 4D 与实时交互方向的重要新增工作。

## 9. Matrix-Game 3.5: Enhancing Real-Time Streaming Interactive World Models with Patch Memory

- **作者**：Runjia Qian, Zile Wang, Jihai Zhang, Kai Zou, Wei Yu, Jiaxing Li, Zexiang Liu, Yaokun Li, Fei Kang, Kaichen Huang, Mengyin An, Haobo Zhang, Biao Jiang, Jiahua Wang, Haofeng Sun, Yang Liu, Yangguang Li
- **年份与发表**：2026，arXiv
- **arXiv ID**：2608.29910
- **DOI**：暂无
- **论文**：[arXiv](https://arxiv.org/abs/2608.29910)
- **正式出版**：暂无
- **项目**：[项目页](https://matrix-game-v3-5.github.io/)
- **代码**：[GitHub](https://github.com/Riemann-Dynamics/Matrix-Game-3.5)
- **数据**：未提供
- **模型**：[Hugging Face 模型页](https://huggingface.co/RiemannDynamics/Matrix-Game-3.5-Base)
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2608.29910)
- **代表图**：Matrix-Game 3.5 流式交互世界模型概览；来源：[论文原图](https://arxiv.org/html/2608.29910v1/teaser_white_Riemann.png)
- **类别标签**：Interactive World Model, Streaming Video Generation, Patch Memory, Long-Horizon Consistency
- **证据等级**：摘要、arXiv comments、项目页和代码仓库已核验；正文待阅读全文
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![Matrix-Game 3.5 流式交互世界模型概览](https://arxiv.org/html/2608.29910v1/teaser_white_Riemann.png)

### 核心内容与 Insight

Matrix-Game 3.5 在 Matrix-Game 3.0 基础上引入：

- geometry-aware patch memory；
- tiled-PRoPE 相机条件；
- 静态场景与动态主体解耦；
- 两阶段渐进式实时蒸馏。

目标是提高长时交互中的场景几何、动态主体身份和相机控制一致性。

### Pipeline

**输入**：当前视频帧、用户相机动作、历史 patch memory。

**过程**：检索 3D patch，使用相机条件控制生成；分别建模静态场景和动态主体；通过蒸馏将双向扩散模型转为少步因果生成器。

**输出**：实时交互视频和持续更新的场景记忆。

### 实验与证据

当前摘要主要描述方法改进，尚未核验具体速度、长时长度、基线和一致性指标。项目页和模型页已确认存在，但模型下载和复现实验尚未验证。

### 代码与数据

代码、项目页和模型链接公开；数据开放情况待核验。

### 局限、失败案例与开放问题

- Patch memory 的检索错误可能导致历史几何污染。
- 静态—动态解耦在复杂交互、遮挡和主体拓扑变化时可能失效。
- 少步蒸馏可能牺牲细节和动作响应稳定性。

### 与知域的关系

该工作延续知域已有 Causal Forcing、Causal Forcing++、minWM 和交互视频世界模型路线，重点贡献在长期记忆和几何一致性。

## 10. Seeing the World and the Self from Egocentric Video

- **作者**：Kai Guan, Minchao Jiang, Ruichen WangLi, Wentao Zhu, Lei Zhang
- **年份与发表**：2026，arXiv
- **arXiv ID**：2609.01276
- **DOI**：暂无
- **论文**：[arXiv](https://arxiv.org/abs/2609.01276)
- **正式出版**：暂无
- **项目**：未提供
- **代码**：未提供
- **数据**：EE4D-JSM，基于 EgoExo4D 构建；具体发布状态待核验
- **模型**：未提供
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.01276)
- **代表图**：RESELF 第一视角场景与自运动联合重建概览；来源：[论文原图](https://arxiv.org/html/2609.01276v1/fig_teaser.png)
- **类别标签**：egocentric vision, 4D Reconstruction, Human Motion, Scene Geometry
- **证据等级**：仅摘要与 arXiv 元数据核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![RESELF 第一视角场景与自运动联合重建概览](https://arxiv.org/html/2609.01276v1/fig_teaser.png)

### 核心内容与 Insight

论文提出 RESELF，同时恢复第一视角视频中的环境场景和穿戴者自身全身运动。它将可见场景的确定性几何重建与严重遮挡身体的生成式运动推断结合起来。

### Pipeline

**输入**：第一视角视频、相机运动、场景观测。

**过程**：使用几何基础模型重建场景和相机轨迹；将几何特征和相机轨迹作为条件输入扩散模型，生成穿戴者运动；通过闭环运动学反馈进一步修正相机头部。

**输出**：场景几何、相机轨迹和穿戴者 4D 运动。

### 实验与证据

摘要说明构建了 EE4D-JSM 数据集，并提出几何条件运动生成框架。尚未核验数据规模、指标、与 EgoExo4D 的划分方式以及身体运动精度。

### 代码与数据

数据集和代码开放状态未确认。

### 局限、失败案例与开放问题

- 身体严重遮挡会导致运动生成存在多解。
- 场景几何误差可能通过条件输入传递到身体运动。
- 相机、身体和场景的联合尺度估计仍可能不稳定。

### 与知域的关系

该工作补充知域的 DreamHand、HandsOnWorld、EgoForge、EgoSim 和 4D hand reconstruction 路线，强调"世界"和"自我"必须在同一坐标系中建模。

## 11. Puffin-World: Scaling a Unified Multimodal Model with Native 3D World States

- **作者**：Kang Liao, Yihang Luo, Xiao-Ming Wu, Linyi Jin, Size Wu, Chunyu Lin, Yao Zhao, Fei Wang, Wei Li, Chen Change Loy
- **年份与发表**：2026，arXiv
- **arXiv ID**：2609.04196
- **DOI**：暂无
- **论文**：[arXiv](https://arxiv.org/abs/2609.04196)
- **正式出版**：暂无
- **项目**：[Puffin-World 项目页](https://kangliao929.github.io/projects/puffin-world/)
- **代码**：[GitHub](https://github.com/KangLiao929/Puffin)
- **数据**：[Hugging Face 数据集集合](https://huggingface.co/collections/KangLiao/puffin-world)
- **模型**：[Hugging Face 模型集合](https://huggingface.co/collections/KangLiao/puffin-world)
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.04196)
- **代表图**：Puffin-World 原生 3D 世界状态与多模态生成概览；来源：[论文原图](https://arxiv.org/html/2609.04196v1/teaser_new_sub1_crop.png)
- **类别标签**：Native 3D World State, Physical World Model, Multimodal Model, World Generation
- **证据等级**：摘要、arXiv comments、项目页和 GitHub 已核验；正文待阅读全文
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![Puffin-World 原生 3D 世界状态与多模态生成概览](https://arxiv.org/html/2609.04196v1/teaser_new_sub1_crop.png)

### 核心内容与 Insight

Puffin-World 将物理状态、几何状态和外观状态作为统一模型中的原生世界状态，并使用 Omni-Camera 表示支持多种相机运动。论文还构建 Puffin-16M，包括约 1500 万 vision-language-camera triplets 和约 100 万条轨迹。

摘要声称发布代码、模型和数据。

### Pipeline

**输入**：图像、语言、相机参数、物理和几何条件。

**过程**：联合建模重力场、纬度、深度和外观；传播未来物理动态；在生成未来视图的同时重建其几何。

**输出**：未来视图、深度、物理状态和可交互世界表示。

### 实验与证据

摘要强调统一建模和规模化数据，但尚未核验：

- Puffin-16M 的数据来源与训练测试划分；
- 物理状态是否由真实传感器或模拟器提供；
- 生成质量、几何质量和物理一致性的具体指标；
- 与 VGGT、DynamicVGGT、世界视频模型的比较。

### 代码与数据

项目页确认 GitHub、模型和数据链接。Hugging Face 页面本次无法直接访问，权重和许可证待人工确认。

### 局限、失败案例与开放问题

- 物理状态的显式表示可能依赖合成或弱标注数据。
- 统一模型同时生成外观和几何，训练目标可能存在冲突。
- 复杂动态场景中的绝对相机与物理状态估计仍需验证。

### 与知域的关系

Puffin-World 对知域的前馈重建、物理世界模型、3D/4D 生成和 Causal-JEPA 路线具有较强参考价值。

## 12. IMPACT: Attention Is the Interaction Map for Scalable Interaction-Aware World Model Training

- **作者**：Rongze Tang, Jianjie Fang, Zhaolu Wang, Ziyou Wang, Xvyuan Liu, Haisheng Su, Xin Zhang, Wei Wu, Chen Gao, Yong Li, Zhibo Chen
- **年份与发表**：2026，arXiv
- **arXiv ID**：2609.00161
- **DOI**：[10.48550/arXiv.2609.00161](https://doi.org/10.48550/arXiv.2609.00161)
- **论文**：[arXiv](https://arxiv.org/abs/2609.00161)
- **正式出版**：暂无
- **项目**：[IMPACT 官方项目页](https://embodiedcity.github.io/IMPACT/)
- **代码**：未提供
- **数据**：未提供
- **模型**：未提供
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.00161)
- **代表图**：交互感知世界模型训练概览；来源：[论文原图](https://arxiv.org/html/2609.00161v1/overview_v5.png)
- **类别标签**：Interaction-Aware World Model, Attention Calibration, Hand-Object Interaction, Video Diffusion
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![IMPACT 交互感知世界模型训练概览](https://arxiv.org/html/2609.00161v1/overview_v5.png)

### 核心内容与 Insight

IMPACT 认为全局平均 MSE 去噪目标会让静态区域主导训练信号，使真正决定交互的动态物体区域受到不足监督。方法使用与被操作物体 token 相关的 cross-attention 作为内部时空先验，再结合局部预测误差构造 interaction map，对去噪监督重新加权。

### Pipeline

**输入**：动作条件视频、交互对象 token、扩散模型 cross-attention 和局部误差。

**过程**：提取 attention 先验，校准局部误差，生成交互区域权重，重加权视频扩散训练目标。

**输出**：更加关注交互区域的世界模型。

### 实验与证据

摘要声称在机器人操作视频上进行了实验，并改善交互生成质量。具体数据集、指标、baseline 和提升幅度尚未核验。

### 代码与数据

未发现公开链接。

### 局限、失败案例与开放问题

- Attention 不一定对应真实交互因果区域。
- 交互对象 token 的识别错误可能导致错误监督。
- 局部重加权可能损害背景和全局几何一致性。

### 与知域的关系

IMPACT 直接对应知域的 HOI、交互世界模型和 StreamingHOI 方向，提供了不依赖外部密集标注的交互区域监督思路。

## 13. VeriPhy: Agentic Physical Reasoning for World Model Evaluation and Refinement

- **作者**：Wenzhuo Xu, Yuchen Zhu, Chongjian Ge, Xuan Shen, Jing Shi, Jason Kuen, Yongxin Chen, Molei Tao, Christopher McComb, Noelia Grande Gutiérrez, Jiuxiang Gu
- **年份与发表**：2026，arXiv
- **arXiv ID**：2609.03153
- **DOI**：暂无
- **论文**：[arXiv](https://arxiv.org/abs/2609.03153)
- **正式出版**：暂无
- **项目**：未提供
- **代码**：未提供
- **数据**：1500-clip 物理缺陷语料，具体开放状态待核验
- **模型**：未提供
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.03153)
- **代表图**：VeriPhy 物理推理与验证示例；来源：[论文原图](https://arxiv.org/html/2609.03153v1/figs/assets/ball_wall_studio_bg_v4.png)
- **类别标签**：Physical Reasoning, World Model Evaluation, Video Verification, Auditable Evidence
- **证据等级**：仅摘要与 arXiv 元数据核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![VeriPhy 物理推理与验证示例](https://arxiv.org/html/2609.03153v1/figs/assets/ball_wall_studio_bg_v4.png)

### 核心内容与 Insight

VeriPhy 将 prompt 编译成类型化物理义务和执行计划，再调用冻结的低层专家进行分割、跟踪、计数、深度、OCR、音频事件和物理测量。每条结果都携带 provenance，最后输出 supported、contradicted 或 unknown 三值判断。

### Pipeline

**输入**：生成视频、文本提示、物理约束。

**过程**：规划物理义务，执行经过验证的测量，记录证据来源，使用固定 resolver 将证据组合成三值状态。

**输出**：带证据链的物理可靠性判断和可定位失败记录。

### 实验与证据

摘要报告：

- 1500 个带人工标注缺陷记录的视频；
- 核心子集 149 个视频、304 条缺陷记录；
- VeriPhy 覆盖 228 条记录；
- 对比方法覆盖 164 条记录。

这些数字仍需核验评测协议、人工标注一致性、召回率与误报率。

### 代码与数据

尚未确认公开代码和数据。

### 局限、失败案例与开放问题

- 固定低层专家的错误会限制上层验证器。
- 三值判断不能完全描述复杂、连续或多义的物理违规。
- 物理规则编译质量决定最终覆盖范围。

### 与知域的关系

该工作为知域的物理世界模型、Causal-JEPA、世界模型可靠性和生成视频评测提供了可操作的验证框架。

## 14. Principia: Relational Physics Tests for Video Models

- **作者**：Varun Varma Thozhiyoor, Shivam Tripathi, Venkatesh Babu Radhakrishnan, Anand Bhattad
- **年份与发表**：2026，arXiv
- **arXiv ID**：2609.04200
- **DOI**：暂无
- **论文**：[arXiv](https://arxiv.org/abs/2609.04200)
- **正式出版**：暂无
- **项目**：[Principia 项目页](https://principiabench.github.io/)
- **代码**：项目页已确认，具体仓库待核验
- **数据**：项目页已确认，具体下载方式待核验
- **模型**：未提供
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.04200)
- **代表图**：Principia 关系物理评测数据概览；来源：[论文原图](https://arxiv.org/html/2609.04200v1/dataset_teaser3.png)
- **类别标签**：Physics Benchmark, Video Generation, Relational Consistency, Physical Reasoning
- **证据等级**：摘要、arXiv comments 和项目页已核验；正文待阅读全文
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![Principia 关系物理评测数据概览](https://arxiv.org/html/2609.04200v1/dataset_teaser3.png)

### 核心内容与 Insight

Principia 不依赖绝对尺度、帧率或相机标定，而是评估同一场景中两个物体之间是否遵循相同物理规律。benchmark 覆盖重力、恢复系数、摩擦、转动惯量、抛体运动、动量、摆和弹簧等现象。

### Pipeline

**输入**：真实或生成视频、物体轨迹和物理关系。

**过程**：提取对象运动，计算标定无关的关系一致性，判断生成结果是否违反物理规律。

**输出**：关系物理一致性分数及按现象划分的评测结果。

### 实验与证据

摘要报告多个视频生成模型在 Principia 上最高分不超过 0.42，而 VBench 约为 0.8；VLM 物理违规识别最高准确率为 67%。这些结果支持"视觉流畅不等于物理可靠"，但需要核验生成样本数量、提示词和评分细节。

### 代码与数据

项目页已公开，代码和数据的具体开放范围待人工检查。

### 局限、失败案例与开放问题

- 关系物理覆盖有限，不能替代所有世界状态评估。
- 从视频中提取对象和轨迹本身可能引入误差。
- 真实视频与生成视频的摄影条件差异可能影响比较。

### 与知域的关系

Principia 为知域的物理世界模型和视频生成评估提供了比 VBench 更针对物理关系的补充指标。

## 15. Do Video Generators Track the World Across Segments? A Benchmark and Method for World-State Reasoning in Video Continuation

- **作者**：Yingmao Miao, Pengfei Zhang, Chaoran Xu, Meng Yu, Jing Tang, Xiangxiang Chu, Chao Shen, Chenhao Lin
- **年份与发表**：2026，arXiv
- **arXiv ID**：2609.03673
- **DOI**：暂无
- **论文**：[arXiv](https://arxiv.org/abs/2609.03673)
- **正式出版**：暂无
- **项目**：未提供
- **代码**：未提供
- **数据**：Statebench，开放状态待核验
- **模型**：Stateagent 方法，具体模型待核验
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.03673)
- **代表图**：视频续接中的世界状态推理评测概览；来源：[论文原图](https://arxiv.org/html/2609.03673v1/Figures/teaser.jpg)
- **类别标签**：World-State Reasoning, Video Continuation, Long-Horizon Memory, Benchmark
- **证据等级**：仅摘要与 arXiv 元数据核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![视频续接中的世界状态推理评测概览](https://arxiv.org/html/2609.03673v1/Figures/teaser.jpg)

### 核心内容与 Insight

论文区分"历史画面记忆"和"由历史动作决定的世界状态"。Statebench 覆盖过去可见状态、遮挡过程状态和复杂转移状态，用于检验视频续接是否真正反映历史视频和新 prompt 共同决定的后续状态。

### Pipeline

**输入**：历史视频、历史 prompt、新 prompt。

**过程**：维护实体—状态表示，根据新 prompt 更新状态，再生成视频续接。

**输出**：包含正确世界状态的后续视频。

### 实验与证据

摘要介绍 benchmark 和 Stateagent，但未提供足够定量结果。需要全文核验：

- 状态标注如何获得；
- 续接视频的评价指标；
- 与普通历史帧检索和视频扩展方法的比较；
- 遮挡状态是否存在唯一答案。

### 代码与数据

未确认公开链接。

### 局限、失败案例与开放问题

- 隐式状态可能无法从历史视频唯一确定。
- 结构化状态表示可能遗漏连续物理量。
- benchmark 设计可能偏向显式实体和离散状态。

### 与知域的关系

该工作直接影响知域对长时记忆、交互视频和世界状态接口的研究，补充 R2M-Bench、ReWorld 和 Matrix-Game 系列。

## 16. Can Video World Models Track Unobserved World States?

- **作者**：Joonghyuk Shin, Yicong Hong, Jaesik Park, Xun Huang
- **年份与发表**：2026，arXiv
- **arXiv ID**：2608.30692
- **DOI**：暂无
- **论文**：[arXiv](https://arxiv.org/abs/2608.30692)
- **正式出版**：暂无
- **项目**：[项目页](https://joonghyuk.com/stateful-vwm-web/)
- **代码**：项目页链接待核验
- **数据**：Shell Game 任务和动态探索任务，开放状态待核验
- **模型**：未提供
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2608.30692)
- **代表图**：不可见世界状态追踪实验设置；来源：[论文原图](https://arxiv.org/html/2608.30692v1/toy_s3_s5_exp.svg)
- **类别标签**：Hidden State, Video World Model, Stateful Memory, Extrapolation
- **证据等级**：摘要、arXiv comments 和项目页已核验；正文待阅读全文
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![不可见世界状态追踪实验设置](https://arxiv.org/html/2608.30692v1/toy_s3_s5_exp.svg)

### 核心内容与 Insight

论文使用 action-conditioned video Shell Game 检验视频世界模型是否追踪不可见的隐状态。摘要称多种模型在训练长度内能够拟合，但在更长交换链上趋近随机猜测；仅增加去噪步骤不能解决问题。

论文进一步指出，能够外推的机制需要跨块维护并原地更新状态，例如允许负特征值的线性注意力或 TTT fast weight。

### Pipeline

**输入**：历史视觉、动作、隐状态转移和视频生成模型。

**过程**：在视频生成同时维持隐藏状态；通过长链交换和动态探索检验状态是否被持续更新。

**输出**：未来观测及隐状态预测能力。

### 实验与证据

摘要明确报告训练 horizon 为 5 次交换，超过该长度后多数模型性能趋近随机。需要全文核验具体模型、训练配置、状态准确率和动态探索实验。

### 代码与数据

项目页已确认；代码和数据开放范围待人工核验。

### 局限、失败案例与开放问题

- Shell Game 是人为构造的离散隐状态任务。
- 该任务中的状态记忆机制未必直接迁移到连续机器人动力学。
- 隐状态追踪能力和视频质量之间的关系仍需单独分析。

### 与知域的关系

该工作为知域的 Causal-JEPA、世界状态记忆、长时交互和 WorldSimProbe 提供了重要诊断任务。

## 17. One Demonstration, Many Objects: Generalizing Manipulation via Local Contact Geometry

- **作者**：Satvik Sharma, Samrat Sahoo, Huang Huang, Fei-Fei Li, Jiajun Wu, Dorsa Sadigh, Jeannette Bohg
- **年份与发表**：2026，arXiv v2
- **arXiv ID**：2609.01938
- **DOI**：暂无
- **论文**：[arXiv](https://arxiv.org/abs/2609.01938)
- **正式出版**：暂无
- **项目**：未提供
- **代码**：未提供
- **数据**：未提供
- **模型**：未提供
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.01938)
- **代表图**：单示范跨物体接触几何泛化概览；来源：[论文原图](https://arxiv.org/html/2609.01938v2/splash_fig.png)
- **类别标签**：Dexterous Manipulation, Contact Geometry, Human Demonstration, Sim-to-Real
- **证据等级**：摘要与 arXiv 元数据核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![单示范跨物体接触几何泛化概览](https://arxiv.org/html/2609.01938v2/splash_fig.png)
- **本次变化**：窗口内从 v1 更新为 v2，摘要内容发生补充；因未发现知域已有记录，按新论文收录。

### 核心内容与 Insight

DemoMimic 使用接触点附近的局部几何作为操作泛化依据，并通过 contact-centric reward 鼓励精准接触。摘要声称单个真实世界策略可跨越不同形状、尺度、质量和摩擦的物体。

### Pipeline

**输入**：人类示范、物体几何、机器人手状态。

**过程**：提取局部接触几何，将接触奖励加入策略训练，并在仿真到真实迁移中保持接触结构。

**输出**：跨物体和跨机械手的灵巧操作策略。

### 实验与证据

摘要报告在 16 个物体、4 个任务和 2 种机械手上达到 71% 成功率，并称具有较小 sim-to-real drop。尚未核验每个任务的样本数、失败类型和 baseline 训练预算。

### 代码与数据

未确认开放状态。

### 局限、失败案例与开放问题

局部接触结构相似并不保证整体动力学、摩擦和可达性相似。对于多接触、软物体、遮挡和动态物体，方法的有效性仍需验证。

### 与知域的关系

该工作把 HOI 的几何与接触结构转化为机器人泛化信号，适合与知域的 HOI-Dyn、Hand-Object World Model 和具身视频学习路线结合。

## 18. Facet-0: A Robotic Foundation Model for Contact-Rich Precise Manipulation

- **作者**：Haoyuan Deng, Haichao Liu, Wenkai Guo, Yuan Ling, Zaijia Yang, Yuanjiang Xue, Haosheng Sun, Liangzi Wang, Ziwei Wang
- **年份与发表**：2026，arXiv
- **arXiv ID**：2609.01596
- **DOI**：[10.48550/arXiv.2609.01596](https://doi.org/10.48550/arXiv.2609.01596)
- **论文**：[arXiv](https://arxiv.org/abs/2609.01596)
- **正式出版**：暂无
- **项目**：[Facet-0 项目页](https://pine-lab-ntu.github.io/facet-0/)
- **代码**：项目页已确认，但仓库地址待核验
- **数据**：ManuFacet-1K，开放状态待核验
- **模型**：项目页已确认，具体权重待核验
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.01596)
- **代表图**：Facet-0 接触丰富操作任务概览；来源：[论文原图](https://arxiv.org/html/2609.01596v1/Teaser1.png)
- **类别标签**：Contact-Rich Manipulation, Action-Wrench Modeling, Flow Matching, Robotic Foundation Model
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![Facet-0 接触丰富操作任务概览](https://arxiv.org/html/2609.01596v1/Teaser1.png)

### 核心内容与 Insight

Facet-0 将动作与未来腕部力矩轨迹联合建模。模型通过 action-wrench proposal 预测动作及其可能诱导的接触后果，并使用 Action-Wrench Critic 区分任务进度相似但接触结果不同的动作。

摘要声称 ManuFacet-1K 包含约 1000 小时力同步数据，覆盖 3 种本体和多个制造单元。

### Pipeline

**输入**：视觉语言语义、运动学状态、历史力矩、可执行动作。

**过程**：流匹配生成动作块和未来腕部力矩；使用分布式 Action-Wrench Critic、阶段奖励和接触选择性 credit 进行策略改进。

**输出**：精密操作动作和接触后果预测。

### 实验与证据

摘要报告在 5 个亚毫米级计算机装配任务上达到 82% 平均成功率，强 baseline 为 15%。需要全文核验：

- 任务是否与训练数据存在相同工位或部件；
- 82% 是否为单次部署或多次重复均值；
- 力传感器在测试时是否可用；
- 与传统视觉策略、力控策略和 VLA 的公平比较。

### 代码与数据

项目页已确认。ManuFacet-1K、模型权重和代码的开放范围待人工核验。

### 局限、失败案例与开放问题

- 力矩预测质量不等于接触控制质量。
- 工业装配数据可能具有较窄的任务和工位分布。
- 亚毫米级成功率对标定、夹具和部件容差非常敏感。

### 与知域的关系

Facet-0 将知域关注的 HOI、动作后果预测和物理世界模型推进到接触力层面，可作为视觉世界模型之外的多模态接触建模参考。

## 19. Temporal Forcing: 4D Representation Alignment for Vision-Language-Action Models

- **作者**：Xingyu Ding, Yuzhong Zhao, Chunhai Zhao, Yinghuan Shi, Chaoyang Zhao, Yifan Zhang
- **年份与发表**：2026，arXiv
- **arXiv ID**：2608.30643
- **DOI**：[10.48550/arXiv.2608.30643](https://doi.org/10.48550/arXiv.2608.30643)
- **论文**：[arXiv](https://arxiv.org/abs/2608.30643)
- **正式出版**：未发现
- **项目**：未发现
- **代码**：作者声明将公开，检查时尚未发现
- **数据**：使用 LIBERO、RoboTwin 2.0 和自建物理任务
- **模型**：未发现公开权重
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2608.30643)
- **代表图**：Figure 1，3D 对齐与 Temporal Forcing 的时序表示对比；来源：[论文原图](https://arxiv.org/html/2608.30643v1/fig1.png)
- **类别标签**：4D Representation, VLA, Long-Horizon Manipulation, History Modeling
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![Temporal Forcing 的时序表示对齐框架](https://arxiv.org/html/2608.30643v1/fig1.png)

### 核心内容与 Insight

论文引入历史路径，并让其 latent 对齐预训练 4D foundation model 的时间一致几何特征。4D 模型只在训练期充当教师，部署时保留基础 VLA 和历史路径。

### Pipeline

**输入**：有界视觉历史、语言任务和机器人状态。

**过程**：历史路径压缩多帧观测；4D 教师从更长因果窗口提取几何 target；当前帧损失锚定局部几何，时间损失约束历史 latent 的状态演化。

**输出**：依赖历史状态的动作；推理时不运行 4D 教师。

### 实验与证据

报告 LIBERO 平均成功率 98.8%，RoboTwin 2.0 十二项任务从 53.5% 提至 62.8%，隐藏放置任务从 20.0% 提至 43.3%。同基础模型受控表中基础为 90.7%、完整方法为 93.6%，仅加入历史为 88.2%；不同表格配置不可直接混用。

### 代码与数据

代码仅声明未来公开；未发现 checkpoint 或自建物理任务数据，暂难复核 4D target 构造成本。

### 局限、失败案例与开放问题

物理实验只有一个多阶段场景；历史窗口、快速动态和跨任务状态泛化不明。收益可能同时来自 4D 教师的语义与几何先验，需要更细对照。

### 与知域的关系

直接连接 VGGT/DynamicVGGT 类 4D 几何模型与 VLA，提供“4D teacher、轻量 history student”路线。

## 20. RoboPhys-3D: A Comprehensive Embodied World Model Evaluation via 3D Reconstruction

- **作者**：Tianyi Wang, Jiazhou Chen, Yiming Xu, Xiangyu Li, Tianyi Zeng, Chih-Hsien Chou, Ning Lu, Liang Peng, Junfeng Jiao, Christian Claudel
- **年份与发表**：2026，arXiv
- **arXiv ID**：2608.28718
- **DOI**：[10.48550/arXiv.2608.28718](https://doi.org/10.48550/arXiv.2608.28718)
- **论文**：[arXiv](https://arxiv.org/abs/2608.28718)
- **正式出版**：未发现
- **项目**：未发现
- **代码**：未发现
- **数据**：RoboPhys-3D；论文描述 5,000 个 episode、25,000 个多视图参考视频
- **模型**：不适用
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2608.28718)
- **代表图**：Figure 1，基于 3D 重建的世界模型评测框架；来源：[论文原图](https://arxiv.org/html/2608.28718v1/fig1.png)
- **类别标签**：Embodied World Model Evaluation, 3D Reconstruction, Robot Manipulation Benchmark, VGGT
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![RoboPhys-3D 基于重建的世界模型评测框架](https://arxiv.org/html/2608.28718v1/fig1.png)

### 核心内容与 Insight

RoboPhys-3D 用同一重建 pipeline 处理参考视频和生成视频，从而估计重建器自身误差，避免把所有几何偏差归因于世界模型。

### Pipeline

**输入**：初始帧、指令、参考多视图轨迹和世界模型生成视频。

**过程**：用 VGGT、VGGT-\(\Omega\)、4DGS、4C4D 等恢复 3D/4D 表示；计算像素、几何、状态理解和任务完成四层指标；构造 Average Full Score 与 RoboPhyscore。

**输出**：对世界模型和 reconstruction backend 的分层诊断分数。

### 实验与证据

四个被测模型中 Cosmos RoboPhyscore 为 0.6330，Wan 为 0.5359。RoboPhyscore 与人工评分 Pearson \(r=0.9761\)、Spearman \(\rho=0.8962\)；重建方法可使分数变化最多 21.8%。这支持校准重建误差，但覆盖的模型与 backend 数量有限。

### 代码与数据

正文描述了数据和协议，但本次未找到公开代码或数据入口，暂不能确认 benchmark 可直接运行。

### 局限、失败案例与开放问题

仅覆盖 RoboTwin 2.0 单一模拟平台和 embodiment；缺少真实机器人与跨硬件评测。指标按当前任务成功相关性选择，可能对模型集合过拟合。

### 与知域的关系

为 Video/WAM 与 VGGT 类重建模型提供交叉评测，适合审查视觉质量、几何正确性和可执行性之间的差异。

## 21. Video Generative Models as Geometry Learner

- **作者**：Haosen Yang, Jifei Song, Zhensong Zhang, Xiatian Zhu, Jiankang Deng
- **年份与发表**：2026，ECCV 2026
- **arXiv ID**：2608.28549
- **DOI**：[10.48550/arXiv.2608.28549](https://doi.org/10.48550/arXiv.2608.28549)
- **论文**：[arXiv](https://arxiv.org/abs/2608.28549)
- **正式出版**：ECCV 2026；正式论文页尚未发现
- **项目**：[GeoNeXt 官方项目页](https://happy-hsy.github.io/projects/GeoNeXt/)
- **代码**：[GitHub](https://github.com/Creative-Intelligence-Studio/GeoNeXt)
- **数据**：使用 Hypersim 与 Virtual KITTI 2
- **模型**：[Hugging Face](https://huggingface.co/happy0612/GeoNeXt)
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2608.28549)
- **代表图**：GeoNeXt 的图像—深度—法线统一框架；来源：[论文原图](https://arxiv.org/html/2608.28549v1/fig2_final.png) · [官方项目页](https://happy-hsy.github.io/projects/GeoNeXt/)
- **类别标签**：Geometry Estimation, Video Diffusion, Feedforward Reconstruction, Depth, Surface Normal
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

![GeoNeXt 的图像—深度—法线统一框架](https://arxiv.org/html/2608.28549v1/fig2_final.png)

### 核心内容与 Insight

GeoNeXt 把深度和法线视作输入图像之后的“后续帧”，利用视频扩散模型的时间注意力在图像、深度和法线之间传递结构，并沿同一去噪轨迹联合预测几何。

### Pipeline

**输入**：单张 RGB。

**过程**：冻结 VAE 将 RGB、深度和法线编码为统一 latent；复制图像 latent 作为几何槽位条件；移除原 SVD 的 CLIP 条件并微调去噪 U-Net；推理联合去噪三类 latent。

**输出**：仿射不变深度和表面法线，可进一步构建网格。

### 实验与证据

训练使用约 39K Hypersim 和 20K Virtual KITTI 2 样本，并在未见深度和法线数据集测试。NYUv2、KITTI、ETH3D、ScanNet、DIODE 的 AbsRel 为 5.3、8.2、5.6、5.9、22.6，整体优于统一生成式 baseline GeoWizard，但并非每项都超过专用判别模型。

### 代码与数据

官方仓库已于 2026-08-31 发布推理代码，并公开 GeoNeXt-Wan 与 GeoNeXt-SVD 权重；仓库注明推理至少约需 24 GB GPU 显存。

### 局限、失败案例与开放问题

默认结果使用 5 个去噪步骤并对 5 个随机种子 ensemble，成本高于单次判别前馈；深度为仿射不变而非公制深度；透明、反射和极端遮挡失败案例缺少系统分析。

### 与知域的关系

展示了生成模型与前馈几何的双向迁移，与 VGGT、SAM 3D、Gen3R、PixWorld、UniRecGen 等重建—生成统一路线直接相关。

## 22. AnyWorld: Factorized Egocentric World Models for Cross-Embodiment Generalization

- **作者**：Cheng Chen, Jerry Bai, Jiacheng Wei, Boyu Chen, Xiaoji Zheng, Fan Wu, Minghao Yang, Tianrun Chen, Ruibo Li, Xiaoyu Yue, Xiaoyang Guo, Yixiao Ge, Guosheng Lin, Fayao Liu
- **年份与发表**：2026，arXiv v2
- **arXiv ID**：2608.29242
- **DOI**：[10.48550/arXiv.2608.29242](https://doi.org/10.48550/arXiv.2608.29242)
- **论文**：[arXiv](https://arxiv.org/abs/2608.29242) · [HTML 全文](https://arxiv.org/html/2608.29242v2)
- **正式出版**：未发现
- **项目**：[AnyWorld 官方项目页](https://xpeng-robotics.github.io/anyworld/)
- **代码**：[GitHub](https://github.com/xpeng-robotics/AnyWorld)
- **数据**：使用 EgoDex、RoboCasa GR1 与 IRON 视频；未发现独立数据集下载页
- **模型**：官方仓库说明发布 AnyWorld ImageEditor 与 WorldModel 权重，具体下载入口和许可证待核验
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2608.29242)
- **代表图**：Figure 1，从单个人类第一视角交互重组多样机器人经验并用于 VLA 适配；来源：[论文原图](https://arxiv.org/html/2608.29242v2/method_figure_v2.png)
- **类别标签**：Cross-Embodiment World Model, Egocentric Video, World Action Model, Experience Recomposition, Robot Learning
- **证据等级**：arXiv v2 全文、官方项目页和官方代码仓库已核验
- **更新类型**：用户指定补充的新论文
- **知域匹配结果**：按 arXiv ID 与规范化标题均未发现已有记录
- **现有知域 ID**：无

![AnyWorld 从人类交互到机器人经验的因子化重组框架](https://arxiv.org/html/2608.29242v2/method_figure_v2.png)

### 核心内容与 Insight

AnyWorld 把第一视角交互拆成动作、相机和目标 embodiment/context 三组条件：图像平面骨架控制描述“发生什么运动”，Plücker ray 描述视角如何演化，目标首帧与 embodiment tag 指定身体、场景布局、物体配置和初始交互几何。这样，同一人类交互可以在没有成对人—机器人视频的条件下重组为多种机器人域 rollout。

关键边界是：论文没有声称把场景因素完全解耦；场景、物体和初始几何仍由目标首帧共同承载。它也不是把人类关节动作直接复制给机器人，而是在下游数据构造时另用 action-calibration module 将人类腕部轨迹映射到机器人相对末端执行器动作空间。

### Pipeline

**输入**：人类第一视角交互视频、渲染的动作骨架控制视频、相机内外参与 Plücker ray、目标机器人首帧、embodiment tag 和任务文本。

**过程**：先用 200K EgoDex clips 预训练 action-camera conditioned video prior，再用未配对的 EgoDex、RoboCasa GR1 和 IRON 视频做 mixed-embodiment fine-tuning；推理时固定或替换动作、相机、目标首帧和 embodiment tag，生成目标机器人域视频。用于 VLA 时，视觉重组与腕部轨迹到机器人相对 EEF 动作的校准并行进行，形成机器人域视频—动作对。

**输出**：可独立控制动作、视角和 embodiment/context 的机器人域 rollout，以及用于目标机器人策略适配的视觉—动作训练经验。

### 实验与证据

在 60 个 EgoDex、RoboCasa GR1 与 IRON 测试视频上，AnyWorld 的 ActionAlign、CameraAlign、EmbodAcc 分别为 0.659、0.789、0.886，平均 0.778；WAN Fun-Control 的平均值为 0.609，Cosmos-Predict2.5 为 0.417。VBench 四项均值为 0.971，与两条 baseline 的 0.968、0.962 接近，说明可控性提升没有在这些代理视频质量指标上出现明显退化。

在下游 UniT 系 VLA 适配中，加入重组经验后，RoboCasa GR1 的 18 项 pick-and-place 成功率从 49.8% 提升至 54.6%；真实 IRON 机器人 20 次香蕉抓取从 20.0% 提升至 55.0%。定向干预实验还显示：只加入左右 counterfactual actions 而保留原单侧视觉状态，空间指令跟随仍不稳定；同时重组机器人域视觉状态和动作后，策略才稳定切换左右目标。该结果支持“视觉状态覆盖 + 动作校准”的联合数据机制，但不构成 SCM、因果识别或一般反事实推理证明。

### 代码与数据

官方 GitHub 已公开 image editing、world model inference、训练/推理脚本、数据格式和模型权重布局说明，代码采用 Apache-2.0。仓库说明 AnyWorld 的适配 Transformer 与 Wan2.1 Combined-Control 基础组件分开提供；本次未发现独立数据集下载页，具体权重入口与上游模型许可证仍需按官方文档复核。

### 局限、失败案例与开放问题

- 视觉 rollout 不能完整表示精细接触控制所需的触觉与接触力。
- 方法依赖可靠的动作—相机提取；严重遮挡、快速运动、tracking error 和强烈相机抖动会降低可控性。
- 当前只覆盖 human、RoboCasa GR1 和 IRON 三类 embodiment，真实机器人结果仅 20 次抓取；对更多形态、物体、软体交互与长时任务的泛化尚未建立。
- ActionAlign、CameraAlign 和 CLIP-based EmbodAcc 都是代理指标，不能单独证明生成视频保持了完整 3D 几何或真实动力学。

### 与知域的关系

AnyWorld 位于知域几条主线的交叉点：它把 egocentric human video 转成跨具身 WAM 的可控经验源；用图像平面运动和相机几何分离动作与视角；并通过真实机器人策略适配检验生成经验是否真正可用。它适合与 Zero-WAM、Vid2WAM、UniT、Scaling Cross-Embodiment World Models、EgoSim 和 XEWorld 对照，重点比较“共享动作表示”“视觉重组”“显式 3D/4D 状态”和“真实闭环收益”各自的贡献。
