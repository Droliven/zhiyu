# 从可预测到可执行：世界模型的记忆、物理约束与 4D 交互接口

**报告标签**：专题, World Action Model, world model, HOI, 3D/4D, egocentric vision, Embodied In-context Learning, causal evaluation, tactile

- **整理日期**：2026-09-14
- **来源**：2026-09-13 检索结果一份、2026-09-14 检索结果两份；另一个 2026-09-14 文件与其中一份完全相同。
- **覆盖范围**：36 篇唯一论文，按 arXiv ID 去重，均为当前本地馆藏未收录的条目。按相关性纳入边界日期论文；既有馆藏不重复计入新增。
- **证据口径**：已逐篇核验 arXiv 单篇元数据，并核对 35 篇 HTML 正文的主要实验及 OpenWAM 官方项目实验面板；尚未核验的代码、数据、显著性和发表状态写作“待核验”。论文中的 action-conditioned、causal attention 和模型命名不自动构成因果识别。

## 核心判断：瓶颈从“能预测未来”转向“未来能否约束动作”

这批论文表面上分为 WAM、具身 ICL、因果世界模型、4D HOI 与灵巧操作，实际围绕同一条链：**观察和示例 → 可保持的状态或记忆 → 可区分动作后果的预测 → 物理/接触约束 → 可执行的策略**。视频质量只检查链条的一端；相机运动、目标身份、接触状态和动作可达性一旦出错，逼真的 rollout 也可能把规划带向错误动作。

**预训练和记忆**方面，OpenWAM 与 GE-Act 2.0 把“大模型能否继承视频先验”推进到“哪些表示、数据和信息流真正帮助动作”。ContextFlow 与 ICI-VLA 则从推理时示例中获取任务信息；MaP-WAM、2AM、UniMPA 分别让计划器、Agent 或动作模型/检索机制持有历史。它们不能仅凭各自 benchmark 排名决定优劣：历史覆盖、检索容量、上下文 token、训练数据和在线更新频率需要共同控制。这是跨论文综合判断，而非单篇作者已完成的结论。

**物理和可靠性**方面，Programmable World Model 与 TourPhysics把状态转移或物理模拟从视觉合成中拆出；FARM、IMPLY、HaWMPO 分别从失败风险、物理锚定和幻觉分数审视 rollout。CST-WM、CLWM 和 habit/physics/nuisance 工作进一步测试模型是否沿预期路径响应动作或干预。现有结果支持特定任务上的结构约束、反事实区分或闭环收益；没有理由把这些结果统一称为开放世界因果识别。

**4D 与接触接口**方面，MINT 和 From Where to How 提供世界空间手/相机轨迹或连续交互预测，A4A 将未来交互点作为跨本体迁移媒介，HuRo 把人类视频转为机器人对齐轨迹，DEX-X、DeCAL、STAR 和 WM-Craftnet 把触觉或接触加入监督。最值得检验的接口是对象中心、时间持续的交互状态：对象位姿/动态点、手物对应、接触模式、可见性与不确定性，并检查它是否比纯视觉 latent 更能预测执行成败。这是由多篇工作引出的研究假设，尚非已验证结论。

## 三个可证伪的研究问题

1. **记忆应存在哪里？** 在同一长程 HOI 任务、相同历史信息量和计算预算下，对比计划级记忆、Agent 侧记忆、模型内部记忆；报告失败恢复、任务阶段切换和推理延迟。若差异在预算对齐后消失，先前收益主要可能来自额外上下文带宽。
2. **什么状态足以让想象指导行动？** 固定视频骨干与数据，分别加入纯视觉 latent、持续 3D/4D 对象轨迹、接触/触觉状态；用错误动作敏感度、对象身份保持、接触时刻与闭环成功率评价。若 4D/接触状态不改善动作排序，则“几何中间表示必需”的假设不成立。
3. **模型是否学到动作后果而非视觉捷径？** 对动作、外观、相机和目标可见性做独立干预，同时控制任务目标；检查反事实未来区分、风险校准和规划收益。只测预测误差或自一致性不足以回答该问题。

## 证据改变了哪些研究判断

