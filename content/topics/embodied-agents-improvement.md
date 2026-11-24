# 具身 Agent、测试时 Harness 与递归自改进（RSI）

**更新日期**：2026-11-23

**报告标签**：Agent与可执行世界, 机器人学习, World Action Model, 具身上下文学习, 数据与评测

> 机器人系统里的 Agent、Harness、WAM 和 RSI 经常被混为一谈，导致很多人误以为“Agentic 机器人就是改改提示词加个重试循环”。理解这一路线的正确起点，是先厘清 **Agent / Harness / RSI 三层工程职责**，再沿着部署时的真实执行路径追问：**谁产生动作、什么证据决定接受动作、反馈又写回哪里？**

[toc]

## 一、先划清概念：Agent、Harness 与 RSI 各自管什么

三者不是互斥门派，而是作用于不同时间尺度和接口层的正交机制：

| 层级 | 作用尺度 | 核心改动对象 | 代表工作 | 典型误区 |
| --- | --- | --- | --- | --- |
| **Embodied Agent** | 单局在线决策 | 任务分解、工具/子策略调用、失败观察与单局重试 | [AMP1](https://arxiv.org/abs/2611.09892)、[LAW](https://arxiv.org/abs/2610.23334)、[SPARK](https://arxiv.org/abs/2606.30613)、[AR-WAM](https://arxiv.org/abs/2609.23578) | 误以为只是“写 Prompt 让 VLM 聊天”，忽视了接口与验证设计 |
| **Test-Time Harness（支架）** | 单步/单局接口 | **不改策略权重**，重构外围观测、空间渲染、动作语法与记忆接口 | [SpatialHarness](https://arxiv.org/abs/2610.12457)、[Geometric Abstraction](https://arxiv.org/abs/2611.05058)、[GPT Policy](https://arxiv.org/abs/2609.19138) | 把外围系统（CAD/仿真/高档推理）的收益全归功于底层策略 |
| **Physical RSI（自改进）** | 跨局持续演进 | 带门禁的经验/代码/技能库沉淀，乃至改进“改进过程本身” | [ASPIRE](https://arxiv.org/abs/2607.00272)、[EmbodiedEvo](https://arxiv.org/abs/2610.18867)、[Physical RSI](https://arxiv.org/abs/2610.29677) | 把“单局重试”或“固定搜索扩技能库”夸大为递归自改进 |

## 二、第一条分界：模型直接出动作，还是出可执行控制程序？

在 [AW-0](https://arxiv.org/html/2610.30136v1#S2.SS3) 默认模式中，代码、视频与动作共同生成，机器人执行动作专家输出的动作块；代码在推理中充当中间条件，却不被执行器直接运行。在 [AMP1](https://arxiv.org/html/2611.09892v1#S4) 中，通用模型生成的 Python 会实际调用几何计算、轨迹规划与控制接口。二者的本质差别在于**代码是网络内部的表征变量，还是握有外部执行权的控制程序**。

[LAW](https://arxiv.org/html/2610.23334v2#S3) 与 [AR-WAM](https://arxiv.org/abs/2609.23578) 则展示了清晰的分层契约：LAW 用高层模型管子任务、WAM 产候选动作、学习式 Value 评分融合；AR-WAM 指出既然上层 Agent 已擅长语言推理，底层 WAM 不必再吃自然语言，直接以目标框 + 可学习操作 Token 作为干净的 Agent-Ready 接口。[SpatialHarness](https://arxiv.org/html/2610.12457v1#S3) 则完全不动冻结策略（GPT-6 Astra），只通过在线同步的数字孪生与互补虚拟视角重构空间观测接口，就在四项真机精细操作上把平均成功率从 18.33% 拉到 **83.33%（+65 pp）**。

| 工作与配置 | 部署时的主要动作路径 | 决策可改动的对象 |
| --- | --- | --- |
| AMP1 | 观测 → 通用模型 → 可执行程序与工具 → 轨迹 | 测量方法、程序逻辑与动作参数 |
| LAW | 子任务 → WAM 动作候选 → Value 评分融合 → 动作块 | 子任务进度、候选选择与动作块 |
| AW-0 默认 | 观测 → 代码／视频／动作联合生成 → 动作专家输出 | 联合生成中的程序条件与动作 |
| AR-WAM | 上层 Agent 目标框与操作 Token → 底层 WAM → 动作块 | 视觉条件接口与底层执行策略解耦 |
| SpatialHarness | 观测 → 三模态同步场景与辅助虚拟视角 → 冻结模型 → 动作 | 策略所见的当前 3D 空间证据 |

## 三、第二条分界：世界信息怎样参与动作选择？

“具有世界模型”至少包含三种不等价的计算机制：**训练期预测监督、联合生成内读取预测、给定候选动作显式预测后果并优化。**

| 世界信息的用途 | 部署期到底做了什么 | 代表工作 |
| --- | --- | --- |
| **训练期预测知识** | 改善策略或价值表征，部署时不生成未来场景 | LAW（Fast-WAM 路径） |
| **联合生成内读取未来** | 未来几何/视频与动作同步去噪，动作专家直接读出关键交互区 | AW-0、[Gnomon4D](https://arxiv.org/html/2611.02474v2#S3) |
| **可单独查询的前向动力学** | 输入指定候选动作，预测 3D 后果并由外部成本函数选优 | [PointWorld](https://arxiv.org/html/2601.03782v1) |

据此也就能看清 [GroundingPI](https://arxiv.org/html/2609.39601v2#S4) 和 [SpatialHarness](https://arxiv.org/html/2610.12457v1#S3) 的真实定位：前者改善“当前目标在哪”，后者（含抓放过渡的检查点假设重放）服务于“当前场景是什么状态”——**估计现在与预测行动后果是两个问题**，准确的状态估计为规划铺路，但本身不是前向动力学规划。

## 四、第三条分界：反馈改变当前执行，还是沉淀为跨局改进？

观察到失败并重试，改变的只是当前回合；只有把验证通过的程序、修复经验或参数持久留存下来帮助后续任务，才进入跨回合改进：

- **从单局纠偏到跨局经验沉淀**：AMP1+ 增加跨回合记忆；[ASPIRE](https://arxiv.org/html/2607.00272v2#S2) 将执行证据提炼为经验证的修复知识与可复用技能；[EmbodiedEvo](https://arxiv.org/html/2610.18867v2#S3) 将探索经验沉淀为结构化 Skills/Lessons 并与冻结执行分离。
- **严谨界定 RSI**：[Physical RSI](https://arxiv.org/html/2610.29677v1#S2) 强调必须区分**任务能力改善**（技能库变大）、**改进过程变好**（历史经验让下次修复/搜索更准），以及更强的**递归自改进**（改进者生成更好的自身后继）。单靠提高任务成功率不能自动宣称实现了 RSI。

## 五、结合 4D 底座的新切口：从“2D 盲查 + 手工 CAD”走向 Verify in 4D

把近期工作放在同一条演进轴上看，当前 Agent/Harness/RSI 路线暴露出两个互补的缺口：

1. **纯 2D Agent 精细操作盲、Token 贵**：在 2D 图像上高频调用 VLM 检查执行状态既难辨毫米级孔—柱偏移，又代价高昂；
2. **显式 3D Harness 太依赖先验**：SpatialHarness 证明了把接触区 3D 关系暴露出来收益极大（+65 pp），却重度依赖**预建刚体 CAD、标定外参与 RGB-D**，难以推广到开放世界未见物体与非刚体。

随着 **[π⁴](https://arxiv.org/abs/2611.23144)**（0.5B 参数、免标定单次前向输出度量 4D 几何与 3D 轨迹）和 **[ARROW](https://arxiv.org/abs/2610.01314)**（无序多视角 4D 查询）的成熟，中间空出的高价值切口已非常明朗：**Verify in 4D**——让高层 Agent 用可检查的 4D 子目标规划，4D WAM（如 Gnomon4D / PointWorld）在执行前“想象”候选动作的 4D 结果，执行后由 π⁴ 免标定地“测量”真实 4D 结果；**预测与实测在同一度量空间直接相减得到的稠密残差**，既能低成本驱动单局卡阻诊断与修复，又能为跨回合门禁进化提供免费、可定位的 4D 监督信号。

## 六、阅读入口

| 工作 | 在本专题中的角色 | 入口 |
| --- | --- | --- |
| AMP1 | 通用模型在线程序控制与跨回合记忆 | [原文](https://arxiv.org/abs/2611.09892) · [卡片](../../index.html#paper=arxiv-2611-09892) |
| SpatialHarness | 测试时在线同步数字孪生与辅助虚拟视角支架 | [原文](https://arxiv.org/abs/2610.12457) · [卡片](../../index.html#paper=arxiv-2610-12457) |
| LAW | 语义进展协调规划、WAM 候选与 Value 信用分配 | [原文](https://arxiv.org/abs/2610.23334) · [卡片](../../index.html#paper=arxiv-2610-23334) |
| AW-0 | 程序结构进入代码/视频/动作联合策略训练 | [原文](https://arxiv.org/abs/2610.30136) · [卡片](../../index.html#paper=arxiv-2610-30136) |
| AR-WAM | 视觉条件（目标框+操作 Token）的 Agent-Ready WAM 接口 | [原文](https://arxiv.org/abs/2609.23578) · [卡片](../../index.html#paper=arxiv-2609-23578) |
| ASPIRE | 验证修复并积累可复用技能库 | [原文](https://arxiv.org/abs/2607.00272) · [卡片](../../index.html#paper=arxiv-2607-00272) |
| EmbodiedEvo | 隔离经验获取与冻结结构化经验的复用 | [原文](https://arxiv.org/abs/2610.18867) · [卡片](../../index.html#paper=arxiv-2610-18867) |
| Geometric Abstraction | 程序结构与实时几何重绑定（不必每步看图） | [原文](https://arxiv.org/abs/2611.05058) · [卡片](../../index.html#paper=arxiv-2611-05058) |
| SPARK | 局部恢复与自主失败检测的边界 | [原文](https://arxiv.org/abs/2606.30613) · [卡片](../../index.html#paper=arxiv-2606-30613) |
| Physical RSI | 严格区分能力改进、过程改进与递归自改进证据 | [原文](https://arxiv.org/abs/2610.29677) · [卡片](../../index.html#paper=arxiv-2610-29677) |
| π⁴ / ARROW | 免标定 4D 感知前端，补齐显式 3D Harness 的 CAD/标定硬伤 | [π⁴](../../index.html#paper=arxiv-2611-23144) · [ARROW](../../index.html#paper=arxiv-2610-01314) |
| Gnomon4D / PointWorld | 4D 几何联合预测与动作条件前向轨迹规划参照 | [Gnomon4D](../../index.html#paper=arxiv-2611-02474) · [PointWorld](../../index.html#paper=arxiv-2601-03782) |

延伸：[GPT Policy](https://arxiv.org/abs/2609.19138) 讨论示范与执行历史上下文；[S-Agent 2.0](https://arxiv.org/abs/2610.28354) 讨论空间工具与单回合记忆（主测问答）；[GroundingPI](https://arxiv.org/abs/2609.39601) 见[物理增强专题](../../index.html#report=topic-physical-knowledge-to-control)；更广的程序化仿真世界见[代码与Agent世界模型](../../index.html#report=topic-code-agentic-world)；产业参照 TypeSafe Jev 保留在[独立条目](../../index.html#paper=paper-4d0d39571e)。
