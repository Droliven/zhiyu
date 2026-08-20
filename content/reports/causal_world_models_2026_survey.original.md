# 因果世界模型（Causal World Models）最新代表工作梳理

- Causal-JEPA: Learning World Models through Object-Level Latent Masking
- A Unifying Perspective on Causal World Models: From Observations to Representations to Structure
- Language Agents Meet Causality — Bridging LLMs and Causal World Models
- Robust Agents Learn Causal World Models
- Building Minimal and Reusable Causal State Abstractions for Reinforcement Learning
- Object-Centric World Models for Causality-Aware Reinforcement Learning
- Causal World Modeling for Robot Control (LingBot-VA)
- VLA-JEPA: Enhancing Vision-Language-Action Model
with Latent World Model
- Mask World Model: Predicting What Matters for Robust Robot Policy Learning


**检索日期：2026-08-19**

> 本报告聚焦“world model + causality / intervention / counterfactual reasoning”，优先选择近年正式发表或较高质量的新预印本。  
> 检索线索来自 arXiv、会议官网及作者公开页面；最终技术判断以**原论文、会议论文页、官方代码仓库**为准。  
> 特别注意：近年来很多论文使用 “causal” 一词，但其含义并不相同。本报告严格区分：
>
> 1. **正式因果学习 / intervention / identifiability**；
> 2. **causal inductive bias / counterfactual-like predictive learning**；
> 3. **object dependency / causality-aware attention**；
> 4. **仅指 temporal causal/autoregressive ordering**。
>
> 因此，论文标题中出现 *causal* 不等于它已经学习到了 Pearl 意义上的可识别因果结构。

---

## 0. 总体结论

目前“Causal World Model”还没有形成像 Video World Model / VLA 那样统一的标准范式，最值得关注的主线大致有三类：

| 路线 | 核心问题 | 代表工作 | 因果含义 | 当前成熟度 |
|---|---|---|---|---|
| **Causal Representation / Structure** | 从高维观测中恢复可干预的 latent variables / causal relations | *Language Agents Meet Causality*, BISCUIT, CBM/CDL | 较强：显式 causal variables / graph / intervention assumptions | ★★★★☆ |
| **Intervention-aware Predictive World Model** | 让 predictive latent 必须依赖实体交互，并支持 counterfactual-like reasoning | **Causal-JEPA** | 中强：latent intervention + causal inductive bias，但作者明确不声称 causal identifiability | ★★★★★ |
| **Causality-aware / Temporal World Model** | object dependency、action→future dynamics 或 causal attention | STICA、LingBot-VA | 较弱到中等：dependency / temporal causality，不等于正式 causal inference | ★★★★☆ |

**最值得注意的空缺**是：  
目前较强的 causal world model 大多仍在 **synthetic object scenes、factored state、低维 simulation** 上验证；而真实视觉、3D/4D world state、egocentric interaction、HOI 和 real robot 场景中的 **interventional / counterfactual causal world modeling** 仍非常不成熟。

换句话说，最新工作已经开始回答：

\[
\text{“哪些实体之间存在 predictive / causal dependency？”}
\]

但远没有解决：

\[
\boxed{
\text{“在一个真实 3D/4D 世界中，agent 的 intervention 如何改变世界，
以及换一个 intervention 世界会怎样？”}
}
\]

---

# 1. Causal-JEPA: Learning World Models through Object-Level Latent Masking

**作者**：Heejeong Nam, Quentin Le Lidec, Lucas Maes, Yann LeCun, Randall Balestriero  
**年份**：2026  
**发表情况**：ICML 2026（论文 HTML 标注 Machine Learning, ICML）；arXiv 2602.11389  
**可靠链接**：

- arXiv: https://arxiv.org/abs/2602.11389
- 官方代码: https://github.com/galilai-group/cjepa

**代表图**：Fig. 1, *C-JEPA training pipeline*；Fig. 2, *Object-level latent masking in C-JEPA*。  
**来源**：arXiv HTML 原文。  
本报告不重新裁切论文图片，建议直接查看原文 Fig. 1/2，以避免图片资产链接失效或脱离上下文。

## 核心概括 / Insight

这是目前最值得关注的新一代 **causal predictive world model** 之一。

作者的出发点是：**object-centric representation 本身并不保证模型真正学习 object interaction**。即使已经把视频表示成 objects/slots，predictor 仍可能依赖每个 object 自己的 temporal dynamics 或统计 shortcut，而不理解 object-object interaction。

C-JEPA 的核心设计非常简单：

> **把某个 object 在 history 中的大部分 latent trajectory 整体 mask 掉，只保留最早的 identity anchor，迫使模型必须根据其他 objects 的状态、actions / proprioception 等信息推断这个 object 的状态。**

因此，模型不能只做：

\[
O_t^i \rightarrow O_{t+1}^i
\]

而必须利用：

\[
\{O^j\}_{j\neq i},\, a_t
\rightarrow O^i
\]

作者把这种 object-level masking 解释为一种 **latent intervention on predictor observability**，并认为它产生了 counterfactual-like training queries，使 interaction reasoning 变成完成预测任务所必需的能力。

### 非常重要的“因果”边界

论文自己明确强调：

> C-JEPA 中的 “causal” 指的是在 object-level masking 下保持稳定的、时间有向的 predictive dependency，以及由 latent observability intervention 诱导的 causal inductive bias；**并不声称 causal identifiability**。

所以这篇论文的贡献应该准确理解为：

**causal inductive bias for world modeling**，而不是“恢复真实 SCM”。

## Pipeline

**输入**：