| 问题 | 正文直接支持的结果 | 对研究设计的含义 |
| --- | --- | --- |
| 记忆更强是否就更会完成任务？ | 2AM 的 completion 从对齐基线 70.79% 到 76.29%，strict SR 却是 12.25% 对 11.83%。 | 记忆取回、阶段完成与严格任务成功应分开报告；不能用 completion 替代闭环成功。[2AM](https://arxiv.org/html/2609.11308v1) |
| 风险分数有没有直接证据？ | HaWMPO 对 50 个动作块有人工标注对照与 bootstrap 区间；FARM 的 Strict-Unseen 未优于所有基线。 | 应同时测分数校准、跨任务失效和实际动作筛选收益，避免只看 Seen AUROC。[HaWMPO](https://arxiv.org/html/2609.09941v1)、[FARM](https://arxiv.org/html/2609.11445v1) |
| 4D 接口的收益来自哪里？ | A4A 在五类策略上收益不等；FOCI 难接地任务仅 7.8%，真值位姿显著改善。 | 把对象定位/对应误差与策略推理误差分开，报告可感知输入和真值输入两套结果。[A4A](https://arxiv.org/html/2609.05892v1)、[FOCI](https://arxiv.org/html/2609.08743v1) |
| 触觉提升能外推到新物体吗？ | Dex-X 去触觉后 cube picking 明显下降，但多数未见形状仅约 23%–27%；WM-Craftnet 全零触觉仍保留大量收益。 | 按物体、接触阶段与模态消融定位增益；不能把完整训练配方的提升全部归于触觉。[Dex-X](https://arxiv.org/html/2609.07747v2)、[WM-Craftnet](https://arxiv.org/html/2609.07002v1) |
| 更快的表示是否让系统实时？ | FIRE3D 网络约 0.601 s/物体，后处理另需 4.181 s；DUET-DINO 还受搜索开销影响。 | 延迟包含感知、状态恢复、候选生成、rollout、评分和执行接口，单模块速度不等于闭环速度。[FIRE3D](https://arxiv.org/html/2609.08848v1) |

这些结果把推荐方向收敛到一个可检验的接口：**持续的对象/接触状态是否能提高错误动作辨别，并在固定计算预算下改善闭环恢复。** 预训练规模、示例压缩和触觉融合已经有密集方案；更明确的研究空间是把对应质量、遮挡不确定性、接触后果与候选动作排序放进同一受控评测。可以从 MemCorr-DP 的几何条件控制和 RodForesight 的候选后果排序出发，使用同一策略、同一示例、同一动作候选比较纯 latent、3D/4D 对应与接触状态，最后用 Beyond Task Success 的逐阶段诊断解释收益或失败。上述组合是本报告提出的方案，不是这些作者联合验证的系统。

## 纳入与排除记录

四份输入中两份逐字相同。其余三份的 41 个正式编号条目按 arXiv ID 合并为 33 篇；随后完成 RodForesight、Beyond Task Success、MemCorr-DP 的原始正文核验，再新增 3 篇，共 36 篇。本地导入前馆藏为 157 篇。作者和标题以 arXiv 记录为准，版本日期逐篇列出；检索文档中互相冲突的线上馆藏数字不沿用。

- **补录**：RodForesight（2609.12103）、Beyond Task Success（2609.07126）、MemCorr-DP（2609.06615），分别补齐动作后果排序、逐阶段可靠性与参考条件干预三环。
- **已收录**：[Streaming4D](https://arxiv.org/abs/2609.00610)（知域 ID `arxiv-2609-00610`）。已确认 v2 于 2026-09-10 提交；没有把“存在新版本”直接视为实质技术更新，本次不重复创建卡片。
- **主题相关但不纳入本专题**：[EgoSIS](https://arxiv.org/abs/2609.08938) 主要是 UAV 空间问答；[IAE-VTG](https://arxiv.org/abs/2609.09736) 主要是视频时序定位；[Rapid Learning of Dexterous In-Hand Pen Writing](https://arxiv.org/abs/2609.11775) 主要是实时 Jacobian 控制。其原始记录已确认，但本次没有证据将其纳入这条“预测—后果—执行”主线。
- **资源状态修正**：GE-Act 2.0、Pelican-Sim 的入口更正为官方页面所指地址；ProWAM、UniMPA、DUET-DINO、PWM、Pelican-Sim 的仓库只有说明/素材，不能写成完整实现已开源；EgoGenEval、WM-Craftnet、FOCI 所列代码地址当前返回 404，卡片记录为待开放核验。

## 正式论文与完整卡片

第 1–11 篇讨论预训练、示例与记忆，第 12–24 篇讨论物理、可靠性与动作后果，第 25–36 篇讨论第一视角 4D、接触与人类视频迁移。论文证据与本报告的研究建议分开陈述。


## 1. OpenWAM: An Open, Modular Exploration Towards Systematic World-Action Model Pretraining

- **作者**：Yuran Wang, Siqiao Huang, Mingleyang Li, Chenhao Zhang, Jiaqi Liang, Weiyang Jin, Yue Chen, Xuemin Chi, Donghao Zhou, Qize Yu, Yu-Kai Wang, Yuhan Rui, Shenzhe Yao, Zhen Yuan, Zhenhao Shen, Kefei Zhu, Zijie Zhu, Ning Gao, Xiaowei Chi, Guanqi He, Shanghang Zhang, Hao Dong, Lin Shao, Hang Zhao
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.07398
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.07398)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.07398)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[OpenWAM](https://openwam-official.github.io/)
- **代码**：[官方仓库](https://github.com/OpenWAM-Official/OpenWAM)（代码目录、配置和测试已公开；Hugging Face 组织页列出模型集合。）
- **数据**：官方说明使用 518.5M 帧、约 6,369 小时视频；独立完整数据下载状态未核验
- **模型**：[Hugging Face](https://huggingface.co/OpenWAM)
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.07398)
- **代表图链接**：[官方项目总览图：OpenWAM 数据—模型—评测框架](https://openwam-official.github.io/figs/overview.png)
- **类别标签**：World Action Model, Open Pretraining, Egocentric Video, Cross-Embodiment, Video-Action Joint Modeling
- **证据等级**：2026-09-14 已核对 arXiv 元数据、官方项目实验面板、代码目录与模型组织页；未逐页审计 PDF 或运行复现。
- **更新类型**：新论文
- **首次提交**：2026-09-07T12:12:32Z
- **最近修订**：2026-09-07T12:12:32Z
- **arXiv 主分类**：cs.RO

### 核心内容与 Insight

OpenWAM试图把 WAM 从单项方法推进为开放、模块化的预训练体系：统一机器人动作接口，同时把机器人轨迹和第一视角人类视频纳入同一视频—动作生成框架。其价值主要在可拆分的数据、模型与评测组件，而非单一结构技巧。

### Pipeline

**输入**：初始视觉、语言、人类/机器人视频及统一到 80 维空间的机器人动作。

**过程**：Wan2.2 VAE 编码视频；TI2V5B 与 ActionDiT 在 30 层联合自注意力中交换信息；互惠掩码和同步去噪联合建模视觉未来与动作。

**输出**：动作条件未来视频与可执行动作块。

### 实验与证据

官方项目页报告 LIBERO 平均 99.3%、RoboTwin 2.0 Full 93.60%；真实 RoboDojo 得分/成功率 37.6/24.4，对比 \(\pi_{0.5}\) 22.9/12.8。项目展示 46 个 checkpoint。结果表明规模化联合预训练具有潜力，但本次未完成论文所有数据划分、训练预算和 baseline 复现细节的逐页审计，不能据此确认全面 SOTA。

### 代码与数据

代码目录、配置和测试已公开；Hugging Face 组织页列出模型集合。 以上状态核验于 2026-09-14；入口和目录存在不等于已经运行复现实验。

### 局限、失败案例与开放问题

训练资源门槛高；统一动作空间可能掩盖不同机器人动力学与控制频率差异。人类视频只占约 30% 的训练组成，其独立贡献需要严格消融。视频与动作共同生成并不自动保证接触可执行性。

### 总结讨论：与知域的关系

OpenWAM是本期最直接的大规模开放 WAM 工作，尤其符合“从人类视频学习、跨 embodiment、联合视频—动作建模”的关注重点。

## 2. GE-Act 2.0: Pretraining and Scaling a World-Action Model for Robotic Manipulation

- **作者**：AgiBot Research Team, Renhang Liu, Wenzhi Zhao, Zhuo Yang, Liliang Chen, Pengfei Zhou, Shengcong Chen, Guanghui Ren, Youlun Peng, Rongjun Jin, Nan Wang, Sukai Wang, Xindong He, Jinyuan Feng, Ziyu Xiong, Linqing Zhong, Yifei Wei, Feng Han, Long Zhang, Da Huang, Nanshu Zhao, Chenghao Yin, Mo Wu, Zhaodong Yan, Kongtao Hu, Yuxiang Yan, Aogelijiang Niyazi, Yu Fang, Jia Zeng, Lizhu Meng, Daizhen Lv, Haoyu Cao, Zhiwen Hou, Lianjin Ye, Yuehan Niu, Zhikai Cai, Xuan Hu, Hui Min, Xiongfeng Cai, Yue Liao, Jing Wu, Soujanya Poria, Ye Li, Sanping Zhou, Maoqing Yao
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.05588
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.05588)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.05588)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[GE-Act 2.0 官方项目](https://ge-act-v2.github.io/)
- **代码**：未在 arXiv 页面发现公开仓库
- **数据**：未公开
- **模型**：未公开
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.05588)
- **类别标签**：World Action Model, Robotics, 预训练, 扩展律, cross-embodiment
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文（边界日期收录）
- **首次提交**：2026-09-04T17:16:48Z
- **最近修订**：2026-09-04T17:16:48Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.05588v1)

### 核心内容与 Insight
GE-Act 2.0 声称是可规模化 WAM 预训练路线：生成与动作组件全部在操作数据上从零初始化（不继承视频生成先验），由三部分组成——控制导向自编码器（CoAE）、单步视觉规划器（SVP）与逆动力学模型（IDM）。CoAE 在激进压缩下保留动作与指令相关信息；SVP 可微单步生成完整未来状态，使视觉规划与逆动力学能在互补数据上分别预训练；之后用知识对齐选择性优化（KASO）联合训练，只选择与记录动作行为兼容的预测未来，减少错配监督。在 100 任务/20 技能组、held-out 场景/背景/光照/物体实例上直接评估预训练 checkpoint（无 per-task 微调）。共训数据从 300 小时扩到 30,000 小时，G1-OP 成功率 17.1%→44.1%，G2-90D 13.4%→31.1%；G2-90D 仅占共训数据不到 2% 却提升 17.7 点，作者解读为跨本体迁移信号。

### Pipeline
**输入**：操作数据（观测+指令+动作），规模 300→30,000 小时。
**过程**：CoAE 压缩观测/指令到信息密集潜在空间 → SVP 单步预测完整未来状态 → IDM 从预测未来反解动作 → 分阶段预训练（视觉规划与逆动力学分离）→ KASO 联合微调（只保留行为兼容的预测未来）。
**输出**：可直接部署的 WAM 策略（无 per-task 微调）。

### 实验与证据

正文表 2 给出受控 KASO 消融：相同预训练组件、相同 300 小时连接/对齐数据下，四物体抓取宏平均由 E2E 的 27.5% 和 E2E+PT 的 22.5% 提升至 37.5%；单物体拾取由 12% 提升至 40%。四物体每目标 10 次、单物体 25 次。表 3 的 RoboTwin Clean-to-Random 中，GE-Act 2.0 的 Hard 为 60.52%，对比 π0.5 的 47.90%，但 Light 项低于 π0.5（65.92% 对 69.20%）。这支持特定训练设计和 OOD 收益，不能概括为所有维度均领先；预训练规模曲线与少量跨本体数据收益还需区分总数据量和配方的作用。 [正文实验与表格](https://arxiv.org/html/2609.05588v1)。

### 代码与数据
arXiv 页面未发现公开代码/模型/数据链接。作为技术报告，若 AgiBot 后续开源将大幅提升可复现性；当前公开内容不足以复现扩展律实验。

### 局限、失败案例与开放问题

分阶段预训练与连接训练的预算需要分开计算；KASO 受控拾取实验样本量较小，宏平均提升不能直接替代跨任务、跨本体的独立验证。

### 总结讨论：与知域的关系
WAM 预训练与扩展律的直接证据，与馆藏 Dyna-2（百万小时扩展律）互补——Dyna-2 回答「数据多大」，GE-Act 2.0 回答「从零怎么训、信号怎么选」。KASO 的「选择行为兼容的未来」与知域关注的世界模型可靠性直接相关。

## 3. Learning to Use Imagination: Progress-Conditioned Future Utilization for World Action Models

- **作者**：Yijie Zhu, Zitong Yu, Wei Li, Hui Ma, Wen Li, Rui Shao, Liqiang Nie
- **年份与发表**：2026，arXiv 预印本，v1；投稿 TPAMI，非接收状态
- **arXiv ID**：2609.06578
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.06578)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.06578)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[ProWAM 项目页](https://github.com/JiuTian-VL/ProWAM)
- **代码**：[官方仓库](https://github.com/JiuTian-VL/ProWAM)（当前仓库仅见 README 与展示素材，未见训练或推理实现。）
- **数据**：未公开
- **模型**：未公开
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.06578)
- **类别标签**：World Action Model, VLA, 执行进度
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-06T12:46:20Z
- **最近修订**：2026-09-06T12:46:20Z
- **arXiv 主分类**：cs.CV
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.06578v1)

### 核心内容与 Insight
WAM 把未来视觉动态并入动作生成，但现有 WAM 对想象未来的利用缺乏对执行进度的适应。作者识别出未来效用的两种非均匀性：(i) inter-progress——不同执行阶段控制需求变化，想象未来的效用随阶段变化；(ii) intra-progress——同一进度状态下个体未来潜在的相关性异构。ProWAM 引入执行进度作为显式中间表示，由两个耦合组件构成：SS-DTPE（自监督双时序进度编码器）耦合短期动作-观测交互建模与长期循环进度聚合；进度条件化想象利用模块（PUAM）根据进度表示自适应调度未来潜在。

### Pipeline
**输入**：观测+动作历史+指令。
**过程**：SS-DTPE 编码执行进度（短期交互+长期聚合）→ 进度表示条件化 PUAM → PUAM 自适应选择/加权想象未来 → 动作生成。
**输出**：进度感知的动作序列。

### 实验与证据

正文表 I 报告 LIBERO 平均成功率 99.1%；表 II 的 RoboTwin 2.0 Clean/Randomized 为 93.9%/92.8%，平均 93.4%；表 III 的 VLABench SR/IS/PS 为 68.4/85.4/81.2。论文包含进度模块与训练配方消融。跨论文总表同时包含不同具身预训练条件，主表排名不能直接视为同预算因果比较；提交 TPAMI 不等于已接收。 [正文实验与表格](https://arxiv.org/html/2609.06578v1)。

### 代码与数据

当前仓库仅见 README 与展示素材，未见训练或推理实现。 以上状态核验于 2026-09-14；入口和目录存在不等于已经运行复现实验。

### 局限、失败案例与开放问题

接近饱和的 LIBERO 分数不能充分检验进度状态是否正确；需要错误进度、阶段回退、接触失败后恢复及端到端延迟评测。

### 总结讨论：与知域的关系
WAM 内部机制方向，与 MaP-WAM（进度校准）、GE-Act 2.0（KASO 选择未来）共同构成「未来利用策略」子主题。对知域 WAM 技术路线是机制层面的补充。

## 4. ContextFlow: In-Context Flow Matching for Robot Manipulation

- **作者**：Jian Ding, Xianjie Dai, Roei Herzig, Nussair Hroub, Jinjie Mai, Dengxin Dai, Bernard Ghanem, Mohamed Elhoseiny
- **年份与发表**：2026，arXiv 预印本，v1；arXiv 作者备注称 ECCV 2026 接收
- **arXiv ID**：2609.06852
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.06852)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.06852)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[ContextFlow](https://dingjiansw101.github.io/contextflow-page/)
- **代码**：[官方仓库](https://github.com/dingjiansw101/ContextFlow)（训练/推理相关源码、脚本和测试已公开；ALOHA 数据集入口可访问。）
- **数据**：[ALOHA In-Context Dataset](https://huggingface.co/datasets/vo2yager/aloha_incontext)
- **模型**：未发现独立权重页
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.06852)
- **代表图链接**：[论文 Figure 1：单示例上下文驱动新任务执行](https://arxiv.org/html/2609.06852#S1.F1)
- **类别标签**：Embodied In-Context Learning, Flow Matching, Robot Manipulation, One-Shot Demonstration
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-06T21:53:58Z
- **最近修订**：2026-09-06T21:53:58Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.06852v1)

### 核心内容与 Insight

ContextFlow让策略在推理时接收一条完整示例轨迹和当前任务观测，在不针对新任务更新参数的情况下生成动作。核心 Insight 是把“示例理解”和“动作生成”分别交给上下文专家与动作专家，并用压缩 token 建立跨时间对应关系，避免自回归离散动作建模的累积误差。

### Pipeline

**输入**：语言指令、一条示例的多视角观测—动作轨迹、当前机器人观测与本体状态。

**过程**：Perceiver 类压缩器将长示例和当前多视角图像压缩为固定数量 token；上下文专家提取任务动态，动作专家通过交叉注意力读取上下文；条件流匹配从噪声迭代生成动作块。

**输出**：未来约 50 步连续机器人动作。

### 实验与证据

LIBERO 使用 32 个训练任务、4 个未见任务，每任务 50 次评估；ContextFlow 在未见任务平均成功率 73.5%，对比 ContextAR 53.5%、ICRT 38.5%、零样本 \(\pi_0\) 44.5%，与对新任务单独微调的 \(\pi_0\) 72.5% 接近。真实 ALOHA 的 6 个未见任务各 10 次，成功次数为 2、5、4、4、4、6；ICRT 几乎全部失败。结果支持单演示条件策略，但不能证明跨机器人或长期自主积累经验。 [正文实验与表格](https://arxiv.org/html/2609.06852v1)。

### 代码与数据

训练/推理相关源码、脚本和测试已公开；ALOHA 数据集入口可访问。 以上状态核验于 2026-09-14；入口和目录存在不等于已经运行复现实验。

### 局限、失败案例与开放问题

性能依赖示例质量和视角对应；一条示例可能无法覆盖接触恢复和多解策略。外部 baseline 的训练数据、模型容量与动作表示并非完全一致。真实实验每任务仅 10 次，统计波动较大。

### 总结讨论：与知域的关系

这是本期最直接的具身 In-Context Learning 工作，可作为“演示轨迹即上下文”的强基线，并与 WAM 的动作后果建模形成接口。

## 5. ICI-VLA: In-Context Imitation with Spatiotemporally Aligned Demonstrations for Vision-Language-Action Models

- **作者**：Songhua Yang, Ziyu Liu, Xuetao Li, Ruqi Xiao, Kangxin Zhu, Miao Li
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.07581
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.07581)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.07581)
- **代码 / 模型**：未确认公开
- **数据**：使用 LIBERO、RoboTwin 2.0 及实体任务
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.07581)
- **类别标签**：Embodied In-Context Learning, VLA, Retrieval, Imitation Learning
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-07T14:55:35Z
- **最近修订**：2026-09-07T14:55:35Z
- **arXiv 主分类**：cs.RO
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.07581v1)

### 核心内容与 Insight

ICI-VLA 让固定参数 VLA 在推理时读取检索到的短示范，不为每个新任务做梯度更新。长演示被切成语义 micro-demonstrations，上下文同时匹配任务阶段和几何状态。

### Pipeline

- **输入**：当前视觉/语言状态与演示库短轨迹。
- **过程**：用 DTW 挖掘时空对齐正样本训练 RD-Encoder；推理时检索微示范；Target Action Masking 降低直接复制。
- **输出**：参数冻结条件下生成的机器人动作。

### 实验与证据

正文表 1 报告 LIBERO 97.7%、RoboTwin 2.0 60.4%，后者比所列最高基线高 19.3 个百分点；论文明确这些历史基线采用各自已发表协议。表 2 中去掉 DTW 后 RoboTwin 平均降至 31.4%，去掉语义检索为 38.1%，Naive ICL 为 10.7%，比跨模型排行更直接支持检索对齐和目标动作掩蔽。表 3 的四个真机任务每项 250 次，共 1,000 次；平均成功率 83.2%，95% Wilson 区间为 [80.8,85.4]。不应把该论文归入“每任务仅 10–25 次且无置信区间”的情况。 [正文实验与表格](https://arxiv.org/html/2609.07581v1)。

### 代码与数据

未确认代码和模型发布；使用公共 benchmark 不等于训练流水线可复现。

### 局限、失败案例与开放问题

检索库覆盖决定能力上限；测试与示范过近会高估泛化。需报告检索延迟、上下文长度、无相关示范和对抗性近邻下的退化。

### 总结讨论：与知域的关系

直接命中 embodied in-context learning，可与世界模型式 test-time planning 对照。

## 6. MemCorr-DP: Counterfactual Correspondence Conditioning for a Diffusion Policy Guided by a Reference

- **arXiv ID**：2609.06615
- **类别标签**：3D/4D, Diffusion Policy, Reference Conditioning, Counterfactual Evaluation
- **更新类型**：新论文
- **作者**：Tan Su, Haoxiang Yang, Ruxin Wang, Binghui Xie
- **论文**：[arXiv](https://arxiv.org/abs/2609.06615)
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.06615)（预印本标识，非期刊 DOI）
- **首次提交**：2026-09-06T14:03:20Z
- **最近修订**：2026-09-06T14:03:20Z
- **arXiv 主分类**：cs.RO
- **年份与发表**：2026，arXiv 预印本，v1
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.06615v1)
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。

### 核心内容与 Insight

MemCorr-DP 把“选哪条示例”转化为当前场景与参考轨迹之间的显式 3D 对应条件，并用同状态、反向任务的成对训练迫使策略真正使用参考。核心价值是可干预的参考接口。

### Pipeline

- **输入**：当前 RGB-D、对象 mask、机器人状态和已知任务的一条固定参考轨迹。
- **过程**：冻结 RoMa v2 匹配并提升为 3D 关系；第一阶段用真值关系和成对反向目标训练扩散策略，第二阶段混合真实匹配误差微调；每次预测 16 步、执行 8 步后重规划。
- **输出**：受参考轨迹条件控制的机器人动作块。

### 实验与证据

正文表 2 在单个 Meta-World Door、位置与 ±15° 相机联合偏移上报告 145/150（96.67%），对比共享动作架构的视觉 Transformer 132/150（88.00%）。训练使用 80 对配置、160 条轨迹，3 个种子；视觉控制参数仅差 +0.36%，但不计冻结 RoMa v2。表 3 中错误参考使最终模型成功率降至 5/300，正确参考为 292/300，支持参考条件确实影响行为。 [正文实验与表格](https://arxiv.org/html/2609.06615v1)。

### 代码与数据

原始论文未提供可确认的公开代码、数据或模型下载入口，开放状态待核验。

### 局限、失败案例与开放问题

只测试单个模拟 Door 的开/关，依赖对象 mask、标定 RGB-D、已知任务和固定参考；未验证跨实例、跨类别、真实机器人或在线检索。成对条件干预不等于完整 SCM 识别。

### 总结讨论：与知域的关系

为具身 ICL、4D 对应和条件敏感性提供小规模可复现的实验设计，连接“示例几何”与“动作后果”。

## 7. Memory as Plans: World-Action Modeling with Memory-Grounded Planning

- **作者**：Sizhe Zhao, Haozhe Xie, Weiyu Zhao, Chenchu Zhang, Huan Wang, Chenyang Wang, Qinglin Liu, Shengping Zhang
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.11561
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.11561)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.11561)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[MaP-WAM](https://sizhezhao.github.io/projects/MaP-WAM/)
- **代码**：项目页未给出可确认的实现入口，待核验。
- **数据**：使用 RMBench 与真实机器人任务；未发现新数据下载页
- **模型**：项目页未给出可确认的权重下载入口，待核验。
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.11561)
- **代表图链接**：[论文 Figure 1：记忆机制比较与 MaP-WAM 框架](https://arxiv.org/html/2609.11561#S1.F1)
- **类别标签**：World Action Model, Long-Horizon Memory, Visual Planning, Progress Prediction
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-10T13:52:51Z
- **最近修订**：2026-09-10T13:52:51Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.11561v1)

### 核心内容与 Insight

MaP-WAM把已完成片段的语言和稀疏视觉证据保存为 episodic memory，仅在规划阶段读取长历史；执行器接收压缩后的语言—视觉计划，从而避免每一步都扩展上下文。它还联合预测动作与进度，用真实观测校正计划位置。

### Pipeline

**输入**：当前观测、任务语言、已完成片段的稀疏视觉与语言记录。

**过程**：语言规划器生成下一片段目标；因果世界模型生成视觉计划；WAP 联合预测未来视觉 latent、动作块和进度；plan-observation alignment 校正进度并触发片段切换，固定计划前缀通过 KV cache 复用。

**输出**：分段语言/视觉计划、动作块与完成进度。

### 实验与证据

RMBench 九项任务平均成功率 83.3%，对比 LingBot-VA 77.1%、Mem-0 42.0%；真实机器人任务平均 78.0%。分任务结果显示个别 M(1) 任务不占优，但多观察记忆任务提升明显。结果支持稀疏视觉记忆和计划分解，但项目页未给所有方法相同推理预算下的完整吞吐、显存与规划器成本对比。 [正文实验与表格](https://arxiv.org/html/2609.11561v1)。

### 代码与数据

官方项目页可访问；本次页面未给出可确认的训练/推理仓库或权重下载入口，代码、数据和模型开放范围待核验。

### 局限、失败案例与开放问题

规划错误可能在整个片段持续影响执行；视觉计划质量受生成模型限制。方法假设已完成片段可以可靠切分并压缩，开放世界中的模糊阶段边界和错误记忆尚未充分评测。

### 总结讨论：与知域的关系

该工作把长期记忆显式转成 WAM 的语言—视觉计划，适合与具身 ICL 的检索示例和流式执行做统一研究。

## 8. 2AM: Grounding Agent-Side Memory as Guidance for Steerable Action Models in Long-Horizon Manipulation

- **作者**：Yutong Hu, Fengjiao Chen, Xuezhi Cao, Renaud Detry
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.11308
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.11308)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.11308)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：未发现
- **代码**：未发现
- **数据**：LIBERO-Mem；未发现独立发布
- **模型**：未发现
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.11308)
- **代表图链接**：[论文 Figure 1：Agent 记忆与无历史 Action Model 的接口](https://arxiv.org/html/2609.11308#S2.F1)
- **类别标签**：Long-Horizon Manipulation, Agent Memory, Steerable Action Model, RGB-Only
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-10T09:35:56Z
- **最近修订**：2026-09-10T09:35:56Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.11308v1)

