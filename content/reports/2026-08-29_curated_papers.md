# ViDiHand：视频扩散表征用于第一视角 4D 双手运动重建

**报告标签**：4D hand reconstruction, egocentric vision, hand-object interaction, video diffusion model, diffusion features, MANO, embodied AI

本报告核验用户给出的 arXiv:2606.30308。阅读范围包括 arXiv v2 正文及补充材料、作者项目页和官方代码仓库；不是仅据摘要。论文 PDF 的本地下载因连接被重置未完成，但 arXiv 官方 HTML 全文可访问并覆盖方法、实验、消融、补充评测和作者局限。检索与核对日期：2026-08-29。

## 1. The Surprising Effectiveness of Video Diffusion Models for Hand Motion Reconstruction

**作者：** Yuxi Wang, Chengkai Jin, Yufei Liu, Wenqi Ouyang, Tianyi Wei, Zhiwei Zeng, Siyuan Huang, Zhiqi Shen, Xingang Pan  
**年份与发表：** 2026，arXiv preprint（cs.CV，v1 提交于 2026-06-29，v2 修订于 2026-07-09）；尚未核验正式会议或期刊录用。arXiv:2606.30308；arXiv DOI：10.48550/arXiv.2606.30308  
**可靠入口：** [arXiv](https://arxiv.org/abs/2606.30308)｜[HTML 全文 v2](https://arxiv.org/html/2606.30308v2)｜[DOI](https://doi.org/10.48550/arXiv.2606.30308)｜[项目](https://vidihand.github.io/)｜[官方代码仓库](https://github.com/NTUYWANG103/ViDiHand)｜[Hugging Face Papers](https://huggingface.co/papers/2606.30308)｜[AlphaXiv](https://alphaxiv.org/abs/2606.30308)  
**类别标签：** 4D hand reconstruction, egocentric vision, two-hand pose, hand-object interaction, video diffusion model, diffusion features, MANO, embodied AI

### 当前挑战

第一视角 4D 手部重建在真实交互中经常遇到手—物体、手—手遮挡、视野边缘截断、运动模糊和鱼眼畸变。逐帧图像方法依赖上游手部检测器，重遮挡下检测漏失会直接变成整帧重建缺失；已有视频方法虽然加入跨帧注意力或 3D 手轨迹 infiller，却主要从稀缺的手姿态标注学习时间先验，且常把手轨迹与物体和场景上下文分开建模。本文针对的具体缺口是：能否直接复用大规模视频生成模型内部已经形成的运动、几何、遮挡与交互表征，在不使用检测器、运动补全器或测试时优化的情况下恢复连续双手轨迹。

### 研究动机

作者主张，大规模视频扩散模型为了生成时空一致的视频，必须隐式处理与 4D 手部重建相似的三类问题：遮挡内容推断、跨帧身份与空间位置稳定、以及平滑运动。因此 ViDiHand 不把生成模型只当冻结特征提取器，而用 hand-overlay rendering 使其表征对 MANO 手部几何敏感，同时冻结 base DiT 以尽量保留原有世界先验。阅读者判断：实验支持“视频预训练表征比随机初始化和所测图像骨干更适合该任务”，但“内部维持 3D 状态”仍是基于任务表现和可视化的机制解释，论文没有直接识别出可解释、可干预的三维状态变量。

### 技术方案

- **输入：** 81 帧第一视角 RGB 视频片段、每段相机内参；训练阶段另使用 EgoDex 的 2D 关节监督，以及 ARCTIC、HOT3D 的 MANO/相机空间手部标注。
- **过程：** 以 1.3B 参数 Wan2.1-VACE 为骨干，仅微调 VACE 分支、冻结 base DiT。Stage 1a 让模型把 2D 关节骨架半透明叠加到原视频，Stage 1b 改为 MANO 网格叠加，并以 flow-matching 学习贯穿遮挡帧的 overlay rendering。随后固定扩散骨干，从第 15 个 DiT block、归一化去噪步约 0.7 的单层激活读取 21 个 latent-frame 特征。双分支解码器用固定左右手 slot 的 hand-token branch 回归整体 MANO 姿态，用 joint-heatmap branch 定位逐关节 2D anchor；双方经 mutual cross-attention 融合。mixed-projection head 回归深度，以相机内参、MANO 关节和 2D anchor 加权最小二乘闭式求解平面内平移。解码器联合优化 MANO、相机、图像重投影、可见性与时间平滑损失。
- **输出：** 每一视频帧中左右手的 on-screen 概率、MANO 全局朝向、15 个关节旋转、10 维形状、相机坐标系三维平移与关节/网格轨迹，即 metric-scale 4D 双手重建。

### 实验结果

实验在 ARCTIC、HOT3D 和 HOI4D 上比较 8 个基线，包括 HaMeR、WiLoR、Hamba、InterWild、WildHands、OmniHands、Dyn-HaMR 和 HaWoR。ARCTIC 与 HOT3D 属于显式训练分布内评测；HOT3D 因官方 test 无 MANO 真值，作者随机留出 validation sequence 的 5% 作 test。HOI4D 不进入任何方法的显式监督训练，但 Wan 视频骨干的互联网预训练语料不可审计，因此只能称“未显式监督见过”，不能证明完全无数据暴露。

作者采用 coverage-aware `-p` 指标：检测到的真阳性使用实际误差，漏检手则以确定性的 canonical MANO 占位误差计入，避免只在容易检测的手上报告 MPJPE。主表中 ViDiHand 在 27 项指标的 26 项排名第一：ARCTIC 的 FAcc 为 0.997（WiLoR 0.919），MPJPE-p / PA-MPJPE-p 为 21.668 / 9.821 mm，EPE-p 为 12.407 px，jitter 为 3.183 mm/frame²；HOT3D 为 FAcc 0.948、MPJPE-p 21.514 mm、jitter 3.741；HOI4D 为 FAcc 0.984、MPJPE-p 30.090 mm、jitter 4.010，并在 9 项中领先 8 项。HOI4D 唯一未领先的是 camera-translation error，ViDiHand 的 CT-p 为 0.117 m，WiLoR 和 OmniHands 分别为 0.115 / 0.108 m。

消融事实支持几个局部设计判断：在所测层中第 15 层的 MPJPE-p / EPE-p 为 20.59 mm / 11.93 px，优于第 8、22、29 层；去噪步约 0.7 在 FAcc、MPJPE-p、EPE-p 上最优，但 jitter 与其他步几乎持平。随机初始化、DINOv3、预训练 T2V、未适配 VACE、mesh overlay、joint+mesh overlay 的 ARCTIC MPJPE-p 依次为 36.39、24.46、21.64、22.67、21.23、20.59 mm，说明视频预训练与 overlay 适配均有贡献。去掉 joint-heatmap 或 mixed-projection 会令 EPE-p 从 11.93 升至 14.91 / 16.26 px；但去掉 mixed-projection 反而把 MPJPE-p 和 jitter 略降到 20.26 和 2.86，说明完整配置是检测覆盖与 2D 定位的折中，并非每一列都最优。

补充材料在“双方都成功检测同一只手”的成对协议下报告 ViDiHand 赢得 120 个比较单元中的 96 个；同时明确指出，在 Procrustes 对齐后的局部关节精度、HOI4D 的 2D 重投影及相机平移上，若只看共同检出的手，若干专用单帧或 SLAM 方法仍可匹配或超过 ViDiHand。故主结果强力支持端到端覆盖、绝对姿态和时间稳定性优势，但不支持其在所有局部 articulation 或跨域相机平移指标上无条件占优。

### 总结讨论

ViDiHand 的核心贡献是把视频扩散模型从生成器改造成 4D 双手重建的表征骨干：overlay 预任务把中间特征对齐到手部几何，双分支解码器把整体 MANO articulation 与局部 2D 定位分开建模，再用显式投影几何组合成 metric-scale 轨迹。相较依赖检测器、手部专用时间模块、SLAM 或测试时优化的管线，它在重遮挡和跨帧稳定性上的结果有充分实验支撑。

对知域方向而言，该工作直接连接 egocentric HOI、4D hand reconstruction 与 video/world prior，可作为从生成模型内部表征提取结构化状态的代表案例。不可扩大之处有两点：其一，作者所称 world prior 是大规模视频预训练得到的统计表征，不等于结构因果模型、干预推断或反事实能力；其二，HOI4D 只保证未用于显式监督，不能排除互联网预训练数据泄漏。当前系统更适合作为离线伪标注器，而非实时闭环机器人感知模块。

### 代码与数据

官方 GitHub 仓库存在并自称 PyTorch 实现，但截至本次核验，README 明确写有 “Code will be released soon”，仓库页面仅显示 README，未见可运行训练/推理代码、权重、环境文件或许可证，因此尚不能复现。论文使用公开的 EgoDex、ARCTIC、HOT3D 和 HOI4D；并未发布新的完整训练数据集。Wan2.1-VACE 的原始预训练语料不可审计，完整数据许可和潜在 benchmark 暴露无法核验。

### 局限、失败案例与开放问题

- 作者报告推理速度仅 5.5 fps，且使用 4 张 A100 GPU；当前定位是离线标注工具，不满足实时闭环控制。
- 方法仍依赖姿态标注视频；Stage 1a 可使用关节级弱标注，但并未实现完全无标注适配。
- HOI4D 仅从显式监督中留出，互联网规模视频骨干的训练语料不可审计，跨数据集结果存在无法排除的暴露风险。
- 覆盖感知主指标把漏检转成 canonical placeholder；它更接近端到端可用性，但与只评共同检出手的传统误差衡量不同，引用排名时必须说明协议。
- 在共同检出手上，部分基线于局部 articulation、2D 重投影或跨域相机平移仍有优势；完整解码器也不是 MPJPE 和 jitter 两列的消融最优项。
- 论文定性结果仍有基线漏手、错手性和幻觉第二只手等案例；ViDiHand 的极端域外失败分布、置信度校准和错误恢复没有系统量化。
- 官方实现、权重和许可证尚未发布；训练成本、数据处理流水线与随机种子复现实验均待核验。
- 作者把多视角、弱标签扩展和全身运动重建列为未来方向；蒸馏、少步或自回归生成骨干能否保留当前精度也仍是开放问题。
