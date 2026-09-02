# 具身 In-Context Learning 专题：视频提示、长上下文与测试时适应

**报告标签**：Embodied ICL, In-context Imitation Learning, VLA, World Action Model, Robot Memory, Test-time Adaptation

**更新日期**：2026-09-02

> 本专题以 Zero-WAM、RoboTTT、HOST、S1、GEN-1.5 和 Dyna-2 为主线，并保留 RA-VLA、PonderPounce 两项相关工作。统一比较上下文是什么、策略在测试时究竟改变了什么、实验探查了什么、证据实际支持什么。RoboTTT 与 HOST 有 arXiv 论文；S1、GEN-1.5 和 Dyna-2 目前只有机构官方研究长文或网页版技术报告，后者的结果均按“作者自报、未外部复现”处理。

## 专题结论

具身 ICL 的关键不是单纯“上下文更长”，而是部署时的新信息能否改变任务语义、阶段判断与动作分布。六项核心工作形成四条路线：Zero-WAM、HOST、S1 直接把人类视频当任务提示；GEN-1.5 把带动作的 sensorimotor 片段作为 physical prompt；RoboTTT 把长历史压入会在推理期做梯度更新的 fast weights；Dyna-2 则主要证明大规模人类视频和未来预测可形成跨 embodiment 的预训练基础，严格说尚未完成单示范 ICL 评测。RA-VLA 和 PonderPounce 分别补足外部检索与执行期 episode memory。

最重要的分类边界是：**上下文条件化不等于参数学习，fast-weight 更新也不等于传统任务微调。** Zero-WAM、HOST、S1、GEN-1.5 的 one-shot 模式、RA-VLA 和 PonderPounce 都冻结模型参数，只改变输入 token、外部检索或 KV/cache 状态；RoboTTT 在每个时间步对专门的 fast model 做梯度更新，但 slow weights 不变；GEN-1.5 还另有 1–10 步梯度适应分支，应与其 zero-gradient ICL 结果分开；Dyna-2 的主要适应发生在预训练与机器人 post-training，而不是由单次示范在测试时触发。

| 工作 | 上下文载体 | 测试时适应位置 | 参数是否更新 | 主要证据与边界 |
|---|---|---|---|---|
| Zero-WAM | 完整人类操作视频 | 视频条件进入 WAM 表征与动作头 | 否 | 7 个未见模拟任务 + 3 项真机；仍缺错配/反转视频干预 |
| RoboTTT | 人类示范、此前观测/动作与失败历史 | TTT fast weights 压缩长历史 | **fast weights 更新**，slow weights 冻结 | 8K context scaling、one-shot、扰动和 DAgger distillation；one-shot 仅 10 次 |
| HOST | 单段人类视频的进度窗口 | 进度定位 → 自身未来观测 → 动作 | 否 | 50 个新技能、基线/SFT、扰动、对齐与级联消融；单一机器人平台 |
| S1 | 单段视频示范 | 视频 prompt 直接条件化策略 | 否 | 1k–100k 小时内部 scaling、4 个长任务、分布偏移和 demo efficiency；无论文/协议不完整 |
| GEN-1.5 | 3–12 秒 sensorimotor physical prompt | 30 秒滚动 context；另有少步梯度分支 | ICL 否；few-step 分支是 | 10 项短任务 one-shot 59%±10%；组合、sim-to-real、人到机器人多为展示 |
| Dyna-2 | 历史视频、语言、状态；大规模人类视频作为预训练经验 | WAM 共享表征与机器人 post-training | 不是单示范测试时适应 | 百万小时 scaling、39 项离线与 14 项真机；属于 ICL 基础而非已证实 ICL |
| RA-VLA | 检索到的行为片段 | action head 分层注入 | 否 | 相关/无关上下文 margin 与检索命中 |
| PonderPounce | 演示 + episode history + cognition | 慢 MLLM cache 向快控制器传 latent | 否 | cognition-null、刷新频率、历史错配 |

## 六项核心工作的共同问题与差异

1. **任务意图从哪里来。** Zero-WAM、HOST、S1 使用人类视频，但训练约束不同：Zero-WAM 用 IFP 迫使表示吸收长程目标；HOST 用显式进度对齐把当前动作目标绑定到演示的未来进程；S1 只披露“以演示定义任务”的 episodic pretraining。GEN-1.5 的 prompt 更接近本体可对齐的传感—动作例子；RoboTTT 同时把跨 episode 示范与 within-episode 历史写进 fast weights；Dyna-2 当前主要从大规模人类视频预训练中获得跨 embodiment 先验。
2. **如何避免模型忽略上下文。** 目前最强的机制证据来自 HOST 的逐级消融、RoboTTT 的 context-length/architecture 对照和 Zero-WAM 的 IFP 消融。S1 的 ICL–language controlled scaling 很有价值，但使用私有内部 benchmark；GEN-1.5 证明插入 prompt 后有可测成功率，却没有公开 no-prompt、wrong-prompt、shuffle-prompt 等完整反事实矩阵；Dyna-2 没有单示范 prompt 干预。
3. **长任务与新技能不能混为一谈。** S1 的卖点是未见任务最长约 10 分钟；RoboTTT 的 Gear Bot 是 5 分钟、10 阶段，但 one-shot 实验另在较短 Circuit 上；HOST 覆盖 50 个未见技能但没有把 10 分钟长程作为主变量；GEN-1.5 明确承认任务简单、短时。因而不能仅按“成功率”横向排名。
4. **“学会”至少有三种含义。** 条件式执行是模型权重不变、行为随 prompt 改变；RoboTTT 是专门 fast weights 的在线梯度状态更新；GEN-1.5 的 few-step adaptation 是常规权重空间微调的极低步数版本。三者的保留能力、成本和安全风险不同。
5. **当前最缺的统一审计。** 同一机器人、同一任务、同一预训练预算下，应同时测正确、缺失、错配、顺序反转、局部剪切和对抗示范，并报告首次成功、完整成功、部分进度、恢复率、延迟、上下文长度、独立种子和失败类型。只有这样才能把“强基础策略恰好会做”与“确实从上下文学会”分开。

## 统一评测建议

1. 同时报告正确上下文、无上下文、错配上下文和打乱上下文。
2. 区分任务成功率、动作敏感性、检索质量和上下文使用强度。
3. 把 token/cache 状态适应、外部检索和参数更新分开，不把它们统称为 test-time learning。
4. 跨 embodiment 时单独评估任务语义迁移与动作坐标对齐。
5. 长任务同时报告阶段完成曲线和错误恢复，避免只用最终二元成功掩盖进度差异。
6. 公司技术长文必须披露任务数、trial 数、随机化、置信区间、数据去污染、基线和失败案例，才可与论文结果同等级比较。

---

## 1. Zero-WAM: In-Context World-Action Modeling from Human Videos for Open-Ended Task Generalization

