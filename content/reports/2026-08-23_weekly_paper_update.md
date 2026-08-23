# 知域每周论文更新：2026-08-23

**报告标签**：周报, World-Action-Model, HOI, 流式生成, 4D重建, 因果建模, 动作流, 自我中心视觉

- **检索日期**：2026-08-23
- **检索窗口**：2026-08-16 至 2026-08-22
- **检索方向**：HOI/3D-4D HOI、自我中心世界模型、Video/World Action Model、前馈重建与生成、世界模型中的因果建模与反事实推理、流式生成
- **候选数量**：18
- **新增论文数量**：5
- **已有论文重要更新数量**：0
- **已收录且无变化数量**：13
- **其他原因排除数量**：0
- **待人工核验数量**：7

## 馆藏检查

- **知域论文数据**：读取成功
- **知域报告索引**：读取成功
- **检查时馆藏论文数量**：68
- **检查时专题报告数量**：11
- **线上数据读取时间**：2026-08-23 00:30，Asia/Shanghai (UTC+8)
- **去重状态**：已与线上馆藏比较

注：线上馆藏中所有 68 篇论文的 `updated_at` 字段均为 2026-08-20 或 2026-08-21，判定为仓库级批量更新，非论文本身的实质变更，因此不作为"已有论文重要更新"计入。

## 检索方法

- **检索来源**：arXiv cs.RO 与 cs.CV 最新提交列表、arXiv 关键词搜索、Tavily/Google 搜索、AlphaXiv
- **关键词**：world model, world action model, hand-object interaction, 3D/4D reconstruction, feedforward, streaming, causal, counterfactual, latent action, action flow, video diffusion, egocentric, manipulation, autoregressive
- **纳入标准**：2026-08-16 至 2026-08-22 期间提交至 arXiv，与知域关注方向有直接技术关联
- **排除标准**：与关注方向无直接关联、仅有工程应用而无方法论贡献、仅摘要不可核验且无法追踪原论文
- **原始资料核验**：优先核对 arXiv 原文摘要，其次核对项目页面，部分通过 AlphaXiv AI Overview 辅助理解；无法访问论文正文时明确标注
- **检索范围限制**：未覆盖 OpenReview、会议期刊正式出版（大部分 8 月论文尚处于预印本阶段）；HuggingFace Daily Papers 页面无法访问；社交媒体线索通过 Tavily 间接获取

## 本周概览

本期最显著的新工作集中在三个方向：

1. **统一动作表示下的通用世界模型**：Hydra-0 提出以图像平面轨迹（action flow）作为跨本体共享的动作接口，使单一世界模型能从异质交互视频（人手、手持夹爪、单臂、双臂机器人）中学习，并支持正向预测与逆向控制两种模式。这是 action representation 路线在 world model 中的一次重要推进，直接呼应了 FlowWAM（光流动作）和 PointAction（3D 点动作）的思路，但在跨本体泛化和正向/逆向双模式上走得更远。

2. **流式自回归视频的 4D 一致性**：Stream4D 指出用静态 3D 高斯泼溅重建作为一致性奖励会惩罚真实运动、导致视频"冻结"，转而用前馈 4D 重建奖励和运动先验替代，在 Self-Forcing、Causal-Forcing、LongLive 三个骨干上均取得 4D 重建质量和运动保持的显著提升。该工作对"流式生成如何维持几何一致性"给出了比 World-R1/VideoGPA 更有针对性的解法。

3. **自我中心 3D 手部恢复**：DreamHand 将视频扩散模型重新定位为确定性几何编码器——单次 clean latent 前向暴露遮挡区域的手部状态，配合双向时空解码器恢复连续双手轨迹。在 ARCTIC 和 HOT3D 上分别削减 30%/40% MPJPE-p，遮挡场景优势达 46%–61%。这为从人类日常视频到机器人操作数据的大规模管线扫清了一个关键瓶颈。

其余两篇：DA-WAM 将动作条件反事实隐变量与规划评分统一在驾驶世界模型中；GigaBrain-WBC-0.5 引入行为世界模型预测下一步隐行为命令分布，使类人全身控制在地形交互下达到 81.3% 成功率。

BeyondMasks（ECCV 2026）提出了视频物体移除的因果一致性评估基准，与知域因果建模方向间接相关但核心场景不同，本期暂不作为正式条目收录，置于待人工核验线索。

## 分类与研究脉络

### World-Action Model 路线

Hydra-0 与 DA-WAM 代表了 WAM 路线内部两种不同的问题分解：