- 视频帧 \(X_{t-T_h+1:t}\)
- 可选 action \(a_t\)
- 可选 proprioception \(p_t\)

**过程**：

1. 冻结的 object-centric encoder（主要使用 VideoSAUR + frozen DINOv2）；
2. 每帧编码成固定数量 object slots：
   \[
   S_t=\{s_t^1,\ldots,s_t^N\}
   \]
3. 训练阶段选若干 object，把其 history latent 大部分 mask；
4. 保留最早时刻的 object identity anchor；
5. ViT-style masked predictor 同时：
   - 恢复 masked history；
   - 预测 future object latents；
6. 使用 latent L2 prediction objective；
7. inference 时不再 mask history，只 rollout future object states。

**输出**：

\[
\hat S_{t+1:t+T_p}
\]

即未来 object-centric latent trajectories。

## 实验概括

### 1. CLEVRER：视觉物理 / 因果推理

- 数据：CLEVRER synthetic multi-object interaction videos；
- 输入 rollout：128 frames；
- 预测至 160 frames；
- downstream reasoning：ALOE；
- 问题类型包括 descriptive / predictive / explanatory / counterfactual；
- baseline：
  - SlotFormer；
  - OCVP-Seq；
  - OC-JEPA（同架构但 history 不做 object masking），是最关键的控制变量。

**关键结果：**

VideoSAUR encoder 下：

- OC-JEPA counterfactual per-question：**47.68**
- C-JEPA（mask 4 objects）：**68.81**
- 绝对提升 **+21.13 points**

SAVi encoder 下：

- OC-JEPA：41.10
- C-JEPA（mask 2 objects）：60.19
- +19.09 points

这组实验最有价值的地方不是简单“accuracy 更高”，而是：

> 同一 predictor / object representation，仅改变 masking objective，就显著提高 counterfactual reasoning。

因此实验支持“interaction-aware objective 比单纯 object-centric representation 更关键”。

### 2. Push-T：contact-rich model predictive control

- benchmark：Push-T；
- planner：CEM + MPC；
- patch-based baseline：DINO-WM；
- object-based controlled baselines：OC-DINO-WM、OC-JEPA。

结果：

- DINO-WM：91.33% success
- C-JEPA：88.67%
- OC-JEPA：76.00%
- OC-DINO-WM：60.67%

同时 C-JEPA 只使用 patch-based world model **约 1.02% 的 latent input feature size**，作者报告 MPC 速度超过 **8× faster**。

### 实验实际支持什么？

支持：

- object-level masking 明显改善 interaction/counterfactual reasoning；
- 在 compact object latent 中进行 world modeling 可以大幅降低 planning cost；
- masking-induced inductive bias 比“仅 object-centric encoder”更有效。

**没有证明：**

- 学到了真实可识别的 causal graph；
- 对真实世界复杂 3D/4D interaction 泛化；
- 对 unseen causal mechanisms 有系统性 OOD generalization。

## 代码与数据开放

- 官方代码已公开；
- 使用公开 CLEVRER、Push-T；
- 未提出新的大规模数据集。

## 局限 / Failure Cases

作者实验直接显示一个重要失败模式：

- mask 太少，interaction forcing 不够；
- **mask 太多会把真正必要的信息也删掉**。

例如 SAVi encoder 下，mask 4 objects 后 counterfactual per-question 反而从 41.10 降至 34.06。

因此最优 masking 强烈依赖 object representation 的质量和稳定性。

其他局限：

- CLEVRER 是 synthetic 场景；
- Push-T 任务单一；
- object slot 本身依赖现有 object-centric encoder；
- 没有显式 3D/4D grounding；
- masking 是对 **observability** 的 intervention，不是直接对真实 environment variables 施加 \(do(\cdot)\)。

**阅读判断**：  
目前这是最适合你关注的论文之一，因为它给出了一个非常干净的答案：**如何让 latent world model 不得不学习 interaction dependency**。但它距离真正“3D grounded interventional world model”仍有很明显的空间。

---

# 2. A Unifying Perspective on Causal World Models: From Observations to Representations to Structure

**作者**：Avinash Kori, Fabrizio Russo  
**年份**：2026  
**发表情况**：arXiv preprint，2026-08-13 提交；截至检索日未确认正式会议发表  
**可靠链接**：

- arXiv: https://arxiv.org/abs/2608.13456

**代表图**：Fig. 1，论文提出的 *Causal Ladder* / Causal World Model abstraction。  
**来源**：arXiv 原文。

## 核心概括 / Insight

这篇不是一个新的 SOTA model，而是一篇**非常新的理论/概念框架论文**，对“什么才应该叫 Causal World Model”很有价值。

作者认为 world model 不应仅仅能生成 plausible future，而应捕获：

- entity properties；
- entity–entity interactions；
- entity–environment interactions；
- action / intervention 下的 transition；
- 支持 decision-making 所需的 utility / task structure。

论文把 CWM 从 observation 一层层提升到：

\[
x_t
\rightarrow
v_t
\rightarrow
r_t
\rightarrow
G_r
\]

其中：

- \(x_t\)：原始 observation；
- \(v_t\)：entity-level representation；
- \(r_t\)：structured relational state；
- \(G_r\)：causal relational structure。

其核心价值是明确区分：

> **predictive dynamics ≠ identified causal dynamics**。

尤其重要的是，论文指出：

\[
P(r_{t+1}\mid r_t,a_t)
\]

只有在满足 consistency、positivity，以及 action randomized 或 no-unmeasured-confounding 等条件下，才能被解释成：

