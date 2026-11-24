## slides 优化

帮我整理概括介绍一下这几个论文：榜一：WALL-OSS-1.0-lite
- https://github.com/X-Square-Robot/wall-x
VLA+WAM: Liber-0 Preview
- https://www.liberai.com/blog/liber0/
Agent+wam: AGIBOT GO-3 Nano Preview
- https://www.agibot.com/article/231/detail/133.html

SenseNova-RoboRSI
- https://github.com/OpenSenseNova/SenseNova-RoboRSI?utm_source=robotics.growbotics.ai&utm_medium=project&utm_campaign=open-source-robotics&utm_content=sensenova-roborsi
WorldScape-R²SI
- https://r2si.worldscape.io/
PhysicalRSI
- https://mmlab.hk/research/PhysicalRSI。有的已经下载到本地 ~/papers/ 了，有的只有网页没有 pdf.


我的问题是:加上 vpp2 这个工作汇总, (1)可以把这些工作分成两派,一派是传统的 vla and or wam, 一派是 agent with optional vla or wam. 根据他们在 robodojo 榜单的表现,看看各自擅长的是什么轨道?相对差异有多大,总体排名主要是由什么因素促成的. 是不是只要某些轨道提高就会让总体分数大幅上涨? 给我们一些定性定量的启发, vla/wam, agent 的优势和不足到底是什么?对于提高最终效果来说,到底什么才是最重要的.模型参数量?数据规模?还是什么? (2) 逐个工作介绍;(3) 我希望 take away 的方面包括: vla 是怎么和wam 一起配合使用的? agent范式中的 wam 或 vla 又是怎么结合的? agent/harness/rsi 范式下不同方法各自区别到底是什么?我对这个路线不熟悉,主观偏见觉得 agentic 就是改改提示词,让 ai 自己观察,规划,执行,验证形成 loop? 你需要通过列表中的代表性工作教会我这类方法的贡献. (4) 我们作为投稿人的贡献到底体现在哪里?感觉水水的没什么实质贡献啊? 在这个语境下,这个后 ai 时代,我们不做这个似乎也说不过去,但是做这个的话,又该怎么做出差异性?怎么结合 3d/4d 信息? 这块有没有一些新的工作? 我希望你基于 slidev 这个框架帮我做一个能给领导直接汇报的 slides. 既方便我阅读学习,又方便给领导展示汇报.注意逻辑清晰,结构严谨,表达清晰凝练,过渡自然顺畅. 一定要注意 taste. 不需要很多防御性的东西. 这是给领导汇报展示的,别放一些不适合展示的解释备注性的东西. 目前 astra 6.2 做的两版我非常不满意，逻辑框架不够清晰，语言不够符合规范的人类报告的习惯。没有太多 take away 的问题和结论。你再改一版



/Users/sanqilu/codes/zhiyu/reports/robodojo-slidev/slides.md 这个版本是我让 carbon 帮我润色的。整体上比 gpt 6.2 astra 出的两版好不少了。但仍然存在一些问题，包括：
- 一些用词与表达上太口语化，像个商业宣传口吻，不像严肃的学术汇报口吻。
- 一些统计分析不够直白清晰，没法让观众一眼看懂。
- 一些页面文字密密麻麻，不适合观众快速抓到关键信息。
- 第 2 页的表格不如一个柱形图更直观清晰
- 第 3 页 4 页按轨道平均去做对比，没有意义啊，轨道平均之后很多信息混杂在一起，没有真正的可比性吧
- 第 5 页”什么决定最终效果“这种表述太口语化了。整体内容再清晰凝练一些。
- 第 8 页 liber 的贡献没看太明白，他没有框架图吗？
- 第 9 页 go3 nano 我其实没看懂 wam 在这个框架中的什么位置起到什么作用。
- 第 10 页 sense nova 也没看明白 vla 在框架中什么位置起到什么作用。以及这个工作没有框架图吗？
- 第 12 页 physical rsi 这个工作我纯纯没看懂
- 第 13 页并不是 vla+wam 的耦合吧，很多工作并不是同时具备 vla+wam 吧
- 第 14 页：“将连续策略封装为有界、可核验的短时算子”这个表达太装神弄鬼了吧，不能说人话吗？严肃正式简洁明了一些。而且这一页是讲 agent + vla/wam 的，怎么又出来 vpp2 了。这一页再讲得清楚一些，这一页比较重要
- 第 15 页：“概念正本清源” 这种标题太装逼了。能不能严肃质朴一些？正文内容我也建议说人话，直白清晰一些。不要说得像圣经和天书一样。
- 第 16 页页讲得直白清晰一些。/Users/sanqilu/codes/zhiyu/reports
- 第 17 页我没看懂啥意思
- 第 18 页 “3d/4d 加速进入具身智能领域”这谁不知道呢？这个标题太肤浅了，另外，我希望你仔细检索一下近期比较好的比较新的工作除了 spatial harness 有没有别的工作已经把 agent/harness/rsi 与 3d/4d 信息、表征、模型结合用起来了？这很重要，这直接决定我我们的课题目标的创新性。
- 第 19 页 “agent 做不好精细操作”你归因是因为 2d 信息缺少精细化信号。但我需要你思考和确认的是，目前很多 agent 在 robodojo 仿真榜单推理，他们推理过程中仅仅只是利用 2d 的信号，没有很好地利用 3d/4d 信号吗？
- 第 20 页的这个 proposal 看着挺琐碎的，核心动机、贡献点和创新点是明朗的吗？方案是可行的吗？
- 第 21 页：”四级消融，干净证明“这种表达不太像严肃学术报告的说法。并且这个方案看着挺装的，徒有其表，没有实质性内容。