### 核心内容与 Insight

2AM将所有任务记忆保留在高层 Agent 中，让动作模型在 episode 层面无历史。Agent把历史的当前后果压缩为子任务语言和可选的 2D grasp/place/move 提示；动作模型只根据当前 RGB、本体和提示执行局部动作。

### Pipeline

**输入**：全局任务、Agent 维护的观测/命令/结果摘要、当前 agent-view 和 wrist RGB、机器人状态。

**过程**：Agent生成结构化 steering command；动作模型以带 dropout、空间噪声和时间抖动的提示监督训练；部署时所有任务相关运动均通过同一动作模型。

**输出**：固定长度绝对末端执行器动作块。

### 实验与证据

在 LIBERO-Mem 上，2AM完成率 76.3%，相对最强报告基线 14.8% 提升 61.5 个百分点；相对对齐的 \(\pi_0\) 复现，完成率提高 5.5 点、宽松成功率提高 25.6 点，而严格成功率相近。后一个受控比较更能支持接口设计，前一个跨系统差距不能完全归因于记忆机制。 [正文实验与表格](https://arxiv.org/html/2609.11308v1)。

### 代码与数据

未发现官方代码、模型或扩展数据下载，Agent 记忆整理和提示生成的复现状态不明。

### 局限、失败案例与开放问题

2D 提示适合可见对象操作，但无法表达隐藏力状态、精确 3D 接触和复杂轨迹；Agent 的错误对象绑定会直接误导动作模型。方法是记忆压缩与分工，不是参数冻结下从少量示例学习新动力学。

### 总结讨论：与知域的关系

该工作为具身 ICL/WAM 提供“记忆只在 Agent，执行器保持短上下文”的系统对照，适合研究上下文接口而非单纯扩大模型窗口。

## 9. UniMPA: A Unified Memory-Prediction-Action Model via Action-Grounded Transition Modeling

- **作者**：Wei Li, Rui Shao, Jie He, Lingsen Zhang, Ziwei Liu, Liqiang Nie
- **年份与发表**：2026，arXiv 预印本，v1；投稿 TPAMI，非接收状态
- **arXiv ID**：2609.11875
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.11875)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.11875)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[UniMPA](https://jiutian-vl.github.io/UniMPA-page/)
- **代码**：[官方仓库](https://github.com/JiuTian-VL/UniMPA)（当前仓库仅见 README 与展示素材，不能认定已公开完整实现。）
- **数据**：使用 LIBERO、LIBERO-Plus、RoboTwin 2.0、VLABench 与真实机器人任务
- **模型**：未发现独立权重页
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.11875)
- **代表图链接**：[官方项目总览：未来预测—双向记忆—动作生成](https://jiutian-vl.github.io/UniMPA-page/#method)
- **类别标签**：Memory-Augmented VLA, Future Prediction, World Action Model, Flow Matching
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-10T17:45:03Z
- **最近修订**：2026-09-10T17:45:03Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.11875v1)

### 核心内容与 Insight

UniMPA将未来预测、经验检索和动作生成统一在“动作支撑的状态转移”上。持续 latent 流跟踪任务进度，像素流只在转移关键时刻启动；预测转移检索历史视觉—动作证据，反向记忆再提供动作原型，流匹配在当前场景中细化。

### Pipeline

**输入**：当前视觉、语言、本体，以及离线构建的视觉—动作和动作—视觉记忆库。

**过程**：World Expert产生未来转移 token；trigger gate选择是否执行像素预测；双向记忆检索可执行经验与动作原型；Prototype-Biased Flow在历史支持的动作区域初始化并经 10 步 Euler 流匹配细化。

**输出**：未来转移表示、检索证据与连续动作块。

### 实验与证据

官方项目页报告 LIBERO 98.6%、LIBERO-Plus 85.3%、RoboTwin 2.0 Hard 58.2%；GALAXEA R1 Lite 21 项任务的 TSR/CSR 为 77.7%/86.3%，\(\pi_{0.5}\) 为 65.3%/75.6%。LIBERO 共 2,000 次 rollout，Hard 设置每任务 100 次；真实任务每项 25 次。移除记忆使 LIBERO/真实 TSR 分别下降 4.1/13.8 点，支持预测与记忆互补。部分 baseline 标有作者复现，需避免把全部差异视为官方同预算结果。 [正文实验与表格](https://arxiv.org/html/2609.11875v1)。

### 代码与数据

当前仓库仅见 README 与展示素材，不能认定已公开完整实现。 以上状态核验于 2026-09-14；入口和目录存在不等于已经运行复现实验。

### 局限、失败案例与开放问题

记忆只在 rollout 结束后异步扩充，不能在当前执行中即时利用新经验；固定预测时间尺度不适合同时覆盖自由空间运动和快速接触；二值 trigger gate 无法表达连续不确定性。

### 总结讨论：与知域的关系

UniMPA把具身 ICL 式经验检索与 WAM 的未来预测、动作生成紧密耦合，是研究“可执行上下文”的重要候选。

## 10. DUET-DINO: Simultaneous Cross-View World Modeling for Latent Planning in Robot Manipulation

- **作者**：Nisarga Nilavadi, Ralf Römer, Moritz Reuss, Michael Krawez, Tobias Jülg, Angela P. Schoellig, Rudolf Lioutikov, Wolfram Burgard
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.10506
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.10506)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.10506)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[DUET-DINO](https://utn-air.github.io/DUET-DINO)
- **数据**：DROID、RoboArena
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.10506)
- **类别标签**：Latent World Model, Multi-View, 7-DoF Planning, DINOv3
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **代码**：[官方仓库](https://github.com/nisarganc/DUET-DINO)（当前仓库仅有 README，代码实现尚未在该入口公开。）
- **首次提交**：2026-09-09T17:41:38Z
- **最近修订**：2026-09-09T17:41:38Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.10506v1)

### 核心内容与 Insight

DUET-DINO 同时建模侧视角全局场景和腕部局部几何，以 cross-attention 交换信息。关键发现是 frozen representation 影响细粒度动态：其设置中 DINOv3 比 V-JEPA 2 更能保留腕视角动作变化。

### Pipeline

- **输入**：同步侧视/腕视 RGB、末端状态和 7D 动作。
- **过程**：冻结 DINOv3；双向 cross-attention；分别预测未来 latent；用 teacher-forcing 与短程 autoregressive loss 训练；CEM 最小化双视角目标 latent 距离。
- **输出**：双视角 future latents 与 7-DoF 动作序列。

### 实验与证据

训练含 62,877 条 DROID、5,856 条 RoboArena 轨迹。仿真 reach、angled-reach、lift 成功率为 92%、72.5%、60%；去掉 cross-attention 后前两项降至 81%、42.5%。真实硬件 angled-reach 仅 26.7%，虽优于所测 baseline，但显示 sim-to-real 与预算瓶颈。双视角约慢两倍，规划步约 15–17 秒。 [正文实验与表格](https://arxiv.org/html/2609.10506v1)。

### 代码与数据

当前仓库仅有 README，代码实现尚未在该入口公开。 以上状态核验于 2026-09-14；入口和目录存在不等于已经运行复现实验。

### 局限、失败案例与开放问题

CEM 昂贵，硬件减少搜索预算；侧视角对相机位姿敏感。视觉 latent 不显式保证对象 SE(3)、接触和动力学一致。

### 总结讨论：与知域的关系

是 DWM/V-JEPA 类 latent world model 向真实 7-DoF manipulation 的推进，也为结合显式 3D/4D 几何提供基线。

## 11. World in World: Explore the World with World Models

- **作者**：Chenxi Song, Yanming Yang, Chi Zhang
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.11548
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.11548)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.11548)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[World in World 项目页](https://chenxi-song.github.io/worldinworld)
- **代码**：[官方仓库](https://github.com/Westlake-AGI-Lab/WorldinWorld)（仓库包含 wiw、lingbot_world、examples 与工具目录，可获取实现。）
- **数据**：未公开
- **模型**：未公开
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.11548)
- **类别标签**：video world model, 交互式探索, 训练自由, egocentric
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-10T13:42:26Z
- **最近修订**：2026-09-10T13:42:26Z
- **arXiv 主分类**：cs.CV
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.11548v1)

### 核心内容与 Insight
自回归视频世界模型支持交互式长程探索，但灵活控制困难：从新视角探索源视频要求 rollout 与记录事件保持同步、在请求视角放置观测内容、合理补全新暴露区域、回访时恢复之前生成的外观。现有方法用任务专用模块或额外训练解决。World in World 提出训练自由的推理期接口：把异构控制证据（源视频观测、目标视角场景投影、引导新暴露区域补全的几何渲染、滚动缓存之外的检索生成状态）转换成相机与时间标注的干净视觉状态，通过冻结因果视频模型的原生 self-attention 读取。每个证据源携带 token 级支持与可用性调度；对应关系路由器处理持久点对应。

### Pipeline
**输入**：源视频 + 目标相机路径/时间 + 控制证据（观测、投影、几何渲染、历史生成）。
**过程**：证据→干净视觉状态转换（相机/时间标注）→ 对应关系路由（持久点对应）→ 冻结因果视频模型 self-attention 读取 → 自回归生成。
**输出**：与源事件同步的新视角长程探索视频。

### 实验与证据

正文表 1 在 DAVIS/OpenVid-1M 的相机控制重渲染中报告 VBench Overall 85.192、旋转误差 2.8326°、PSNR 23.1511；相比 UniWorld-View 的 84.295、4.1958°、22.4735，所测维度有所改善。表 2 中去掉 target-view warp 的旋转误差从 1.7823° 升到 6.1158°，说明几何条件是主要贡献之一。不同模块消融的增益并不均等；这些主要是重渲染与视角控制指标，不能替代真实机器人的长程交互验证。 [正文实验与表格](https://arxiv.org/html/2609.11548v1)。

### 代码与数据

仓库包含 wiw、lingbot_world、examples 与工具目录，可获取实现。 以上状态核验于 2026-09-14；入口和目录存在不等于已经运行复现实验。

### 局限、失败案例与开放问题
长程相机控制、几何条件与外部证据冲突仍会累积误差；重渲染评测未验证接触可执行性。其训练自由属性说明能复用冻结骨干，不能直接推出在所有交互任务上优于训练式方法。

### 总结讨论：与知域的关系
命中「交互式世界模型 + 长程一致性 + 流式生成」，与馆藏 Streaming4D、OctWorld 相关。其「控制证据调度」思想与知域「流式生成」专题直接互补。

## 12. HaWMPO: Hallucination-Aware World Model-based Policy Optimization for Generalist Robot Policy

- **作者**：Zengjue Chen, Peidong Liu, Jiawei Li, Qi Wang
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.09941
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.09941)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.09941)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：未发现
- **代码**：未在 arXiv 页面发现公开仓库
- **数据**：未公开
- **模型**：未公开
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.09941)
- **类别标签**：world model, RL, VLA, 幻觉, 策略优化
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-09T09:33:25Z
- **最近修订**：2026-09-09T09:33:25Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.09941v1)

