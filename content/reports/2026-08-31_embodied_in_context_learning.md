# 具身 In-Context Learning 专题：视频示范、检索与 Episode Context

**报告标签**：Embodied ICL, In-context Imitation Learning, VLA, World Action Model, Robot Memory, Test-time Adaptation

> 从知域现有馆藏中抽取 3 篇直接研究具身 in-context learning 的工作，比较上下文是什么、如何注入策略、部署时是否更新参数，以及如何证明策略真的依赖上下文。

## 专题结论

具身 ICL 的关键并不是“上下文更长”，而是上下文能否改变任务语义和动作分布。Zero-WAM、RA-VLA、PonderPounce 分别覆盖完整人类视频、检索到的局部行为片段和持续增长的 episode history；三者均不在目标任务部署时更新模型参数，但更新的推理状态和上下文接口不同。

| 工作 | 上下文载体 | 注入方式 | 部署时参数更新 | 关键审计 |
|---|---|---|---|---|
| Zero-WAM | 完整人类操作视频 | 视频任务条件 + future prediction | 否 | 换错视频后预测/动作是否改变 |
| RA-VLA | 检索到的行为片段 | action head 分层注入 | 否 | 相关/无关上下文 margin 与检索命中 |
| PonderPounce | 演示 + episode history + cognition | 慢 MLLM cache 向快控制器传 latent | 否 | cognition-null、刷新频率、历史错配 |

## 统一评测建议

1. 同时报告正确上下文、无上下文、错配上下文和打乱上下文。
2. 区分任务成功率、动作敏感性、检索质量和上下文使用强度。
3. 把 token/cache 状态适应、外部检索和参数更新分开，不把它们统称为 test-time learning。
4. 跨 embodiment 时单独评估任务语义迁移与动作坐标对齐。

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
