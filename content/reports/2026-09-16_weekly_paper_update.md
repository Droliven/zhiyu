<!-- suggested_filename: 2026-09-16_weekly_paper_update.md -->

# 从视频预测到结构化世界状态：WAM、3D/4D 与具身交互新进展

**报告标签**：周报, World Action Model, 3D/4D, HOI, 人类视频, 流式世界模型, 前馈重建, 因果审计, 具身导航

- **检索日期**：2026-09-16
- **检索窗口**：2026-09-07 至 2026-09-16
- **检索方向**：3D/4D HOI、Egocentric World Model、Video / World Action Model、embodied in-context learning、人类视频与跨本体学习、因果/反事实世界模型、Feedforward Reconstruction and Generation、流式生成及高度相关具身研究
- **候选数量**：23
- **新增论文数量**：13
- **已有论文重要更新数量**：0
- **已收录且无变化数量**：5
- **其他原因排除数量**：5
- **待人工核验数量**：0

## 馆藏检查

- **知域论文数据**：读取成功。`papers.json` 可正常访问，并包含 `id`、`title`、`arxiv_id`、`doi`、`links`、`source_reports`、`updated_at` 等用于增量匹配的字段。
- **知域报告索引**：读取成功。
- **检查时馆藏论文数量**：线上读取时未能可靠取得精确数组长度；本地导入前已核验为 193 篇。
- **检查时专题报告数量**：24
- **线上数据读取时间**：2026-09-16 18:55，UTC+8
- **去重状态**：已与线上馆藏比较；正式新增候选均进一步按 arXiv ID、规范化标题和版本关系检查。线上页面自身也说明，线上去重只是第一层检查，后续本地导入还会再次去重。
- **索引异常说明**：`reports.json` 中存在日期晚于本次执行日的报告记录；此类记录没有被用于扩展本期 2026-09-07 至 2026-09-16 的检索窗口。

## 检索方法

本期先读取知域 `papers.json` 与 `reports.json`，再围绕 World Action Model、world model + human video、latent action、3D action、4D affordance、hand-object interaction、interaction field、streaming world model、feedforward reconstruction、counterfactual VLA、physical world-model consistency、embodied navigation 等关键词进行交叉检索。论文发现阶段同时参考论文聚合和搜索索引，但正式条目的事实核验均回到 arXiv 原始页面、arXiv HTML 正文或作者官方项目页；没有把搜索摘要、论文聚合站或社区帖子直接作为实验结论来源。

去重首先在本期候选之间按 arXiv ID、标题规范化和版本关系完成，再对线上 `papers.json` 做精确 ID/标题匹配。对于已经存在于知域且没有发现新版本、正式发表、代码/数据/模型首次发布等变化的工作，不重新作为新增论文收录。

本期代表图优先使用 arXiv HTML 可直接打开的 png/jpg 原图。ModAR 的 HTML 未转换出插图文件，因此将其 arXiv 源文件 Fig. 1（`figures/teaser.pdf`）下载并保存为本地 WebP。

## 本周概览

本期最明显的变化发生在 **World Action Model 的表示接口**。WLA³、XPACE 和 ModAR 都不再把“未来 RGB 视频”视为唯一合理的世界预测接口：WLA³尝试把跨人类/机器人数据共享的世界状态变化压缩为 latent action；XPACE让同一视频骨干同时承担 world-action policy 与 action-conditioned simulator；ModAR则进一步系统比较 point tracks、DINO feature、depth、RGB 等预测模态，结果显示在其任务和数据规模上，tracks、语义特征与深度都有正贡献，而额外生成未来 RGB 没有稳定增益。

这一趋势对 3D/4D WAM 尤其重要：**“是否预测视频”正在让位于“预测什么中间世界状态最有利于动作”**。GeomVLA把未来场景运动显式拉到共享 3D 空间；WLA³把 world transition 抽象为跨本体 latent action；ModAR把几何、运动、语义预测安排在动作之前。对于后续研究，仅仅在 VLA 上增加一个 3D 分支已经很难形成强 novelty，更值得探索的是长期 4D object/contact state、交互约束、跨本体可执行 grounding，以及中间世界状态与动作决策之间的因果/信息关系。

**人类视频进入机器人学习的方式也进一步分化。** WLA³把人类视频中的世界转移作为 latent-action 监督；ReWeight不要求所有人类数据都有效，而是先做 demonstration retrieval，再按跨本体行为差异加权；XPACE则用无动作视频学习动态、用带动作的人类和机器人轨迹联合学习 world/action，并让模拟器合成 recovery experience。三者分别对应“共享动作表示”“数据选择/加权”“世界模型自生成训练数据”三条路线。

流式生成方向出现了一个值得关注的表示变化：AlayaVista不持续在当前透视视野里维护全部世界状态，而是维护 360° panoramic latent state，再按当前相机查询透视视频。这与 StreamingHOI 一类工作的具体任务不同，但“**全局持久状态 + 局部按需高保真渲染**”是一个可迁移的系统设计思想。

HOI 方面，本期两篇工作并非 4D HOI world model，而是在结构感知上补强：Single-Query Bimanual HOI 将人、左右手、姿态和交互目标绑定到单个 person-centric query；JSSR则利用校准双目和关节条件的几何候选搜索估计最近交互表面点。前者解决多人物场景中的“手属于谁、与什么交互”，后者解决“每个关节最近的交互表面在哪里”。它们分别提供了未来 4D HOI 系统可借用的结构关联与几何接触接口。

在因果主题上，本期没有发现足以归类为 **causal identification / structural causal model** 的新型世界模型。IMPACT-VLA使用闭环输入替换和重新执行构造 counterfactual trajectories，是一种 intervention-based attribution；One Model, Two Physical Stories 使用干预梯度审计视频输出与语言/解析物理约束之间的一致性。这两篇都值得纳入“反事实评测/审计”，但不应升级表述为结构因果世界模型。

## 分类与研究脉络

**World Action Model / 人类视频学习。** WLA³、XPACE、ModAR、ReWeight共同说明，跨本体规模化的瓶颈越来越集中在“监督接口是否共享”。WLA³选择 latent world transition；XPACE共享视频世界模型并同时建模动作；ModAR让结构模态顺序生成后再预测动作；ReWeight则不改变核心策略接口，而是在 post-training 数据层面选择更接近机器人行为的人类样本。前三者改变模型内部的 world/action coupling，ReWeight改变数据进入 policy 的权重。

**3D/4D 与动作统一。** GeomVLA是本期最直接把 scene、motion、action 放进统一 3D 表示的工作。它与知域已收录 A4A 的区别也较清楚：A4A把人类示范中的未来 3D 点运动作为跨本体 4D affordance 预训练目标，而 GeomVLA把当前机器人场景提升到 3D 后预测 future scene trajectory，并让这一中间状态直接条件化动作生成。A4A 已在知域中收录。

**世界状态持久化。** AlayaVista与GLAM虽然任务一个是流式视觉生成、一个是导航，但都弱化“当前相机帧就是世界状态”这一假设。AlayaVista维护 panoramic latent；GLAM在历史 global map token 上预测未来空间记忆和 waypoint latent。一个强调可渲染状态，一个强调可导航的预测空间记忆。

**Feedforward Reconstruction。** FFVO并不是通用 3D 场景生成器，而是把 feedforward joint-reconstruction backbone 专门改造成长时程视觉里程计。其价值更多在 VGGT / π³ / feedforward reconstruction 路线的基础设施层：长视频几何不能只依赖逐帧位置回归，而需要局部到全局的时间聚合和显式轨迹监督。

**HOI 表示。** Single-Query Bimanual HOI关注 person-centric 2D结构化交互检测；JSSR关注 stereo geometry 下的 3D interaction field endpoint。它们都不等价于 HarmoHOI/StreamingHOI 一类动态交互生成，也没有直接恢复完整对象 mesh 或长期 4D interaction trajectory，因此更适合作为感知前端或监督接口，而非 4D HOI world model 本身。

