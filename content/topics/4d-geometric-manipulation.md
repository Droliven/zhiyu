# 3D/4D 几何增强具身操作：从免标定 4D 底座、空间内化到几何世界动作模型

**更新日期**：2026-11-23

**报告标签**：3D/4D, World Action Model, VLA, 机器人学习, 动作表征

> 2D 视觉策略在视角变化、深度遮挡与精细对齐面前频频失效，但“给模型塞进深度图或点云”往往破坏预训练权重复用并受限于传感器噪声。本专题沿**免标定 4D 感知底座 → 潜空间与策略权重内化 → 动作耦合的 4D 世界动作模型**三层脉络，梳理 3D/4D 几何真正提升机器人操作的代表路线与边界。

本专题聚焦“几何如何服务操作控制”，与侧重纯视觉重建/生成的[3D/4D 生成与重建专题](../../index.html#report=topic-3d-reconstruction)形成上下游衔接；方法与数字均来自馆藏独立卡片核验的原文。

[toc]

## 一、核心脉络：3D/4D 几何进入操作策略的三条接口

同样号称“3D/4D 增强”，不同工作把几何放在了系统里完全不同的位置，决定了它对标定、深度相机和推理延迟的依赖程度：

| 层次与定位 | 核心问题 | 代表工作 | 推理期是否需深度/标定 | 一句话机制精髓 |
| --- | --- | --- | --- | --- |
| **第一层：免标定 4D 感知底座** | 如何从任意 RGB 恢复一致的 3D 几何与 4D 运动？ | [π⁴](https://arxiv.org/abs/2611.23144)、[ARROW](https://arxiv.org/abs/2610.01314) | 否（纯 RGB） | 单次前向输出动态点图与 3D 轨迹，为下游提供免标定 4D 测量前端 |
| **第二层：几何原生潜空间与表征内化** | 如何在不改推理架构的前提下把 3D 装进生成/策略底座？ | [GAE](https://arxiv.org/abs/2609.24981)、[Spatial Forcing](https://arxiv.org/abs/2510.12276)、[SLA](https://arxiv.org/abs/2611.08373)、[MECo-WAM](https://arxiv.org/abs/2607.05468) | 否（训练期对齐/压缩） | 把 3D 几何压进紧凑潜空间，或从后训练到持续预训练隐式对齐进 VLA 视觉 Token，部署零开销 |
| **第三层：几何耦合的 4D 世界动作模型** | 动作如何直接读取几何未来、物体运动或工具位姿？ | [Gnomon4D](https://arxiv.org/abs/2611.02474)、[TCP4D](https://arxiv.org/abs/2611.23143)、[AffordanceWAM](https://arxiv.org/abs/2609.22332)、[PointWorld](https://arxiv.org/abs/2601.03782) | 视路线（RGB 或需当前深度） | 在联合去噪或前向规划中直接对齐“机械臂—物体相对 4D 运动”与可执行动作 |

## 二、第一层：免标定 4D 感知底座——先把世界“看准”

机器人部署最怕复杂外参标定与昂贵深度传感器。近期前馈 4D 基础模型已经能从任意未标定 RGB 图像直接恢复动态 3D 几何与点轨迹，其中 **ARROW** 与 **π⁴** 构成了两种最具代表性的架构取舍：

- **[ARROW](https://arxiv.org/abs/2610.01314)（无序内容寻址 + 稀疏直接 3D 查询）**：把 D4RT 的固定帧号位置编码替换为 DA3 相机 Token 派生的**内容 ID Token**，让单目视频、多相机同步流与无序静态图集共享同一查询接口。非顺序跨视角混训让多视角 3D 跟踪 APD 暴涨 +28.85 pp 并反哺单目 SOTA。优点是稀疏查询极灵活；短板是直接回归参考系 3D 端点，缺少绝对度量尺度且远距离易与局部表面漂离。
- **[π⁴](https://arxiv.org/abs/2611.23144)（0.5B 循环底座 + 2D 对应解析抬升）**：用循环 Transformer 权重共享把全系统压到 ~0.5B（几何 343M），省出显存直接训练 64 视角联合上下文，推理期单次前向支持数百至上千帧不 OOM（Oxford Spires ATE 0.73 m）。更关键的是它**冻结置换等变度量几何底座，让运动分支只在 2D 预测对应，再解析采样抬升到目标帧度量表面**——从构造上消灭轨迹漂离表面。

**对具身操作的定位**：π⁴ 与 ARROW 都是**被动感知器**，不包含动作条件演化与接触物理；但 π⁴ 兼具“免标定、绝对度量尺度、长序列稳定、0.5B 轻量”，已具备充当下一代 4D WAM 感知前端与在线执行验证器的成熟条件。

## 三、第二层：潜空间与表征内化——零部署开销的 3D 赋能

如果不想在推理时外挂重型 3D 重建或点云编码器，最务实的路线是在**训练期或表征层**把 3D 几何内化进模型：

- **[GAE](https://arxiv.org/abs/2609.24981)（面向世界生成的几何原生潜空间）**：一针见血地指出原始几何特征（DA3-Giant 3,072 通道）有效秩仅约 11 维、条件数高达 $10^8\text{–}10^{16}$，根本不适合流匹配。GAE 在冻结编码器与冻结几何头之间压缩出 64/128 通道共享潜空间，并用 **C-RADIO 单点对齐 + DINOv2 成对关系损失**塑形，在固定同一 DiT 下使 RealEstate10K/DL3DV FVD 降 12.7%/23.1%、相机轨迹误差减半。它验证了“几何原生潜空间”作为生成底座的潜力（目前限于静态场景漫游）。
- **[Spatial Forcing](https://arxiv.org/abs/2510.12276) → [SLA](https://arxiv.org/abs/2611.08373)（从“下游微调补丁”到“持续预训练底座”的两代隐式 3D 对齐）**：两者来自同一团队（OpenHelix-Team），共享“训练期把 VLA 视觉 Token 隐式对齐到冻结 3D 教师、部署零新增 3D 传感器”的核心范式，但定位与机制有四点关键跃迁：

| 对比维度 | Spatial Forcing（`2510.12276`） | SLA（`2611.08373`） |
| --- | --- | --- |
| **介入阶段** | 仅**下游后训练**微调（任务特化补丁） | 基于 $\pi_{0.5}$ 的**大规模持续预训练 + 后训练两阶段** |
| **3D 教师** | **VGGT**（纯 RGB，无法利用数据自带深度/标定） | **OmniVGGT**（有深度/标定时通过 GeoAdapter 吸收，缺失时平滑回退纯 RGB；补标定 +3.2 pp） |
| **对齐层机制** | 手工挑选单一较深固定层（如 OpenVLA-OFT 第 24 层） | 全 18 层特征依赖 Sigmoid **自适应门控**动态融合（比最佳固定层 C2R 再高 +5.0 pp） |
| **跨本体数据工程** | 沿用单基准原动作与状态空间 | **25% 状态 Dropout** 破除背轨迹捷径 + 统一基座系与 **$\mathrm{SO}(3)$ 旋转向量**（消除欧拉角 $\pm 2\pi$ 跳变） |
| **代表收益与边界** | LIBERO 98.5%、训练提速 3.8×、5% 数据达 75.8%；纯零新增推理模块 | RoboTwin C2R **72.3%**（超 SF 62.6% **+9.7 pp**）、真机 8 条件 **83.8%**（超 SF 68.0% **+15.8 pp**）；RoboDojo-Real 评测额外保留历史图像 Memory |

  **机制与归因要点**：SLA 的 Table 6 消融表明，无 3D 对齐时预训练数据从 5% 扩到 100% 几乎原地踏步（C2R 43.8% → 48.2%），仅后训练对齐（SF 模式）达 57.1%，仅持续预训练对齐达 63.2%，**两阶段都对齐才一路涨到 72.3%**——证明隐式 3D 对齐前移至预训练能打开异构数据扩展天花板。同时须守住归因边界：SLA 主榜单跃升并非只靠 3D 教师，其同配置消融中 **25% 状态 Dropout** 单项即带来 +41.1 pp（逼迫策略放弃“看本体状态背轨迹”转而读取对齐后的视觉空间特征），$\mathrm{SO}(3)$ 旋转向量亦优于欧拉角 +13.7 pp。因此 **SF 验证的是“隐式 3D 对齐机制有效”，而 SLA 验证的是“将其规模化到百万级异构预训练所需的完整工程拼图”**；两者的共同边界在于仍只强化当前帧静态 3D 感知，不含动作条件未来演化。
- **[MECo-WAM](https://arxiv.org/abs/2607.05468)（推理高效的 4D 几何先验监督）**：同样主张 4D 几何不必成为推理期显式输入输出，而是作为训练期密集监督塑造动作与世界预测表征，在保持推理轻量的同时提升空间控制精度。

## 四、第三层：几何耦合的 4D 世界动作模型——让动作真正读懂“交互运动”

仅有当前帧的 3D 感知或隐式对齐，仍未回答“机械臂动起来之后，物体和接触区在未来几秒会怎么动”。第三层工作直接把 4D 几何运动耦合进动作生成或轨迹优化：

- **[Gnomon4D](https://arxiv.org/abs/2611.02474)（Where & When 交互读出）**：指出纯 RGB 未来混杂外观与运动、逐帧深度缺跨时对应；即使预测了几何，动作专家也容易只盯机械臂整体而忽视接触区。它构造共享时空位移场 **GeoDelta**，由视频、GeoDelta、动作三专家联合去噪，并用 InSAttn（空间聚焦物体—本体相对运动区）与 TransAgg（时间聚合关系转换时刻）把关键几何未来精准喂给动作专家，在十任务消融上从纯 RGB 80.0% 稳步提至 86.2%。
- **[TCP4D](https://arxiv.org/abs/2611.23143)（工具中心点 $\mathrm{SE}(3)$ 跟踪与生成统一）**：针对“表面点跟踪器抓不住悬空 TCP 且缺姿态”的痛点，在共享 4D 表征上直接回归度量 TCP $\mathrm{SE}(3)$+夹爪状态（DROID ATE 7.60 mm），再沿历史 TCP 轨迹采样局部 4D 特征做 4 步流匹配动作生成（RoboTwin C2C 69.19%，真机无需深度 78.33% 超越 DP3）；同时支持零源状态日志的跨本体视频增广。
- **[AffordanceWAM](https://arxiv.org/abs/2609.22332) 与 [PointWorld](https://arxiv.org/abs/2601.03782)（对象可供性 vs. 动作条件 3D 前向规划）**：AffordanceWAM 以对象中心时空可供性作为人类与机器人数据的共享预测目标；PointWorld 则把候选机器人轨迹直接作为输入，预测 3D 场景点云运动并由外部优化器按目标成本选动作——提供真正可检验“换一个动作会怎样”的反事实前向接口（代价是规划耗时数秒）。

## 五、横向比较与下一步研究切口

将三层工作放在一起，当前 3D/4D 几何增强具身操作尚未打通的核心缺口非常清晰：

1. **静态/被动 4D 与动作条件 4D 割裂**：π⁴ 与 GAE 擅长免标定重建与静态几何原生潜空间，但不懂动作干预；Gnomon4D 与 PointWorld 能做动作耦合几何预测，却依赖当前深度/掩码或较高规划开销。**用 π⁴ 风格的免标定 4D 原生 Token 替换手工深度/掩码，构筑跨遮挡持久的 4D 世界动作模型**，是极有价值的交汇点。
2. **几何预测尚未闭环自检**：Gnomon4D、TCP4D 等预测了未来几何或轨迹，但执行后并未拿真实测得的 4D 结果去核对“预测是否兑现”，出错后无法诊断与恢复（这正衔接[具身 Agent 与 RSI 专题](../../index.html#report=topic-embodied-agents-improvement)）。
3. **几何运动学 ≠ 接触物理**：几何对齐能大幅提升自由空间对准与视角鲁棒性，但遇到柔性形变、滑移、卡阻等力控问题时，必须向[物理增强专题](../../index.html#report=topic-physical-knowledge-to-control)延伸。

## 参考文献与馆藏入口

1. [π⁴: A Foundation Model for 4D Scene Geometry and Motion](https://arxiv.org/abs/2611.23144) · [馆藏卡片](../../index.html#paper=arxiv-2611-23144)
2. [ARROW: Arbitrary Reconstruction and Tracking of 4D Observations in the Wild](https://arxiv.org/abs/2610.01314) · [馆藏卡片](../../index.html#paper=arxiv-2610-01314)
3. [GAE: Learning a Geometry-Native Latent Space for 3D-Consistent World Generation](https://arxiv.org/abs/2609.24981) · [馆藏卡片](../../index.html#paper=arxiv-2609-24981)
4. [Spatial Forcing: Implicit Spatial Representation Alignment for Vision-Language-Action Model](https://arxiv.org/abs/2510.12276) · [馆藏卡片](../../index.html#paper=arxiv-2510-12276)
5. [SLA: Scaling Spatial-Language-Action Model via Continual Pre-training](https://arxiv.org/abs/2611.08373) · [馆藏卡片](../../index.html#paper=arxiv-2611-08373)
6. [Learning 4D Geometric Priors for Inference-Efficient World Action Models（MECo-WAM）](https://arxiv.org/abs/2607.05468) · [馆藏卡片](../../index.html#paper=arxiv-2607-05468)
7. [Gnomon4D: Learning Where and When to Focus for Geometric Motion-Grounded World-Action Modeling](https://arxiv.org/abs/2611.02474) · [馆藏卡片](../../index.html#paper=arxiv-2611-02474)
8. [TCP4D: A Unified Tool-Center-Point Tracking and Generation Model for Robot Manipulation](https://arxiv.org/abs/2611.23143) · [馆藏卡片](../../index.html#paper=arxiv-2611-23143)
9. [AffordanceWAM: Affordance-Aware Joint World-Action Modeling for Robot Manipulation](https://arxiv.org/abs/2609.22332) · [馆藏卡片](../../index.html#paper=arxiv-2609-22332)
10. [PointWorld: Scaling 3D World Models for In-The-Wild Robotic Manipulation](https://arxiv.org/abs/2601.03782) · [馆藏卡片](../../index.html#paper=arxiv-2601-03782)
