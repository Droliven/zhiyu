

**报告标签**：Physical World Model, Physics-Aware Video Generation, World Simulator

# 物理世界模型与物理一致视频生成论文精读（2026-09-03）

本报告逐篇核验用户给出的 10 篇论文。证据等级：A＝正式会议论文、原文及官方资源均可核；B＝arXiv 正文与官方项目/代码可核；C＝仅预印本正文或开放信息不完整。实验数字均来自作者论文，不代表独立复现。未加入代表图：虽然论文 HTML 可显示插图，但本轮未对每个图像资源的稳定原图直链逐一完成响应类型验证，按仓库规范宁缺毋滥。

## 1. VOID: Video Object and Interaction Deletion

**作者：** Saman Motamed, William Harvey, Benjamin Klein, Luc Van Gool, Zhuoning Yuan, Ta-Ying Cheng  
**年份与发表：** 2026，arXiv preprint（v1，2026-04-02）；arXiv:2604.02296；正式 DOI 未见  
**可靠入口：** [arXiv](https://arxiv.org/abs/2604.02296)｜[项目](https://void-model.github.io/)｜[代码](https://github.com/Netflix/void-model)｜[AlphaXiv](https://alphaxiv.org/abs/2604.02296)  
**标签：** Counterfactual Video, Video Editing, Object Removal, Physical Interaction  
**证据等级：** B（arXiv 正文、项目与官方代码可核）。

**代表图：** VOID，Fig. 3，方法总览：从目标对象定位、移除到交互补全与背景修复。来源：[Fig. 3 原图](https://arxiv.org/html/2604.02296v1/void.jpg)

![VOID Fig. 3](https://arxiv.org/html/2604.02296v1/void.jpg)

### 当前挑战

传统 video object removal 能补背景、阴影和反射，却不会重写被删除对象造成的下游碰撞、支撑或人体操控。例如移除多米诺骨牌中段后，后续骨牌不应继续倒下；这要求生成新的动力学，而不是空间补洞。

### 研究动机

作者把对象删除改写为有成对监督的 counterfactual editing：保持其他初始条件不变，在模拟器中移除目标对象并重新运行。核心差异是同时删除对象及其 interaction effects。这里的“反事实”有明确的配对重模拟语义，但真实视频阶段没有事实反事实真值，依赖生成先验与 VLM 推断 affected regions。

### 技术方案

- **输入：** 原视频、用户点击得到的目标对象时序 mask
- **过程：** 用 Kubric/HUMOTO 构造有/无目标对象的配对视频；VLM 与分割模型扩展出 object/effect/overlap/unaffected 四区 quadmask；CogVideoX-Fun-5B 首轮生成替代轨迹，必要时以首轮 optical flow 构造 warped noise 做第二轮结构稳定
- **输出：** 删除目标对象及其下游物理交互后的 counterfactual video

### 实验结果

训练数据含约 1,900 对 Kubric 刚体视频和约 4,500 对 HUMOTO 人–物交互视频；测试含 75 个真实视频和 30 个合成视频。25 名参与者各评 5 个场景，共 125 次比较，VOID 获 64.8% 首选，Runway 为 18.4%，Generative Omnimatte 为 11.2%。三种 VLM judge 也把 VOID 总分列为最高。证据支持它优于所测 removal/editing baselines；真实数据没有 ground-truth counterfactual，不能将偏好分数解释成动力学准确率。

### 总结讨论

VOID 是列表中最明确使用 paired counterfactual supervision 的工作，也是与 HOI 因果编辑最直接的相邻论文。它能处理支撑消失、碰撞阻断和移除操作者，但反事实机制主要由模拟配对、VLM mask 和视频先验共同实现，没有显式恢复 SCM 或物理参数。

### 代码与数据

官方 Netflix 代码公开；仓库标明基于 CogVideoX-Fun、Generative Omnimatte、Kubric 和 HUMOTO。论文为 CC BY 4.0；代码仓库的具体许可证、训练对下载方式及第三方权重条款仍应在复现前逐项核对。

### 局限、失败案例与开放问题

- 真实视频无成对真值，VLM judge 与人类偏好可能奖励视觉合理而非真实因果结果。
- 首轮新运动会弯曲、拉伸或漂移，第二轮只是缓解而非消除。
- affected-region 推断错误会直接限制结果。
- 训练干预主要是“删除对象”，不覆盖连续力、属性或机制干预。

## 2. NewtonGen: Physics-Consistent and Controllable Text-to-Video Generation via Neural Newtonian Dynamics

**作者：** Yu Yuan, Xijun Wang, Tharindu Wickremasinghe, Zeeshan Nadir, Bole Ma, Stanley H. Chan  
**年份与发表：** 2026，ICLR 2026；arXiv:2509.21309；正式 DOI 未见  
**可靠入口：** [arXiv](https://arxiv.org/abs/2509.21309)｜[ICLR/OpenReview](https://openreview.net/pdf?id=zcAwK50ft0)｜[项目](https://yuyuanspace.com/NewtonGen/)｜[代码](https://github.com/pandayuanyu/NewtonGen)｜[AlphaXiv](https://alphaxiv.org/abs/2509.21309)  
**标签：** Text-to-Video, Neural ODE, Newtonian Dynamics, Motion Control  
**证据等级：** A（会议论文、项目与代码可核）。

**代表图：** NewtonGen，Fig. 2，整体框架：神经牛顿动力学、物理控制与视频生成的组合。来源：[Fig. 2 原图](https://arxiv.org/html/2509.21309v2/framework.png)

![NewtonGen Fig. 2](https://arxiv.org/html/2509.21309v2/framework.png)

### 当前挑战

文本到视频模型可能让物体向上坠落、速度或方向突变，也难按初速度、加速度等连续参数控制。仅从外观分布学习运动，缺少可外推的动力学状态。

### 研究动机

以少量 physics-clean trajectories 训练 Neural Newtonian Dynamics（NND），先预测用户条件下的未来状态，再把轨迹交给运动控制视频模型渲染。物理模型负责 motion law，生成模型负责 appearance。

### 技术方案

- **输入：** 场景文本、运动类型和用户指定的初始位置/速度/加速度等条件
- **过程：** 物理编码器提取 latent state；线性 physics-informed Neural ODE 建模已知动力学，三层 MLP 残差拟合非线性/未知项；从任意初态积分未来轨迹，再条件化 motion-controlled T2V
- **输出：** 满足指定运动参数的合成视频及 latent physical trajectory

### 实验结果

论文比较 Sora、Veo3、CogVideoX-5B、Wan2.2、PhyT2V 等。匀速 PIS-v 为 0.9830，参考轨迹为 0.9972；匀加速 PIS-ax 为 0.6568，仍低于参考 0.8489。用 PISABench 真实下落视频训练时，PIS-vx/PIS-ay 为 0.8485/0.6008，低于模拟训练的 0.9803/0.8189，显示真实噪声与 domain gap。表中部分闭源模型结果依赖其服务输出，公平性受生成接口和随机性影响。

### 总结讨论

NewtonGen 的贡献是可学习 ODE 动力学与 T2V 解耦，并提供数值条件控制；它不是通用物理引擎，也没有从任意文本自动识别完整对象、接触和约束图。适用于低维、可参数化运动的可控生成。

### 代码与数据

官方代码已公开，README 给出 CogVideoX-5B、Go-with-the-Flow LoRA 和已学习 ODE 权重依赖。许可证与 PISABench/预训练权重的组合条款需复现者自行核验。

### 局限、失败案例与开放问题

- 真实视频成绩明显低于模拟数据。
- 运动族及状态参数由设计者定义，不是开放世界机制发现。
- 视频 renderer 仍可能偏离正确 latent trajectory。
- 未覆盖复杂多体接触、形变、遮挡后的状态估计和闭环控制。

## 3. World Modeling with Probabilistic Structure Integration

**作者：** Klemen Kotar, Wanhee Lee, Rahul Venkatesh, Honglin Chen, Daniel Bear, Jared Watrous, Simon Kim, Khai Loong Aw, Lilian Naing Chen, Stefan Stojanov, Kevin Feigelis, Imran Thobani, Alex Durango, Khaled Jedoui, Atlas Kazemian, Dan Yamins  
**年份与发表：** 2025，arXiv preprint（v1，2025-09-10）；arXiv:2509.09737；正式 DOI 未见  
**可靠入口：** [arXiv](https://arxiv.org/abs/2509.09737)｜[AlphaXiv](https://alphaxiv.org/abs/2509.09737)  
**标签：** Probabilistic World Model, Structure Extraction, Random-Access Autoregression, Causal Prompting  
**证据等级：** C/B（全文可核；未见独立项目与完整代码入口）。

**代表图：** World Modeling with Probabilistic Structure Integration，Fig. 1，概率结构整合的世界模型循环。来源：[Fig. 1 原图](https://arxiv.org/html/2509.09737v1/concept_v2.png)

![World Modeling with Probabilistic Structure Integration Fig. 1](https://arxiv.org/html/2509.09737v1/concept_v2.png)

### 当前挑战

视觉模型通常只能沿固定方向预测，特定任务又需要单独监督的 depth、flow、segmentation 或 control encoder，难形成类似语言模型的通用查询接口。

### 研究动机

PSI 提出“概率预测→结构提取→结构回灌”的循环：先学任意变量集合之间的条件分布，再通过模型内条件推断抽取低维结构，最后将这些结构作为新 token 类型加入训练。

### 技术方案

- **输入：** 互联网视频切分的时空 tokens，以及后续抽取的 flow、depth、segmentation 等结构 tokens
- **过程：** random-access autoregressive sequence model 学习广泛条件分布；通过条件/干预式 prompting 抽取中间结构；将结构作为条件和预测目标重新混入训练数据
- **输出：** 任意条件视频预测、零样本视觉结构、相机/对象控制与改进后的 world model

### 实验结果

作者训练实例使用 1.4 万亿互联网视频 tokens，报告 optical flow、自监督 depth 和 object segmentation 的强结果，并完成一轮结构回灌后的预测改进。在 WildRGB-D novel-view synthesis 和 3DEditBench object manipulation 上，论文称优于所选专用/编辑基线。由于缺少公开训练语料、代码和可复现算力配置，本报告将这些视为作者自报告，而非独立确认。

### 总结讨论

PSI 的“causal inference”主要指从完整条件分布做结构查询与提示；它提供灵活 control handles，但不自动满足环境 SCM 的可识别性。对世界模型研究的影响在于：新增单一 depth/flow/segmentation head 很难构成 novelty，必须证明结构回灌或任务机制上的额外价值。

### 代码与数据

论文公开，arXiv 标注相应许可；未核验到完整训练代码、1.4T-token 数据清单或权重，因此端到端复现性有限。

### 局限、失败案例与开放问题

- 训练规模巨大且数据构成不透明。
- 条件分布丰富不等于因果方向或干预效应可识别。
- 抽取结构可能继承预测模型的偏差。
- 未给出机器人闭环、真实力学参数恢复或安全干预验证。

## 4. PhysGen: Rigid-Body Physics-Grounded Image-to-Video Generation

**作者：** Shaowei Liu, Zhongzheng Ren, Saurabh Gupta, Shenlong Wang  
**年份与发表：** 2024，ECCV 2024；arXiv:2409.18964；正式 DOI 待核  
**可靠入口：** [arXiv](https://arxiv.org/abs/2409.18964)｜[项目](https://stevenlsw.github.io/physgen/)｜[代码](https://github.com/stevenlsw/physgen)｜[AlphaXiv](https://alphaxiv.org/abs/2409.18964)  
**标签：** Image-to-Video, Rigid-Body Simulation, Force Control, Physics-Grounded Rendering  
**证据等级：** A（ECCV 论文、项目与代码可核）。

**代表图：** PhysGen，Fig. 2，刚体物理引导的图像到视频生成流程。来源：[Fig. 2 原图](https://arxiv.org/html/2409.18964v1/method_v1.png)

![PhysGen Fig. 2](https://arxiv.org/html/2409.18964v1/method_v1.png)

### 当前挑战

纯数据驱动 I2V 难保证碰撞、摩擦、弹性和力响应；传统 simulator 又缺少从单张开放世界图像恢复场景并生成逼真视频的能力。

### 研究动机

PhysGen 采用“感知→显式模拟→生成渲染”：把物理正确性放在 image-space rigid-body simulation 中，用 diffusion refinement 补外观，而不是要求扩散模型自行发现牛顿动力学。

### 技术方案

- **输入：** 单张图像，以及施加到对象的力、力矩、初速度等条件
- **过程：** 基础视觉模型/GPT-4V 辅助分解可移动对象并估计几何、材质和物理参数；模拟刚体、碰撞、摩擦与弹性；将运动指导送入视频 diffusion renderer 并细化
- **输出：** 可按输入物理条件控制的短视频及中间物理轨迹

### 实验结果

10 张复杂开放世界图像、118 个可移动实例的感知评测在 IoU 0.5 下 precision 0.93、recall 0.82；论文还做视频基线比较和用户研究。单次生成约 3 分钟：感知约 1 分钟、120-step simulation 5 秒、render 1 分钟、generative refinement 35 秒。结果支持刚体场景的可控性，不覆盖通用材质与长期真实预测。

### 总结讨论

PhysGen 是此列表的显式 simulator 基线。它能执行真正的力/初态干预，但结果取决于从单图估计的几何和参数；视频生成器的视觉合理性不能反向证明估计参数正确。

### 代码与数据

官方 PyTorch 代码和 Colab 可用；仓库包含 perception、simulation、rendering 与 evaluation 流程。第三方模型、GPT 服务与数据许可证需分别核验。

### 局限、失败案例与开放问题

- 聚焦刚体，形变、液体、断裂和复杂关节不在核心模型内。
- 单图存在尺度、遮挡、质量和摩擦不可辨识性。
- 约 3 分钟/视频，不适合实时闭环。
- 生成 refinement 可能掩盖 simulator error。

## 5. RealWonder: Real-Time Physical Action-Conditioned Video Generation

**作者：** Wei Liu, Ziyu Chen, Zizhang Li, Yue Wang, Hong-Xing Yu, Jiajun Wu  
**年份与发表：** 2026，arXiv preprint（2026-03-05）；arXiv:2603.05449；正式 DOI 未见  
**可靠入口：** [arXiv](https://arxiv.org/abs/2603.05449)｜[项目、代码与权重](https://liuwei283.github.io/RealWonder/)｜[AlphaXiv](https://alphaxiv.org/abs/2603.05449)  
**标签：** Action-Conditioned Video, Real-Time Simulation, 3D Reconstruction, Distillation  
**证据等级：** B（预印本、项目、代码/权重入口可核）。

**代表图：** RealWonder，Fig. 2，实时物理动作条件视频生成框架。来源：[Fig. 2 原图](https://arxiv.org/html/2603.05449v1/approach_eccv.png)

![RealWonder Fig. 2](https://arxiv.org/html/2603.05449v1/approach_eccv.png)

### 当前挑战

连续 3D force、robot action 和 camera control 与视频模型的像素/latent 接口不匹配；显式 simulator 有结构但渲染不逼真，扩散生成又太慢。

### 研究动机

用 physics simulation 作为 action 与 video generator 的桥：模拟器把动作转成 optical flow 与 coarse RGB，再由四步蒸馏模型实时渲染。

### 技术方案

- **输入：** 单张图像、文本，以及力/力矩、机器人抓手轨迹或相机运动序列
- **过程：** 单图重建可模拟 3D 几何与材质；物理引擎处理刚体、形变体、流体和颗粒；渲染 flow/coarse RGB；四步 causal distilled generator 流式生成
- **输出：** 480×832 的 action-conditioned video stream

### 实验结果

作者报告单 GPU 13.2 FPS、0.73 秒 latency；PhysGaussian、CogVideoX、Tora、RealWonder 的 PhysReal 分别为 0.468/0.624/0.578/0.705，RealWonder 的 consistency 为 0.265。运行速度对照中 Tora 0.107 FPS、CogVideoX-I2V 0.225、PhysGaussian 0.207。论文同时展示不同动作导致不同结果；这些指标仍以视觉/自动评测为主，不能等同于物理参数误差。

### 总结讨论

RealWonder 显著推进 PhysGen 的实时性和材料覆盖，并明确接受物理动作。论文也展示 generator 会给未模拟水动力的船补出波纹：这提高观感，却说明输出含生成先验“脑补”，不能直接当作 simulator ground truth。

### 代码与数据

项目页提供代码与 checkpoints 入口。完整训练数据、第三方模型与仿真资产的许可证及硬件配置需按仓库说明复核。

### 局限、失败案例与开放问题

- 单图 3D/材质估计错误会系统性污染模拟。
- renderer 可能添加 simulator 中不存在的动力学。
- “causal”在架构中主要指时间生成与动作传递，不是因果识别。
- 13.2 FPS 不代表端到端机器人感知、规划和执行延迟。

## 6. PhiZero: A World Model Built Around Physical Language

**作者：** Shuyao Shang, Yuqi Wang, Ruopeng Gao, Xu Chen, Tieniu Tan, Lue Fan, Zhaoxiang Zhang  
**年份与发表：** 2026，arXiv preprint（2026-07-30）；arXiv:2607.28624；正式 DOI 未见  
**可靠入口：** [arXiv](https://arxiv.org/abs/2607.28624)｜[项目](https://phi-zero.github.io/)｜[代码](https://github.com/yaoyao-jpg/PhiZero)｜[模型](https://huggingface.co/ShuyaoShang/PhiZero)｜[AlphaXiv](https://alphaxiv.org/abs/2607.28624)  
**标签：** Physical Language, Discrete Transition Tokens, Reason-then-Render, World Model  
**证据等级：** B（全文、项目、代码与模型页可核）。

**代表图：** PhiZero，Fig. 2，以物理语言为中间表示的训练与推理管线。来源：[Fig. 2 原图](https://arxiv.org/html/2607.28624v1/Pipeline.png)

![PhiZero Fig. 2](https://arxiv.org/html/2607.28624v1/Pipeline.png)

### 当前挑战

像素空间未来预测把动力学埋在高维生成器中，自然语言又太粗，难表达细粒度状态变化并复用于生成、理解和跨 embodiment transfer。

### 研究动机

学习紧凑的离散“physical language”表示相邻 latent states 的 transition，先自回归推演物理 token，再由 diffusion decoder 渲染，即 reason-then-render。

### 技术方案

- **输入：** 第一帧、文本 action intent 与训练期无标注/模拟视频
- **过程：** transition-level Q-Former 从相邻 Wan VAE states 提取 32 queries，FSQ 离散为 25K 词表中的 physical tokens；Qwen3-VL-4B 初始化 reasoner 预测 token sequence；Wan2.2-5B decoder 渲染
- **输出：** 物理语言序列、未来视频、likelihood-based 物理判断和可复用 motion transfer code

### 实验结果

数据由 50K 小时池筛至 10K 小时，并形成 5M 个四秒 clips 与 1M motion-rich clips。33 帧视频只用 256 tokens，对比 Wan VAE 44,800，重建 PSNR/SSIM/LPIPS 为 28.9/0.903/0.087。项目页报告 Physics-IQ、PhyGround、WorldModelBench 的所列物理指标领先；论文也在 IntPhys2、LikePhys、YoCausal 做 pairwise likelihood 判断。强压缩相对 VAE 会损失重建质量，物理 benchmark 的 judge/coverage 仍限制结论。

### 总结讨论

PhiZero 的 novelty 是 transition-level discrete interface，而不是可读自然语言或显式方程。它能复用运动 token 做外观/embodiment transfer，但 token 语义未必对应可识别物理变量，不能把“reason”直接解释为符号因果推理。

### 代码与数据

代码与 Apache-2.0 模型页已上线，模型页给出 reasoner/tokenizer 权重结构；但页面同时提示仓库需要获权认证，Wan2.2 基座不随权重提供。完整训练数据清单仍未开放，实际下载权限需人工确认。

### 局限、失败案例与开放问题

- 离散 token 可压缩但未保证可解释或可组合。
- 训练数据规模大且含模拟/筛选管线，完整复现成本高。
- 文本 action intent 不等于机器人低层动作。
- motion transfer 的外观变化不验证新对象真实质量、摩擦或接触机制。

## 7. Code as Worlds: Agentic Discovery of Executable World Representations for Physical Reasoning

**作者：** Hanyang Wang, Yimo Cai, Weiliang Chen, Jiawei Chi, Haowen Sun, Qiyu Dai, Yi-Hsin Hung, Xingzhuo Guo, Jinshan Ren, Runmao Yao, Ziwei Liu, Mingsheng Long, Yueqi Duan, Jun Gao, Jiangran Lyu, Fangfu Liu, Jialong Wu  
**年份与发表：** 2026，arXiv preprint（v1，2026-08-27）；arXiv:2608.27549；正式 DOI 未见  
**可靠入口：** [arXiv](https://arxiv.org/abs/2608.27549)｜[项目](https://mirros-lab.github.io/code-as-world/)｜[AlphaXiv](https://alphaxiv.org/abs/2608.27549)  
**标签：** Executable World Representation, Agentic Discovery, Physical Reasoning, Code Generation  
**证据等级：** B/C（全文和项目可核；代码/数据开放完整度待核）。

**代表图：** Code as Worlds，Fig. 2，代理发现、执行并修正可执行世界表示的闭环。来源：[Fig. 2 原图](https://arxiv.org/html/2608.27549v1/pipeline-wjl.png)

![Code as Worlds Fig. 2](https://arxiv.org/html/2608.27549v1/pipeline-wjl.png)

### 当前挑战

VLM 能描述物理事件，却常缺少对象状态、数值参数和 governing dynamics，无法执行、检验或针对变量做干预。

### 研究动机

把世界表示成可执行代码，显式组织 scene composition、dynamics 和 appearance；通过 propose→execute→render→verify→refine 的 abductive loop，从文本或视频反推出可运行 hypothesis。

### 技术方案

- **输入：** 自然语言描述或真实视频，以及可调用的代码执行/物理渲染环境
- **过程：** agent 提议包含对象、参数、规则和相机的 world code，执行并渲染，与观测核对后迭代修正；验证后的世界再生成定量物理监督训练 VLM
- **输出：** 可检查和编辑的 executable world、模拟轨迹/视频，以及 Code-as-World-VL 推理模型

### 实验结果

QuantiPhy 上 4B/9B/27B 模型平均 MRA 为 50.6/55.4/58.6，论文报告 27B 超过所测 proprietary baselines。sim-to-real renderer 将 JEDi MMD 从 simulator render 的 3.000 降到 1.484，同时 trajectory ADE 基本保持 1.682→1.677，Accuracy@2%D 为 78.81%→77.49%。结果支持可执行监督与数值推理，但不能说明所有真实视频都能唯一恢复正确物理程序。

### 总结讨论

这是列表中最显式的结构化/可干预世界表示。其 agentic search 属于模型选择与系统识别，但多解性、验证器偏差和程序先验会造成“能解释观测但机制错误”的等价解。

### 代码与数据

论文为 CC BY 许可，项目页提供 technical report、演示和 Code 入口；具体仓库、训练数据、执行沙箱与模型权重的完整发布状态需人工复核。

### 局限、失败案例与开放问题

- 程序搜索与反复渲染计算昂贵。
- 单段观测通常不足以辨识质量、摩擦和隐藏力。
- 可执行代码有安全风险，复现需隔离 sandbox。
- QuantiPhy 成绩主要验证 quantitative reasoning，不等于机器人闭环成功。

## 8. PhysisForcing: Physics Reinforced World Simulator for Robotic Manipulation

**作者：** Peiwen Zhang, Yufan Deng, Shangkun Sun, Juncheng Ma, Duomin Wang, Jonas Du, Zilin Pan, Ye Huang, Hao Liang, Songyan Huang, Ruihua Zhang, Enze Xie, Ming-Yu Liu, Daquan Zhou  
**年份与发表：** 2026，arXiv preprint（2026-06-26）；arXiv:2606.28128；正式 DOI 未见  
**可靠入口：** [arXiv](https://arxiv.org/abs/2606.28128)｜[项目](https://dagroup-pku.github.io/PhysisForcing.github.io/)｜[代码](https://github.com/DAGroup-PKU/PhysisForcing)｜[AlphaXiv](https://alphaxiv.org/abs/2606.28128)  
**标签：** Robotic Manipulation, Trajectory Alignment, Relational Alignment, World Simulator  
**证据等级：** B（预印本、项目和推理代码/权重可核）。

**代表图：** PhysisForcing，Fig. 2，面向机器人操作的物理强化世界模拟器架构。来源：[Fig. 2 原图](https://arxiv.org/html/2606.28128v1/figs/Fig2_Method.png)

![PhysisForcing Fig. 2](https://arxiv.org/html/2606.28128v1/figs/Fig2_Method.png)

### 当前挑战

通用或机器人微调的视频模型仍会让运动物体变形，并在接触附近产生不连续轨迹、错误时空关系和不可信 robot–object response。

### 研究动机

不增加推理成本，在训练时把监督集中到 physics-informative regions：像素级轨迹约束局部运动，语义级关系约束 interacting entities 的时空关系。

### 技术方案

- **输入：** 机器人操作视频、参考 point trajectories、物理关键区域和冻结视频理解编码器的 region relations
- **过程：** 在 DiT 中间特征同时优化 pixel-level trajectory alignment loss 与 semantic relational alignment loss；适配 Wan2.2 和 Cosmos3 backbones
- **输出：** 物理一致性更强的机器人视频 world model 及可供 inverse dynamics/policy 使用的 rollout

### 实验结果

作者报告 Wan2.2-I2V-A14B 和 Cosmos3-Nano 在 R-Bench 相对 base 提升 22.3%/9.2%，相对 vanilla finetuning 提升 7.1%/3.7%。WorldArena action-planner closed-loop success 从 16.0% 提至 24.0%，强 baseline WoW 为 20.5%。RoboTwin 下游六任务平均 success 68.2→72.8，但 shake_bottle 97.5→94.5、stack_bowls_two 69.5→63.0，说明不是所有任务改善。消融中 Wan5B ft 44.8，完整方法 47.5。

### 总结讨论

论文的价值在于把像素轨迹与对象关系监督连接到真实 manipulation planning；“physics reinforced”仍是 representation alignment，不是显式力学状态或因果识别。负增益任务应保留，避免只报告平均提升。

### 代码与数据

MIT 仓库公开 PF-Cosmos/PF-Wan 推理代码与权重；README 在核验时仍写 training code 和 auxiliary checkpoints coming soon，完整训练复现尚不充分。

### 局限、失败案例与开放问题

- 两项下游任务出现性能下降。
- 轨迹/关系 teacher 的错误会传入 DiT。
- 依赖 benchmark evaluator，接触力和对象状态未显式测量。
- 训练代码尚未完整开放，数据与 GPU 成本需补核。

## 9. ProPhy: Progressive Physical Alignment for Dynamic World Simulation

**作者：** Zijun Wang, Panwen Hu, Jing Wang, Terry Jingchen Zhang, Yuhao Cheng, Long Chen, Yiqiang Yan, Zutao Jiang, Hanhui Li, Xiaodan Liang  
**年份与发表：** 2026，CVPR 2026 Oral；arXiv:2512.05564；正式 DOI 待核  
**可靠入口：** [CVF 正式论文](https://openaccess.thecvf.com/content/CVPR2026/papers/Wang_ProPhy_Progressive_Physical_Alignment_for_Dynamic_World_Simulation_CVPR_2026_paper.pdf)｜[arXiv](https://arxiv.org/abs/2512.05564)｜[项目](https://zijunwa.github.io/prophy/)｜[代码](https://github.com/zijunwa/ProPhy)｜[AlphaXiv](https://alphaxiv.org/abs/2512.05564)  
**标签：** Physics-Aware T2V, Mixture-of-Experts, VLM Distillation, Physical Alignment  
**证据等级：** A（CVF 正式论文、项目和代码可核）。

**代表图：** ProPhy，Fig. 2，渐进式物理对齐的动态世界模拟框架。来源：[Fig. 2 原图](https://arxiv.org/html/2512.05564v2/framework.png)

![ProPhy Fig. 2](https://arxiv.org/html/2512.05564v2/framework.png)

### 当前挑战

现有 T2V 对整段视频施加粗粒度物理条件，对局部物理事件响应近似各向同性，难处理碰撞、尘土、液体等不同区域和时刻的物理线索。

### 研究动机

以两阶段 Mixture-of-Physics-Experts 先路由语义物理类别，再在 token level 选择 refinement experts；从 VLM 蒸馏物理属性，使不同专家专门化于不同现象。

### 技术方案

- **输入：** 文本 prompt、视频，以及 Qwen2.5-VL-32B 生成的 token-level physical annotations
- **过程：** Semantic Expert Block 学高层物理类别；Refinement Expert Block 做细粒度 token routing；relative/absolute alignment 与 load-balancing loss 将 VLM 判断迁移到 CogVideoX/Wan
- **输出：** physics-aware text-to-video 结果及可操控的 expert activations

### 实验结果

训练从 WISA-80K 随机取 20K 视频，以 600 prompts 评 VideoPhy2/VBench。CogVideoX 加 ProPhy 后 VideoPhy2 Joint 指标报告提升 19.7%；Wan2.1-1.3B 的 PC/SA/Joint 从 57.8/30.0/24.8 提至 65.0/32.0/26.5。消融显示完整 PB+SEB+REB 最好。手工给对象路由错误 expert 会产生刚性车门像布料般变形，支持 experts 与物理属性相关；这仍不是因果变量可识别性的证明。

### 总结讨论

ProPhy 占据“progressive semantic-to-token physical alignment”位置。它提升文本视频的局部物理表现，但任务不是 action-conditioned rollout，也没有显式 simulator state。

### 代码与数据

MIT 代码公开，包含 annotation 与 inference；官方 checkpoints 在 README 核验时仍标注 soon，训练依赖 WISA 数据和 Qwen2.5-VL-32B。

### 局限、失败案例与开放问题

- VLM 物理知识可能含系统偏差和 hallucination。
- benchmark 依赖 VLM/语义判分，缺少数值轨迹真值。
- 20K 视频覆盖有限，复杂组合物理未充分验证。
- expert specialization 相关性不能直接解释为物理定律发现。

## 10. PhysRVG: Physics-Aware Unified Reinforcement Learning for Video Generative Models

**作者：** Qiyuan Zhang, Biao Gong, Shuai Tan, Zheng Zhang, Yujun Shen, Xing Zhu, Yuyuan Li, Kelu Yao, Chunhua Shen, Changqing Zou  
**年份与发表：** 2026，ECCV 2026；arXiv:2601.11087；正式 DOI 待核  
**可靠入口：** [arXiv](https://arxiv.org/abs/2601.11087)｜[项目](https://lucaria-academy.github.io/PhysRVG/)｜[代码](https://github.com/ant-research/PhysRVG)｜[模型](https://huggingface.co/HappyP4nda/PhysRVG)｜[AlphaXiv](https://alphaxiv.org/abs/2601.11087)  
**标签：** Video Reinforcement Learning, Rigid-Body Motion, Verifiable Reward, Collision  
**证据等级：** B/A（arXiv、代码和权重可核；ECCV 接收由官方仓库公告，正式 proceedings/DOI 待核）。

**代表图：** PhysRVG，Fig. 2，统一物理奖励强化学习的核心设计。来源：[Fig. 2 原图](https://arxiv.org/html/2601.11087v1/motiv.png)

![PhysRVG Fig. 2](https://arxiv.org/html/2601.11087v1/motiv.png)

### 当前挑战

像素重建式 finetuning 会把正确物理约束当作众多条件之一；直接对高维视频做 RL 又因奖励稀疏、batch 小和早期低质采样而不稳定，碰撞尤其容易被错误轨迹蒙混。

### 研究动机

设计基于对象 mask/轨迹与 collision detection 的可验证 reward，并以 Mimicry–Discovery Cycle 在稳定模仿与物理探索之间切换，避免纯 RL 崩溃。

### 技术方案

- **输入：** 初始图像/视频、物理运动条件、对象 masks 与刚体轨迹/碰撞监督
- **过程：** Stage 1 将 Wan2.2-5B TI2V 全参适配为 V2V；Stage 2 用 PEFT 的 MDcycle，Mimicry branch 稳定训练，Discovery branch 以 physics reward 探索；混合 SDE/ODE 采样
- **输出：** 碰撞、自由落体、摆动和滚动等物理一致视频

### 实验结果

PhysRVGBench 上论文报告 PhysRVG IoU 0.64、trajectory offset 15.03；表中 Magi-1 为 0.27/113.42。VBench/VideoPhy2 多项视觉与物理指标同时报告。消融显示纯 RL 前 50 steps 不稳，MDcycle 收敛更平滑；16K FT+250 MD steps 达 0.64/15.03，继续到 30K FT 几乎不增益。训练使用 4×8 张 H20；作者指出即使 effective batch 640，全参数 RL 仍会崩溃。

### 总结讨论

PhysRVG 的关键贡献是可验证刚体 reward 与稳定 video RL，而非通用世界模型。碰撞 reward 能减少消失和错误轨迹，但 reward 只编码覆盖到的运动族，可能出现 metric gaming 或对新机制失效。

### 代码与数据

训练/推理代码和 Hugging Face 权重已公开；模型页包含 DiT/LoRA 与 SAM2 依赖。Stage 1 使用开源与 proprietary video collections，完整数据可复现性仍受限制。

### 局限、失败案例与开放问题

- 训练成本高：32 张 H20，且高维 RL 仍不稳定。
- 主要覆盖四类刚体运动，非刚体/流体/多接触未证明。
- reward 依赖分割与轨迹估计，可被感知错误或捷径利用。
- 物理指标改善不自动转化为机器人策略或反事实规划能力。
