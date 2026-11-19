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