- **作者**：Jiaming Zhou, Qihang Zhang, Gangwei Xu, Cunxin Fan, Yujie Zhao, Ruilin Wang, Yiming Luo, Shuai Yang, Xing Zhu, Yujun Shen, Junwei Liang, Yinghao Xu
- **年份与发表**：2026，arXiv 预印本（v1：2026-08-26；v2：2026-08-27）
- **arXiv ID**：2608.26103
- **DOI**：10.48550/arXiv.2608.26103
- **可靠入口**：[论文](https://arxiv.org/abs/2608.26103) · [项目](https://robbyant-research.github.io/Zero-WAM/) · [AlphaXiv](https://alphaxiv.org/abs/2608.26103)
- **类别标签**：Embodied ICL, World Action Model, Human Video, Robot Manipulation
- **证据边界**：沿用知域既有来源报告的论文核验；本专题重新分类，不声称完成独立复现。

- **代表图**：Figure 2 : Data construction and in-context human video generation. Top: Task-diverse VA data provide task-balanced robotic video-action pre-training data, while HumanGen contains Pre-train ICL (External), Pre-train ICL (In-house), Simulation ICL, and Real-world ICL pairs. Bottom: the in-context human video generation pipeline converts task-sampled robot videos into human video instructions.。来源：[原图](https://arxiv.org/html/2608.26103v2/data_combine_v1.1.png)

![Zero-WAM: In-Context World-Action Modeling from Human Videos for Open-Ended Task Generalization 代表图](https://arxiv.org/html/2608.26103v2/data_combine_v1.1.png)

### 核心内容与 Insight

Zero-WAM 将具身 ICL 明确定义为：部署时以一段人类操作视频规定未见任务，不更新模型参数，由机器人策略把视频中的目标状态变化翻译为自身 embodiment 下的动作。论文真正解决的是“模型可能无视上下文”的捷径问题：仅做 next-chunk prediction 时，训练任务的局部机器人历史常已足够预测下一步，因此作者加入 in-context future chunk prediction（IFP），迫使主干表示吸收人类视频提供的长程任务信息。

### Pipeline

- **输入**：人类任务演示视频（可附语言）、当前及历史机器人观测与动作。
- **过程**：先以任务均衡方式整理机器人 video-action 数据；再用 VLM、图像编辑和视频生成模型，把机器人轨迹自动转换成语义匹配但背景、视角、物体和 embodiment 可变化的人类视频，构成 HumanGen；模型以人类视频为 prefix memory，因果预测未来机器人视频块，再由 action Transformer 解码动作；IFP 训练分支从当前主干表示预测多个跨步未来视频块，部署时移除。
- **输出**：未来机器人视频块与可执行动作块。

### 实验与证据

RoboTwin 2.0 按任务划分 43 个训练任务和 7 个完全未见测试任务，每任务每个随机种子运行 100 次闭环 rollout，共 3 个种子。Zero-WAM 的宏平均成功率为 46.95%±0.72%，LingBot-VA 为 17.45%±1.40%，WAN-Action 为 10.98%±1.07%；7 个任务全部领先，但最难的三块堆叠仍只有 9.00%±2.16%。真实双臂 Franka 上，物体放容器、三物体顺序操作、双桌腿插入分别为 53.3%、33.3%、16.7%，对照 LingBot-VA 为 43.3%、10.0%、0%。作者还做了人类视频条件、IFP 和任务均衡预训练消融；这些结果支持上下文有贡献，但完整模型同时改变预训练数据、条件模态与目标函数，不能把全部增益单独归因于 ICL。

### 代码与数据

项目页公开，论文详细披露 HumanGen 构建流程和组成；本轮未核验到 HumanGen、训练代码或模型权重的公开下载。HumanGen 中人类视频由生成模型自动合成并经 VLM 筛选，规模大，但真实性、失败过滤误差和生成模型偏差需要独立审计。

### 局限、失败案例与开放问题

训练耗时约 15,360 GPU 小时；HumanGen 依赖闭源或外部生成模型，语义一致性仍可能失真；模拟评测只有 7 个未见任务，真实实验每类 30 次试验且成功率仍有限；“zero-shot”是对测试任务无参数更新，不代表模型没有使用同类任务、目标物或机器人数据。人类视频是否被真正使用，应继续做错配视频、顺序反转视频、相同首帧不同目标视频等反事实测试，而不仅是去掉视频。

### 与知域的关系

以完整人类视频规定未见任务，是“部署前视频示范上下文”的代表；重点审计模型是否真正使用上下文，而非只依赖当前机器人状态。

## 2. RA-VLA: Retrieval-Augmented VLA for Test-Time Adaptation

- **作者**：Sanghwan Jang, Minjin Jeon, Minsoo Kim, Seongjin Choi, Dongha Kim, Hwanjo Yu
- **年份与发表**：2026，ICML 2026；arXiv v1：2026-08-26
- **arXiv ID**：2608.25585
- **DOI**：10.48550/arXiv.2608.25585
- **可靠入口**：[论文](https://arxiv.org/abs/2608.25585) · [AlphaXiv](https://alphaxiv.org/abs/2608.25585)
- **类别标签**：ICIL, Retrieval-Augmented VLA, Test-time Adaptation, Robot Manipulation
- **证据边界**：沿用知域既有来源报告的论文核验；本专题重新分类，不声称完成独立复现。

- **代表图**：Figure 1 : Adaptation bottleneck in existing ICIL frameworks. Existing ICIL methods (a) prioritize superficial visual similarity over functional intent in context retrieval, (b) fail to effectively leverage contextual guidance, and (c) exhibit significant computational overhead for larger contexts. While this overhead is plotted for RICL, other ICIL baselines follow a nearly identical trend.。来源：[原图](https://arxiv.org/html/2608.25585v1/intro.png)

![RA-VLA: Retrieval-Augmented VLA for Test-Time Adaptation 代表图](https://arxiv.org/html/2608.25585v1/intro.png)

### 核心内容与 Insight

RA-VLA 针对 ICIL 的两个具体失败：检索器按视觉相似而非行为功能找示范，以及 VLA 即使拿到正确示范仍受预训练行为惯性支配。它不把整条演示粗暴拼进上下文，而是先检索行为对齐的局部片段，再在 action head 中注入这些片段；训练时用 contextual adherence margin，要求相关上下文产生的动作误差显著低于随机无关上下文。这个“相关/无关上下文干预”比仅做 no-context 消融更能检验策略是否真正使用示范。

### Pipeline

- **输入**：当前双视角 RGB、语言指令、机器人本体状态，以及每个未见任务 1–5 条专家演示组成的 buffer。
- **过程**：滑窗切分专家轨迹并离线缓存视觉语言特征；轻量检索器按余弦相似度选 top-K 片段，检索器以同任务轨迹的 DTW 动作对齐作为正样本学习行为表征；flow-matching action head 逐层接收检索片段；相关与随机上下文之间施加回归 margin，并以检索动作均值初始化去噪动作。
- **输出**：适配未见任务的动作 chunk；目标任务部署时不更新权重。

### 实验与证据

LIBERO 使用四个 suite 轮流留一整套为未见任务，每个 held-out task 提供 3 条专家演示并评测 50 次；RA-VLA 四套平均成功率 38.45%，最强对照 RICL-R 为 20.85%，绝对提升 17.60 个百分点。真实 UR5e 留一任务评测，每个未见任务提供 4 条示范、12 次试验；RA-VLA 平均 56.25%，RICL-R 为 35.42%。行为对齐检索器把 LIBERO-Goal 上 RA-VLA 从 10.2% 提升至 53.2%；contextual sensitivity 从去掉 adherence loss 后的 0.0353 提升到 0.3639，并伴随成功率提升。作者还报告独立编码与缓存使延迟随检索片段数量近似恒定。

### 代码与数据

论文基于 GR00T N1.5、LIBERO 和自采 UR5e 数据；本轮未找到官方代码、权重或真实演示数据下载。因训练阶段需要未见测试任务之外的任务来学习检索器和 adherence，所谓 training-free adaptation 只指新目标任务部署阶段无权重更新，不是整个系统无需训练。

### 局限、失败案例与开放问题

DTW 正样本依赖训练演示动作，行为距离对不同 embodiment、速度和坐标系的稳健性尚未充分证明；LIBERO 的 suite-level 留出比随机任务留出严格，但仍是同一模拟生态；真实评测每任务仅 12 次；示范 buffer 的错误、恶意或次优轨迹会直接污染检索与控制。论文也指出 demonstration buffer 存在数据注入安全风险。后续应报告错误检索率、上下文错配校准、跨 embodiment 检索和大 buffer 的端到端延迟。

### 与知域的关系

代表检索增强 ICIL：先找行为对齐片段，再向 action head 注入上下文；可与 Zero-WAM 的完整视频条件和 PonderPounce 的执行期记忆直接比较。

## 3. PonderPounce: A Pretrained MLLM as an Episode Context Engine for Robot Control

- **作者**：Suhwan Choi, Jaeyoon Jung, Sungkyung Kim, Yunsung Lee, Youngjae Yu
- **年份与发表**：2026，arXiv 预印本（v1：2026-08-25）
- **arXiv ID**：2608.24115
- **DOI**：10.48550/arXiv.2608.24115
- **可靠入口**：[论文](https://arxiv.org/abs/2608.24115) · [项目](https://worv-ai.github.io/ponderpounce/) · [AlphaXiv](https://alphaxiv.org/abs/2608.24115)
- **类别标签**：Episode Context, Robot Memory, Demonstration Conditioning, Dual-system VLA
- **证据边界**：沿用知域既有来源报告的论文核验；本专题重新分类，不声称完成独立复现。

- **代表图**：Figure 1: Pretrained MLLM context as scalable robot memory. Unlike designs processing context within the controller or through purpose-built memory, PonderPounce retains history in Ponder ’s context and asynchronously routes cognition to Pounce . This separation keeps context processing off the action path and lets System 2 scale without changing the controller architecture.。来源：[原图](https://arxiv.org/html/2608.24115v1/figures/PP-Title.png)

![PonderPounce: A Pretrained MLLM as an Episode Context Engine for Robot Control 代表图](https://arxiv.org/html/2608.24115v1/figures/PP-Title.png)

### 核心内容与 Insight

PonderPounce 把具身 ICL 扩展为更宽的 episode-context learning：上下文不仅是任务前给定的演示，还包括执行过程中不断累积的观察、先前 cognition 和部分可见事件。慢系统 Ponder 用预训练 MLLM 的原生 causal context 保存这些信息，快系统 Pounce 不重读全部历史，只接收最新连续 cognition token 及其 age。其关键假设是：MLLM 预训练获得的长上下文整合能力可以通过低带宽 latent 接口迁移给机器人控制器。

### Pipeline

- **输入**：指令、可选演示、持续追加的 episode 观察、当前本体状态。
- **过程**：Ponder 以 append-only causal context 累积历史，并在较慢时钟上产生 transition 判断、内部子目标/演示推理及 cognition carrier；Pounce 在快时钟上接收当前观察、指令、本体状态、最新 cognition 与其陈旧年龄，flow matching 生成动作；两者联合端到端训练，部署中通过 KV cache 与异步调度避免反复编码全部上下文。
- **输出**：20Hz 回放的动作 chunk，以及只在内部使用的 cognition/子目标状态。

### 实验与证据

RoboMME 16 个记忆任务、每任务 50 个 episode，PonderPounce 在基础数据规模上平均 60.83%，9× 数据上 75.54%；FrameSamp+Modul 分别为 44.51% 和 57.88%。在相同 Pounce 架构和接口下，9B context engine 比 0.8B 高 10.79 个百分点，但这只证明规模相关，不隔离参数量、预训练质量和优化差异。RoboCasa-DC 五个 held-out demonstration-conditioned 任务上，PonderPounce 为 12.5%±0.9%，SeeTraceAct 为 11.6%；关闭 cognition 降至 8.6%±0.4%。绝对成功率较低，且公开 baseline 无误差条，不能据此声称广泛领先。持续刷新干预显示只在 transition 更新 cognition 会从 60.83% 降至 1.83%，说明当前 checkpoint 强依赖高频上下文更新。

### 代码与数据

项目页公开，但本轮未核验到代码或权重。系统推理延迟报告为 cognition refresh p50 78 ms、action invocation 25 ms，并借助 KV cache 与 fused kernel 支持 20Hz 动作播放；这属于作者环境的 batch-1 测量，不等于并发吞吐或端侧成本。RoboMME 使用模拟器派生的 transition、subgoal 与 demonstration-reasoning 标注，监督成本未量化。

### 局限、失败案例与开放问题

仅评测两个模拟 benchmark，缺少真实机器人验证；9B MLLM 加 3–3.6B controller 的训练和推理成本高；上下文限制为 16K token；RoboMME baseline 未获得同等推理监督，架构与监督因素纠缠；连续 cognition 与单独训练的文本子目标接口性能差异小于运行间波动。需要用相同监督预算、错配演示、历史反事实、长期上下文溢出和真实延迟测试来判断其 ICL 能力。

### 与知域的关系

把 ICL 扩展到执行期间持续增长的 episode context；参数不更新，只更新 causal cache 与 cognition，需与 fast-weight/test-time training 分开索引。

## 4. RoboTTT: Context Scaling for Robot Policies

- **作者**：Yunfan Jiang, Yevgen Chebotar, Ruijie Zheng, Fengyuan Hu, Yunhao Ge, Jimmy Wu, Tianyuan Dai, Scott Reed, Li Fei-Fei, Yuke Zhu, Linxi "Jim" Fan
- **机构**：NVIDIA GEAR Lab、Stanford University
- **年份与发表**：2026，arXiv 预印本（v1：2026-07-16）
- **arXiv ID**：2607.15275
- **DOI**：10.48550/arXiv.2607.15275
- **可靠入口**：[论文](https://arxiv.org/abs/2607.15275) · [DOI](https://doi.org/10.48550/arXiv.2607.15275) · [项目](https://research.nvidia.com/labs/gear/robottt/)
- **类别标签**：Embodied ICL, Test-Time Training, Long-context Robot Policy, Fast Weights, VLA
- **证据边界**：论文正文、附录和项目视频已核验；截至本次检索未发现作者代码、权重或训练数据公开入口。

- **代表图**：Figure 2，RoboTTT 在 GR00T N1.7 的 DiT action head 中加入 TTT layer；每步观测通过自监督更新写入 fast weights，后续动作再读取该状态。来源：[arXiv HTML 原图](https://arxiv.org/html/2607.15275v1/x2.png)

![RoboTTT architecture](https://arxiv.org/html/2607.15275v1/x2.png)

### 核心内容与 Insight

RoboTTT 研究的不是“给策略多放几帧”而是如何让机器人在固定推理成本下真正使用数千步历史。它把 Test-Time Training layer 插入 GR00T N1.7 的 16 层 DiT action head：每层的两层 MLP fast model 以当前 token 上的自监督重建损失做一步梯度下降，更新后的参数既是计算权重，也是跨时间传递的 recurrent state。slow weights、VLM 与 fast-weight 初值由外层训练学习；部署时只让 fast weights 随历史变化。因此它属于**参数状态 ICL**，但不是对整套策略做目标任务 fine-tuning。

长序列训练的两个关键配套是 sequence action forcing 与 TBPTT。前者对序列中每个 action chunk 独立采样噪声强度，使模型既看到近似干净的历史动作，也学习当前动作的 flow-matching 去噪；后者在 segment 边界截断梯度却继续传递 fast weights，使显存由 segment 长度而非总 context 决定。为让失败经验可在测试时被利用，作者另提出 DAgger Distillation：完整保留“机器人失败动作 → 人类纠正”作为上下文，只在纠正动作上计算监督损失，让外层训练把在线恢复算法蒸馏进 fast-weight 更新动力学。

### Pipeline

- **输入**：语言、四视角 RGB、本体状态、加噪 action chunk，以及此前的人类视频、机器人观察和已执行动作。
- **过程**：VLM 提取当前视觉语言 token；每个时间步的 self/cross-attention 处理局部信息，16 个 register tokens 携带视觉语义进入跨时间 TTT layers；fast MLP 对当前 token 做梯度更新并传到下一步；DiT 以 flow matching 生成动作块。人类演示段只更新 fast weights，不计算 action loss。
- **输出**：当前 H-step 动作块，以及持续演化但固定大小的 fast-weight 状态；其单步计算不随累计 context 线性增长。

### 实验与证据

论文实际探查六组问题，不能只保留“8K context 更好”这一句。

1. **长上下文是否改善多阶段真机任务。** 在双臂 YAM、四个 RGB 相机上评测 Pup Go Car、Circuit、Gear Bot；分别收集 8、6、5 小时真机数据，平均任务时长约 2、1、5 分钟。Circuit 有约 80 种部件/顺序配置，20 种训练、60 种测试。Pup Go Car 和 Circuit 每方法 20 次，Gear Bot 10 次。RoboTTT 的三任务平均 rubric completion 为 79%，GR00T 单步为 42%、一帧历史版本约为最佳 short-context 参照、GDN 为 56%；相对单步提高 87%，相对 GDN 提高 41%。Gear Bot 完整成功 2/10，其他方法为 0。它支持长历史有助于阶段消歧、遮挡下精细操作和失败恢复，但 rubric partial credit 与 full success 必须分开理解。
2. **预训练 context length 是否形成 scaling axis。** 保持结构与后训练协议一致，把预训练长度从 128 扩到 8K timesteps。RoboTTT 平均完成分随长度稳定上升，8K 为 71.5%，比同模型 1K 的 43.9% 高 63%，比最佳短上下文 45.6% 高 57%，未见饱和；参数匹配的 GDN 没有同样趋势。该对照说明收益不只是“有 recurrent state”，而与可通过外层目标塑形的梯度 fast weights 和长序列训练相关；但每个长度没有公开独立随机种子，不能把一条内部曲线当成普适扩展律。
3. **能否从一段人类视频 one-shot 模仿。** Circuit 的所有配置使用同一句 “assemble circuit”，目标部件和顺序只能从人类视频识别。训练配置每种收集 5–20 段人手组装视频，与同配置机器人轨迹拼成序列；测试为未见配置。RoboTTT 完整成功 6/10，GDN 0/10，后者常选错部件或顺序。这个实验直接支持 fast weights 能读出示范配置；但样本只有 10 次、只在一个任务族上做，也没有错误视频或顺序反转对照。
4. **是否能利用 episode 内历史应对外部扰动。** Pup Go Car 中，在屋顶或轮胎装好后由人移除，所有模型共同加入 30 分钟扰动训练。RoboTTT 对屋顶恢复 15/20，GDN 13/20，短上下文方法最多 10/20；轮胎恢复中 RoboTTT 与 GDN 都为 18/20。该结果支持长状态对回退阶段有帮助，但轮胎上不能证明梯度 fast weights 优于一般 recurrent memory，而且鲁棒性并非零样本涌现，训练见过该类扰动。
5. **DAgger Distillation 是否学到在线改进。** 汇总 100 条 DAgger 轨迹（RoboTTT 与 GR00T 各采 50 条）。标准只学人类纠正的 DAgger 对四方法平均提高 9%、对 sequence models 提高 13%；将失败动作保留为 context 的 DAgger Distillation 对 RoboTTT/GDN 平均提高 33%，其中 RoboTTT 36%、GDN 29%。GR00T 把失败动作也当监督目标与只学纠正都为 57%，说明失败动作的价值主要来自上下文而非模仿。它支持“失败—纠正映射可被序列策略利用”，但不是证明模型在部署中继续优化显式任务损失。
6. **哪些结构和训练选择真正必要。** 去掉 sequence action forcing 后闭环动作质量严重下降；把 fast MLP 换成线性层虽仍胜过 GR00T，但比 MLP 低 27%；在只处理 state tokens 的 TTT 上加入 action tokens 相对提高 23%，再加 register tokens 提高 18%，而单独给 GR00T 加 register tokens 无益。这些消融把收益收窄到非线性 fast model、动作历史与视觉语义桥接的组合，不能归因于单纯参数增加。

### 代码与数据

模型基于 GR00T N1.7；原 DiT action head 为 538M 参数，加入 TTT 后约 690M。预训练只更新新增 sequence layers，使用 16 张 GB200、30K steps；任务后训练用 8 张 GPU、1K context、20K steps 并更新全模型。部署为 RTX 5090、30 Hz。论文没有披露预训练混合数据的完整规模与构成，也未给出代码、权重、数据和许可证，因此现阶段可审计方法与内部实验，不能复现 8K scaling 或真机结果。

### 局限、失败案例与开放问题

三项主任务都在同一 YAM 双臂平台，任务后训练使用各自数小时数据；因此论文证明的是长上下文对已后训练任务的收益，不是通用任务零样本执行。one-shot 只有 Circuit 10 次；context scaling 没有独立种子或误差条；Pup Go Car 的主要结果又加入了 DAgger 数据，与纯 context scaling 曲线不是完全相同 checkpoint。fast weights 每步由代理重建目标更新，未来还需测错配历史、恶意示范、状态漂移、超长 rollout 稳定性和 reset 策略。所谓“固定推理延迟”指复杂度不随累计历史增长，不代表没有 TTT 更新开销。

### 与知域的关系

RoboTTT 是本专题中唯一明确在部署期执行梯度更新的核心工作。它把上下文从 token/KV cache 压入参数空间，必须与 Zero-WAM/HOST/S1/GEN-1.5 的 frozen-weight prompting 分开索引。

## 5. Robots Acquire Manipulation Skills in Seconds from a Single Human Video（HOST）

- **作者**：Guangyan Chen, Meiling Wang, Te Cui, Zichen Zhou, Qi Shao, Shalfun Li, Hang Su, Roy Gan, Hao Wang, Mengyin Fu, Yi Yang, Yufeng Yue
- **机构**：北京理工大学、X SQUARE ROBOT（自变量机器人）、清华大学
- **年份与发表**：2026，arXiv 预印本（v1：2026-07-22）
- **arXiv ID**：2607.20033
- **DOI**：10.48550/arXiv.2607.20033
- **可靠入口**：[论文](https://arxiv.org/abs/2607.20033) · [DOI](https://doi.org/10.48550/arXiv.2607.20033) · [项目](https://host-site.host-robotics.workers.dev/)
- **类别标签**：Embodied ICL, One-shot Visual Imitation, Human-to-Robot, World Action Model, Robot Memory
- **证据边界**：论文、补充材料和项目页已核验；论文给出较完整的训练规模与真机 trial，但作者代码和完整数据未公开。

- **代表图**：Figure 2，HOST 用共享任务进度对齐演示与机器人轨迹，再按“进度定位 → 机器人未来观测 → 动作”的顺序生成。来源：[arXiv HTML 原图](https://arxiv.org/html/2607.20033v1/x2.png)

![HOST method overview](https://arxiv.org/html/2607.20033v1/x2.png)

### 核心内容与 Insight

HOST 把 one-shot visual imitation 的失败归结为两种结构错配：人和机器人完成同一任务的速度不同，固定时间偏移会把监督目标配到错误阶段；即便阶段对齐，人手、机器人、视角和场景外观仍不同，直接从人类帧回归低维动作过难。它因此先离线学习无帧级标注的共享 task-progress manifold，把每个机器人训练目标绑定到演示的**未来进程**；推理时再通过单个 autoregressive diffusion model 依次预测当前进度、机器人自身未来观测和动作。

作者所称的级联只指模型内部生成顺序和 attention mask：动作读取已预测未来观测，未来观测读取已预测进度。它是有向的计算依赖，不是结构因果模型、`do(·)` 干预或可识别的因果机制。HOST 的新技能保存在外部视频上下文里而非权重中；以后可按语言与初始场景检索该视频，从而避免为每个新技能反复 fine-tune 和遗忘旧技能。

### Pipeline

- **输入**：一段人类视频、可选语言、最近 K 步三视角机器人观察、当前 20 维本体状态。
- **过程**：训练期用基于 Qwen3-VL-Embedding-8B 的对齐模块恢复人/机器人帧的单调进度；HOST 根据预测进度滑动演示窗口，以 Wan VAE 编码视频，在 mixture-of-transformers 中按 progress → future robot observations → 32-step actions 的顺序做联合 flow matching。Stage 1 用 193,462 条、229 任务的 robot–robot pairs；Stage 2 用 5,847 段自采人类视频及同任务机器人轨迹适配跨 embodiment。
- **输出**：归一化任务进度、机器人自身视角未来 latent 与 32 步双臂动作块；推理时模型权重冻结。

### 实验与证据

HOST 的实验链条较完整，实际探查十个问题。

1. **覆盖面。** 单一 ARX R5 双臂平台、三 RGB 相机、20 维动作；50 个训练集未包含其操作技能的新任务，每任务 20 次、随机化物体位姿，由人按任务标准判定。作者称 50 项都获得非零可执行能力，整体平均成功率 62%。这证明覆盖不局限于一两个 cherry-picked 视频，但非零能力不等于每项可靠，完整逐任务不确定性未报告。
2. **与 frozen-weight baselines 的比较。** 在核心新任务子集上，对比同样接收一段视频的 Vid2Robot、AWDA，以及只接语言的 π0.5、Wall-OSS、HOST-base。OSVI 的 conditioning 被移植到 HOST backbone，Vid2Robot 为作者复现。HOST 比最强 OSVI 高 43 个百分点、比最强 zero-shot language policy 高 45 个百分点。它支持“如何使用演示”比仅提供视频更重要；但重实现质量与不同 baseline 的原始预训练仍是混杂因素。
3. **与监督微调的数据/时间效率比较。** π0.5、Wall-OSS、HOST-base 分别用 10/20/50 条机器人演示做 LoRA SFT。50 条时最强 Wall-OSS+SFT 为 56%，仍低于 HOST 单视频的 62%；SFT 的采集加训练约 4.0–4.9 小时，HOST 只需录制视频，平均 29 秒，相对最快 SFT 为 507×。这里的“acquisition time”主要省掉机器人遥操作和离线训练，不是模型单次推理延迟。
4. **是否遗忘旧技能。** 在 7 个训练内旧任务上比较适应前后。50-demo SFT 后 π0.5、HOST-base、Wall-OSS 分别只保留原性能的 17%、21%、40%；HOST 因权重不变而基本保留。该实验支持外部上下文避免参数覆盖，但也带有定义上的优势：HOST 没有把新知识写进共享权重，持续能力依赖视频存储与正确检索。
5. **部署扰动。** 相对默认 62%，灯光变化、OOD 物体替换、场景更换和执行中人为移动物体分别下降 1、4、6、9 个百分点。最后一种需要重新定位进度并恢复。结果支持进度定位对一定域差和中途扰动有效，但最强扰动后约 53% 仍意味着近半失败，安全边界没有展开。
6. **对齐是否比时钟匹配可靠。** 以人工标注事件为参照，按相对时间匹配的平均进度误差为 0.079±0.062，共享进度对齐为 0.006±0.008；推理期进度 head 相对离线对齐标签 MAE 为 0.013。它证明所测 paired data 中 task-progress alignment 更准确，但离线 alignment module 本身充当“真值”，不能替代完整人工 ground truth。
7. **target coupling 的逐项贡献。** 整段视频条件成功率 0.21；按 timestamp 选局部窗为 0.29；按共享进度选窗为 0.45；再把预测目标绑定到演示未来进程达到 0.62。该消融直接支持时间异步与被动条件是 OSVI 瓶颈之一。
8. **self-grounded prediction 的逐级贡献。** 在已使用 target coupling 的直接 video→action baseline 上，成功率为 0.34；加入进度定位为 0.43；并行预测未来自身观测为 0.55；让动作条件于预测未来的完整级联为 0.62。每级都提高闭环结果，支持中间自身视角未来可缓和跨 embodiment 差异；但视觉预测质量主要定性展示，未给 FVD、几何一致性或反事实校准。
9. **同 embodiment 预训练是否必要。** 固定 Stage 2 人—机器人 pairs，只增加 Stage 1 robot–robot 数据比例，新任务成功率单调上升；0% Stage 1 明显较差。它支持大量同机器人演示先学习“跟随程序”，再用较少人类 paired data 跨域，而不能说 5,847 对人—机器人数据已经很少或易收集。
10. **技能存储与复用。** 视频连同语言和初始场景进入外部 memory；查询以文本/场景相似度加权，在固定阈值上区分旧任务与新任务。论文展示较宽阈值区间内召回与新任务识别均较高，且检索视频驱动的执行接近新录视频。这里没有公开 memory 规模继续扩大、细粒度近邻任务、错误检索或对抗视频下的完整数值，长期可扩展性仍未证明。

### 代码与数据

训练规模、两阶段 steps（500K/100K）、30-layer video/action experts、三相机拼接分辨率、动作 horizon 等在附录披露较充分；但完整机器人轨迹、人类 paired videos、权重、代码和评测脚本未见公开下载。Vid2Robot 结果来自作者重实现，复现公平性需要代码才能审计。

### 局限、失败案例与开放问题

论文只在一类双臂平行夹爪平台验证，尚未证明跨机器人 embodiment；普通 RGB 视频缺乏接触力与触觉，对精细插接/柔性操作可能不足；50 项都来自作者内部任务体系，训练—测试语义去污染与任务定义需公开；相似度 memory 随规模增长可能混淆指令和场景都很相近的技能。62% 是重要进展但仍不适合无监督部署。最关键的后续干预是错误视频、同首帧不同程序、局部步骤删除、视频倒放和近邻检索冲突。

### 与知域的关系

HOST 是六项核心工作中机制审计最完整的 frozen-weight video ICL：它不仅给视频，还显式解决“当前执行位于示范哪里”和“如何转成自身未来”两个接口问题。

## 6. Introducing S1: In-Context Learning for Robotics

- **作者**：Skild AI Team
- **年份与发表**：2026-08-18，Skild AI 官方研究长文；无 arXiv ID、DOI 或 PDF，未核验同行评审
- **可靠入口**：[官方研究长文](https://skild.ai/blogs/s1)
- **类别标签**：Embodied ICL, Robot Foundation Model, Video Prompt, Long-horizon Manipulation, Human-to-Robot
- **证据边界**：官方页面的正文、图表说明和视频已核验；架构、模型规模、任务列表、trial 级结果、代码、权重与数据未公开，所有量化均为公司内部评测。

- **代表图**：S1 长时未见任务示例封面；官方页面展示单段人类 prompt 后的 pancake、coffee、kit assembly 与 plant potting 自主执行。来源：[官方图片](https://assets.skild.ai/site/v1/blog/sb-812a99baf442e4fb5939/cover-v2-poster.jpg)

![S1 in-context manipulation](https://assets.skild.ai/site/v1/blog/sb-812a99baf442e4fb5939/cover-v2-poster.jpg)

### 核心内容与 Insight

S1 把机器人 ICL 定义为：训练时所有任务只通过 episode 内视频示范指定，使高多样性预训练迫使策略从示范解析意图、功能对应和任务进度；测试时放入一段来自不同场景、视角乃至 embodiment 的视频，不做 post-training。官方把 pretraining 视为 meta-learning outer loop，把 frozen-weight prompt conditioning 视为 inner loop，但没有披露显式 inner-loop 优化器。S1 相对同期工作的差异化主张不是短动作 one-shot，而是**从一段视频完成预训练未见、最长约 10 分钟的任务组合**。

### Pipeline

- **输入**：任务视频 prompt、当前机器人视觉/状态；示范可以是人类第一视角或其他采集形态。
- **过程**：在以示范而非语言定义任务的 episodic mixture 上预训练；数据引擎混合 robot teleoperation、UMI、egocentric video 和 simulation，以硬件接近度、任务多样性与可扩展性互补。部署时视频进入 context window，策略闭环预测本体动作，权重不更新。
- **输出**：机器人动作序列；官方未披露 action representation、控制频率、context token 数、模型结构和推理延迟。

### 实验与证据

官方长文包含五类量化/定性探查。

1. **长时未见任务展示。** plant potting、pancake cooking、pour-over coffee、kit assembly 四项声称完全不在训练中，包含数十个操作步骤、最长约 10 分钟，由一段视觉示范驱动。plant potting 从录完一次人类示范到机器人开始执行为 11 分钟，其中主要时间是场景设置。视频显示组合、阶段跟踪与部分新动作，但页面未给每项 trial 数、成功率、失败视频或独立评审，因此它证明“存在成功案例”，不能量化可靠性。
2. **ICL 与 language VLA 的数据 scaling。** 在过滤后的同一预训练池上，ICL 和 language-conditioned policy 使用相同数据、架构（仅 prompt embedding 不同）和 compute，训练数据从 1K 扩到 100K 小时；内部 seen/unseen suites 的任务长 4–8 分钟，用累计逐步成功率，失败后允许人工 intervention 继续评完整流程。seen tasks 在 1K 小时时 VLA 53%、ICL 43%；数据扩大后 ICL 达 96%。unseen tasks 在 100K 小时时 ICL 66%、VLA 9%，约 7.3×。这支持示范条件对 OOD 长任务随数据规模改善得更快；但人工恢复改变 rollout 分布，任务数、每点 trial/种子、误差条和 VLA 最终 seen 数值未公开。
3. **部署分布与 prompt 分布偏移。** 已知窄分布任务设置 L1–L5：从原物原位，逐步增加 15 cm/30°、30 cm/45° 位姿扰动，替换同 affordance 物体并垂直移动，直到迫使半数动作换另一只手。相对训练分布偏移时，L5 下 language VLA 的降幅最多是 ICL 的三倍；固定训练条件、只增大 prompt 与执行场景差距时，ICL 对位姿和同 affordance 替换仍稳健，到执行计划必须换手的 L5 才明显下降。页面图未在正文给出逐级原始数值与统计量，因此只能支持相对趋势。
4. **一段 prompt 相当于多少 post-training 数据。** 对未见长任务给 language VLA 1–2,000 条 teleop 示范做 post-training；S1 ICL 固定为单示范 66%。曲线插值交点约 380 条，采集这些 4–10 分钟示范需 50–100 小时；2,000 条后 SFT 达 86%，最终超过 ICL。该实验说明 ICL 显著降低达到“可用起点”的数据成本，也诚实表明充分 SFT 仍更可靠；“380”是内部曲线插值，不是跨模型通用换算率。
5. **恢复、常识与示范纠错。** 官方展示移动物体、换物体和改灯光后继续执行，滑板轮装配失败后重试，用杯子替代 watering can、只补满已有液体，以及人类打蛋出错而机器人更平稳执行等案例。它们说明策略不是逐像素轨迹回放，并生成可检验的 common-sense 假设；但没有样本量和对照，不构成量化鲁棒性或“理解物理”的证明。

### 代码与数据

官方只给高层数据源分类与“1K–100K 小时”受控子集范围，并称所有展示由同一模型权重生成。没有公开 S1 架构、参数量、完整预训练规模与去污染清单、benchmark、trial 日志、代码或权重。页面说明后续文章才会展开训练方法，因此当前不应反推具体网络或把 S1 写成已可复现论文。

### 局限、失败案例与开放问题

最关键缺口是内部 benchmark 不透明：无法核验“完全未见任务”、累计逐步成功率的评分细则、人工 intervention 频率和独立种子。长任务展示没有失败分母；data scaling 同时依赖高成本内部质量控制，外部无法复刻。S1 没有报告 wrong-prompt、no-prompt、reverse-prompt、prompt truncation 和相似训练片段检索，因而还不能排除强预训练策略与上下文捷径的贡献。公司称最长 10 分钟，但上下文实现与推理成本均未知。

### 与知域的关系

S1 把具身 ICL 的评价轴从短时原子技能推进到“未见技能 × 长时组合”。它当前最值得跟踪的是 100K 小时下 66% vs 9% 的受控趋势，但证据等级低于公开论文，因为方法和评测仍不可复现。

## 7. GEN-1.5: Embodied Foundation Models are One-Shot Learners

- **作者**：Generalist Team
- **年份与发表**：2026-08-19，Generalist AI Blog 官方研究长文；无 arXiv ID、DOI 或 PDF，未核验同行评审
- **可靠入口**：[官方研究长文](https://generalistai.com/blog/gen-1.5)
- **类别标签**：Embodied ICL, Physical Prompting, Robot Foundation Model, Few-step Adaptation, Sim-to-Real
- **证据边界**：官方正文、图表说明和视频已核验；核心模型、数据、代码和评测协议未公开，one-shot 量化来自 10 项内部短任务。

- **代表图**：GEN-1.5 官方文章封面。来源：[官方图片](https://generalistai.com/assets/pages/blog/gen-1.5/assets/images/generalist-gen1p5-og.jpg)

![GEN-1.5 physical prompting](https://generalistai.com/assets/pages/blog/gen-1.5/assets/images/generalist-gen1p5-og.jpg)

### 核心内容与 Insight

GEN-1.5 的关键概念是 physical prompting：把一段包含 sensor data 与 action trajectories 的例子插入 30 秒 context window，剩余空间滚动接收当前观察；模型立即以 100 Hz 输出动作。示范通常由人手持一对 grippers 记录，也可以来自机器人或模拟器，因此比纯 RGB 人类视频拥有更直接的 action/embodiment 接口。作者称 ICL 并非显式 meta-learning、辅助目标或特制 prompt packing 的产物，而是大规模连续物理预训练中自然涌现。

这篇长文同时讨论两种不同能力：zero-gradient physical prompting 和用 1–10 个 gradient steps 的 few-shot adaptation。前者才是严格 ICL；后者会改变模型权重，作者也把它类比 test-time training。两套数值不能合并成同一种 one-shot 结果。

### Pipeline

- **输入**：3–12 秒单条 sensorimotor demonstration、滚动视频记忆，以及其他传感、语言和本体输入；也可拼接两条 physical prompts。
- **过程**：一个从头训练的大型多模态模型在连续物理交互片段上预训练超过 8 个月；ICL 模式只改变 context buffer。few-step 模式则从 1–5 分钟、约 10–50 条示范采样序列，用接近预训练的超参数做 1–10 次梯度更新。
- **输出**：100 Hz action trajectories；官方未披露 action space、机器人平台数量、参数量、训练数据小时数和实时延迟。

### 实验与证据

1. **十项 short-horizon 新任务的 one-shot/few-shot 主结果。** 任务含开罐、拉拉链、从钱包取钱等。3–12 秒单示范、0 梯度的 physical prompt 平均成功率 59%±10%；5 分钟/任务、约 50 条示范、10 gradient steps 为 83%±9%。作者承认任务简单、短时且 one-shot 仍较脆弱。标准差看起来是跨任务离散度，不等同独立训练种子的置信区间；每任务试验数和 baseline 未披露。
2. **少步梯度适应。** 1–10 步即可提高 held-out task；10 步后权重相对初始变化不足 0.15%。极端 1-step、1 分钟数据的一个 held-out task 成功率 66.5%，更大 batch 和学习率更好；作者没有调参或系统 sweep。它支持预训练表征对新任务高度可塑，但只有一个任务的 1-step 数值，且这不是 frozen-weight ICL。
3. **prompt composition。** 将“解开铅笔袋”和“取出钱”两条独立示范同时放入 context，模型按顺序连接为一个行为，并自行生成重定位、重抓与恢复动作。该案例说明 context 可以规定组合而非逐轨迹复刻，但只有展示，没有组合任务成功率、顺序交换或错误组合对照。
4. **zero-shot sim-to-real physical prompt。** 模型预训练不含模拟数据，任务也没有在模拟或真实环境训练；把模拟器 rollout 放进 context 后，真机执行，并对手型、物体位置和尺寸变化有一定泛化。这是很强的跨域案例，但页面未给任务数、成功率或 simulator mismatch 分层，不能外推为一般 sim-to-real 方法。
5. **human-to-robot ICL。** 部分任务由人在机器人相机前直接用手展示，机器人随后复现。官方只称 “in some cases”，没有系统指标；因此它证明存在成功样例，证据强度低于 HOST 的 50-task/20-trial protocol。
6. **预训练 scaling 与涌现过程。** 文章展示连续 8 个月、三个训练阶段的 held-out next-action error 持续下降，并描述适应从数百步逐渐降到 10 步、1 步、最终 0 步；但图没有公开数据规模、compute、模型版本或重复训练，不能建立可复核 scaling law，也不能确定 ICL 是何时、由何变量涌现。
7. **物理泛化与即兴策略。** 5 分钟人类示范、1–10 步微调后的模型会用香蕉当刷子、用簸箕铲块、移开遮挡、双手旋盖、换手操作，并泛化到新杯瓶。最近邻语言检索覆盖 1,891,392 scenes，作者称未找到相同策略。这些展示主要属于 lightly fine-tuned models，不应被误写成 one-shot ICL 的量化证据；最近邻检索也不能证明预训练中绝无视觉/行为近邻。

### 代码与数据

官方只披露 30 秒 memory、100 Hz action、连续预训练超过 8 个月、10 项 ICL 均值和少步数据预算。参数量、训练总小时、数据分布、机器人/手型构成、去污染、任务明细、trial 数、评分规则、代码、权重和 benchmark 都未公开。当前可将其作为重要 capability report，而非可复现实验论文。

### 局限、失败案例与开放问题

59% 平均值意味着 one-shot 仍有明显失败；30 秒 context 对更长任务如何保存 prompt、是否会被滚动观察挤出没有说明。短任务和 S1 的 4–10 分钟任务不能直接比较；physical prompt 含动作轨迹，与 Zero-WAM/HOST 的纯人类 RGB 视频也不是同等信息预算。组合、sim-to-real、人到机器人和工具即兴多为视频案例，缺少分母。few-step 结果与 ICL 混在同一发布中容易造成概念混淆，入库必须分别标注。

### 与知域的关系

GEN-1.5 展示了“上下文适应—极少步参数适应”的连续谱，并提供 sensorimotor prompt、prompt composition 与 sim-to-real 三种独特接口。它是能力信号很强、公开可审计性较弱的公司技术发布。

## 8. Dyna-2: A 1-Million-Hour Scaling Law for World-Action Models

- **作者**：Dyna Robotics
- **年份与发表**：2026 年 8 月，Dyna Robotics 官方网页版 technical report；无 arXiv ID、DOI 或 PDF，未核验同行评审
- **可靠入口**：[官方技术报告](https://www.dyna.co/dyna-2) · [知域完整精读](2026-09-02_dyna_2_technical_report.md)
- **类别标签**：World Action Model, Scaling Law, Cross-embodiment Transfer, Human Video Pretraining, Video Generation
- **证据边界**：本节聚焦它与 ICL 的关系；完整公式、逐任务表格和一步视频蒸馏审计见独立精读。模型、数据和代码均未公开。

- **代表图**：Dyna-2 一步视频蒸馏中固定教师目标与随学生能力推进的移动目标几何示意。来源：[官方原图](https://www.dyna.co/assets/research/dyna2-fig16-one-step-geometry.jpg)

![Dyna-2 one-step video distillation](https://www.dyna.co/assets/research/dyna2-fig16-one-step-geometry.jpg)

### 核心内容与 Insight

Dyna-2 不是严格的 one-shot ICL 工作。它的主要问题是：把人类第一视角操作视频从 1K 扩到 1M 小时，并让同一模型联合预测未来视频和动作，能否形成可迁移到未见机器人数据与少量机器人 post-training 的基础。其 ICL 意义在于提供“为什么视频上下文策略可能随规模变强”的预训练证据：未来预测迫使表征建模跨 embodiment 共享的场景变化，额外无动作视频又形成独立扩展轴。但官方没有把单段新示范插入测试 context、再用正确/错误示范对照，因此不能把 Dyna-2 本身标为已验证的 in-context learner。

### Pipeline

- **输入**：历史视频帧、语言、机器人或人体状态；人类视频动作伪标签来自 3D 手腕轨迹与指间开合；另有无动作视频。
- **过程**：video/action mixture-of-transformers 共享注意力交互，以 flow matching 联合学习未来视频与动作；动作推理读取共享历史表征，但不直接消费生成的未来视频。机器人任务需要额外 post-training。一步视频分支用随学生能力推进的平滑移动目标蒸馏多步教师。
- **输出**：动作块与未来视频；当前证据更接近“video prediction 训练共享表示 → reactive action”，不是“生成多个未来 → 评价 → 规划”。

### 实验与证据

Dyna-2 官方报告共有十组实验/探查，在 ICL 专题中应保留其完整逻辑链。

1. **同域人类 scaling。** 1K/10K/100K/1M 小时嵌套人类数据上，held-out human action MSE 0.062/0.057/0.056/0.054，accuracy@0.5 为 0.40/0.44/0.45/0.47；四指标四点幂律拟合均单调，但没有独立种子与 exponent 置信区间。
2. **zero-shot robot 离线迁移。** 预训练未用机器人轨迹，直接在 39 项机器人任务预测动作，MSE 0.180/0.174/0.124/0.117，accuracy@0.5 为 0.067/0.074/0.136/0.159。它证明扩大所用人类数据能改善该套未见机器人数据的开放环预测，不等于闭环新任务成功。
3. **相同机器人 post-training 后的真机排序。** 四级 checkpoint 用完全相同、每任务最多 10 小时的数据后训练；14 项真机平均归一化分 20%/28%/45%/53%，1M 在 9/14 项最好。Rope Tie、Food Scooping 等单项在 1M 反而回落，故只有平均趋势，不是每任务单调。
4. **训练目标消融。** 5K/50K/100K 带伪动作视频上，joint video+action 在 39/39 项均优于 action-only；只有再加入额外 video-only 数据的 recipe 随规模稳定改善。该实验支持未来预测和额外视频分别有贡献，但没有等 token/FLOPs 对照。
5. **video-only 独立扩展轴。** 固定 50K 动作数据，把额外视频从 0 扩到 50K，robot MSE 约 0.34→0.12；固定 250K 动作数据，额外 0/250K/750K 视频使 MSE 约 0.10→0.084。同域 human MSE 未同步改善，收益主要出现在跨 embodiment，但来源可能是动态、视觉多样性或其他共变因素。
6. **WAM–VLA 受控对照。** 早期 Dyna-2 与内部 Dyna-1 VLA 使用相同数据、超参、7 项真机任务和 3 个 checkpoints。WAM 汇总成功率为 VLA 的 1.55×、质量 grade 1.12×，21 个 cells 中胜/负/平为 65%/29%/6%。它只支持该内部配对，不能证明所有 WAM 优于所有 VLA。
7. **精度、扰动与目标持续性案例。** 展示更均匀的芹菜切割、改灯/遮顶视相机后继续执行、不断把已切食材放回时持续清空。这些是定性视频，没有样本量和扰动成功率。
8. **未见客户站点。** 相同任务 post-training 且都不使用目标站点数据，内部均近 100% pass；客户现场 Dyna-1 46%、Dyna-2 87%。这里是 site generalization，不是新任务 ICL；客户数、总 trial 和失败类型未公开。
9. **语言遵循。** 同场景换指令的 36 次评测中，action-only 早期模型 0.35，video co-train 早期模型 0.67，完整 Dyna-2 0.96。它支持视频目标/规模与语言 grounding 相关，但完整模型同时改变多项因素，“counterfactual cases”也不是 SCM 反事实识别。
10. **一步视频生成。** 3 秒三视角视频上，100-NFE 教师 10.203 秒、FVD 80；Dyna-2 一步学生 110 ms、FVD 121、相对真实 motion 75%、flicker 1.94，优于硬截一步和 DMD2 一步。它证明蒸馏质量/速度折中，但未测一步未来是否提高规划或控制成功率。

### 代码与数据

官方没有公开个人作者、PDF、arXiv、模型规模、训练 token/FLOPs、百万小时语料构成、去污染、代码、权重、完整机器人数据或许可证。39 项离线套件含 27 项外部 xdof ABC 与 12 项内部任务；14 项真机与客户现场评测也不可复现。所有数值应绑定 2026-09-02 的网页版本。

### 局限、失败案例与开放问题

四个数据点不足以确立普遍 scaling law；多数真机任务约 10 次，单项非单调；video co-training 同时改变目标、样本量和训练成本；zero-shot robot data 不保证任务语义未在人类视频出现；语言同场景干预与 temporal causal mask 都不是因果识别；一步视频尚未成为经验证的 planner。对本专题最关键的缺失是：没有示范作为测试时自变量，也没有正确/错配示范下的行为差异。

### 与知域的关系

Dyna-2 应被放在 ICL 专题的“规模化预训练基础/邻接工作”而非“已验证单示范 ICL”栏。它给出的研究启发是：比较 ICL 方法时不能只看 prompt 接口，还要控制 video prediction、video-only 数据和跨 embodiment pretraining 的底座强度。