### 核心内容与 Insight
通用机器人策略在复杂长程场景成功率受限；在线 RL 改善 VLA 但依赖昂贵物理交互、样本效率低且有安全风险。世界模型提供想象 rollout 的替代，但长程 rollout 的预测幻觉产生有偏状态转移，误导策略学习。HaWMPO 提出幻觉感知世界模型策略优化：action-conditioned 幻觉感知模型估计生成图像序列的可靠性，把幻觉分数并入组相对策略优化（GRPO）的 Reward-Soft 机制，训练中抑制不可靠动作块。LIBERO 上平均成功率最佳（超基线模型 15.0%、超最强 baseline 2.8%），G1 机器人真机验证。

### Pipeline
**输入**：VLA 策略 + 世界模型 + 目标任务。
**过程**：世界模型生成想象 rollout → 幻觉感知模型逐动作块估计可靠性 → 幻觉分数进入 Reward-Soft（GRPO）→ 抑制不可靠动作块 → 策略更新（闭环）。
**输出**：世界模型后训练（post-training）的 VLA 策略。

### 实验与证据

正文表 1 在所选 LIBERO Spatial/Goal/Object 设置下报告平均成功率 63.7%，对比 OpenVLA-OFT-base 48.7%、WMPO 56.8%、WoVR* 60.9%，分别高 15.0、6.9、2.8 个百分点。表 3 还在 50 个 LIBERO 动作块上与人类幻觉标注比较：HAM 的 AUROC 为 0.9375，轨迹 bootstrap 95% CI 为 [0.8648,0.9911]；AP 为 0.8952，95% CI 为 [0.7660,0.9885]。因此“完全未直接验证幻觉分数”不成立，但样本仅 50 个块、标签仍依赖人工定义，不能等同普遍可靠的物理误差估计。 [正文实验与表格](https://arxiv.org/html/2609.09941v1)。

### 代码与数据
未发现公开代码/模型/数据。不可复现（基于摘要信息）。

### 局限、失败案例与开放问题

人类标注幻觉对照仅 50 个动作块；检测分数在长程、相机变化和真实物理失败上的校准仍待验证。报告的 2.8 是百分点增益，且来自指定训练/测试设置。

### 总结讨论：与知域的关系
直接命中「世界模型中的可靠性」与「世界模型用于策略优化」。与知域 8 月收录的失败条件世界模型（FACT 等）专题衔接，把「失败/幻觉」从评测对象变成训练信号。

## 13. Programmable World Model

- **作者**：Zheng-Hui Huang, Guixu Lin, Jiacheng Lin, Yi-Chuan Huang, Ruihan Yu, Muyao Niu, Siqi Yang, Yu-Lun Liu, Yung-Yu Chuang, Kaipeng Zhang, Zhixiang Wang
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.10540
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.10540)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.10540)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[PWM 项目页](https://alaya-lab.github.io/pwm)
- **代码**：[官方仓库](https://github.com/AlayaLab/pwm)（当前仓库仅见 README 与 assets，尚不能认定训练/推理代码可复现。）
- **数据**：未公开
- **模型**：未公开
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.10540)
- **类别标签**：world model, 可编程状态, 视频生成, 交互
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-09T17:59:32Z
- **最近修订**：2026-09-09T17:59:32Z
- **arXiv 主分类**：cs.CV
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.10540v1)

### 核心内容与 Insight
视频世界模型生成越来越真实的交互体验，但缺乏可靠机制在长交互中维持持久世界状态与执行可编程规则。Programmable World Model 把世界状态演化与视觉观测生成解耦：Agent 把 NL 指令翻译成可执行程序，指定实体状态与状态转移规则，直接控制个体实体及其交互；轻量引擎执行程序，更新并维护显式、持久的全局世界状态（包括屏外实体与非视觉属性）。为连接世界状态与视觉生成，引入 state-augmented 3D OBB 作为中间表示，与目标相机轨迹一起确定性编译成像素对齐的时空条件信号，供预训练视频模型（生成渲染器）使用。

### Pipeline
**输入**：自然语言指令（+ 初始场景）。
**过程**：NL→可执行程序（实体状态+转移规则）→ 轻量引擎执行，维护显式全局状态（含屏外/非视觉属性）→ 状态+3D OBB → 像素对齐时空条件 → 预训练视频模型渲染。
**输出**：遵循可编程规则的交互式视觉序列，状态可查询/可干预。

### 实验与证据

正文表 1 在 50 个 CombatStateBench 片段上评价视觉质量与状态：Count Accuracy 为 94.00%，State Accuracy 为 98.00%，对比 LingBot-World-V2 的 40.75%/8.00% 和 YUME 的 32.00%/58.00%。计数评估覆盖 400 个抽样帧，状态评估覆盖 50 个死亡事件、每事件 3 个转换后帧。结果支持显式状态对该程序化场景的一致性约束；视觉生成器遵循外部已定义规则，不等于从观测中识别出了真实物理机制。 [正文实验与表格](https://arxiv.org/html/2609.10540v1)。

### 代码与数据

当前仓库仅见 README 与 assets，尚不能认定训练/推理代码可复现。 以上状态核验于 2026-09-14；入口和目录存在不等于已经运行复现实验。

### 局限、失败案例与开放问题

程序提供状态和转移规则，实验集中在 CombatStateBench；规则不完整、外部状态估计错误和连续接触动力学会限制迁移。

### 总结讨论：与知域的关系
命中「世界模型中的显式状态」趋势，与 TourPhysics（#10）、World in World（#8）构成「世界模型外挂机制」三方案：物理模拟（TourPhysics）、程序状态（PWM）、推理期接口（WiW）。对知域 world model 专题是状态建模路线的新证据。

## 14. TourPhysics: Bringing Physics to World Models for Exploration and Manipulation from a Single Image

- **作者**：Xin Zhang, Yabo Chen, Zixuan Duan, Haibin Huang, Chi Zhang, Feng Xu, Xuelong Li
- **年份与发表**：2026，arXiv 预印本，v2
- **arXiv ID**：2609.04911
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.04911)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.04911)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：未在 arXiv 页面发现项目页链接
- **代码**：未公开
- **数据**：未公开
- **模型**：未公开
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.04911)
- **类别标签**：world model, physics, video generation, 单图重建
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文（v1 提交于 2026-09-04，v2 提交于 2026-09-07，窗口内有实质性修订）
- **首次提交**：2026-09-04T09:15:03Z
- **最近修订**：2026-09-07T04:56:06Z
- **arXiv 主分类**：cs.CV
- **正文**：[arXiv HTML v2](https://arxiv.org/html/2609.04911v2)

### 核心内容与 Insight
交互式视觉世界模型必须区分观测与物理干预：相机运动揭示新表面，干预改变物体运动、接触与形变。现有视频世界模型多由外观先验驱动，长程常丢失物理或空间一致性。TourPhysics 是从单张图初始化的在线框架（扩展自团队 ACM MM 2026 工作 PhysOmni），把确定性模拟与视频生成结合，为模拟器状态、几何证据、生成器控制与外观记忆分配独立角色。每个动作：模拟器先计算有限物理与相机轨迹，再生成对应观测；被接受的观测发布终端状态并更新外观记忆与后续生成器控制，已提交状态与模拟器几何在合成与重试期间保持不变。区分用于投影/可见性的模拟器几何与用于条件化生成器的相对深度；reference-anchored 记忆通过几何跨视角对应检索已接受的静态外观。

### Pipeline
**输入**：单张图像 + 声明式物理配置。
**过程**：模拟器计算物理+相机轨迹 → 生成器合成观测 → 接受/拒绝（物理一致性判定）→ 发布终端状态，更新外观记忆 → 下一动作（记忆通过几何对应检索）。
**输出**：长程一致的探索/操作视频，遵循指定的相机与物体轨迹。

### 实验与证据

正文表 2 明确列出输入先验和有效样本范围：相机 ATE 为 0.0233，物体 ADE 为 0.0297，S@0.05 为 81.18%；相机指标使用 40 个输入身份的 49 条轨迹，物体指标使用 49 个身份、93 条轨迹中的 168 个物体。表 3 的碰撞/形变指标是相对于模拟器配对渲染轨迹的图像空间代理，VideoPhy-2 只作辅助感知诊断。部分基线视频经过时间拉伸，且本方法额外获得声明式物理配置；因此不应把表中差异解释为相同信息条件下的纯模型优劣。 [正文实验与表格](https://arxiv.org/html/2609.04911v2)。

### 代码与数据
未公开。

### 局限、失败案例与开放问题

额外物理配置与模拟器状态构成强输入先验；对模拟轨迹的图像匹配不能证明视频生成器自身学会了真实物理。

### 总结讨论：与知域的关系
直接命中「世界模型中的物理 grounding」与「交互式世界模型」，与知域 8/30 物理世界模型专题、馆藏 PhysOmni 系工作衔接。其「观测-干预分离」视角对因果世界模型讨论有意义（区分被动观测与主动干预）。

## 15. Pelican-Sim 1.0: A General World Model Simulator for Embodied Intelligence

- **作者**：Shilong Zou, Shilin Zhang, Yingji Zhang, Yuhang Huang, Yi Zhang, Zeyuan Ding, Han Dong, Junwei Liao, Yong Dai, Jian Tang, Xiaozhu Ju
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.12036
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.12036)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.12036)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[Pelican-Sim 1.0](https://zoushilong1024.github.io/Pelican-Sim1.0/)
- **代码**：[官方仓库](https://github.com/ZouShilong1024/Pelican-Sim1.0)（官方项目链接对应此仓库，当前只有 README、许可证与 gitignore，完整实现尚未公开。）
- **数据**：约 100 万条真实与仿真轨迹；未发现完整数据下载页
- **模型**：项目/仓库状态待核验
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.12036)
- **代表图链接**：[论文 Figure 1：统一世界模拟器及四类下游用途](https://arxiv.org/html/2609.12036#S1.F1)
- **类别标签**：Embodied World Model, Action-Conditioned Video, Cross-Embodiment, Policy Optimization
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-10T17:51:01Z
- **最近修订**：2026-09-10T17:51:01Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.12036v1)

### 核心内容与 Insight

Pelican-Sim 1.0把异构机器人的动作归一到 28 维数值接口，并把 URDF/相机渲染的动作视频作为连接动作和像素的中间条件。Sparse MoE吸收跨域动力学差异，因果适配与少步蒸馏将生成压缩为四步自回归 rollout。

### Pipeline

**输入**：初始 RGB、28 维统一动作值、相机对齐动作视频。

**过程**：Video DiT 与 sparse MoE 预测未来帧；动作视频注入提升空间控制；35 步模型经因果适配和蒸馏变为四步生成器；微调 VLM 评分器用于数据筛选、策略评价、动作选择与 GRPO 优化。

**输出**：动作条件未来视频、策略分数、候选动作选择和想象 rollout 奖励。

### 实验与证据

相对融合 baseline，动作视频注入 PSNR 提升 0.904；sparse MoE 相对 dense backbone 的 FVD 降低 6.530；四步生成相对 35 步获得 5.67 倍加速。在 RoboTwin 中，每任务 50 个真实演示加 500 个生成轨迹将策略成功率从 70% 提高到 93%；五个 checkpoint 的策略评价 Pearson 相关为 0.994；动作选择和策略优化相对成功增益为 47.7% 和 20.3%。这些结论依赖同一基准和 VLM 评价器，相关性不能解释为跨平台因果有效性。 [正文实验与表格](https://arxiv.org/html/2609.12036v1)。

### 代码与数据

官方项目链接对应此仓库，当前只有 README、许可证与 gitignore，完整实现尚未公开。 以上状态核验于 2026-09-14；入口和目录存在不等于已经运行复现实验。

### 局限、失败案例与开放问题

统一数值动作不足以完全描述控制频率、顺应性和硬件延迟；动作视频渲染依赖可靠 URDF 与标定。生成器与 VLM 评分器可能共享视觉偏差，世界模型错误会被下游选择和优化放大。

### 总结讨论：与知域的关系

该工作覆盖 Egocentric/World Action Model 的规模化训练与闭环使用，并提供与 Flow WAM、X-WAM 比较的系统级参照。

## 16. FARM: Reading Failure Signals from the Internal Predictive States of a Frozen Robotic World Model

- **作者**：Haoran Pei, Mingrui Luo, Senbao Wang, Haoran Lv, Jie Guo, Sheng Zhong, Ruixi Ci
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.11445
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.11445)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.11445)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：未发现
- **代码**：[官方仓库](https://github.com/HaoranPei-casia/FARM)（仓库含 src、configs、data_indices、examples 和 tests；数据使用条件见 DATA.md。）
- **数据**：10-task benchmark 与 PIPER X、SO-101、Franka 真实机器人数据；未发现独立下载
- **模型**：使用冻结 VLA-JEPA；未新增公开权重
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.11445)
- **代表图链接**：[论文 Figure 1：冻结预测状态上的失败读出](https://arxiv.org/html/2609.11445#S3.F1)
- **类别标签**：World Model Monitoring, Failure Detection, Frozen Representation, Causal History
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-10T12:14:37Z
- **最近修订**：2026-09-10T12:14:37Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.11445v1)

### 核心内容与 Insight

FARM不重新训练世界模型，只在冻结 VLA-JEPA 的内部预测状态上训练一个 33,985 参数读出头，输出逐步失败概率并沿仅包含过去的轨迹聚合风险。研究问题是预测 latent 是否已编码部署失败，而非再构造一个专用生成模型。

### Pipeline

**输入**：当前及历史观测、语言、动作条件下的冻结世界模型内部状态。

**过程**：压缩预测 token 为 32 维失败表示；监督小型读出器；使用时间因果的前缀聚合得到轨迹风险。

**输出**：逐步失败分数和在线轨迹风险。

### 实验与证据