**视频规划与具身导航。** CueNav继续验证了“先生成可视化未来，再由 embodiment-specific inverse dynamics 转成动作”的路线，并通过 BEV/global cue 给视频模型提供长程任务信息。其方法与 manipulation WAM 的技术接口高度相关，但当前证据来自导航，而不是手物操作。

## 证据审计

WLA³的主要实机结果较强：论文摘要报告最终 32D latent action 在 LARYBench 上为 67.89% 平均分类准确率，并在六个真实机器人任务上达到 81.9% 平均成功率，而 \(\pi_{0.5}\) 为 66.2%。但官方项目页面展示的 latent-action headline 数字为 70.75%，与 arXiv 摘要的 67.89% 不一致；在版本关系进一步澄清前，不应把两个数字混用。

XPACE在真实机器人上的平均成功率报告为 68.3%，高于论文中的 DreamZero 40.0% 和 GR00T 6.7%；模型生成 recovery data 后，实验中平均成功率还从 61.7% 提升到 86.7%。但其主要系统比较并非“仅改变 architecture”的严格控制实验：XPACE还使用额外 Stage-I 视频适配和异构经验。因此这些结果支持“完整训练方案有效”，不能单独归因于某一个 world-action architecture。

ModAR提供了本期较有价值的模态消融：tracks、DINO feature 和 depth 均有贡献，而进一步加入 RGB 没有稳定收益。不过作者也明确提醒，对 Flex-\(\pi\) 的 75% vs. 72% 比较属于系统级比较，两者参数规模和训练 FLOPs 差异很大，不能据此声称其架构本身在严格同预算条件下全面优于 Flex-\(\pi\)。

GeomVLA的 3D 表示实验具有直接相关性，但需要区分不同表中的训练设置：部分五任务实验与完整 50-task RoboTwin 训练并不完全同条件。论文中的 matched 2D-JA / 3D-JA 对照更能直接支持“显式 3D 表示有帮助”，而不是把所有跨系统表格都解释成纯结构优势。

AlayaVista同时在一致性、感知质量和相机可控性上报告改进，但部分指标存在 trade-off，例如其 translation error 并非所有基线中最好。训练使用 MUGEN 系列数据，而评测也使用 MUGEN-HQ 样本；当前正文核验没有看到足以支持“存在泄漏”的证据，但后续若以其数字作为 benchmark，应进一步确认视频级去重和训练/评测隔离策略。

ReWeight的实验支持“选择性使用人类数据优于直接随机混合”：仿真平均成功率由 robot-only 的 39% 和随机 human-robot mix 的 44% 提升到 57%，真实实验达到 68.8%。这支持 retrieval + weighting 在作者测试任务中的作用，但不能外推为所有人类视频天然可以无损转移到任意机器人。

IMPACT-VLA需要特别控制“反事实”措辞。它确实执行了闭环输入替换并重新 rollout，因此比静态特征敏感性分析更接近干预式 attribution；但它没有建立 structural causal model、没有完成因果可识别性证明，也不能把 intervention kernel 下的效果直接解释成现实世界中的已识别因果效应。其采样式 Shapley 分析还受到 rollout 随机性和替换输入是否处于策略训练分布内的影响。

One Model, Two Physical Stories的结论同样是“审计发现跨模态物理不一致”，而不是“训练出了因果世界模型”。其实验覆盖四类物理机制和 20 个设置，文本 probe 全部回答正确并不保证同一模型生成的视频遵守相同物理规律；但仿真基准本身也不是硬件世界的完整真值，作者明确承认其机制、模型系列和随机种子覆盖有限。

GLAM目前主要证据来自 HM3D 50% 子集上的受控复现。结果支持其完整系统相对复现 BSC-Nav 有更高成功率，但当前实验不足以单独证明“future-map prediction”就是全部增益来源，也不足以支持跨建筑、跨机器人本体的广泛泛化结论。

FFVO在 WOD、KITTI 和专有数据上支持长时轨迹解码的有效性，但其主要局限包括高速、极端天气、暗光以及长序列显存约束；同时 Sim(3) 对齐后的 ATE 和连续帧 RPE 不能完整揭示全局尺度漂移。

Single-Query Bimanual HOI的数据构建使用规则、VLM 辅助和人工核验，这使 person-centric supervision 可规模化，但也意味着部分训练标签继承伪标注误差。其结果支持结构化 person-query 对双手归属和交互关系检测有效，不等于已经解决度量 3D/4D HOI。

JSSR正文的消融支持 calibrated stereo candidate reasoning 对 interaction field estimation 有增益；但论文同时说明 challenge leaderboard 分数与主消融表使用不同训练设置，因此 leaderboard 名次不能直接当作同 checkpoint 的严格横向比较。

CueNav的导航结果支持 BEV/global visual cue 和 body-aware observation 对长程视频规划及跨本体部署有帮助，但其 video planner 推理代价、短预测 horizon 和有限历史上下文仍是扩展到持续 world model 的主要瓶颈。

## 对研究选题的影响

**对 3D/4D World Action Model：** GeomVLA与ModAR使“加入几何”本身的 novelty 门槛显著升高。更有空间的路线是 object/contact-centric persistent 4D state、跨时间身份保持、局部接触动力学、可执行 action grounding，以及让 3D/4D 状态成为长期 rollout 的稳定记忆，而不是单步附加条件。

**对人类视频学习具身策略：** WLA³、XPACE、ReWeight已经覆盖“学习共享 latent transition”“联合世界/动作建模”“检索与加权人类数据”三个方向。新工作的竞争点应进一步落到：如何自动判断人类数据中哪些 transition 在机器人上可执行、如何显式建模 embodiment mismatch，以及 3D/4D interaction/contact 是否比纯视觉相似度提供更可靠的迁移标准。

**对 StreamingHOI / 流式世界模型：** AlayaVista的全景 latent state 与按视口渲染机制提示，可以把高成本的“完整世界记忆”与高分辨率的“当前查询输出”解耦。若迁移到 HOI，可以考虑长期维护 object/hand/contact 的低频全局状态，只对当前交互区域生成高频几何或视频细节。

**对 HOI 感知前端：** Single-Query Bimanual HOI给出了 person-centric 双手绑定，JSSR提供 joint-conditioned stereo interaction endpoint。二者组合后，一个自然的新问题是：能否把“属于同一人的左右手 + 接触表面点 + 对象身份”沿时间维度提升为持久的 4D interaction graph，而不是逐帧检测。

**对世界模型因果研究：** IMPACT-VLA和物理一致性审计进一步说明，“counterfactual”一词已经被广泛用于输入替换、模拟 rollout 和 attribution。后续若要形成明确的 causal novelty，应把 intervention、causal identification、SCM 和 counterfactual inference 的层级写清楚，而不是仅把 action-conditioned rollout 或时间因果 attention 称为因果世界模型。

## 已收录且无重要变化

- **FIRE3D: Feed-forward Interactive 3D Scene Reconstruction Within A Minute** — 知域 ID：`arxiv-2609-08848`。知域已收录项目、代码、模型和数据入口，`updated_at` 为 2026-09-14；本次未核验到 2026-09-14 之后新的实质变化，因此排除原因：**知域已收录，本周期无实质更新**。
- **OpenWAM: An Open, Modular Exploration Towards Systematic World-Action Model Pretraining** — 知域 ID：`arxiv-2609-07398`。已有项目、代码及模型入口，本次未发现新的版本关系或资源首次开放事件；排除原因：**知域已收录，本周期无实质更新**。
- **FARM: Reading Failure Signals from the Internal Predictive States of a Frozen Robotic World Model** — 知域 ID：`arxiv-2609-11445`。已有代码入口且知域已于 2026-09-14 核验；排除原因：**知域已收录，本周期无实质更新**。
- **A4A: Cross-Embodiment Transfer of Action-Oriented 4D Affordances from Human Demonstrations** — 知域 ID：`arxiv-2609-05892`。已有项目和代码记录；排除原因：**知域已收录，本周期无实质更新**。
- **2AM: Grounding Agent-Side Memory as Guidance for Steerable Action Models in Long-Horizon Manipulation** — 知域 ID：`arxiv-2609-11308`。知域已有完整记录，本周期未核验到实质新增资源或版本变化；排除原因：**知域已收录，本周期无实质更新**。

