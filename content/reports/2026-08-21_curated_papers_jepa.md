# FACT、PSG-JEPA、Gaussian-JEPA 与 Masked Visual Actions：失败条件世界模型与 JEPA 表征整理

**报告标签**：World Action Model, JEPA, 预测表征, 机器人学习  
**检索与核对日期：2026-08-21**  
**阅读范围：** 四篇均核对其 arXiv HTML 全文（含方法、实验、附录要点）、项目页；FACT 与 Masked Visual Actions 另核官方 GitHub / Hugging Face；PSG-JEPA 与 Gaussian-JEPA 另核官方 GitHub。均为 2026 年 arXiv 预印本，尚未见正式会议/期刊版本或 DOI。不是仅依据标题或摘要。

> **贯穿四篇的核心问题：预测模型究竟缺少哪一个接口，才会“能预测，却未必能服务于行动”？** 四篇给出的答案分别落在数据、表征、观察和动作四层：FACT 缺的是“失败动作—真实后果”的监督接口；PSG-JEPA 缺的是视觉 latent 与机器人本体状态/变化之间的 grounding；Gaussian-JEPA 缺的是跨 3D Gaussian 随机重采样仍稳定的学习目标；Masked Visual Actions 缺的是视频模型能够直接理解、且可跨本体迁移的动作表达。
>
> **阅读地图：** 先读 FACT，看负样本如何只教“后果”而不教坏动作；再读 PSG-JEPA，看训练期特权状态如何让预测 latent 暴露控制相关变量；随后以 Gaussian-JEPA 作为边界清楚的 3D 表征对照，理解“预测潜空间而非重建一次观察”的价值；最后读 Masked Visual Actions，把问题拉回视频 WAM 的动作入口。由此可以形成一条研究链：**缺失的接口/监督是什么 → 方法怎样补上 → 实验真正验证到哪一步 → 哪个设计原则可以迁移。**
>
> 需要统一把握证据边界：FACT 的 “causal” 指 action-then-imagine 的条件顺序，Masked Visual Actions 的 “counterfactual” 指同一初值下的动作条件 rollout；二者都不是结构因果识别。PSG-JEPA 的 identifiability 是探针可恢复性，不是因果可识别。Gaussian-JEPA 不做控制，与本课题为间接相关。

---

## 1. FACT: Failure-Aware Causal Training for World-Action Models