\[
P(r_{t+1}\mid r_t;do(a_t=a))
\]

这对当前大量“action-conditioned world model = causal world model”的说法是非常重要的校正。

## Pipeline / Framework

这篇没有传统神经网络 pipeline，而是提出一个 CWM 抽象：

1. observation encoder：\(x_t\rightarrow v_t\)；
2. entity / relational state：\(v_t\rightarrow r_t\)；
3. causal structure：\(G_r\)；
4. action-conditioned / interventional transition；
5. counterfactual / generative reasoning；
6. utility-aware decision making。

## 实验

**无实证实验。**

这是一个 formal / conceptual paper，不应把它当成 empirical SOTA 方法。

## 代码与数据

- 无新数据；
- 无必要的训练代码。

## 局限

- 理论/框架性工作，尚未证明实际视觉 world model 能满足其识别条件；
- entity / relational representations 如何从真实图像自动学习仍是开放问题；
- 对真实机器人和 3D/4D world state 没有实验验证。

**阅读判断**：  
如果你要写 Causal HOI World Model 的 motivation，这篇非常值得作为“概念基准”：它帮助你避免把普通 action-conditioned prediction 直接说成 causal inference。

---

# 3. Language Agents Meet Causality — Bridging LLMs and Causal World Models

**作者**：John Gkountouras, Matthias Lindemann, Phillip Lippe, Efstratios Gavves, Ivan Titov  
**年份**：2025  
**发表情况**：ICLR 2025  
**可靠链接**：

- ICLR Proceedings: https://proceedings.iclr.cc/paper_files/paper/2025/hash/5c5bc3553815adb4d1a8a5b8701e41a9-Abstract-Conference.html
- arXiv: https://arxiv.org/abs/2410.19923
- 官方代码: https://github.com/j0hngou/LLMCWM

**代表图**：原文 Fig. 1/2，展示 causal representation learner、causal transition model 与 LLM planner 的连接。  
**来源**：ICLR 2025 论文 / arXiv 原文。

## 核心概括 / Insight

这篇工作比很多“causal world model”更接近正式 causal representation learning。

它的核心 idea：

> **LLM 很会高层规划，但其 causal knowledge 来自互联网，可能错误或与当前环境不匹配；因此应该让 agent 自己从环境数据中学习一个 causal world model，再把 causal state / transition 翻译成语言供 LLM 查询。**

因此 world model 不只是一个 future predictor，而是一个 **learned causal simulator**。

方法继承 BISCUIT 的 causal representation learning 思路，从 high-dimensional image observations 中学习 latent causal variables，并通过 action/intervention 信息识别环境 dynamics。

## Pipeline

**输入**：

- 当前图像 observation；
- 自然语言 action description。

**过程**：

1. causal representation learner：
   \[
   I_t\rightarrow z_t^{causal}
   \]
2. action encoder：
   \[
   a_t^{text}\rightarrow e(a_t)
   \]
3. causal transition：
   \[
   (z_t^{causal},a_t)\rightarrow z_{t+1}^{causal}
   \]
4. causal mapper 将 latent variables 映射到可理解的 state descriptors；
5. LLM 使用 world model rollout 的 state descriptions 做 reasoning；
6. planning 使用 LLM proposal + CWM simulation + RAP/MCTS-style search。

**输出**：

- next causal world state；
- rollout state description；
- 最终 action plan。

## 因果假设

论文依赖 BISCUIT 一类 identifiable causal representation learning 的假设，例如：

- 不同 causal variables 应有可区分的 binary interaction patterns；
- intervention pattern 随时间具有足够变化。

这比 C-JEPA 的 “causal inductive bias” 更强，但也意味着方法对 intervention richness 有较强假设。

## 实验概括

### 环境

1. **GridWorld**
   - controllable causal processes；
   - 用于不同 temporal horizon 的 causal inference / planning。

2. **AI2-THOR / iTHOR kitchen**
   - 3D rendered environment；
   - 状态包括物体位置、open/closed、pickup state；
   - actions 包括 Toggle / Open / Pickup / Put / Move / NoOp。

### Causal inference

在 iTHOR 中：

- ToggleObject：约 **95.7%**
- OpenObject：约 **92.6%**
- PutObject：约 **50.6%**
- PickupObject：约 **43.1%**

作者指出 pickup / put 这类涉及更复杂位置和对象关系的 action 明显更难。

### Planning

论文使用 LLaMA 3 作为 reasoning/planning agent。

例如：

- GridWorld 2-step：
  - causal-aware：约 **0.95**
  - LM-only：约 **0.20**
- iTHOR 2-step：
  - causal-aware：约 **0.58**
  - LM-only：约 **0.25**
- iTHOR 4-step：
  - causal-aware：约 **0.44**
  - LM-only：约 **0.11**

实验支持：

> environment-specific causal world model 对长 horizon planning 的价值会比单纯 LLM commonsense 更明显。

### 计算

作者报告训练主要在 A100 上完成：

- autoencoder / representation 部分约 1–2 days；
- flow / language-related heads 约 0.5–1 h。

## 代码与数据

- 官方代码公开；
- 包含环境数据生成脚本；
- pretrained models 通过作者链接 / Zenodo 提供。

## 局限

作者明确指出：

- 当前 environments 仍较简单；
- real-world scalability 尚未证明；
- causal variables 的解释/映射仍有 supervision 成分；
- 希望未来减少对 labeled causal variables 的依赖。

额外可观察 failure：

- iTHOR 中涉及 position / pickup / put 的 dynamics 明显更困难；
- 视觉输入虽来自 3D simulator，但不等于真实 3D perception；
- 没有真实 robot / ego video；
- 识别条件依赖 intervention diversity。