请你基于我们最关心的四个问题再重新调整。(1)可以把这些工作分成两派,一派是传统的 vla and or wam, 一派是 agent with optional vla or wam. 根据他们在 robodojo 榜单的表现,看看各自擅长的是什么轨道?相对差异有多大,总体排名主要是由什么因素促成的. 是不是只要某些轨道提高就会让总体分数大幅上涨? 给我们一些定性定量的启发, vla/wam, agent 的优势和不足到底是什么?对于提高最终效果来说,到底什么才是最重要的.模型参数量?数据规模?还是什么? (2) 逐个工作介绍;(3) 我希望 take away 的方面包括: 结合现有工作回答vla 是怎么和wam 一起分工配合使用的? agent范式是如何与wam 或 vla 结合的? agent/harness/rsi 范式下不同方法各自区别到底是什么?我对这个路线不熟悉,主观偏见觉得 agentic 就是改改提示词,让 ai 自己观察,规划,执行,验证形成 loop? 你需要通过列表中的代表性工作教会我这类方法的贡献. （4）围绕 4d 信息、表征、模型，这块，我们还能做些什么工作？

----

我投递完 gnomon4d 之后，最近在调研和思考，下一个工作究竟做什么，在发现问题，并酝酿 proposal.
主要的方向还是 3d/4d 世界动作模型。再尝试考虑结合 agentic 的热点。

周四初步理了一些汇报内容：/Users/sanqilu/codes/zhiyu/reports/robodojo-slidev/slides.md，/Users/sanqilu/codes/zhiyu/slides/robodojo-2026-11/index.html

你看看写得到不到位，目前我担心的有三个点：
- 有没有更相关的更契合的新的工作出来但没写上的，比如这两天看到的：π^4: A Foundation Model for 4D Scene Geometry and Motion
- 目前的 proposal 不是特别深入或 make sense, 没有真正地深入发现问题。proposal 也不够具体和细致，看不出到底是否可行。
- 总体的把握要参考围绕我们课题组领导的大的逻辑框架，可以参考：/Users/sanqilu/files/专家报告/4D数据及其世界模型.pdf，他在最后提到：更原生的4D场景token表征、融入物理的4D原生具身世界模型

总之我希望你帮我把周四初版的那个报告细化完善，我明天要再拿去汇报。
原则上一定要逻辑清晰结构严谨，思路明确。
一般来说，好的报告页面不需要密密麻麻的小字，那样没法让读者很快抓到重点，既不方便读，也不方便讲。

---

## 自动抓取任务