| 维度 | Hydra-0 | DA-WAM |
|------|---------|--------|
| 核心问题 | 跨本体的统一动作表示 | 驾驶场景中未来预测与规划的统一 |
| 动作表示 | 图像平面轨迹流（action flow） | 轨迹编码后的隐动作表示 |
| 条件方式 | 动作流作为像素对齐条件 | 每个候选轨迹独立生成反事实隐状态 |
| 预测目标 | 未来视频帧 | 未来隐状态 + 轨迹评分 |
| 正/逆向 | 双向（正向预测 + 逆向控制） | 仅正向（规划用） |
| 训练信号 | 流匹配损失 | 预测监督 + 规划损失联合 |
| 数据规模 | 2,202 h 多本体视频 | NAVSIM 驾驶数据 |

Hydra-0 的 action flow 概念直接延伸了 FlowWAM（光流动作）和 PointAction（3D 点动作），但选择停留在 2D 图像平面而非 3D 空间，换取了与视频生成骨干的自然对齐和跨本体兼容性。DA-WAM 则走另一条路：将预测性表示学习和轨迹规划目标统一在 EMA-encoder + action-conditioned predictor + factorized scorer 的单一训练目标下，避免预测与规划脱耦导致的"动作特异性信息稀释"。

### 流式生成与 4D 一致性

Stream4D 解决的问题是：流式自回归视频在长 rollout 中几何漂移和运动退化。此前 World-R1 和 VideoGPA 使用静态 3DGS 重建作为奖励信号，但这会惩罚真实运动（因为动态物体无法被静态重建解释），最终导致视频冻结。Stream4D 的核心改动是用 MoVieS 进行前馈 4D 重建，奖励能够被一致动态 4D 场景解释的视频。这直接关系到知域关注的"流式生成"方向，并且与 Causal-Forcing/Self-Forcing 的蒸馏范式形成了互补：蒸馏解决速度问题，4D 一致性奖励解决长程几何和运动问题。

### 自我中心 3D 手部与 HOI

DreamHand 的关键 insight 是：视频扩散模型的 clean latent（\(\sigma=0\) 单次前向）已经隐含编码了被遮挡手的状态信息，不需要做随机采样和像素空间渲染。这与此前 ViDiHand（多步随机采样）和 EgoForce/HaWoR（窗口回归）形成了根本性的方法差异。从 HOI 数据管线角度，DreamHand 为从日常自我中心视频恢复可用的 3D 手部轨迹提供了迄今为止最稳健的方案。

### 行为世界模型

GigaBrain-WBC-0.5 提出的行为世界模型（BWM）将传统追踪器的"被动跟踪"范式改为"因果 Transformer 同时预测下一步动作、状态和隐行为命令分布"。预测的命令分布用于在线检测不可行指令并回退到已学行为。这与世界动作模型的方向有交叉，但聚焦在全身控制的低层策略而非视觉生成。

## 证据审计

### Hydra-0

- **实验直接支持的结论**：action flow 条件相比原生动作条件降低机器人运动误差 90.4% 和物体运动误差 60.2%；RoboLab 基准上 replayed 与 reference 成功率 Pearson \(r=0.96\)；逆向模式无需任务特定专家演示即可将隐特征映射为可执行动作。
- **尚需注意**：论文将 action flow 定位为跨本体统一接口，但实验中逆向模式仅在单一本体设置中验证，跨本体逆向迁移的证据尚不充分。16× 生成加速来自蒸馏而非 action flow 本身。2,202 小时训练视频的过滤标准未在摘要中披露。

### Stream4D

- **实验直接支持的结论**：4D PSNR 在三个骨干上分别提升 3.46/5.53/6.76 dB；运动保持优于 World-R1/VideoGPA；人类评估偏好更高。
- **尚需注意**：MoVieS 作为 4D 重建奖励组件，其自身的重建误差和偏差会传递到奖励信号中，论文未讨论该组件的失败模式。运动先验的峰值高斯目标对"自然运动量级"的假设是否跨场景泛化，尚缺消融。评估在 500 个运动突出提示词上进行，对低运动场景的覆盖不明。

### DreamHand

- **实验直接支持的结论**：MPJPE-p 在 ARCTIC 上降 30%、HOT3D 上降 40%；含出视野评估时增益达 46%–61%；无需外接检测器；支持免相机内参配置。
- **尚需注意**：论文自述"repurpose VDM"但方法依赖 Wan VAE+DiT 的特定架构，迁移到其他视频扩散骨干的通用性未验证。离线 clip-level 框架意味着不适合实时场景。retargeting 演示为定性，缺定量评估。

### DA-WAM

- **实验直接支持的结论**：NAVSIM-v1 和 v2 上 SOTA；消融验证了 action-conditioned predictor 和 hard negative 的贡献。
- **尚需注意**：反事实隐状态的监督仅在专家轨迹上直接施加，其余候选通过评分器间接优化——这假设评分器能正确编码安全边界，但评分器自身的校准未讨论。方法专用于驾驶规划，非通用世界模型框架。

