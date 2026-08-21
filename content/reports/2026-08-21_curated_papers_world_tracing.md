# World Tracing：像素对齐的生成式多层几何

**报告标签**：3D/4D, 生成式几何, 单目三维重建, 动态几何, 扩散模型  
**检索与核对日期：2026-08-21**  
**阅读范围：** 已核对 arXiv v1 HTML 全文、技术附录、官方项目页、官方 GitHub 推理代码仓库与其公开权重说明，不是仅据摘要。当前仅见 World Labs Technical Report / arXiv 预印本，未发现正式会议或期刊版本。

> 阅读总判断：World Tracing 的核心贡献不是把单目深度估计再做大，而是把“可见表面重建”和“遮挡后几何生成”统一为输入像素射线上的有序多层相机坐标点。公开实验支持它在作者设定的对象、场景与短动态片段上兼顾像素对齐和几何完整性；但 best-of-8 选样、内部场景测试集、合成深度剥离监督和固定六层表示限制了结论外推。

---

## 1. World Tracing: Generative Pixel-Aligned Geometry Beyond the Visible

**作者：** Hao Zhang, Mohamed El Banani, Jen-Hao Cheng, Paul Zhang, Yi Hua, Ben Mildenhall, Christoph Lassner, Narendra Ahuja, Gengshan Yang  
**年份与发表：** 2026，World Labs Technical Report；arXiv:2606.13652v1（cs.CV，交叉列于 cs.GR，2026-06-11 提交）。未发现正式会议/期刊版本；DOI `10.48550/arXiv.2606.13652` 是 arXiv/DataCite DOI，不代表同行评审出版。  
**类别标签：** 3D/4D、生成式几何、单目三维重建、分层深度、点图、流匹配、动态场景  
**可靠入口：** [arXiv](https://arxiv.org/abs/2606.13652)｜[HTML 全文](https://arxiv.org/html/2606.13652v1)｜[DOI](https://doi.org/10.48550/arXiv.2606.13652)｜[项目页](https://haoz19.github.io/world-tracing-page/)｜[官方代码](https://github.com/haoz19/world-tracing)｜[对象模型权重](https://huggingface.co/haoz19/object-model-6layer)｜[在线演示](https://huggingface.co/spaces/haoz19/world-tracing-demo)｜[AlphaXiv](https://alphaxiv.org/abs/2606.13652)

### 当前挑战

**领域长期挑战。** 单张图像到三维存在不可消除的遮挡歧义：观测只约束第一可见表面，背面、被前景遮住的物体和视锥外结构只能依赖先验生成。已有两条路线各自牺牲一端：单目深度/pointmap 方法逐像素对齐、能忠实恢复可见表面，却天然每条射线只给一个点；image-to-3D 生成器能补出完整物体，但通常在规范坐标系生成，可能改变输入中的姿态、前后关系或局部轮廓，后续还要做相机与物体配准。

**本文针对的具体缺口。** 作者要同时保留相机坐标中的像素—三维对应和遮挡后完整几何。最近的分层表示 LaRI / DualPM 虽允许一条射线有多个交点，但回归式深度加逐层有效性 mask 会遭遇两类失败：不可见背面是多模态的，点回归易平均成平滑形状；越深层有效像素越稀疏，本文对象渲染统计从 L0 平均 8.14% 降至 L5 的 0.60%，mask 分类容易塌缩为“无效”。场景和动态方法还常使用不同表示，难以共享同一接口。

评测层面也有长期缺口：视觉上“像真的”mesh/video 指标未必衡量其是否忠实于输入。本文因此以可见深度误差、Chamfer distance 和 F-score 为主，而不是只报美学质量。不过，作者使用随机生成方法 best-of-8 结果，且有 200 个内部场景样本，仍不是完全无选择偏差、完全公开的统一比较。

### 研究动机

**作者明确主张：** 下游三维编辑、视角变化视频和纹理 mesh 生成真正需要的是相机坐标中既忠实又完整的几何，而不是彼此分离的 depth map 与 canonical asset。核心 Insight 是把每个输入像素对应的相机射线表示为由近到远的 (L) 个三维交点：L0 是可见表面，L1–L5 是后续遮挡表面。于是“重建”与“生成”成为同一个 (L\times H\times W\times3) 张量中的不同层，像素对应由表示本身保证。

这一选择同时改变了三个接口：

- **表征接口：** 从每像素一个深度/点或规范坐标 mesh，改成相机坐标、多层、像素对齐 XYZ pointmaps；无需把相机内参作为输入，必要时可从 L0 的像素—点对应闭式拟合自洽内参。
- **监督接口：** 对没有第 (L) 个真实交点的射线，用最近的前一有效交点前向填充，取消逐层有效性分类头；单层 RGB-D 样本则只打开 L0 loss mask，使同一架构可混合单层和多层监督。
- **生成信号：** 用直接作用于 XYZ 像素空间的 flow matching 表达不可见几何的多模态分布，并用混合 timestep 日程分别照顾近似重建的 L0 与更偏生成的深层。

与本知识库 3D/4D 世界建模课题直接相关之处，是它提供了可供编辑、视频新视角和动态几何共享的显式世界状态接口。**阅读者推断：** 该接口可能比单层深度更适合作为生成式世界模型的几何记忆；但论文没有因果干预、反事实识别或长期交互实验，不能据此把 World Tracing 称为因果世界模型。

### 技术方案

- **输入：** 静态对象/场景版本接收一张 RGBA 图像（场景中 alpha 用于屏蔽天空等无限深度区域）；动态版本接收短单目视频。模型不要求相机内参作为输入。
- **过程：** 冻结的 MoGe ViT-L 从图像提取像素对齐特征；含噪的六层 XYZ 张量按 (14\times14) patch 转成逐层 geometry tokens，与对应图像 token 在像素位置上融合。WT-DiT 交替使用层内二维注意力、同射线跨层注意力和全局注意力，并用 layer FiLM 区分层序；WT-D 在全局块后增加时间注意力。训练先用 depth peeling 从三维资产渲染每条射线的前六个交点，缺失深层以前向填充变密；XYZ 经对象 z-score 或场景 median + signed-log 归一化后做 (x_0)-parameterized flow matching，并加入软相邻层单调约束。推理从高斯噪声出发，用 20 个 ODE 步得到多层点图。
- **输出：** (X\in\mathbb{R}^{L\times H\times W\times3}) 的相机坐标多层 XYZ pointmaps（默认 (L=6)）；L0 对应输入可见表面，更深层给出沿相同像素射线的遮挡几何。公开模型本身不预测颜色或逐层可见性，颜色从输入 RGB 采样，alpha 作为各层共同有效域。

三个变体共用表示和主要目标：WT-O 处理静态对象，WT-S 处理静态场景，WT-D 从 WT-O 微调并加入时间注意力处理动态对象。主模型为约 1.7B 参数（1.4B 可训练）、504×504、六层；论文以 64 张 H100、全局 batch 512 训练，WT-D 再从对象 checkpoint 微调。

与最近 baseline 的实质差异是：相对 MoGe-2 / VGGT / Pi3X，它从单可见点扩展到同射线多交点；相对 LaRI，它用生成式 flow matching 和稠密 depth-filling 目标，去掉稀疏 mask head；相对 TRELLIS.2 / SAM 3D 等规范坐标生成器，它把输入相机帧和像素对应保留为原生坐标；相对动态 GVFDiffusion / SS4D / ActionMesh，它保持相同的逐像素多层目标，仅额外加入时间耦合。

### 实验结果

**数据与划分。** 训练多层数据包括约 30 万个公开对象、约 1700 万渲染视图（Objaverse-XL、Objaverse、3D-FUTURE、Toys4K、GSO、TrueBones 等），3D-FRONT 加一个内部场景语料，以及约 1.68 万个动态资产片段。主表使用仅三维资产训练的 checkpoint：对象测试为 100 个 held-out assets；场景公开测试为 50 个 held-out 3D-FRONT 样本，另以 200 个内部场景样本作泛化探针；动态测试使用 Obj.-Val、Truebone 和 ActionBench。附录另在 NYU Depth V2 的 1,449 帧与 ETH3D 的 454 帧上评估加入 12 个 RGB-D 式数据集混训的 WT-S。内部场景语料与测试集无法由外部完整审计。

**指标与 baseline。** 可见面报告 SSI 对齐后的 MAE、RMSE、AbsRel、δ 阈值；完整几何报告 Chamfer-L1/L2 与 F-score，并区分 L0 和 All-L；动态片段对逐帧误差求均值。baseline 覆盖深度/pointmap（DA3、MoGe-2、VGGT、Pi3X）、分层回归（LaRI）、image-to-3D（TRELLIS.2、SAM 3D、LaS-Comp、ReconViaGen）和动态几何（GVFDiffusion、SS4D、ActionMesh）。随机扩散/生成方法在部分表中取 8 个 seed 的最优几何结果，不能与单次采样成本混为一谈。

**主结果（实验事实）。**

- 对象可见深度中，WT-O 的 MAE / RMSE / AbsRel 为 **0.0149 / 0.0243 / 0.0079**，优于表中 VGGT 的 0.0257 / 0.0370 / 0.0138 和 MoGe-2 的 0.0261 / 0.0368 / 0.0141。100 样本完整几何上，WT-O point cloud 的 Chamfer-L1 **0.0213**、F@0.05 **0.898**，表中 TRELLIS.2 为 0.0566 / 0.598；接入 TRELLIS.2 后的 WT-O* mesh 为 0.0326 / 0.808。
- 50 个 held-out 3D-FRONT 场景上，WT-S 的可见 AbsRel **0.0114**、L0 CD-L1 **0.0093**、All-L F@0.05 **0.8951**；LaRI-scene 分别为 0.0359、0.0268、0.6671。200 个内部样本上 WT-S 仍在表中最佳，但其 All-L F@0.05 降至 0.6500，显示跨分布退化。
- 动态全局 CD-L2 中，WT-D 在 Truebone / Obj.-Val 为 **0.0063 / 0.0034**，优于各 baseline；ActionBench 为 **0.0291**，落后 ActionMesh 的 **0.0243**。三组均值 WT-D 为 **0.0105**、ActionMesh 为 0.0162。该例外说明优势取决于 ground truth 与输出表示是否匹配。
- 真实深度附录中，RGB-D 混训 WT-S 20 步相对仅三维资产版改善 NYU / ETH3D indoor AbsRel（0.0398→0.0382、0.0398→0.0345）；50 步版本为 0.0374 / 0.0332，但 Pi3X 在 NYU 为 0.0341。证据支持混合单层监督能补强可见面，不支持其全面取代专用深度模型。

**消融与诊断。** timestep 日程消融的全层 CD-L2：plateaued logit-normal 0.031、标准 logit-normal 0.027、两者 mixture **0.024**；前者偏好 L0，后者偏好深层，支持混合日程的权衡。联合 depth + mask 早期训练中两任务梯度余弦可接近零或为负（500 iter 示例 -0.19），配合深层有效面积统计，支持去掉 mask head 的优化动机。小规模 LayerScale 消融在 10k iter 降低 loss，但不是最终规模的完整因果归因。论文没有给主表置信区间或多次训练方差。

**证据真正支持的结论。** 在作者构建的几何指标和测试范围内，多层像素对齐生成可以同时改善 L0 忠实度与遮挡面覆盖，并能作为若干下游管线的几何先验。三项下游编辑/视频/mesh 主要是演示与任务相关指标，不足以证明任意真实场景中的长期一致性，也不能把与性能的相关性解释成多层表示是唯一致因。

### 总结讨论

World Tracing 把单目三维的“忠实但不完整”和“完整但不对齐”两端收束到一个清晰接口：输入像素网格上的相机坐标多层点栈。技术上最有价值的不是单个注意力块，而是表示、depth-filling 监督与 flow-matching 生成目标的配套设计。公开对象、3D-FRONT 与动态结果支持这一组合在指定分布内有效，ActionBench 例外、真实深度仍输给部分专用模型、内部数据和 best-of-8 则界定了证据强度。

适用边界包括：输入应能给出可靠前景/天空有效域；固定六层难覆盖高穿孔结构；相机坐标 point cloud 仍需额外管线变成带纹理闭合 mesh；生成的遮挡面是条件先验，不是被输入观测证明的真实背面。官方推理说明还指出，有色背景会被冻结图像编码器当作内容而产生“ghost”几何，室外天空需外部 mask。

阅读判断：适合作为单图到 3D、显式几何世界状态和 4D 几何预测的强基线，也适合作为 canonical image-to-3D 的对照。引用时应写“在所测几何 benchmark 上优于所列 baseline”，不要扩大成普遍 SOTA；下游演示说明接口可组合，不等于编辑或视频系统经过端到端、统计充分的普适验证。

### 代码与数据

- **代码：** [haoz19/world-tracing](https://github.com/haoz19/world-tracing) 公开对象、场景、动态推理、20 步 Euler ODE 采样、Rerun 可视化、内参拟合及 TRELLIS.2 bridge；仓库明确写为 **inference-only release**，不含训练代码。
- **模型：** 公开对象 `haoz19/object-model-6layer`（1.7B，504²）、场景 `haoz19/scene-model-6layer-840`（1.5B，840²）和动态 `haoz19/dynamic-model-16frame`（2.1B，336²×16 帧）权重，以及 Hugging Face 在线演示。
- **许可证：** 论文和官方仓库标注 CC BY-NC-ND 4.0；仓库说明代码、权重与演示限非商业研究使用，禁止再分发衍生物。使用前仍应逐项核对所依赖 MoGe、TRELLIS.2 与数据集的各自许可证。
- **数据：** 训练资产来源列表和渲染流程在论文中给出，但内部场景语料、内部 200 样本测试集、完整渲染产物及训练流水线未公开，因此不能仅凭当前 release 完整复现论文训练和全部表格。

### 局限、失败案例与开放问题

- 固定 (L=6) 是工程折中；树叶、笼子、格栅等高穿孔结构可能沿一条射线需要更多交点，需自适应层数或可变深度表示。
- 训练主要依赖渲染和 depth peeling；无纹理、反光表面仍有 synthetic-to-real artifact，室外天空与复杂背景还依赖额外 mask。
- 20 步迭代采样不是实时方案；官方单张 A100/H100 推理约 13–17 秒，动态 8 帧约 30 秒，默认四 seed sweep 约再乘四，实时应用需要蒸馏或少步采样。
- 动态模型只覆盖短片段；长程记忆、持续身份、长期遮挡后重现和大幅相机运动仍未解决，ActionBench 也不是最优。
- best-of-8 seed 选择、无主结果置信区间和内部场景数据降低了公平比较与独立复现强度；应补单次/期望性能、方差与完全公开测试。
- 当前公开仓库只有推理代码与权重；完整训练数据、训练代码和内部评测均未开放，无法端到端复现实验主张。
