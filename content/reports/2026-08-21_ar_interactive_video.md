# 自回归交互视频：从 DMD 到 Causal Forcing++、LongLive-2.0 与 minWM

**报告标签**：视频生成, 自回归扩散, 交互世界模型  
**检索与核对日期：2026-08-21；补充核对：2026-08-24**
**阅读范围：** 十篇均核对其 arXiv HTML 全文（含方法、实验、讨论/局限要点）、项目页和官方 GitHub（若公开）。DMD 另核 CVPR 2024 Open Access 页，CausVid 另核 CVPR 2025 Open Access 页，Self Forcing 另核 NeurIPS 2025 Spotlight 页。不是仅依据标题或摘要。

> 这是一条从单步图像蒸馏走向实时交互长视频的技术链：**DMD** 用 target score 与 fake score 之差近似分布级 KL 梯度；**DMD2** 去掉昂贵的 ODE 回归集，并以 two-time-scale 更新、GAN 项和推理态多步模拟稳定/增强蒸馏。**CausVid** 随后把不对称 DMD 用于因果 4-step 视频学生；**Self Forcing** 指出 DMD 必须在自 rollout 分布上匹配；**Causal Forcing / Causal Forcing++** 依次修正 ODE 初始化对象与轨迹成本；**LongLive** 解决分钟级流式与 prompt 切换，**LongLive-2.0** 再把长视频训练、少步 LoRA、NVFP4 与并行推理做成一套基础设施；**minWM** 把蒸馏配方接到相机可控世界模型。**MAGI-1** 是非 DMD 的原生 chunk-wise AR 对照。DMD/DMD2 只做图像，但它们定义了后续视频方法反复复用的损失与稳定化部件；其余工作的“causal”也指注意力/时序因果，不是结构因果或 \(do(\cdot)\)。

---

## 1. One-step Diffusion with Distribution Matching Distillation