**阅读判断**：  
这是“**causal latent simulator 真正用于 counterfactual planning**”最值得看的代表之一，也很适合和 C-JEPA 对比：

- C-JEPA：弱 causal assumption、强 scalable predictive bias；
- 本文：更正式的 causal representation，但环境和假设更受限。

---

# 4. Robust Agents Learn Causal World Models

**作者**：Jonathan Richens, Tom Everitt  
**年份**：2024  
**发表情况**：ICLR 2024 Oral  
**可靠链接**：

- OpenReview: https://openreview.net/
  - 可搜索完整标题 *Robust agents learn causal world models*
- arXiv: https://arxiv.org/abs/2402.10877

**代表图**：原文 Fig. 1（causal influence diagram / domain shift setup）与 Fig. 2（regret 与 causal model recovery error）。  
**来源**：ICLR 2024 / arXiv 原文。

## 核心概括 / Insight

这篇论文的价值主要是**理论上解释为什么 robust intelligent agent 需要 causal world model**。

核心结果可以概括为：

> 如果一个 agent 能在足够丰富的 local distribution shifts 下做到低 regret、快速适应，那么它的内部知识必须能够恢复环境的近似 causal model；反过来，拥有 causal model 也足以支持这种 robust adaptation。

随着 regret 接近 0，恢复出的 causal model 也趋近真实 causal model。

它给 Causal WM 提供的是一种理论 justification：

\[
\text{OOD robust adaptation}
\Rightarrow
\text{causal structure knowledge}
\]

而不是一种新的视觉 world-model architecture。

## Pipeline / 理论设定

无常规 neural pipeline。

论文考虑：

- 数据生成 causal Bayesian network；
- agent 需要在多个 shifted environments 中决策；
- domain shift 对 causal mechanisms 做局部改变；
- 根据 agent 的决策行为与 adaptation properties，分析其是否必须包含 causal model。

## 实验

主要是用于验证理论趋势的 synthetic experiments。

论文随机生成大量 causal environments（图中实验使用约 1000 个随机环境），比较：

- agent regret；
- 从 agent 行为中恢复 causal model 的误差。

实验支持理论预测：

> causal model error 随 robust adaptation / regret 改善而下降。

但这不是 embodied/visual benchmark。

## 代码与数据

- 主要为理论与 synthetic simulation；
- 未依赖大型公开数据集；
- 本报告未确认独立官方代码仓库，因此不声称代码已发布。

## 重要局限

这一点必须特别注意：

论文主定理关注的核心 setting 并**没有覆盖一般意义的 mediated MDP**——即 action 经 environment state 再影响 future state / utility 的复杂 sequential manipulation 情况。

此外：

- 变量主要是离散 / 简化设定；
- 依赖 causal sufficiency 等理论假设；
- domain shifts 是特定类别 local interventions；
- 没有视觉 world model；
- 没有 robot manipulation。

**阅读判断**：  
这篇非常适合回答“**为什么 causal world model 有学术必要性？**”，但不能直接作为 HOI architecture baseline。

---

# 5. Building Minimal and Reusable Causal State Abstractions for Reinforcement Learning

**方法简称**：Causal Bisimulation Modeling (CBM)  
**作者**：Zizhao Wang, Caroline Wang, Xuesu Xiao, Yuke Zhu, Peter Stone  
**年份**：2024  
**发表情况**：AAAI 2024  
**可靠链接**：

- AAAI: https://ojs.aaai.org/index.php/AAAI/article/view/29507
- arXiv: https://arxiv.org/abs/2401.12497

**代表图**：建议查看论文中 CBM causal dynamics / state abstraction pipeline 图。  
**来源**：AAAI 2024 原论文。

## 核心概括 / Insight

CBM 关注一个非常重要但常被忽视的问题：

> 一个 good world state 不应该包含所有 observable variables，而应该只保留完成当前任务真正需要的 **causal variables**。

它先学习 environment 的 reusable causal dynamics，再根据具体 reward/task 找出与任务结果有 causal dependency 的变量，构建最小 state abstraction。

所以它区分：

- **environment dynamics**：可跨任务复用；
- **task reward dependency**：任务相关；
- **policy state**：只保留当前任务真正需要的变量。

这给 causal world model 一个很重要的思想：

\[
\boxed{
\text{Good state representation}
\neq
\text{maximum reconstruction information}
}
\]

而是：

\[
\text{minimal intervention-relevant state}
\]

## Pipeline

**输入**：

- factored low-dimensional state \(s_t\)；
- action \(a_t\)；
- reward \(r_t\)。

**过程**：

1. 学 causal dynamics dependency；
2. 使用 implicit / energy-based dynamics model，判断哪些输入变量真正影响下一状态变量；
3. 学 task-specific reward dependency；
4. 从 causal graph 中回溯与 reward 有关的 ancestors；
5. 得到 binary state mask；
6. policy 只在 minimal causal abstraction 上学习。

**输出**：

- reusable causal dynamics model；
- task-specific minimal state abstraction；
- downstream policy。

## 实验

### 环境

- 两个 Robosuite manipulation environments；
- 四类 manipulation tasks，包括 Pick、Stack、Tool-use series；
- 另包含 DMC Cheetah / Walker 类任务分析。

为了系统测试 abstraction，作者加入：

- 20 controllable distractor variables；
- 20 uncontrollable distractor variables。

### Causal graph learning

Implicit dynamics 相比 explicit predictor 的 causal graph recovery 更准确。

示例：