正文表 II 的 350 条轨迹、五折 OOF 检验得到 pooled AUROC/AUPRC 85.68/88.59。表 III 的匹配 10-task 评测中，FARM 在 Seen pooled 为 83.70/83.19，在 Strict-Unseen 为 65.67/69.38；Strict-Unseen 下 STAC-Single 达到 68.28/74.62，说明源任务优势未全部迁移。训练型方法平均 3 个种子，Adapt-35 每任务每外折使用 35 条目标标注轨迹。0.2256 ms 是已有世界模型状态之后的监控器增量延迟，不含世界模型预测总成本。 [正文实验与表格](https://arxiv.org/html/2609.11445v1)。

### 代码与数据

仓库含 src、configs、data_indices、examples 和 tests；数据使用条件见 DATA.md。 以上状态核验于 2026-09-14；入口和目录存在不等于已经运行复现实验。

### 局限、失败案例与开放问题

监督读出会继承训练任务的失败定义和类不平衡；对新硬件的固定读出迁移有限。风险可预测性可能来自视觉异常相关线索，而非动力学因果结构。

### 总结讨论：与知域的关系

FARM为 WAM/VLA-JEPA 增加部署可靠性维度，可与 Causal-JEPA 类表示研究结合，但应明确其属于时间因果掩码和风险预测，不是因果识别。

## 17. IMPLY: Physically Anchored Consistency for World-Model Rollouts

- **作者**：Aman Mehta, Riya Baviskar
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.12441
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.12441)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.12441)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：未发现
- **代码**：未发现
- **数据**：使用 CALIPER 对象与 V-JEPA 2-AC 场景适配实验
- **模型**：不适用
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.12441)
- **代表图链接**：[论文 Figure 1：自一致性与物理锚定一致性的受控比较](https://arxiv.org/html/2609.12441#S4.F1)
- **类别标签**：World Model Evaluation, Physical Consistency, Intervention Evidence, Rollout Selection
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-11T05:02:08Z
- **最近修订**：2026-09-11T05:02:08Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.12441v1)

### 核心内容与 Insight

IMPLY指出，多次 rollout 彼此一致仍可能全部忽略当前物体。方法通过反演模拟器，读取每个推动结果隐含的质量和摩擦，并加入模型已观察到的两次校准推动，检查一个物理对象是否能同时解释所有 rollout。

### Pipeline

**输入**：不同推动速度下的动作条件 rollout，以及两个真实观察到的校准推动。

**过程**：从像素或 latent 读取位移；反演模拟器拟合质量 \(m\) 和摩擦 \(\mu\)；计算联合拟合残差作为物理锚定不一致分数。

**输出**：rollout 集的可信度分数及候选集合排序。

### 实验与证据

在 200 个对象、每对象 5 个速度的受控 stand-in 中，对象盲模型的自一致性 AUROC 仅 0.70，加入锚定后为 1.00；最低锚定不一致选择的中位位移误差 1.5 mm，接近 oracle 1.6 mm，而首样本为 7.1 mm。对场景适配的 V-JEPA 2-AC，正确对象校准与真值相关 0.91，错误对象仅 0.05；锚定分数选择正确证据 73%，自一致性 52%。结果强力支持“必须用观测证据锚定”，但只在简单推动与可参数化物理中验证。 [正文实验与表格](https://arxiv.org/html/2609.12441v1)。

### 代码与数据

未发现代码和复现实验包。方法依赖模拟器反演、位移读出与校准推动协议。

### 局限、失败案例与开放问题

当前物理模型主要是质量—摩擦—位移关系，难以直接推广到抓取、柔性物体、多接触和视觉遮挡。两次真实校准不是零成本；位移读出误差和模拟器失配会影响评分。

### 总结讨论：与知域的关系

IMPLY为世界模型的因果/反事实讨论提供重要边界：它使用干预式观察锚定 rollout，但尚不是结构因果识别；适合作为 WAM 可信度评测模块。

## 18. Beyond Visual Quality: Evaluating Physical Consistency under Ego-Motion with EgoGenEval

- **作者**：Yilin Long, Chenming Zhu, Zitang Gou, Jingli Lin, Tai Wang
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.11172
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.11172)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.11172)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：未发现独立项目页（代码在 GitHub）
- **代码**：论文或项目列出 `https://github.com/InternRobotics/EgoGenEval`，2026-09-14 访问返回 404；当前公开状态待核验。
- **数据**：EgoGenEval 基准 + EgoGen-Train 训练集
- **模型**：不适用（基准）
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.11172)
- **类别标签**：世界模型评测, egocentric, 物理一致性, 基准
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-10T07:19:50Z
- **最近修订**：2026-09-10T07:19:50Z
- **arXiv 主分类**：cs.CV
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.11172v1)

### 核心内容与 Insight
视觉生成器生成高保真图像但常在 ego-motion 下违反物理一致性，限制空间推理与具身规划使用。现有基准多聚焦孤立图像或单步质量。EgoGenEval 是几何接地、pose-free 的基准：1,400 例 / 2,360 目标视角，覆盖单步与多步 ego-motion；分别度量 Camera Motion Grounding（CMG）与 Scene State Preservation（SSP），双指标经盲人评判验证。16 个 pose-free 生成器 + 2 个 pose-conditioned 参考的评测发现：现有模型难以在执行相机运动的同时保持场景状态，没有系统能在两轴同时做好。并构建 EgoGen-Train（同几何来源）验证基准数据能否改进能力。

### Pipeline
**输入**：源视图 + ego-motion 描述（pose-free 设定）。
**过程**：几何接地生成案例（1,400 例）→ CMG（相机运动接地）与 SSP（场景状态保持）双指标 → 盲人评判验证指标 → EgoGen-Train 微调生成器。
**输出**：生成器物理一致性的标准化评测 + 改进数据。

### 实验与证据

正文主表分别列出 16 个 pose-free 模型与 2 个 pose-conditioned 参考系统；两类输入权限不同，不混合排行。GPT-Image-2 的 CMG/SSP 为 0.72/0.60，而 GT-target oracle 为 0.98/0.90；高视觉质量尚不能保证相机运动接地与场景状态保持。论文给出人类一致性和评分校准。指标主要针对跨视角几何、对象/场景状态，不覆盖接触力、摩擦或材料响应；“本批最强评测证据”不能靠模型数量直接判定。 [正文实验与表格](https://arxiv.org/html/2609.11172v1)。

### 代码与数据

论文或项目列出的代码地址当前返回 404，不能认定已公开可获取代码。论文中资源发布声明保留为作者声明，数据、权重的实际可获取状态待核验。

### 局限、失败案例与开放问题
pose-free 与 pose-conditioned 系统的输入权限不同，论文将后者单列参考是必要的。人类一致性验证支持所定义的评分任务，但 CMG/SSP 不能覆盖力、材料或接触动力学，GT-target 得分也并非数学上界。

### 总结讨论：与知域的关系
直接命中「世界模型评测」与「egocentric 物理一致性」，是知域证据审计方法论的外部基准资源。对任何声称「世界模型物理一致」的工作，EgoGenEval 是可引用的评测标准。

## 19. How to Learn from What a Human Would Avoid? Intervention-Aware World Models with Real-World RL for Dexterous Manipulation

- **作者**：Jiaju Yin, Zhenhui Zhang, Lixin Xu, Heng Zhang, Jun Shao, Yating Feng, Arash Ajoudani, Renjing Xu
- **年份与发表**：2026，arXiv 预印本，v1；arXiv 作者备注称 CoRL 2026 接收
- **arXiv ID**：2609.06009
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.06009)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.06009)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[WHIRL](https://whirl-dexterous.github.io/)
- **代码 / 数据 / 模型**：未确认公开
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.06009)
- **类别标签**：Dexterous Manipulation, World Model, Human Intervention, Safe RL
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-05T10:28:23Z
- **最近修订**：2026-09-05T10:28:23Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.06009v1)

### 核心内容与 Insight

WHIRL 不把人类接管只当纠错动作，而把“人何时会接管”建模为未来风险。接管事件编码操作者的隐式安全边界，世界模型预测未来接管概率，再作为 actor 的风险 shaping，提前避开高风险区域。

### Pipeline

- **输入**：真实机器人状态、动作、奖励、终止信号和二值接管记录。
- **过程**：训练包含 dynamics、reward、termination、intervention-probability 四个头的 latent world model；策略在 imagined rollout 中联合优化回报和预测风险。
- **输出**：具备主动避险倾向的灵巧手策略。

### 实验与证据

在 16-DoF LEAP Hand 上覆盖规则/不规则物体抓取、棱柱操作和长时任务。摘要报告复杂抓取成功率 96.7%，按步数加权的干预负担最多下降 84%。这支持所测真实任务中的风险 shaping 收益，但未证明对不同操作者、风险偏好或机器人普遍成立；摘要未给完整方差和失败分布。 [正文实验与表格](https://arxiv.org/html/2609.06009v1)。

### 代码与数据

项目页存在；未确认代码、训练数据或权重已实际开放，不能认定可复现。

### 局限、失败案例与开放问题

二值接管混合反应延迟、注意力和个人风险偏好；接管概率是风险代理，不是事故概率。需检查漏接管状态是否被误标安全，并研究跨操作者校准。

### 总结讨论：与知域的关系

连接灵巧 HOI、真实机器人 RL 和动作条件世界模型。重要启发是：不仅学习人做了什么，也学习人拒绝进入哪些状态。

## 20. CST-WM: A Causally Structured World Model for Embodied Visual Tracking

- **作者**：Junyi Hu, Shuaihang Yuan, Yi Fang
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.06302
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.06302)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.06302)
- **代码 / 模型**：未确认公开
- **数据**：EVT-Bench、Habitat 3.0
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.06302)
- **类别标签**：Causal World Model, Embodied Tracking, Action Leakage, MPC
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **项目**：[官方项目](https://junyi2005.github.io/cst-wm/)
- **首次提交**：2026-09-05T23:24:32Z
- **最近修订**：2026-09-05T23:24:32Z
- **arXiv 主分类**：cs.CV
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.06302v1)

### 核心内容与 Insight

CST-WM 针对 embodied tracking 的“因果幻觉”：模型可能把动作直接写入目标状态。它将 latent 拆为 target-evidence、robot、observation 三支，并阻断不合理的 action-to-target shortcut。

### Pipeline

- **输入**：机器人观测、动作和目标信息。
- **过程**：按预设因果路径学习结构化 latent transition，并在 rollout 上用 MPC 选动作。
- **输出**：未来 belief/latent、跟踪动作和重捕获行为。

### 实验与证据

正文表 4 在 EVT-Bench 上报告 SR/TR/CR 为 88.7/83.4/1.41，对比 TrackVLA++ 的 86.0/81.0/2.10；表 5 的长遮挡重捕获率为 0.69，对比 Adapted NWM 的 0.54。表 3 给出 scene-disjoint 数据划分、3 个随机种子、模型容量和 CEM 参数。结构消融与 action-leakage 诊断支持阻断指定任务中的动作捷径；这依赖“机器人动作不直接改变目标自身状态”的任务假设，不能原样迁移到手物接触操纵。 [正文实验与表格](https://arxiv.org/html/2609.06302v1)。

### 代码与数据

公共环境存在，论文实现与权重未确认。

### 局限、失败案例与开放问题

预设图可能遗漏目标自身动力学与遮挡者运动；机器人与目标真实接触时，动作到目标状态的直接影响并非错误边。

### 总结讨论：与知域的关系

提供具体可测的因果捷径问题，可与 Causal-JEPA 对照，也提醒因果边应随物理关系变化。

## 21. Learning Counterfactual World Models for Embodied Reasoning under Partial Observability

- **作者**：Todd Y. Zhou, Daniel Zhang
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.05834
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.05834)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.05834)
- **代码 / 模型**：未确认公开
- **数据**：Occluded Push、Aliased Maze、Deferred Kitchen 等任务
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.05834)
- **类别标签**：Counterfactual Reasoning, Partial Observability, Intervention
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-05T02:56:47Z
- **最近修订**：2026-09-05T02:56:47Z
- **arXiv 主分类**：cs.AI
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.05834v1)

### 核心内容与 Insight

论文提出 counterfactual collapse：未来视觉上合理，却不能区分不同动作干预的后果。CLWM 使用 recurrent belief、action-conditioned latent dynamics 和 contrastive counterfactual objective，使同一历史下的不同 intervention futures 可分。

### Pipeline

- **输入**：部分可观测历史、候选动作及后续观测。
- **过程**：更新 belief，按动作预测 latent future，并用对比目标拉开不同干预后果。
- **输出**：用于 reasoning/planning 的 future latent。

### 实验与证据

正文表 1 给出 5 个种子、每模型 100 个固定测试 episode：Occluded Push 成功率 74.6±1.5% 对 65.1±1.6%，Aliased Maze 78.9±1.4% 对 67.3±1.5%，其中 ± 为种子均值标准误；Deferred Kitchen exploit rate 从 18.4% 降至 9.7%。表 2 中移除 perceptual-alias negatives 后 Push/Maze 降至 67.5/69.1，支持反事实负样本作用。所有模型从头训练，作者明确未在大规模预训练 encoder 上测量，不能直接外推到视频基础模型。 [正文实验与表格](https://arxiv.org/html/2609.05834v1)。

### 代码与数据

未确认实现、环境和权重开放。

### 局限、失败案例与开放问题

反事实分支来自环境构造，不等同现实中不可观测的潜在结果；对比目标可能学动作分类捷径。需测试 unseen intervention、隐藏混杂和多步累积。

### 总结讨论：与知域的关系

直接命中反事实世界模型，提供比 temporal causal attention 更明确的 intervention-level 目标。

## 22. Identifying Habit, Physics, and Nuisance in Robot World Models

- **作者**：Jinting Hang, Zhenhui Cai
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.09210
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.09210)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.09210)
- **代码 / 模型**：未确认公开
- **数据**：StackCube、DROID、RH20T
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.09210)
- **类别标签**：Structural Causal Model, Robot World Model, Intervention, Adaptation
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-06T00:20:22Z
- **最近修订**：2026-09-06T00:20:22Z
- **arXiv 主分类**：cs.RO
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.09210v1)

### 核心内容与 Insight

