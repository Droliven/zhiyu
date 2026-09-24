# 代码与 Agent 世界模型：可执行状态、视觉渲染与闭环验证

**更新日期**：2026-09-24

**报告标签**：Agent与可执行世界, 世界模型, 物理建模与仿真

> 按代码在系统中的职责区分世界构造、观测解释、持久状态、视觉渲染和机器人编排，比较“能运行”“拟合观测”与“预测真实后果”的证据差别。

本报告以现有馆藏为检索范围。正文区分方法事实、实验支持与综合判断；未完成全文核验的条目只作延伸线索，不据此建立定量排名。不同任务、输入权限、数据量和执行预算的成绩不直接横排。

[toc]

## 统一问题：谁持有世界状态，谁负责世界演化

代码进入世界模型至少有三种方式：写程序生成一个场景；用可执行程序解释已有视频；由程序维护持续世界状态，再让生成器渲染观察。三者都可能使用编码 Agent，却有不同的输入、真值和成功标准。

“Agentic”也不是一种统一世界表征。Agent 可以是代码作者、测量与优化调度器、规划器或机器人技能路由器。只有说明 Agent 修改了什么状态、调用何种执行器、通过何种证据接受结果，架构才可比较。

## 从任务到执行器的分类

| 系统角色 | 代表工作 | 状态与执行器 | 成功标准 |
| --- | --- | --- | --- |
| 从要求构造动态资产 | [SimWorlds](https://arxiv.org/abs/2607.01766) | Blender对象、动画、模拟及场景协议 | 要求落实到可检查对象和运动 |
| 从观测发现可执行解释 | [Code as Worlds](https://arxiv.org/abs/2608.27549) | 对象、参数、运动及渲染程序 | 模拟与视觉证据一致，状态可用于定量问答 |
| 从视频联合恢复形状与状态 | [AgentSTAR](https://arxiv.org/abs/2609.24487) | 共享形状程序及逐帧刚体/关节状态 | 形状、姿态和时序跟踪误差 |
| 持久程序状态加生成渲染 | [Code World Model](https://arxiv.org/abs/2608.25927)、[CoDeR](https://arxiv.org/abs/2609.26458) | 可执行世界/白盒与扩散渲染器 | 编辑可持续、视图与状态一致 |
| 部件程序与几何后端 | [Part-X-MLLM](https://arxiv.org/abs/2511.13647) | 部件框、引用及编辑命令 | 可寻址理解、局部编辑和结构执行 |
| 物理/几何资产接入模拟器 | [ϕ-RIE](https://arxiv.org/abs/2609.26795)、[TourPhysics](https://arxiv.org/abs/2609.04911) | 高斯/网格、碰撞体及模拟器状态 | 渲染与物理状态同步 |
| 编排外部机器人技能 | [VoLo](https://arxiv.org/abs/2606.07723)、[RoboDawn](https://arxiv.org/abs/2609.22966)、[AR-WAM](https://arxiv.org/abs/2609.23578) | 任务历史、工具、运动控制器 | 真实闭环任务完成与失败恢复 |

最后一行是相关系统边界，不应仅因使用 Agent 就与代码世界生成混为一个排行榜。Part-X-MLLM 的 executable 指编辑程序能被后端执行，也不是已经学会随动作演化的物理规律。

## 构造路线：多 Agent 的价值应来自可检查分工

![SimWorlds 的分阶段构造和审核](../images/2607.01766-main.webp)

图1：SimWorlds 原文方法图。规划、编码和审核围绕持续场景工作，工具接口提供执行与渲染反馈。[来源](https://arxiv.org/html/2607.01766#S3)。

SimWorlds 将场景要求分解为对象、布局、材质、运动和渲染阶段，用协议把计划实体映射到引擎对象。确定性验证器检查动画曲线、模拟烘焙及对象变化，VLM 检查语义与外观。这里真正重要的是**视觉证据与程序证据互补**，而非 Agent 数量本身。

其50场景评估中，机制通过率0.87对0.67、VLM评分0.82对0.78，说明两种检查会看到不同缺陷。但协议指标依赖系统暴露可检查中间产物，跨系统比较要留意接口差异。一个只有最终视频的系统无法通过同样的引擎检查，并不自动证明它的视频更差。

Part-X-MLLM 把类似思想放到部件层：语言模型生成可引用的部件计划，OmniPart/VoxHammer等后端处理具体几何。它提高了可编辑性和诊断性，后端质量、部件框精度及跨步骤身份保持仍是独立瓶颈。

## 发现路线：拟合一个解释，和发现真实机制有距离

Code as Worlds 根据文字或视频提出世界程序，执行后比较实例、深度、轨迹和渲染，再迭代修订。可查询的模拟状态进一步生成数值问答监督。它最直接的贡献是把“观测解释”连接到“可计算的物理量标签”，而不是证明所有隐藏参数都可由单目视频唯一恢复。

AgentSTAR 共享一份对象形状代码，逐帧优化位姿及关节参数。相同二维轮廓可能来自不同三维形状或翻转姿态，因此只优化IoU会退化；其完整harness的EPE为5.59，去时序项6.15、去harness11.26，仅IoU优化可到151.46。结果支持执行管理、状态约束和多种证据的重要性，而非“VLM看图即可精确恢复3D”。每视频最高10小时预算也说明当前方案偏离线资产恢复。

**综合判断：**要检验机制是否被恢复，应在拟合完成后冻结程序，换初态、视角或动作验证。继续针对同一视频调参，只能增强解释拟合；对未见干预仍准确，才提供更强的机制证据。

## 状态与渲染解耦：一致性获得了明确载体，也产生新接口误差

![Code World Model 的代码状态与视频生成接口](../images/2608.25927-main.webp)

图2：Code World Model 原文框图。代码和执行引擎维护状态，视频生成器通过代理观察读取状态。[来源](https://arxiv.org/html/2608.25927#S3)。

Code World Model 让引擎生成深度、语义/实例等视觉代理；视频模型把低保真观察变成高质量画面。CoDeR 进一步划分 Creator、Executor、Artist 和 Traveler，使用白盒几何与人物动作作为可持续修改的世界基础。明确的状态能支持对象持久存在、编辑和重访，但从状态到视觉代理、再到生成图像的两次映射仍可能丢失细节。

例如代码正确记录了接触，而渲染器仍生成手指穿透；或者生成画面看起来门已打开，程序状态却仍为关闭。仅用视觉质量或仅用程序执行检查都看不到完整问题。理想评测要同时检查状态、代理和最终视频，并验证用户看到的结果与后续交互实际采用的状态一致。

ϕ-RIE 强调另一个实际难点：可移动对象与移除对象后的背景必须联合构建，否则移动资产会暴露残留高斯和空洞。TourPhysics 则先由模拟器确定轨迹，再生成观察；其结果依赖声明式物理配置，不能与只接收单图的系统看作相同输入权限。

## 四层证据，分别回答四个问题

| 层次 | 推荐测量 | 容易误读的展示 |
| --- | --- | --- |
| 程序有效性 | 可执行率、状态约束、错误修复次数 | 程序能运行就被称为“物理正确” |
| 观测一致性 | 遮挡处理后的几何、轮廓、轨迹和相机误差 | 渲染相似就被称为“真实机制恢复” |
| 干预一致性 | 固定世界下换动作/初态、保持未改变量 | 每次修改后重新优化，再宣称泛化 |
| 系统可用性 | 总构建时间、调用成本、交互延迟、失败恢复 | 输出24FPS视频就被称为24FPS实时生成 |

Code as Worlds 的QuantiPhy MRA、CoDeR的WorldScore、SimWorlds的协议通过率和AgentSTAR的跟踪误差不能互相排名。Code World Model 目前偏案例证据；CoDeR在约5000帧后仍可能退化，细手部和接触也会出错。这些限制对应不同接口，应明确记录而不是归为一个笼统的“长时一致性不足”。

## 系统设计的可复用结论

**综合判断：**代码适合承载离散对象身份、可查询参数、可审计逻辑和可重复执行过程；神经生成适合补足感知及外观先验。二者结合时，应该定义状态写入权限、执行失败语义、渲染不一致的处理方式，以及用户编辑后哪些状态必须保持。最有价值的验证是跨层一致性，而不是再增加一个只凭画面打分的审核 Agent。

阅读建议是 SimWorlds→Code as Worlds→AgentSTAR，先理解构造、发现与优化的区别，再读 Code World Model/CoDeR 的显式状态加渲染范式，最后用ϕ-RIE检查资产可交互性的工程缺口。VoLo/RoboDawn作为机器人编排对照，帮助识别“世界模型能力”和“工具系统能力”的边界。

## 参考文献与馆藏入口

以下按正文首次出现顺序列出；原始论文、详细卡片与本报告中的跨论文判断分别保留。

1. [SimWorlds: A Multi-Agent System for Dynamic 3D Scene Creation](https://arxiv.org/abs/2607.01766) · [馆藏卡片](../../index.html#paper=arxiv-2607-01766)
2. [Code as Worlds: Agentic Discovery of Executable World Representations for Physical Reasoning](https://arxiv.org/abs/2608.27549) · [馆藏卡片](../../index.html#paper=arxiv-2608-27549)
3. [AgentSTAR: Agentic Shape Tracking and Reconstruction from Monocular Videos](https://arxiv.org/abs/2609.24487) · [馆藏卡片](../../index.html#paper=arxiv-2609-24487)
4. [Code World Model: Coding Agent as World Brain](https://arxiv.org/abs/2608.25927) · [馆藏卡片](../../index.html#paper=arxiv-2608-25927)
5. [Code Plans, Diffusion Renders: Open-Ended Generative World Modeling](https://arxiv.org/abs/2609.26458) · [馆藏卡片](../../index.html#paper=arxiv-2609-26458)
6. [Part-X-MLLM: Part-aware 3D Multimodal Large Language Model](https://arxiv.org/abs/2511.13647) · [馆藏卡片](../../index.html#paper=arxiv-2511-13647)
7. [ϕ-RIE: From Photorealistic Reconstruction to Interactive Environments](https://arxiv.org/abs/2609.26795) · [馆藏卡片](../../index.html#paper=arxiv-2609-26795)
8. [TourPhysics: Bringing Physics to World Models for Exploration and Manipulation from a Single Image](https://arxiv.org/abs/2609.04911) · [馆藏卡片](../../index.html#paper=arxiv-2609-04911)
9. [VoLo: A Physical Orchestrator for Open-Vocabulary Long-Horizon Manipulation](https://arxiv.org/abs/2606.07723) · [馆藏卡片](../../index.html#paper=arxiv-2606-07723)
10. [Transferring the Intelligence of VLMs to Robotic Control](https://arxiv.org/abs/2609.22966) · [馆藏卡片](../../index.html#paper=arxiv-2609-22966)
11. [AR-WAM: A Visual-Conditioned Agent-Ready World Action Model for Robotic Manipulation](https://arxiv.org/abs/2609.23578) · [馆藏卡片](../../index.html#paper=arxiv-2609-23578)