### GigaBrain-WBC-0.5

- **实验直接支持的结论**：地形交互成功率 81.3%（最强基线的 4.3×）；不可行指令下成功率 83.1%；跌倒恢复 99.3%（最强基线的 16.8×）；从 Unitree G1 迁移到 Maker L01 仅需简单微调。
- **尚需注意**：地形标注管线依赖 retargeted motion 的 3D 接触几何恢复，其精度下界未分析。BWM 的"预测下一步隐行为命令分布"与训练数据中的命令分布相关，对分布外行为的处理能力未显式评估。

## 对研究选题的影响

1. **Hydra-0 的 action flow 表示对动作空间设计有直接影响**：如果研究涉及跨本体学习或多源视频训练，action flow 提供了一个不需要本体特定坐标的统一接口。这与知域已收录的 FlowWAM（光流动作）、PointAction（3D 点动作）形成直接对照，需要在方案比较中考虑 2D 图像平面流 vs 3D 光流 vs 3D 点之间的权衡。

2. **Stream4D 对流式生成的评估和奖励设计有参考价值**：当前知域关注流式生成（Self-Forcing, Causal-Forcing, LongLive），Stream4D 的 4D 重建奖励提供了一个静态 3D 奖励的直接替代方案。如果研究涉及流式视频的一致性评估或强化学习奖励设计，应考虑 4D 一致性替代 3D 一致性。

3. **DreamHand 对自我中心 HOI 数据管线有实用影响**：从人类视频恢复 3D 手部轨迹是 HOI 研究的数据入口，DreamHand 的遮挡鲁棒性直接提升了该管线的可用性。如果研究依赖自我中心视频的 3D 手部标注，DreamHand 可作为前置模块。

4. **DA-WAM 的反事实隐建模对世界模型中因果建模方向有方法论参考**：DA-WAM 的"每个候选轨迹独立生成反事实隐状态"与知域关注的因果世界建模方向（Causal-JEPA 等）有交叉——两者都试图建模"如果不做 A 而做 B 会怎样"，但 DA-WAM 的反事实是规划层面的隐空间干预，而非结构因果模型层面的识别。

## 已收录且无重要变化

- DreamWAM (arxiv-2608-04996) — 知域已收录，本周期无 arXiv 实质更新
- Causal Forcing++ (arxiv-2605-15141) — 知域已收录，最新 arXiv 版本为 v3 (2026-06-01)，本周期无变化
- Self Forcing (arxiv-2506-08009) — 知域已收录，最新 arXiv 版本为 v2 (2025-11-10)，本周期无变化
- FlowWAM (arxiv-2607-13017) — 知域已收录，本周期无实质更新
- Causal-JEPA (arxiv-2602-11389) — 知域已收录，本周期无实质更新
- DynamicVGGT (arxiv-2603-08254) — 知域已收录，本周期无实质更新
- HandsOnWorld (arxiv-2607-02075) — 知域已收录，本周期无实质更新
- Egocentric World Model for HOI Synthesis (arxiv-2603-13615) — 知域已收录，本周期无实质更新
- HO-Flow (arxiv-2604-10836) — 知域已收录，本周期无实质更新
- FACT (arxiv-2608-10232) — 知域已收录，本周期无实质更新
- Dexterous World Models (arxiv-2512-17907) — 知域已收录，本周期无实质更新
- A Unifying Perspective on Causal World Models (arxiv-2608-13456) — 知域已收录，本周期无实质更新
- Discrete-WAM (arxiv-2606-05645) — 知域已收录，本周期无实质更新

注：以上论文在知域的 `updated_at` 均为 2026-08-20/21，但经核对 arXiv 原文，均无新版本发布，判定为仓库级批量更新。

## 待人工核验线索

1. **ForgeWM: Progressive Causal Training for World Models** (arXiv 2608.14022, 提交于 2026-08-14) — 刚在检索窗口之外（8 月 14 日），与知域关注的世界模型因果训练方向直接相关。如检索窗口向前扩展一天，则应纳入。

2. **Marionette: Predicting World States by Rendering, Painting, and Sculpting** (arXiv 2608.14530, 提交于 2026-08-14) — 同在窗口外（8 月 14 日），涉及世界状态预测的渲染-编辑范式。可能与知域已有论文存在版本关系，需人工核对。

3. **H2R-Bench: Benchmarking Human-to-Robot Video Generation** (arXiv 2608.13049, 提交于 2026-08-13) — 人类到机器人视频生成基准，与 HOI 和世界动作模型方向相关但在窗口外。

