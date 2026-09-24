# 生成式世界模型：预测表征、长程记忆与实时执行

**更新日期**：2026-09-24

**报告标签**：世界模型, 视频生成, 流式与自回归, 自监督与预测表征

> 把预测什么、如何维持状态、未来如何用于决策和怎样实时运行拆开讨论，连接视频表征、WAM预训练、流式蒸馏与几何记忆。

本报告以现有馆藏为检索范围。正文区分方法事实、实验支持与综合判断；未完成全文核验的条目只作延伸线索，不据此建立定量排名。不同任务、输入权限、数据量和执行预算的成绩不直接横排。

[toc]

本篇保留生成式世界模型的总体框架。表征与预测机制另见[JEPA与隐式状态表征](../../index.html#report=topic-jepa-latent-state)，蒸馏、缓存和实时交互另见[流式与自回归交互视频生成](../../index.html#report=report-c7ced2c92d)，手物生成与物理资产见[手物交互重建与生成](../../index.html#report=topic-contact-hoi)。三个方向均在报告厅保留独立入口。

## 统一框架：生成未来不等于用好未来

一个系统可以预测逼真视频，却不会选动作；也可以只预测紧凑latent，支持有效控制。判断世界模型应分别回答四个问题：**预测目标是什么、状态存在哪里、决策怎样消费预测、完整闭环需要多少时间**。这些轴相互影响，但不能以一个视频分数取代全部。

本专题讨论通用的表征、生成与运行机制；代码持有的显式世界状态见“代码与Agent”专题，动作接口见“Visual Action”，几何WAM体系仍保留精品报告的独立地位。

## 从像素到任务表征：压缩什么，决定保留什么

| 预测目标 | 代表路线 | 主要收益 | 关键检验 |
| --- | --- | --- | --- |
| RGB视频latent | 视频扩散、联合WAM | 复用视频预训练，可视化未来 | 是否把容量花在无关纹理；动作响应是否准确 |
| 语义/预测特征 | [VLA-JEPA](https://arxiv.org/abs/2602.10098)、[SLIM](https://arxiv.org/abs/2608.09771)、[SG-WAM](https://arxiv.org/abs/2608.01397) | 减少解码开销，围绕控制学习 | 目标特征是否保留位置、接触和任务差异 |
| 可解码表征空间 | [VideoRAE](https://arxiv.org/abs/2607.14088)、[LeVJEPA](https://arxiv.org/abs/2608.27395) | 连接强视频编码与生成训练 | 编码器好不等于latent易生成；表征不变性可能抹去状态变化 |
| 多种结构化未来 | [DreamWAM](https://arxiv.org/abs/2608.04996)、[ModAR](https://arxiv.org/abs/2609.17524)、[MachEmbodied-U0](https://arxiv.org/abs/2609.25627) | 深度、轨迹、语义与动作互补 | 哪种监督有效；未来真值是否泄漏给动作 |
| 几何原生latent | [GAE](https://arxiv.org/abs/2609.24981) | 外观与几何在codec形成时对齐 | 重建、生成和几何一致性须分开评测 |

LeVJEPA使用全局/局部视图一致性与SIGReg学习编码器，本身没有动作条件动力学；VideoRAE学习可重建、可生成的表征空间。把这两类工作叫世界模型“组件”比直接宣称它们已能模拟交互更准确。

![GAE 的几何原生codec与流生成](../images/2609.24981-main.webp)

图1：GAE原文方法图。冻结几何骨干的多层特征被压缩为可同时解码RGB和几何的latent，再用于条件flow matching。[来源](https://arxiv.org/html/2609.24981#S3)。

GAE还用token级和关系级对齐组织latent，说明“重建充分”与“便于生成”并非同一要求。VideoRAE中局部—全局REPA消融也支持表示组织的重要性。不过不同codec的FVD、压缩率和通道数，只有在匹配生成骨干、分辨率和数据时才有直接比较意义。

## 未来进入策略有三种位置

第一种是**训练辅助**：未来目标塑造当前表示，部署删除预测分支。[GeoSem-WAM](https://arxiv.org/abs/2606.03188)、[4D几何先验蒸馏](https://arxiv.org/abs/2607.05468)和[GigaWorld-Policy](https://arxiv.org/abs/2607.13960)体现这种路径。第二种是**在线条件**：动作读取正在生成或已生成的未来。[Efficient-WAM](https://arxiv.org/abs/2606.10040)以低成本未来降低代价。第三种是**候选评价**：对不同动作预测不同未来，再规划选择，例如[DUET-DINO](https://arxiv.org/abs/2609.10506)。

DreamWAM的LIBERO-Plus no-rollout设置51.36→63.44，说明收益可以来自训练期表征塑造，而不需要运行时想象。ModAR在自身设置中完整模态75%，移除tracks约61%、反转模态顺序约65%；但与大模型比较包含参数及约20倍训练FLOPs差异，因此更应重视内部消融。

DUET-DINO的双视角latent规划在真实angled-reach仅26.7%，规划步约15–17秒，显示表示更好也可能被搜索成本和域偏移限制。选择在线世界预测，必须证明其新增计算在闭环中真正值回成本。

## 从大规模预训练到有效迁移：小时数不是唯一解释

[Motus](https://arxiv.org/abs/2512.13030)、[OpenWAM](https://arxiv.org/abs/2609.07398)、[Dyna-2](https://www.dyna.co/dyna-2)和[GE-Act 2.0](https://arxiv.org/abs/2609.05588)覆盖联合视频动作、统一动作空间、人类视频扩展和分阶段对齐。它们共同说明数据接口与训练配方很重要，却不能把不同语料、机器人和评测协议下的小时数连成一条通用扩展律。

Dyna-2的嵌套数据子集比跨论文规模排行更接近受控扩展实验；OpenWAM的统一动作和开放checkpoint有利于研究配方，但仍需固定baseline训练预算。GE-Act的KASO消融在相同预训练组件和300小时连接数据下比较，比单报最终榜单更能定位“预测未来是否兼容动作”的作用。是否依赖目标本体数据、伪动作质量和人工过滤，都应随数据规模一起记录。

## 流式生成：训练分布、缓存和蒸馏必须共同设计

[DMD](https://arxiv.org/abs/2311.18828)和[DMD2](https://arxiv.org/abs/2405.14867)为少步分布匹配提供基础，但最初是图像生成方法，其FID提升不能直接外推到交互视频。[Self Forcing](https://arxiv.org/abs/2506.08009)让训练接触模型自己产生的历史，缓解教师强制与部署rollout的分布差异；[Causal Forcing](https://arxiv.org/abs/2602.02214)和[Causal Forcing++](https://arxiv.org/abs/2605.15141)进一步处理因果学生与初始化/蒸馏监督的匹配。

缓存解决计算重复，不自动解决世界状态。[LongLive](https://arxiv.org/abs/2509.22622)的短窗、frame sink和prompt切换时KV-recache在连贯性与新指令响应之间折中；[LongLive-2.0](https://arxiv.org/abs/2605.18739)再用低精度、并行和异步VAE提速。其5B模型BF16为24.8 FPS/VBench85.06，NVFP4两步45.7 FPS/83.14：加速伴随质量变化，不能只引用最高FPS。

[minWM](https://arxiv.org/abs/2605.30263)把这些问题推进到完整交互系统。比较实时性应固定硬件、分辨率、批量、首帧延迟和交互刷新频率；动作回放频率、输出视频帧率和生成吞吐是三个不同数字。

## 长时记忆：保存过去图像与维护世界不是一回事

[ReWorld](https://arxiv.org/abs/2608.23565)、[Matrix-Game 3.5](https://arxiv.org/abs/2608.29910)和[WorldCrafter](https://arxiv.org/abs/2609.24984)采用不同历史检索与记忆接口。WorldCrafter保留最近帧，选择互补视野，再按未来相机查询固定大小记忆token，减少反复检索相似但冗余画面。[AlayaVista](https://arxiv.org/abs/2609.14462)则维护全景状态并按视角读取，状态载体更明确，但全景补全同样含生成假设。

![WorldCrafter 的隐式几何记忆读写](../images/2609.24984-main.webp)

图2：WorldCrafter原文方法图。记忆编码器写入历史潜变量及相机，目标位姿控制读取，视频模型在固定预算下使用记忆。[来源](https://arxiv.org/html/2609.24984#S3)。

WorldCrafter快速版的重访LPIPS比基础版更好，相机旋转误差却由13.536增至18.251，说明记忆、控制与画面质量存在不同方向的变化。[R2M-Bench](https://arxiv.org/abs/2608.27328)提出重访与时间间隔匹配的非重访对照，是排除普通渲染稳定性混淆的有用思路；馆藏目前对其定量证据仍有限，不把概念设计直接写成已证实的最优评测。

## 实时控制还需要新观察，而不是仅仅更快生成

[DualWAM](https://arxiv.org/abs/2609.24868)把高噪声全局规划与低噪声局部修正异步连接，强调最新腕部观察纠偏。这与单纯把离线视频生成速度提高到实时不同：接触任务要求观察进入后能及时改变动作。应同时报告观察年龄、动作段长度、执行中的可中断性及失败恢复。

**综合判断：**当前可复用的设计规律是，按任务决定预测内容，按预算决定未来的消费位置，按部分可观测性决定记忆载体。一个统一大模型可以覆盖多模式，但收益是否来自数据规模、辅助监督、在线规划或系统加速，仍需分项证据。

阅读可按VideoRAE/GAE→DreamWAM/ModAR→Motus/OpenWAM→Self/Causal Forcing→WorldCrafter/DualWAM推进，依次理解表征、目标、预训练、运行和闭环。不要把这条阅读顺序理解成论文之间严格的技术继承关系。

## 参考文献与馆藏入口

以下按正文首次出现顺序列出；原始论文、详细卡片与本报告中的跨论文判断分别保留。

1. [VLA-JEPA: Enhancing Vision-Language-Action Model with Latent World Model](https://arxiv.org/abs/2602.10098) · [馆藏卡片](../../index.html#paper=arxiv-2602-10098)
2. [SLIM-0.5B: Learning Action-Grounded Predictive Latents for Robot Manipulation](https://arxiv.org/abs/2608.09771) · [馆藏卡片](../../index.html#paper=arxiv-2608-09771)
3. [SG-WAM: Self-Guided World Modeling in Geometry-Aware Policy Space](https://arxiv.org/abs/2608.01397) · [馆藏卡片](../../index.html#paper=arxiv-2608-01397)
4. [VideoRAE: Taming Video Foundation Models for Generative Modeling via Representation Autoencoders](https://arxiv.org/abs/2607.14088) · [馆藏卡片](../../index.html#paper=arxiv-2607-14088)
5. [LeVJEPA: Efficient & Scalable Video Pretraining without the Heuristics](https://arxiv.org/abs/2608.27395) · [馆藏卡片](../../index.html#paper=arxiv-2608-27395)
6. [DreamWAM: Beyond RGB Future Prediction for World Action Models](https://arxiv.org/abs/2608.04996) · [馆藏卡片](../../index.html#paper=arxiv-2608-04996)
7. [Modality-Autoregressive World-Action Models](https://arxiv.org/abs/2609.17524) · [馆藏卡片](../../index.html#paper=arxiv-2609-17524)
8. [MachEmbodied-U0: Unified Understanding and Generation Model for Embodied Intelligence](https://arxiv.org/abs/2609.25627) · [馆藏卡片](../../index.html#paper=arxiv-2609-25627)
9. [GAE: Learning a Geometry-Native Latent Space for 3D-Consistent World Generation](https://arxiv.org/abs/2609.24981) · [馆藏卡片](../../index.html#paper=arxiv-2609-24981)
10. [GeoSem-WAM: Geometry- and Semantic-Aware World Action Models](https://arxiv.org/abs/2606.03188) · [馆藏卡片](../../index.html#paper=arxiv-2606-03188)
11. [Learning 4D Geometric Priors for Inference-Efficient World Action Models](https://arxiv.org/abs/2607.05468) · [馆藏卡片](../../index.html#paper=arxiv-2607-05468)
12. [GigaWorld-Policy-0.5: A Faster and Stronger WAM Empowered by AutoResearch](https://arxiv.org/abs/2607.13960) · [馆藏卡片](../../index.html#paper=arxiv-2607-13960)
13. [Efficient-WAM: A 1B-Parameter World-Action Model with Low-Cost Future Imagination](https://arxiv.org/abs/2606.10040) · [馆藏卡片](../../index.html#paper=arxiv-2606-10040)
14. [DUET-DINO: Simultaneous Cross-View World Modeling for Latent Planning in Robot Manipulation](https://arxiv.org/abs/2609.10506) · [馆藏卡片](../../index.html#paper=arxiv-2609-10506)
15. [Motus: A Unified Latent Action World Model](https://arxiv.org/abs/2512.13030) · [馆藏卡片](../../index.html#paper=arxiv-2512-13030)
16. [OpenWAM: An Open, Modular Exploration Towards Systematic World-Action Model Pretraining](https://arxiv.org/abs/2609.07398) · [馆藏卡片](../../index.html#paper=arxiv-2609-07398)
17. [Dyna-2: A 1-Million-Hour Scaling Law for World-Action Models](https://www.dyna.co/dyna-2) · [馆藏卡片](../../index.html#paper=paper-1d4c797b72)
18. [GE-Act 2.0: Pretraining and Scaling a World-Action Model for Robotic Manipulation](https://arxiv.org/abs/2609.05588) · [馆藏卡片](../../index.html#paper=arxiv-2609-05588)
19. [One-step Diffusion with Distribution Matching Distillation](https://arxiv.org/abs/2311.18828) · [馆藏卡片](../../index.html#paper=arxiv-2311-18828)
20. [Improved Distribution Matching Distillation for Fast Image Synthesis](https://arxiv.org/abs/2405.14867) · [馆藏卡片](../../index.html#paper=arxiv-2405-14867)
21. [Self Forcing: Bridging the Train-Test Gap in Autoregressive Video Diffusion](https://arxiv.org/abs/2506.08009) · [馆藏卡片](../../index.html#paper=arxiv-2506-08009)
22. [Causal Forcing: Autoregressive Diffusion Distillation Done Right for High-Quality Real-Time Interactive Video Generation](https://arxiv.org/abs/2602.02214) · [馆藏卡片](../../index.html#paper=arxiv-2602-02214)
23. [Causal Forcing++: Scalable Few-Step Autoregressive Diffusion Distillation for Real-Time Interactive Video Generation](https://arxiv.org/abs/2605.15141) · [馆藏卡片](../../index.html#paper=arxiv-2605-15141)
24. [LongLive: Real-time Interactive Long Video Generation](https://arxiv.org/abs/2509.22622) · [馆藏卡片](../../index.html#paper=arxiv-2509-22622)
25. [LongLive-2.0: An NVFP4 Parallel Infrastructure for Long Video Generation](https://arxiv.org/abs/2605.18739) · [馆藏卡片](../../index.html#paper=arxiv-2605-18739)
26. [minWM: A Full-Stack Open-Source Framework for Real-Time Interactive Video World Models](https://arxiv.org/abs/2605.30263) · [馆藏卡片](../../index.html#paper=arxiv-2605-30263)
27. [ReWorld: An Interactive World Model with Long-Horizon Memory](https://arxiv.org/abs/2608.23565) · [馆藏卡片](../../index.html#paper=arxiv-2608-23565)
28. [Matrix-Game 3.5: Enhancing Real-Time Streaming Interactive World Models with Patch Memory](https://arxiv.org/abs/2608.29910) · [馆藏卡片](../../index.html#paper=arxiv-2608-29910)
29. [WorldCrafter: Consistent Video World Model with Implicit 3D-aware Memory](https://arxiv.org/abs/2609.24984) · [馆藏卡片](../../index.html#paper=arxiv-2609-24984)
30. [AlayaVista: Streaming World Modeling from Panoramic States to Perspective Video](https://arxiv.org/abs/2609.14462) · [馆藏卡片](../../index.html#paper=arxiv-2609-14462)
31. [R2M-Bench: Evaluating Revisit Memory via Relative Consistency in Interactive Video World Models](https://arxiv.org/abs/2608.27328) · [馆藏卡片](../../index.html#paper=arxiv-2608-27328)
32. [DualWAM: Dual-System World Action Models for Asynchronous Global Planning and Local Refinement](https://arxiv.org/abs/2609.24868) · [馆藏卡片](../../index.html#paper=arxiv-2609-24868)
