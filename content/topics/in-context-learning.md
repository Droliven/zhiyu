# 具身上下文学习：示范、记忆、检索与测试时适应

**更新日期**：2026-09-24

**报告标签**：具身上下文学习, 长时记忆, 适应与泛化

> 用部署时到底改变了什么来分类：外部示范、回合记忆、检索结果、快速权重和持久参数，分别评估新任务学习与长任务执行。

本报告以现有馆藏为检索范围。正文区分方法事实、实验支持与综合判断；未完成全文核验的条目只作延伸线索，不据此建立定量排名。不同任务、输入权限、数据量和执行预算的成绩不直接横排。

[toc]

## 先分清两种问题：学一个新任务，还是记住正在做的任务

机器人忘记已放过几个零件，与机器人从未学过如何装配，是不同问题。前者需要保留回合状态、对象身份、次数和阶段；后者需要从示范中确定任务语义及可执行步骤。把所有带历史输入的方法统称为 in-context learning，会掩盖两种机制及其评价协议。

这里将**上下文条件适配**定义为外部示范或经验改变当前行为，而把**回合记忆**定义为保持当前任务所需的过去信息。二者可以共存，但应分别通过未见任务和长时部分可观测任务验证。

## 机制分类：部署时更新的对象

| 路线 | 改变什么 | 代表工作 | 核心审查点 |
| --- | --- | --- | --- |
| 示范条件策略 | 输入中的视频或观测—动作示例 | [HOST](https://arxiv.org/abs/2607.20033)、[ContextFlow](https://arxiv.org/abs/2609.06852)、[Zero-WAM](https://arxiv.org/abs/2608.26103) | 是否新任务；是否真正使用示范；示范与执行进度如何对齐 |
| 检索增强策略 | 从外部演示库取出的局部上下文 | [ICI-VLA](https://arxiv.org/abs/2609.07581)、[RA-VLA](https://arxiv.org/abs/2608.25585) | 检索库权限、检索成本、动作标签和目标任务示范预算 |
| 回合记忆与规划 | 历史 token、摘要、子目标和进度 | [PonderPounce](https://arxiv.org/abs/2608.24115)、[2AM](https://arxiv.org/abs/2609.11308)、[Memory as Plans](https://arxiv.org/abs/2609.11561) | 对象身份、重复次数、停止条件是否正确 |
| 快速权重记忆 | 随历史递推的 fast weights | [RoboTTT](https://arxiv.org/abs/2607.15275) | 哪些参数更新，是否每回合重置，梯度成本与长期污染 |
| 显式少步微调 | 持久策略参数 | [GEN-1.5 的 few-step 设置](https://generalistai.com/blog/gen-1.5) | 不能与其零梯度 physical prompt 成绩混用 |
| 冻结通用 VLM 编排 | 提示、工具结果与外部历史 | [GPT-Policy](https://arxiv.org/abs/2609.19138)、[RoboDawn](https://arxiv.org/abs/2609.22966) | 运动学工具、标定、模型调用和重试预算 |

[S1](https://skild.ai/blogs/s1) 的官方报告提供大规模示范条件训练及长程案例，但公开架构、试验数和原始统计并不完整。应把它作为规模化路线的证据，和机制、协议较清晰的论文互补阅读，而非直接混合排行榜。

## 真正的瓶颈是对齐，不是把更长视频塞进上下文

HOST 先学习人类与机器人视频的单调进度，再滑动示范窗口，依次预测进度、机器人未来观察和动作。这个中间进度把“现在示范做到哪一步”和“机器人接下来应做什么”接起来。ContextFlow 则压缩多视角示范为固定 token，经上下文专家条件化动作流；它展示的是单示范条件策略，不等于机器人已能长期积累自身经验。

检索方法面对另一种对齐：图像相似不代表行为阶段相同。ICI-VLA 用 DTW 对齐训练检索表征，并通过目标动作掩蔽降低直接复制；RA-VLA 还约束策略对相关与随机上下文产生不同响应。ReWeight 虽然也检索人类示范，但其结果进入后训练样本权重，是离线数据利用，不是冻结策略的部署期 ICL。[ReWeight 原文](https://arxiv.org/abs/2609.13851)

真正有说服力的诊断应包括：错误示范、同物不同任务、同任务不同外观、交换步骤及删除关键片段。模型在正确示范下成功只是第一步；错误示范能以预期方式改变行为，才说明条件通道被实际利用。

![GPT-Policy 的上下文与工具执行闭环](../images/2609.19138-main.webp)

图1：GPT-Policy 原文图。任务参考与在线执行历史分开管理，固定 VLM 选择结构化工具，控制器回传结果；工具能力是系统能力的一部分。[来源](https://arxiv.org/html/2609.19138#S3)。

## 长上下文如何压缩，决定了哪些记忆会丢失

PonderPounce 让慢速上下文引擎累积历史，快速动作模型读取最新 cognition 及其陈旧程度；RoboTTT 则以更新后的 fast weights 作为递归状态，把历史压入权重空间。后者虽然服务于上下文学习，但不是“部署时没有任何梯度更新”。其8K上下文相对1K的62%提升是作者报告的相对增益，不能写成增加62个百分点。

2AM 将历史压缩为带目标点的抓取、放置和移动命令，动作模型不读取整段历史。这个方案的优势是接口清楚，风险是摘要会丢失精确次数和停止条件。Memory as Plans 则把记忆连接到分段视觉计划和进度校正；其评价应同时检查计划切换错误和完整任务结果。

[Zeva-Ego](https://arxiv.org/abs/2609.24411) 的 ACE 人类视频中间训练与 ICCL 部署适配也应分开：前者学习动作相关表征，后者把动作—效果历史直接送给动作专家。四次尝试58%→89%包含新增环境反馈，不能与一次尝试的零样本策略等预算比较。

## 代表证据：把试验单位与收益写在一起

| 工作与设置 | 报告结果 | 更有解释力的边界 |
| --- | --- | --- |
| HOST，50个未见任务，每任务20次 | 平均62% | 单一双臂平台；获取新技能的时间不等于每步推理延迟 |
| ContextFlow，LIBERO四个未见任务 | 73.5%，ContextAR 53.5% | 留出任务范围较小；不能扩展为任意本体泛化 |
| ICI-VLA，四个实机任务共1000次 | 83.2%，95% Wilson区间80.8–85.4 | 去DTW后RoboTwin60.4%→31.4%，比跨模型排行更能定位贡献 |
| RA-VLA，整套LIBERO留出、每任务三示范 | 38.45%，RICL-R20.85% | 与普通LIBERO已见任务的高分不可直接比较 |
| 2AM，LIBERO-Mem | 宽松63.00%，严格11.83% | 对齐基线严格12.25%；完成更多不代表停止更准确 |
| PonderPounce，RoboMME | 60.83%；只在阶段切换更新则1.83% | 当前模型强依赖持续刷新，不能视为低频规划一次即可执行 |

[MemCorr-DP](https://arxiv.org/abs/2609.06615) 提供有用的条件利用测试：错误参考使成功数降到5/300，正确参考为292/300。但主要场景是已知 Door 任务，说明参考确实改变策略，不足以证明学习全新任务。这类控制比“加一条示范提高若干分”更有诊断价值。

## 一套可比较的评估协议

先明确泛化轴：未见物体、未见布局、未见技能、未见组合、未见本体；不要用其中一项代替全部。其次固定每任务示范数、人工反馈次数和允许重试次数；把额外环境接触与离线预训练预算都记录下来。最后同时报告严格成功率、阶段完成度、首次成功尝试数和端到端耗时。

记忆任务还要测错误记忆恢复：重复次数被误记、目标被换位、旧参考过期、动作失败但历史写成成功。只测更长输入会混淆容量与可用信息；应加入相同 token 预算的随机历史、近期历史与相关历史对照。

## 综合判断与阅读路径

**综合判断：**示范条件策略的关键在任务进度与动作对齐；长期执行的关键在可更新的状态记忆和停止判断；快速权重与少步微调则是不同的适配机制。把它们按“部署时更新对象”区分，比按标题中是否出现 in-context 更稳定。

先读 HOST/ContextFlow 理解示范接口，再用 ICI-VLA/RA-VLA 理解检索和反复制；然后对照 RoboTTT、PonderPounce、2AM 的三种记忆载体。最后阅读 S1/GEN-1.5 的规模化报告，并保留其未公开的统计与系统细节，不用案例视频替代可靠性结论。

## 参考文献与馆藏入口

以下按正文首次出现顺序列出；原始论文、详细卡片与本报告中的跨论文判断分别保留。

1. [Robots Acquire Manipulation Skills in Seconds from a Single Human Video（HOST）](https://arxiv.org/abs/2607.20033) · [馆藏卡片](../../index.html#paper=arxiv-2607-20033)
2. [ContextFlow: In-Context Flow Matching for Robot Manipulation](https://arxiv.org/abs/2609.06852) · [馆藏卡片](../../index.html#paper=arxiv-2609-06852)
3. [Zero-WAM: In-Context World-Action Modeling from Human Videos for Open-Ended Task Generalization](https://arxiv.org/abs/2608.26103) · [馆藏卡片](../../index.html#paper=arxiv-2608-26103)
4. [ICI-VLA: In-Context Imitation with Spatiotemporally Aligned Demonstrations for Vision-Language-Action Models](https://arxiv.org/abs/2609.07581) · [馆藏卡片](../../index.html#paper=arxiv-2609-07581)
5. [RA-VLA: Retrieval-Augmented VLA for Test-Time Adaptation](https://arxiv.org/abs/2608.25585) · [馆藏卡片](../../index.html#paper=arxiv-2608-25585)
6. [PonderPounce: A Pretrained MLLM as an Episode Context Engine for Robot Control](https://arxiv.org/abs/2608.24115) · [馆藏卡片](../../index.html#paper=arxiv-2608-24115)
7. [2AM: Grounding Agent-Side Memory as Guidance for Steerable Action Models in Long-Horizon Manipulation](https://arxiv.org/abs/2609.11308) · [馆藏卡片](../../index.html#paper=arxiv-2609-11308)
8. [Memory as Plans: World-Action Modeling with Memory-Grounded Planning](https://arxiv.org/abs/2609.11561) · [馆藏卡片](../../index.html#paper=arxiv-2609-11561)
9. [RoboTTT: Context Scaling for Robot Policies](https://arxiv.org/abs/2607.15275) · [馆藏卡片](../../index.html#paper=arxiv-2607-15275)
10. [GEN-1.5: Embodied Foundation Models are One-Shot Learners](https://generalistai.com/blog/gen-1.5) · [馆藏卡片](../../index.html#paper=paper-5299527392)
11. [In-Context Robot Learning with VLM Agents](https://arxiv.org/abs/2609.19138) · [馆藏卡片](../../index.html#paper=arxiv-2609-19138)
12. [Transferring the Intelligence of VLMs to Robotic Control](https://arxiv.org/abs/2609.22966) · [馆藏卡片](../../index.html#paper=arxiv-2609-22966)
13. [Introducing S1: In-Context Learning for Robotics](https://skild.ai/blogs/s1) · [馆藏卡片](../../index.html#paper=paper-d14a137e07)
14. [ReWeight: Leveraging Human Data for VLA Post-Training via Demonstration Retrieval and Sample Weighting](https://arxiv.org/abs/2609.13851) · [馆藏卡片](../../index.html#paper=arxiv-2609-13851)
15. [Zeva-Ego: Egocentric Mid-Training with In-Context Causal Learning for Robot Manipulation](https://arxiv.org/abs/2609.24411) · [馆藏卡片](../../index.html#paper=arxiv-2609-24411)
16. [MemCorr-DP: Counterfactual Correspondence Conditioning for a Diffusion Policy Guided by a Reference](https://arxiv.org/abs/2609.06615) · [馆藏卡片](../../index.html#paper=arxiv-2609-06615)
