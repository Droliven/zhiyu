# 视频表征、潜在动作与世界动作模型论文整理

**报告标签**：video representation, latent action, world action model, robot learning, video generation

本报告核验用户给出的三条线索。其中“rapwam”按主题与检索结果规范化为 **RepWAM**；精确拼写 RAPWAM 指向早期并行 Prolog 架构，与本列表另外两篇论文无关。以下内容以 arXiv 正文、作者项目页及官方代码仓库为依据。论文均为 2026 年 arXiv 预印本，尚未核验正式会议或期刊录用信息。

## 1. VideoRAE: Taming Video Foundation Models for Generative Modeling via Representation Autoencoders

**作者：** Zhihao Xie, Junfeng Wu, Xinting Hu, Junchao Huang, Li Jiang  
**年份与发表：** 2026，arXiv preprint，arXiv:2607.14088；DOI 待核验  
**可靠入口：** [arXiv](https://arxiv.org/abs/2607.14088)｜[项目](https://zhxie0117.github.io/VideoRAE/)｜[代码](https://github.com/zhxie0117/VideoRAE)｜[Hugging Face Papers](https://huggingface.co/papers/2607.14088)  
**类别标签：** video representation, representation autoencoder, video tokenizer, video generation, V-JEPA 2, VideoMAEv2  
**代表图：** VideoRAE，Fig. 1，对比传统像素重建驱动的 3D-VAE 与冻结视频基础模型驱动的表示自编码器。来源：[Fig. 1 原图](https://arxiv.org/html/2607.14088v1/x1.png)

![VideoRAE Fig. 1](https://arxiv.org/html/2607.14088v1/x1.png)

### 当前挑战

视频生成通常在 3D-VAE 或离散 tokenizer 的压缩空间中训练，但这些编码器主要优化像素重建和对抗损失，可能弱化高层语义及长时空结构，迫使后续生成器重新学习复杂动态。另一方面，V-JEPA 2、VideoMAEv2 等视频基础模型具有强理解表征，但冻结特征能否同时做到高压缩、可重建且适合自回归和扩散生成，此前缺少系统验证。

### 研究动机

作者的核心主张是：与其从零训练像素驱动的编码器，不如直接把冻结 VFM 的分层特征变成生成潜空间，使语义与宏观时空结构在生成器训练前就进入 latent。阅读判断是，这项工作主要回答“理解表征能否成为视频生成 tokenizer”，并不证明该 latent 自动获得可控物理状态、因果变量或机器人动作语义。

### 技术方案

- **输入：** 视频片段，以及冻结的 V-JEPA 2 或 VideoMAEv2 编码器产生的多尺度时空特征。
- **过程：** 聚合 VFM 不同层级特征，以轻量 1D self-attention projector 压缩；连续分支直接服务 DiT，离散分支用 multi-codebook high-dimensional SimVQ 量化；解码器以像素重建、LPIPS、GAN 及局部—全局 representation alignment（REPA）联合训练，连续分支不依赖 KL 正则。
- **输出：** 可重建视频的连续 latent 或离散 token，并供扩散式或自回归式视频生成器使用。

### 实验结果

作者在 UCF-101 与 TokenBench 上评估重建，在 UCF-101 上评估类别条件生成，并做 2B 规模文本到视频替换实验。离散 V-JEPA 2 版本在 UCF-101 / TokenBench 获得 rFVD 13 / 28；UCF-101 类别条件生成中，AR 与 DiT 分支分别报告 gFVD 40 与 93。与 LARP 的受控训练曲线相比，VideoRAE 在 400 epoch 达到相近于 LARP 2000 epoch 的 gFVD，支持论文所称约 5 倍收敛加速，但这不是端到端训练成本或跨数据集速度定律。REPA 消融把连续/离散 gFVD 分别从 105/67 降到 93/40；多尺度层 8–24 配置报告 PSNR 29.39、gFVD 40。实验支持“VFM latent 对所测视频生成设置有效”，尚不能外推到具身控制或真实世界因果动力学。

### 总结讨论

VideoRAE 的实质贡献是把 frozen VFM encoder、强压缩 projector、双形态 latent 和解码侧语义对齐组合成统一 tokenizer。值得注意的是，VideoMAEv2 版本有更强像素重建，而 V-JEPA 2 版本有更好 gFVD，说明重建保真并不等同于生成友好性。对知域的直接价值在于为“共享视频表征能否同时服务理解与生成”提供可操作接口；它不是 world-action model，也没有动作条件闭环实验。

### 代码与数据

官方项目页与 GitHub 仓库可访问，仓库标注 MIT License；当前公开内容与权重、训练配置的完整可复现程度仍应以实际 release 文件逐项核验。实验使用 UCF-101、TokenBench、Kinetics-600 等数据，完整文本到视频训练数据组成和许可边界需回到仓库说明核验。

### 局限、失败案例与开放问题

- 主要结果来自视频重建和生成基准，没有动作控制或真实交互验证。
- 与工业级 VAE 的训练数据、算力和预训练来源不完全等价，SOTA 表述只适用于论文给定协议。
- 约 5 倍是特定收敛曲线比较，不能解释为所有训练流程或推理均加速 5 倍。
- frozen VFM 的语义偏差、训练数据覆盖及跨领域迁移失败尚未系统展开。
- 2B 文生视频替换实验支持相对收敛优势，但不足以建立更大模型规模下的普遍规律。

## 2. What Matters for Latent Actions in Robot Learning

**作者：** Xizhou Bu, Qingda Hu, Lei Zhou, Lingfeng Zhang, Yingbo Tang, Zihao Liu, Xinyi Tao, Zhiqiang Ma, Qingqiu Huang, Chufeng Tang, Hongbo Wang, Jing Zhang, Jiayi Ma, Hangjun Ye, Wei Li, Xiaoshuai Hao  
**年份与发表：** 2026，arXiv preprint，arXiv:2608.19613；DOI 待核验  
**可靠入口：** [arXiv](https://arxiv.org/abs/2608.19613)｜[项目](https://carldegio.github.io/latent_action.github.io/)｜[代码](https://github.com/XizoB/What-Matters-for-Latent-Actions-in-Robot-Learning)  
**类别标签：** latent action model, robot learning, VLA, representation learning, manipulation, empirical study  
**代表图：** What Matters for Latent Actions in Robot Learning，Fig. 1，统一的三阶段训练与评测框架。来源：[Fig. 1 原图](https://arxiv.org/html/2608.19613v1/main.png)

![What Matters for Latent Actions in Robot Learning Fig. 1](https://arxiv.org/html/2608.19613v1/main.png)

### 当前挑战

潜在动作模型常用无动作视频学习帧间转移，但现有工作在建模范式、正则、latent 维度、动作头和数据规模上各自采用不同设置，难以判断性能来自哪项设计。更实际的障碍是，下游机器人策略评测昂贵，而 probe loss 或重建误差等廉价代理指标是否能可靠预测控制成功率并未得到统一检验。

### 研究动机

作者试图把代表性 LAM 统一到同一自编码框架，在相同三阶段流程下系统比较 41 项设计选择，并检验四种代理指标。其价值是控制混杂变量后给出工程优先级，而不是提出一个单一新模块。阅读判断是，论文所说的 latent action 是从观测转移中学习的紧凑表征；其“causal leakage”指未来帧进入 IDM 造成的信息捷径，不等同于 SCM 意义的因果识别或 `do(·)` 干预。

### 技术方案

- **输入：** Stage I 的相邻无标签视频帧，Stage II 的视频—文本数据及自动标注 latent action，Stage III 的机器人观测、语言指令和少量物理动作数据。
- **过程：** 在统一 IDM–FDM / consecutive-frame-difference autoencoding 框架中比较 LAPO、LAOF、CoMo、语义差分和光流等范式，以及 AE、VAE、VQ-VAE、Sparsity、SIGReg、不同正则强度与 8–1024 维 latent；随后比较 DAP、LAP、JAP 及混合动作头，并以 Linear/MLP Probe、SSIM Gain、MSE Gain 四项代理指标关联下游结果。
- **输出：** 经 latent-action 数据微调的 VLM backbone，以及在 LIBERO、LIBERO-Plus、RoboTwin2.0 和真机任务上输出物理动作的策略。

### 实验结果

论文在三套仿真基准中统一评测 41 项选择，并在 7-DoF Franka Panda + 1-DoF UMI gripper 上验证四个任务。作者报告：原始 LAPO 仍是强基线；简单语义特征差分有竞争力，而光流质量并不稳定转化为控制性能；正则强度通常比正则类型更关键；`d_z=32` 是所测设置的较佳折中；JAP 通过并行预测 latent 与物理动作持续约束 backbone，整体优于只在预训练使用 latent 的 DAP。代理指标只适合粗筛，同维度下 FDM 重建指标总体比 probe 指标相关性更强，跨 latent 维度时相关性下降。Stage II 数据从全量的 14.5% 扩到 100% 后三套基准均改善，LIBERO-Plus 最大提升 9.0 个百分点。真机汇总中 LA-Tuned 为 317/400，基线为 259/400，即 79.25% 对 64.75%，提升 14.5 个百分点；这是受控设置中的实验事实，不代表所有 LAM 都有同等收益。

### 总结讨论

这篇论文最重要的结论不是“某个新 LAM 胜出”，而是 latent action 的收益很大程度来自如何持续塑造 VLM backbone：联合 latent/physical action 目标比把 latent 当一次性预训练标签更有效。它还提醒，低 probe loss 不足以证明下游控制好，像素光流也不是更优动作表征的充分条件。对知域的意义在于提供可证伪的设计轴和统一消融模板；不能把这些相关性结果扩大成 latent action 已恢复真实因果动作变量。

### 代码与数据

作者项目页和官方 GitHub 仓库均可访问，项目页提供代码入口；论文使用 LIBERO、LIBERO-Plus、RoboTwin2.0、OXE 组成的视频数据与自采真机示范。仓库许可证、全部训练权重及 59M 视频标注数据的完整可复现性仍需逐项核验。

### 局限、失败案例与开放问题

- 结论集中在机械臂操作，尚未验证灵巧手、四足、人形或更长时程任务。
- 41 项选择虽广，但仍受统一 backbone、数据混合和三阶段训练协议约束。
- 代理指标对跨 latent 维度排序不可靠，不能替代完整策略评测。
- IDM 访问未来帧存在信息捷径风险；瓶颈与正则不能保证语义可辨识或因果可解释。
- 真机只有四项桌面任务、单一平台和固定相机视角，外部有效性有限。
- 作者明确把更大规模野外视频和跨机器人平台泛化列为未来工作。

## 3. RepWAM: World Action Modeling with Representation Visual-Action Tokenizers

**作者：** Junke Wang, Qihang Zhang, Shuai Yang, Yiming Luo, Yujun Shen, Zuxuan Wu, Yu-Gang Jiang, Yinghao Xu  
**年份与发表：** 2026，arXiv preprint，arXiv:2606.13674；DOI 待核验  
**可靠入口：** [arXiv](https://arxiv.org/abs/2606.13674)｜[项目](https://wdrink.github.io/RepWAM/)｜[代码](https://github.com/wdrink/RepWAM)｜[Hugging Face Papers](https://huggingface.co/papers/2606.13674)  
**类别标签：** world action model, visual-action tokenizer, latent action, robot manipulation, flow matching, video representation  
**代表图：** RepWAM，Fig. 1，RepViTok 将视觉 token 与冻结视觉基础模型对齐，并在同一语义空间中以 IDM/FDM 学习转移 token。来源：[Fig. 1 原图](https://arxiv.org/html/2606.13674v1/x1.png)

![RepWAM Fig. 1](https://arxiv.org/html/2606.13674v1/x1.png)

### 当前挑战

现有 World Action Models 往往沿用视频生成模型中以像素重建为中心的 VAE latent。它们能保存外观，却不一定提供足够的指令语义、接触相关结构或动作转移信息，可能导致未来预测与闭环控制之间存在表征错位。用户给出的“rapwam”经核验最符合本文 RepWAM；报告不把无关的 RAP-WAM Prolog 架构计入馆藏。

### 研究动机

作者希望把视觉状态和引发状态变化的 latent action 放在共享语义空间中建模，让 world expert 的未来预测与 action expert 的控制输出通过同一 representation visual-action tokenizer 对齐。作者称其 DiT 为 causal world action model，主要依据时序生成/注意结构；阅读时不应将这一命名自动解释为结构因果模型、干预识别或反事实保证。

### 技术方案

- **输入：** 视频观测序列、语言指令；适配阶段再加入 embodiment-specific 机器人轨迹和动作。
- **过程：** RepViTok 先以冻结视觉基础模型对齐视觉 latent，再用耦合 IDM/FDM 将相邻视觉 latent 的转移编码为 latent action；预训练阶段以配对的 world expert 与 action expert、flow matching 联合建模未来视觉状态和 latent action；随后用真实机器人示范把 latent dynamics 适配为可执行动作。
- **输出：** 指令条件的未来视觉 latent、对应 latent action，以及闭环执行所需的机器人动作序列。

### 实验结果

RepWAM 在 RoboTwin 2.0 的 50 项任务中报告 5B 模型 Easy 89.3、Hard 88.4。1.3B 受控替换中，RepViTok 相比 WAN2.2 VAE 将 Easy/Hard 平均成功率从 78.0/76.0 提高到 86.6/83.1。tokenizer 消融中，RepViTok 相对 reconstruction-only WAN2.2 VAE 的 gFVD 分别下降 9.5%/13.2%，但论文同时显示仅提高开放环 action 指标并不必然带来闭环成功。latent-action 两阶段训练在所测设置取得 gFVD 48.23/58.83、PSNR 22.86/19.93、OLS 19.87/16.98；PickFruit 成功率为 50%，对比无 latent action 的 30% 和 joint prediction 的 20%。三项真机任务各 10 次 rollout：RepWAM-5B 在摘取水果、推抽屉、插试管分别为 60%、80%、60%；样本量较小，应视为初步闭环证据。

### 总结讨论

RepWAM 将 WAM 的问题焦点从“是否生成未来视频”推进到“未来与动作共享什么 latent 接口”。最有价值的消融是：语义 tokenizer、两阶段 latent-action 预训练与机器人动作适配分别有可测贡献，而简单附加 joint-prediction head 反而损害动态质量。对知域的意义是它给出 `observation → semantic visual latent → latent transition → robot action` 的可实现分解；但共享语义空间和时序 causal mask 仍不等于可识别因果机制。

### 代码与数据

官方项目页与 GitHub 仓库可访问；论文和仓库表述为代码与权重将开放，当前具体 checkpoint、训练脚本、数据处理与许可证完整性需以仓库最新内容逐项核验。实验涉及 RoboTwin 2.0、AgiBot Eval、ImageNet、UCF101 以及自采 Franka 双臂示范。

### 局限、失败案例与开放问题

- 真机每任务仅 10 次 rollout，置信区间和随机种子稳定性没有充分呈现。
- RepWAM 从零训练，与继承 WAN 视频生成预训练的系统并非完全等成本比较。
- 5B 相比 1.3B 的提升与模型容量、训练资源耦合，尚不能只归因于 tokenizer。
- 视觉未来与 latent action 的联合预测仍可能编码外观相关捷径，并不保证动作语义可解释。
- 当前预训练主要是机器人域视频；作者把扩展到互联网、尤其第一视角人类视频列为未来工作。
- 闭环延迟、算力成本、失败恢复与安全边界仍缺少系统报告。
