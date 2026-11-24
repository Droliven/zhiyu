# 动态操作与实时闭环：运动感知、异步执行与流式世界模型

**更新日期**：2026-11-23

**报告标签**：World Action Model, VLA, 机器人学习, 流式与自回归, 规划与控制

> 当操作对象在推理与执行期间持续运动，或在高速交互中发生轨迹突变时，“单帧观测 + 同步大块推理”的静态策略会全面失灵。本专题聚焦平行夹爪与通用机械臂的动态操作，沿**破除静态偏置与运动感知 → 异步执行与快慢解耦闭环 → 低延迟流式世界模型与几何前瞻**三条轴线，梳理代表工作与核心取舍。

本专题聚焦“时间紧迫、目标在动、延迟敏感”的实时控制问题，与关注慢速长程推理的[具身 Agent 与 RSI 专题](../../index.html#report=topic-embodied-agents-improvement)以及关注底层物理机理的[物理增强专题](../../index.html#report=topic-physical-knowledge-to-control)互补。

[toc]

## 一、动态操作到底难在哪？三道必须同时跨过的门槛

静态桌面抓取允许策略“看一眼 → 停 0.5 秒算一整段动作 → 闭眼执行完再看”，但动态操作中这套流程会在三个环节接连崩盘：

| 动态瓶颈 | 典型失败模式 | 代表解决路线 | 代表工作 |
| --- | --- | --- | --- |
| **1. 单帧运动歧义与静态偏置** | 看不出目标速度/方向；中途重规划触发“目标响应坍缩”，无视目标搬家 | 双路径光流+运动学条件、统一光流动作表征、零重训反事实规范规划 | [DynamicWAM](https://arxiv.org/abs/2608.00793)、[FlowWAM](https://arxiv.org/abs/2607.13017)、[DPP](https://arxiv.org/abs/2609.33172) |
| **2. 推理滞后与块边界卡顿** | 算完动作块时目标已移走；过期前缀拖后腿；切块瞬间模式跳变抖动 | 推理期软掩码修补（RTC）、轻量快模型+过期前缀裁剪（LAAS）、慢规划/快执行异步解耦与低成本想象 | [RTC](https://arxiv.org/abs/2506.07339)、[DynamicVLA](https://arxiv.org/abs/2601.22153)、[AHA-WAM](https://arxiv.org/abs/2606.09811)、[DualWAM](https://arxiv.org/abs/2609.24868)、[Efficient-WAM](https://arxiv.org/abs/2606.10040) |
| **3. 在线世界预测过慢** | 视频扩散去噪与 VAE 解码动辄数百毫秒，无法进入实时闭环推演与筛选 | 少步因果流蒸馏、宽度压缩超快 VAE、低维几何前瞻筛选 | [LynnReal-Hand](https://arxiv.org/abs/2611.21479)、[PrimeSim](https://arxiv.org/abs/2611.04870)、[RodForesight](https://arxiv.org/abs/2609.12103) |

## 二、看懂目标运动，并破除静态策略的“响应坍缩”

要拦截传送带、转盘或滚动物体，面临两条截然不同的路线：一条是**让模型显式学会看懂运动**，另一条是**零重训撬动静态模型已有的技能**。

- **双路径运动条件（[DynamicWAM](https://arxiv.org/abs/2608.00793)）**：揭示了一个极易踩坑的表示陷阱——把历史光流渲染成 RGB 喂给视频 VAE 虽保留空间运动形态，但逐帧归一化会抹掉绝对位移尺度，且图片不含帧间时长 $\Delta\tau$。它采用“视频侧拼入 4 段归一化光流帧 + 动作侧注入 12 维显式运动学 Token（位移、时长、速度、加速度）”的双路径设计：DOMINO 同步评测从静态 WAM 的 22.7% 跃升至 **38.2%**，真机 12 项直线/圆周/复合运动任务均值达 **46.67%**（超 $\pi_{0.5}$ +22.9 pp）。类似的，**[FlowWAM](https://arxiv.org/abs/2607.13017)** 尝试直接以光流作为 WAM 的统一动作表征，打通跨本体运动信号。
- **零重训反事实规划（[DPP](https://arxiv.org/abs/2609.33172)）**：给出了极具启发性的反直觉诊断——静态预训练 WAM 抓不住移动物体，往往不是不会抓，而是陷入了**目标响应坍缩（Target-Response Collapse）**：机械臂一旦走到中途状态 $S_k$，该姿态与原目标高度绑定，导致策略无视目标移位（执行 48 步后响应增益从 0.885 跌至 0.063）。DPP 先用 WAM 推演估计交互时刻 $\tau$ 并外推目标未来位置 $\hat{x}(\tau)$，再把 $\hat{x}(\tau)$ 通过 RGB-D 编辑放回**最熟悉的初始机械臂画面 $S_0$** 里唤醒静态技能，最后用 IK 激活桥接异步接入当前执行状态。在 RoboTwin2.0-Dyn 上，零动态训练的 FastWAM+DPP（**83.33% / 80.73%**）与 ImageWAM+DPP（**78.67% / 91.15%**）反超了额外用动态数据训练的 DynamicWAM（52.00% / 53.13%）；真机移动抓取达 **76.7%**（基线 0%）。

## 三、消除感知—执行滞后：异步修补、延迟裁剪与快慢解耦

即便看懂了目标运动，如果每次策略查询要停顿几百毫秒，动态拦截依然会慢半拍。近期工作沿着四条互补路径向推理延迟开刀：

- **推理期软掩码修补（[RTC](https://arxiv.org/abs/2506.07339)）**：异步闭环的基石算法。把新旧动作块衔接建模为流/扩散模型的 inpainting——冻结延迟窗口内必执行的前 $d$ 步，对重叠段施加指数衰减软掩码，用 $\Pi\text{GDM}$ 伪逆梯度补全剩余轨迹。无需重训，在 $\pi_{0.5}$ 真机 6 任务上顶住 $+200\text{ ms}$ 注入延迟几乎零衰减（而 Temporal Ensembling 直接振荡触发保护急停）。DynamicWAM 真机叠加 RTC 后均值从 42.08% 提至 **46.67%**。
- **轻量快主干 + 延迟感知前缀裁剪（[DynamicVLA](https://arxiv.org/abs/2601.22153)）**：指出了纯重叠平滑的盲区——RTC/TE 只平滑块边界，却没有剔除已经过期的动作前缀。DynamicVLA 用 0.4B 紧凑模型（FastViT + SmolLM2）把单块推理压至 **0.226 s**，配合无阻塞连续推理（CI）与延迟感知动作流（LAAS）在线丢弃过期 $m$ 步前缀，在 1,800 回合 DOM 动态基准上拿到 **47.06%**（远超 RTC 11.22% 与 $\pi_{0.5}$ 11.06%）；同模型消融显示不开 LAAS 时 RTC/TE 均卡在 ~39.8%，打开 LAAS 立刻再涨 +7.3 pp。
- **慢世界规划 + 快动作执行异步解耦（[AHA-WAM](https://arxiv.org/abs/2606.09811)、[DualWAM](https://arxiv.org/abs/2609.24868)）**：正面解决 WAM 的时间粒度错配。AHA-WAM 让 5B 视频 DiT 低频规划长程上下文（$h_v=64$，带 6 帧滚动 K/V 记忆），把 1B 动作 DiT（$h_a=16$）移出视频关键路径，靠**观测引导上下文路由（OVCR）**与变相位偏移训练实时消除复用上下文的相位漂移（直接朴素异步会从 91.83% 掉到 88.60%，加 OVCR+记忆后反升至 RoboTwin 2.0 **92.80%**）；叠加 TensorRT/CUDA Graph 与 2 步 ODE 蒸馏，单卡 RTX 5090D 跑出 **24.17 Hz / 56.95 Hz**。DualWAM 则让低频全局 System 2 与高频腕部 System 1 接力完成同一条世界—动作去噪轨迹。
- **低成本潜空间未来想象（[Efficient-WAM](https://arxiv.org/abs/2606.10040)）**：通过压缩模型规模（1B 参数）与轻量化未来预测表征，直接从骨干侧压低世界想象的推理账单。

## 四、低延迟流式世界模型底座与几何前瞻筛选

如果动态闭环需要在线调用视觉或几何世界预测（而非把世界分支完全移出高频路径），去噪步数、解码速度与预测表示必须同步轻量化：

- **少步因果流式视频底座（[LynnReal-Hand](https://arxiv.org/abs/2611.21479)、[PrimeSim](https://arxiv.org/abs/2611.04870)）**：LynnReal-Hand 以 3 步因果流图 + 区域感知双分数蒸馏 + 宽度压缩 Ultra-Fast-VAE（解码提速 17.8×），在单卡 H200 上将 33B 交互世界模型推到 **540p / 18.03 FPS**；PrimeSim 借助少步因果生成与分层记忆，实现跨本体动作条件的 **10.1 FPS** 交互仿真。
- **低维几何前瞻候选筛选（[RodForesight](https://arxiv.org/abs/2609.12103)）**：针对细长、跨材料杆件插接等易卡阻任务，先用视觉伺服缩小初始误差，再用极轻量的低维“杆尖—孔”几何世界模型在执行前对扩散策略提出的多个候选动作打分排序，不靠触觉硬件也能提前规避接触卡阻。

## 五、核心取舍与选题方向

| 路线 | 强项 | 主要代价与盲区 |
| --- | --- | --- |
| **运动条件训练（DynamicWAM / FlowWAM）** | 端到端学懂速度与节拍，动作接口不变 | 限于固定外置相机 2D 光流，难防干扰物与深向运动，需动态数据 |
| **零重训反事实规划（DPP）** | 不采动态数据即可唤醒静态 WAM 技能，拦截指标极高 | 强依赖目标跟踪可预测性（SAM 2 + FoundationPose）与 RGB-D 编辑精度 |
| **异步修补与前缀裁剪（RTC / DynamicVLA）** | 通用性强，彻底消灭块间停顿与过期前缀 | RTC 不降单次延迟；LAAS 要求 $n \ge 2m$，大骨干仍受限于硬件延迟 |
| **慢世界 + 快动作解耦（AHA-WAM / DualWAM）** | 保留长程世界规划同时跑出 24–57 Hz 高频闭环 | 引入时域超参配比，且单靠高频异步不能自动消除静态训练的移动目标偏置 |
| **少步流式世界模型（LynnReal-Hand / PrimeSim）** | 画面交互响应快（10–18 FPS），支持在线视觉推演 | 硬件门槛高（H200），且短因果窗缺少长时 3D 记忆 |

**下一步值得突破的方向**：
1. **3D/4D 对象级运动条件 + 快慢异步解耦**：把 [DynamicWAM](https://arxiv.org/abs/2608.00793) 的固定 2D 光流升级为以目标为中心的 3D/4D 速度场（衔接 [π⁴](https://arxiv.org/abs/2611.23144) 或 [Gnomon4D](https://arxiv.org/abs/2611.02474)），再接入 [AHA-WAM](https://arxiv.org/abs/2606.09811) 的快慢解耦框架，同时拿到“看懂 3D 运动”与“50 Hz 闭环”。
2. **动态拦截与临近纠偏的自适应时域切换**：自由逼近阶段用 [DPP](https://arxiv.org/abs/2609.33172) 或长动作块高效抢位，临近交互或目标突发改向时自动切入 [DynamicVLA](https://arxiv.org/abs/2601.22153) / [RTC](https://arxiv.org/abs/2506.07339) 短时域异步纠偏。

## 参考文献与馆藏入口

1. [Real-Time Execution of Action Chunking Flow Policies (RTC)](https://arxiv.org/abs/2506.07339) · [馆藏卡片](../../index.html#paper=arxiv-2506-07339)
2. [DynamicVLA: A Vision-Language-Action Model for Dynamic Object Manipulation](https://arxiv.org/abs/2601.22153) · [馆藏卡片](../../index.html#paper=arxiv-2601-22153)
3. [AHA-WAM: Asynchronous Horizon-Adaptive World-Action Modeling with Observation-Guided Context Routing](https://arxiv.org/abs/2606.09811) · [馆藏卡片](../../index.html#paper=arxiv-2606-09811)
4. [Efficient-WAM: A 1B-Parameter World-Action Model with Low-Cost Future Imagination](https://arxiv.org/abs/2606.10040) · [馆藏卡片](../../index.html#paper=arxiv-2606-10040)
5. [FlowWAM: Optical Flow as a Unified Action Representation for World Action Models](https://arxiv.org/abs/2607.13017) · [馆藏卡片](../../index.html#paper=arxiv-2607-13017)
6. [DynamicWAM: Dual-Path Motion Conditioning for World-Action Models in Dynamic Manipulation](https://arxiv.org/abs/2608.00793) · [馆藏卡片](../../index.html#paper=arxiv-2608-00793)
7. [Dynamic Manipulation with World–Action Models via Counterfactual Planning (DPP)](https://arxiv.org/abs/2609.33172) · [馆藏卡片](../../index.html#paper=arxiv-2609-33172)
8. [DualWAM: Dual-System World Action Models for Asynchronous Global Planning and Local Refinement](https://arxiv.org/abs/2609.24868) · [馆藏卡片](../../index.html#paper=arxiv-2609-24868)
9. [RodForesight: A World Model Enhanced Diffusion Policy for Slender and Material Agnostic Rod Insertion](https://arxiv.org/abs/2609.12103) · [馆藏卡片](../../index.html#paper=arxiv-2609-12103)
10. [LynnReal-Hand: Unlocking World Interaction with Hand Control](https://arxiv.org/abs/2611.21479) · [馆藏卡片](../../index.html#paper=arxiv-2611-21479)
11. [PrimeSim: A Generalist World Model Simulator from Large-Scale Cross-Embodiment Data](https://arxiv.org/abs/2611.04870) · [馆藏卡片](../../index.html#paper=arxiv-2611-04870)
12. [π⁴: A Foundation Model for 4D Scene Geometry and Motion](https://arxiv.org/abs/2611.23144) · [馆藏卡片](../../index.html#paper=arxiv-2611-23144)
13. [Gnomon4D: Learning Where and When to Focus for Geometric Motion-Grounded World-Action Modeling](https://arxiv.org/abs/2611.02474) · [馆藏卡片](../../index.html#paper=arxiv-2611-02474)