我打算构建一个自动任务，帮我检索抓取最新的工作。但你现在的任务仅仅是帮我修改润色这个定时任务的提示词。/Users/sanqilu/codes/zhiyu/methods/论文周报抓取.md  line 3-401 中是旧版提示词，现在我的关注可能有些调整。一个大的方面是具身智能，细分包括：
（1）gnomon4d代表的 3d/4d 几何增强:/Users/sanqilu/papers/gnomon4d_main.pdf, /Users/sanqilu/papers/gnomon4d_supp.pdf，以及柴颖代表的的几何 wam 特色: /Users/sanqilu/papers/gaf.pdf, /Users/sanqilu/papers/chaiying_GF_WAM-1.pdf;
（2）物理增强, 可能涉及 vlm 的理解；
（3）动态操作，比如 dynamic-wam 等；
（4）agent/harness/rsi；
（5）in context learning 人类示教高效迁移；
可能还有其他的我没写全；

另一个大的方面是：手物交互理解、生成、重建。

这一块现在已经有不少新的进展了，包括：

黎峻佟的 hoi 理解表示学习；邱梓彦的 ego-exo HOI 理解；
李宗翰代表的单图优化式重建 realhoi: /Users/sanqilu/papers/lizonghan_RealHOI_Recurrent_Alignme.pdf，
张家珺代表的序列优化式重建: /Users/sanqilu/papers/zhangjiajun_EgoMetriCap_Egocentric_H.pdf，
张子沐代表的单视角视频生成式重建：/Users/sanqilu/papers/zhangzimu_HandCrafter_Monocular_3D_.pdf
尚士朔代表的 像素对齐、遮挡鲁棒、拓扑一致的生成式重建：/Users/sanqilu/papers/尚士朔-像素对齐、遮挡鲁棒、拓扑一致的生成式重建.pdf
刘攀代表的 2d-3d hoi 共生生成：'/Users/sanqilu/papers/刘攀2d-3d hoi 共生生成.pdf'
邓肯代表的：vlm 物理感知的 hoi 视频生成与强化学习优化; 黎峻佟代表的：agentic vlm规划的2d 3d hoi生成
程嘉嘉代表的 agentic embodied manipulation 生成：

但我上面的罗列的逻辑比较零散，你看看这些课题彼此之间有什么有机的逻辑关系。
帮我重写一遍这个任务的提示词，每周都帮我检索高质量的相关的论文，然后针对每个论文要出一个逻辑清晰结构严谨有taste 的论文卡片。

---


帮我调研一下这几个工作:
ARROW: ARBITRARY RECONSTRUCTIONAND TRACKING OF 4D OBSERVATIONS IN THE WILD, 
sla scaling spatial language action model via continual pre-training
pi^4,
spatial harness
针对每个论文要出一个逻辑清晰结构严谨有taste 的论文卡片，入库 zhiyu. 已有的话，看看是不是写的够好，不够好可以调整。关键是让人读完之后就能理解精髓。


## 大组课题逻辑与规划

我现在正在思考和规划课题组全部人员具身智能发面的研究规划。
我初步思考大致分类可能包括：
细分包括：
（1）已经产出的 gnomon4d代表的 3d/4d 几何增强: /Users/sanqilu/papers/gnomon4d_main.pdf, /Users/sanqilu/papers/gnomon4d_supp.pdf，以及柴颖代表的的几何 wam 特色: /Users/sanqilu/papers/gaf.pdf, /Users/sanqilu/papers/chaiying_GF_WAM-1.pdf;
（2）物理增强, 可能涉及 vlm 的理解；
（3）agent/harness/rsi；
（4）动态操作，比如 dynamic-wam 等；
（5）in context learning 人类示教高效迁移；
可能还有其他的我没写全；

现在请你结合现有的成果，包括 gnomon4d, gaf, gaf-wam 等，以及网络上能检索到的最新的质量比较高的工作：
- /Users/sanqilu/codes/zhiyu/docs/talks/2026-09-15_wam_depth/3D-4D Geometric World Action Model_汇报正文.md
- /Users/sanqilu/files/专家报告/4D数据及其世界模型.pdf
- /Users/sanqilu/codes/zhiyu/reports/robodojo-slidev/slides.md

帮我思考规划设计一下课题组的研究框架。最好逻辑清晰结构严谨，彼此关联。
结果帮我出个 slidev 吧，保存到：/Users/sanqilu/codes/zhiyu/slides/

gpt 6 astra 出的这个版本：/Users/sanqilu/codes/zhiyu/slides/embodied-research-framework-v2/slides.md 我不太喜欢，感觉没什么清晰的逻辑框架或 insight，看着又凌乱有肤浅