其他原因排除的 5 条高相关外围线索为：Tele360（arXiv:2609.15032，实时前馈动态人体重建，但缺少交互/action/world-model 核心）；JEPLO（arXiv:2609.15770，JEPA/LiDAR locomotion，距离当前 HOI/WAM 主线较远）；DWMP（arXiv:2609.12347，偏 locomotion planning）；CLAW / Amortized Low-Rank Adaptation for Model-Based Reinforcement Learning（arXiv:2609.12278，通用 MBRL 适配）；CorrRisk-WM（arXiv:2609.16724，自动驾驶风险世界模型）。这些工作保留为外围观察项，但本期不进入正式新增。

## 待人工核验线索

无。进入正式列表的 13 篇论文均取得了可核验的 arXiv 原始论文入口，并完成正文或 arXiv HTML 核验；资源开放状态无法确认时直接标记为“未核验到”，没有据二手线索推断代码、数据或模型已经开放。

## 1. WLA³: World Latent Action Modeling for Semantics, Dynamics, and Kinematics

- **作者**：Peidong Liu, Zhiyuan Xiang, Mingyang Li, Wenhao Li, Jiale Zhang, Jiahao Sun, Jiawei Li
- **年份与发表**：2026，arXiv v1，2026-09-14 提交
- **arXiv ID**：2609.15870
- **DOI**：[10.48550/arXiv.2609.15870](https://doi.org/10.48550/arXiv.2609.15870)
- **代表图**：WLA³，Fig. 1，方法总览：从异构世界状态转移学习紧凑 latent action。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2609.15870v1/overview.png)