- Block env：约 90.5 ± 0.4 vs 87.5 ± 0.1
- Tool-use：约 85.5 ± 0.1 vs 82.6 ± 0.2

state abstraction accuracy 的差距更明显：

- Pick：implicit 约 95.7 ± 6.0
- explicit 约 53.2 ± 4.6

### Downstream RL

baseline：

- CDL；
- TIA；
- Denoised MDP；
- Oracle；
- Full-state。

结果显示 CBM 的 minimal causal state 在多个任务上达到接近 oracle 的 sample efficiency，并优于保留过多无关变量的方法。

论文在 causal graph/dynamics 实验使用约 3 seeds，task learning 使用约 5 seeds，并报告误差范围。

## 代码与数据

- 基于 Robosuite / DMC；
- 本次检索没有在 AAAI/arXiv 主页面可靠确认一个独立官方 CBM 代码仓库，因此这里不声称代码已公开。

## 局限

最大限制：

> **输入已经是 factored low-dimensional state，而不是从图像中发现 causal variables。**

因此它解决的是：

\[
\text{known state factors}
\rightarrow
\text{causal abstraction}
\]

而不是：

\[
RGB/Video
\rightarrow
\text{unknown causal state}
\]

另外：

- causal graph ground truth 主要存在于 simulator；
- distractors 是人工构造；
- 没有 counterfactual visual rollout；
- 没有 3D/4D representation learning。

**阅读判断**：  
这篇对你的研究很有启发：真正值得学习的不是 mesh/pose 越多越好，而是学习一个 **minimal causal state**。

---

# 6. Object-Centric World Models for Causality-Aware Reinforcement Learning

**方法**：STICA  
**作者**：Yosuke Nishimoto, Takashi Matsubara  
**年份**：2026  
**发表情况**：AAAI 2026  
**可靠链接**：

- AAAI: https://ojs.aaai.org/index.php/AAAI/article/view/39642
- arXiv: https://arxiv.org/abs/2511.14262

**代表图**：Fig. 1，STICA overall architecture。  
**来源**：AAAI / arXiv 原论文。

## 核心概括 / Insight

STICA 认为 holistic world latent 在 object-rich environment 中效率不高，因此：

1. observation 被拆为 object-centric tokens；
2. Transformer world model 学 object token dynamics；
3. policy / value network 估计 token-level cause–effect relevance；
4. causality-aware attention 重点关注真正影响 reward / decision 的 objects。

它的核心价值是：

> **world model 不只是 object-centric，policy 也应该显式选择“哪些 object 对当前 decision 有影响”。**

## Pipeline

**输入**：

- image observation；
- action；
- reward。

**过程**：

1. object-centric encoder 得到 object tokens；
2. 加入 action / reward tokens；
3. Transformer world model 预测下一时刻 object tokens、reward、discount；
4. policy/value networks 估计 token-level dependency score；
5. causality-aware attention 根据 dependency 调节决策。

**输出**：

- imagined object-level world trajectories；
- policy action / value。

## “Causal” 的边界

这篇必须谨慎引用。

作者实际使用的是 **token-level cause–effect / dependency score** 来指导 attention。  
它更接近：

> causality-aware object dependency

而不是完整 causal discovery / intervention identification。

所以不能用这篇证明：

> “object-centric attention 已经学到了真实 causal graph”。

## 实验

### Safety Gym

- 8 个 object-rich 3D tasks；
- first-person observation；
- baseline：TWM、DreamerV3、TD-MPC2；
- learning curves 多 run 汇总；
- STICA 在绝大多数任务上表现最好或最具竞争力。

### OCVRL

包含：

- 2D object-goal；
- object-interaction；
- 3D object-reaching。

典型 final success：

| Model | Object-goal | Interaction | 3D Reaching |
|---|---:|---:|---:|
| TWM | 0.727 | 0.080 | 0.772 |
| DreamerV3 | 0.677 | 0.156 | 0.697 |
| STICA | **0.737** | **0.333** | **0.867** |

消融表明：

- object-centric WM 本身只带来部分收益；
- causality-aware attention 对 downstream performance 的贡献更明显。

## 代码 / 数据

- 基于公开 RL benchmarks；
- arXiv/作者页面声明 code available；可优先从论文页提供的代码入口确认最新版本。

## 局限

- “causality” 主要是 learned dependency / relevance，不是正式 intervention；
- 没有 counterfactual world-state evaluation；
- benchmark 以 simulation 为主；
- 没有真实机器人；
- 没有显式 3D world-state causal consistency。

**阅读判断**：  
值得作为 **object-centric causal WM** 的相邻工作，但如果你做真正 Causal HOI，应明确比它更进一步：从 relevance/dependency 走到 **interventional / counterfactual dynamics**。

---

# 7. Causal World Modeling for Robot Control (LingBot-VA)

**作者**：Lin Li, Qihang Zhang, Yiming Luo, Shuai Yang, Ruilin Wang, Fei Han, Mingrui Yu, Zelin Gao, Nan Xue, Xing Zhu, Yujun Shen, Yinghao Xu  
**年份**：2026  
**发表情况**：arXiv 2601.21998；官方项目/代码已公开。是否作为正式会议版本引用，应以作者仓库最新信息为准。  
**可靠链接**：

- arXiv: https://arxiv.org/abs/2601.21998
- 官方代码: https://github.com/Robbyant/lingbot-va

**代表图**：Fig. 2，LingBot-VA architecture。  
**来源**：arXiv 原文。

## 核心概括 / Insight

这是机器人 World Action Model 中非常新的代表工作，但它也是理解“causal”一词被过度使用的好例子。