论文用 SCM 区分操作者习惯、共享物理和观测干扰：\(a=g(h,z,u)\)、\(z'=f(z,a)\)、\(o=r(z,c)\)。多模态示范常来自选动作习惯，而非物理随机；若排除限制成立，应冻结共享 dynamics，只适配薄接口。

### Pipeline

- **输入**：状态或图像、动作、操作者/命令信息和下一状态。
- **过程**：训练动作条件动力学；用动作替换/打乱、操作者交换、外观与相机扰动测试路径；比较 freeze、finetune、scratch。
- **输出**：下一状态预测、habit-aware reverse score 和适配接口。

### 实验与证据

StackCube 错误动作使误差约增 10.4 倍，16-shot 下 freeze+interface 优于 finetune/scratch；DROID 图像中错误动作约增 9.5 倍而外观扰动比值近 1；多步错误动作比随 horizon 增大。闭环仅仿真。证据是对 SCM 排除限制的代理检验，不是无条件 causal identification。 [正文实验与表格](https://arxiv.org/html/2609.09210v1)。

### 代码与数据

使用公开数据和仿真环境，但实现与权重未确认公开。

### 局限、失败案例与开放问题

跨任务 habit transfer 不确定，跨相机退化明显；若习惯改变接触参数，\(h\to z\) 不可忽略，冻结 dynamics 会错设。

### 总结讨论：与知域的关系

价值主要在干预诊断协议，可直接启发 Causal-JEPA 增加可证伪的动作/外观对照。

## 23. RodForesight: A World Model Enhanced Diffusion Policy for Slender and Material Agnostic Rod Insertion

- **arXiv ID**：2609.12103
- **类别标签**：World Model, Diffusion Policy, Contact-Rich Manipulation, Action Selection
- **更新类型**：新论文
- **作者**：Chuanbo Yu, Mingyu Yue, Yan Lyu, Chuhan Song, Peng Wang
- **论文**：[arXiv](https://arxiv.org/abs/2609.12103)
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.12103)（预印本标识，非期刊 DOI）
- **首次提交**：2026-09-10T18:31:55Z
- **最近修订**：2026-09-10T18:31:55Z
- **arXiv 主分类**：cs.RO
- **年份与发表**：2026，arXiv 预印本，v1
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.12103v1)
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。

### 核心内容与 Insight

RodForesight 用低维杆尖—孔几何后果对候选动作排序：先用视觉伺服缩小初始状态范围，再让世界模型筛选扩散策略提出的接触敏感动作。它把“预测是否有用”落实为执行前的动作选择。

### Pipeline

- **输入**：杆与孔的两帧语义 mask、当前几何状态及扩散策略候选。
- **过程**：粗接近进入 hand-off 区域；扩散策略生成 8 组 16 步候选，GRU 世界模型预测径向、深度、倾斜变化；选择预测对齐更好的动作块并执行前 4 步。
- **输出**：完成细杆插入的闭环动作与预测几何后果。

### 实验与证据

正文使用 Cosserat 杆与接触模型构造分支监督：300 条成功示范、6,654 个窗口、53,232 条匹配分支。表 II 中两阶段无世界模型为 88.9%，Transformer 世界模型为 93.3%，GRU 版本为 96.7%；位置/初始姿态泛化的总体成功率为 87.5%。表 V 的 623 组候选比较中，全体动作精确命中率仅 3.4%，但 regret 为 0.025；应看候选近似等价性和 regret，不能只看是否选中同一个 oracle 动作。 [正文实验与表格](https://arxiv.org/html/2609.12103v1)。

### 代码与数据

原始论文未提供可确认的公开代码、数据或模型下载入口，开放状态待核验。

### 局限、失败案例与开放问题

评测依赖 Cosserat 动力学、已设材料与接触参数，不能表述成已完成真实制造产线验证。两阶段分解本身带来很大收益，世界模型的独立贡献应与两阶段无模型基线比较；稀疏多样候选子集仅 28 组。

### 总结讨论：与知域的关系

作为“低维物理后果能否改善动作排序”的直接案例，与 4D 接触表征和可靠 rollout 专题衔接。

## 24. Beyond Task Success: Stage-Wise Reliability of World Model Planning under Sensing Degradation

- **arXiv ID**：2609.07126
- **类别标签**：World Model, Reliability Evaluation, Planning, Sensing Degradation
- **更新类型**：新论文
- **作者**：Geonmyeong Lee, Byoung-Tak Zhang
- **论文**：[arXiv](https://arxiv.org/abs/2609.07126)
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.07126)（预印本标识，非期刊 DOI）
- **首次提交**：2026-09-07T07:19:37Z
- **最近修订**：2026-09-07T07:19:37Z
- **arXiv 主分类**：cs.RO
- **年份与发表**：2026，arXiv 预印本，v1
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.07126v1)
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。

### 核心内容与 Insight

该工作把感知退化逐级追踪到表示、未来预测、动作偏好和最终结果。重要发现是误差影响不会按固定比例逐层传播，因此只看任务成功或 latent 距离都会遗漏规划脆弱点。

### Pipeline

- **输入**：相同起终点任务的干净/退化观测历史，以及冻结世界模型和规划器。
- **过程**：施加 10 类视觉/时间退化，配对比较表示偏移、未来预测偏移、候选动作排名和闭环成功；用另一任务与另一世界模型检查结论范围。
- **输出**：分阶段退化诊断及规划器实际暴露于损坏观测的条件统计。

### 实验与证据

主评测使用 DINO-WM、OGBench OGBScene Drawer 的同一组 50 个可重规划任务。表 2 的 Cube 补充实验中，DINO-WM 在 Motion blur 下 14/17 成功、Low-light 下 8/17；LeWM 分别为 11/15 和 2/15。分母是各模型干净条件下成功的子集，不是统一总体。Delay-10 还需区分真正暴露于延迟的规划步骤，避免重规划掩盖错误动作排序。 [正文实验与表格](https://arxiv.org/html/2609.07126v1)。

### 代码与数据

原始论文未提供可确认的公开代码、数据或模型下载入口，开放状态待核验。

### 局限、失败案例与开放问题

退化为受控合成条件，模型与任务覆盖有限；分阶段相关和配对退化不等于已经证明修复某一表示就能恢复闭环表现。不同模型的干净成功子集不能直接当作同分母排名。

### 总结讨论：与知域的关系

为本专题“错误来自哪里、是否影响动作”的实验协议提供直接参考，可作为新的 4D/接触接口实验的诊断层。

## 25. MINT: A Unified Model for World-Space Camera and Hand Motion Estimation from Scalable Egocentric Pipeline Supervision

- **作者**：Zijie Zhu, Weiren Cai, Yizhou Wang, Zhenjie Yang, Yide Liu, Jiahao Chen, Guanqi He
- **年份与发表**：2026，arXiv 预印本，v2
- **arXiv ID**：2609.04958
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.04958)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.04958)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：未在 arXiv 页面发现项目页
- **代码**：将开源（作者声明，含标注管线）
- **数据**：发布 1,021 小时 egocentric 轨迹数据集
- **模型**：将开源（作者声明）
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.04958)
- **类别标签**：egocentric vision, hand motion, camera trajectory, 数据管线, HOI
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文（v1 上周期边界，v2 窗口内；馆藏无此记录）
- **首次提交**：2026-09-04T10:05:11Z
- **最近修订**：2026-09-08T08:22:56Z
- **arXiv 主分类**：cs.CV
- **正文**：[arXiv HTML v2](https://arxiv.org/html/2609.04958v2)

### 核心内容与 Insight
从 egocentric 视频恢复世界坐标下的相机与手部运动是活动理解、机器人学习与 AR 的关键能力。现有系统分阶段处理（相机运动、深度估计、手部重建、轨迹精化），计算开销大且无法联合建模。MINT 从单一共享时空视频表示，联合预测相机轨迹、视场角（FoV）、相机帧手部状态与逐帧手部可观测性，再通过显式坐标变换得到世界空间手部运动。训练数据稀缺的解法是开源标注管线 EGOPIPELINE：把大量公开 egocentric 视频转换为结构化相机与手部轨迹监督；MINT 先在大规模伪标签上预训练，再在小规模高质量标注上微调。

### Pipeline
**输入**：egocentric RGB 视频。
**过程**：共享时空表示 → 联合预测相机轨迹/FoV/手部状态/可观测性 → 显式坐标变换 → 世界空间手部轨迹；EGOPIPELINE 生成伪标签用于预训练，小规模高质量标注微调。
**输出**：世界空间手部运动轨迹 + 相机轨迹。

### 实验与证据

正文表 1 区分 MINT 与 MINT+UKF：HOT3D 上基础模型 PA-MPJPE-p/EPE-p 为 13.656 mm/55.117 px，UKF 后为 13.646 mm/55.058 px；jitter 从 12.057 降至 2.373 mm/frame²，FAcc 均为 0.945。表 2 的 HOT3D 平均 RPE-T 为 4.694 mm、RPE-R 为 0.284°；摘要写作 4.690 mm，存在细小文本差异，本卡采用表格值。零样本手部结果与相机指标共同支持监督管线摊销的价值，但相机平移、旋转、尺度和手部误差不可合并成一个“全面 SOTA”判断。 [正文实验与表格](https://arxiv.org/html/2609.04958v2)。

### 代码与数据
模型、训练/推理代码、标注管线与 1,021 小时数据集将发布，是本周 egocentric 方向数据基础设施的重要资产。

### 局限、失败案例与开放问题

UKF 改善时间平滑但引入后处理；世界坐标输出依赖相机和尺度估计，伪标签中的系统误差可能传递到下游世界模型。

### 总结讨论：与知域的关系
命中 egocentric vision + HOI + 世界空间轨迹，与 Coherent4D（#12）共同提供「世界空间轨迹」型监督资产。对知域 egocentric world model 方向是数据与基线双重补充。

## 26. From Where to How: Continuous 4D Interaction Forecasting from Egocentric Video

- **作者**：Qiaohui Chu, Haoyu Zhang, Meng Liu, Haoxiang Shi, Dongmei Jiang, Liqiang Nie
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.08636
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.08636)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.08636)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[From Where to How](https://corrineqiu.github.io/from-where-to-how/)
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.08636)
- **类别标签**：Egocentric Video, 4D Interaction, HOI Forecasting, Flow Matching
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **代码**：[官方仓库](https://github.com/CorrineQiu/from-where-to-how)（仓库包含项目网站、data 与 process 目录，完整训练权重和数据下载范围需按仓库说明核验。）
- **首次提交**：2026-09-08T12:06:23Z
- **最近修订**：2026-09-08T12:06:23Z
- **arXiv 主分类**：cs.CV
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.08636v1)

### 核心内容与 Insight

论文将“未来在哪里交互”和“身体如何运动”统一为连续 4D 预测。Coherent4D 约 233K 样本、三个域，每个样本把未来 3D 交互位置与全身姿态在同一坐标和时间轴对齐；HIGFlow 采用 where-to-how 级联。

### Pipeline

- **输入**：egocentric 历史视频。
- **过程**：融合语义 grounding 与短时动态预测未来 3D 交互位置；以位置序列条件化 deterministic motion anchor，再用 residual flow matching 生成全身运动。
- **输出**：时间对齐的未来 3D 交互位置与全身姿态序列。

### 实验与证据

正文表 I 列出 Coherent4D 的 233,828 个样本：193,598/20,484/19,746 train/val/test，覆盖 Cooking、Health、Bike Repair 三域。表 II 的位置 ADE（mm）依次为 Health 40.21、Bike Repair 80.91、Cooking 93.46，对比 FIction 的 40.30、88.55、100.61；Health FDE 则略差（41.44 对 40.58）。表 III 分开报告真值/预测交互位置条件以及 Single/Best-5，不能把真值条件或 best-of-5 当成单次端到端部署效果。 [正文实验与表格](https://arxiv.org/html/2609.08636v1)。

### 代码与数据

仓库包含项目网站、data 与 process 目录，完整训练权重和数据下载范围需按仓库说明核验。 以上状态核验于 2026-09-14；入口和目录存在不等于已经运行复现实验。

### 局限、失败案例与开放问题

预测未来交互位置和姿态不直接给出机器人可执行动作；不同域、真值位置条件、预测位置条件和 best-of-N 必须分别比较。

### 总结讨论：与知域的关系

是 3D/4D HOI 与 egocentric world modeling 的直接交叉，可作为从交互位置预测走向人体—环境联合预测的参考。

## 27. A4A: Cross-Embodiment Transfer of Action-Oriented 4D Affordances from Human Demonstrations

- **作者**：Yifan Han, Litao Liu, Yuqi Gu, Ye Lu, Hanqing Wang, Sidney Wai, Ishaan Myrie, Qi Zhang, Jingjin Yu, Gen Li
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.05892
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.05892)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.05892)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[A4A](https://ru-arcl.github.io/a4a/)
- **代码**：[官方仓库](https://github.com/ru-arcl/a4a)（官方仓库含 code 与 docs 目录；资源入口存在，完整训练复现尚未运行。）
- **数据**：构建超过 80,000 段 4D affordance 视频，其中约 30,000 段为自采 RGB-D；未发现独立下载页
- **模型**：未发现
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.05892)
- **代表图链接**：[论文 Figure 1：Action-Oriented 4D Affordance 概念与跨 embodiment 迁移](https://arxiv.org/html/2609.05892#S1.F1)
- **类别标签**：Human-to-Robot, 4D Affordance, VLA Pretraining, HOI, Cross-Embodiment
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-05T05:23:29Z
- **最近修订**：2026-09-05T05:23:29Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.05892v1)

### 核心内容与 Insight

A4A把人类视频中可迁移的监督定义为“任务条件下交互相关 3D 点未来如何移动”，而不是人体关节或外观。该表示同时携带对象几何、运动方向和作用位置，并弱化人手与机器人末端执行器的形态差异。

### Pipeline

**输入**：人类 HOI 视频/RGB-D 演示、语言任务和机器人观测。

**过程**：GroundingDINO、SAM2、CoTracker3 与深度修正提取交互对象的 3D 点轨迹；预训练阶段用查询点替换机器人状态，并以未来点运动替换动作目标；微调时恢复机器人本体和动作接口。

**输出**：预测的 4D affordance 轨迹，以及经该预训练初始化的机器人动作策略。

### 实验与证据

LIBERO-Object 10 个任务使用 500 条演示、每任务 50 次评估。平均成功率从 Octo 28.2% 提升到 57.2%，OpenVLA 66.4% 到 76.4%，OpenVLA-OFT 98.0% 到 98.6%，\(\pi_0\) 77.8% 到 87.8%，\(\pi_{0.5}\) 94.0% 到 96.0%。多架构一致增益支持表示可迁移，但高基线模型存在天花板效应。真实任务每技能 100 个演示、10 次 rollout，样本规模不足以稳定比较小差异。 [正文实验与表格](https://arxiv.org/html/2609.05892v1)。

### 代码与数据

官方仓库含 code 与 docs 目录；资源入口存在，完整训练复现尚未运行。 以上状态核验于 2026-09-14；入口和目录存在不等于已经运行复现实验。

### 局限、失败案例与开放问题

表示依赖检测、分割、跟踪与深度估计；遮挡、薄物体、透明反光表面和快速接触会产生级联误差。未来点轨迹描述运动后果，但不直接包含力、摩擦或可执行抓取约束。

### 总结讨论：与知域的关系

该工作直接连接从人类视频学习、4D HOI 与 WAM，可作为 HarmoHOI/StreamingHOI 类几何表示进入机器人控制的参考接口。

## 28. Grounding Generated Video Plans in Simulation Towards Versatile Dexterous Controllers

- **作者**：Tianyue Wu, Boyuan An, Shuqi Zhao, Heyu Guo, Wanli Xing, Yi Ma, Kaifeng Zhang, Ruihai Wu, Masayoshi Tomizuka
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.10050
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.10050)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.10050)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[GALATEA](https://boyuan-an.github.io/GALATEA/)
- **代码**：项目页可访问，但本次未找到可确认的实现下载入口，开放状态待核验。
- **数据**：超过 1,500 段生成视频计划被重建并物理落地；未发现独立数据下载页
- **模型**：未发现
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.10050)
- **类别标签**：Dexterous HOI, Video Planning, Simulation Grounding, Human-Object Reconstruction
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-09T11:26:25Z
- **最近修订**：2026-09-09T11:26:25Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.10050v1)