4. **VGGT-Align: Aligning 3D Reconstructions with VGGT** (arXiv 2608.15260, 提交于 2026-08-15) — 前馈 3D 重建方向，与 DynamicVGGT 可能存在版本关系，需核对。提交于 8 月 15 日，紧邻窗口边界。

5. **DreamX-Phi 1.0: Action-Conditioned Video World Model for Robotic Manipulation** (arXiv 2608.13489, 提交于 2026-08-13) — 动作条件视频世界模型，与 WAM 方向直接相关但在窗口外。WorldArena 2.0 Challenge 冠军。

6. **BeyondMasks: Evaluating Causal and Physical Consistency in Video Object Removal** (arXiv 2608.20107, ECCV 2026, 提交于 2026-08-20) — 在窗口内，提出了因果一致性的评估框架和 CORE 评估协议，将视频物体移除重新定义为因果场景一致性问题。核心贡献在评估层面而非方法论层面，与知域因果建模方向间接相关。需人工判断是否纳入正式条目。

7. **Gallileo-4D: Frozen Backbone Ensemble for Dynamic 4D Reconstruction** (arXiv 2608.19743, 提交于 2026-08-20) — PhysAI 4D 重建挑战赛第三名技术报告，主要贡献是推理时集成策略而非方法创新，与前馈重建方向的关联较弱。需人工判断是否纳入。

## 1. Hydra-0: Action Flow for Generalist World Modeling and Control