LingBot-VA 的基本逻辑：

> video prediction 可以学习 action 与 future visual dynamics 的关系；因此将 video world model 与 action prediction 在同一 autoregressive diffusion framework 中联合学习，可以给 robot policy 提供更密集的 dynamics supervision。

架构上：

- video latent stream；
- action stream；
- MoT；
- autoregressive causal ordering；
- visual transition 再反哺 action generation；
- closed-loop ground-truth observation feedback；
- asynchronous execution。

## Pipeline

**输入**：

- 当前多视角 RGB observations；
- robot state / language instruction。

**过程**：

1. video model 预测未来 visual latent；
2. action model 根据 visual transition 预测 action；
3. video/action 交替 autoregressive generation；
4. causal attention mask 保证时间/信息顺序；
5. real observation 定期替换 imagined state，形成闭环；
6. KV cache + async execution 加速。

**输出**：

- future video latent；
- robot action chunk。

## 实验

论文使用约 5.3B 总模型规模，训练数据包括多来源 robot datasets。

公开描述中包含约 **16K hours** robot data，并进行大规模 video-action pretraining。

### RoboTwin 2.0

- 50 tasks；
- Clean + Randomized；
- 多任务训练；
- 论文报告 Easy / Hard 均取得非常强结果，long-horizon 任务优势更明显。

### LIBERO

论文报告平均约 **98.5%**；  
评估采用多个 seeds / 大量 trials。

需要注意公平性：

> 部分 baseline 数字来自已有论文/报告，而非全部由作者在完全相同代码和训练设置下重新跑，因此不宜把小幅差距解释成严格 apples-to-apples superiority。

### Real-world

论文展示：

- long-horizon manipulation；
- few-shot post-training；
- novel object / layout generalization。

这些结果支持的是实际机器人控制能力，而不是正式 causal identification。

## 代码 / 数据

- 官方代码仓库公开；
- model weights / 部分 post-training datasets 公开；
- RoboTwin / LIBERO 训练使用方式有说明。

## 最重要的局限：它的 “causal” 不是 causal inference

LingBot-VA 中的 causality 主要指：

\[
action \rightarrow future\ visual\ dynamics
\]

以及 autoregressive **causal attention / temporal ordering**。

论文并没有：

- causal graph discovery；
- \(do(\cdot)\) intervention identification；
- structural causal model；
- counterfactual benchmark；
- identifiability proof。

因此从严格 causal learning 角度，它更适合放在：

> **causality-motivated generative world model**

而不是“formal Causal WM”。

**阅读判断**：  
非常值得用作机器人世界模型 baseline，但如果你的论文强调 causal reasoning，必须在定义上与 LingBot-VA 拉开距离。

---

# 8. 最新值得跟踪、但暂不建议作为核心 anchor 的工作

以下是检索到的 2026 新预印本。它们有一定相关性，但当前影响力、验证规模或 peer-review 状态不足以和上述核心论文等量齐观。

## 8.1 Learning Implicit Causal World Models from Multi-Agent Demonstrations

**作者**：Jasorsi Ghosh  
**年份**：2026-07  
**发表情况**：arXiv preprint  
**链接**：https://arxiv.org/abs/2607.26336

### 核心 idea

从 offline multi-agent demonstrations 学 environment dynamics，利用 policy variance 和 sequential backdoor condition 区分 strategic intent 与环境 causal transition，不要求预先给定 causal graph。

### 实验

Two-Door、Navigation、Giveway 等 coordination tasks，覆盖 full / partial observability。

### 当前判断

**值得关注，但当前证据偏小型 synthetic / coordination benchmark。**

它的价值在于：

> causal WM 不一定需要主动 intervention dataset；agent policy variation 本身可能提供 identification signal。

但尚不能说明能扩展到真实视觉/机器人。

---

## 8.2 Entity-Centric World Models: Interaction-Aware Masking for Causal Video Prediction

**方法**：IA-JEPA  
**年份**：2026-05  
**发表情况**：arXiv preprint  
**链接**：https://arxiv.org/abs/2605.15466

### 核心 idea

传统 patch masking 更容易学习 texture/static shortcut。IA-JEPA 特别 mask collision / momentum transfer 等 interaction-relevant entities，希望逼迫 JEPA latent 学 physical events。

在 CLEVRER causal reasoning 上报告：

- IA-JEPA：14.26%
- standard patch-masked baseline：3.22%

并报告 latent entropy、physical energy linear probing 等分析。

### 当前判断

它与 C-JEPA 同属：

> **用 masking objective 改变 predictive representation 学到什么**

但目前：

- 单作者预印本；
- causal reasoning absolute accuracy 仍不高；
- benchmark 较有限。

因此更适合作为 C-JEPA 周边的新趋势，而非核心 anchor。

---

## 8.3 UWM-JEPA: Predictive World Models That Imagine in Belief Space

**作者**：Santosh Kumar Radha, Oktay Goktas  
**年份**：2026-05  
**发表情况**：arXiv preprint  
**链接**：https://arxiv.org/abs/2605.25313

### 核心 idea

它关注 partial observability 下的 **counterfactual action rollout**：

> 单一 vector latent 难以表达“多个兼容 hidden futures”的 belief，因此使用 density-matrix latent + learned unitary predictor 保存 uncertainty structure。

实验在 hidden-velocity toy setting 中表明，counterfactual-target training 对 action sensitivity 很关键。

### 当前判断

概念新颖，但离视觉 / embodied world model 较远，目前仍偏 proof-of-concept。

值得关注的 insight 是：