**作者：** Tianwei Yin, Michaël Gharbi, Richard Zhang, Eli Shechtman, Frédo Durand, William T. Freeman, Taesung Park
**年份与发表：** 2024，CVPR 2024。MIT / Adobe Research。预印本 arXiv:2311.18828（v4，cs.CV）；arXiv DOI：10.48550/arXiv.2311.18828。
**可靠入口：** [arXiv](https://arxiv.org/abs/2311.18828)｜[HTML 全文](https://arxiv.org/html/2311.18828)｜[CVPR Open Access](https://openaccess.thecvf.com/content/CVPR2024/html/Yin_One-step_Diffusion_with_Distribution_Matching_Distillation_CVPR_2024_paper.html)｜[项目页](https://tianweiy.github.io/dmd/)｜[AlphaXiv](https://alphaxiv.org/abs/2311.18828)
**代表图：** DMD，Fig. 2，分布匹配梯度与 ODE 回归正则的整体训练框架。来源：[Fig. 2 原图 PNG](https://arxiv.org/html/2311.18828v4/overview.png)

![DMD Fig. 2: distribution matching plus regression regularization](https://arxiv.org/html/2311.18828v4/overview.png)

### 当前挑战

扩散模型质量高但通常要几十至上百次网络前向；直接把确定性 teacher 轨迹回归成一次映射，又会迫使学生复现特定 noise–image 对，在一对多的图像分布上容易平均化或损失细节。本文针对的缺口是：**能否不逐样本模仿 teacher 轨迹，而让一步生成器的整体输出分布逼近预训练扩散模型。**

- 直接最小化生成分布与 teacher 分布的 KL 不可行，因为一步生成器没有显式密度。
- 仅靠 score distillation 的近似梯度会有 mode collapse / 不稳定；仅靠回归又限制学生只能跟随预计算 ODE 路径。
- 论文只验证图像生成，不验证视频时序、AR rollout 或 KV cache；其价值是后续 CausVid / Self Forcing 的损失基础。

### 研究动机

核心 Insight：**在加噪空间中，KL 对生成图像的梯度可以写成 target diffusion score 与 fake diffusion score 的差。** target score 由冻结的 teacher 给出；fake score 由一个在线训练的扩散模型估计学生当前输出分布。梯度再通过一步生成器回传。作者同时保留小权重 LPIPS 回归正则，用 teacher 的确定性采样 noise–image 对固定大尺度结构并抑制 mode collapse。

与本报告 **基础相关而非视频直接相关**：CausVid 的 asymmetric DMD、Self Forcing 的 rollout distribution matching，以及后续 CF 系列的 real/fake score 都沿用这一“两个 score 之差”框架；但 DMD 原文没有证明该目标在自回归视频上稳定。

### 技术方案

- **输入：** 随机噪声；类标签（ImageNet）或文本 prompt（Stable Diffusion v1.5）。
- **过程：** 从 teacher 初始化一步生成器 \(G_\theta\)；对生成图像随机加噪，冻结的 real diffusion model 估计 \(s_{\text{real}}\)，在线 fake diffusion model 在学生样本上学习 \(s_{\text{fake}}\)，二者之差形成近似反向 KL 梯度。训练中偶尔读取预计算的确定性 ODE noise–image 对，对 \(G_\theta(z)\) 与 teacher 输出施加 LPIPS 回归。作者对梯度作归一化，以控制不同噪声级别的尺度。
- **输出：** 一次网络前向的类条件或文本条件图像；SD-v1.5 版本以 FP16 在论文硬件口径下约 20 FPS。

相对 progressive distillation / consistency model，DMD 的主监督不是逐点复制 teacher 轨迹，而是输出分布匹配；但初版仍依赖预计算回归集，这正是 DMD2 要去掉的部分。

### 实验结果

**作者主张：** 一步学生在大幅减少前向次数的同时，质量接近原扩散模型，并优于当时已发表的 few-step 方法。

实验实际支持：

- **ImageNet 64×64：** 一步 DMD 的 FID **2.62**；论文同时在 CIFAR-10 / ImageNet 的无条件或类条件设置与扩散蒸馏、GAN 基线比较。
- **zero-shot COCO-30k：** SD-v1.5 一步 DMD 的 FID **11.49**；生成一次约 90 ms，而论文所用 Stable Diffusion 基线约 2590 ms。20 FPS 是批量/FP16 吞吐口径，不等同于单图 50 ms 延迟。
- **消融结论：** 去掉分布匹配，回归结果更平滑、细节弱；去掉回归正则，训练更容易 mode collapse。两项联合才是初版稳定配方。
- **训练代价：** 文本到图像版本需先用多步确定性 sampler 制作大量 noise–image 对；DMD2 指出仅这一步的成本已超过其后续完整训练计算的 4 倍。

**证据未支持：** 一步模型与 teacher 在多样性上完全等价；图像 FID 改善能直接外推到视频动态；DMD 的近似 KL 梯度是无偏估计。

### 总结讨论

DMD 真正重要的贡献不是“把扩散变成 GAN”，而是提供了可反传的分布匹配梯度：冻结 teacher score 把样本拉向目标分布，在线 fake score 抵消当前生成分布自身的密度方向。它允许 teacher/student 架构不同，因此适合后来把双向视频 teacher 蒸成因果学生。适用边界是单步图像蒸馏；初版的 ODE 回归集、反向 KL 的 mode seeking、fake score 追踪误差都是后续工作的关键欠账。阅读判断：报告 CausVid 时应把 DMD 写成其损失来源，而不能说 DMD 已经解决 AR 暴露偏差。

### 代码与数据

- **代码 / 模型：** 项目页提供论文、视频、slides 与 poster，但本次核对未找到作者维护的官方代码仓库或权重下载；不要把 DMD2 仓库误写成 DMD 初版代码。
- **数据：** ImageNet / COCO 为评测或训练来源；文本版还依赖 teacher 生成的预计算 noise–image 回归对，制作成本高且不是纯粹“无数据蒸馏”。

### 局限、失败案例与开放问题

- 需要昂贵的多步 teacher ODE 回归数据集，限制大模型扩展。
- fake score 模型追踪非平稳学生分布，梯度有近似误差。
- reverse-KL 倾向 mode seeking，作者用回归项换稳定性，可能牺牲分布自由度。
- 一步学生在复杂文本组合、细节和多样性上仍受 SD-v1.5 teacher 与蒸馏设定限制。
- 没有视频、长序列或交互控制实验。

---

## 2. Improved Distribution Matching Distillation for Fast Image Synthesis

**作者：** Tianwei Yin, Michaël Gharbi, Taesung Park, Richard Zhang, Eli Shechtman, Frédo Durand, William T. Freeman
**年份与发表：** 2024，NeurIPS 2024 Main Conference Track，*Advances in Neural Information Processing Systems 37*。MIT / Adobe Research。预印本 arXiv:2405.14867（v2，cs.CV）；正式论文 DOI：10.52202/079017-1505；arXiv DOI：10.48550/arXiv.2405.14867。
**可靠入口：** [arXiv](https://arxiv.org/abs/2405.14867)｜[HTML 全文](https://arxiv.org/html/2405.14867)｜[NeurIPS 论文页](https://proceedings.neurips.cc/paper_files/paper/2024/hash/54dcf25318f9de5a7a01f0a4125c541e-Abstract-Conference.html)｜[项目页](https://tianweiy.github.io/dmd2/)｜[代码与模型](https://github.com/tianweiy/DMD2)｜[AlphaXiv](https://alphaxiv.org/abs/2405.14867)
**代表图：** DMD2，Fig. 3，TTUR、GAN 判别分支与分布匹配联合训练。来源：[Fig. 3 原图 PNG](https://arxiv.org/html/2405.14867v2/gan_pipeline_new.png)

![DMD2 Fig. 3: distribution matching, TTUR, and GAN loss](https://arxiv.org/html/2405.14867v2/gan_pipeline_new.png)

### 当前挑战

DMD 的分布目标有吸引力，但实际稳定性依赖预计算的 ODE 回归对：制作昂贵，而且把学生绑定到 teacher 的特定采样路径，形成质量上限。直接删掉回归项又会因 fake score 跟不上快速变化的生成分布而发生亮度振荡和训练崩坏。扩展到多步生成时，训练若从“真实图像加噪”开始、推理却从“学生上一步输出”开始，还会出现新的输入分布错位。

本文具体要解决三点：**无回归集的稳定纯 DMD、利用真实数据超过 imperfect teacher score、多步训练与推理分布对齐。**

### 研究动机

核心 Insight 有三层：

- fake score 是移动目标，应比 generator 更频繁更新；作者采用 **5 次 fake-score 更新 : 1 次 generator 更新** 的 two-time-scale update rule（TTUR）。
- teacher score 本身近似真实数据分布；在 fake denoiser bottleneck 加一个轻量 GAN classifier，让真实图像直接校正分布匹配误差。
- 多步学生必须在训练时看到自己前几步产生的 noisy synthetic states，而非只看 real images 加噪；这与后来 Self Forcing 强调的 train–test distribution 对齐在思想上相通，但 DMD2 仍是非 AR 图像生成。

与本报告 **基础相关**：DMD2 解释了 fake-score 更新频率、GAN 辅助和多步 self-simulation 为什么能稳定蒸馏；后续视频工作主要继承 DMD 主体，但在时序 rollout 上发展出 Self Forcing，而不是直接照搬 DMD2 的图像多步管线。

### 技术方案

- **输入：** 随机噪声、类标签或文本 prompt；ImageNet 真实图像用于 GAN 项，文本模型基于 SD-v1.5 / SDXL。
- **过程：** 删除 DMD 的 ODE LPIPS 回归；每次更新生成器前多次更新 fake diffusion score。fake denoiser 的 encoder/bottleneck 同时接 GAN 分类头，区分加噪后的真实与生成样本；generator 联合优化 distribution matching 与 non-saturating GAN loss。多步版本把 generator 重新参数化为可接受当前噪声状态与时间步的 denoiser，并以 backward simulation 生成接近推理态的训练输入。
- **输出：** 1-step ImageNet / SD-v1.5 图像，以及 1–4 step 的 SDXL 百万像素图像。

相对 DMD，DMD2 不再需要 teacher ODE 配对集，且允许真实数据把学生质量推过 teacher sampler；相对纯 GAN，它保留 teacher score、CFG 接口和分布匹配约束。

### 实验结果

**作者主张：** DMD2 在一与少步图像生成上达到新的最佳结果，部分指标超过蒸馏 teacher。

实验实际支持：

- **ImageNet 64×64，一步：** FID **1.28**，相对 DMD 的 2.62 明显改善。
- **zero-shot COCO 2014，一步 SD-v1.5：** FID **8.35**，比 DMD 的 11.49 改善 3.14；论文以 teacher 的 50-step PNDM 为比较口径，并称推理成本约降 500×，该倍数依赖其 FLOPs/前向设定。
- **SDXL，4-step：** COCO-10K FID / CLIP 为 **19.32 / 0.332**。人评中，4-step DMD2 在视觉吸引力上有 24% 样本被偏好于 100-step teacher，文本对齐接近；这不是“总体胜率 76%”或全面支配 teacher。
- **消融：** 直接去回归项，ImageNet FID 退到 3.48；加 TTUR 恢复到 DMD 量级；再加 GAN 项约降 1.1 FID。SDXL 消融显示去 GAN 会过饱和/过平滑，去 distribution matching 的纯 GAN 文本对齐和稳定性更差，去 backward simulation 的 patch FID 变差。
- **成本边界：** TTUR 提高单次 generator 更新成本；10:1 更稳定但太慢，作者选择 5:1 折中。

**证据未支持：** DMD2 在所有 prompt 上优于 SDXL teacher；1-step SDXL 已达到 4-step 质量；加入 GAN 后仍是完全不依赖真实数据的蒸馏。

### 总结讨论

DMD2 把初版“分布匹配 + 轨迹回归”的妥协改成更纯的分布训练：用更快的 fake-score 内循环解决移动 critic，用真实数据 GAN 项修 teacher score，用推理态模拟解决多步 mismatch。它与 Self Forcing 的关键共同点是训练输入必须接近推理生成分布，但 DMD2 没有历史帧或 AR cache。阅读判断：应把它放在 CausVid 前作为稳定化基础与概念先驱；不能用其图像 FID 为视频 DMD 的时序稳定性背书。

### 代码与数据

- **代码 / 模型：** [tianweiy/DMD2](https://github.com/tianweiy/DMD2)，项目页声明代码、模型和数据可用。
- **数据：** ImageNet 实验使用真实训练图像；文本实验涉及 COCO 评测与 SD 系 teacher。GAN 项意味着训练不再是仅从预训练模型取知识。
- **许可：** 仓库代码与各 SD / SDXL 权重许可需分别遵守，不能由论文开放状态一并推断。

### 局限、失败案例与开放问题

- 4-step 才能匹配最大 SDXL teacher 的质量，一步仍有明显差距。
- 文本到图像多样性相对 teacher 略降，GAN 权重与多样性/对齐存在权衡。
- TTUR 需要多次 fake-score 更新，提高训练算力与实现复杂度。
- GAN 项需要真实数据，并引入对抗训练稳定性问题。
- backward simulation 解决的是图像多步输入错位，不包含 AR 视频的长程暴露偏差。

---

## 3. From Slow Bidirectional to Fast Autoregressive Video Diffusion Models

**作者：** Tianwei Yin, Qiang Zhang, Richard Zhang, William T. Freeman, Frédo Durand, Eli Shechtman, Xun Huang  
**年份与发表：** 2025，CVPR 2025（*Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*，pp. 22963–22974）。Tianwei Yin 与 Qiang Zhang 为共同一作，通讯 tianweiy@mit.edu。预印本 arXiv:2412.07772（v4，cs.CV）。arXiv DOI：10.48550/arXiv.2412.07772。IEEE Xplore 正式 DOI 本次未单独打开核验。模型通称 **CausVid**。  
**可靠入口：** [arXiv](https://arxiv.org/abs/2412.07772)｜[HTML 全文](https://arxiv.org/html/2412.07772)｜[CVPR Open Access](https://openaccess.thecvf.com/content/CVPR2025/html/Yin_From_Slow_Bidirectional_to_Fast_Autoregressive_Video_Diffusion_Models_CVPR_2025_paper.html)｜[项目页](https://causvid.github.io/)｜[代码](https://github.com/tianweiy/CausVid)｜[模型](https://huggingface.co/tianweiy/CausVid)｜[AlphaXiv](https://alphaxiv.org/abs/2412.07772)  
**代表图：** CausVid，Fig. 1，双向 50-step 与 4-step 因果流式生成的延迟对比。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2412.07772v4/teaser_final.png)

![CausVid Fig. 1: bidirectional vs few-step causal streaming generation](https://arxiv.org/html/2412.07772v4/teaser_final.png)

### 当前挑战

领域长期问题是：高质量视频扩散依赖双向注意力，单帧生成必须看到未来，延迟与显存随帧数二次增长，无法做流式交互。本文针对的具体缺口是：**如何把已经训好的双向 DiT 变成可 KV cache 的少步因果生成器，同时不把误差累积原样传给学生。**

- **作者明确指出的失败模式：** 双向 DiT 生成 128 帧需整段算完才能看第一帧（文中 teacher 约 219 s）；朴素 AR 视频模型虽降低首帧等待，但仍远达不到交互帧率，且逐步累积误差。
- **蒸馏缺口：** 当时视频蒸馏几乎都把非因果 teacher 蒸成非因果学生，且多针对 <2 s 短片。把因果 teacher 再蒸成 few-step 学生会继承更弱 teacher 和其误差累积。
- **评测缺口：** 主表短视频用 MovieGen 前 128 个 prompt 的 VBench 三轴，不是完整 VBench；完整 946-prompt VBench-Long 放在附录。不要把 94.7 的 Temporal Quality 和 84.27 的 Total Score 混成同一套数字。

### 研究动机

核心 Insight：**不对称蒸馏——用双向 teacher 的分布匹配监督因果学生，而不是先把 teacher 也改成因果再蒸馏。** DMD 在分布层匹配，允许 teacher/student 架构不同；ODE 轨迹初始化用来稳住后续 DMD。这改变的是注意力接口（block-wise causal）和训练信号（分布匹配而非逐步 denoising），不是再训一个更强的双向生成器。

与本知识库课题 **间接相关**：它是后续 Self Forcing / Causal Forcing 的起点，也把交互视频、游戏渲染、机器人视频奖励列为应用方向，但本文本身不做动作条件世界模型，也不做 \(do(\cdot)\)。可借鉴点是：因果注意力 + KV cache + few-step 蒸馏这一工程接口。

### 技术方案

- **输入：** 文本 prompt；可选首帧图像或流式视频块。潜空间由 3D VAE 把 16 像素帧压成 5 个 latent 帧。训练分辨率 \(352\times 640\)、12 FPS、约 10 s。
- **过程：** 学生与 teacher 同构，但块内双向、块间因果。先用 bidirectional teacher 生成约 1000 条 ODE 轨迹，对学生做 3000 iter 回归初始化；再用 asymmetric DMD（双向 \(s_{\text{data}}\) 监督因果 \(G_\phi\)，在线训 \(s_{\text{gen}}\)）6000 iter。推理每块 4 步，时间步 \([999,748,502,247]\)，用 KV cache；推理时不再需要训练用的 block-causal mask。全流程约 2 天 × 64 H100。数据约 40 万内部有版权单镜头视频 + 图像，按 CogVideoX 配方过滤。
- **输出：** 流式视频帧。文中测得首帧延迟 1.3 s、之后约 9.4 FPS（H100，10 s / 120 帧 / \(640\times 352\)）。零样本支持 I2V、流式 V2V（SDEdit 式对块加 \(t_1\) 噪声再一步去噪）、动态换 prompt。

与最近 baseline 的实质差异：相对 CogVideoX / MovieGen，生成是因果流式而非整段双向；相对把因果 teacher 再蒸馏的朴素路线，teacher 保持双向。作者自己的消融显示：many-step 因果微调会把误差累积传下去；双向 teacher + ODE init 才是最终配置。

### 实验结果

**作者主张：** 这是首个质量上能与双向扩散竞争的自回归视频生成方法；VBench-Long total 84.27 超过当时所有官方评测模型；相对同规模 CogVideoX 延迟降约 \(160\times\)、吞吐升约 \(16\times\)。

实验实际支持（数字均来自原文表格/正文）：

- **短视频（MovieGen 前 128 prompt，长度尽量贴近 10 s）：** Temporal / Frame / Text = **94.7 / 64.4 / 30.1**，高于 CogVideoX-5B、OpenSORA、Pyramid Flow、MovieGen。
- **约 30 s 长视频：** Temporal / Frame / Text = **94.9 / 63.4 / 28.9**；成像质量随时间曲线显示因果 teacher 会崩，不对称 DMD 学生能撑住。
- **效率（H100，10 s / 120 帧）：** CausVid 1.3 s / 9.4 FPS vs CogVideoX-5B 208.6 s / 0.6 FPS、双向 teacher 219.2 s / 0.6 FPS。
- **消融：** 双向 many-step 94.6/62.7/29.6；因果 many-step 92.4/60.1/28.5；ODE init + 因果 teacher 的 4-step 学生 91.9/61.7/28.2；最终 ODE init + 双向 teacher **94.7/64.4/30.1**。无 ODE init 的双向 teacher 4-step 为 93.4/60.6/29.4。
- **I2V（VBench-I2V 设定，无额外训练）：** 92.0 / 65.0 / 28.9，高于 CogVideoX-5B 与 Pyramid Flow。
- **流式 V2V：** 相对 StreamV2V，在 60 条 ≥16 帧的 DAVIS 视频上 Temporal/Frame/Text 为 93.2/61.7/27.7 vs 92.5/59.3/26.9。
- **附录 VBench-Long（946 prompt，16 指标）：** Total **84.27**，Quality 85.65，Semantic 78.75；Dynamic Degree 92.69。这是完整榜，不是主表 128-prompt 子集。
- **用户研究：** MovieGenBench 前 29 prompt × 3 评分者；相对 MovieGen / CogVideoX / Pyramid Flow 偏好 >50%。固定 seed=0。

**证据未支持：** 无限长视频无质量下降；DMD 保持 teacher 多样性；该内部 teacher 的数字可直接与后来 Wan2.1-1.3B 上的 CausVid 重实现横比（分辨率、骨干都不同）。

### 总结讨论

CausVid 把“双向质量 vs 因果流式”收成一套可复现配方：block-causal DiT、ODE 初始化、不对称 DMD、KV cache。CVPR 版与后续 Wan 重实现不是同一套权重，引用时要写清骨干。适用边界是文本/图像条件的流式视频，不是动作条件世界模型。失败与开放问题包括：超长视频仍会过曝/退化；VAE 必须凑满 5 个 latent 帧才出像素，限制首帧延迟；反向 KL 会压多样性。阅读判断：适合作为 AR 视频蒸馏谱系的起点；不要把 84.27 写成击败了所有闭源系统，也不要把“causal student”写成因果世界模型。

### 代码与数据

- **代码：** [tianweiy/CausVid](https://github.com/tianweiy/CausVid)，README 标明 CVPR 2025。
- **权重：** Hugging Face `tianweiy/CausVid`。
- **数据：** 约 40 万内部有版权视频，完整预训练语料不能公开复现。后续 Self Forcing 比较用的是官方 Wan-1.3B 重实现，不是这篇内部 teacher 的原权重。

### 局限、失败案例与开放问题

- 14 分钟示例已有轻微过曝；作者承认极端长视频质量仍降。
- 首帧延迟被 5-latent-frame VAE 卡住，要再降一个数量级需 frame-wise VAE。
- reverse KL / DMD 降低输出多样性。
- 学生帧质量可超过双向 teacher，但 temporal flickering 与多样性更差。
- 主表 128-prompt 与附录全量 VBench-Long 不可混引。
- 训练数据不公开，原始 CausVid 与 Wan 重实现不可直接比分数。

---

## 4. Self Forcing: Bridging the Train-Test Gap in Autoregressive Video Diffusion

**作者：** Xun Huang, Zhengqi Li, Guande He, Mingyuan Zhou, Eli Shechtman  
**年份与发表：** 2025，NeurIPS 2025 Spotlight（官方会议页标注 Spotlight Poster）。预印本 arXiv:2506.08009（v2）。Adobe Research + UT Austin。通讯 xuhuang@adobe.com。尚无单独核验的会议 DOI；arXiv DOI：10.48550/arXiv.2506.08009。  
**可靠入口：** [arXiv](https://arxiv.org/abs/2506.08009)｜[HTML 全文](https://arxiv.org/html/2506.08009)｜[NeurIPS 2025](https://nips.cc/virtual/2025/loc/san-diego/poster/116208)｜[项目页](https://self-forcing.github.io/)｜[代码](https://github.com/guandeh17/Self-Forcing)｜[PDF](https://self-forcing.github.io/static/self_forcing.pdf)｜[AlphaXiv](https://alphaxiv.org/abs/2506.08009)  
**代表图：** Self Forcing，Fig. 1，Teacher Forcing / Diffusion Forcing / Self Forcing 三种训练范式。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2506.08009v2/overview.png)

![Self Forcing Fig. 1: teacher forcing vs diffusion forcing vs self-rollout training](https://arxiv.org/html/2506.08009v2/overview.png)

### 当前挑战

领域长期问题仍是暴露偏差：训练时看 ground-truth 上下文，推理时必须吃自己的错。本文针对的不是“再做一个更快的 CausVid”，而是 **CausVid 的 DMD 匹配了错误分布**。

- **作者对 CausVid 的具体批评：** CausVid 用 Diffusion Forcing 生成训练输出，再拿 DMD 去对齐真实视频分布；但 DF 输出并不来自推理时的自回归分布，因此 DMD 在匹配错误对象。
- **TF / DF 的共同失败：** 两者都能并行训练整段视频，却都在 GT 或噪声上下文上做帧级去噪；推理时上下文是自己生成的干净帧，误差随 AR 步数放大，表现为过饱和、过锐化。
- **效率缺口：** 真·实时需要吞吐高于播放帧率 **且** 首帧延迟低于感知阈值；只报 FPS 不够。
- **长视频 KV：** 双向 DF 不能 cache；已有因果实现每次滑窗重算重叠 KV。朴素 rolling cache 会因第一帧统计特性不同而闪烁。

### 研究动机

核心 Insight：**训练时按推理配方自 rollout（带 KV cache），再对整段生成视频做 holisitic 分布匹配。** 这样 DMD / SiD / GAN 匹配的是真正的 \(p_\theta(x^{1:N})\)，而不是 DF 的训练替代分布。梯度截断到每帧最后一步、随机采样中间步 \(s\)，并把 KV 从梯度图拆掉，使顺序 unroll 在 post-training 阶段可承受。

与本知识库课题 **间接相关但接口关键**：它把交互视频、游戏、世界模拟列为延迟以毫秒计的目标，训练配方被 Causal Forcing / LongLive / minWM 直接继承。它优化的是生成分布对齐，不是动作条件或物理干预。

### 技术方案

- **输入：** 文本 prompt（VidProM 过滤 + Qwen2.5-7B 扩写）。骨干 Wan2.1-T2V-1.3B，5 s、16 FPS、\(832\times 480\)。
- **过程：** 先按 CausVid 协议用 16k 条 ODE 对做因果初始化。然后 Self Forcing：对每一帧从噪声逐步去噪，条件是自己已生成的 KV；只在随机步 \(s\) 打开梯度，其余步 stop-grad；KV 不回传。损失可选 DMD（real score 用 Wan-14B）、SiD 或 R3GAN。实现 chunk-wise（3 latent 帧/块）与 frame-wise 两种。长视频用固定长度 rolling KV，训练时禁止最后一块看见第一块，以模拟 cache 里不再有 image latent 的外推条件。DMD 约 1.5 h × 64 H100。
- **输出：** 流式视频。chunk-wise 4-step：17.0 FPS、0.69 s 延迟（H100）；frame-wise：8.9 FPS、0.45 s。

与最近 baseline 的实质差异：相对 CausVid，DMD 的样本来自自 rollout 而非 DF；相对 TF/DF+DMD，上下文来自 \(p_\theta\) 而非 \(p_{\text{data}}\)。作者强调动机是纠暴露偏差，不只是减步数，因此 consistency distillation 这类只缩短步数的方法不适用。

### 实验结果

**作者主张：** 在相近参数量上同时拿到最高 VBench 与实时吞吐，用户偏好超过初始化用的双向 Wan2.1。

实验实际支持：

- **主表（官方 CausVid Wan-1.3B 重实现对照）：** chunk-wise Self Forcing VBench Total/Quality/Semantic = **84.31 / 85.07 / 81.28**，17.0 FPS / 0.69 s；Wan2.1 84.26 / 85.30 / 80.09 但 0.78 FPS / 103 s；CausVid 重实现 81.20 / 84.05 / 69.80。frame-wise 84.26 / 85.25 / 80.30，8.9 FPS / 0.45 s。
- **消融：** chunk-wise 上 SF-DMD 84.31 高于 DF+DMD 82.76、TF+DMD 82.32、many-step TF 83.58。frame-wise 差距更大：SF-DMD 84.26 vs DF 77.24 / TF 80.34。SiD / GAN 略低于 DMD 但仍高于 TF/DF 蒸馏。
- **Rolling KV：** 滑窗重算 KV 生成 10 s 仅 4.6 FPS；训练时挡住首块后 rolling cache 16.1 FPS 且减轻闪烁。
- **用户研究：** MovieGenBench 全部 1003 prompt，每条 1 名用户二选一；SF 优于含 Wan2.1 在内的对照。这是偏好而非绝对质量标尺。
- **训练成本：** 与 TF/DF 单步耗时接近；同墙钟下 VBench 更高。作者把它归因于 SF 用 FlashAttention-3 全注意力，而 TF/DF 要 FlexAttention 因果 mask。

**证据未支持：** 训练上下文之外的任意长视频不退化；gradient truncation 不影响长程依赖；项目页“单卡 4090 实时”与文中 H100 测速不是同一套数字，引用时要写硬件。

### 总结讨论

Self Forcing 把 CausVid 的不对称 DMD 补上了缺失的一环：匹配对象必须是推理分布。Wan-1.3B 上的对照支持这一诊断，尤其是 frame-wise 设定下 TF/DF 崩而 SF 不崩。适用边界是 5 s 级训练上下文上的 T2V 流式生成。失败案例是外推显著长于训练长度时质量仍掉；作者也承认截断梯度可能伤长程依赖。阅读判断：后续 Causal Forcing 接受其 DMD 阶段、只改 ODE 初始化，说明这篇的 self-rollout 已被当作标准；不要把 VBench 84.31 写成已经解决世界模拟，也不要把“holistic matching”写成因果识别。

### 代码与数据

- **代码：** [guandeh17/Self-Forcing](https://github.com/guandeh17/Self-Forcing)，基于 Wan2.1 与 CausVid 开源实现。
- **DMD/SiD：** 作者称可无视频数据，只靠预训练扩散模型；GAN 变体用 14B 模型生成的 70k 视频。
- **Prompt：** VidProM 过滤后约 25 万条再 LLM 扩写；VBench 评测同样扩写。完整原始视频预训练语料仍依赖 Wan。

### 局限、失败案例与开放问题

- 超出训练上下文的长视频仍可见质量下降。
- 每帧只回传最后一步、KV 切断梯度，长程信用分配受限。
- 朴素 rolling KV 若不在训练中挡住首块，会因 image latent 统计不匹配而闪烁。
- frame-wise 比 chunk-wise 动态更强、时序一致性更弱（附录雷达图）。
- reverse KL 仍可能压多样性；GAN 需要大 batch（768）。
- 开源实现与 Adobe 内部实验设置若有差异，需以仓库 README 为准。

---

## 5. Causal Forcing: Autoregressive Diffusion Distillation Done Right for High-Quality Real-Time Interactive Video Generation

**作者：** Hongzhou Zhu, Min Zhao, Guande He, Hang Su, Chongxuan Li, Jun Zhu  
**年份与发表：** 2026，arXiv preprint（v2/v5 HTML 与摘要一致；cs.LG/cs.CV 线索见 arXiv）。Hongzhou Zhu 与 Min Zhao 共同一作；通讯 Jun Zhu（dcszj@tsinghua.edu.cn）。清华 / 生数 / UT Austin / 人大。尚无 DOI / 正式出版页。arXiv:2602.02214。  
**可靠入口：** [arXiv](https://arxiv.org/abs/2602.02214)｜[HTML 全文](https://arxiv.org/html/2602.02214)｜[项目页](https://thu-ml.github.io/CausalForcing.github.io/)｜[代码](https://github.com/thu-ml/Causal-Forcing)｜[AlphaXiv](https://alphaxiv.org/abs/2602.02214)  
**代表图：** Causal Forcing，Fig. 3，ODE 初始化需要帧级单射，以及 Self Forcing 用双向 teacher 监督 AR 学生为何违规。来源：[Fig. 3 原图 PNG](https://arxiv.org/html/2602.02214v5/Fig3.png)

![Causal Forcing Fig. 3: frame-level injectivity vs bidirectional ODE pairs](https://arxiv.org/html/2602.02214v5/Fig3.png)

### 当前挑战

领域长期问题仍是把双向基础模型蒸成实时 AR 学生。本文针对的缺口是 **ODE 初始化的理论对象错了**，而不是再调 DMD。

- **作者用对照隔离问题：** 即使把 AR 学生初始化成已经 few-step 的双向 DMD 模型（采样步差距消失、只剩架构差距），后续 DMD 仍明显弱于标准双向 DMD。结论：架构差距必须在 ODE 阶段补，DMD 补不上。
- **帧级单射：** ODE 回归要求噪声样本对应唯一干净样本。双向 PF-ODE 只在整段视频上单射；AR 学生按帧生成，同一噪声帧在不同未来上下文下可对应多个干净帧。MSE 最优解退化成条件期望，表现为糊。Lemma 3.2 / Prop. 3.3 给出形式化陈述；经验支撑是 Fig. 3c 的糊视频，不是对真实物理因果的证明。
- **TF vs DF：** 作者主张 AR 扩散训练应用 teacher forcing。Prop. 3.4 说 DF 在干净前缀条件下不跟随数据分布；Fig. 4 显示 DF 更易崩溃，其更高 Dynamic Degree 被作者读成病态运动而非更好动态。

### 研究动机

核心 Insight：**few-step AR 学生的 ODE 教师必须自己也是 AR，其 PF-ODE 才天然满足帧级单射。** 三阶段因此变成：TF 训多步 AR teacher → 用该 teacher 采因果 ODE 轨迹做学生初始化 → 再走 Self Forcing 同款不对称 DMD（双向 real/fake score + 学生自 rollout）。这改变的是初始化目标，不是 DMD 损失本身。

与本知识库课题 **直接相关于交互视频世界模型接口，间接相关于因果**。标题里的 Causal 指时序因果注意力与因果 ODE，不是结构因果。Causal Forcing++ / minWM 把它当成可插拔 Stage 2。

### 技术方案

- **输入：** 文本；骨干 Wan2.1-T2V-1.3B，81 帧、\(832\times 480\)，chunk-wise（3 latent 帧）。
- **过程：** Stage 1：在双向模型合成的 3K 集 \(\mathcal{D}_{\text{Bi}}\) 上 TF 训 AR 扩散 2K 步。Stage 2：用该 AR teacher 在 GT 历史上对当前帧解 PF-ODE，存 3K 条 \(\mathcal{D}_{\text{Causal}}\)，对学生做 1K 步回归。Stage 3：与 Self Forcing 相同的 asymmetric DMD，VidProM，750 步。作者强调 ODE+DMD 总步数与 Self Forcing 同预算。附录还给出因果 CD，作为 ODE 的替代初始化，质量仍低于 score distillation。
- **输出：** 4-step chunk-wise 流式视频；吞吐/延迟与 Self Forcing 相同（文中 17.0 FPS / 0.69 s，H100）。

与最近 baseline 的实质差异：相对 Self Forcing，只换 ODE teacher（AR vs 双向）；相对 APT2（GAN + TF-CD、无时序 KV cache），本文留在不对称 DMD + KV cache 路线。作者声明 APT2 未开源故不比数字。

### 实验结果

**作者主张：** 同训练预算、同推理成本下全面超过 Self Forcing；相对 SF 提升 Dynamic Degree 19.3%、VisionReward 8.7%、Instruction Following 16.7%。

实验实际支持：

- **主表：** Causal Forcing Total/Quality/Semantic = **84.04 / 84.59 / 81.84**；Dynamic Degree **68**，VisionReward **6.326**，Instruct **56**，用户排序 1.64（越小越好）。Self Forcing 83.74 / 84.48 / 80.77 / 57 / 5.820 / 48 / 2.87。CausVid 81.33 / 83.98 / 70.72 / 62 / 5.741 / 12。Wan2.1-1.3B 83.37 / 84.30 / 79.65 / 61 / 5.275 / 42，但 0.78 FPS / 103 s。MAGI-1-4.5B 在此表上 78.88 total、0.19 FPS / 282 s。
- **评测拆分：** VBench 总体；VisionReward / Instruct / Dynamic Degree 用作者另编的 100 条高运动 prompt（补充材料），并 ×100。用户研究 10 人 × 10 prompt 排序。这些子集不是 VBench 官方 split。
- **消融：** TF 3.343 VisionReward vs DF 1.583。Causal ODE+DMD vs SF ODE+DMD：chunk-wise VisionReward 6.326 vs 3.330，Dynamic 68 vs 24；frame-wise Dynamic 64 vs 2，VisionReward 6.204 vs 1.951。因果 CD 相对不对称 CD 有提升，但仍弱于 DMD。
- **百分比：** 19.3% 来自 (68−57)/57；8.7% 来自 (6.326−5.820)/5.820；16.7% 来自 (56−48)/48。这是作者定义的相对提升，不是 VBench Total 的 19%。

**证据未支持：** DMD 阶段被证明“不能”缩小架构差距（只是该对照下没缩小）；帧级非单射在所有双向 DiT 上必然成立（引理依赖“对其余帧非几乎处处常数”的假设，作者用注意力图文献作为经验理由）；长视频外推已被作者自己排除，需 LongLive 等正交方法。

### 总结讨论

Causal Forcing 把 Self Forcing 的失败从“DMD 匹配错分布”推进到“ODE 回归对象不单射”。在 Wan-1.3B、同预算设定下，运动与 VisionReward 的增益与消融同向。适用边界仍是 5 s 注意力窗口的 T2V 蒸馏。作者明确：直接外推会长于训练长度会出训练–推理差。阅读判断：理论部分是关于 PF-ODE 回归良定性，不要写成发现了世界的因果结构；引用 19.3% 时必须标明是 100-prompt Dynamic Degree，不是 VBench Total。

### 代码与数据

- **代码：** [thu-ml/Causal-Forcing](https://github.com/thu-ml/Causal-Forcing)，同时承接 Causal Forcing++。
- **数据：** \(\mathcal{D}_{\text{Bi}}\) / \(\mathcal{D}_{\text{Causal}}\) 为内部合成轨迹；DMD 用 VidProM。完整复现依赖 Wan 权重与这些合成对。
- **许可：** 以仓库 LICENSE 为准，本次未逐文件核验。

### 局限、失败案例与开放问题

- 训练长度 5 s，外推需 LongLive / Rolling Forcing / Infinity-RoPE 等，本文不解决。
- Dynamic Degree / VisionReward 用自建 100 prompt，与 VBench 官方运动轴不是同一分布。
- 用户研究仅 10×10，排序均值不能当大规模主观结论。
- 因果 CD 仍是 vanilla LCM，作者承认弱于 score distillation。
- ODE 轨迹存储/生成成本高，直接催生 Causal Forcing++。
- 与 APT2 无数字对照，架构不同不能外推胜负。

---

## 6. Causal Forcing++: Scalable Few-Step Autoregressive Diffusion Distillation for Real-Time Interactive Video Generation

**作者：** Min Zhao, Hongzhou Zhu, Kaiwen Zheng, Zihan Zhou, Bokai Yan, Xinyuan Li, Xiao Yang, Chongxuan Li, Jun Zhu  
**年份与发表：** 2026，arXiv preprint（v3 HTML）。Min Zhao 与 Hongzhou Zhu 共同一作；通讯 Jun Zhu。清华 / 生数 / 人大。arXiv:2605.15141。尚无 DOI / 正式出版页。  
**可靠入口：** [arXiv](https://arxiv.org/abs/2605.15141)｜[HTML 全文](https://arxiv.org/html/2605.15141)｜[代码（Causal-Forcing 仓库）](https://github.com/thu-ml/Causal-Forcing)｜[minWM](https://github.com/shengshu-ai/minWM)｜[AlphaXiv](https://alphaxiv.org/abs/2605.15141)  
**代表图：** Causal Forcing++，Fig. 1，相对 Self Forcing / Causal Forcing 的正确性、效率与延迟对比。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2605.15141v3/overall.png)

![Causal Forcing++ Fig. 1: causal CD replacing causal ODE initialization](https://arxiv.org/html/2605.15141v3/overall.png)

### 当前挑战

Causal Forcing 在 chunk-wise 4-step 已能打，但交互仍受 **块粒度过粗** 和 **每块 4 步延迟** 限制。本文把设定推到 **frame-wise × 1–2 采样步**，并指出这时 Stage 2 初始化成为瓶颈：

- Self Forcing 式双向 ODE：目标与 AR 学生不对齐，在 frame-wise 低步数下 DMD 后会崩（消融里 Dynamic Degree 可到 0）。
- 直接用多步 AR 当初始化：没有 few-step 能力，1-step 时动态/指令跟随接近崩溃。
- Causal Forcing 的因果 ODE：目标正确，但每条样本要跑完整 PF-ODE（文中例 48 步）并离线存盘；80K 视频规模约 11,600 A800 GPU·h + 1,900 GiB。

作者还检查了因果 DMD 当 Stage 2：早期帧更锐，但 reverse KL 的 mode-seeking 在历史漂移后把概率质量迅速推进低质量区，暴露偏差比因果 CD 更重。这是作者的机制假说，配有 Fig. 5 示意，不是因果识别实验。

### 研究动机

核心 Insight：**因果 ODE 与因果 CD 学的是同一个 AR 条件 flow map / consistency function；CD 用相邻时间步的一次在线 teacher ODE 步代替整条离线轨迹。** 局部配对的逐步间隙更小，因而更好优化。Stage 1 / Stage 3 沿用 Causal Forcing，只换 Stage 2。

与本知识库课题 **直接相关**：第 3.3 节把同一配方蒸到相机位姿条件生成器，明确对标 Genie 3 式交互世界模型；完整工程化交给 minWM。动作条件变体仍是 chunk-wise 4-step，frame-wise 2-step 留作未来工作。

### 技术方案

- **输入：** 文本；Wan2.1-1.3B；480×832、81 帧；**frame-wise** AR。Stage 1–2 用含 OpenVid 采样的 80K 视频；Stage 3 用 VidProM。
- **过程：** Stage 1 TF AR 扩散 20K 步。Stage 2 因果 CD：平方距离、48 个离散时间步、Euler，5K 步；学生 \(G_\theta(x_t^i,x_{\mathrm{gt}}^{<i},t)=x_t^i-t\,v_\theta(\cdot)\)。Stage 3 不对称 DMD 1K 步；batch 64。少于 4 步时采用 ASD 技巧：第一帧仍 4 步，后续 20 个 latent 帧用 1 或 2 步——因此文中 1/2/4-step 的首帧延迟相同。动作世界模型：WorldPlay 标注相机 → PRoPE 注入双向 Wan → 再走 CF++。
- **输出：** 流式帧。效率在 **单卡 A800、不含 VAE** 上测：2-step 14.1 FPS / 0.27 s；1-step 20.7 FPS / 0.27 s；4-step 8.69 FPS / 0.27 s。与 Self Forcing / Causal Forcing 的 H100+VAE 测速不可直接比。

与最近 baseline 的实质差异：相对 Causal Forcing，Stage 2 从离线因果 ODE 换成在线因果 CD；相对 Self Forcing，初始化教师是 AR 而非双向。APT2 同样用过 TF-CD，但走 GAN、无双向 DMD teacher、无时序 KV cache。

### 实验结果

**作者主张：** frame-wise 2-step 在 VBench Total / Quality / VisionReward 上超过 SOTA 的 chunk-wise 4-step Causal Forcing，首帧延迟降 50%，Stage 2 成本约 \(4\times\)。

实验实际支持：

- **主表（相对先前 chunk-wise 4-step 方法）：** CF++ 2-step Total/Quality/Semantic **84.14 / 84.89 / 81.13**，Dynamic 64，VisionReward 6.661，Instruct 51。Causal Forcing 84.04 / 84.59 / 81.84 / 68 / 6.326 / 56。4-step CF++ Quality 84.94、VisionReward 6.798、Dynamic 71，但 Semantic 80.75、Instruct 47，并非全面领先。1-step Total 83.35，Instruct 38。
- **“超过 CF 0.1 / 0.3 / 0.335”：** 2-step vs CF 的 Total 84.14−84.04、Quality 84.89−84.59、VisionReward 6.661−6.326。Semantic 与 Instruct 并未全面超过 CF。
- **消融（frame-wise，Stage 2 成本含 ODE 数据制作）：** 2-step 下因果 CD 84.14 / 6.661 / 51，2900 GPU·h、0 额外存储；因果 ODE 83.77 / 6.224 / 46，11600 GPU·h、1900 GiB；SF ODE 79.44、Dynamic 0；多步 AR init Dynamic 8；因果 DMD init VisionReward 6.108。1-step 下多步 AR init Instruct −14、Dynamic 0。
- **动作条件：** Fig. 4 定性展示前进/俯仰；无 VBench 或控制误差表。

**证据未支持：** 1-step 已达到 4-step 质量；CF++ 在所有轴上严格支配 Causal Forcing；A800 无 VAE 的 0.27 s 等于 H100 端到端延迟；动作世界模型已实时。

### 总结讨论

Causal Forcing++ 把“正确的 AR flow map”从昂贵离线轨迹改成可扩展的局部 consistency。frame-wise 2-step 的 Total/Quality/VisionReward 支持这一替换；Instruct 和部分动态轴上 4-step Causal Forcing 仍有优势。适用边界是 Wan-1.3B 级 T2V 蒸馏，外加一个尚未量化的相机控制演示。阅读判断：这是工程可扩展性论文，理论等价依赖于 CD 误差 \(\mathcal{O}((\Delta t)^p)\) 的标准界；不要把 VisionReward +0.335 写成交互世界模型已闭环。失败案例见消融可视化：错误初始化会出现糊、场景崩、物体漂移。

### 代码与数据

- **代码：** 并入 [thu-ml/Causal-Forcing](https://github.com/thu-ml/Causal-Forcing)；世界模型栈见 [shengshu-ai/minWM](https://github.com/shengshu-ai/minWM)。
- **数据：** Stage 1–2 的 80K 含 OpenVid；ODE 对照需额外轨迹存储。动作数据经 WorldPlay 生成。
- **测速口径：** 文中反复强调与 SF/CF 论文的 H100 口径不同。

### 局限、失败案例与开放问题

- 1-step 语义与指令跟随仍明显弱于 2-step。
- ASD 技巧使“1-step 模型”的第一帧其实仍是 4-step。
- 动作世界模型只有定性图，未推到 frame-wise 2-step。
- 因果 DMD 初始化不适合 AR rollout，作者认为与 reverse KL 有关，但未做因果消融。
- 效率数字不含 VAE，真实交互延迟会被解码拖累。
- 与 APT2 仍无公平数字对照。

---

## 7. MAGI-1: Autoregressive Video Generation at Scale

**作者：** Sand.AI, Hansi Teng, Hongyu Jia, Lei Sun, Lingzhi Li, Maolin Li, Mingqiu Tang, Shuai Han, Tianning Zhang, W. Q. Zhang, Weifeng Luo, Xiaoyang Kang, Yuchen Sun, Yue Cao, Yunpeng Huang, Yutong Lin, Yuxin Fang, Zewei Tao, Zheng Zhang, Zhongshu Wang, Zixun Liu, Dai Shi, Guoli Su, Hanwen Sun, Hong Pan, Jie Wang, Jiexin Sheng, Min Cui, Min Hu, Ming Yan, Shucheng Yin, Siran Zhang, Tingting Liu, Xianping Yin, Xiaoyu Yang, Xin Song, Xuan Hu, Yankai Zhang, Yuqiao Li  
**年份与发表：** 2025，arXiv preprint（v1，cs.CV）。arXiv:2505.13211。arXiv DOI：10.48550/arXiv.2505.13211。作者列表以 GitHub README / arXiv bibtex 为准；HTML 页未逐人展开署名。尚无会议/期刊版本。  
**可靠入口：** [arXiv](https://arxiv.org/abs/2505.13211)｜[HTML 全文](https://arxiv.org/html/2505.13211)｜[技术报告 PDF](https://static.magi.world/static/files/MAGI_1.pdf)｜[代码](https://github.com/SandAI-org/MAGI-1)｜[MagiAttention](https://github.com/SandAI-org/MagiAttention)｜[产品](https://sand.ai)｜[AlphaXiv](https://alphaxiv.org/abs/2505.13211)  
**代表图：** MAGI-1，Fig. 1，24 帧 chunk 的流水线自回归去噪与 block-causal mask。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2505.13211v1/algorithm_v4.png)

![MAGI-1 Fig. 1: chunk-wise autoregressive denoising with block-causal attention](https://arxiv.org/html/2505.13211v1/algorithm_v4.png)

### 当前挑战

领域长期问题是：大规模视频扩散几乎都在整段上做统一噪声的双向去噪，丢掉时间因果，难以流式、也难以把 T2V / I2V / 续写统一进同一预训练。本文针对的是 **可扩展的 chunk-wise AR 扩散世界模型**，不是 few-step DMD。

- **架构缺口：** 卷积 VAE 在现代 GPU 上慢；标准注意力核难以高效做块因果；超长上下文（文称最多 4M token）需要新的分布式注意力。
- **任务分裂：** 双向模型通常预训练只做 T2V，I2V 要另改结构或微调。
- **推理缺口：** 块与块之间错位、长视频饱和/棋盘伪影、用户短 prompt 与训练长 caption 不匹配。
- **评测立场：** 作者认为产品形态更接近 I2V，因此主客观评测偏 I2V，而不是 T2V 榜。Self Forcing 表里 MAGI-1-4.5B 的 T2V VBench 并不高，两套评测目标不同。

### 研究动机

核心 Insight：**以固定 24 帧（1 s @ 24 FPS）为自回归单元，块内双向、块间因果，噪声时间步沿时间单调递增；T2V / I2V / 续写只是干净块比例不同。** 块尚未完全干净就可以启动下一块，最多四块流水线并行。蒸馏走 shortcut model（可 8/16/32/64 步），不是 CausVid 系 DMD。

与本知识库课题 **直接相关于“视频世界模型”这一自称，间接相关于交互控制**。它提供 chunk-wise 换 prompt、续写和物理基准上的 V2V 优势，但开源权重在后续蒸馏论文的 T2V 实时对比中偏慢。作者把 Physics-IQ 优势部分归因于“自回归促进因果推理”；这是机制解释，实验只证明 V2V 续写分数更高，不能当成因果识别。

### 技术方案

- **输入：** 文本（T5）；可选首帧或前缀视频。Transformer VAE：空间 8×、时间 4× 压缩，潜空间 16 维。
- **过程：** Flow matching；块因果注意力 + 并行空间–时间自注意力与文本交叉注意力 + GQA + QK-Norm + FFN sandwich LN；24B 用 SwiGLU 与 Softcap 调制。4.5B / 24B 三阶段分辨率爬升（4.5B：360p→480p→720p，最长 16 s）。干净块最多加 5% 噪声、不接文本、损失只加在噪声块上。推理用双权重 CFG：\(w_{\text{prev}}=1.5\)、\(w_{\text{text}}=7.5\)，长于约 5 s 时再按 \(t\) 细调，否则饱和。用户 prompt 用 MLLM 增强。蒸馏为 shortcut，最小 \(s=1/64\) 并含 CFG 蒸馏。
- **输出：** 流式视频块；峰值算力/显存与总时长无关。产品页提供在线生成。

与最近 baseline 的实质差异：相对 Sora 类整段双向，生成是因果流水线；相对 CausVid/Self Forcing，这是从零训的大规模 AR 扩散 + shortcut，而不是把 Wan 蒸成 4-step。后续蒸馏论文把它当慢 AR 基线是因为它默认多步。

### 实验结果

**作者主张：** I2V 上运动与语义强，Physics-IQ 上 V2V 大幅领先；24B 证明可扩展。

实验实际支持：

- **VAE（H800，169 条 25 帧 256² 视频）：** PSNR 36.55，解码 12.28 ms，参数 614M；解码快于 OpenSoraPlan / CogVideoX / Hunyuan / StepVideo / Wan2.1 表内实现。
- **VBench-I2V（4 s、24 FPS、16:9）：** Magi-1 2× decoder Total **89.28**，Quality 82.44，I2V Score 96.12，Dynamic Degree **68.21**；1× decoder Total 88.88。作者称当时 leaderboard 第一。对比模型分数来自 leaderboard 汇编，不是全部同代码重跑。
- **内部 I2V 人评（100 对，双盲 Win/Tie/Lose）：** 总体优于开源 Wan-2.1 与 HunyuanVideo、Hailuo i2v-01，略弱于 Kling1.6 HD；指令跟随与运动较好，视觉质量仍落后头部闭源。长度按对手裁成 5–6 s。Fig. 16 为条形比例，正文未给精确百分比表。
- **Physics-IQ：** Magi-1 V2V **56.02** vs VideoPoet V2V 29.50；Magi-1 I2V **30.23** 仍高于表中其他 I2V。V2V 看前 3 s（96 帧 @24 FPS）预测后 5 s。作者展示失败：碰撞后球的停止、火柴点燃气球、撕裂后碎片运动等次级效应不对，但常给出另一套看起来合理的运动。
- **定性：** \(w_{\text{prev}}=1.0\) 时块间错位；过大则静帧。I2V 续写会丢历史速度（笔旋转、遮挡后重现）。

**证据未支持：** T2V 实时 SOTA（Self Forcing 表 4.5B 为 0.19 FPS / 282 s、Total 79.18）；物理直觉等于理解物理定律；开源 4.5B 与论文 24B 评测可互换。

### 总结讨论

MAGI-1 说明：不靠 DMD，单靠大规模 chunk-wise AR 扩散也可以做流式世界模型，并在 I2V 与 V2V 物理续写上拿出硬数字。它与 CausVid 谱系是互补基座：一个提供可蒸馏的开源 1.3B 双向教师（Wan），一个提供原生 AR 的大模型。适用边界是块级（1 s）交互粒度，不是帧级实时。阅读判断：Physics-IQ 的 V2V vs I2V 落差支持“历史运动很重要”，不要写成自回归算法已被证明捕捉因果。开源仓库目前主打推理与权重，完整训练栈/数据不能从论文外完全复现。

### 代码与数据

- **代码 / 权重：** [SandAI-org/MAGI-1](https://github.com/SandAI-org/MAGI-1)；分布式注意力 [SandAI-org/MagiAttention](https://github.com/SandAI-org/MagiAttention)。
- **产品：** [sand.ai](https://sand.ai)。
- **数据：** 多阶段内部策展 + MLLM 过滤/caption；训练语料不随仓库完整公开。

### 局限、失败案例与开放问题

- 开源对照里 4.5B 多步 AR 延迟远高于蒸馏 1.3B 模型。
- 视觉质量在内部人评中仍落后 Kling1.6 HD。
- Physics-IQ 次级碰撞、燃烧、撕裂碎片失败；“合理替代”不是正确物理。
- 长视频必须细调 guidance，否则饱和/棋盘。
- 干净块不接文本，续写时用户文本如何注入需看实现。
- 24B、4M token 的训练基础设施无法从开源推理仓库复现。

---

## 8. LongLive: Real-time Interactive Long Video Generation

**作者：** Shuai Yang, Wei Huang, Ruihang Chu, Yicheng Xiao, Yuyang Zhao, Xianbang Wang, Muyang Li, Enze Xie, Yingcong Chen, Yao Lu, Song Han, Yukang Chen  
**年份与发表：** 2025，arXiv preprint（cs.CV）。arXiv:2509.22622。单位 NVIDIA / MIT / HKUST(GZ) / HKU / THU。尚无 DOI / 正式出版页。arXiv DOI：10.48550/arXiv.2509.22622。  
**可靠入口：** [arXiv](https://arxiv.org/abs/2509.22622)｜[HTML 全文](https://arxiv.org/html/2509.22622)｜[项目页](https://hanlab.mit.edu/projects/longlive)｜[代码](https://github.com/NVlabs/LongLive)｜[模型](https://huggingface.co/Efficient-Large-Model/LongLive-1.3B)｜[AlphaXiv](https://alphaxiv.org/abs/2509.22622)  
**代表图：** LongLive，Fig. 2，短窗注意力 + frame sink，以及 prompt 切换时的 KV-recache。来源：[Fig. 2 原图 PNG](https://arxiv.org/html/2509.22622v1/figures/method.png)

![LongLive Fig. 2: short-window attention, frame sink, and KV-recache](https://arxiv.org/html/2509.22622v1/figures/method.png)

### 当前挑战

CausVid / Self Forcing 能实时短片，但 **分钟级 + 中途换 prompt** 会同时碰到效率与一致性：

- 双向 / Diffusion-Forcing：SkyReels-V2 生成 60 s 约 50 分钟（H100），因为不能 KV cache。
- 因果 AR 多用 train-short–test-long，自生成历史越来越脏，长视频漂移。
- 换 prompt 时：清空 KV 则跳变；保留 KV 则新 prompt 不生效或滞后——旧 prompt 已通过交叉注意力写进 cache。
- 短窗注意力能加速，但丢掉远距线索；先前工作认为 attention sink 挡不住视频长滚动崩坏。

本文针对的是 **交互式长视频的训练–推理对齐与 cache 刷新接口**，不是新的蒸馏理论。

### 研究动机

核心 Insight：**在 Self Forcing 式因果 few-step 模型上，用 KV-recache 在切换点用“已生成帧 + 新 prompt”重算 cache；用 streaming long tuning 按 5 s 片段滚动监督（train-long–test-long）；短窗 + 把第一 chunk 当永久 frame sink。** 作者发现 sink 只有在长滚动崩坏被 streaming tuning 治住之后才有效。这改变的是 cache 与训练时间窗，不是生成器骨干。

与本知识库课题 **间接相关**：Causal Forcing 文中把它列为正交的长视频适配；它支持流式换 prompt，但没有相机/动作条件。可借鉴点是交互时“状态该怎么刷新”。

### 技术方案

- **输入：** 顺序文本 prompt；骨干 Wan2.1-T2V-1.3B，先 Self Forcing DMD 改成因果 few-step，并打开短窗与 frame sink。
- **过程：** Streaming long tuning：每步只生成并 DMD 监督下一段 5 s，历史 KV detach；序列最长 60 s，每 batch 恰好一次 prompt 切换（5–55 s 均匀采样）。切换时 recache 一次，teacher（Wan-14B）也看新 prompt。短窗约 9 latent 帧，sink 为第一 chunk 的 3 latent 帧。LoRA rank 256（约 27% 参数，350M）。64×H100 约 12 小时，合计约 32 GPU-day。也实现了线性注意力骨干 SANA-Video。
- **输出：** 流式长视频；H100 上 20.7 FPS；单卡最长演示 240 s。INT8 PTQ 后模型 1.4 GB，5090 上 16.4 FPS。

与最近 baseline 的实质差异：相对 Self Forcing，训练看到自己的长程脏上下文，并且专门训切换；相对 MAGI-1 的手动调 KV 窗换 prompt，recache 是一次前向重写。SkyReels-V2 不能比实时。

### 实验结果

**作者主张：** 短片质量不掉、长片与交互长片领先，同时最快。

实验实际支持：

- **短片 VBench：** Total/Quality/Semantic **84.87 / 86.97 / 76.47**，20.7 FPS。Quality 高于 Self Forcing chunk-wise（85.07），Semantic **低于** SF 的 81.28。速度得益于短窗。
- **单 prompt 30 s VBench-Long：** Total **83.52** vs Self-Forcing 81.59、FramePack 81.95、SkyReels-V2 75.29；吞吐 20.7 vs 17.0 / 0.92 / 0.49。FramePack 是 I2V，需先合成首帧。
- **交互 60 s（自建 160 条，每条 6×10 s prompt）：** Quality 84.38 vs SF 82.46、SkyReels 80.49。分段 CLIP 在 0–10 s 到 50–60 s 上全程高于两对照（末段 24.32 vs SF 23.19）。这不是官方 VBench 交互协议。
- **KV-recache 消融（10 s、5 s 切换）：** recache 的 Background/Subject/CLIP = 94.81 / 94.04 / 27.87；清 cache 92.75 / 89.59 / 28.95（语义略高但一致性差）；留 cache 94.77 / 93.69 / 25.92（跟不住新 prompt）。
- **窗与 sink：** 一致性随窗长上升，约 24 帧饱和；9 local + 3 sink 接近 21 帧窗的一致性，端到端时间 −28%、峰值显存 −17%（H100）。
- **LoRA：** rank 256 的 30 s Total 83.12，接近全量微调 83.52；rank 32 仅 81.08。
- **INT8：** VBench Total 84.31 vs BF16 84.87。
- **用户研究：** 48 题 × 26 有效问卷，四维二选一；正文未给胜率表，细节在附录。

**证据未支持：** Semantic 全面超过 Self Forcing；240 s 有完整 VBench；质量上限超过 Wan 基座（作者在局限中明确否定）。

### 总结讨论

LongLive 把实时 AR 视频从 5 s 推到可交互的分钟级：recache 处理提示词切换，streaming tuning 处理自生成历史，sink 让短窗不丢身份。短片 Semantic 下降、长片/交互上升，符合“为长程与切换做了特化”的阅读。适用边界是文本交互长视频，不是动作世界模型。失败来自基座上限和无真实长视频监督。阅读判断：适合作为 CausVid 谱系的长程插件；不要把 20.7 FPS 写成已含复杂 3D 控制。

### 代码与数据

- **代码：** [NVlabs/LongLive](https://github.com/NVlabs/LongLive)，含训练与推理。
- **权重：** Hugging Face `Efficient-Large-Model/LongLive-1.3B`。
- **数据：** 无额外真实视频；prompt 来自 VidProM + Qwen2-72B 写下一镜。作者强调未引入新的外部视频集。

### 局限、失败案例与开放问题

- 自监督微调不能修正基座系统性偏差；短片段质量很难超过 teacher。
- 训练每条长序列只插一次切换，推理多段切换是外推。
- 交互评测是自建 160 条，CLIP 不等于人类叙事连贯。
- 短片 Semantic 低于 Self Forcing，存在长程特化的代价。
- 240 s 主要是展示，缺少与 60 s 同协议的完整表。
- 依赖 Wan 与 14B teacher，完整蒸馏链仍重。

---

## 9. LongLive-2.0: An NVFP4 Parallel Infrastructure for Long Video Generation

**作者：** Yukang Chen, Luozhou Wang, Wei Huang, Shuai Yang, Bohan Zhang, Yicheng Xiao, Ruihang Chu, Weian Mao, Qixin Hu, Shaoteng Liu, Yuyang Zhao, Huizi Mao, Ying-Cong Chen, Enze Xie, Xiaojuan Qi, Song Han
**年份与发表：** 2026，arXiv preprint（cs.CV / cs.DC，v2）。Yukang Chen、Luozhou Wang、Wei Huang、Shuai Yang 为共同一作；NVIDIA。arXiv:2605.18739；arXiv DOI：10.48550/arXiv.2605.18739。尚无正式会议或期刊页。
**可靠入口：** [arXiv](https://arxiv.org/abs/2605.18739)｜[HTML 全文](https://arxiv.org/html/2605.18739)｜[项目页](https://nvlabs.github.io/LongLive/LongLive2/)｜[代码](https://github.com/NVlabs/LongLive)｜[文档](https://nvlabs.github.io/LongLive/LongLive2/docs/)｜[AlphaXiv](https://alphaxiv.org/abs/2605.18739)
**代表图：** LongLive-2.0，Fig. 1，训练侧 Balanced SP / NVFP4 / few-step LoRA 与推理侧 W4A4、KV 量化、异步 VAE 的全链路。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2605.18739v2/fig1-overall.png)

![LongLive-2.0 Fig. 1: end-to-end NVFP4 training and inference infrastructure](https://arxiv.org/html/2605.18739v2/fig1-overall.png)

### 当前挑战

LongLive 1.0 已能分钟级流式生成，但其算法链仍是“ODE 初始化 → DMD → streaming long tuning”，基座只有 1.3B；长序列训练会被视频 token、VAE 编码和 teacher-forcing mask 的显存/通信成本卡住，推理还要同时承担 DiT、不断增长的 KV cache 和 VAE 解码。本文针对的不是新的 DMD 理论，而是：**如何把 5B、720p、multi-shot 长视频的训练与端到端推理共同扩展到实时。**

- 常规 sequence parallel 只均分 token，没有利用 AR teacher forcing 中“干净历史 + 加噪目标块”的结构，容易负载不均或需要复杂 mask。
- 只量化 DiT 权重不足以解决长视频 KV cache；只报 denoiser FPS 也会掩盖 VAE 解码空转。
- Blackwell 有 NVFP4 Tensor Core，A100/H100 没有同等原生 W4A4 加速；硬件口径必须分开。
- 算法侧，作者认为高质量长视频数据与基础设施足够时，可以直接把双向模型 TF 微调成 long multi-shot AR，而不必把 ODE/DMD/long tuning 全串进主模型训练。

### 研究动机

核心 Insight：**把 AR 数据布局、sequence parallel、4-bit 数值格式和流式解码作为一个系统共同设计。** Balanced SP 在每个 rank 上配对 clean-history 与 noisy-target temporal chunks，使 teacher-forcing mask 自然落在本地布局；训练线性层使用 NVFP4，并让 reduction、normalization statistics、optimizer states 等敏感操作保留高精度。推理则同时做 W4A4 model、NVFP4 KV cache、并行 KV 解量化和异步 streaming VAE。

算法上另一个重要变化是 **clean pipeline**：直接在真实 long multi-shot 数据上把 Wan2.2-TI2V-5B 调成 AR；实时 4/3/2-step 能力以独立 DMD LoRA 叠加，不污染主 AR checkpoint。与本知识库课题 **直接相关于部署与长程状态接口，间接相关于世界模型**：它支持 T2V/I2V、多镜头和交互 prompt，不提供相机动作或物理干预控制。

### 技术方案

- **输入：** 长单镜头或多镜头视频、shot-level prompts；骨干 Wan2.2-TI2V-5B，支持 T2V / I2V，目标分辨率最高 1280×720。训练按时间 chunk 拆成干净历史和当前加噪目标。
- **过程：** Balanced sequence parallel 将成对 chunks 分发到各 rank，并用 SP-aware chunked VAE encoding 控制峰值显存；主模型直接做长视频 teacher-forcing AR 微调，可使用 BF16 或 end-to-end NVFP4。少步阶段以 standalone LoRA 做 DMD，teacher/student/real-score 同步到 W4A4。推理将线性层权重与激活量化为 NVFP4，KV cache 以 chunk 为单位量化（论文给出的存储式从约 \(4T_cHd\) bytes 降到 \(9T_cHd/8\)，实测约 3.6× 压缩），sink-token 滑窗内用定制 CUDA 并行解量化；VAE 在独立 stream 上边生成边解码。非 Blackwell 用多卡 SP inference 替代原生 NVFP4 加速。
- **输出：** 720p 流式、可多次切换 prompt 的长视频；主模型可叠加 4/3/2-step LoRA，在 GB200 NVL72 的论文口径下最高 45.7 FPS 端到端吞吐。

相对 LongLive 1.0，2.0 更换为 5B Wan2.2 基座、引入真实 multi-shot 数据与 shot-level attention sink，并把量化/并行覆盖训练、蒸馏、KV 和 VAE；相对 Self/Causal Forcing，主 AR 模型不需要 ODE 初始化，DMD 只负责独立的实时 LoRA。

### 实验结果

**作者主张：** 这是首个面向长视频生成的 end-to-end NVFP4 训练与推理系统，训练最高加速约 2.15×，推理最高约 1.84×，5B 模型达到 45.7 FPS。

实验实际支持：

- **公开模型总表：** BF16 LongLive-2.0-5B 为 **24.8 FPS / VBench 85.06**；NVFP4 4-step 为 **29.7 FPS / 84.51**；NVFP4 2-step 为 **45.7 FPS / 83.14**。LongLive-1.3B 为 20.7 FPS / 84.87。速度提升伴随 VBench 下降，2-step 不是免费加速。
- **步数–速度：** 3-step 35.2 FPS，2-step 45.7 FPS；论文称相对既有方法最高约 2×。这些是 1280×720、Blackwell 集群与其端到端 pipeline 的特定口径，不能写成单卡 45.7 FPS。
- **训练基础设施：** 随视频长度增加，GEMM 占比上升，NVFP4 收益更明显；Balanced SP + NVFP4 在论文设置中给出最高 **2.15×** 加速，并降低峰值显存。需按各表的 GPU 数与视频长度比较，不能把峰值倍数视为所有配置恒定值。
- **60 s 长视频（MovieGenBench prompts + VBench-Long，4-step）：** LongLive-2.0 在比较方法中平均 rank 最好；NVFP4 的 Subject Consistency **97.62** 最优，BF16 的 Background Consistency **97.00** 最优。量化与 BF16 各胜不同维度，并非 NVFP4 全轴更高。
- **推理部件消融：** W4A4、NVFP4 KV、并行解量化与异步 VAE 共同形成最高约 **1.84×** 端到端加速；KV 存储约 3.6× 压缩。作者明确强调 end-to-end FPS，不只统计 DiT。

**证据未支持：** GB200 上的 NVFP4 加速可原样迁移到 H100/A100；VBench 83.14 的 2-step 模型质量优于 4-step/BF16；多镜头 benchmark 已覆盖叙事一致性与剪辑质量；“clean pipeline”说明 DMD 不再有用——论文仍用 DMD 训练实时 LoRA。

### 总结讨论

LongLive-2.0 的贡献是算法–基础设施收口，而不是替代 LongLive 1.0 的三项算法 Insight。1.0 解决 train-long–test-long、KV-recache 与 frame sink；2.0 解决 5B 长视频怎样训练、怎样把少步蒸馏以 LoRA 插拔、怎样让 4-bit model/KV 与 VAE 真正端到端跑快。它还给出一个重要谱系修正：主 AR 能力可以由高质量长视频 TF 直接得到，ODE/DMD 不必承担所有能力迁移；但实时化仍使用 DMD。阅读判断：适合作为“长视频生成系统层”的收尾卡片；不能把 NVFP4 吞吐写成新的生成建模定律，也不能把 prompt 交互等同动作世界模型。

### 代码与数据

- **代码：** [NVlabs/LongLive](https://github.com/NVlabs/LongLive)，main 分支为 2.0，1.0 保留在 `v1.0` 分支；仓库声明 Apache-2.0。
- **模型：** 仓库/项目页提供 LongLive-2.0-5B、NVFP4 4-step / 2-step 等权重入口；以 release 页面实际文件为准。
- **数据：** 论文使用长单镜头与 multi-shot 策展数据，具体语料规模、来源与可再分发性需按论文附录/仓库数据说明核对；完整训练集并非由代码仓库自动提供。
- **实现边界：** NVFP4 路径依赖 Transformer Engine、定制 CUDA/Triton kernel 与 Blackwell；非 Blackwell 文档走 sequence-parallel 推理。

### 局限、失败案例与开放问题

- NVFP4 的实质加速依赖 Blackwell Tensor Cores；H100/A100 只能用 SP 等替代路线。
- 2-step 45.7 FPS 的 VBench 低于 4-step 与 BF16，速度–质量权衡明确存在。
- 多镜头和 prompt 切换仍是文本接口，没有相机/动作控制与闭环环境反馈。
- 真实 long multi-shot 数据质量是 clean pipeline 成立的重要前提，数据不完整公开会影响复现。
- 系统包含量化、SP、LoRA、KV kernel、异步 VAE，多部件组合使跨硬件公平复现困难。
- 60 s 指标与演示不能证明任意时长无漂移；长程叙事和镜头转场仍缺统一标准。

---

## 10. minWM: A Full-Stack Open-Source Framework for Real-Time Interactive Video World Models

**作者：** Min Zhao, Hongzhou Zhu, Bokai Yan, Zihan Zhou, Yimin Chen, Wenqiang Sun, Kaiwen Zheng, Guande He, Xiao Yang, Chongxuan Li, Fan Bao, Jun Zhu  
**年份与发表：** 2026，arXiv preprint。arXiv:2605.30263。Min Zhao 为项目负责人；Hongzhou Zhu、Bokai Yan、Zihan Zhou、Yimin Chen 共同一作；Fan Bao / Jun Zhu 为顾问。生数 / 清华 / 人大 / HKUST / UT Austin。尚无 DOI / 正式出版页。  
**可靠入口：** [arXiv](https://arxiv.org/abs/2605.30263)｜[HTML 全文](https://arxiv.org/html/2605.30263)｜[代码 / 项目](https://github.com/shengshu-ai/minWM)｜[AlphaXiv](https://alphaxiv.org/abs/2605.30263)  
**代表图：** minWM，Fig. 1，从 T2V/TI2V 基础模型到相机可控 few-step AR 世界模型的全栈流程。来源：[Fig. 1 原图 PNG](https://arxiv.org/html/2605.30263v1/paper_pipeline.png)

![minWM Fig. 1: full-stack conversion from bidirectional T2V to camera-controllable few-step AR world models](https://arxiv.org/html/2605.30263v1/paper_pipeline.png)

### 当前挑战

作者认为缺的不是又一篇蒸馏论文，而是 **可复现的全栈**：数据、可控微调、AR 训练、少步蒸馏、流式推理散落在不同仓库。交互世界模型还要求因果 rollout、相机（或其它动作）可控、延迟够低。

本文针对的工程缺口：

- 把 Wan2.1-T2V-1.3B（交叉注意力条件）和 HY1.5-TI2V-8B（MMDiT）两条异构骨干接到同一配方。
- 也可把已有世界模型（HY-WorldPlay）迁到新数据/新延迟。
- 需要可操作的训练经验：轨迹质量、可控性步数、最小 batch。

它 **没有** 提出新的蒸馏理论，明确复用 Causal Forcing / Causal Forcing++。

### 研究动机

核心 Insight：**先把双向基础模型微调成相机可控（PRoPE 把相对投影变换写进注意力），再把 CF/CF++ 的三阶段全部换成带相机条件的版本。** 改变的是控制接口与可复现性，不是新的生成损失。与本知识库课题 **直接相关**：这是开源实时视频世界模型配方，动作目前主要是相机轨迹，不是关节/操作 WAM，也不是反事实。

### 技术方案

- **输入：** 文本，以及每帧相机内参 \(K_i\) 与 world-to-camera \(T_i^{cw}\)；可选图像（TI2V）。输出设定 480×832、77 帧，AR chunk = 4 latent 帧，蒸馏 4 步。
- **过程：** PRoPE 构造 \(4\times 4\) 提升投影矩阵，按 GTA 形式注入自注意力，使 token 对依赖相对位姿。然后 Stage 1 TF AR、Stage 2 因果 ODE 或因果 CD、Stage 3 不对称 DMD；student / \(s_{\text{real}}\) / \(s_{\text{fake}}\) 自 rollout 都吃同一相机条件。HY1.5：batch 32、lr \(1\times 10^{-5}\)，双向 8K → AR 4K → Stage2 1.5K → DMD 500（8K 权重作 Stage 3 score，Stage 1 从 5K 初始化）。Wan2.1：lr \(2\times 10^{-6}\)，双向 5K → 4K → 2K → 200。
- **输出：** 相机可控的 few-step AR 视频。A800、不含 VAE 的首帧延迟：HY1.5 few-step AR **3.446 s**（相对多步双向 771 s，约 \(224\times\)）；Wan2.1 few-step AR **1.137 s**（相对 269 s，约 \(237\times\)）。

与最近 baseline 的实质差异：相对 Causal Forcing++ 论文里的定性相机 demo，这里给出两条骨干的可运行脚本、分阶段 checkpoint 和数据消融；相对 HY-WorldPlay，强调可迁移而非从零宣称新 SOTA 质量。

### 实验结果

**作者主张：** 全栈可复现；few-step AR 大幅降低首帧延迟且保住相机可控。

实验实际支持：

- **延迟表：** 见上。多步 AR 已有约 9.4–9.5× 加速，few-step 再降一个数量级。这是架构（先出首帧）+ 蒸馏的共同结果，不是单点算法奇迹。
- **定性：** Fig. 2 显示蒸馏后仍能切换相机动作。
- **数据消融：** 当前设定下 SpatialVid 的感知估计位姿 **未能** 学到可靠相机控制（过滤后仍差）。DL3DV 重建再按指定轨迹渲染，或 OpenVid 图像 + WorldPlay 生成轨迹，可以学会。作者把前者失败解释为位姿噪声假说，并写明 **不能** 据此断言 SpatialVid 不适合该任务。
- **步数（HY1.5）：** 1–2K 步基本不可控；约 5K 开始有响应但不稳；8K 较强。
- **Batch（Wan2.1）：** <4 经常学不会；8 改善但不稳；16 可跑通且可控性高。主实验 batch 32。

**无的实验：** 没有 VBench / VisionReward / 轨迹误差表；没有与 Genie 3、WorldPlay、Matrix-Game 的公平质量对比；没有非相机动作。禁止把延迟加速写成质量 SOTA。

### 总结讨论

minWM 是 Causal Forcing 谱系的工程收口：异构骨干、分阶段权重、以及“估计位姿不够、GT 或生成 GT 才够”的训练经验。它证明配方可以接到世界模型控制，而不是证明学到了物理因果。适用边界是相机轨迹控制的实时视频世界模型原型。失败案例被作者写进消融：SpatialVid、过小 batch、过少微调步。阅读判断：若课题要复现 Genie 3 风格的开源相机世界模型，应优先跟这个仓库；若课题要操作 WAM 或反事实，它只提供流式生成后端，不提供动作语义。

### 代码与数据

- **代码：** [shengshu-ai/minWM](https://github.com/shengshu-ai/minWM)，README 称 full-stack tutorial 而非单一模型；含脚本、checkpoint、文档、推理。GitHub 记技术报告于 2026-05-29 发布。
- **开源数据策略：** OpenVid 等图像 + WorldPlay 生成带指定轨迹的视频。论文内部还用过 DL3DV 渲染。
- **许可 / 权重完整性：** 以仓库为准，本次未逐文件核验所有 stage 的权重是否齐全。

### 局限、失败案例与开放问题

- 没有标准视频质量榜，无法与 CF++ T2V 数字横比世界模型质量。
- SpatialVid 失败只是当前设定的负结果。
- 控制信号目前主要是相机；作者把 pose 等列为未来。
- 延迟不含 VAE；HY1.5 的 3.4 s 首帧对“实时游戏”仍偏慢。
- chunk=4 latent、4-step，未展示 CF++ 的 frame-wise 2-step 世界模型。
- 依赖 WorldPlay 生成轨迹时，教师模型偏差会进入“GT”。