### 核心内容与 Insight

该工作不直接把生成视频像素映射为机器人动作，而是将视频计划重建为手指和物体的联合运动，再在物理模拟器中训练闭环跟踪器。关键 Insight 是：视觉计划只有同时保留代理运动与对象效果，并经过接触动力学验证，才更可能成为可执行控制目标。

### Pipeline

**输入**：文本/任务条件下生成的 HOI 视频。

**过程**：对视频执行少量人工筛选和 HOI 重建，获得手指级与物体轨迹；在模拟器中将其作为噪声参考，采用改进的 tracking-style RL 和优化器训练多计划控制器；部署时由视频模型给出计划，策略闭环跟踪。

**输出**：可执行抓取、推拉、非预抓取交互及抓取后物体姿态调整动作。

### 实验与证据

正文表 I 在 H2O、HO-Cap 各 40 段、每段 150 帧上做 HOI 重建对照；表 II 报告 intent-executing 轨迹的对象位置误差 10.2 mm、旋转 17.4°、手部 36.2 mm，旋转误差并非所有方法中最低。表 III 的未见真机轨迹分为 jar neck、jar top、mug rim、mug handle，各 10 次，总计 27/40 成功（67.5%）。结果支持仿真接地后的轨迹执行，但测试范围与计划筛选机制仍限制泛化结论。 [正文实验与表格](https://arxiv.org/html/2609.10050v1)。

### 代码与数据

官方项目页可访问；本次页面未给出可确认的训练/推理仓库或权重下载入口，代码、数据和模型开放范围待核验。

### 局限、失败案例与开放问题

仍需要人工参与计划筛选/重建；生成视频中的接触穿透和对象身份漂移可能污染参考；模拟器对软体、摩擦和手部接触的建模误差会影响 sim-to-real。训练成本随计划数增长。

### 总结讨论：与知域的关系

这是从人类式/生成 HOI 视频到灵巧控制的关键桥梁，直接关联 Video/WAM、4D HOI 重建和接触物理落地。

## 29. FIRE3D: Feed-forward Interactive 3D Scene Reconstruction Within A Minute

- **作者**：Hongchi Xia, Tianhang Cheng, Wei-Chiu Ma, Shenlong Wang
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.08848
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.08848)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.08848)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[FIRE3D](https://xiahongchi.github.io/Fire3D/)
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.08848)
- **类别标签**：Feedforward Reconstruction, Interactive 3D, Object-Centric Scene
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **代码**：[官方仓库](https://github.com/xiahongchi/Fire3D)（代码包含 training、eval、data_processing 与模型模块；Hugging Face 模型库已确认权重文件，数据集已确认场景 tar 文件，两者当前均非 gated。）
- **首次提交**：2026-09-08T15:01:49Z
- **最近修订**：2026-09-08T15:01:49Z
- **arXiv 主分类**：cs.CV
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.08848v1)
- **模型**：[官方模型文件](https://huggingface.co/hongchi/Fire3D)（已确认存在配置和权重文件）
- **数据**：[官方数据集](https://huggingface.co/datasets/hongchi/Fire3D)（已确认场景 tar 文件；具体子集和许可见数据卡）

### 核心内容与 Insight

FIRE3D 不只恢复可渲染表面，而是在一分钟内生成可模拟的对象级资产，显式输出每个对象的 6-DoF 位姿、包围盒、网格和纹理，使对象物理分离并可交互。

### Pipeline

- **输入**：单张 RGB 或普通 RGB 视频。
- **过程**：估计带位姿 RGB-D，再由端到端前馈网络预测组合式对象场景；无测试时优化。
- **输出**：对象位姿、包围盒、完整网格与纹理组成的 simulation-ready 场景。

### 实验与证据

正文表 3 的 iTHOR 真值感知条件下，CD/PSNR 为 1.38/23.85；推断感知条件下降为 6.15/19.04，输入估计误差仍显著影响结果。表 7 明确区分每物体网络推理 0.601 s 与后处理 4.181 s，含几何与纹理的合计为 4.783 s/物体；还需计入获得 posed RGB-D 的成本。因此“一分钟内”必须结合物体数和上游输入范围理解，不能把 0.60 s/物体当成端到端场景耗时。 [正文实验与表格](https://arxiv.org/html/2609.08848v1)。

### 代码与数据

代码包含 training、eval、data_processing 与模型模块；Hugging Face 模型库已确认权重文件，数据集已确认场景 tar 文件，两者当前均非 gated。 以上状态核验于 2026-09-14；入口和目录存在不等于已经运行复现实验。

### 局限、失败案例与开放问题

对象可交互资产仍依赖输入位姿/深度质量、物体数和后处理；几何完整不自动代表质量、摩擦、刚度或接触动力学正确。

### 总结讨论：与知域的关系

补齐 VGGT/Gen3R 类快速几何恢复到“可交互对象资产”的接口，可用于世界模型或 HOI 仿真初始化。

## 30. HuRo: Robotizing Human Videos for Scalable VLA Pretraining

- **作者**：Jinho Jeong, Se June Joo, Jaehyun Kang, Dongyun Kim, Yena Kim, Hanjung Kim, Seon Joo Kim
- **年份与发表**：2026，arXiv 预印本，v2；arXiv 作者备注称 CoRL 2026 接收
- **arXiv ID**：2609.10706
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.10706)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.10706)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[HuRo](https://3587jjh.github.io/HuRo)
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.10706)
- **类别标签**：Human Video, Robotization, VLA Pretraining, Dexterous Manipulation
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **代码**：[官方仓库](https://github.com/3587jjh/HuRo)（仓库含 pipeline、configs、run_pipeline.sh 和部署说明；完整 142M 帧数据的独立下载范围待核验。）
- **首次提交**：2026-09-09T18:02:05Z
- **最近修订**：2026-09-11T06:22:28Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v2](https://arxiv.org/html/2609.10706v2)

### 核心内容与 Insight

HuRo 把异构 egocentric 视频统一转为机器人观测—动作序列：估计手、相机和语言，做三维运动重定向，去除人臂并叠加机器人。关键证据是规模曲线，以及“视觉+动作端到端预训练”优于只迁移视觉。

### Pipeline

- **输入**：Ego4D、EPIC-Kitchens、EgoDex、EgoVerse、Ego10K 视频。
- **过程**：相机/手追踪；估计世界空间手姿与相机轨迹；语言分段；重定向到 ALLEX；分割修复人臂并渲染机器人；预训练 VLA。
- **输出**：约 630K episodes、142M 帧和下游 VLA 参数。

### 实验与证据

四个真实任务总体完成率 51.5%→80.3%，OOD 34.9%→72.2%。无 overlay 版本 ID 89.4% 略高于 full 88.4%，但 OOD 55.7% 对 72.2%，支持 visual robotization 主要改善所测 OOD。Visual+Action 也优于 Visual Only。结果来自 ALLEX 和有限任务，不是跨机器人 scaling law。 [正文实验与表格](https://arxiv.org/html/2609.10706v2)。

### 代码与数据

仓库含 pipeline、configs、run_pipeline.sh 和部署说明；完整 142M 帧数据的独立下载范围待核验。 以上状态核验于 2026-09-14；入口和目录存在不等于已经运行复现实验。

### 局限、失败案例与开放问题

作者指出 overlay 未显式处理遮挡；缺力觉/触觉；重定向不模拟自碰撞和接触。五源审计仅 55.2% 轨迹无检测到非抓取自接触，因此更适合预训练监督而非直接执行示范。

### 总结讨论：与知域的关系

是从人类视频学习具身策略的大规模证据；其世界空间手运动和相机轨迹可进一步用于显式 3D world-action modeling。

## 31. Dex-X: Learning Visual-Tactile Dexterous Manipulation From Human Videos with Simulated Interaction

- **作者**：Ruoqu Chen, Feixiang Ruan, Liu Cao, Zihao Wang, Botian Xu, Shiqin Tong, Jiajun Liu, Mingzhi Pei, Chenyu Zhang, Wanli Xing, Kaifeng Zhang, Mengdi Xu
- **年份与发表**：2026，arXiv 预印本，v2
- **arXiv ID**：2609.07747
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.07747)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.07747)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[DEX-X](https://dexx-code.github.io/dexx-code/)
- **代码 / 数据 / 模型**：项目页开放状态待核验
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.07747)
- **类别标签**：Human Video, Dexterous Manipulation, Visual-Tactile Learning, HOI
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-07T16:47:39Z
- **最近修订**：2026-09-09T06:54:53Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v2](https://arxiv.org/html/2609.07747v2)

### 核心内容与 Insight

DEX-X 把单目人类示范重建为仿真 hand-object interaction，再用仿真作为“触觉补全引擎”，为只有视觉的人类视频生成接触监督。

### Pipeline

- **输入**：单目人类操作视频。
- **过程**：恢复手—物体运动并转入模拟；生成 tactile supervision；联合点云和触觉训练；zero-shot sim-to-real。
- **输出**：视觉—触觉灵巧操作策略和补全交互数据。

### 实验与证据

正文表 1 的六类仿真任务平均总体成功率为 65.9%，但 In-hand Rotation 仅 36.8%，低于 ManipTrans 的 56.9%；DAPG 只覆盖五类单手任务，不能直接比较其五类平均与六类平均。表 2 的真机 cube picking 为 28/30（93.3%），去触觉后 11/30（36.7%），支持触觉在该任务中的作用。表 3 的未见物体只有 Thin Cube 达 23/30，其他未见形状约为 23.3%–26.7%，跨对象泛化仍有限。 [正文实验与表格](https://arxiv.org/html/2609.07747v2)。

### 代码与数据

官方项目页可访问；本次页面未给出可确认的训练/推理仓库或权重下载入口，代码、数据和模型开放范围待核验。

### 局限、失败案例与开放问题

仿真六任务均值和真机单任务结果不能互相替代；不同类别的基线覆盖不同，未见对象成功率明显低于训练对象。

### 总结讨论：与知域的关系

高度关联 3D HOI、人类视频学习和灵巧操作；接触/触觉可作为检验生成世界物理一致性的额外通道。

## 32. DeCAL: Towards Physically-Grounded Dexterous Vision-Language-Action Models via Contact-Aware Latent Co-Imagination

- **作者**：Yankai Fu, Ning Chen, Junkai Zhao, Heng Zhang, Guocai Yao, Pengwei Wang, Zhongyuan Wang, Shanghang Zhang
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.09119
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.09119)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.09119)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[DeCAL](https://aureleopku.github.io/DeCAL/)
- **代码**：[官方仓库](https://github.com/AureleoPKU/DeCAL)（源码、launch、配置与测试目录已公开；完整训练数据/权重范围待核验。）
- **数据**：六项真实接触任务，每项 100 条高质量演示；未公开下载
- **模型**：未发现
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.09119)
- **代表图链接**：[官方项目方法图：接触门控与视觉—触觉 latent 共想象](https://aureleopku.github.io/DeCAL/#method)
- **类别标签**：Dexterous HOI, Vision-Tactile-Language-Action, Contact Dynamics, World Modeling
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-08T17:47:43Z
- **最近修订**：2026-09-08T17:47:43Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.09119v1)

### 核心内容与 Insight

DeCAL通过 MoT 为理解、想象和动作配置专门专家；接触门控在无接触时降低触觉影响，在接触阶段提高权重；视觉—触觉 latent 共想象联合预测未来外观与力变化，使动作专家获得接触动态线索。

### Pipeline

**输入**：多视角视觉、触觉形变/力、本体状态和语言。

**过程**：视觉与触觉编码后经 Adaptive Visuo-Tactile Fusion 门控；理解、想象、动作专家交换 token；训练期联合学习未来视觉/触觉 latent 和动作生成。

**输出**：灵巧手动作块及辅助性的未来视觉—触觉表示。

### 实验与证据

六项真实任务每项 100 条演示、默认 20 次测试。DeCAL 的六项成功率为 100%、80%、65%、80%、60%、40%，平均约 71%；对比 DECO 为 90%、60%、35%、70%、45%、35%。进度率平均 83.4%。未见物体的 Twist Cap 成功率 75%。结果支持自适应触觉融合，但许多差异只对应 20 次试验中的少数成功；不同 baseline 架构和训练配方仍不完全匹配。平均动作块延迟 0.27 秒。 [正文实验与表格](https://arxiv.org/html/2609.09119v1)。

### 代码与数据

源码、launch、配置与测试目录已公开；完整训练数据/权重范围待核验。 以上状态核验于 2026-09-14；入口和目录存在不等于已经运行复现实验。

### 局限、失败案例与开放问题

依赖特定触觉传感器和遥操作系统；触觉漂移、跨手型标定及传感器损坏会影响门控。任务均为实验室接触操作，跨对象、跨机器人和长期磨损下的泛化证据有限。

### 总结讨论：与知域的关系

DeCAL把接触后果显式加入灵巧 HOI/WAM，可为 StreamingHOI 或 4D HOI 生成引入触觉监督提供依据。

## 33. WM-Craftnet: World Synesthesia Model for Generalizable and Robust Dexterous In-Hand Manipulation

- **作者**：Jie Yin, Zeyuan Zhao, Xiaojing Tan, Yang Liu, Chiyu Wang, Xinyang Gu
- **年份与发表**：2026，arXiv 预印本，v1；arXiv 作者备注称 CoRL 2026 接收
- **arXiv ID**：2609.07002
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.07002)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.07002)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[WM-Craftnet 项目页](https://wmcraftnet.github.io/)
- **代码**：论文或项目列出 `https://github.com/sharpa-robotics/WM-Craftnet`，2026-09-14 访问返回 404；当前公开状态待核验。
- **数据**：未公开
- **模型**：未公开
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.07002)
- **类别标签**：HOI, dexterous, tactile, world model, in-hand manipulation
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-07T03:48:06Z
- **最近修订**：2026-09-07T03:48:06Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.07002v1)