\[
\text{Counterfactual world modeling}
\neq
\text{deterministic next-latent prediction}
\]

partial observability 下应显式考虑 **belief over alternative futures**。

---

# 9. 奠基性工作：建议补读

这些不是最新，但帮助理解上述论文。

## 9.1 BISCUIT: Causal Representation Learning from Binary Interactions

**年份**：2023  
**链接**：https://arxiv.org/abs/2306.09643

与本主题关系：

- 从 high-dimensional observations 学 latent causal variables；
- 利用 binary intervention/interaction patterns 获得 identifiability；
- 是 *Language Agents Meet Causality* 的重要方法基础。

**推荐理由**：如果你想认真讨论“latent 变量什么时候有资格叫 causal variable”，这篇比单纯读 JEPA 更重要。

---

## 9.2 Causal Dynamics Learning for Task-Independent State Abstraction

**简称**：CDL  
**年份**：2022，ICML 2022  
**链接**：https://arxiv.org/abs/2206.13452  
**代码**：https://github.com/wangzizhao/CausalDynamicsLearning

核心：

- 学 sparse causal dynamics；
- 删除与环境 transition 无关的状态依赖；
- 获得可跨任务复用的 task-independent state abstraction。

它是 CBM 的重要前序工作。

---

## 9.3 CoPhy: Counterfactual Learning of Physical Dynamics

较早，但如果你的兴趣是“**同一个场景，在不同 intervention 下会发生什么**”，CoPhy 仍是值得回看的 physical counterfactual benchmark / modeling 工作。

其价值不是当前 SOTA，而是历史上较早把：

\[
\text{physical dynamics}
+
\text{counterfactual question}
\]

明确联系起来。

---

# 10. 横向比较：这些论文到底谁“最 causal”？

| 工作 | 视觉输入 | Object-centric | 显式 causal variables / graph | Intervention | Counterfactual | Planning/control | 3D/robot | 因果强度判断 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **Causal-JEPA** | ✓ | ✓ | ✗ | latent observability intervention | ✓ counterfactual-like + CLEVRER QA | ✓ Push-T MPC | robot sim | **中强：causal inductive bias** |
| **Language Agents Meet Causality** | ✓ | 部分 | ✓ latent causal variables | ✓ action/interactions | ✓ rollout/planning | ✓ | iTHOR 3D sim | **强：CRL + causal simulator** |
| **Robust Agents Learn Causal WM** | ✗ | N/A | ✓ theoretical CBN | ✓ domain mechanism shifts | 理论上支持 | decision | ✗ | **强理论，弱 embodied** |
| **CBM** | ✗，factored state | 变量级 | ✓ learned dynamics graph | implicit action intervention | 非主要评估 | ✓ RL | manipulation sim | **强：state-level causal dynamics** |
| **STICA** | ✓ | ✓ | ✗ | ✗ | ✗ | ✓ RL | 3D sim | **中弱：dependency / causality-aware** |
| **LingBot-VA** | ✓ | ✗ | ✗ | action-conditioned | 不做正式 counterfactual test | ✓ real robot | ✓ | **弱：temporal/action causality** |
| **Implicit CWM from MA demos** | 低维/sim | agent-centric | implicit | policy variance | 部分 | multi-agent | sim | **有理论意图，证据尚早** |
| **IA-JEPA** | ✓ | ✓ | ✗ | masking | causal QA | ✗ | visual benchmarks | **中：interaction bias** |

---

# 11. 研究脉络：Causal World Model 正在从什么走向什么？

我认为目前出现了一个清楚的演进：

## 阶段 1：Predictive World Model

\[
z_t,a_t\rightarrow z_{t+1}
\]

只要求预测未来正确。

---

## 阶段 2：Structured / Object-Centric World Model

\[
\{O_t^i\},a_t
\rightarrow
\{O_{t+1}^i\}
\]

开始暴露 entities / relations，减少 pixel-level shortcut。

---

## 阶段 3：Causal Inductive Bias

典型 C-JEPA：

\[
\text{latent intervention / masking}
\rightarrow
\text{force interaction reasoning}
\]

问题从“预测未来”变成：

> **预测是否真正依赖正确的 interaction variables？**

---

## 阶段 4：Interventional Causal World Model

目标是：

\[
S_t,\operatorname{do}(a)
\rightarrow
S_{t+k}^{(a)}
\]

并同时能够回答：