![WLA³ Fig. 1](https://arxiv.org/html/2609.15870v1/overview.png)
- **论文**：[arXiv](https://arxiv.org/abs/2609.15870)
- **正式出版**：未核验到
- **项目**：[WLA³ Project](https://wla-3.github.io/)
- **代码**：未核验到公开官方仓库
- **数据**：未核验到独立公开下载入口
- **模型**：未核验到公开权重入口
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.15870)
- **类别标签**：World Action Model, latent action, 人类视频, 跨本体迁移
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

### 当前挑战

异构机器人、人类第一视角视频与 UMI 数据使用不同动作空间，缺少可跨本体共享且噪声可控的动作监督，直接映射原生机械动作难以扩展。

### 研究动机

核心问题是异构机器人数据和海量人类第一视角视频缺少统一、低噪声的动作标签。WLA³不尝试把所有 embodiment 的原生 action 映射到同一个机械动作空间，而是把局部时间窗口中的**世界状态变化**编码为共享 latent action，再让机器人控制头把这种共享表示与本体动作共同预测。

最值得关注的是：它把 human-video scaling 的接口从“动作伪标签”转向“transition representation”。这与传统 action tokenizer 不同，因为 supervision 可以来自同步视觉变化以及可用的 embodiment-state change，而机器人轨迹负责把共享 latent grounding 到可执行动作。

### 技术方案

**输入**：同步相机观测、人类第一视角视频，以及数据中可用的机器人/身体状态变化。

**过程**：WLAM编码局部 world transition，形成紧凑的 32D local latent action 和更丰富的 transition feature；使用 partial-modality reconstruction 与 overlapping-window consistency 约束表示。随后这些表示分别进入 latent-action-conditioned dynamics、SLA 语义监督以及联合预测 latent action 与原生机器人控制的 action expert。

**输出**：跨本体 latent action、世界转移表征以及对应机器人的可执行动作。

### 实验结果

论文摘要报告 LARYBench 32D latent action 平均分类准确率 67.89%；六个 AgiBot G1 真实桌面任务中，WLA³平均成功率为 81.9%，\(\pi_{0.5}\) 为 66.2%。训练数据从约 5K 小时增加到 20K 小时时，实机平均成功率由 57.6% 上升到 81.9%；累计消融中，基础版本 72.1%，加入 LAC-WM 后 76.3%，进一步加入 LARA 为 79.8%，最终加入 SLA 达 81.9%。

官方项目还列出约 84.1K 小时聚合数据，包括约 53,874 小时 human、14,151 小时 real robot、11,676 小时 simulation 和 4,393 小时 UMI 数据。需要注意，项目页面当前显示 LARYBench headline 为 70.75%，与 arXiv 摘要的 67.89% 不一致，应等待作者澄清具体 checkpoint/评测版本。

### 代码与数据

项目页已公开，但本次未核验到稳定的官方训练代码、可下载数据集或模型权重入口。项目页面的资源状态不应被等同于完整可复现发布。

### 局限、失败案例与开放问题

实机证据集中在六个桌面操作任务，尚不足以证明 latent action 对广泛机器人本体、移动操作、长程任务或互联网规模人类视频都具有相同可迁移性。项目页和论文摘要的 latent-action 数字不一致也是当前复核时需要保留的版本风险。

### 总结讨论

这是本期对“**从人类视频学习具身 WAM**”最直接的工作之一。它与 A4A 的 4D affordance 路线形成有意义对照：A4A显式使用未来 3D 点运动，WLA³使用更抽象的 world-transition latent。后续研究可以直接比较这种抽象 latent 与显式 3D/4D interaction state 在跨本体可执行性上的差异。

## 2. XPACE: Joint World and Action Modeling from Heterogeneous Experience

- **作者**：Jiacheng Wei, Jerry Bai, Xiaoyu Yue, Zidong Wang, Xiaoyang Guo, Cheng Chen, Fanqi Pu, Fan Wu, Zhixu Yue, Yizhuo Li, Feng Qiu, Bo Liu, Yuying Ge, Hui Zhou, Chenyi Chen, Yixiao Ge
- **年份与发表**：2026，arXiv v1，2026-09-15 提交
- **arXiv ID**：2609.17372
- **DOI**：[10.48550/arXiv.2609.17372](https://doi.org/10.48550/arXiv.2609.17372)
- **代表图**：XPACE，Fig. 1，统一 world-action policy 与 action-conditioned simulator。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2609.17372v1/teaser.png)

![XPACE Fig. 1](https://arxiv.org/html/2609.17372v1/teaser.png)
- **论文**：[arXiv](https://arxiv.org/abs/2609.17372)
- **正式出版**：未核验到
- **项目**：未核验到稳定官方项目页
- **代码**：未核验到官方公开仓库
- **数据**：未核验到
- **模型**：未核验到
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.17372)
- **类别标签**：World Action Model, world simulator, 人类视频, self-improvement
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

### 当前挑战

无动作视频、带动作的人类轨迹与机器人示范通常由不同模型或训练阶段割裂处理，世界预测难以直接反哺策略，并容易在偏离专家分布后失效。

### 研究动机

XPACE把 world-action policy 与 world simulator 合并进共享视频 backbone。无动作视频负责学习视觉动态；带动作的人类和机器人轨迹共同提供视频与动作 supervision。模型随后不只预测动作，还能以给定动作模拟视觉后果，并利用自己的 simulator 构造偏离专家轨迹后的 recovery experience。

关键 Insight 是把 world model 从辅助 loss 提升为**可生成新 policy training data 的闭环组件**。

### 技术方案

**输入**：无动作视频、带动作的人类演示、机器人演示，以及部署时当前视觉/任务上下文。

**过程**：先以大规模视频学习 visual dynamics，再联合训练 future video 与 robot action；采用 coarse-to-fine curriculum逐渐提高机器人控制比重。world simulator进一步适配自己的 generated context，在专家轨迹附近生成 deviation-recovery rollout，过滤后用于 policy fine-tuning。

**输出**：可执行机器人动作，以及指定动作条件下的未来视频模拟。

### 实验结果

XPENG IRON 真实机器人实验中，论文报告 XPACE 平均成功率 68.3%，DreamZero 为 40.0%，GR00T 为 6.7%；对应 progress 指标约 0.84、0.68、0.36。需要注意，监督机器人/人类 corpus虽进行了匹配，但 XPACE额外使用 Stage-I video adaptation，因此该表支持的是完整系统方案，而非纯 architecture-controlled 胜负。

使用 simulator 生成恢复数据进行 self-improvement 后，平均 progress 从 0.81 提升至 0.93，成功率从 61.7% 提升到 86.7%；其中 water-pouring 任务由 50% 提升到 95%。

### 代码与数据

本次未核验到稳定官方代码、模型或数据下载入口，因此不根据第三方索引声称其已经开源。

### 局限、失败案例与开放问题

完整方案同时变化数据、预训练和架构，导致部分对比难以隔离“共享 world/action architecture”本身的贡献。simulation-generated recovery 是否会在更长 horizon 下累积模型偏差、过滤器如何处理错误但视觉上合理的 trajectory，也仍是核心开放问题。

### 总结讨论

XPACE与 Dyna、OpenWAM、FlowWAM 等路线高度相关，但增加了一个重要闭环：**世界模型自己生成 recovery supervision**。它值得与显式 3D/4D simulator 或 contact-aware world model结合，以研究视频上看似合理的恢复轨迹是否真的物理可执行。

## 3. Modality-Autoregressive World-Action Models

- **作者**：Adam Hung, Bardienus P. Duisterhof, Deva Ramanan, Jeffrey Ichnowski
- **年份与发表**：2026，arXiv v1，2026-09-15 提交
- **arXiv ID**：2609.17524
- **DOI**：[10.48550/arXiv.2609.17524](https://doi.org/10.48550/arXiv.2609.17524)
- **代表图**：ModAR，Fig. 1，按模态顺序预测未来观测后再预测动作。arXiv HTML 无 PNG 直链，图下载自论文源文件 `figures/teaser.pdf`。来源：[Fig. 1 本地 WebP](content/images/2609.17524-representative.webp)

![ModAR Fig. 1](content/images/2609.17524-representative.webp)
- **论文**：[arXiv](https://arxiv.org/abs/2609.17524)
- **正式出版**：未核验到
- **项目**：[ModAR Project](https://adamhung60.github.io/ModAR/)
- **代码**：项目页标记 “coming soon”
- **数据**：未核验到独立公开入口
- **模型**：未核验到
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.17524)
- **类别标签**：World Action Model, 多模态预测, 3D/几何, 人类视频
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

### 当前挑战

现有 WAM 常默认先生成未来 RGB，但高成本像素预测未必保留最有利于控制的运动、几何和语义信息，也难利用缺少完整模态标注的异构数据。

### 研究动机

ModAR直接挑战“WAM 应该先生成未来 RGB”的默认设计。模型按顺序预测 point tracks、DINO feature、depth 等未来模态，后面的模态条件在前面已经生成的结构信息上，最后才预测动作。作者的实验结论是：tracks、DINO 和 depth 在其设定中均有贡献，但加入未来 RGB 没有稳定额外收益。

### 技术方案

**输入**：视觉观测、任务信息及 action-labeled / actionless demonstrations。

**过程**：以 modality-autoregressive diffusion/denoising 顺序生成结构化未来模态，例如 point tracks → DINO feature → depth，再基于这些预测状态生成动作；不同模态可以使用不同监督数据。

**输出**：多个未来世界模态和机器人动作。

### 实验结果

六个 RoboTwin 任务分别研究 50、250、1250 条总演示，其中基础 robot action-labeled 数据保持为 50 条，其余可加入 actionless 数据。在 250 条数据规模下，ModAR平均成功率 75%，Flex-\(\pi\) 为 72%。不过作者明确把该结果定义为系统级比较：ModAR约 30.1M 参数，而 Flex-\(\pi\) 约 6B，并存在约 20× 训练 FLOPs 差异。

完整模态版本平均为 75%；去除 context noise 后 63%，反转模态顺序约 65%，移除 tracks 约 61%，移除 DINO feature 约 65%，移除 depth 约 70%，去掉 RGB 则没有下降。完整推理约 147.9 ms，即约 6.76 Hz，测试硬件为 RTX 5090。

三个真实双臂任务上，100 robot demos 的平均结果约 70%；加入 200 个 in-domain human demos 后为 81.1%，再加入约 1000 个 EgoDex OOD human demos 后为 83.3%。

### 代码与数据

官方项目页存在，但代码当前标记为 “coming soon”；本期不将其记为已开源。

### 局限、失败案例与开放问题

论文明确指出任务数量有限、任务标签仍是离散类别、模态顺序需要更系统探索，且 sequential modality generation 带来延迟；当前数据规模也不足以回答互联网级人类视频扩展性。

### 总结讨论

这是对 WAM“世界状态应该是什么”的直接实验。对计划研究 3D/4D WAM 的路线而言，它意味着必须把 tracks/depth/semantic feature 作为强 baseline，而不能只和 RGB-video WAM 比较。

## 4. GeomVLA: Unifying Scene, Motion, and Action in 3D

- **作者**：Ziyin Xiong, Nikos Gkanatsios, Moritz Reuss, Katerina Fragkiadaki
- **年份与发表**：2026，arXiv；作者页面标注 CoRL 2026
- **arXiv ID**：2609.13812
- **DOI**：[10.48550/arXiv.2609.13812](https://doi.org/10.48550/arXiv.2609.13812)
- **代表图**：GeomVLA，Fig. 1，在共享 3D 空间连接感知、未来场景运动与机器人控制。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2609.13812v1/teaser_new4.png)

![GeomVLA Fig. 1](https://arxiv.org/html/2609.13812v1/teaser_new4.png)
- **论文**：[arXiv](https://arxiv.org/abs/2609.13812)
- **正式出版**：CoRL 2026 状态已由作者材料核验，正式 proceedings DOI 本次未核验到
- **项目**：[GeomVLA Project](https://ziyin-xiong.github.io/geomvla.io/)
- **代码**：项目页提供代码按钮，但本次访问目标返回 404，故不记为可用开源代码
- **数据**：使用公开/基准机器人数据，未核验到独立新数据发布
- **模型**：未核验到公开权重
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.13812)
- **类别标签**：3D VLA, 3D/4D, World Action Model, scene motion
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

### 当前挑战

以 2D 图像特征连接视觉、未来运动与机器人动作时，跨视角几何和场景点运动缺少统一坐标语义，容易造成世界预测与动作生成之间的表示错位。

### 研究动机

GeomVLA把视觉、未来场景运动和动作统一到显式 3D 坐标系。视觉语言特征先通过 depth 与 calibration lift 到 3D；随后 task-conditioned 3D Scene Trajectory Denoiser 预测场景点的未来运动，其 latent 再条件化机器人 action denoiser。

关键区别在于中间 prediction target 不是 RGB，也不是抽象隐藏状态，而是具有物理坐标语义的未来 3D motion。

### 技术方案

**输入**：多视角或相机观测、深度/标定、语言任务和机器人状态。

**过程**：视觉/VLM 特征 lift 到 3D；预测未来 3D scene trajectory；将预测 motion latent 注入 3D flow-based action denoiser。

**输出**：任务相关的未来 3D 场景运动以及机器人控制动作。

### 实验结果

官方结果包括 CALVIN 4.624、LIBERO 98.4% 以及 RoboTwin/真实任务结果。在更有解释价值的 matched 2D-JA 与 3D-JA 对照中，CALVIN 分别约 4.195 与 4.508，五任务 RoboTwin 为 66.2% 与 81.6%，真实机器人为 28.8% 与 59.4%，直接支持显式 3D 表示在这些设置中的作用。

但不同表格的训练任务范围不完全一致：完整 GeomVLA与 \(\pi_{0.5}\) 使用 50 个 RoboTwin 任务训练，而某些消融只使用五任务数据，因此不应将所有数字混合成严格同条件架构比较。

### 代码与数据

官方项目页存在，但本次核验时项目中的代码链接返回 404，因此当前不能认定代码已经可用。

### 局限、失败案例与开放问题

模型依赖 depth 与 calibration，输入几何误差会直接传播到 3D representation。当前实验仍集中在 benchmark-scale robot demonstrations，尚未验证大规模人类视频、强 cross-embodiment 或长期 object permanence。

### 总结讨论

这是本期最直接对应“结合 3D/4D 信息的具身 WAM/VLA”的论文之一。它显著提高了未来研究的 baseline：后续仅称“3D-aware VLA”已经不够，应进一步体现 temporal persistence、interaction/contact 或跨 embodiment 4D state 的新价值。

## 5. AlayaVista: Streaming World Modeling from Panoramic States to Perspective Video

- **作者**：Jiaming Tan, Mingliang Zhai, Zhen Li, Yuwei Wu, Chuanhao Li, Kaipeng Zhang
- **年份与发表**：2026，arXiv v1，2026-09-13 提交
- **arXiv ID**：2609.14462
- **DOI**：[10.48550/arXiv.2609.14462](https://doi.org/10.48550/arXiv.2609.14462)
- **代表图**：AlayaVista，Fig. 1，由全景 latent state 查询并渲染当前透视视口。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2609.14462v1/teaser.png)

![AlayaVista Fig. 1](https://arxiv.org/html/2609.14462v1/teaser.png)
- **论文**：[arXiv](https://arxiv.org/abs/2609.14462)
- **正式出版**：未核验到
- **项目**：[AlayaVista Project](https://alaya-lab.github.io/AlayaVista/)
- **代码**：[GitHub](https://github.com/AlayaLab/AlayaVista)
- **数据**：论文构建 MUGEN；本次未确认独立公开下载入口
- **模型**：未核验到公开权重
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.14462)
- **类别标签**：流式生成, World Model, panoramic state, 视频生成
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

### 当前挑战

透视视频流只能观察当前视口；相机离开后，视野外内容容易从模型状态中消失，而持续生成完整高分辨率全景又带来过高计算成本。

### 研究动机

AlayaVista针对流式交互视频中的 off-screen memory 问题，将“世界状态”和“当前视口”解耦：由单张透视图先扩展出 360° scene prior，随后在 panoramic latent space 中持续更新世界，再根据相机轨迹查询当前 perspective viewport。

这避免了始终生成完整高分辨率全景视频，同时又让离开视野的场景内容保留在全局 latent 中。

### 技术方案

**输入**：单张 perspective image 与后续相机控制。

**过程**：预训练 panorama expansion 构造 360° ERP prior；camera-conditioned panoramic latent generator 持续更新世界状态；latent viewport renderer从全局状态抽取当前视野；deterministic latent upsampler 与 perspective generative refiner恢复细节。生成器采用 chunk-autoregressive/causal 机制，并使用 few-step distillation 降低流式推理成本。

**输出**：相机可控、连续的 perspective RGB video。

### 实验结果

论文构建 MUGEN：约 1,318 小时、至少 4K 分辨率、6,446 段来源视频，并附加相机、深度和实例等标注。评测使用 200 个 MUGEN-HQ case、每个 81 帧、1024×576。AlayaVista报告 SSIM 0.4616、LPIPS 0.5321、一致性 0.9240、质量 0.5579、动态性 0.9200、PSNR 14.10，rotation error 2.132；大多数感知/一致性指标占优，但 translation error 0.03312 并非所有比较中最佳。

### 代码与数据

论文 HTML 的官方资源区提供 AlayaLab/AlayaVista GitHub 仓库入口，因此代码入口可确认。

### 局限、失败案例与开放问题

论文没有集中列出完整 limitations section。根据架构可明确识别的一项风险是：初始 perspective-to-panorama expansion 必然需要生成不可见区域，因此世界状态起点包含 hallucinated content。另一个需后续核验的问题是 MUGEN/MUGEN-HQ 的视频级训练—评测去重方式；本报告没有发现泄漏证据，因此这里只作为审计问题，不作为负面结论。

### 总结讨论

它与 StreamingHOI 的任务对象不同，但对“流式世界状态如何长期保存”非常 relevant。尤其值得尝试把 panoramic latent 的思想替换为 object-centric / interaction-centric 4D memory，再按当前手物交互区域生成高频局部状态。

## 6. ReWeight: Leveraging Human Data for VLA Post-Training via Demonstration Retrieval and Sample Weighting

- **作者**：Chenwei Wang, Dianye Huang, Match W. L. Ko, Chenjia Bai, Zhongliang Jiang
- **年份与发表**：2026，arXiv v1，2026-09-12 提交
- **arXiv ID**：2609.13851
- **DOI**：[10.48550/arXiv.2609.13851](https://doi.org/10.48550/arXiv.2609.13851)
- **代表图**：ReWeight，Fig. 1，检索人类示范并为 VLA post-training 分配样本权重。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2609.13851v1/figures/fig1.png)

![ReWeight Fig. 1](https://arxiv.org/html/2609.13851v1/figures/fig1.png)
- **论文**：[arXiv](https://arxiv.org/abs/2609.13851)
- **正式出版**：未核验到
- **项目**：[ReWeight Project](https://reweight-vla.github.io/)
- **代码**：未核验到官方公开仓库
- **数据**：未核验到新增数据发布
- **模型**：未核验到
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.13851)
- **类别标签**：VLA, 人类视频, cross-embodiment, post-training
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

### 当前挑战

人类与机器人在形态、视角和动作可达性上存在系统差异，随机混合人类示范可能引入不可执行行为，数据规模增加并不必然改善目标机器人策略。

### 研究动机

论文的出发点不是“更多人类数据一定更好”，而是 cross-embodiment mismatch 会让随机混入的人类数据伤害或限制 policy post-training。ReWeight先学习包含 visual observation 与 future action 的跨本体 visuomotor representation，再通过 optimal transport 找到与目标机器人数据行为相近的人类 demonstrations，并给 discrepancy 较小的 sample 更大训练权重。

### 技术方案

**输入**：目标机器人 demonstrations、候选 egocentric human demonstrations、VLA policy。

**过程**：编码未来行为相关的跨本体 visuomotor representation；使用 optimal transport 做 demonstration retrieval；根据人类—机器人 sample discrepancy 分配 loss weight；对 VLA 做 post-training。

**输出**：利用筛选后人类经验增强的目标机器人策略。

### 实验结果

在八个 RoboTwin 2.0 仿真任务中，\(\pi_{0.5}\) robot-only 平均成功率 39%，随机 human+robot mix 为 44%，ReWeight 为 57%。四个真实 DoBot 双臂任务上，ReWeight 平均成功率 68.8%；在加入随机化、光照和干扰因素的设置中仍显著优于基线。

### 代码与数据

项目页可访问，但本次没有核验到官方代码、数据或权重下载入口。

### 局限、失败案例与开放问题

当前证据说明 retrieval/weighting 在作者测试的任务与机器人中有效，但“相似度”仍依赖目标机器人数据来定义。如何在目标机器人 demonstrations 极少甚至为零时判断人类行为的可迁移性，是比继续扩大视频池更关键的问题。

### 总结讨论

这篇对“从人类视频学习”路线很有实用价值，也可与 A4A/WLA³互补：A4A寻找 geometry-level transferable target，WLA³学习 transition latent，ReWeight则解决**哪些 human samples 值得进入训练**。三者组合是值得实验的路线。

## 7. IMPACT-VLA: Interaction-aware Multimodal Propagation Attribution via Counterfactual Trajectories for Vision-Language-Action Policies

- **作者**：Jinwoong Kim, Sangjin Park
- **年份与发表**：2026，arXiv v1，2026-09-14 提交
- **arXiv ID**：2609.15005
- **DOI**：[10.48550/arXiv.2609.15005](https://doi.org/10.48550/arXiv.2609.15005)
- **代表图**：IMPACT-VLA，Fig. 1，基于闭环反事实轨迹的阶段化多模态归因框架。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2609.15005v1/figures/fig1_framework.png)

![IMPACT-VLA Fig. 1](https://arxiv.org/html/2609.15005v1/figures/fig1_framework.png)
- **论文**：[arXiv](https://arxiv.org/abs/2609.15005)
- **正式出版**：未核验到
- **项目**：未核验到
- **代码**：未核验到
- **数据**：使用 LIBERO
- **模型**：基于 OpenVLA-OFT；无新增权重发布得到核验
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.15005)
- **类别标签**：VLA, counterfactual attribution, intervention, 因果审计
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

### 当前挑战

静态特征敏感性或单步遮蔽无法反映多模态信息在闭环执行中的跨阶段传播、恢复和交互，因而难以定位视觉、语言与本体感知何时真正影响成功。

### 研究动机

IMPACT-VLA研究的不是训练更强策略，而是解释视觉、语言和 proprioception 在**哪个执行阶段**对任务成功真正重要。它先从成功参考轨迹中建立 behavioral phases，再把 phase × modality 作为 attribution block，通过闭环重新执行替换后的输入，观察改变如何沿后续状态和动作传播。

### 技术方案

**输入**：成功参考 rollout、待解释 policy、视觉/语言/本体感知等模态。

**过程**：按 action transition 分割 behavioral phase；与 policy query boundary 对齐；对 phase-modality block 做 closed-loop replacement；执行新的轨迹；以 sampled Shapley 和 cross-phase interaction 分析各 block 对最终成功的影响，并区分 behavioral recovery 与 functional recovery。

**输出**：阶段化模态贡献、跨阶段交互以及干预后的 counterfactual trajectory。

### 实验结果

在 30 个 LIBERO manipulation tasks、OpenVLA-OFT 上，25/30 个任务即 83.3% 出现 dominant-modality transition。对负交互 pair，早期 block 被替换时，后期 block 的 marginal gain 约提高 3.3×；作者还报告不同 intervention kernel 下的 attribution ranking 具有一定稳定性。

### 代码与数据

本次没有核验到官方代码或项目发布。

### 局限、失败案例与开放问题

论文采用真实闭环重新执行，因此属于有意义的 intervention-based attribution；但它不是 causal identification，也没有结构因果模型。输入替换可能造成策略训练分布之外的状态，且 sampled permutations 的 rollout 随机性限制了对很小 attribution 差异的解释。

### 总结讨论

它适合加入知域“因果/反事实世界模型”的**审计工具层**，但应与 Causal-JEPA、SCM、intervention identification 等模型层工作分开。其最大价值是提供一种检查多模态 VLA temporal dependency 的实验协议。

## 8. One Model, Two Physical Stories: Auditing Misalignment in Multi-Modal World Modeling

- **作者**：Geigh Zollicoffer, Minh Vu, Rajiv Ranasinghe, Manish Bhattarai
- **年份与发表**：2026，arXiv v1，2026-09-13 提交
- **arXiv ID**：2609.14833
- **DOI**：[10.48550/arXiv.2609.14833](https://doi.org/10.48550/arXiv.2609.14833)
- **代表图**：One Model, Two Physical Stories，Fig. 1，同一场景下文本物理、视频生成与仿真参考的不一致。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2609.14833v1/figures/fig1_illustration_paper.png)

![One Model, Two Physical Stories Fig. 1](https://arxiv.org/html/2609.14833v1/figures/fig1_illustration_paper.png)
- **论文**：[arXiv](https://arxiv.org/abs/2609.14833)
- **正式出版**：未核验到
- **项目**：未核验到
- **代码**：未核验到
- **数据**：实验使用构造的物理机制与模拟设置；未核验到独立数据发布
- **模型**：未核验到
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.14833)
- **类别标签**：World Model, 物理一致性, intervention, counterfactual audit
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

### 当前挑战

多模态模型可能在文本中正确描述物理规律，却生成违反同一规律的视频；仅分别评测语言推理或视频质量无法发现这种模型内部跨模态不一致。

### 研究动机

论文指出多模态 world model 可能同时讲出“两套物理故事”：文本推理得到正确的弹跳、碰撞或运动关系，但同一模型的视频生成却违反该关系。作者定义 internal misalignment——模型自己的语言/物理 contract 与视频不一致，以及 external misalignment——视频与解析/模拟物理环境不一致。

### 技术方案

**输入**：物理初始条件、模型文本预测、模型视频生成和解析/模拟物理参考。

**过程**：把机制拆成 event、magnitude、timing contract；构造由弱到强的 intervention ladder；逐步向模型提供自身 contract 或修正的 physical contract；检查视频行为是否随干预回到一致物理结果。

**输出**：内部/外部物理一致性测量以及干预后变化。

### 实验结果

实验覆盖四种 physical mechanisms 和 20 个 settings。论文报告 22/22 个文本 physics probes 得到与参考环境一致的回答，但 neutral video 经常与这些文本答案或模拟物理不一致。这直接支持“语言物理知识正确 ≠ 视频 world model 执行相同物理规律”。

### 代码与数据

本次未核验到公开代码或独立数据集。

### 局限、失败案例与开放问题

作者明确指出，Isaac/PhysX 环境并不等同于真实硬件物理；实验只覆盖一个模型系列、四类机制和有限随机种子。因此当前结果支持“存在可复现的跨模态 misalignment”，而不是所有多模态模型都必然存在同样幅度的物理错误。

### 总结讨论

对世界模型路线很重要，因为它提供了比 PSNR/FVD 更直接的**物理一致性审计**。它使用 intervention，但不是 causal identification。后续可以将类似 contract test 扩展到 HOI 中的接触、摩擦、遮挡后物体状态和反事实动作。

## 9. GLAM: Training a Latent World Model over Global Spatiotemporal Memory for Active Exploration and Navigation

- **作者**：I-Tak Ieong, Ruizhi Feng, Zhaoyang Lu, Yifei Cao, Jiayao Zhao, Leon Li, Senhua Zhu, Wenbo Ding
- **年份与发表**：2026，arXiv v1，2026-09-13 提交
- **arXiv ID**：2609.14561
- **DOI**：[10.48550/arXiv.2609.14561](https://doi.org/10.48550/arXiv.2609.14561)
- **代表图**：GLAM，Fig. 2，基于全局时空记忆的 latent world model 导航架构。来源：[Fig. 2 原图 PNG](https://arxiv.org/html/2609.14561v1/figs/GLaM_Nav.png)

![GLAM Fig. 2](https://arxiv.org/html/2609.14561v1/figs/GLaM_Nav.png)
- **论文**：[arXiv](https://arxiv.org/abs/2609.14561)
- **正式出版**：未核验到
- **项目**：未核验到稳定官方项目入口
- **代码**：未核验到
- **数据**：使用 Habitat / HM3D v0.2
- **模型**：未核验到公开权重
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.14561)
- **类别标签**：latent world model, 长时记忆, active exploration, navigation
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

### 当前挑战

主动探索和导航依赖跨时间累积的全局空间状态，当前 RGB 或局部地图不足以表达未来可达区域和长期目标，像素预测又不是规划所需的最直接接口。

### 研究动机

GLAM将世界模型的预测对象从 RGB 改成 global spatiotemporal map memory。给定历史 map tokens、目标和当前 pose，模型同时预测 future map representation 与 robot-centric waypoint latent；采用 JEPA-like latent prediction，而非像素重建。

### 技术方案

**输入**：历史 global map tokens、navigation goal、当前机器人 pose。

**过程**：latent world model预测未来地图状态和 waypoint representation；预训练 waypoint encoder/decoder负责将规划 latent 映射回可执行导航 waypoint。

**输出**：未来空间记忆 latent 和机器人导航 waypoint。

### 实验结果

训练轨迹来自 Habitat HM3D v0.2 上的 ObjectNav expert replay，并切成多时间尺度 prediction samples。在论文的 50% HM3D subset reproduction 设置中，BSC-Nav约为 78.50% SR / 47.70 SPL，GLAM NAV约为 86.89% SR / 48.35 SPL。成功率提升明显，但 SPL 提升较小，因此不能仅据此声称路径效率获得同幅度改善。

### 代码与数据

本次未核验到新的官方代码或模型发布。

### 局限、失败案例与开放问题

目前主要量化实验是 benchmark 子集复现；尚缺乏充分组件消融来单独隔离 future-map prediction 的贡献。真实办公室展示具有可行性，但不是多建筑、多本体统计评测。

### 总结讨论

GLAM对 egocentric world model 的价值在于长期 memory representation。若把 global map token 替换成 object/contact-centric 3D/4D memory，可能形成更接近 manipulation world model 的持续状态表示。

## 10. FFVO: A Feedforward Pose Decoder for Long-Horizon Visual Odometry

- **作者**：Meng-Li Shih, Shih-Yang Su, Yuliang Zou, Hao Xiang, Haidong Zhu, Vincent Casser, Brian Curless, Dmitry Kalenichenko, Mingxing Tan, Dragomir Anguelov
- **年份与发表**：2026，arXiv v1，2026-09-12 提交
- **arXiv ID**：2609.13733
- **DOI**：[10.48550/arXiv.2609.13733](https://doi.org/10.48550/arXiv.2609.13733)
- **代表图**：FFVO，Fig. 3，冻结 π³ 骨干与可训练 camera-token / local-to-global pose decoder。来源：[Fig. 3 原图 PNG](https://arxiv.org/html/2609.13733v1/images/method_overview.png)

![FFVO Fig. 3](https://arxiv.org/html/2609.13733v1/images/method_overview.png)
- **论文**：[arXiv](https://arxiv.org/abs/2609.13733)
- **正式出版**：未核验到
- **项目**：未核验到
- **代码**：未核验到
- **数据**：WOD、KITTI 及 proprietary benchmark
- **模型**：未核验到
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.13733)
- **类别标签**：Feedforward Reconstruction, visual odometry, 3D/4D, long-horizon
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

### 当前挑战

前馈联合重建模型扩展到长视频时，全局聚合全部图像 token 的开销迅速增长，逐帧位姿回归又难同时保持局部运动精度与长程轨迹一致性。

### 研究动机

FFVO将 feedforward joint reconstruction backbone 专门改造成长时程 camera-pose decoder。它使用紧凑 camera tokens 避免对长视频中全部 image tokens 做昂贵全局聚合，并将时间建模拆为 local motion aggregation 与 global sequence integration。

### 技术方案

**输入**：长视频单目图像序列。

**过程**：feedforward reconstruction backbone提取视觉/几何表示；compact camera token 汇总每帧相机状态；hierarchical local-to-global temporal decoder处理短程运动和长程一致性；中间 trajectory supervision 稳定训练。

**输出**：完整长序列相机轨迹。

### 实验结果

在作者消融中，finetuned \(\pi^3\) 的 ATE/RPE-translation/RPE-rotation 约为 15.989 / 8.452 / 0.596；加入 camera token 后为 11.776 / 5.509 / 0.379；再加 auxiliary supervision 为 11.195 / 5.354 / 0.373；使用 local temporal structure 后降至 7.070 / 1.090 / 0.289，增加 token 数后进一步小幅改善至 7.060 / 1.070 / 0.281。

### 代码与数据

论文使用 WOD、KITTI 与 13,140 个 100-frame proprietary sequences；本次未核验到官方代码或模型权重发布。

### 局限、失败案例与开放问题

论文明确讨论高速超过约 55 mph、极端天气和低光环境困难；FFVO-Long仍因显存限制采用 segment-wise post-optimization。Sim(3)-aligned ATE 与连续 RPE 也可能低估尺度不一致和长期漂移；正文没有给出足够完整的 latency/throughput/memory benchmark。

### 总结讨论

FFVO不是生成式 world model，但直接属于 Feedforward Reconstruction 基础路线。对 DynamicVGGT/Gen3R 类模型向长视频或 4D 扩展时，它的 hierarchical temporal pose decoder 是值得比较的基础组件。

## 11. Single-Query Person-Centric Bimanual Hand-Object Interaction Detection

- **作者**：Jonghyun Kim, Junho Roh, Yubin Yoon, Hyotae Lee, Jongkuk Park, Taehwan Hwang, Jaechul Kim, Jungho Lee
- **年份与发表**：2026，arXiv；arXiv comment 标注 Accepted to ECCV 2026
- **arXiv ID**：2609.12155
- **DOI**：[10.48550/arXiv.2609.12155](https://doi.org/10.48550/arXiv.2609.12155)
- **代表图**：Single-Query Bimanual HOI，Fig. 2，person-centric query 同时预测人体、双手与交互目标。来源：[Fig. 2 原图 JPG](https://arxiv.org/html/2609.12155v1/figures/oih_architecture.jpg)

![Single-Query Bimanual HOI Fig. 2](https://arxiv.org/html/2609.12155v1/figures/oih_architecture.jpg)
- **论文**：[arXiv](https://arxiv.org/abs/2609.12155)
- **正式出版**：ECCV 2026 接收状态已由 arXiv comment 核验；正式 proceedings DOI 本次未核验到
- **项目**：[Project](https://lgecto-ail-vil.github.io/SingleQuery-BHOI/)
- **代码**：未核验到稳定官方公开仓库
- **数据**：论文构建 COCO-based person-centric bimanual interaction annotations
- **模型**：未核验到公开权重
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.12155)
- **类别标签**：HOI, 双手交互, person-centric, structured detection
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

### 当前挑战

逐手检测在多人和双手交互场景中容易丢失人体归属、左右手结构以及每只手的交互对象，局部检测正确也不保证完整 person-centric 关系正确。

### 研究动机

传统 hand-centric HOI detector把每只手独立检测，容易在多人场景中丢失“左右手属于哪个人”的关系。该工作改成 one-query-per-person：单个 query同时输出 human box、body pose、左右手框与状态，并为每只手关联 interaction target。

### 技术方案

**输入**：单张包含一个或多个人的 RGB 图像。

**过程**：person query通过 part-aware deformable attention访问人体、手和姿态区域；同一 query预测 person/pose/hand structure；hand-to-query relationship matrix 让每只手从已检测 person/object query 及 off token 中选择交互目标。

**输出**：完整 person-centric 双手结构、hand state 及 hand-object target association。

### 实验结果

论文构建 COCO-based 数据，并与 Hands23 等来源对齐；约 2K COCO validation 图像增加人工 person-centric annotation。对训练标签，作者进行了 VLM-assisted verification 与人工 audit：770 个样本检查中规则错误率由约 2.5% 降至 2.1%，500 个 double-label 样本人工一致率约 98.4%。

在无 pose 的直接比较中，相比 DirectBox，检测 mAP大致接近（49.1 vs 48.8），但中等严格度 interaction 指标约从 44.9 提升到 60.8，hard 指标从 12.6 提升到 28.9，支持 person-centric relation modeling 对完整双手交互关系的贡献。

### 代码与数据

项目页已公开，但本次没有核验到可用的官方训练代码或权重发布。

### 局限、失败案例与开放问题

失败仍集中在模糊、小尺度、严重遮挡和深度关系困难的手/物体；训练标签部分来自规则与 VLM 辅助，因此存在残余伪标注误差。更重要的是，该工作解决的是 2D structured interaction detection，不是 metric 3D/4D HOI。

### 总结讨论

它为 HarmoHOI/StreamingHOI 类长期交互建模提供了一个更合理的结构单位：**person + two hands + targets**，而不是独立 hand track。后续可进一步增加跨帧 identity、3D contact 和 object motion。

## 12. Joint-Conditioned Stereo Surface Reasoning for Interaction Field Estimation

- **作者**：Yanlin Jin, Yifan Yang, Bowen Yang, Kai Zhu
- **年份与发表**：2026，arXiv v1，2026-09-07 提交
- **arXiv ID**：2609.06955
- **DOI**：[10.48550/arXiv.2609.06955](https://doi.org/10.48550/arXiv.2609.06955)
- **代表图**：JSSR，Fig. 1，关节条件的双目表面候选搜索与 interaction field 估计。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2609.06955v1/jssr.png)

![JSSR Fig. 1](https://arxiv.org/html/2609.06955v1/jssr.png)
- **论文**：[arXiv](https://arxiv.org/abs/2609.06955)
- **正式出版**：未核验到
- **项目**：未核验到
- **代码**：未核验到
- **数据**：基于 SHOW3D Interaction Field 相关数据/评测
- **模型**：未核验到
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.06955)
- **类别标签**：3D HOI, interaction field, stereo geometry, contact reasoning
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

### 当前挑战

仅靠单目或直接回归难以稳定估计每个手部关节最近的物体表面点，遮挡、深度歧义和逐关节独立预测会削弱接触邻域的几何一致性。

### 研究动机

JSSR把 interaction field 重新表述为：对每个 hand joint，找到其最近 object-surface endpoint。不同关节需要自己的 endpoint，但同一只手的关节可以共享局部 surface evidence。因此模型把 learned direct prediction 与显式 stereo geometry candidate search 结合。

### 技术方案

**输入**：七个时间步的同步 stereo image pairs，以及相机 calibration。

**过程**：DINOv3 backbone联合预测 3D joints、direct interaction field 和各视图 surface endpoint evidence；沿校准相机射线采样深度候选；结合 joint-specific image compatibility 与 cross-view matching评分；同手关节共享 candidate support，并用 residual gate决定是否采用 geometric correction。

**输出**：每个 hand joint 到最近 object surface 的 3D interaction-field vector / endpoint。

### 实验结果

论文去除 535 个不一致 annotation 后，使用 72,307 个训练样本和 12,201 个 clip-held-out evaluation 样本，避免 temporal overlap。消融中 ResNet基线 mean ADE约 29.172 mm、Acc@10 26.91%；DINO direct prediction约 16.278 / 50.04%；加入完整 JSSR后约 15.740 / 51.23。完整 stereo reasoning相对 temporal endpoint baseline的 mean ADE进一步改善约 0.454 mm。

论文系统在 SHOW3D Interaction Field Challenge 中排名第三，但作者明确指出 leaderboard 数字与消融 checkpoint 使用的训练设置不同，因此不能直接把 challenge score 和主表模型逐项等同。

### 代码与数据

本次未核验到官方代码或独立模型发布。

### 局限、失败案例与开放问题

这里所谓“surface reasoning”是共享的 stereo-validated endpoint support；模型不恢复完整 object mesh、CAD model 或完整 object pose。因此它解决了 contact-neighborhood geometry，但距离 object-centric 4D interaction world representation 还有明显差距。

### 总结讨论

这是本期最直接的 3D HOI 感知论文之一。它可以作为 4D HOI 世界模型的低层监督：未来研究可以不只预测 hand trajectory，还同时预测每个关节未来接触 surface endpoint 及其随物体运动产生的 4D trajectory。

## 13. Seeing What Matters: Visual Cue Guided Video Planning for Generalizable Robot Navigation

- **作者**：Hojin Lee, Sizhe Lester Li, Maximilian Hilger, Susie Lu, Achim J. Lilienthal, Vincent Sitzmann, Daniel A. Duecker
- **年份与发表**：2026，arXiv v1，2026-09-15 提交
- **arXiv ID**：2609.16737
- **DOI**：[10.48550/arXiv.2609.16737](https://doi.org/10.48550/arXiv.2609.16737)
- **代表图**：CueNav，Fig. 2，视觉 cue 引导的视频规划与本体相关 inverse dynamics。来源：[Fig. 2 原图 PNG](https://arxiv.org/html/2609.16737v1/Fig2.png)

![CueNav Fig. 2](https://arxiv.org/html/2609.16737v1/Fig2.png)
- **论文**：[arXiv](https://arxiv.org/abs/2609.16737)
- **正式出版**：未核验到
- **项目**：[CueNav Project](https://cuenav.github.io/)
- **代码**：项目页当前标记 “coming soon”
- **数据**：未核验到独立公开数据发布
- **模型**：未核验到公开权重
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.16737)
- **类别标签**：Video Planning, World Model, embodied navigation, cross-embodiment
- **证据等级**：全文已核验
- **更新类型**：新论文
- **知域匹配结果**：未发现已有记录
- **现有知域 ID**：无

### 当前挑战

短时第一视角视频规划缺少长程全局任务信息，生成的视觉未来也不能直接转换为不同机器人本体可执行的连续控制，限制了导航泛化与闭环效率。

### 研究动机

CueNav继续沿“用生成视频作为 plan，再把视觉未来翻译为动作”的路线推进，但增加两个 cue：BEV map给视频模型全局任务上下文，保留机器人身体的一部分则提供 embodiment information。最终动作并不是从视频直接读取几何 waypoint，而是由 embodiment-specific inverse dynamics model 根据生成视频中的 dense flow 解码。

### 技术方案

**输入**：近期 egocentric visual observation、文本/语义目标、BEV/global cue，以及可见的机器人 embodiment cue。

**过程**：video planner生成短时未来视觉计划；从预测视频提取 dense optical flow；针对每个机器人本体训练的 IDM将 visual motion翻译成连续控制；系统持续闭环重新规划。

**输出**：未来视频计划和实际导航控制命令。

### 实验结果

狭窄通道实验中，CueNav在 1 m 宽度条件下达到约 70% 成功率，并在 1.5 m 条件完成全部测试。maze navigation训练轨迹来自 3×3 布局，评测扩展到 6×6；在 6×6 设置中，使用 BEV cue 的成功率约 55%，无 BEV约 30%。作者还在 Husky A300 与 Unitree Go2 上复用同一个 video planner，仅替换 embodiment-specific IDM，作为跨本体部署证据。

### 代码与数据

虽然 arXiv 摘要称额外结果和代码位于项目网站，但本次直接核验项目页时，Code 区仍标为 “coming soon”，因此本报告按**代码尚未公开可用**处理。

### 局限、失败案例与开放问题

主要限制是视频生成推理成本和闭环 replanning rate；预测仍是短 horizon，历史上下文有限，长程环境需要外部 visual cue 补充。作者也将更长记忆与模型蒸馏列为后续扩展方向。

### 总结讨论

CueNav不是 manipulation WAM，但它很好地暴露了 Video/WAM 的一个接口问题：**生成的未来视频怎样变成不同机器人真正可执行的动作**。其 embodiment-specific IDM 与 WLA³的共享 latent action、A4A的 4D affordance形成三种不同答案，值得作为跨本体 action grounding 的对照路线。