**作者：** Quanquan Peng, Yutong Liang, Rui Yan, Nicklas Hansen, Xiaolong Wang  
**年份与发表：** 2026，arXiv preprint（v1，cs.RO，2026-08-10）。Peng 与 Liang 为共同一作；单位 UC San Diego。尚无 DOI / 正式出版页。arXiv 论文许可为 CC BY-NC-ND 4.0；代码仓库声明 Apache-2.0。  
**可靠入口：** [arXiv](https://arxiv.org/abs/2608.10232)｜[HTML 全文](https://arxiv.org/html/2608.10232)｜[项目页](https://fact-wam.github.io/)｜[代码](https://github.com/Bariona/FACT)｜[模型](https://huggingface.co/Bariona/fact-wam)｜[演示](https://huggingface.co/spaces/Bariona/fact-world-action-model)｜[AlphaXiv](https://alphaxiv.org/abs/2608.10232)  
**代表图：** FACT，Fig. 2，共享因果扩散 Transformer：动作、value 与未来视频同骨干，value/未来视频只看干净动作槽 \(G\)。来源：[Fig. 2 原图 PNG](https://arxiv.org/html/2608.10232v1/x2.png)

![FACT Fig. 2: action-then-imagine causal diffusion transformer](https://arxiv.org/html/2608.10232v1/x2.png)

### 当前挑战

WAM 希望用未来预测为动作生成注入物理先验，但成功演示主导的训练分布留下了一个关键接口空白：模型看过“怎样成功”，却没有系统学过“坏动作会导致什么”。这不是简单增加视频头能够解决的，因为失败 rollout 有双重身份——它是宝贵的后果监督，却是危险的动作模仿目标。

现有路线会把这个矛盾放大。DreamZero 等 video-first WAM 必须先完成视频去噪，再由 IDM 解码动作；BagelVLA、Fast-WAM、Gigaworld-Policy 等把预测帧或 latent 作为动作条件，但未来目标仍偏向专家成功轨迹。于是测试时即使动作已经偏离，模型仍可能配出“任务会成功”的未来；只在专家流形上训练的 value 头也会对坏动作过度乐观。FACT 因而要补的不是更多成功数据，而是一条严格分流的监督接口：**失败轨迹可以教后果和进度，不能教策略复现失败动作。**

这里的 “causal” 具体指 **action-then-imagine 的时间顺序与 teacher-forced 动作条件**；实验没有涉及 SCM、\(do(\cdot)\) 或反事实识别。

### 研究动机

FACT 的核心判断是：**动作必须先于想象；世界分支必须回答“这个动作会怎样”，而不是替动作提供一个成功偏向的未来。** 因此 token 顺序被写成 prefix \(P\) → 噪声动作 \(A\) → 干净 GT 动作 \(G\) → value \(V\) → 未来视频 \(I\)。动作分支看不到 \(G\)，而 value 与视频只条件在干净动作上。

这套顺序使监督可以自然分流：成功演示优化 \(\mathcal{L}_a+\mathcal{L}_v+\mathcal{L}_I\)；失败窗口则 mask 掉 \(\mathcal{L}_a\)，只让观察到的失败未来和被压低的进度进入世界分支。推理时 Stage 1 可只生成动作，不必等待视频；需要更高可靠性时，Stage 2 再用 value 对 \(N\) 个候选排序。

其可迁移启示不是“失败数据越多越好”，而是：**负轨迹应按语义进入正确损失。** 对策略而言它是不可模仿样本，对世界模型而言却是覆盖决策边界所必需的监督。本文与 WAM 课题直接相关，可和 FlowWAM、LingBot-VA、Causal World Modeling for Robot Control 对照，但它建模的是动作条件后果，不是结构因果。

### 技术方案

- **输入：** 语言指令 \(\ell\)；多视角 RGB（主视 + 左右腕）与本体感觉 \(s_t\) 打包成 prefix；训练时还有动作块 \(a_{t:t+H}\)（\(H=48\)）、未来视频窗口（当前帧加四个偏移 \([0,H/4,H/2,3H/4,H]\)）以及归一化进度目标。
- **过程：** 从 WAN2.2-5B / Wan2.2-TI2V-5B 初始化共享视频 DiT；每个 block 的 FFN 后接轻量 action adapter。三模态共用 flow-matching 去噪损失，\(w_a=20\)，\(w_v=w_I=1\)。进度目标在成功轨迹上为 \(p_{t+H}=t/T\)（均匀进度奖励）；失败轨迹再减去 \(\lambda_{\mathrm{fail}}=1\) 的失败指示并 clip 到 \([0,1]\)。失败数据来自先在成功数据上训练的策略 rollout，并标注失败 onset。推理默认 20 步 flow-Euler；动作-only 路径缓存 prefix KV。可选 \(N\) 候选并行 Stage 1，再 Stage 2 取 \(\arg\max_k V_\theta(o_t,\ell,a^{(k)})\)。
- **输出：** 默认可执行动作块；需要时再输出动作条件进度值与未来视频。主策略评估走动作-only，不在测试时生成视频。

与最近 baseline 的实质差异：相对 Motus / video-first WAM，FACT 先出动作、部署可跳过视频；相对把未来当动作条件的 WAM，未来与 value 条件在干净动作而非噪声动作上；相对直接把失败当 BC 数据，失败只进世界分支。作者强调共享骨干让未来/value 损失能回到动作通路，而不是 MoT 里隔离的 world expert。

### 实验结果

实验围绕四个递进问题展开：世界分支是否帮助策略、失败监督是否额外有效、它是否真的修正了坏动作下的未来、修正后的 value 能否用于候选排序。作者主张失败感知的动作条件后果学习提高策略成功、降低成功偏向幻觉，并使 value 头可选地用于排序；以下数字限定了这一主张实际成立的范围（均来自原文表格/正文）：

- **RoboTwin 2.0（50 任务；Clean 每任务 50 条、Randomized 每任务 500 条合训；每任务 100 trial；另加约 1.3K rollout 失败）：** 无视频共训 81.8% 平均成功 → 视频共训 85.6%（Clean 86.3 / Rand. 84.9）→ 再加失败 87.5%（88.4 / 86.6）。Motus 87.8%，Gigaworld-Policy 86.0%，\(\pi_{0.5}\) 79.8%。附录按任务表上 Hanging Mug 即便加失败仍只有 36/49；Turn Switch 加失败后 Clean 从 66 降到 61。这些数字与同日入库的 FlowWAM / G0.5 **不是同一套训练脚本**，不宜直接排成 SOTA 竞赛。
- **延迟（RTX PRO 6000）：** 动作-only FACT w/ failure **380 ms**，Motus 1220 ms（作者称约 \(3\times\) 更快），\(\pi_{0.5}\) 47 ms。速度优势相对 video-first WAM，不是相对纯 VLA。
- **真机（双 YAM 臂，主视 D435 + 两腕 D405；seen 五任务，cube 类 200 条专家演示、其余 50 条，cube 任务约 30 条失败；每格 20 trial）：** seen 平均 Cosmos 25、\(\pi_0\) 48、Motus 64、FACT 82、FACT+failure 89、再加 \(N=4\) scoring 92；\(\pi_{0.5}\) 88。unseen（改颜色/形状/指令）FACT 67 → +failure 77 → +scoring 82；\(\pi_{0.5}\) 85。作者写明 \(\pi_{0.5}\) 有大规模机器人预训练而 FACT 没有。所有表内 baseline 都在同一批成功演示上 fine-tune。
- **消融（真机 seen）：** 去掉因果 mask（无失败、且去掉干净 \(G\) 槽）77%；失败动作仍算模仿损失 **63%**；去掉视频共训 58%；**只用 scoring、不训失败** 79%（低于无 scoring 的 82%）。这支持“value 头必须先见过失败后果才有用”，不是“多采样总能涨点”。
- **幻觉诊断（512 个 held-out 窗口，成功/失败各半，20 步去噪）：** 失败窗口 PSNR 19.51→25.92，SSIM 0.7461→0.8290；成功窗口几乎不变（PSNR 26.12 vs 26.08）。Fig. 5 定性显示同一坏动作下，成功-only 模型仍想象抓住，失败共训预测真实失败。
- **失败比例：** 三个 RoboTwin clean 任务上 \(p\in\{0,50,100\}\%\) 失败混合，平均成功 32.7%→57.3%；\(p=100\%\) 时失败约占训练集 45%。这是子集探针，不是 50 任务主表。
- **\(N\) sweep：** 长时程抓取上 \(N=1\to 4\) 完成度明显上升，更大 \(N\) 的增益相对延迟变小；真机 optional scoring 取 \(N=4\)。

合在一起看，策略增益、失败动作模仿消融与 PSNR/SSIM 诊断形成了相互支撑的证据链；但它不支持结构因果或 \(do(\cdot)\) 识别，也不支持失败数据对所有任务单调有益（Turn Switch 是反例）、FACT 在无机器人预训练时击败 \(\pi_{0.5}\) 的真机 unseen，或 value 头等同于独立 critic。

### 总结讨论

FACT 最重要的贡献，是把负轨迹在 WAM 中应接入的位置说清楚：未来预测条件在**已执行动作**上，失败负责监督后果，而不负责提供 BC 目标。RoboTwin 上接近 Motus且部署更快、真机 seen 上失败共训与 scoring 的增益、以及失败模仿导致 63% 的反向消融，共同支持这一设计；PSNR/SSIM 则进一步说明增益确实伴随成功偏向幻觉减轻。

可迁移到其他研究的原则是“按任务语义拆监督”，而不是盲目混合正负数据。它的适用边界仍是短中程操作式 WAM，不是形式因果，也不是互联网级无动作预训练。引用时应保留两个尺度差异：380 ms 相对 Motus 的 1220 ms 有优势，但仍远慢于 \(\pi_{0.5}\) 的 47 ms；teacher-forced 动作条件也不能写成因果识别。

### 代码与数据

- **代码：** [Bariona/FACT](https://github.com/Bariona/FACT) 含 RoboTwin 数据准备、训练、推理与闭环评估；Apache-2.0。
- **权重：** Hugging Face `Bariona/fact-wam` 为 RoboTwin checkpoint（从 Wan2.2-TI2V-5B fine-tune），含 `norm_stats_delta.json`；另有 Spaces 演示。
- **数据：** 仓库脚本下载 `Bariona/robotwin-v2`；真机失败 rollout 与完整专家语料未作为可复现公开包核验。WAN 骨干与 T5 指令嵌入是外部依赖。
- **许可冲突需分开写：** 代码 Apache-2.0，arXiv 论文页为 CC BY-NC-ND 4.0。

### 局限、失败案例与开放问题

- Hanging Mug、Turn Switch 等任务上失败共训增益很小或为负；失败数据不是万灵药。
- 进度目标用均匀 \(t/T\)，失败再减常数，不是学习到的稠密成功检测器。
- Best-of-\(N\) 用额外 Stage 2 换可靠性；主文策略数字多数仍是单样本。
- 真机每格 20 trial；unseen 仍低于有大规模预训练的 \(\pi_{0.5}\)。
- “causal”是动作→未来的时间箭头与注意力掩码，没有因果图、干预识别或反事实 benchmark。
- 作者自己把在线 rollout、DAgger 式修正、以及用更好进度估计器替换 value 头列为未来工作。

---

## 2. Is Forward Prediction Enough? Physical State Grounding for JEPA World Models

**作者：** Haodong Yan, Jiaguan Zhu, Mingyuan Jia, Ruiqing Yin, Junjie He, Zhide Zhong, Junfeng Li, Jinxuan Lu, Hengtao Li, Tianran Zhang, Jiayi Chen, Wenxuan Song, Wen Chen, Yuxiang Gao, Haoang Li  
**年份与发表：** 2026，arXiv preprint（v1，cs.RO，2026-08-07）。单位 HKUST(GZ) 与 COCO Matrix。正文声明存在 equal contribution / project leader / corresponding author，项目页未逐一标注归属，具体分工待核验。尚无 DOI / 正式出版页。  
**可靠入口：** [arXiv](https://arxiv.org/abs/2608.06799)｜[HTML 全文](https://arxiv.org/html/2608.06799)｜[项目页](https://haodong-yan.github.io/psg-jepa-project-page/)｜[代码](https://github.com/Haodong-Yan/PSG-JEPA)｜[AlphaXiv](https://alphaxiv.org/abs/2608.06799)  
**代表图：** PSG-JEPA，Fig. 1，前向预测 JEPA 的本体可识别性缺口，以及训练期-only 的 state / transition grounding。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2608.06799v1/teaser.png)

![PSG-JEPA Fig. 1: physical state grounding beyond forward prediction](https://arxiv.org/html/2608.06799v1/teaser.png)

### 当前挑战

预测 latent 不等于控制可用 latent。LeWM 已用 SIGReg 防止 collapse，但在 OGBench-Cube 上冻结其表征后，单 latent 的线性/MLP 探针几乎读不出末端 yaw（\(r\le 0.08\)），成对探针也只能部分恢复关节/夹爪速度；DINOv2 预训练仅把 yaw 推到约 0.50。这说明本文面对的不是“表征是否坍塌”，而是更具体的接口缺口：**前向预测目标没有保证视觉 latent 显式承载机器人本体状态及其变化。**

形式上，\(\hat{z}_{t+1}=F(z_t,a_t)\) 可预测，并不推出 \(z_t\) 能读出本体感觉，也不推出 \((z_t,z_{t+k})\) 能读出净关节变化；缺失的对齐只能由下游 planner / policy 用有限任务监督再学习。常见的 IDM 正则 \((z_t,z_{t+1})\mapsto a_t\) 也没有完全补上接口：动作序列会随 horizon 变长，同一端点变化还可能对应多种动作，因而不是稳定的物理转移目标。作者称这一现象为 robot-centric identifiability gap，指的是**探针可恢复性**，不是因果识别意义上的 identifiability。

### 研究动机

PSG-JEPA 用训练期特权监督补上这条连接：一个头要求单个 latent 恢复本体感觉，另一个头要求多 horizon 端点对恢复净关节角变化；训练完成后两个头都被丢弃，LeWM 的 encoder–predictor、SIGReg 和推理成本保持不变。

关键选择是用 \(\Delta q_{t,k}=q_{t+k}-q_t\) 代替动作序列。净变化由端点唯一确定、维度不随 horizon 增长，更适合约束“这两个表征之间发生了什么”。编码器输入仍然只有图像，本体量只作为 grounding 目标或探针标签，因此方法补的是训练监督，而非部署传感器接口。

可迁移启示是：**自监督目标决定的不只是表征是否有信息，还决定信息是否以低成本可读的形式出现。** 对潜空间世界模型而言，少量训练期特权状态可以主动塑造这种可读性；但这里的 identifiability 仍不能外推为因果可识别。

### 技术方案

- **输入：** 图像观测窗口 \(T=C+1=4\)（\(C=3\) 帧上下文）、对应动作；训练期另有对齐的本体感觉 \(s_t\)（关节角、夹爪、末端位姿）及其关节分量 \(q_t\)。编码器和预测器 **从不把本体当作输入**。
- **过程：** 共享编码器 \(z_{t+i}=E_\phi(o_{t+i})\)；因果动作条件预测器 teacher-forced 一步预测，\(\mathcal{L}_{\mathrm{fwd}}\) 为 MSE；保留 LeWM 的 SIGReg，\(\lambda_{\mathrm{reg}}=0.09\)。状态头 \(H_s(z)\to s\)；转移头 \(H_\Delta(z_{t+i},z_{t+i+k})\to\Delta q\)，对 \(k\in\{1,2,3\}\) 各 horizon 等权，避免短程对占优。总损失 \(\mathcal{L}_{\mathrm{PSG}}=\mathcal{L}_{\mathrm{JEPA}}+\lambda_g(\mathcal{L}_{\mathrm{static}}+\mathcal{L}_{\mathrm{dynamic}})\)，\(\lambda_g=0.1\)，全 benchmark 固定。训练后丢掉 \(H_s,H_\Delta\)。
- **输出：** 推理期与 LeWM 相同：图像 → 规划用 latent，以及可选的动作条件未来 latent。Grounding 头不参与部署。

与最近 baseline 的实质差异：相对 DINO-WM / V-JEPA 2-AC，编码器可被前向损失和 grounding 共同塑造；相对 LeWM，只多训练期目标；相对自构的 LeWMActionIDM，监督的是净关节变化而非动作。官方代码在 OGBench-Cube 上提供训练与 GC-IDM 规划；LIBERO-Goal 有独立目录与 checkpoint；OGBench-Scene 仓库标注 coming soon。

### 实验结果

实验按“能否读出 → 能否预测 → 能否规划与控制”逐层验证。作者主张物理 grounding 提高 latent 可读性、冻结表征上的目标条件规划以及仿真/真机策略，同时不增加推理模块；实际证据如下：

- **探针（OGBench-Cube，episode-level train/test，线性 ridge / 浅 MLP，Pearson \(r\)）：** 单 latent 上 EE-yaw：LeWM 0.08/0.08，DINOv2 0.51/0.50，LeWMActionIDM 0.11/0.10，PSG-JEPA **0.94/0.98**；JointPos 从 LeWM 的 0.71/0.69 到 0.83/0.81。成对探针 GripVel：LeWM 0.44/0.47 → PSG-JEPA 0.69/0.76；Action 与 LeWMActionIDM 持平（0.80/0.86 vs 0.80/0.84）。这支持“状态从单 latent 读、变化从配对读”，不是因果边恢复。
- **冻结 latent + 同一 GC-IDM（三层 MLP，512 hidden，AdaLN-Zero；200 个 goal；3 planner seeds）：** OGBench-Cube 全数据、5 epoch：PSG-JEPA **95.0±0.7** vs LeWM 80.7±1.9；100 epoch 仍 98.7 vs 89.7。25% 数据、100 epoch：93.2 vs 83.5。OGBench-Scene 全数据 5 epoch：83.5 vs 76.2。作者另称 Cube 上 5% 数据、100 epoch 规划成功 84.5%，LeWM 大约需要五倍数据才追上（Fig. 3；主表未列该格）。Planner 训练预算与表征质量耦合，不是同一 world-model rollout planner。
- **开环 latent 预测（512 段，无 teacher forcing）：** Cube 上 5 步 MSE 0.0093→0.0046，30 步 0.1488→0.0485（约 −67%）；Scene 30 步 0.1608→0.0982（约 −39%）。Grounding 没有牺牲递归预测。
- **LIBERO-Goal 策略（10 任务，OFT 头宽 1024、四层、两帧输入、8 步 action chunk，30 epoch，3 seeds×每任务 50 rollout）：** PSG-JEPA **85.3±3.9** vs LeWM 77.7±0.5、LeWMActionIDM 82.6±2.2、DINOv2 80.1±5.3。编码器与头联合微调，不是冻结表征。
- **真机（AgileX 双臂 Mobile ALOHA 设计，前视+两腕 RGB；每任务 100 条遥操作，50 trial）：** Place-to-Bread 84 vs 62，Place-to-Plate 74 vs 58，Pour-Water 80 vs 60，平均 **79.3 vs 60.0**。只对照 LeWM，没有 DINOv2 / IDM 真机表。
- **消融：** 去掉 transition 时规划 SR@5ep 95.0→81.3；去掉 state 时状态探针均值 0.94→0.69；只留相邻或只留端点 horizon 时 LIBERO 约 81.2–81.5，完整模型 85.3。各分量都有贡献；规划对 transition 更敏感，探针对象对 state 更敏感。

这些结果把探针提升与下游收益联系起来，但证据尚未覆盖物体状态或接触力学，也没有说明 grounding 能用于缺少本体日志的互联网视频，更不能把这里的 “identifiability” 等同于因果可识别。

### 总结讨论

PSG-JEPA 将“JEPA 世界模型是否足够”变成了一个可检验问题：本体状态与状态变化能否从规划 latent 中低成本读出？yaw 探针最高 \(r=0.98\)、低预算 GC-IDM、递归 latent 预测以及 LIBERO/真机策略给出了方向一致的答案，说明训练期 grounding 不只是让探针数字更好，也改善了后续使用表征的样本效率。

更广泛的研究启示是：设计世界模型目标时，应把“下游需要读出什么”前置，而不是期待前向预测自动保留所有控制变量。边界同样明确：监督只覆盖有本体日志的操作数据，物体、接触和视觉干扰没有进入 grounding 目标；GC-IDM 成功不等于模型预测控制已获得闭环物理一致性，\(r=0.98\) 也不等于完整世界状态已被识别。

### 代码与数据

- **代码：** [Haodong-Yan/PSG-JEPA](https://github.com/Haodong-Yan/PSG-JEPA) 覆盖 OGBench-Cube 训练、GC-IDM 规划评估、LIBERO-Goal 策略；GitHub 未声明 SPDX 许可证（本次 API 返回 `license: None`）。OGBench-Scene 标注尚未放出。
- **数据 / 权重：** 训练用 LeWM 发布的 `cube_single_expert` 像素 `.h5`（Hugging Face `quentinll/lewm` collection），不是 OGBench 官方 state 文件；作者警告跨 GPU 重渲染会与论文数字不一致。LIBERO 目录含已发布 checkpoint 与评估日志（本次未逐文件核验完整性）。
- **依赖：** `stable-worldmodel`、LeWM 模块与 Nguyen et al. 的 GC-IDM 评估代码。

### 局限、失败案例与开放问题

- Grounding 目标是机器人本体，不是物体位姿、接触或场景图；探针缺口针对 EE-yaw 等本体量。
- 真机只对比 LeWM，50 trial / 任务，没有 IDM / DINOv2 真机对照。
- LIBERO 是联合微调编码器，不能把 85.3% 全部归因于冻结表征。
- 仓库与论文范围不完全对齐：Scene 代码未发布；许可证未核到 SPDX。
- 无本体日志的人类视频/跨本体设定未验证。
- 作者未提供形式 identifiability 证明；证据是探针可恢复性与下游成功。

---

## 3. Gaussian-JEPA: Joint-Embedding Predictive Learning for 3D Gaussian Splats

**作者：** Bin Ren, Qi Ma, Yue Li, Zongyan Han, Yidi Li, Yuqian Fu, Rao Muhammad Anwer, Theo Gevers, Fahad Shahbaz Khan, Salman Khan  
**年份与发表：** 2026，arXiv preprint（v1，cs.CV，2026-08-16）。单位 MBZUAI、ETH Zürich、University of Amsterdam、太原理工、KAUST。尚无 DOI / 正式出版页。  
**可靠入口：** [arXiv](https://arxiv.org/abs/2608.15651)｜[HTML 全文](https://arxiv.org/html/2608.15651)｜[项目页](https://amazingren.github.io/Gaussian-JEPA)｜[代码](https://github.com/Amazingren/Gaussian-JEPA)｜[AlphaXiv](https://alphaxiv.org/abs/2608.15651)  
**代表图：** Gaussian-JEPA，Fig. 2，1K Gaussian → 64 token，共享 context 预测多尺度目标块。来源：[Fig. 2 原图 PNG](https://arxiv.org/html/2608.15651v1/framework.png)

![Gaussian-JEPA Fig. 2: multi-scale latent prediction on Gaussian tokens](https://arxiv.org/html/2608.15651v1/framework.png)

### 当前挑战

3DGS 资产可能包含数万 Gaussian，而实用编码器通常只能接收固定数量的 primitive，例如 1K。于是同一物体经两次独立重采样，会产生不同的输入集合；这不是刻意设计的语义增强，而是密集资产与固定预算编码器之间不可避免的观察噪声。缺失的接口因此是：**怎样让表征指向同一底层物体，而不是绑定于某一次采样实现。**

Gaussian-MAE 在输入空间重建被 mask 组的 centroid 与属性，监督仍锚定当次抽到的 primitive；对比学习则依赖预先选择的视角/增强，不直接要求模型推断缺失空间内容。3D Gaussian token 又同时耦合几何、各向异性支撑、可见度与外观，缺失区域尺度不一，使“重建什么”尤其难定义。Gaussian-JEPA 处理的是这一静态 3D 表征问题，不是机器人控制或视频世界模型。

### 研究动机

方法把监督对象从“这次采样的 14 维属性”改成“完整物体中被遮挡多尺度块的潜在表征”。Online encoder 只看 context；共享 EMA encoder 看完整 token 场，再按块索引提供目标。两个名为 geo/app 的互补投影与 VISReg 式 feature-space grounding 提供额外约束，但它们是对全部属性特征学出的视图，不是手工拆开的几何/外观通道。

这一改动补上的，是随机观察实现与底层对象表征之间的接口。对本知识库而言它是间接相关的 3DGS 表征工作：不输出动作、不做 rollout、不评机器人；真正可迁移的思路是**预测跨观察稳定的潜变量，而不是复刻一次观测**，并用重采样一致性、部分观察和冻结迁移来检验这一目标是否兑现。

### 技术方案

- **输入：** 物体级 3DGS 资产 \(\mathcal{X}=[C,O,S,R,\mathrm{SH}]\in\mathbb{R}^{N\times 14}\)；每次迭代先缓冲再无放回抽 \(p=1024\) 个 primitive。Centroid FPS 出 \(n=64\) 组、每组 KNN \(k=32\)，PointNet 式 tokenizer 得 \(D=384\) token。
- **过程：** 默认目标日程 \(\mathbf{s}=[11,9,7,5]\)（32 个 target token + 32 个 context）。Online encoder 编码 context 一次；每个目标块由共享 EMA encoder 处理全场后索引。Predictor 用目标中心位置查询、不看目标 token 内容。\(\mathcal{L}_{\mathrm{pred}}\) 为两路 SmoothL1；\(\mathcal{L}_{\mathrm{ground}}\) 为两路 VISReg 加跨协方差惩罚；\(\lambda=0.1\)。无输入空间解码器，损失不含 centroid/opacity/scale/rotation/SH。
- **输出：** 预训练后的 Gaussian token 特征，供冻结检索、补全解码器、部件分割与分类微调。不是视频或控制指令。

与最近 baseline 的实质差异：相对 Gaussian-MAE，监督在 stop-gradient 潜空间而非原始属性；相对 Point-JEPA / 3D-JEPA，token 含 14 维 Gaussian 属性且目标块尺度异构。分类/分割里的点云数字来自文献原协议，作者已用 † 标明，不是同输入重跑。

### 实验结果

实验最值得关注的不是常规分类榜单，而是三个与问题定义直接对应的检验：独立重采样后是否稳定、只见部分物体时是否还能检索、冻结编码器后能否支持完整资产补全。作者同时报告语义迁移；实际结果如下：

- **数据划分：** ShapeNet55-GS 预训练 51,934 / 测试 520（Gaussian-MAE 资产）；ModelNet10 3,991/908、ModelNet40 9,842/2,467，**ModelNet 物体不进预训练**；ShapeNet-Part 用官方划分。Objaverse 只用于补充 PCA 图，不进训练或主表。
- **重采样一致性（ModelNet40-GS 全部 2,467 测试物体，五次独立 1K 采样，1 gallery + 4 query = 9,868）：** 相对 drift 0.3400→**0.2594**（相对降 23.7%），96.2% 物体上 drift 更低；R@1 92.95 vs 93.00（几乎持平），R@5 98.89→99.36。
- **部分观察检索（缺组 0–85%）：** 55% 缺失时 R@1/R@5/R@10 = 39.82/65.28/75.95 vs MAE 的 19.80/39.02/49.14（+20.02 / +26.26 / +26.81）。30% 缺失时 R@1 仍高 10.56 点。
- **ShapeNet55-GS 补全（半空间 crop 的 512 Gaussian → 预测独立 1K 完整采样；冻结 encoder + 相同解码器，三颗 decoder seed）：** CD 0.0732→0.0678（−7.4%），F1% 6.62→7.42；seed-0、50% 可见度渲染 PSNR 16.03→17.24、SSIM 0.7148→0.7469。
- **ShapeNet-Part：** class/instance mIoU 84.5 / 86.1，相对 Gaussian-MAE +0.3 / +0.1。点云 Point-JEPA 文献数字为 83.9 / 85.8，协议不同。
- **ModelNet 分类（相对 Gaussian-MAE）：** Full FT MN10/40 94.94/92.63（+0.78 / +0.09）；线性探针 93.72/90.47（+0.22 / +1.50）；MLP-3 探针 MN40 +2.55 至 90.27。冻结骨干上的 MN40 差距大于全微调。
- **消融：** 单目标空间 93.06 LP / 90.85 R@1；双空间+特征 grounding 93.50 / 93.23；双空间若改回属性重建，R@1 掉到 88.18。\(M=6\) 最高 LP（93.83）但 R@1 降到 91.89；选 \(M=4\) 是折中。过大尺度差 \(\delta=2\) 两指标都降。Centroid+covariance 的 R@1（94.14）高于全属性（93.23），全属性 LP 更高——外观有助于语义、不一律提高重采样稳定。

结果支持它相对匹配的 Gaussian-MAE 学到了更稳定的物体级表征，尤其是在部分观察与冻结设定中；但没有覆盖场景级或动态 3DGS、机器人迁移，也不能据此声称严格公平地超过点云 SOTA（输入与协议不同），MN40 全微调的 +0.09 本身也不足以证明实际优势。

### 总结讨论

Gaussian-JEPA 的价值不在于把 JEPA 名称移植到 3DGS，而在于重新定义学习目标：不再重建一次随机采样，而是预测被遮挡区域的稳定表征。相较 MN40 全微调 +0.09，重采样 drift 相对下降 23.7%、高缺失率检索和冻结补全更直接验证了这一点。

可迁移的研究启示是：当输入只是底层对象的随机实现时，评测也应主动改变观察实现，检验表征是否抓住不变量。其边界是物体级静态 Gaussian 资产；它不是 WAM，也不是场景理解基础模型，geo/app 的命名更不代表几何与外观已经被严格解耦。

### 代码与数据

- **代码：** [Amazingren/Gaussian-JEPA](https://github.com/Amazingren/Gaussian-JEPA) 含预训练、分类、部件分割、补全与文档；许可证 **CC BY-SA 4.0**（不是 Apache）。
- **数据：** 依赖 Gaussian-MAE 发布的 ShapeNet/ModelNet Gaussian 资产；完整复现需这些外部资产与作者预处理（centroid 单位球、opacity/scale/SH 规范化等）。
- **权重：** README 指向下游结果文档；本次未逐一核验预训练 checkpoint 是否已全部上传。

### 局限、失败案例与开放问题

- 仅物体级资产；作者自己把场景扩展留作后续。
- 编码器固定 1K primitive，无法直接吃完整密集资产。
- 分类全微调在 MN40 上与 MAE 几乎持平，主增益在冻结/部分观察设定。
- geo/app 是学习视图，消融说明外观通道甚至可能损害重采样 R@1。
- 与点云方法的表不是同输入协议。
- 无控制、无时间、无动作；不能当作 JEPA world model 引用。

---

## 4. Masked Visual Actions for Unified World Modeling

**作者：** Hadi Alzayer, Wenlong Huang, Haonan Chen, Christopher Luey, Lvmin Zhang, Maneesh Agrawala, Gordon Wetzstein, Li Fei-Fei, Yilun Du, Jiajun Wu, Jia-Bin Huang  
**年份与发表：** 2026，arXiv preprint（v1，cs.CV，2026-07-21）。单位 Stanford、University of Maryland College Park、Harvard。尚无 DOI / 正式出版页。  
**可靠入口：** [arXiv](https://arxiv.org/abs/2607.19343)｜[HTML 全文](https://arxiv.org/html/2607.19343)｜[项目页](https://masked-visual-actions.github.io/)｜[代码](https://github.com/HadiZayer/masked-visual-actions)｜[权重](https://huggingface.co/HadiZayer/masked-visual-actions)｜[AlphaXiv](https://alphaxiv.org/abs/2607.19343)  
**代表图：** Masked Visual Actions，Fig. 1，同一 checkpoint：遮罩机器人轨迹做正向动力学，遮罩物体运动做逆向合成。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2607.19343v1/teaser.png)

![Masked Visual Actions Fig. 1: forward and inverse queries via masked trajectories](https://arxiv.org/html/2607.19343v1/teaser.png)

### 当前挑战

大规模视频模型已经学习运动、接触和形变先验，却仍缺少一个关键入口：**怎样把动作交给模型，同时不破坏它在像素空间学到的先验。** 文本太欠定，tracks、力和关键点过于稀疏，关节角或末端位姿又依赖具体本体，并与视频预训练空间错位。Ctrl-World 等方法因此可能在训练域内紧跟动作，遇到未见本体却退化为静止或损坏的视频。

把低维动作“画出来”也不自动解决问题。同一骨干上的 skeleton 或 end-effector 可视化在 DROID 域内与 masked actions 接近，但换成自定义夹爪时会把机器人幻觉回训练集外观，在 BEHAVIOR 双臂场景中还会扭曲本体。UVA / UWM / X-WAM 等统一模型虽然在模态通道上做 masking，动作仍是低维向量，正向与逆向切换也难跨本体迁移；BridgeV2W、Action Images、Mask2IV 等像素条件则大多只描述机器人主动运动和正向预测。

所以缺的不是更大骨干，而是一个与预训练视觉空间对齐、能统一主动与被动实体运动的动作接口。

### 研究动机

核心做法是把动作表示成视频中任意实体的部分可见时空轨迹：露出机器人的运动，模型补全物体和场景响应，得到正向动力学；露出物体的期望运动，同一模型补全机器人行为，得到逆向动作合成。主动与被动不再对应两套架构，而是对同一交互先验提出不同 masked-video 查询。

因为条件和输出都在像素空间，masked video 可以直接拼接注入 Wan-Fun-Control，无需另开低维动作通道。训练只使用主动机器人实体的 mask，逆向查询来自零样本泛化。这个接口与 FlowWAM 的光流视频动作、FACT 的数值动作块构成直接对照：它试图用更稠密的视觉条件换取跨本体迁移与正逆统一。可迁移启示是，动作表征应尽量复用基座模型已经擅长的模态；但作者明确承认模型学到的是交互相关，而非因果关系。

注意：库中已有 **Mask World Model: Predicting What Matters for Robust Robot Policy Learning**，是另一篇工作（预测语义 mask 当输出），标题相近但不是本文。

### 技术方案

- **输入：** 参考帧 \(I_0\)、masked 条件视频 \(M\odot V\)（未露出区域填均匀灰）、文本 prompt。正向时 \(M\) 为机器人轨迹；逆向时为物体/期望运动。
- **过程：** 骨干 Wan-Fun-Control 2.2 14B（双 expert MoE，高低噪 DiT 在 timestep 0.358 分界）。条件经同一 VAE 编码后与视频 latent 拼接。LoRA rank 256，batch 4，8×H200，约 10,000 step / 4 天。数据约 **15 小时**，混合 DROID 与 RoboCasa 的成功和失败轨迹。两条互补构造：(1) SAM 类分割“A robotic arm”，无需标定，但测试难提供精确 mask，且遮挡可能泄漏原视频动态；(2) 按机器人状态渲染 URDF（DROID 标定 refinement 跟随 PointWorld；RoboCasa 只渲染半透明机器人、夹爪标红）。推理期任意动作可渲染成 control video。
- **输出：** 完整 RGB 视频。正向：场景对机器人运动的响应；逆向：与给定物体运动一致的机器人运动，再经单独训练的 IDM 变成可执行关节/末端指令。规划时对 Diffusion Policy 的 \(N\) 条候选在想象中 rollout，用 Gemini 3.1 Pro 按任务成功、交互保真、物理真实排序。

与最近 baseline 的实质差异：相对 Ctrl-World，条件是像素轨迹而非原始动作向量；相对 Wan-Move，条件是实体 mask 而非 GT tracks；相对 skeleton/EE 可视化，条件稠密且与像素对齐。GitHub 明确：**没有改视频模型或训练器**，只是 DiffSynth-Studio 上的 LoRA 薄层；URDF 渲染工具标注 coming soon。

### 实验结果

实验依次检查这个视觉动作接口是否可控、是否跨本体、是否能给策略提供有用排序，以及能否反向生成动作。作者主张约 15 小时 masked 微调后，单一 checkpoint 具备这些能力；实际证据如下：

- **可控生成（LPIPS↓ / SSIM↑ / PSNR↑）：** DROID 上 Masked Visual Actions 0.0945 / 0.887 / 23.74，Ctrl-World 0.362 / 0.708 / 18.15，Wan-Move（GT tracks）0.534 / 0.562 / 12.99，纯 I2V 0.521 / 0.548 / 12.42。BEHAVIOR（训练未见的 R1-Pro 双臂）0.123 / 0.843 / 22.90 vs Ctrl-World 0.196 / 0.837 / 18.39。**重要公平性注释：** 作者脚注写明 Ctrl-World 在全部 DROID 上训练，因此见过文中 held-out 场景；本方法没有。BEHAVIOR 上 Ctrl-World 的 SSIM 已接近，差距主要在 LPIPS/PSNR 与定性是否塌缩。
- **条件消融：** DROID 域内 EE vis / skeleton / masked 接近（PSNR 22.64 / 22.74 / 23.74）。自定义夹爪真机：0.183 / 0.169 / **0.148** LPIPS。BEHAVIOR：0.171 / 0.162 / **0.123**。稀疏条件会幻觉出训练集机器人或扭曲双臂。
- **规划（RoboCasa，每任务 10 场景，Diffusion Policy 候选，\(N=10\)，Gemini 3.1 Pro 评判）：** Fig. 8 显示多样任务成功率相对直接执行上升，且随评估样本数增加。这是 test-time scaling / Best-of-N，评判器是闭源 VLM，不是学习到的 value 头。作者把“同一初值下想象不同动作”称作 counterfactuals，**实验是相关排序，不是因果识别**。
- **策略评估：** 开环 Diffusion Policy，每场景 10 条；视频模型内成功率与 GT 环境相关系数 **\(r=0.982\)**。作者同时写明视频模型对任务进度有正偏差（想象成功率系统性更高）。真机四任务各 20 条演示，按 rubric 的进度分布接近真机，同样有正偏差。
- **逆向动作提取（RoboCasa CoffeeServeMug；视频模型未见该任务；IDM 与 DP/ACT/SmolVLA 都用 100 条演示；20 trial）：** 作者报告本方法 **90%**，高于所列模仿学习 baseline（具体 baseline 数字在 Fig. 11，HTML 未转成可复制表；此处不编造）。正向-only 训练即可零样本转逆向。

结果说明 masked trajectory 是比稀疏可视化和原始动作向量更可迁移的条件接口，但尚不能推出模型学到了接触因果、闭源 VLM judge 无偏、15 小时数据足以无标定扩展到任意新本体，或视频模型成功率能够替代真机评测——后者已有系统性正偏差。

### 总结讨论

Masked Visual Actions 将“视频世界模型如何接收动作”具体化为像素空间中的遮罩轨迹，并用同一 checkpoint 完成正向模拟与逆向合成。DROID/BEHAVIOR 保真度、自定义夹爪与双臂上的稀疏条件失败，以及策略评估相关 \(r=0.982\)，共同支持“稠密、像素对齐的条件更容易跨本体迁移”。与此同时，成功率正偏差和闭源 VLM 排序器提醒我们：生成保真并不自动等于可靠规划。

对后续研究最有价值的问题是：动作接口能否写成基座模型原生理解的模态，同时保留执行精度。本文给出了实体 mask 这一端点，FlowWAM 的光流视频是另一端点；二者都值得与 FACT 的数值动作块比较。适用边界是能够渲染或分割实体轨迹的操作视频，且延迟受 14B 骨干限制。想象 rollout 不能写成反事实识别，Ctrl-World 的 DROID 结果也不是同等训练数据下的严格失败对照。

### 代码与数据

- **代码：** [HadiZayer/masked-visual-actions](https://github.com/HadiZayer/masked-visual-actions) 为 DiffSynth-Studio 上的推理脚本与 LoRA 训练配方；Apache-2.0。URDF control video 渲染工具尚未发布。
- **权重：** Hugging Face `HadiZayer/masked-visual-actions`（high/low noise 两套 LoRA）。基座是 ModelScope `PAI/Wan2.2-Fun-A14B-Control`。
- **数据：** DROID + RoboCasa；论文称将释放数据，GitHub 目前需要用户自备 CSV（`prompt, reference_image, video, control_video`）。完整 15 小时 masked 语料是否已全部上传待核验。
- **评测依赖：** 规划用 Gemini 3.1 Pro，闭源且不可完全复现。

### 局限、失败案例与开放问题

- 作者原文：模型学的是物体交互的 **相关** 而非因果，因果仍是开放问题。
- 能力与时延受基座 14B 视频模型限制；没有改骨干表达能力。
- 分割路径可能从遮挡泄漏原视频动态；渲染路径需要相机标定，且默认只渲染机器人。
- 视频内评测对成功有正偏差；不能当作无偏仿真器。
- 规划排序依赖闭源 VLM；自定义夹爪/未见双臂上稀疏条件失败，说明泛化来自 mask 接口而非任意可视化。
- 逆向仍需要单独 IDM 才能落地关节指令；视频本身不是可执行策略。