\[
S_t,\operatorname{do}(a')
\rightarrow
S_{t+k}^{(a')}
\]

也就是：

> **same world, alternative interventions, alternative futures**。

目前这一步在真实视觉/机器人世界中仍明显不足。

---

## 阶段 5：3D/4D-Grounded Causal World Model —— 明显空缺

对于 embodied / HOI，更有意义的最终形式可能不是 generic latent：

\[
z_t\rightarrow z_{t+1}
\]

而是：

\[
\boxed{
S_t^{3D/4D},
\operatorname{do}(a)
\rightarrow
S_{t+k}^{3D/4D}
}
\]

并要求 causal effect：

- 对 camera/viewpoint invariant；
- 对 appearance nuisance robust；
- 对 object identity / embodiment 有 transferable mechanism；
- 支持 counterfactual fork；
- 可以 novel-view render / 3D evaluate。

目前上述核心论文中，**没有一篇完整解决这个问题**。

---

# 12. 对 3D/4D HOI World Model 最有价值的研究启发

如果目标是将 causality 与 3DV / HOI 结合，我认为不应简单做：

\[
\text{RGB}\rightarrow
\{\text{mask, pose, mesh, contact, trajectory}\}
\]

然后宣称“显式物理变量 = causal”。

更值得研究的是：

## 12.1 3D/4D 作为 causal grounding，而不是 causal definition

例如：

\[
I_t
\rightarrow
Z_t^{Causal-4D}
\]

然后学习：

\[
(Z_t^{Causal-4D},do(a))
\rightarrow
Z_{t+k}^{Causal-4D}
\]

3D point / pose / flow / mesh / contact 可以作为：

- grounding supervision；
- probes；
- evaluator；

但核心 scientific object 是：

> **intervention-induced world transformation**。

---

## 12.2 从 world prediction 到 causal delta prediction

HOI 短时 interaction 中，大部分世界并不变化。

因此比重建完整 future 更自然的是：

\[
\boxed{
\Delta Z
=
F(Z_t,do(a))
}
\]

即只建模 intervention 导致的 world change。

这是一个更紧凑的 causal world model formulation。

---

## 12.3 真正需要的 benchmark 是 counterfactual，而不是只看 prediction

例如固定同一初始 3D world：

\[
S_t
\]

构造：

- \(a_1\)：有效 interaction；
- \(a_2\)：轨迹略偏，interaction 不发生；
- \(a_3\)：不同方向 / 不同 manipulation；
- \(a_4\)：no-op。

要求：

\[
S_t
\xrightarrow{a_1,a_2,a_3,a_4}
\{S_{t+k}^{1},S_{t+k}^{2},S_{t+k}^{3},S_{t+k}^{4}\}
\]

这种 **same-world counterfactual branching** 比普通 video prediction 更能验证 model 是否真正利用 intervention。

---

# 13. 推荐阅读优先级

如果只读 6 篇，我建议：

1. **Causal-JEPA (2026)**  
   最新、最直接的 object-centric causal predictive WM；重点看它如何通过 objective 而非架构强迫 interaction reasoning。

2. **A Unifying Perspective on Causal World Models (2026)**  
   用来澄清“什么情况下 action-conditioned prediction 才能叫 causal”。

3. **Language Agents Meet Causality (ICLR 2025)**  
   目前很典型的 “causal representation → learned simulator → counterfactual planning”。

4. **Robust Agents Learn Causal World Models (ICLR 2024 Oral)**  
   理解 causal WM 为什么对 OOD robustness 有理论价值。

5. **CBM (AAAI 2024)**  
   理解“minimal causal state”而不是“reconstruct everything”。

6. **STICA (AAAI 2026)**  
   理解 object-centric dynamics + causal relevance，同时也学习如何严格区分 dependency 与真正 causal inference。

然后把 **LingBot-VA** 作为机器人生成式 world model 的对照读：

> 它很强，但它也很好地说明了“action-conditioned / temporal causal”与“causal inference / counterfactual reasoning”不是一回事。

---

# 14. 一句话总结

目前因果世界模型最核心的前沿，不再只是：

\[
\text{predict the future}
\]

而是在研究：

\[
\boxed{
\text{learn the variables and mechanisms that determine how
the future changes under intervention}
}
\]

而对于 3D/4D / HOI，一个真正还没有被很好解决的问题是：

\[
\boxed{
\text{Can a world model learn intervention-conditioned,
view-invariant causal transformations of a persistent 3D/4D world,
and use them for counterfactual reasoning?}
}
\]

这比“预测 mask / pose / trajectory / contact”高一个抽象层级，同时又保留了足够强的 3DV grounding。

---

## 参考文献 / 官方入口

1. Nam et al., **Causal-JEPA: Learning World Models through Object-Level Latent Masking**, 2026.  
   https://arxiv.org/abs/2602.11389

2. Kori & Russo, **A Unifying Perspective on Causal World Models: From Observations to Representations to Structure**, 2026.  
   https://arxiv.org/abs/2608.13456

3. Gkountouras et al., **Language Agents Meet Causality -- Bridging LLMs and Causal World Models**, ICLR 2025.  
   https://proceedings.iclr.cc/paper_files/paper/2025/hash/5c5bc3553815adb4d1a8a5b8701e41a9-Abstract-Conference.html

4. Richens & Everitt, **Robust Agents Learn Causal World Models**, ICLR 2024 Oral.  
   https://arxiv.org/abs/2402.10877

5. Wang et al., **Building Minimal and Reusable Causal State Abstractions for Reinforcement Learning**, AAAI 2024.  
   https://ojs.aaai.org/index.php/AAAI/article/view/29507

6. Nishimoto & Matsubara, **Object-Centric World Models for Causality-Aware Reinforcement Learning**, AAAI 2026.  
   https://ojs.aaai.org/index.php/AAAI/article/view/39642

7. Li et al., **Causal World Modeling for Robot Control**, 2026.  
   https://arxiv.org/abs/2601.21998

8. Ghosh, **Learning Implicit Causal World Models from Multi-Agent Demonstrations**, 2026.  
   https://arxiv.org/abs/2607.26336

9. Paidi, **Entity-Centric World Models: Interaction-Aware Masking for Causal Video Prediction**, 2026.  
   https://arxiv.org/abs/2605.15466

10. Radha & Goktas, **UWM-JEPA: Predictive World Models That Imagine in Belief Space**, 2026.  
    https://arxiv.org/abs/2605.25313

11. Lippe et al., **BISCUIT: Causal Representation Learning from Binary Interactions**, 2023.  
    https://arxiv.org/abs/2306.09643

12. Wang et al., **Causal Dynamics Learning for Task-Independent State Abstraction**, ICML 2022.  
    https://arxiv.org/abs/2206.13452