- **作者**：Hongyu Li, Bowen Wen, Xinghao Zhu, Yixuan Wang, Yilun Du, Yunzhu Li, George Konidaris, Stan Birchfield, Soha Pouya, Chenran Li, Yan Chang
- **年份与发表**：2026，arXiv 预印本
- **arXiv ID**：2608.18077
- **DOI**：10.48550/arXiv.2608.18077
- **论文**：[arXiv](https://arxiv.org/abs/2608.18077)
- **正式出版**：无
- **项目**：[Hydra-0 Project Page](https://nvidia-isaac.github.io/video_to_data/hydra-0/)
- **代码**：暂未公开
- **数据**：未提及
- **模型**：未提及
- **AlphaXiv**：[AlphaXiv](https://www.alphaxiv.org/abs/2608.18077)
- **类别标签**：World-Action-Model, 动作表示, 跨本体学习, 流匹配, 视频世界模型
- **证据等级**：仅摘要与项目页可见，待阅读全文核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无
- **代表图**：Hydra-0，Fig. 1，action flow 统一跨本体世界建模与控制的方法总览。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2608.18077v1/method_overview.png)

![Hydra-0 Fig. 1：action flow 世界建模与控制总览](https://arxiv.org/html/2608.18077v1/method_overview.png)

### 核心内容与 Insight

Hydra-0 提出以 **action flow**——图像平面上的轨迹流——作为跨本体的统一动作表示。核心 insight 是：无论是人手、手持夹爪、单臂还是双臂机器人，其可见运动都可以被描述为相机平面上的像素轨迹。这一表示将异质交互数据置于同一动作空间中，使单一通用世界模型能从多本体视频学习动作后果，并在正向模式下做未来场景预测、在逆向模式下从期望物体运动推导兼容机器人动作。

关键创新点：action flow 既是条件信号（正向：给定轨迹流预测视频），也是控制接口（逆向：给定目标物体流反推机器人运动），且两者共享同一世界模型潜在空间。

### Pipeline

**输入**：当前观测帧 + 动作流（像素平面轨迹序列，含可见性标记）

**过程**：动作流在训练时从交互视频中用密集追踪器恢复并用接地掩码分为本体轨迹和物体轨迹；在部署时从机器人运动学投影得到。视频扩散模型以第一帧 + 动作流为条件，用流匹配目标训练。逆向模式中，目标物体流编码到隐空间，经监督式动作头映射为可执行动作。

**输出**：正向模式输出未来视频序列（用于开环策略评估）；逆向模式输出可执行机器人动作（无需任务特定专家演示）

### 实验与证据

- **数据**：2,202 小时过滤多本体训练视频（EgoDex 人手、Deform360 手持夹爪、DROID 单臂、XVLA-Soft-Fold 双臂）
- **指标**：机器人运动误差、物体运动误差、RoboLab 成功率 Pearson 相关
- **定量结果**：action flow 条件相比原生动作条件，机器人运动误差降低 90.4%，物体运动误差降低 60.2%；RoboLab 300 episode 上 replayed 与 reference 成功率 \(r=0.96\)；蒸馏后生成加速 16×
- **消融**：摘要中提及零样本组合和数据高效适应，具体消融设计待全文核验
- **实验直接支持的结论**：action flow 作为条件显著优于原生动作条件；世界模型评分与实际控制成功率高度相关；逆向模式可工作
- **尚未被实验支持的主张**：跨本体逆向迁移（逆向模式仅在单一本体验证）；action flow 在非操作场景的通用性

### 代码与数据

代码、数据和模型在论文提交时均未公开。项目页仅展示演示视频和方法说明。无法判断复现性。

### 局限、失败案例与开放问题

- 逆向模式的跨本体迁移未验证
- action flow 依赖密集追踪器在训练时的恢复质量，追踪失败如何影响世界模型训练未讨论
- 2D 图像平面表示丢失深度信息，对需要 3D 精度的操作可能不足
- 2,202 小时视频的过滤标准未在摘要中披露

### 与知域的关系

Hydra-0 与知域关注的 World-Action-Model 方向直接相关。其 action flow 概念是 FlowWAM（光流动作）在 2D 图像平面的对应，但额外支持正向/逆向双模式操作，这是此前 WAM 路线中未见的。对跨本体学习、从人类视频到机器人控制的研究路线有直接影响。

---

## 2. Stream4D: 4D-Consistency for Streaming Autoregressive Diffusion Video Models

- **作者**：Yuanhao Ban, Jiaqi Feng, Hengguang Zhou, Xiaohuan Pei, Justin Cui, Cho-Jui Hsieh
- **年份与发表**：2026，arXiv 预印本（Under review）
- **arXiv ID**：2608.19556
- **DOI**：10.48550/arXiv.2608.19556
- **论文**：[arXiv](https://arxiv.org/abs/2608.19556)
- **正式出版**：无
- **项目**：[Stream4D Project Page](https://banyuanhao.github.io/Stream4D/)
- **代码**：暂未公开
- **数据**：未提及
- **模型**：未提及
- **AlphaXiv**：无
- **类别标签**：流式生成, 4D重建, 自回归扩散, 视频一致性, 奖励设计
- **证据等级**：仅摘要与项目页可见，待阅读全文核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无
- **代表图**：Stream4D，Fig. 1，静态 3D 奖励导致场景冻结，而动态 4D 奖励保留运动并改善长程一致性。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2608.19556v1/figure1_teaser.png)

![Stream4D Fig. 1：静态 3D 奖励与动态 4D 奖励对比](https://arxiv.org/html/2608.19556v1/figure1_teaser.png)

### 核心内容与 Insight

Stream4D 解决流式自回归视频生成中的长程几何漂移和运动退化问题。核心 insight 是：**用静态 3D 高斯泼溅重建作为一致性奖励会惩罚真实运动**——因为动态物体无法被单个刚性 3D 重建解释，奖励最大化的捷径是冻结画面。在自回归设置下，每个 chunk 会传播前一个 chunk 的错误，这种"冻结捷径"尤其有害。

Stream4D 用前馈 4D 重建（MoVieS）替代静态 3D 重建，使得能够被一致动态 4D 场景解释的视频获得高奖励。附加运动先验奖励自然场景流幅度并惩罚抖动和非刚性伪影，加上轻量感知锚点稳定外观。

### Pipeline

**输入**：自回归扩散骨干生成的视频 rollout

**过程**：MoVieS 将 rollout 重建为动态 4D 高斯场景，在估计相机下重渲染，4D PSNR 作为一致性奖励；场景流幅度的峰值高斯目标 + 平滑/刚性正则作为运动先验；HPSv2 作为感知锚点；三项 z 归一化后求和作为总奖励。

**输出**：奖励信号反馈给自回归扩散策略，用于 RLHF 或蒸馏微调

### 实验与证据

- **骨干**：Self-Forcing, Causal-Forcing, LongLive
- **指标**：MoVieS 4D-PSNR, Gemini Consistency win%, VideoReward Overall win%
- **定量结果**：4D-PSNR 提升 +3.46/+5.53/+6.76 dB；Gemini Consistency win% 82.2%/73.9%/74.2%；VideoReward Overall win% 66.2%/76.0%/84.4%
- **消融**：项目页对比了 World-R1 和 VideoGPA（静态 3D 奖励基线），Stream4D 在运动保持上一致更优
- **实验直接支持的结论**：4D 重建奖励有效替代静态 3D 奖励，避免运动退化；跨骨干泛化；人类偏好更高
- **尚未被实验支持的主张**：运动先验的"自然运动量级"假设是否跨场景泛化

### 代码与数据

代码和模型在项目页标注 "Under review"，暂未公开。

### 局限、失败案例与开放问题

- MoVieS 自身的重建误差和偏差会传递到奖励信号中，失败模式未讨论
- 运动先验对"自然运动量级"的假设可能不适用于所有场景
- 评估在 500 个运动突出提示词上进行，低运动/静态场景覆盖不明
- 依赖 MoVieS 做 4D 重建，计算开销未报告

### 与知域的关系

Stream4D 与知域关注的流式生成方向（Self-Forcing, Causal-Forcing, LongLive）直接相关。它不是新的生成骨干，而是这些骨干上的一致性奖励改进，对"流式生成如何维持长程几何与运动一致性"给出了比 World-R1/VideoGPA 更有针对性的方案。4D 重建奖励的思路对前馈重建方向也有间接参考。

---

## 3. DreamHand: Repurposing Video Diffusion Models for Occlusion-Robust Egocentric 3D Hand Motion Recovery

- **作者**：Yufei Liu, Xixi Wang, Hao Li, Ganlong Zhao, Kaitong Cai, Chengkai Jin, Chunxiao Liu, Jianbo Liu, Siyuan Huang, Xingang Pan, Hongsheng Li
- **年份与发表**：2026，arXiv 预印本
- **arXiv ID**：2608.20308
- **DOI**：10.48550/arXiv.2608.20308
- **论文**：[arXiv](https://arxiv.org/abs/2608.20308)
- **正式出版**：无
- **项目**：[DreamHand Project Page](https://ggxxii.github.io/dreamhand/)
- **代码**：暂未公开
- **数据**：未提及
- **模型**：暂未公开
- **AlphaXiv**：无
- **类别标签**：HOI, 自我中心视觉, 3D手部恢复, 视频扩散, 遮挡处理
- **证据等级**：仅摘要与项目页可见，待阅读全文核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无
- **代表图**：DreamHand，Fig. 2，clean-latent 编码、Ray Head 与双向时空解码器组成的整体框架。来源：[Fig. 2 原图 PNG](https://arxiv.org/html/2608.20308v1/dreamhand_method.png)

![DreamHand Fig. 2：遮挡鲁棒的自我中心 3D 手部恢复框架](https://arxiv.org/html/2608.20308v1/dreamhand_method.png)

### 核心内容与 Insight

DreamHand 的核心 insight 是：**视频扩散模型的 clean latent（\(\sigma=0\) 单次前向）已经编码了被遮挡和出视野手部的状态信息**，不需要多步随机采样做像素空间渲染。因此，将 VDM 从随机像素生成器重新定位为确定性几何编码器——Deterministic Clean-Latent Encoder——即可从单次前向中提取出包含遮挡区域信息的特征。

配合双向时空解码器（Bidirectional Spatiotemporal Decoder），DreamHand 从离线 clip 级别恢复连续双手轨迹，实现度量级 3D 定位，无需外接检测器。Ray-Based Camera Solver 支持免相机内参配置。

### Pipeline

**输入**：自我中心视频片段

**过程**：Wan VAE 编码为 latent → Wan DiT（\(\sigma=0\)，确定性前向）提取 Block-15 特征 → 特征分两路：(1) Ray Head 预测相机内参（训练时监督，推理时可弃用）；(2) 双向时空解码器从特征恢复连续双手 3D 关节轨迹 → Ray-Based Camera Solver 从射线解算平移

**输出**：双手 3D 关节位置序列（度量坐标），可选配相机内参

### 实验与证据

- **基准**：ARCTIC, HOT3D, OAKINK2, HOCapture, 野生视频
- **指标**：MPJPE-p, PA-p, MPJPE+OOS, EPE2D-p, GO-p, CT-p, Jitter, FAcc, Recall, F1
- **定量结果**：ARCTIC 上 MPJPE-p 降低 30%（遮挡密集场景）；HOT3D 上降低 40%；含出视野手部评估时增益 46%–61%；五个基准全部 SOTA
- **基线**：InterWild, HaMeR, Hamba, WildHands, WiLoR, EgoForce, OmniHands, Dyn-HaMR, HaWoR
- **消融**：项目页展示了 K-free 配置（免相机内参）与标准配置的对比；展示了逐步遮挡程度的性能曲线
- **实验直接支持的结论**：clean-latent 编码在遮挡和出视野场景下显著优于逐帧/窗口回归方法；无需外接检测器；免内参配置可行
- **尚未被实验支持的主张**：方法对 Wan VAE+DiT 以外骨干的通用性；实时适用性（离线 clip 级别）

### 代码与数据

代码和模型暂未公开。项目页展示定性演示和 retargeting 结果，但无下载链接。

### 局限、失败案例与开放问题

- 方法依赖 Wan VAE+DiT 的特定架构，迁移到其他视频扩散骨干的通用性未验证
- 离线 clip-level 框架，不适合实时场景
- retargeting 演示为定性，缺定量评估
- "clean latent 隐含遮挡信息"的机制解释停留在经验层面，理论分析不足

### 与知域的关系

DreamHand 与知域关注的自我中心世界模型和 HOI 方向直接相关。从人类日常自我中心视频恢复 3D 手部轨迹是 HOI 数据管线的关键入口，DreamHand 的遮挡鲁棒性直接提升了该管线的可用性。与知域已收录的 EgoGrasp（自我中心 HOI 估计）、Hand2World（自我中心交互生成）、HandsOnWorld（自我中心视频生成）形成互补——DreamHand 提供更上游的 3D 手部数据。

---

## 4. DA-WAM: Decision-Aligned Future Latents for Driving World Models

- **作者**：Ruiguo Zhong, Benshan Ma, Xiaolong Chen, Lang Zhang, Mingyue Feng, Yaonong Wang, Pei Liu, Jun Ma
- **年份与发表**：2026，arXiv 预印本（v2 于 2026-08-20 更新）
- **arXiv ID**：2608.19085
- **DOI**：10.48550/arXiv.2608.19085
- **论文**：[arXiv](https://arxiv.org/abs/2608.19085)
- **正式出版**：无
- **项目**：未提及
- **代码**：未提及
- **数据**：NAVSIM
- **模型**：未提及
- **AlphaXiv**：[AlphaXiv](https://www.alphaxiv.org/abs/2608.19085)
- **类别标签**：World-Action-Model, 驾驶世界模型, 反事实推理, 动作条件预测, 规划
- **证据等级**：仅摘要与 AlphaXiv AI Overview 可见，待阅读全文核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无
- **代表图**：DA-WAM，Fig. 2，为每条候选轨迹预测专属未来隐状态并进行因子化规划评分的整体框架。来源：[Fig. 2 原图 PNG](https://arxiv.org/html/2608.19085v2/Figures/overview2.png)

![DA-WAM Fig. 2：候选轨迹与未来隐状态一一对齐的规划框架](https://arxiv.org/html/2608.19085v2/Figures/overview2.png)

### 核心内容与 Insight

DA-WAM 的核心 insight 是：**世界模型对规划最有用时，其预测应当是"决策信息性的"——每个候选轨迹应有其专属的未来隐状态预测**，而非所有候选共享一个"全局未来"。现有方法或将预测表示学习与规划优化脱耦，或跨候选共享预测状态，稀释了动作特异性的后果信息。

DA-WAM 统一了预测性表示学习、动作条件未来建模和轨迹评分于单一决策目标：在线编码器（V-JEPA 2.1 + LoRA）提取场景隐 token，动作条件预测器为每个候选轨迹生成独立未来隐状态，因子化评分器基于未来隐状态评估轨迹。专家匹配轨迹的预测隐状态由观测未来表示直接监督；安全关键硬负例在规划边界提供额外监督。

### Pipeline

**输入**：当前视觉观测（相机帧）+ 候选轨迹集合 \(\{\tau_i\}_{i=1}^N\)

**过程**：在线编码器 \(E_\theta\)（V-JEPA 2.1 + LoRA）提取当前场景 token \(Z_t\)；轨迹编码器 \(E_\tau\) 将每条候选编码为动作表示 \(a_i\)；动作条件预测器 \(P_\phi\) 结合 \(a_i\) 和 \(Z_t\) 预测每条候选的未来隐状态 \(\hat{Z}^i\)；因子化评分器基于 \(\hat{Z}^i\) 输出轨迹评分；目标编码器 \(E_{\bar\theta}\)（EMA 更新）提供未来表示监督

**输出**：每条候选轨迹的评分（用于规划选择）

### 实验与证据

- **数据集**：NAVSIM-v1, NAVSIM-v2
- **指标**：规划相关指标（具体指标待全文确认）
- **定量结果**：声称 SOTA，具体数值待全文核验
- **消融**：AlphaXiv 概述提及消融验证了 action-conditioned predictor 和 hard negative 的贡献
- **实验直接支持的结论**：统一预测与规划目标优于脱耦方案；每候选独立未来隐状态优于共享方案
- **尚未被实验支持的主张**：反事实隐建模在更复杂场景下的校准性；方法的通用性（限于驾驶规划）

### 代码与数据

代码未公开。使用 NAVSIM 公开基准。

### 局限、失败案例与开放问题

- 反事实隐状态的监督仅在专家轨迹上直接施加，其余候选通过评分器间接优化——评分器校准是隐假设
- 方法专用于驾驶规划，非通用世界模型框架
- 依赖 V-JEPA 2.1 作为视觉骨干，迁移性未验证
- 硬负例的选取策略和其对评分器决策边界的影响需进一步分析

### 与知域的关系

DA-WAM 与知域关注的 World-Action-Model 和因果建模方向直接相关。其"每候选独立反事实隐状态"的思路与 Causal-JEPA 等因果世界建模方向有概念交叉——两者都试图建模"如果做 A 而非 B 会怎样"——但 DA-WAM 的反事实是规划层面的隐空间干预（action-conditioned counterfactual latents），而非结构因果模型层面的识别。对"世界模型如何服务于决策"这一路线提供了新的架构选择。

---

## 5. GigaBrain-WBC-0.5: A Behavior World Model for Robust Whole-Body Control with Environment Interaction

- **作者**：Ziyang Cheng, Tianshu Tang, Jinxin Lan, Xinze Chen, Yuhan Gong, Zhichao Liu, Changzhong Wu, Yahao Mao, Zongyan Deng, Mingxuan Ma, Huasen Xi, Yilong Liu, Yutong Wu, Xiaofeng Wang, Yang Wang, Yun Ye, Guan Huang, Xiaojie Jin, Zheng Zhu, Jiwen Lu
- **年份与发表**：2026，arXiv 预印本（Technical report）
- **arXiv ID**：2608.18234
- **DOI**：10.48550/arXiv.2608.18234
- **论文**：[arXiv](https://arxiv.org/abs/2608.18234)
- **正式出版**：无
- **项目**：[GigaBrain-WBC-0.5 Project Page](https://shepherd1226.github.io/gigabrain-wbc-0.5/)
- **代码**：暂未公开
- **数据**：未提及
- **模型**：暂未公开
- **AlphaXiv**：无
- **类别标签**：行为世界模型, 全身控制, 类人机器人, 因果Transformer, 地形交互
- **证据等级**：仅摘要可见，待阅读全文核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无
- **代表图**：GigaBrain-WBC-0.5，Fig. 2，行为命令量化与因果 Transformer 联合预测动作、状态和下一步隐行为命令的整体框架。来源：[Fig. 2 原图 PNG](https://arxiv.org/html/2608.18234v1/overview.png)

![GigaBrain-WBC-0.5 Fig. 2：行为世界模型整体框架](https://arxiv.org/html/2608.18234v1/overview.png)

### 核心内容与 Insight

GigaBrain-WBC-0.5 提出行为世界模型（BWM）范式：**因果 Transformer 同时预测下一步动作、下一步状态和下一步隐行为命令分布**，使动作网络本身建模环境如何塑造其下一步能做什么。传统追踪器在空场景训练，从未学习地形和物体接触如何重塑动力学，而是试图通过不断增大参考运动语料来覆盖——一旦可行行为变得环境依赖，这条路线就失效了。

BWM 的预测命令分布被复用于在线检测不可行指令并回退到已学行为，使机器人以"尽力而为"方式执行任务。自动地形标注管线从 retargeted 运动恢复完整 3D 接触几何，使地形标注达到现有运动数据集的规模。

### Pipeline

**输入**：实时命令 + 本体感知 + 视觉/地形观测

**过程**：因果 Transformer 联合预测 (1) 下一步动作、(2) 下一步状态、(3) 下一步隐行为命令分布；预测的分布用于检测不可行命令并回退；自动地形标注管线在训练时为运动数据提供 3D 接触几何

**输出**：全身控制指令；不可行命令检测与回退

### 实验与证据

- **基线**：三个大规模追踪器基线
- **指标**：成功率
- **定量结果**：地形交互成功率 81.3%（最强基线的 4.3×）；不可行指令下成功率 83.1%；跌倒恢复 99.3%（最强基线的 16.8×）；Unitree G1 → Maker L01 简单微调即可迁移
- **消融**：待全文核验
- **实验直接支持的结论**：BWM 在地形交互和不可行指令场景下大幅优于传统追踪器；跌倒恢复能力极强；跨硬件可迁移
- **尚未被实验支持的主张**：BWM 对分布外地形/行为的处理能力；命令分布预测的校准性

### 代码与数据

代码和模型暂未公开。

### 局限、失败案例与开放问题

- 地形标注管线依赖 retargeted motion 的 3D 接触几何恢复，精度下界未分析
- BWM 预测的命令分布与训练数据中的命令分布相关，分布外行为的处理能力未显式评估
- 仅在类人机器人全身控制中验证，BWM 范式是否适用于其他控制场景未讨论
- 多本体迁移的"简单微调"具体成本未量化

### 与知域的关系

GigaBrain-WBC-0.5 与知域关注的世界模型方向有交叉——其行为世界模型预测下一步隐行为命令分布，与世界动作模型预测未来场景/动作的思路有概念关联。但该工作聚焦在低层全身控制的策略层面而非视觉生成层面，属于世界模型在控制中的应用而非世界动作模型的方法论推进。对全身交互控制、地形感知行为生成的研究路线有参考价值。