### 核心内容与 Insight
通用且鲁棒的 dexterous in-hand 操作需要从部分、噪声观测推断物体姿态、几何、接触与潜在滑动。WM-Craftnet 是 world-model-conditioned 框架：从本体感觉、深度、触觉与动作学习紧凑的 action-conditioned 潜在动态，由多模态重建与奖励预测监督。关键设计：world model 不用作潜在想象或策略优化，而是作为循环任务上下文（World Synesthesia Model, WSM）供非对称 actor-critic 策略使用。WSM 训练时从噪声深度重建干净深度目标，为真机部署提供去噪几何状态。消融显示预测性世界建模、干净深度监督与触觉接触线索共同塑造学习状态；9 物体预训练的 WSM 作为 49 物体下游策略的可复用先验。

### Pipeline
**输入**：本体感觉 + 深度 + 触觉 + 动作。
**过程**：WSM 学习 action-conditioned 潜在动态（多模态重建+奖励预测监督，深度去噪）→ 作为循环任务上下文 → 非对称 actor-critic 策略生成动作。
**输出**：多物体 in-hand 旋转/操作策略，支持扰动恢复与 sim-to-real 迁移。

### 实验与证据

正文表 1 在九物体 z 轴转动中，完整 WSM 的 Return/RotR 为 753.3±3.6/1.293±0.004；从头训练为 414.3±15.7/0.742±0.012。表 2 的噪声深度监督 Return 为 708.0±3.5，完整 WSM 为 753.3±3.6，表中明确 ± 为 95% CI。训练时通过模拟器提供 clean-depth 监督；它优于噪声目标，但需要额外特权信号。全零触觉仍有 724.9 Return，提示该设置中触觉不是收益的唯一来源。 [正文实验与表格](https://arxiv.org/html/2609.07002v1)。

### 代码与数据

论文或项目列出的代码地址当前返回 404，不能认定已公开可获取代码。论文中资源发布声明保留为作者声明，数据、权重的实际可获取状态待核验。

### 局限、失败案例与开放问题

clean-depth 训练目标来自模拟器，存在特权监督和 sim-to-real 差异；深度、循环状态与触觉的收益需通过匹配控制分别解释。

### 总结讨论：与知域的关系
命中 HOI + dexterous + tactile world model 交叉点，与 DeCAL（#13）共享「触觉进入世界模型」趋势。对知域「Hand-Object Interaction World Model」专题是新证据，尤其「世界模型用作上下文而非想象」这一反直觉设计。

## 34. STAR: Sparse Tactile Representation Learning in Vision-Tactile-Language-Action Models for Dexterous Manipulation

- **作者**：Xiangcheng Liu, Tianhao Wu, Le Zheng, Yidong Wang, Bowen Jiang, Mingjie Pan, Xinlin Ren, Yi Liu, Jianlan Luo
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.12549
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.12549)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.12549)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[STAR](https://stardex-web.github.io/Star/)
- **代码**：未发现稳定独立仓库
- **数据**：约 200 小时、10,576 条轨迹、65 项任务；公开状态待核验
- **模型**：未发现
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.12549)
- **代表图链接**：[论文 Figure 3：STAR 触觉预训练与策略训练流程](https://arxiv.org/html/2609.12549#S4.F3)
- **类别标签**：Dexterous Manipulation, Tactile Representation, VTLA, Sparse Tokens
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-11T07:57:24Z
- **最近修订**：2026-09-11T07:57:24Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.12549v1)

### 核心内容与 Insight

STAR针对灵巧手触觉在时间、空间和信息上的稀疏性，先以高遮蔽率做视觉—触觉联合预训练，再把局部接触 token 与全局触觉 token 分开建模，并用未来触觉预测增强接触阶段表示。

### Pipeline

**输入**：多视角 RGB、每手高维压阻触觉、本体状态与语言。

**过程**：以 75% mask 做跨模态预训练；稀疏—全局触觉编码器选择局部活跃区域并保留全局摘要；在 \(\pi_{0.5}\) 骨干上联合未来触觉预测和流匹配动作训练。

**输出**：50 步动作块及多个未来时间点的触觉预测。

### 实验与证据

数据包含 65 个任务和 10,576 条轨迹，约 69.5% 为灵巧操作。四项真实任务每方法 20 次，STAR 平均成功率/任务完成率为 0.61/0.79，去除 STAR 的 \(\pi_{0.5}\)-Dex 为 0.44/0.61，普通 \(\pi_{0.5}\) 为 0.28/0.44。结果支持完整训练配方，但数据规模、灵巧任务比例与 baseline 预训练差异可能共同贡献，不能把全部提升只归因于单一 sparse token 结构。 [正文实验与表格](https://arxiv.org/html/2609.12549v1)。

### 代码与数据

项目页可访问；未确认 200 小时数据、触觉预训练代码、权重和硬件接口是否完整开放。

### 局限、失败案例与开放问题

触觉阵列维度和布局与具体硬件强绑定；未来触觉预测的时间点固定，可能错过短暂滑移。每项 20 次试验不足以稳定排序相近变体，且未充分报告长期推理频率和传感器故障鲁棒性。

### 总结讨论：与知域的关系

STAR与 DeCAL共同形成触觉 HOI/WAM 板块，强调世界模型不应只预测视觉未来，还需压缩和预测接触信号。

## 35. ArtManip: Category-Level Articulated In-Hand Manipulation

- **作者**：Yang Yang, Tengyu Liu, Puhao Li, Zeyuan Chen, Yuyang Li, Xingwan Wang, Yingying Wu, Zhaopeng Cui, Siyuan Huang
- **年份与发表**：2026，arXiv 预印本，v1
- **arXiv ID**：2609.12498
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.12498)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.12498)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[官方项目](https://artmanip.github.io/)
- **代码**：[官方仓库](https://github.com/youngcv/artgym)（官方项目指向 artgym，包含 isaacgymenvs、rl_games、make_data、脚本和部署说明。）
- **数据**：程序化铰接物体与任务导向抓取资产；未发现公开下载
- **模型**：未发现
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.12498)
- **代表图链接**：[论文 Figure 1：类别级铰接手内操作任务与系统概览](https://arxiv.org/html/2609.12498#S1.F1)
- **类别标签**：Articulated HOI, Dexterous In-Hand Manipulation, Sim-to-Real, Category-Level Generalization
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-11T06:59:21Z
- **最近修订**：2026-09-11T06:59:21Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.12498v1)

### 核心内容与 Insight

ArtManip研究单一策略在同类不同几何和初始抓取下持续开合铰接物体。系统自动生成程序化对象与任务导向抓取，以关节物理随机化和奖励课程训练特权教师，再将 latent 蒸馏到部分观测学生策略。

### Pipeline

**输入**：铰接物体类别、程序化几何、初始抓取与仿真特权状态；部署时使用机器人可观测信号。

**过程**：生成多样对象和抓取；随机化关节阻尼等动力学；课程式 RL 训练教师；latent distillation 训练学生；仿真筛选高质量抓取后零样本部署。

**输出**：22-DoF 灵巧手的连续控制，可重复完成对象开—合循环。

### 实验与证据

仿真未见实例中，Knife、Lighter、Stapler、Tong 成功率为 85.0%、72.1%、83.2%、79.8%；Knife 类从单实例到 30 个训练实例，未见对象成功率从 29.4% 升至 85.0%，支持训练多样性。真实世界 12 个对象、四类、300 次执行中，257 次至少完成一个开合循环，执行级成功率 85.7%。Geo-OOD/Dyn-OOD 的 55.5%/74.9% 仍低于分布内结果，说明几何和动力学外推有限。 [正文实验与表格](https://arxiv.org/html/2609.12498v1)。

### 代码与数据

官方项目指向 artgym，包含 isaacgymenvs、rl_games、make_data、脚本和部署说明。 以上状态核验于 2026-09-14；入口和目录存在不等于已经运行复现实验。

### 局限、失败案例与开放问题

类别仅覆盖四种单关节或近似单关节物体；程序化数字孪生与真实复杂几何仍有差距。策略依赖仿真筛选的初始抓取，尚未形成从视觉识别、抓取获取到持续手内操作的完整闭环。

### 总结讨论：与知域的关系

ArtManip扩展了 HOI 从单次抓取/重建到长时铰接接触控制，可为 4D HOI 表示、接触世界模型和生成式动作规划提供任务基准。

## 36. FOCI Policy: Focus on Object-Centric Interactions for Relational Manipulation Policies

- **作者**：Ze Fu, Pinhao Song, Yutong Hu, Renaud Detry
- **年份与发表**：2026，arXiv 预印本，v1；arXiv 作者备注称 CoRL 2026 接收
- **arXiv ID**：2609.08743
- **DOI**：[arXiv DOI](https://doi.org/10.48550/arXiv.2609.08743)（预印本标识，非期刊 DOI）
- **论文**：[arXiv](https://arxiv.org/abs/2609.08743)
- **正式出版**：未在 arXiv 记录中列出正式出版链接；会议接收信息见年份与发表。
- **项目**：[FOCI Policy 项目页](https://fitz0401.github.io/foci-page/)
- **代码**：论文或项目列出 `https://github.com/fitz0401/foci_policy`，2026-09-14 访问返回 404；当前公开状态待核验。
- **数据**：未公开
- **模型**：未公开
- **AlphaXiv**：[AlphaXiv](https://alphaxiv.org/abs/2609.08743)
- **类别标签**：object-centric, HOI, 关系操作, 数据效率
- **证据等级**：2026-09-14 已核对 arXiv 元数据、正文主要实验与对照；未运行复现实验。
- **更新类型**：新论文
- **首次提交**：2026-09-08T13:35:56Z
- **最近修订**：2026-09-08T13:35:56Z
- **arXiv 主分类**：cs.RO
- **正文**：[arXiv HTML v1](https://arxiv.org/html/2609.08743v1)

### 核心内容与 Insight
object-centric 操作策略通过建模物体运动而非直接预测机器人动作来改善泛化，但现有表示要么过简（无法捕捉交互动态）要么过密（学习效率低）。观察：许多刚体关系操作任务由短交互阶段主导，期间任务相关物体间的相对运动受紧密约束。FOCI Policy 做两层抽象：(1) 时间上——从演示自动提取紧凑交互段；(2) 空间上——用任务相关物体间的相对 SE(3) 运动表示技能，对场景配置与机器人本体不变。

### Pipeline
**输入**：演示（含物体轨迹）+ 场景观测。
**过程**：自动提取紧凑交互段 → 表示相对 SE(3) 运动技能 → 物体间交互建模 → 策略生成物体运动 → 控制器执行。
**输出**：关系操作策略（RLBench/COLOSSEUM/真机）。

### 实验与证据

正文表 1 在八项 RLBench 关系操作中采用 1 次演示、单 RGB-D 相机，每任务 25 个测试并平均 3 次运行；例如 phone_on_base/stack_wine 为 96.0±3.3/97.3±1.9。表 3 扩至 RLBench-18 后，容易接地/难接地任务为 79.6%/7.8%，整体 43.7%；给真值位姿后整体为 88.2%。因此少样本收益依赖任务对象能够正确定位。表 2 的 COLOSSEUM 全扰动成功率为 25.3%，相较其 58.9% 的无扰动结果仍大幅下降。 [正文实验与表格](https://arxiv.org/html/2609.08743v1)。

### 代码与数据

论文或项目列出的代码地址当前返回 404，不能认定已公开可获取代码。论文中资源发布声明保留为作者声明，数据、权重的实际可获取状态待核验。

### 局限、失败案例与开放问题

对象接地是主要瓶颈：困难任务 7.8% 与真值位姿上界的差距明显。相对 SE(3) 表示的结构性质不能替代跨本体实测。

### 总结讨论：与知域的关系
命中 HOI + object-centric + 紧凑段抽象，与知域「交互世界模型」专题相关。其「时间上压缩交互段 + 空间上相对运动」与流式 HOI 的表示设计有方法联系。
