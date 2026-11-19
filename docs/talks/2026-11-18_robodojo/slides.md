---
theme: default
title: 具身操作策略与闭环智能体：RoboDojo 代表工作分析与 4D 研究方向
info: RoboDojo 七项工作定量对比、核心机制拆解与 4D 研究选题分析
layout: none
defaults:
  layout: none
aspectRatio: 16/9
canvasWidth: 1024
colorSchema: light
fonts:
  provider: none
drawings:
  enabled: false
mdc: false
---

<section class="sheet dark cover">
  <div class="cover-left">
    <div class="eyebrow">具身操作专题学术汇报 · 2026.11</div>
    <h1>具身操作策略与闭环智能体：<br>RoboDojo 分析与 4D 研究方向</h1>
    <p class="subtitle">围绕七项代表性工作，分析端到端策略（VLA/WAM）与闭环智能体（Agent）的能力边界、协作机制，以及结合 4D 表征与世界模型的研究课题。</p>
    <div class="agenda-grid">
      <div class="agenda-item"><span>01 · 榜单表现与定量分析</span>两类方法各擅长哪些维度？总分排名受哪些关键因素驱动？</div>
      <div class="agenda-item"><span>02 · 七项代表工作介绍</span>逐一梳理模型结构、训练数据、核心机制与实验局限</div>
      <div class="agenda-item"><span>03 · 核心机制总结</span>VLA 与 WAM 分工；Agent / Harness / RSI 层次及四系统局内与跨局对比</div>
      <div class="agenda-item"><span>04 · 4D 结合现状与课题方向</span>现有 Agent 静态 3D 局限；去遮挡持久状态、4D 轨迹接口与无力控接触纠偏</div>
    </div>
    <p class="backlink"><a href="../../">← 返回知域知识库</a></p>
  </div>
  <div class="cover-right">
    <h3>汇报涵盖的七项代表工作（RoboDojo-Sim）</h3>
    <div class="camp-box">
      <div class="camp-title"><span style="color:#9dc2e6">第一类 · 端到端操作策略（VLA / WAM）</span><small>单模型直接输出动作</small></div>
      <div class="camp-list">
        · <b>WALL-OSS-1.0-lite</b>（自变量 · VLA · 42.59）<br>
        · <b>VPP2</b>（RobotEra / 清华 · WAM · 39.26）<br>
        · <b>Liber-0 Preview</b>（LiberAI · VLM+WAM · 30.74）
      </div>
    </div>
    <div class="camp-box">
      <div class="camp-title"><span style="color:#7adcd0">第二类 · 闭环与自进化系统（Agent + VLA/WAM）</span><small>高层决策与底层控制结合</small></div>
      <div class="camp-list">
        · <b>GO-3 Nano Preview</b>（智元 · Code Agent+WAM · 61.90）<br>
        · <b>SenseNova-RoboRSI</b>（商汤 · Agent+VLA · 57.39）<br>
        · <b>WorldScape-R²SI</b>（Manifold · 双层 Agent+WAM · 46.58）<br>
        · <b>PhysicalRSI</b>（港大 / KAI · 代码进化+VLA · 36.27）
      </div>
    </div>
    <div class="camp-box" style="padding-bottom:0">
      <div class="camp-list" style="font-size:12px;color:#92aeaa">
        对照与延伸文献：GPT-6 Astra、Q0-Preview、SpatialHarness、Geometric Abstraction、PointWAM、TraceGen、Robot-Factored WM 等。
      </div>
    </div>
  </div>
</section>

<!--
本次汇报围绕四个具体问题展开：第一，在统一双臂评测基准 RoboDojo 上，端到端 VLA/WAM 与引入外层 Agent 的系统在各维度上表现如何，排名主要由什么决定；第二，七项代表工作的具体方法与底层实现；第三，VLA 与 WAM 怎样配合，Agent、Harness 与 RSI 各自改变了系统的哪一部分；第四，核查现有 Agent 对三维几何信号的真实使用情况，并梳理围绕 4D 信息、表征与模型可开展的研究课题。
-->

---

<section class="sheet">
  <div class="topbar">
    <span class="part">01 榜单表现与定量分析</span>
    <span class="meta-tag">RoboDojo-Sim · 42 项双臂操作任务 · 总体得分柱状图</span>
  </div>
  <h1>总体表现：两类方法在总分与计分口径上的分布</h1>
  <p class="lead">RoboDojo 仿真榜包含泛化、精细、长程、记忆、开放五个维度。<b>策略榜按五项等权均分排序</b>；<b>Agent 榜按剔除开放任务后的四项等权均分排序</b>（竖线标记）。</p>
  <div class="rank-chart">
    <div style="display:flex;justify-content:space-between;font-size:11.8px;color:var(--muted);margin-bottom:6px">
      <span>系统名称与类别</span>
      <span><i style="display:inline-block;width:10px;height:9px;background:var(--slate);margin-right:4px"></i>策略模型五项均分　<i style="display:inline-block;width:10px;height:9px;background:var(--teal);margin-right:4px"></i>Agent 系统五项均分　<i style="display:inline-block;width:3px;height:11px;background:var(--rust);margin:0 4px -1px 8px"></i>四项均分（不含开放）</span>
    </div>
    <div class="rank-group-label">第一类：端到端策略模型（VLA / WAM，全榜共 57 项提交）</div>
    <div class="rank-row">
      <span class="rank-name">WALL-OSS-1.0-lite</span>
      <span class="pill pol">VLA</span>
      <div class="rank-track"><div class="rank-bar pol" style="width:60.8%"></div><div class="rank-marker" style="left:68.6%"></div></div>
      <span class="rank-score"><b>42.59</b> <small>(四项 48.05)</small></span>
    </div>
    <div class="rank-row">
      <span class="rank-name">VPP2</span>
      <span class="pill pol">WAM</span>
      <div class="rank-track"><div class="rank-bar pol" style="width:56.1%"></div><div class="rank-marker" style="left:68.5%"></div></div>
      <span class="rank-score"><b>39.26</b> <small>(四项 47.93)</small></span>
    </div>
    <div class="rank-row">
      <span class="rank-name">Liber-0 Preview</span>
      <span class="pill pol">VLM+WAM</span>
      <div class="rank-track"><div class="rank-bar pol" style="width:43.9%"></div><div class="rank-marker" style="left:52.5%"></div></div>
      <span class="rank-score"><b>30.74</b> <small>(四项 36.76)</small></span>
    </div>
    <div class="rank-group-label">第二类：闭环与自进化系统（Agent + 可选 VLA/WAM，全榜共 14 项提交）</div>
    <div class="rank-row">
      <span class="rank-name">GO-3 Nano Preview*</span>
      <span class="pill agt">Agent+WAM</span>
      <div class="rank-track"><div class="rank-bar agt" style="width:88.4%"></div><div class="rank-marker" style="left:88.5%"></div></div>
      <span class="rank-score"><b>61.90</b> <small>(四项 61.95)</small></span>
    </div>
    <div class="rank-row">
      <span class="rank-name">SenseNova-RoboRSI*</span>
      <span class="pill agt">Agent+VLA</span>
      <div class="rank-track"><div class="rank-bar agt" style="width:82.0%"></div><div class="rank-marker" style="left:81.6%"></div></div>
      <span class="rank-score"><b>57.39</b> <small>(四项 57.10)</small></span>
    </div>
    <div class="rank-row">
      <span class="rank-name">WorldScape-R²SI</span>
      <span class="pill agt">Agent+WAM</span>
      <div class="rank-track"><div class="rank-bar agt" style="width:66.5%"></div><div class="rank-marker" style="left:65.6%"></div></div>
      <span class="rank-score"><b>46.58</b> <small>(四项 45.93)</small></span>
    </div>
    <div class="rank-row">
      <span class="rank-name">PhysicalRSI*</span>
      <span class="pill agt">Agent+VLA</span>
      <div class="rank-track"><div class="rank-bar agt" style="width:51.8%"></div><div class="rank-marker" style="left:54.5%"></div></div>
      <span class="rank-score"><b>36.27</b> <small>(四项 38.12)</small></span>
    </div>
    <div class="rank-row">
      <span class="rank-name" style="color:var(--muted)">GPT-6 Astra（纯 VLM 参考）</span>
      <span class="pill warn">Agent 直控</span>
      <div class="rank-track"><div class="rank-bar ref" style="width:41.4%"></div><div class="rank-marker" style="left:39.5%"></div></div>
      <span class="rank-score">28.97 <small>(四项 27.62)</small></span>
    </div>
  </div>
  <div class="takeaway">
    <strong>直接观察：</strong>（1）单独用 GPT-6 Astra 直接输出末端位姿（28.97）低于全部三项策略模型；（2）剔除开放任务后，<b>WALL-OSS (48.05) 与 VPP2 (47.93) 的四项均分实际高于 WorldScape-R²SI (45.93) 和 PhysicalRSI (38.12)</b>。
  </div>
  <div class="foot"><span>注：柱长按 70 分为满刻度绘制；* 表示早于最新通用性规则提交、使用了任务级程序或经验包的系统</span><span>02 / 22</span></div>
</section>

<!--
先看总体得分柱状图。横条是包含开放任务的五项总分，红竖线是不含开放任务的四项均分。从这张图可以直接读出两个重要事实：第一，如果只是把前沿多模态大模型 GPT-6 Astra 直接拿来输出末端位姿，总分只有 28.97，不如训练过的端到端策略模型；第二，如果看红竖线（剔除开放指令后的四项均分），WALL-OSS（48.05）和 VPP2（47.93）实际上比 WorldScape-R²SI（45.93）和 PhysicalRSI（38.12）还要高。下面我们拆开每个模型在六个细分维度上的具体数值，不做跨模型平均，直接看各自强在哪里、弱在哪里。
-->

---

<section class="sheet">
  <div class="topbar">
    <span class="part">01 榜单表现与定量分析</span>
    <span class="meta-tag">逐模型分维度对比 · 避免组均值掩盖个体差异</span>
  </div>
  <h1>分维度表现：开放与记忆呈阵营分界，精细与随机泛化取决于具体设计</h1>
  <p class="lead">直接对比各模型在六个细分指标上的任务进度分（满分 100；泛化由标准布局与随机布局两部分组成）：</p>
  <table class="sm-table">
    <thead>
      <tr>
        <th>模型 / 系统</th>
        <th>标准布局泛化</th>
        <th>随机布局泛化</th>
        <th>精细操作 (8项)</th>
        <th>长程执行 (8项)</th>
        <th>跨时记忆 (6项)</th>
        <th>开放指令 (8项)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>WALL-OSS-1.0-lite</b></td>
        <td class="sm-cell"><span class="sm-num">53.44</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:53.4%;background:var(--slate)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">39.88</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:39.9%;background:var(--slate)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">38.16</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:38.2%;background:var(--slate)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">49.94</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:49.9%;background:var(--slate)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">57.42</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:57.4%;background:var(--slate)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">20.76</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:20.8%;background:var(--slate)"></div></div></td>
      </tr>
      <tr>
        <td><b>VPP2</b></td>
        <td class="sm-cell"><span class="sm-num">52.14</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:52.1%;background:var(--slate)"></div></div></td>
        <td class="sm-cell"><span class="sm-num warn">20.63</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:20.6%;background:var(--rust)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">43.03</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:43.0%;background:var(--slate)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">56.28</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:56.3%;background:var(--slate)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">56.01</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:56.0%;background:var(--slate)"></div></div></td>
        <td class="sm-cell"><span class="sm-num warn">4.61</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:4.6%;background:var(--rust)"></div></div></td>
      </tr>
      <tr>
        <td><b>Liber-0 Preview</b></td>
        <td class="sm-cell"><span class="sm-num">39.31</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:39.3%;background:var(--slate)"></div></div></td>
        <td class="sm-cell"><span class="sm-num warn">10.67</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:10.7%;background:var(--rust)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">38.28</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:38.3%;background:var(--slate)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">45.98</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:46.0%;background:var(--slate)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">37.77</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:37.8%;background:var(--slate)"></div></div></td>
        <td class="sm-cell"><span class="sm-num warn">6.68</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:6.7%;background:var(--rust)"></div></div></td>
      </tr>
      <tr class="sep">
        <td><b>GO-3 Nano Preview*</b></td>
        <td class="sm-cell"><span class="sm-num">45.93</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:45.9%;background:var(--teal)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">26.97</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:27.0%;background:var(--teal)"></div></div></td>
        <td class="sm-cell"><span class="sm-num hi">78.65</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:78.7%;background:var(--teal)"></div></div></td>
        <td class="sm-cell"><span class="sm-num hi">68.21</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:68.2%;background:var(--teal)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">64.50</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:64.5%;background:var(--teal)"></div></div></td>
        <td class="sm-cell"><span class="sm-num hi">61.71</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:61.7%;background:var(--teal)"></div></div></td>
      </tr>
      <tr>
        <td><b>SenseNova-RoboRSI*</b></td>
        <td class="sm-cell"><span class="sm-num hi">56.58</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:56.6%;background:var(--teal)"></div></div></td>
        <td class="sm-cell"><span class="sm-num hi">53.15</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:53.2%;background:var(--teal)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">40.16</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:40.2%;background:var(--teal)"></div></div></td>
        <td class="sm-cell"><span class="sm-num hi">66.41</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:66.4%;background:var(--teal)"></div></div></td>
        <td class="sm-cell"><span class="sm-num hi">66.97</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:67.0%;background:var(--teal)"></div></div></td>
        <td class="sm-cell"><span class="sm-num hi">58.56</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:58.6%;background:var(--teal)"></div></div></td>
      </tr>
      <tr>
        <td><b>WorldScape-R²SI</b></td>
        <td class="sm-cell"><span class="sm-num">46.62</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:46.6%;background:var(--teal)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">39.28</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:39.3%;background:var(--teal)"></div></div></td>
        <td class="sm-cell"><span class="sm-num warn">23.51</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:23.5%;background:var(--rust)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">51.48</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:51.5%;background:var(--teal)"></div></div></td>
        <td class="sm-cell"><span class="sm-num hi">65.78</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:65.8%;background:var(--teal)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">49.16</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:49.2%;background:var(--teal)"></div></div></td>
      </tr>
      <tr>
        <td><b>PhysicalRSI*</b></td>
        <td class="sm-cell"><span class="sm-num">31.57</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:31.6%;background:var(--teal)"></div></div></td>
        <td class="sm-cell"><span class="sm-num warn">11.04</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:11.0%;background:var(--rust)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">38.05</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:38.1%;background:var(--teal)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">46.37</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:46.4%;background:var(--teal)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">46.74</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:46.7%;background:var(--teal)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">28.88</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:28.9%;background:var(--teal)"></div></div></td>
      </tr>
      <tr>
        <td style="color:var(--muted)">GPT-6 Astra（参考）</td>
        <td class="sm-cell"><span class="sm-num">35.32</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:35.3%;background:#8c999c"></div></div></td>
        <td class="sm-cell"><span class="sm-num">31.40</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:31.4%;background:#8c999c"></div></div></td>
        <td class="sm-cell"><span class="sm-num warn">12.65</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:12.7%;background:var(--rust)"></div></div></td>
        <td class="sm-cell"><span class="sm-num warn">21.45</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:21.5%;background:var(--rust)"></div></div></td>
        <td class="sm-cell"><span class="sm-num">43.04</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:43.0%;background:#8c999c"></div></div></td>
        <td class="sm-cell"><span class="sm-num">34.36</span><div class="sm-bar-bg"><div class="sm-bar-fill" style="width:34.4%;background:#8c999c"></div></div></td>
      </tr>
    </tbody>
  </table>
  <div class="takeaway">
    <strong>三点规律：</strong>（1）<b>开放指令</b>阵营分界最明显（全部 Agent ≥28.9，全部策略 ≤20.8）；（2）<b>精细操作</b>与是否为 Agent 无必然关系（R²SI 仅 23.51，低于三项策略模型）；（3）<b>随机布局退化</b>普遍存在，仅在线重定位系统（SenseNova、R²SI）与 WALL-OSS 保持稳定。
  </div>
  <div class="foot"><span>数据来源：RoboDojo 官方仿真榜单（2026.11），各单元格内条形按 100 分满刻度绘制</span><span>03 / 22</span></div>
</section>

<!--
把八个系统的六个细分维度并排画出来，不再算组平均，规律就非常清楚了：最右边“开放指令”这一列呈现出完全的阵营分化，所有带 VLM 推理的 Agent 都在 29 到 62 分之间，而端到端策略最高只有 20.76，VPP2 和 Liber-0 只有个位数。但看“精细操作”和“随机布局泛化”这两列，组内差异比组间差异还大：同样是 Agent+WAM，GO-3 精细操作 78.65，WorldScape-R²SI 只有 23.51；同样有外层代码，SenseNova 随机布局 53.15，而写死阶段流程的 PhysicalRSI 掉到 11.04。
-->

---

<section class="sheet">
  <div class="topbar">
    <span class="part">01 榜单表现与定量分析</span>
    <span class="meta-tag">受控对比与总分权重分析</span>
  </div>
  <h1>排名差异来源：同基座受控增益与两套计分规则的敏感项</h1>
  <p class="lead">由于跨系统对比混杂了不同基座模型与工具，最具可比性的是<b>固定同一基座 VLM（GPT-6 Astra）的三组系统对照</b>，以及同榜单相邻名次的逐项差值分解：</p>
  <div class="cols-2">
    <div class="card accent-teal">
      <div class="kicker">同基座受控对比 · 固定 GPT-6 Astra</div>
      <h3>外层系统显著提升长程与记忆，但精细操作仍是瓶颈</h3>
      <div style="font-size:11.5px;color:var(--muted);margin-bottom:6px">
        <span style="color:#7b8a8e">■</span> Astra 直控 (28.97)　<span style="color:var(--slate)">■</span> + R²SI (46.58)　<span style="color:var(--teal)">■</span> + RoboRSI* (57.39)
      </div>
      <div class="comp-row">
        <div class="comp-head"><span>泛化（标/随均值）</span><span>33.4 → 43.0 → <b>54.9</b></span></div>
        <div class="tri-bars">
          <div class="tri-track"><div style="width:47.7%;height:100%;background:#8c999c"></div></div>
          <div class="tri-track"><div style="width:61.4%;height:100%;background:var(--slate)"></div></div>
          <div class="tri-track"><div style="width:78.4%;height:100%;background:var(--teal)"></div></div>
        </div>
      </div>
      <div class="comp-row">
        <div class="comp-head"><span>精细操作</span><span>12.7 → <span class="warn">23.5</span> → 40.2</span></div>
        <div class="tri-bars">
          <div class="tri-track"><div style="width:18.1%;height:100%;background:#8c999c"></div></div>
          <div class="tri-track"><div style="width:33.6%;height:100%;background:var(--rust)"></div></div>
          <div class="tri-track"><div style="width:57.4%;height:100%;background:var(--teal)"></div></div>
        </div>
      </div>
      <div class="comp-row">
        <div class="comp-head"><span>长程执行</span><span>21.5 → 51.5 → <b>66.4</b></span></div>
        <div class="tri-bars">
          <div class="tri-track"><div style="width:30.7%;height:100%;background:#8c999c"></div></div>
          <div class="tri-track"><div style="width:73.6%;height:100%;background:var(--slate)"></div></div>
          <div class="tri-track"><div style="width:94.9%;height:100%;background:var(--teal)"></div></div>
        </div>
      </div>
      <div class="comp-row">
        <div class="comp-head"><span>跨时记忆</span><span>43.0 → <b>65.8</b> → <b>67.0</b></span></div>
        <div class="tri-bars">
          <div class="tri-track"><div style="width:61.4%;height:100%;background:#8c999c"></div></div>
          <div class="tri-track"><div style="width:94.0%;height:100%;background:var(--slate)"></div></div>
          <div class="tri-track"><div style="width:95.7%;height:100%;background:var(--teal)"></div></div>
        </div>
      </div>
      <p style="margin-top:7px;font-size:12.8px">在同一 VLM 下，加入显式状态记录、技能库与底层策略调用后，<b>长程提升 30–45 分，记忆提升约 23 分</b>。</p>
    </div>
    <div class="card accent-slate">
      <div class="kicker">单维度提升对总分排名的拉动效应</div>
      <h3>特定短板维度的改善可直接改变总体排名</h3>
      <ul>
        <li><b>策略榜（五项各占 20%，单项 +10 分 = 总分 +2.0 分）：</b><br>
          · <b>历史记忆是分水岭：</b>全榜无历史帧设计的早期策略（如 π0.5 记忆仅 5.89 分）总分均低于 21 分；WALL-OSS 与 VPP2 引入历史关键帧后记忆达 56–57 分，直接贡献 <b>+10 分以上总分</b>。<br>
          · <b>头部差距来自开放与随机布局：</b>WALL-OSS 与 VPP2 前四项均分仅差 0.12 分，WALL-OSS 凭开放任务（+16.15 分，折合总分 <b>+3.23 分</b>）位列策略榜第一。</li>
        <li style="margin-top:6px"><b>Agent 榜（不含开放，四项各占 25%，单项 +10 分 = 总分 +2.5 分）：</b><br>
          · 头部 Agent 的记忆（64–68 分）与长程（51–68 分）差距相对收敛。<br>
          · <b>精细操作与随机泛化决定名次：</b>GO-3 Nano 在泛化上低于 SenseNova 18.4 分（总分 −4.60），但凭精细操作高出 38.5 分（总分 <b>+9.62</b>）实现反超。</li>
      </ul>
    </div>
  </div>
  <div class="foot"><span>左侧条形按 70 分满刻度绘制；三个系统均使用 GPT-6 Astra 作为高层推理模型</span><span>04 / 22</span></div>
</section>

<!--
为了做出有意义的定量归因，左边固定同一个基座大模型 GPT-6 Astra 做受控比较：裸跑时精细 12.7、长程 21.5；加上 R²SI 或 RoboRSI 的外层执行机制后，长程和记忆都大幅跃升，但 R²SI 的精细操作仍然只有 23.5 分。右边回答“提高某些轨道是否会让总分大幅上涨”：是的。对端到端策略而言，补上历史帧记忆就能把总分拉高约 10 分，保留语言先验拉开开放任务又能再涨 3 分以上；而在剔除开放任务的 Agent 榜上，记忆和长程大家都能做到五六十分，真正决定排名高低的是精细操作和随机布局泛化。
-->

---

<section class="sheet dark">
  <div class="topbar">
    <span class="part">01 榜单表现与定量分析</span>
    <span class="meta-tag">定性与定量总结 · 影响性能的核心因素</span>
  </div>
  <h1>影响操作性能的关键因素：来自受控对照实验的三点启发</h1>
  <p class="lead">现有结果并未在严格相同的数据与动作空间下单纯缩放模型参数，但横向结果与各论文内部消融一致表明：<b>单纯增加参数量或原始视频时长并非决定因素</b>（如 4B WALL-OSS 总分高于 14.9B VPP2；14B VPP2 视频指令跟随率 90% 高于 64B Cosmos3 的 78%）。真正显著改变性能的是以下三项因素：</p>
  <div class="cols-3">
    <div class="card accent-teal">
      <div class="kicker">因素一 · 训练监督质量</div>
      <h3>精确动作真值优于单纯扩大无标注视频规模</h3>
      <div class="kpi-row"><span class="kpi">1 万h &gt; 200 万h</span></div>
      <p>Liber-0 固定下游微调设置对比五类预训练数据源：<b>1 万小时带手部运动测量的传感器手套数据</b>，在抓放与非抓放精细操作上均优于 200 万小时网络人类视频，并可减少 75% 真机遥操作示范。</p>
    </div>
    <div class="card accent-teal">
      <div class="kicker">因素二 · 决策与控制分层</div>
      <h3>高层子目标分解与闭环动作审查截断长程误差</h3>
      <div class="kpi-row"><span class="kpi">5.8% → 25.8% → 54.2%</span></div>
      <p>商汤在 RoboDojo 上的受控实验显示：开环调用 π0.5 成功率仅 5.83%；加入 <b>VLM 闭环动作审查</b>升至 25.83%；再结合任务经验包达 54.17%。VPP2 引入 VLM 拆分子任务后，五组任务成功率也从 27.6% 升至 57.6%。</p>
    </div>
    <div class="card accent-teal">
      <div class="kicker">因素三 · 空间可观测性</div>
      <h3>暴露接触区域的关键几何关系直接决定精细成败</h3>
      <div class="kpi-row"><span class="kpi">+65.0 个百分点</span><span class="kpi-unit">冻结策略</span></div>
      <p>复旦 SpatialHarness 固定同一操作策略与真机相机，仅在线同步三维场景并渲染无遮挡辅助视角，四项真机精细任务平均成功率提升 65.0 个百分点（抽屉放物从 0% 升至 66.7%）。</p>
    </div>
  </div>
  <div class="card" style="margin-top:11px;padding:9px 14px">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;font-size:13.2px;line-height:1.45">
      <div><span style="color:#9dc2e6;font-weight:700">VLA / WAM 优势与不足：</span>单步推理延迟低（50–220ms）、连续接触控制平滑；但缺乏显式状态核验，长程误差累积且难以零样本泛化至开放指令。</div>
      <div><span style="color:#7adcd0;font-weight:700">Agent 系统优势与不足：</span>擅长任务分解、跨遮挡状态记录与失败恢复；但 API 延迟与 Token 开销高（单任务可达数百万 Token），精细接触仍受限于底层策略与三维感知精度。</div>
    </div>
  </div>
  <div class="foot"><span>实验出处：Liber-0 Sec 4.1 · SenseNova GPT-6 Astra Report Fig 7 · VPP2 Fig 9 · SpatialHarness Fig 4</span><span>05 / 22</span></div>
</section>

<!--
小结第一部分：VLA/WAM 强在低延迟连续动作生成，弱在长程误差累积和开放语义理解；Agent 强在子目标拆解、状态记忆和异常恢复，弱在推理耗时与毫米级接触控制。三组严格的受控实验指向三个决定性变量：训练侧的精确动作锚定数据、控制侧的闭环审查机制，以及感知侧对接触几何的清晰观测。接下来进入第二部分，逐一介绍七项代表工作。
-->

---

<section class="sheet">
  <div class="topbar">
    <span class="part">02 七项代表工作介绍 · 策略派 (1/3)</span>
    <span class="meta-tag">X Square Robot（自变量机器人）· VLA · 策略榜 #1</span>
  </div>
  <h1>WALL-OSS-1.0-lite：保留 VLM 语义先验并引入关键帧记忆的轻量 VLA</h1>
  <div class="work-meta">
    <span class="pill pol">Qwen3.5-4B 主干</span>
    <span class="pill pol">32 步双臂末端位姿输出</span>
    <span class="pill agt">RoboDojo-Sim：42.59 / 34.97%</span>
  </div>
  <div class="cols-2 wide-l">
    <div>
      <div class="arch-canvas">
        <div class="arch-3col">
          <div style="display:flex;flex-direction:column;gap:6px">
            <div class="arch-node"><span class="nt">多视角 RGB + 本体状态</span><span class="ns">头相机 / 双腕相机 + 关节</span></div>
            <div class="arch-node teal-border"><span class="nt" style="color:var(--teal)">滑窗关键帧记忆</span><span class="ns">重读近期头相机帧并筛选保留</span></div>
            <div class="arch-node"><span class="nt">自然语言任务指令</span><span class="ns">保留预训练图文理解接口</span></div>
          </div>
          <div class="arch-arrow">→</div>
          <div class="arch-node slate" style="padding:10px">
            <span class="nt" style="font-size:12.5px">Qwen3.5-4B 紧耦合主干</span>
            <span class="ns">统一跨层级推理与动作表征</span>
            <div class="mini-sub"><b>梯度桥接协同预训练：</b>同时优化离散动作预测、图文任务与连续流匹配，避免微调冲掉 VLM 原有语义能力</div>
          </div>
          <div class="arch-arrow">→</div>
          <div class="arch-node teal-border" style="padding:10px">
            <span class="nt" style="color:var(--teal);font-size:12.5px">4 轮残差动作精化</span>
            <span class="ns">Chained Residual Refiner</span>
            <div class="mini-sub" style="color:var(--ink)">输出双臂 <b>32 步末端位姿 + 夹爪状态</b>；10 环境批处理约占 19GB 显存</div>
          </div>
        </div>
      </div>
      <div class="metric-strip">
        <div class="m-box best"><span class="lbl">标准泛化</span><span class="val">53.44</span></div>
        <div class="m-box best"><span class="lbl">随机泛化</span><span class="val">39.88</span></div>
        <div class="m-box"><span class="lbl">精细操作</span><span class="val">38.16</span></div>
        <div class="m-box"><span class="lbl">长程执行</span><span class="val">49.94</span></div>
        <div class="m-box best"><span class="lbl">跨时记忆</span><span class="val">57.42</span></div>
        <div class="m-box"><span class="lbl">开放指令</span><span class="val">20.76</span></div>
      </div>
    </div>
    <div class="card">
      <h3>核心设计与实验特点</h3>
      <ul>
        <li><b>针对的问题：</b>在预训练 VLM 上直接微调连续动作头容易破坏原有的视觉-语言泛化先验；而完全冻结 VLM 又会削弱语义与底层控制的绑定。</li>
        <li><b>训练与结构设计：</b>WALL 系列通过离散动作 token 将梯度平滑传入 VLM 主干并与多模态 VQA 共训，推理时由连续分支加 4 轮链式残差模块精化双臂末端轨迹。</li>
        <li><b>关键帧记忆机制：</b>在模型内部维护近期头相机画面的滑动窗口并自主筛选保留关键帧，使纯端到端模型在记忆维度达到 <b>57.42 分</b>，标准与随机布局泛化均列策略组第一。</li>
        <li><b>局限：</b>仅支持 <code>arx_x5</code> 末端位姿模式，开放新指令得分（20.76）仍明显低于高层 Agent 系统。</li>
      </ul>
    </div>
  </div>
  <div class="foot"><span>参考：WALL-OSS 论文（arXiv:2509.11766）、Wall-OSS-0.5（arXiv:2605.30877）与 <code>wall-oss-1.0-lite-robodojo</code> 模型卡</span><span>06 / 22</span></div>
</section>

<!--
第一项工作是自变量机器人的 WALL-OSS-1.0-lite。它基于 4B 规模的 Qwen3.5，针对“微调动作容易破坏 VLM 原有语义能力”的问题，采用离散动作、图文问答与连续流匹配共训的策略保留图文先验。针对长程与遮挡任务，它在输入端加入滑窗关键帧筛选机制，输出端用四轮链式残差模块细化 32 步双臂末端位姿。这使得它在仅有 4B 参数量的情况下，同时拿到了策略组最高的泛化分（53.44 / 39.88）和接近 Agent 水平的记忆分（57.42）。
-->

---

<section class="sheet">
  <div class="topbar">
    <span class="part">02 七项代表工作介绍 · 策略派 (2/3)</span>
    <span class="meta-tag">RobotEra &amp; 清华大学 · WAM · 策略榜 #2</span>
  </div>
  <h1>VPP2：事件级视频预训练与单步一致性蒸馏的世界动作模型</h1>
  <div class="work-meta">
    <span class="pill pol">Wan2.1-14B 视频主干 + 0.9B Action DiT</span>
    <span class="pill pol">单步视频预测 0.12s + 动作生成 0.10s</span>
    <span class="pill agt">RoboDojo-Sim：39.26 / 32.26%</span>
  </div>
  <div class="cols-2 wide-l">
    <div>
      <div class="media-frame" style="padding:8px">
        <img src="/media/vpp.png" alt="VPP2 三阶段训练流程" style="max-height:180px">
      </div>
      <p class="cap">VPP2 原论文图 4：阶段 1 事件级视频续训 → 阶段 2 固定 8s 时长一致性蒸馏为单步前向 → 阶段 3 MoT 动作专家读取视频潜特征预测动作。</p>
      <div class="metric-strip">
        <div class="m-box best"><span class="lbl">标准泛化</span><span class="val">52.14</span></div>
        <div class="m-box weak"><span class="lbl">随机泛化</span><span class="val">20.63</span></div>
        <div class="m-box best"><span class="lbl">精细操作</span><span class="val">43.03</span></div>
        <div class="m-box best"><span class="lbl">长程执行</span><span class="val">56.28</span></div>
        <div class="m-box best"><span class="lbl">跨时记忆</span><span class="val">56.01</span></div>
        <div class="m-box weak"><span class="lbl">开放指令</span><span class="val">4.61</span></div>
      </div>
    </div>
    <div class="card">
      <h3>核心设计与实验特点</h3>
      <ul>
        <li><b>针对的问题：</b>通用视频生成底座缺乏准确的操作物理动态，且直接合入动作模块会降低视频模型的开放场景泛化能力与推理速度。</li>
        <li><b>三阶段训练流程：</b>（1）将操作视频切分为 1–12s 完整子任务片段，配详细文本描述做<b>事件级视频续训</b>；（2）改为固定 8s 窗口并通过<b>一致性蒸馏压缩为单步生成</b>（耗时 0.12s）；（3）冻结视频主干（仅开 LoRA），用 0.9B Action DiT 读取视频 KV 缓存学习隐式逆动力学（总延迟 <b>0.22s</b>）。</li>
        <li><b>实验表现与局限：</b>ALOHA 真机零样本成功率达 <b>58.5%</b>（同数据下 π0.5 为 40.0%、Fast-WAM 为 20.5%）；RoboDojo 上额外输入首帧与 8 帧历史使记忆达 56.01，但因缺少语言推理基座，开放指令仅 <b>4.61 分</b>，随机布局退化较明显。</li>
      </ul>
    </div>
  </div>
  <div class="foot"><span>参考：Video Prediction Policy 2: Predict Better, Act Better（arXiv:2610.10270v4）</span><span>07 / 22</span></div>
</section>

<!--
第二项工作是清华与星动纪元的 VPP2。它系统解决了视频世界动作模型的两个核心障碍：预测不准和生成太慢。图中三步非常清晰：先用带细粒度动作描述的完整子任务事件微调 14B 视频底座，再通过一致性蒸馏把未来 8 秒的多视角视频预测压缩到 1 次前向传播（0.12 秒），最后在冻结视频主干的前提下训练 0.9B 的动作扩散网络读取视频特征，整套闭环延迟仅 0.22 秒。它在精细和长程维度位居策略组榜首，但纯视频主干不擅长理解未见过的复杂语言指令，因此开放维度只有 4.61 分。
-->

---

<section class="sheet">
  <div class="topbar">
    <span class="part">02 七项代表工作介绍 · 策略派 (3/3)</span>
    <span class="meta-tag">LiberAI · VLM + WAM · 大规模人类经验迁移</span>
  </div>
  <h1>Liber-0 Preview：联合动作测量手套、多专家世界模型与拟人硬件对齐</h1>
  <div class="work-meta">
    <span class="pill pol">MoT 语言/视觉/动作三专家架构</span>
    <span class="pill pol">RoboDojo 评测：上层 Qwen3-VL + 下层 WAM</span>
    <span class="pill agt">RoboDojo-Sim：30.74（Lite 纯 WAM 版 29.24）</span>
  </div>
  <div class="cols-2 wide-l">
    <div>
      <div class="media-frame" style="padding:4px">
        <img src="/media/liber0-arch.webp" alt="Liber-0 官方架构图" style="max-height:212px">
      </div>
      <p class="cap">Liber-0 官方架构图（Fig. 2 主体）：语言、视觉、动作三专家联合预测未来帧与动作；顶部为可选高层 Agent 子目标输入，底部联合 VQA/分割/视频理解辅助共训。</p>
      <div class="metric-strip">
        <div class="m-box"><span class="lbl">标准泛化</span><span class="val">39.31</span></div>
        <div class="m-box weak"><span class="lbl">随机泛化</span><span class="val">10.67</span></div>
        <div class="m-box"><span class="lbl">精细操作</span><span class="val">38.28</span></div>
        <div class="m-box"><span class="lbl">长程执行</span><span class="val">45.98</span></div>
        <div class="m-box"><span class="lbl">跨时记忆</span><span class="val">37.77</span></div>
        <div class="m-box weak"><span class="lbl">开放指令</span><span class="val">6.68</span></div>
      </div>
    </div>
    <div class="card">
      <h3>核心贡献：弥合人类视频向机器人迁移的三道差距</h3>
      <ul>
        <li><b>1. 穿戴手套补齐动作真值（LiberSense Glove）：</b>互联网人类视频缺少精确手部轨迹；自研手套同步采集第一视角图像与手部精确运动，作为连接 220 万小时人类视频与物理动作的监督锚点。</li>
        <li><b>2. 多专家架构 + 统一本体编码（对应左图）：</b>采用 Mixture-of-Transformers 同步预测未来图像与动作，由 Physical Encoder 编码人手或不同机器人的几何运动学参数作为条件，并联合 VQA、分割、视频理解做辅助共训。</li>
        <li><b>3. 拟人平台对齐与双层评测：</b>自研三自由度手腕与同视角相机的 LEO 机器人，在 60 项真机任务上实现 <b>36.0% 零样本成功率</b>。在 RoboDojo 提交代码中，<b>Preview 版用 Qwen3-VL 先生成子任务与目标框再交由 WAM 输出 32 步关节动作</b>，但在异构双臂夹爪的随机布局上得分较低（10.67）。</li>
      </ul>
    </div>
  </div>
  <div class="foot"><span>参考：Liber-0 官方技术报告（liberai.com/blog/liber0）与 <code>XPolicyLab/policy/Liber_0_preview</code> 源码</span><span>08 / 22</span></div>
</section>

<!--
第三项工作是 Liber-0。左图是它官方的完整架构图：中间是语言、视觉、动作三个 Transformer 专家通过多模态自注意力交互，同时预测未来视频帧和未来动作；左下角 Physical Encoder 把当前关节状态和人/机器人的形态运动学参数编码进来，底部用 VQA、图像分割、编辑和视频理解做语义共训。它的核心贡献是用“传感器手套测准手部真值 + 本体条件编码 + 拟人硬件 LEO 对齐相机视角”打通 220 万小时人类经验迁移。另外看图顶部虚线框有个可选 Agent：核对 XPolicyLab 源码可以看到，榜单上的 Liber-0 Preview 实际在 WAM 前面串了一个 Qwen3-VL 输出子任务和检测框，因此被标为 VLM+WAM，比纯 WAM 的 Lite 版高约 1.5 分。
-->

---

<section class="sheet">
  <div class="topbar">
    <span class="part">02 七项代表工作介绍 · Agent 派 (4/7)</span>
    <span class="meta-tag">AGIBOT（智元机器人）· Code Agent + WAM · WAM 的具体位置与作用</span>
  </div>
  <h1>GO-3 Nano Preview：Python 任务程序主控 + 异常时单向切换 WAM 接管</h1>
  <div class="work-meta">
    <span class="pill agt">开发期：编码 Agent 多轮修订任务程序</span>
    <span class="pill agt">部署期：程序主控 + GE-Act WAM 单向接管</span>
    <span class="pill agt">RoboDojo-Sim：61.90（四项 61.95）</span>
  </div>
  <div class="cols-2 wide-l">
    <div>
      <div class="arch-canvas">
        <div style="font-size:11.5px;font-weight:700;color:var(--teal);margin-bottom:6px">RoboDojo 实际运行流程（核对自 <code>go3_agent_preview</code> 源码与 16 页技术附录）</div>
        <div style="display:grid;grid-template-columns:1.15fr 22px 1fr;align-items:stretch;gap:4px">
          <div class="arch-node teal-border">
            <span class="nt" style="color:var(--teal)">1. 主执行分支：Python 生成器程序</span>
            <span class="ns">每局按任务加载 <code>gm/programs/&lt;task&gt;.py</code></span>
            <div class="mini-sub" style="color:var(--ink)">读取三路 RGB、关节角、末端 <code>link6</code> 位姿与相机标定 → 估算目标 → <code>yield</code> 关节动作 → 视觉/关节检查进度与局部重试</div>
            <div style="margin-top:5px;font-size:10.8px;color:var(--sub)">✓ 若程序顺利完成阶段目标：<b>全程不调用 WAM</b></div>
          </div>
          <div class="arch-arrow">→</div>
          <div class="arch-node dark-box">
            <span class="nt" style="color:#f79b79">2. 触发单向接管：WAM 后端</span>
            <span class="ns">局部恢复耗尽时显式调用：<code>switch_to_wam()</code></span>
            <div class="mini-sub" style="background:rgba(255,255,255,0.12);color:#f5f4ee">通过 WebSocket 将当前三路 RGB、14 维关节状态和指令发给独立 GPU 上的 <b>GE-Act 2.0 (WAM)</b></div>
            <div style="margin-top:5px;font-size:10.8px;color:#7adcd0">→ 生成未来视频与关节动作块，<b>持续控制直至本局结束</b></div>
          </div>
        </div>
        <div style="margin-top:7px;padding-top:6px;border-top:1px dashed var(--rule);font-size:11.2px;color:var(--sub)">
          <b>开发期自进化循环：</b>编码 Agent 收集执行日志 → 提出故障假设并修改定位/时序/切换条件 → 在相同布局下做父子版本成对检验（退化则拒绝）→ 冻结代码用于正式评测。
        </div>
      </div>
      <div class="metric-strip">
        <div class="m-box"><span class="lbl">标准泛化</span><span class="val">45.93</span></div>
        <div class="m-box weak"><span class="lbl">随机泛化</span><span class="val">26.97</span></div>
        <div class="m-box best"><span class="lbl">精细操作</span><span class="val">78.65</span></div>
        <div class="m-box best"><span class="lbl">长程执行</span><span class="val">68.21</span></div>
        <div class="m-box best"><span class="lbl">跨时记忆</span><span class="val">64.50</span></div>
        <div class="m-box best"><span class="lbl">开放指令</span><span class="val">61.71</span></div>
      </div>
    </div>
    <div class="card">
      <h3>如何理解新闻稿与打榜实现的关系？</h3>
      <ul>
        <li><b>区分两个层面：</b>智元官网新闻稿发布的是旗舰 <b>GO-3 Preview</b> 体系（含 WRAM 控制自编码器/动作一致性未来筛选、百台真机混合后训练 Genie Evolver 与部署协议 Genie Master）；榜单条目是其面向 RoboDojo 的 <b>Nano Preview</b> 实现。</li>
        <li><b>WAM 的确切角色：</b>在打榜系统中，WAM 并非每步都运行，而是作为<b>程序恢复失败后的单向接管策略（Fallback Policy）</b>——确定性几何与阶段顺序由代码精准控制（使精细操作达 <b>78.65 分</b>），程序难以处理的状态交由神经网络 WAM 续接完成。</li>
        <li><b>局限：</b>每个任务依赖经 6–32 轮开发调优的专属程序且开发集与评测集场景存在重叠，因此在随机布局泛化上回落至 <b>26.97 分</b>。</li>
      </ul>
    </div>
  </div>
  <div class="foot"><span>参考：智元新闻稿（2026.10.29）与 <code>XPolicyLab</code> PR #214 开源代码及 16 页技术报告附录</span><span>09 / 22</span></div>
</section>

<!--
这一页专门讲清楚 GO-3 Nano 里 WAM 到底在什么位置、起什么作用。核对他们在 XPolicyLab PR #214 提交的真实源码和 16 页技术附录后，结构非常明确：在推理每一局时，首先运行的是一段 Python 生成器任务程序，负责用相机标定算目标位置、发关节指令并检查每一步有没有做成；如果程序顺利做完，根本不会联系 WAM。只有当程序里的局部重试次数用完、自己明确抛出 switch_to_wam 检查点时，控制器才把当前三路图像、关节角和指令发给另一张 GPU 上常驻的 GE-Act WAM 服务，由 WAM 单向接管直到本局结束。因为前期经过了 6 到 32 轮针对各任务的程序迭代，所以精细操作极高（78.65），但遇到随机布局就降到了 26.97。
-->

---

<section class="sheet">
  <div class="topbar">
    <span class="part">02 七项代表工作介绍 · Agent 派 (5/7)</span>
    <span class="meta-tag">商汤科技 SenseNova · Agent + VLA · VLA 的具体位置与受控消融</span>
  </div>
  <h1>SenseNova-RoboRSI：冻结经验包 + VLA 动作提议与 VLM 闭环审查</h1>
  <div class="work-meta">
    <span class="pill agt">上层 VLM (GPT-6 Astra / 自训 27B)</span>
    <span class="pill agt">底层 VLA 服务 (OpenPI π0.5)</span>
    <span class="pill agt">RoboDojo-Sim：57.39（四项 57.10）</span>
  </div>
  <div class="cols-2 wide-l">
    <div>
      <div class="arch-canvas">
        <div class="arch-3col">
          <div class="arch-node">
            <span class="nt" style="color:var(--slate)">离线准备：任务经验包 K</span>
            <span class="ns">模型阅读训练集示范，总结并冻结只读包：</span>
            <div class="mini-sub" style="color:var(--ink)">· 任务阶段策略 (<code>.md</code>)<br>· 参考轨迹与抓取点 (<code>.npz</code>)<br>· 接触视觉裁剪图 (<code>.png</code>)<br>· 运动学与检查脚本 (<code>.py</code>)</div>
          </div>
          <div class="arch-arrow">→</div>
          <div class="arch-node teal-border">
            <span class="nt" style="color:var(--teal)">在线上层：VLM Agent</span>
            <span class="ns">读取当前图像、状态与经验包 K</span>
            <div class="mini-sub" style="color:var(--ink)">1. 规划当前子目标<br>2. <b>审查并修正 VLA 提议的动作块</b>（每 L=4 步审查一次）<br>3. 根据执行后画面判断完成或重试</div>
          </div>
          <div class="arch-arrow">⇄</div>
          <div class="arch-node dark-box">
            <span class="nt" style="color:#7adcd0">在线底层：VLA 容器</span>
            <span class="ns">独立部署 OpenPI <code>π0.5</code></span>
            <div class="mini-sub" style="background:rgba(255,255,255,0.12);color:#f5f4ee">接收当前相机图像、本体状态与子任务描述 → <b>提议短步末端动作序列</b>供上层审查执行</div>
          </div>
        </div>
      </div>
      <div class="card" style="padding:9px 12px">
        <div style="font-size:11.8px;font-weight:650;color:var(--ink);margin-bottom:5px">VLA 协作方式受控消融（摘自商汤实证报告 Fig. 7，RoboDojo 类别平均成功率与 Token 消耗）</div>
        <div class="comp-row" style="margin:4px 0"><div class="comp-head"><span>单独运行底层 VLA (π0.5)</span><span><b>6.91%</b></span></div><div class="tri-track"><div style="width:12.8%;height:100%;background:#8c999c"></div></div></div>
        <div class="comp-row" style="margin:4px 0"><div class="comp-head"><span>A.1 VLM + VLA 开环执行（无 VLM 动作审查）</span><span><b>5.83%</b> · 0.39M Tokens</span></div><div class="tri-track"><div style="width:10.8%;height:100%;background:var(--rust)"></div></div></div>
        <div class="comp-row" style="margin:4px 0"><div class="comp-head"><span>A.3 VLM + VLA 闭环审查（每 L=4 步审查修正）</span><span><b>25.83%</b> · 2.80M Tokens</span></div><div class="tri-track"><div style="width:47.7%;height:100%;background:var(--slate)"></div></div></div>
        <div class="comp-row" style="margin:4px 0"><div class="comp-head"><span>A.5 冻结经验包 ICL + VLA 闭环审查</span><span><b class="hi">54.17%</b> · 19.34M Tokens</span></div><div class="tri-track"><div style="width:100%;height:100%;background:var(--teal)"></div></div></div>
      </div>
    </div>
    <div class="card">
      <h3>VLA 的具体作用与第二阶段模型训练</h3>
      <ul>
        <li><b>VLA 处在什么位置：</b>底层 <code>π0.5</code> 作为独立推理容器，负责根据当前图像生成候选末端动作序列；<b>不能开环盲跑（仅 5.83%）</b>，必须由上层 VLM 每隔 4 步做闭环视觉审查与修正（升至 25.83%），再配合任务经验包达到 54.17%。</li>
        <li><b>用验证轨迹反哺 27B 开源模型：</b>闭环系统虽然成功率高，但单任务消耗高达 19.3M Token。团队将环境验证通过的交互轨迹转为监督数据微调 <code>Qwen3.8-27B</code>（开源 <code>RoboRSI-27B-Preview</code>），在 RoboCasa365 上成功率从 <b>26.0% 升至 46.5%</b>，同时平均输出 Token <b>减少 73.3%</b>（59.5K→15.9K）。</li>
      </ul>
    </div>
  </div>
  <div class="foot"><span>参考：商汤实证报告 <code>has_gpt-6_achieved_embodied_intelligence.pdf</code>（Fig. 2, 3, 7）与 <code>SenseNova-RoboRSI</code> 仓库</span><span>10 / 22</span></div>
</section>

<!--
这一页把 SenseNova-RoboRSI 的系统框图和 VLA 的具体作用完全拆开。看上方流程图：测试前，模型先读训练集示范总结出只读经验包 K；测试时，底层独立容器跑 π0.5 VLA，负责提议 4 步一组的候选末端动作，上层 VLM 结合经验包对 VLA 提议的动作做闭环审查和修正。看左下方他们报告第 10 页的严格消融数据：单独跑 π0.5 只有 6.91%；如果让 VLM 只派活、开环不审查 VLA，只有 5.83%；加上 VLM 闭环审查涨到 25.83%；再加上经验包涨到 54.17%，但代价是消耗近两千万 Token。所以他们第二步把跑通的轨迹拿去微调 27B 模型，既提分又把 Token 降了 73%。
-->

---

<section class="sheet">
  <div class="topbar">
    <span class="part">02 七项代表工作介绍 · Agent 派 (6/7)</span>
    <span class="meta-tag">Manifold AI · 双层 Agent + WAM · 技能与反应模型协同进化</span>
  </div>
  <h1>WorldScape-R²SI：双层智能体同时迭代通用技能文档与底层反应模型</h1>
  <div class="work-meta">
    <span class="pill agt">内层 Robot Agent + 外层 Recursion Agent</span>
    <span class="pill agt">双路径更新：技能文档 ΔH + 模型权重 Δθ</span>
    <span class="pill agt">完全符合最新通用规则 · 46.58 / 39.35%</span>
  </div>
  <div class="cols-2 wide-l">
    <div>
      <div class="arch-canvas">
        <div class="arch-node teal-border" style="margin-bottom:6px">
          <span class="nt" style="color:var(--teal)">外层 Recursion Agent（跨回合离线演化循环）</span>
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:5px;text-align:center;font-size:11px">
            <div style="background:var(--surface);padding:5px 4px;border-radius:3px;font-weight:600">1. 复盘轨迹记录</div>
            <div style="background:var(--surface);padding:5px 4px;border-radius:3px;font-weight:600">2. 改技能 / 训模型</div>
            <div style="background:var(--rust-soft);color:var(--rust);padding:5px 4px;border-radius:3px;font-weight:700">3. 固定测试集验证</div>
            <div style="background:var(--teal-soft);color:var(--teal);padding:5px 4px;border-radius:3px;font-weight:700">4. 达标自动发版</div>
          </div>
        </div>
        <div style="display:flex;justify-content:space-between;padding:2px 8px 6px;font-size:11px;font-weight:600">
          <span style="color:var(--teal)">↓ 路径 A：更新 SKILL.md (ΔH)　|　路径 B：更新反应模型权重 (Δθ)</span>
          <span style="color:var(--sub)">↑ 回传轨迹与得分</span>
        </div>
        <div class="arch-node dark-box" style="padding:9px 11px">
          <span class="nt" style="color:#7adcd0">内层 Robot Agent（单回合在线决策 · 基于 GPT-6 Astra）</span>
          <span class="ns" style="margin-top:3px;font-size:11.2px">每步读取三视角 RGB、本体状态与回合记忆 → 依据共享技能库选择<b>调用运动控制工具</b>或<b>调用反应模型 WSP（执行 1 个动作块后立即归还控制权）</b></span>
        </div>
      </div>
      <div class="metric-strip">
        <div class="m-box best"><span class="lbl">标准泛化</span><span class="val">46.62</span></div>
        <div class="m-box best"><span class="lbl">随机泛化</span><span class="val">39.28</span></div>
        <div class="m-box weak"><span class="lbl">精细操作</span><span class="val">23.51</span></div>
        <div class="m-box"><span class="lbl">长程执行</span><span class="val">51.48</span></div>
        <div class="m-box best"><span class="lbl">跨时记忆</span><span class="val">65.78</span></div>
        <div class="m-box best"><span class="lbl">开放指令</span><span class="val">49.16</span></div>
      </div>
    </div>
    <div class="card">
      <h3>核心机制与消融结果</h3>
      <ul>
        <li><b>内层如何结合 WAM：</b>将“调用底层反应模型（WorldScape Policy，WAM 变体）”封装为一个标准技能。模型每次仅执行一段短动作块就停下交回控制权，由内层 Agent 根据新观测决定下一步。</li>
        <li><b>外层双路径更新与门禁：</b>外层既修改结构化 <code>SKILL.md</code>（写明适用前提、工具选择、进度检查与恢复规则），又筛选执行片段微调底层反应模型；候选版本必须在开发验证集上通过步数预算测试才会被采用（如对齐方块任务淘汰了 3 个未达标版本，v4 实现 8/8 布局在 200 步内完成）。</li>
        <li><b>局限：</b>内层仅接收 RGB 图像与关节状态（无深度或三维几何工具），导致精细接触操作得分偏低（<b>23.51</b>）。</li>
      </ul>
    </div>
  </div>
  <div class="foot"><span>参考：本地 <code>~/papers/r2si.pdf</code>（R²SI 技术报告）与项目主页（r2si.worldscape.io）</span><span>11 / 22</span></div>
</section>

<!--
第六项工作是 Manifold AI 的 WorldScape-R²SI。它由内外两层 Agent 组成：内层每一步读取多视角 RGB 和历史记录，既可以调运动控制工具，也可以调底层反应模型 WSP 跑一小段动作块，跑完立刻把控制权交回内层检查；外层负责跨回合复盘，走两条路径改进系统——路径 A 改写共享技能文档 SKILL.md，路径 B 从探索记录里挑高质量片段去训练底层反应模型 WSP，并且所有改动必须通过验证集门禁测试才能升版。它在不使用任务特权信息的前提下比同基座参考系统高出 17.61 分，主要短板在精细接触（23.51 分）。
-->

---

<section class="sheet">
  <div class="topbar">
    <span class="part">02 七项代表工作介绍 · Agent 派 (7/7)</span>
    <span class="meta-tag">HKU MMLab × Kinetix AI · 代码自进化 + VLA · 工作原理直白拆解</span>
  </div>
  <h1>PhysicalRSI 1.0：用大模型离线迭代 Python 控制程序并按需调用 π0.5</h1>
  <div class="work-meta">
    <span class="pill agt">技能库 = 22 个 Python 控制程序 + π0.5 策略</span>
    <span class="pill agt">模型权重固定，仅改写并筛选代码</span>
    <span class="pill agt">RoboDojo-Sim：36.27 / 31.38%</span>
  </div>
  <div class="cols-2 wide-l">
    <div>
      <div class="arch-canvas">
        <div style="font-size:11.5px;font-weight:700;color:var(--slate);margin-bottom:5px">一、在线评测时怎么运行？（固定技能库，不改代码）</div>
        <div class="arch-3col" style="margin-bottom:8px">
          <div class="arch-node"><span class="nt">1. 开局看首帧选程序</span><span class="ns">VLM 根据首帧画面与指令，从技能库选定一套控制程序</span></div>
          <div class="arch-arrow">→</div>
          <div class="arch-node teal-border"><span class="nt" style="color:var(--teal)">2. 运行 Python 状态机</span><span class="ns">按阶段算目标像素/桌面坐标、生成关节插值动作队列</span></div>
          <div class="arch-arrow">→</div>
          <div class="arch-node"><span class="nt">3. 局部调用 π0.5</span><span class="ns">需要柔顺抓放的子阶段可调用预加载的 <code>π0.5</code> 权重</span></div>
        </div>
        <div style="font-size:11.5px;font-weight:700;color:var(--teal);margin:6px 0 5px;padding-top:6px;border-top:1px dashed var(--rule)">二、离线开发时怎么自我改进？（达尔文式筛选循环）</div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;text-align:center;font-size:11px">
          <div class="arch-node" style="padding:6px"><span class="nt">① 跑当前代码</span>收集成功与失败录像日志</div>
          <div class="arch-node" style="padding:6px"><span class="nt">② 诊断并改写</span>VLM 并行写出多版修改后的 Python 代码</div>
          <div class="arch-node teal-border" style="padding:6px"><span class="nt" style="color:var(--teal)">③ 实测跑分对比</span>在新布局上逐一运行各候选代码</div>
          <div class="arch-node" style="padding:6px"><span class="nt">④ 保留最高分版</span>胜出代码存入技能库供后续复用</div>
        </div>
      </div>
      <div class="metric-strip">
        <div class="m-box"><span class="lbl">标准泛化</span><span class="val">31.57</span></div>
        <div class="m-box weak"><span class="lbl">随机泛化</span><span class="val">11.04</span></div>
        <div class="m-box"><span class="lbl">精细操作</span><span class="val">38.05</span></div>
        <div class="m-box"><span class="lbl">长程执行</span><span class="val">46.37</span></div>
        <div class="m-box"><span class="lbl">跨时记忆</span><span class="val">46.74</span></div>
        <div class="m-box"><span class="lbl">开放指令</span><span class="val">28.88</span></div>
      </div>
    </div>
    <div class="card">
      <h3>具体例子：它到底改写了什么代码？</h3>
      <ul>
        <li><b>例 1（遮挡找物）：</b>直接调 <code>π0.5</code> 在杯子扣住积木后会抓错杯子；离线改写后的 Python 代码在扣杯前先用字典 <code>m = {颜色: 坐标}</code> 存下积木位置，再去抓目标杯子。</li>
        <li><b>例 2（双物互换位置）：</b>原代码直接搬运导致两物碰撞且朝向错乱；改写后的代码自动增加一个“先放到空白临时位置（buffer pose）”的中转步骤。</li>
        <li><b>例 3（跨任务代码复用）：</b>通用拾取任务写好的“像素转桌面三维坐标”函数，在插充电器任务中直接 <code>import</code> 复用。</li>
        <li><b>为什么随机布局仅 11.04 分：</b>公开库包含 22 个针对特定任务的固定阶段插值程序并依赖预设桌面平面高度，物体位置大幅随机变化时容易失效。</li>
      </ul>
    </div>
  </div>
  <div class="foot"><span>参考：<code>XPolicyLab/policy/PhysicalRSI</code> 评测源码与项目主页（mmlab.hk/research/PhysicalRSI）</span><span>12 / 22</span></div>
</section>

<!--
这一页用最直白的方式把 PhysicalRSI 讲清楚。把它拆成“在线怎么跑”和“离线怎么改”两半就很好懂了：在线评测时，它有一个预先准备好的技能库，里面放着 π0.5 模型和 22 个 Python 控制脚本；开局时大模型看第一帧图选一个脚本，之后就由这个 Python 脚本按状态机一步步算坐标、发动作（局部抓放可以调 π0.5）。那这些脚本哪来的？是离线开发时靠下方的四步循环“进化”出来的：跑失败了，让大模型读录像改写出几个新版本的 Python 脚本——比如加一行字典记住杯子底下的积木坐标，或者加一步空位中转——再上仿真器跑分，谁分高留谁。优点是极其简单直观，缺点是写死阶段逻辑的脚本遇到随机布局只剩 11.04 分。
-->

---

<section class="sheet">
  <div class="topbar">
    <span class="part">03 核心机制对比与总结</span>
    <span class="meta-tag">Takeaway 1 · 结合现有工作看 VLA / VLM 与 WAM 如何分工配合</span>
  </div>
  <h1>VLA / VLM 与 WAM 的分工配合：现有工作的三种协作方式</h1>
  <p class="lead">单独的 VLA 具备语言语义理解但缺乏未来物理演化约束；单独的 WAM 具备视觉动态先验但长程语义规划弱、视频生成慢。<b>真正同时包含两类模块的工作</b>主要采用以下三种分工机制：</p>
  <div class="cols-3">
    <div class="card accent-slate">
      <div class="kicker">分工方式一 · 上下层串行引导</div>
      <h3>VLM 拆解子任务与目标框<br>WAM 生成短程动作</h3>
      <ul>
        <li><b>代表：</b><code>Liber-0 Preview</code>、<code>VPP2 + VLM</code>。</li>
        <li><b>配合：</b>上层 VLM（如 Qwen3-VL）读取多视角画面与已完成步骤，输出当前子任务及目标检测框 <code>&lt;bbox&gt;</code>；底层 WAM 据此预测未来视觉特征与关节动作块。</li>
        <li><b>收益：</b>补齐纯 WAM 的语义排序短板（VPP2 加 VLM 后五任务成功率由 27.6% 升至 57.6%）。</li>
      </ul>
    </div>
    <div class="card accent-teal">
      <div class="kicker">分工方式二 · 候选提议与价值评估</div>
      <h3>WAM 提议动作并学动态表征<br>VLM 监控进度并打分筛选</h3>
      <ul>
        <li><b>代表：</b>北大 <code>LAW</code>（2610.23334）、理想 <code>ME-Brain-1.0</code>（榜单 VLA+WAM）。</li>
        <li><b>配合：</b><code>LAW</code> 中视频分支仅在训练期提供动态监督，部署期不生成视频；WAM 输出候选动作，上层 VLM 异步判断阶段进度并用 Value 模块评分融合。<code>ME-Brain-1.0</code> 先联合训练动作与世界状态潜变量，再冻结世界模型微调策略。</li>
      </ul>
    </div>
    <div class="card accent-rust">
      <div class="kicker">分工方式三 · 按操作阶段切换控制</div>
      <h3>远距离由视频模型规划轨迹<br>近距离接触切换至 VLA</h3>
      <ul>
        <li><b>代表：</b><code>Veo-Act</code>（2604.04502）、<code>DualWAM</code>（2609.24868）。</li>
        <li><b>配合：</b>自由空间大范围移动由视频生成模型预测轨迹并经逆动力学转为粗动作；末端接近物体进入接触阶段时，切换给高频反应式 VLA 根据实时腕部画面完成抓取或插接。</li>
      </ul>
    </div>
  </div>
  <div class="takeaway">
    <strong>分工共性：</strong>VLM/VLA 负责<b>语义推理、目标定位或近场接触纠偏</b>；WAM 负责<b>训练期动态表征学习或短程轨迹预测</b>，部署期多经蒸馏或省略像素解码以保证实时性。
  </div>
  <div class="foot"><span>参考：<code>Liber_0_preview/generation.py</code> · <code>ME_Brain_1/README.md</code> · LAW（2610.23334）· Veo-Act（2604.04502）</span><span>13 / 22</span></div>
</section>

<!--
进入第三部分第一个问题：在同时包含 VLA/VLM 和 WAM 的工作里，两者到底是怎么分工配合的？这里严格挑选真正同时包含两类模块的工作，归纳为三种分工：第一种是上下层串行（如榜单上的 Liber-0 Preview），上层 Qwen3-VL 拆子任务、画目标检测框，下层 WAM 接过来生成 32 步动作；第二种是提议与评估配合（如北大 LAW 和榜单上的 ME-Brain-1.0），WAM 在训练时提供世界状态动态监督、在推理时提议候选动作，上层 VLM 判断子任务进度并用价值网络选动作；第三种是按空间距离接力（如 Veo-Act），远距离移动靠视频模型规划，近距离接触交给反应式 VLA。
-->

---

<section class="sheet dark">
  <div class="topbar">
    <span class="part">03 核心机制对比与总结</span>
    <span class="meta-tag">Takeaway 2 · Agent、Harness 与 RSI 各自改变了什么？</span>
  </div>
  <h1>Agent、Harness 与 RSI 的层次区别：远不止“修改提示词循环”</h1>
  <p class="lead">如果只是调整几句提示词让大模型“观察—规划—执行—重试”，每次开新局面对同一任务仍会重复相同的错误。代表性工作的实际技术贡献分别落在以下三个不同层面：</p>
  <div class="cols-3">
    <div class="card" style="border-top:3px solid #9dc2e6">
      <div class="kicker" style="color:#9dc2e6">1. 在线 Agent（单局内的决策与重试）</div>
      <h3>解决“当前这局做错了怎么重来”</h3>
      <ul>
        <li><b>工作方式：</b>在单次任务执行过程中，大模型读取最新画面，发现没抓到或放偏了就重新规划下一步动作。</li>
        <li><b>局限所在：</b>工具接口、观测画面与策略权重都是固定的。<b>本局踩过的坑不会留到下一局</b>，每次新开一局都要重新消耗步数去试错。</li>
      </ul>
    </div>
    <div class="card accent-teal">
      <div class="kicker">2. Harness（模型外围的观测与控制接口）</div>
      <h3>解决“模型看不清、记不住、控不准”</h3>
      <ul>
        <li><b>实质是系统接口工程，而非提示词润色：</b><br>
          · <b>输入端加工：</b>局部高分辨率裁剪、相机标定射线转三维坐标、同步渲染无遮挡虚拟视角（SpatialHarness）；<br>
          · <b>显式状态保持：</b>用代码变量持久化记录被遮挡物体的位置与已完成步骤；<br>
          · <b>输出端约束：</b>用运动规划器（CuRobo/IK）做碰撞检查、设定动作块步长与审查节点。</li>
      </ul>
    </div>
    <div class="card" style="border-top:3px solid #f79b79">
      <div class="kicker" style="color:#f79b79">3. RSI（跨局自动诊断、修改与回归测试）</div>
      <h3>解决“如何把试错经验永久留存下来”</h3>
      <ul>
        <li><b>核心闭环：</b>独立的外层 Agent 分析一批成功与失败记录 → 定位失败原因 → <b>修改技能文档/控制代码（ΔH）或筛选轨迹微调模型权重（Δθ）</b> → <b>在固定测试集上做回归对比</b>。</li>
        <li><b>关键贡献在“验证门禁”：</b>修改不一定变好（如 GO-3 双臂重叠交接候选版均分从 61.7 降至 55.0，R²SI 对齐任务 3 个候选版超时，均被测试门禁自动拦截丢弃）。</li>
      </ul>
    </div>
  </div>
  <div class="takeaway">
    <strong>三层关系：</strong><b>Agent</b> 是单局内的在线闭环决策；<b>Harness</b> 是决定模型能读取什么观测、调用什么控制原语的运行时接口层；<b>RSI</b> 是跨回合自动修改 Harness 或底层模型并通过测试集筛选升级的优化机制。
  </div>
  <div class="foot"><span>参考：NUS/NTU 综述 <code>Toward Recursive Self-Improvement in Physical AI</code>（arXiv:2610.29677）与 R²SI / GO-3 实验记录</span><span>14 / 22</span></div>
</section>

<!--
先分清 Agent、Harness 和 RSI 这三个概念各自改的是哪一层：第一层“在线 Agent”只是在当前这一局里看图重试，下一局清零重来；第二层“Harness”改的是模型外围的工程接口——比如怎么裁剪图像、怎么算三维坐标、怎么记录被遮挡物体位置、怎么用运动规划器防碰撞；第三层“RSI”是在多局之间自动读失败日志、改代码或训小模型，并用回归测试门禁淘汰变差的版本。立住这三个层次后，接下来连续两页用完全一致的顺序对比列表中的四个代表系统：第 15 页看它们在“单回合内”怎么和 VLA/WAM 配合，第 16 页看它们在“跨回合间”怎么自我改进。
-->

---

<section class="sheet">
  <div class="topbar">
    <span class="part">03 核心机制对比与总结</span>
    <span class="meta-tag">Takeaway 3a · 四项代表系统对比（一）：单回合内执行与控制权分配</span>
  </div>
  <h1>四项系统对比（一）：单回合内 Agent 如何与 VLA / WAM 结合？</h1>
  <p class="lead">单独用大模型直接控制机械臂耗时长且接触精度低；单独运行 VLA/WAM 缺乏过程检查与失败恢复。四个系统在<b>单次任务执行内部</b>采用了四种不同的控制权分配方式：</p>
  <table class="tbl">
    <thead>
      <tr>
        <th>代表系统</th>
        <th>日常谁在控制机械臂？</th>
        <th>什么时候调用 VLA / WAM？</th>
        <th>传给底层什么输入？</th>
        <th>底层执行多久交回控制权？</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>WorldScape-R²SI</b><br><span class="pill agt">Agent + WAM</span></td>
        <td>内层 VLM 按决策步在运动控制工具与反应模型之间动态选择。</td>
        <td>当前加载的 <code>SKILL.md</code> 判断某子阶段适合用连续策略执行时。</td>
        <td>三路 RGB 图像、本体关节状态与任务指令。</td>
        <td><b>执行 1 个短动作块（chunk）后立即停下</b>，把新画面交回 VLM 决定下一步。</td>
      </tr>
      <tr>
        <td><b>SenseNova-RoboRSI</b><br><span class="pill agt">Agent + VLA</span></td>
        <td>上层 VLM 统筹规划，底层 <code>π0.5</code> 生成末端动作提议。</td>
        <td>在需要连续操作的每一步或每组短序列前调用 <code>vla_propose</code>。</td>
        <td>当前相机画面、状态与 VLM 拆解出的当前子任务指令。</td>
        <td>每提议/执行 <b>L=4 步末端动作</b>，由上层 VLM 做一次视觉审查与修正。</td>
      </tr>
      <tr>
        <td><b>GO-3 Nano Preview</b><br><span class="pill agt">Code Agent + WAM</span></td>
        <td>Python 任务程序主控（计算几何目标并 <code>yield</code> 关节动作）。</td>
        <td><b>仅当程序内部重试耗尽、无法继续时</b>触发 <code>switch_to_wam</code>。</td>
        <td>切换时刻的三路 RGB、14 维关节状态和原始任务指令。</td>
        <td><b>单向切换，不再交回：</b>由 <code>GE-Act</code> WAM 持续闭环控制直至本局结束。</td>
      </tr>
      <tr>
        <td><b>PhysicalRSI</b><br><span class="pill agt">Agent + VLA</span></td>
        <td>开局由 VLM 看首帧选定一套控制程序，局内由该程序控制。</td>
        <td>选定了神经网络技能，或代码程序运行到抓放子阶段时。</td>
        <td>相机图像、本体状态，以及可选的稀疏历史记忆帧。</td>
        <td>按程序预设阶段运行；直到整局重置前不重新调用高层 VLM 换程序。</td>
      </tr>
    </tbody>
  </table>
  <div class="takeaway">
    <strong>局内差异小结：</strong>按<b>高层在线介入频率</b>由高到低排列——<code>R²SI</code>（单 chunk 交回）与 <code>SenseNova</code>（每 4 步审查）在线纠偏强但 API 开销高；<code>GO-3</code> 与 <code>PhysicalRSI</code> 由本地程序主导执行，推理快但跨布局适应性受限。
  </div>
  <div class="foot"><span>核对自四项工作公开源码与技术报告（R²SI Sec 4.2 · SenseNova Fig 7 · GO-3 Appendix Sec 4.1 · PhysicalRSI README）</span><span>15 / 22</span></div>
</section>

<!--
先看第一张对比表——这四个系统在单回合内部是怎么调底层 VLA/WAM 的。按高层介入频率从上往下排：WorldScape-R²SI 每次只让反应模型跑一个短 chunk 就强制收回控制权；SenseNova 每 4 步末端动作由 VLM 做一次闭环视觉审查，这两者在随机布局下最稳。往下看 GO-3 Nano 和 PhysicalRSI，局内平时都是本地 Python 程序在跑，GO-3 只在程序重试彻底失败时才单向切给 WAM 跑完剩余回合，PhysicalRSI 则在开局选好脚本后一路跑到结束。紧接着翻到下一页，按完全相同的四行顺序看它们在回合之间是怎么进化的。
-->

---

<section class="sheet">
  <div class="topbar">
    <span class="part">03 核心机制对比与总结</span>
    <span class="meta-tag">Takeaway 3b · 四项代表系统对比（二）：跨回合修改对象与经验留存</span>
  </div>
  <h1>四项系统对比（二）：跨回合 RSI 改了什么、怎么测、留存在哪里？</h1>
  <p class="lead">按与上一页完全对应的顺序，对比四个系统在<b>跨回合开发演化阶段</b>修改的对象、回归验证方式与最终留存产物：</p>
  <table class="tbl">
    <thead>
      <tr>
        <th>代表系统</th>
        <th>跨回合修改了什么？</th>
        <th>如何检验修改是否有效？</th>
        <th>经验最终保存在哪里？</th>
        <th>主要优势与局限</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>WorldScape-R²SI</b><br><small style="color:var(--muted)">Manifold AI</small></td>
        <td><b>双路径修改：</b>既改写 <code>SKILL.md</code> 流程与恢复规则，并筛选轨迹微调反应模型。</td>
        <td>候选系统必须在开发测试布局上满足成功率与步数预算门槛才自动晋升。</td>
        <td>跨任务共享的通用 <code>SKILL.md</code> 库 + 更新后的反应模型权重 <code>Δθ</code>。</td>
        <td>完全符合零任务特权通用规则；但缺乏三维几何工具，精细接触较弱（23.51）。</td>
      </tr>
      <tr>
        <td><b>SenseNova-RoboRSI</b><br><small style="color:var(--muted)">商汤科技</small></td>
        <td>第一阶段优化运行时配置与经验包；第二阶段用验证轨迹训练 27B 具身 VLM。</td>
        <td>统一评测框架下同条件版本复测；筛选环境原生高分轨迹构造训练样本。</td>
        <td>版本化任务经验包 + <b>开源 <code>RoboRSI-27B-Preview</code> 模型权重</b>。</td>
        <td>跨 10+ 基准通用，内化进 27B 后减少 73% Token；早期打榜经验包按任务名挂载。</td>
      </tr>
      <tr>
        <td><b>GO-3 Nano*</b><br><small style="color:var(--muted)">智元机器人</small></td>
        <td>调整任务程序的识别规则、抓取点、等待步数及切换 WAM 的触发条件。</td>
        <td>基于故障假设构造单变量修改，在匹配布局与步数预算下与父版本成对测试。</td>
        <td>冻结的任务程序版本 + 预计算的标定参考数组（WAM 权重不变）。</td>
        <td>精细操作得分极高（78.65）；但逐任务定制程序，开发与评测场景有重叠。</td>
      </tr>
      <tr>
        <td><b>PhysicalRSI*</b><br><small style="color:var(--muted)">港大 / KAI</small></td>
        <td>改写任务的 Python 控制函数（目标定位、状态字典、中转步骤、分阶段公差）。</td>
        <td>并行生成多个候选脚本，在新布局上运行并按得分保留最高分个体。</td>
        <td>可读、可跨任务 <code>import</code> 的 Python 技能代码库（模型权重不变）。</td>
        <td>结构简单透明；但固定阶段脚本对随机布局泛化弱（11.04 分）。</td>
      </tr>
    </tbody>
  </table>
  <div class="takeaway">
    <strong>跨局差异小结：</strong>下两行（<code>GO-3</code>、<code>PhysicalRSI</code>）<b>只改外部 Python 控制代码、不改模型权重</b>；上两行进一步<b>将验证过的交互轨迹回流更新模型权重</b>（<code>R²SI</code> 更新底层反应模型，<code>SenseNova</code> 微调上层 27B VLM 以降低在线推理开销）。
  </div>
  <div class="foot"><span>参考：R²SI Table 1 · SenseNova-RoboRSI 文档 · GO-3 Appendix Sec 3 · PhysicalRSI 项目页</span><span>16 / 22</span></div>
</section>

<!--
把四个系统横向放在一张表里，区别就一目了然了：PhysicalRSI 和 GO-3 Nano 改的都是外部 Python 任务程序，模型权重不动；WorldScape-R²SI 同时更新共享的技能文档和底层反应小模型的权重；SenseNova 则进一步把高成本闭环跑出来的成功轨迹拿去训练 27B 视觉语言大模型，把外部经验内化进模型参数里以降低推理 Token 消耗。接下来进入第四部分，回答关于 3D/4D 信号核查与我们的课题方向。
-->

---

<section class="sheet">
  <div class="topbar">
    <span class="part">04 3D/4D 结合现状与课题方向</span>
    <span class="meta-tag">现有 Agentic 系统的 3D 利用（一）· RoboDojo 榜单实战源码核查</span>
  </div>
  <h1>现有 Agentic 的 3D 利用（一）：榜单系统从“不用 3D”到“标定射线几何”</h1>
  <p class="lead">围绕<b>“用没用 3D、用的什么 3D、怎么用的 3D”</b>核查 <code>XPolicyLab</code> 各榜单提交源码：仿真环境虽无深度图（<code>RGB only</code>），但<b>开放了相机内外参矩阵与机械臂正运动学</b>，系统分化为两档：</p>
  <table class="tbl">
    <thead>
      <tr>
        <th>榜单系统分档</th>
        <th>用没用 3D？</th>
        <th>用的什么 3D 信息来源？</th>
        <th>在 Agent 中具体怎么用？</th>
        <th>精细操作表现与直接瓶颈</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>纯 2D 推理型</b><br><small style="color:var(--muted)">GPT-6 Astra 直控<br>WorldScape-R²SI</small></td>
        <td><span class="pill warn">未使用</span></td>
        <td>无三维坐标解算，仅输入多视角 RGB 图像与关节状态。</td>
        <td>直接由 VLM 根据画面估计末端移动方向，或调用纯 2D 输入的反应模型输出动作块。</td>
        <td>精细得分低（<b>12.65 / 23.51</b>）；透视歧义下难以对齐毫米级孔位。</td>
      </tr>
      <tr class="group-sep">
        <td><b>标定解析几何型</b><br><small style="color:var(--muted)">Q0-Preview<br>GO-3 Nano*<br>PhysicalRSI*</small></td>
        <td><span class="pill agt">已使用</span></td>
        <td>仿真器提供的<b>精确相机内外参矩阵</b> + 预设桌面高度平面 <i>z</i> + 机械臂正运动学（FK）末端位姿。</td>
        <td>在 Python 工具中显式解算：<br>① <b>单目射线—已知高度平面求交</b>（<code>at_height</code>）；<br>② <b>头/腕双视角手动选点三角化</b>（<code>triangulate</code>）；<br>③ <b>微抬 2cm 重投影像素比对</b>验证是否抓稳。</td>
        <td>精细得分大幅升至 <b>65.30 / 78.65</b>；但<b>强依赖理想外参、已知平面高度与人工稀疏选点</b>。</td>
      </tr>
    </tbody>
  </table>
  <div class="takeaway">
    <strong>承上启下：</strong>榜单代码对比证明<b>显式引入 3D 几何能将 Agent 精细操作提高 40 分以上</b>；但“相机射线 + 平面求交”看不见未知高度物体的完整三维表面、接触自遮挡（商汤真机插头 0/11 成功）及薄边缘跨视角误匹配——<b>近期学术论文正尝试用更完整的三维表征替代手工射线（见下页）</b>。
  </div>
  <div class="foot"><span>代码依据：<code>XPolicyLab/policy/Q0_Preview/assets/geometry/</code> · <code>GO_3_Nano_preview</code> · 商汤真机报告 Sec 4.2</span><span>17 / 22</span></div>
</section>

<!--
第 17 和第 18 两页连在一起，用同一套框架回答“现有 Agentic 系统到底用没用上 3D、用的什么 3D、怎么用的 3D”。先看第 17 页 RoboDojo 榜单实战代码：R²SI 和裸 GPT-6 Astra 确实没用 3D，所以精细操作只有 12 到 23 分；而高分的 Q0-Preview 和 GO-3 Nano 已经大量用上了 3D，它们用的是仿真器给的精确相机内外参和桌面高度平面，靠单目射线与平面求交、双目手动选点三角化来算抓取位姿，直接把精细操作拉高到 65 到 78 分。但这种“标定射线几何”必须知道平面高度和精确外参，而且遇到夹爪挡住插孔就看不见了。那近期学术论文是怎么在 Agentic 系统里升级 3D 表征的？紧接着看第 18 页。
-->

---

<section class="sheet">
  <div class="topbar">
    <span class="part">04 3D/4D 结合现状与课题方向</span>
    <span class="meta-tag">现有 Agentic 系统的 3D 利用（二）· 近期学术论文的三种 3D 用法与缺失的 4D 层</span>
  </div>
  <h1>现有 Agentic 的 3D 利用（二）：近期论文已升级至静态 3D，但仍缺动态 4D</h1>
  <p class="lead">承接上页：为突破手工射线几何的局限，近期具身 Agentic / Harness / RSI 论文沿用<b>同一套接口改造思路</b>引入了三类显式三维表征，但与动态 4D 模型之间仍存在明显断层：</p>
  <table class="tbl">
    <thead>
      <tr>
        <th>代表具身 Agentic 工作</th>
        <th>用的什么 3D 信息/表征？</th>
        <th>在 Agent / Harness 中具体怎么用？</th>
        <th>仍未解决的边界</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>SpatialHarness</b><br><small style="color:var(--muted)">arXiv:2610.12457</small></td>
        <td>多视角初始化重建 + RGB-D + <b>刚体/关节物体 CAD 网格模型</b>。</td>
        <td><b>补齐无遮挡观测：</b>在线同步真实物体位姿到三维仿真器，渲染正交虚拟视角供冻结策略判断对齐（真机四任务 +65.0pp）。</td>
        <td style="width:215px">依赖预建刚体 CAD 与标定；不含柔性形变与接触后滑移判别。</td>
      </tr>
      <tr>
        <td><b>Geometric Abstraction</b> (2611)<br><b>SPARK</b> (2606) · <b>ReKep</b></td>
        <td>分割提取的<b>三维几何面角色</b>（如 <code>bottom_face</code>）或<b>三维关键点</b>。</td>
        <td><b>绑定控制程序参数：</b>将高层 Agent 生成的程序实时重绑定到三维几何基元，直接按三维位姿残差局部纠偏，减少慢 VLM 调用。</td>
        <td>限于规则刚体或稀疏点；<b>接触遮挡时标记为不可用，无法推断接触与滑移状态</b>。</td>
      </tr>
      <tr>
        <td><b>RoboHarn-Evo</b> (2609.37583)<br><b>MOTIO</b> (2610.33446)</td>
        <td>物体局部坐标系下的<b>相对三维位姿关系</b>（或度量级 3D 资产）。</td>
        <td><b>跨局沉淀几何规则：</b>在跨回合 RSI 中根据物理反馈修订“相对三维动作策略知识库”（迁 RoboDojo 零样本 +25~35pp）。</td>
        <td>沉淀为静态符号/文本几何规则或离线长耗时脚本，<b>无连续时空运动建模</b>。</td>
      </tr>
      <tr class="group-sep">
        <td><b>对照：现有动态 4D 模型</b><br><span class="warn">（均无高层 Agent）</span></td>
        <td>稠密三维点流或表面 4D 运动场（<code>Gnomon4D</code>、<code>PointWAM</code>、<code>PointWorld</code>）。</td>
        <td>仅在单阶段策略去噪内部读取未来几何，或配合传统数值采样器做短程轨迹规划，<b>未接入高层 Agent 闭环</b>。</td>
        <td><b>缺少高层任务分解、接触异常归因与跨回合技能自进化</b>。</td>
      </tr>
    </tbody>
  </table>
  <div class="foot"><span>两页汇总结论：现有 Agentic 系统已从“不用 3D”走到“标定射线（P17）”与“静态刚体/符号 3D（P18）”，真正空白在于<b>引入免标定动态 4D 表征与模型</b></span><span>18 / 22</span></div>
</section>

<!--
第 18 页紧接上一页，看近期学术界是怎么在具身 Agentic 系统里升级 3D 的，同样回答“用的什么 3D、怎么用的 3D”：第一种 SpatialHarness 用的是预先建好的物体刚体 CAD 模型和 RGB-D，同步到仿真器里渲染侧面虚拟视角来解决遮挡；第二种 Geometric Abstraction、SPARK、ReKep 用的是分割出来的三维几何面或三维关键点，绑定进 Agent 写的控制程序里算位姿残差；第三种 RoboHarn-Evo 用的是物体局部坐标系下的相对三维位姿规则，在跨回合 RSI 里积累文本化的几何经验。把 17、18 两页合在一起结论非常清晰：现有 Agentic 系统已经用上了 3D，但用的全是“静态、刚体、依赖标定或 CAD 先验”的 3D；而真正建模连续时间变化的动态 4D 表征和世界模型（最下一行 Gnomon4D、PointWorld），目前还全部停留在没有 Agent 的底层单阶段模型里。这就自然引出了后面三页我们围绕 4D 能做的三个具体课题。
-->

---

<section class="sheet">
  <div class="topbar">
    <span class="part">04 3D/4D 结合现状与课题方向</span>
    <span class="meta-tag">课题构想一（状态感知层）· 解决接触瞬间自遮挡与 CAD 先验依赖</span>
  </div>
  <h1>课题一：免 CAD 的持久化 4D 场景记忆与“去夹爪透视”观测</h1>
  <p class="lead"><b>针对 P17–18 的共同盲区：</b>标定射线与 <code>Geometric Abstraction</code> 仅感知当前帧可见像素——<b>一旦夹爪靠近挡住插孔或杯子扣住物体，三维坐标立即丢失</b>；而 <code>SpatialHarness</code> 抗遮挡必须预先手工扫描全套刚体 CAD 资产。</p>
  <div class="cols-2 wide-l">
    <div>
      <div class="arch-canvas">
        <div class="arch-3col">
          <div class="arch-node">
            <span class="nt" style="color:var(--slate)">1. 接近前（无遮挡期）</span>
            <span class="ns">前馈多视图几何锁定</span>
            <div class="mini-sub" style="color:var(--ink)">在视线清晰阶段重建插槽与手持物末端的局部三维表面，存入持久化场景状态</div>
          </div>
          <div class="arch-arrow">→</div>
          <div class="arch-node teal-border">
            <span class="nt" style="color:var(--teal)">2. 接触期（夹爪遮挡）</span>
            <span class="ns">URDF 遮挡剔除 + 运动传播</span>
            <div class="mini-sub" style="color:var(--ink)">用精确已知的机械臂 URDF 剔除夹爪遮挡像素，结合手腕运动与局部可见边缘持续追踪物-槽三维相对位姿</div>
          </div>
          <div class="arch-arrow">→</div>
          <div class="arch-node dark-box">
            <span class="nt" style="color:#7adcd0">3. 透视输出接口</span>
            <span class="ns">X-Ray 正交视图 &amp; 间隙向量</span>
            <div class="mini-sub" style="background:rgba(255,255,255,0.12);color:#f5f4ee">在持久 4D 状态中<b>擦除夹爪遮挡</b>，向冻结策略或 Agent 实时渲染透视对齐截面并输出毫米级偏差</div>
          </div>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:8px">
        <div class="media-frame" style="display:flex;align-items:center;gap:10px;padding:6px 10px">
          <img src="/media/plug-align.jpg" alt="接近前可见" style="width:92px;height:68px;object-fit:cover;border-radius:3px">
          <div style="font-size:12px;line-height:1.4"><b>接近前：</b>孔位几何清晰可见，锁定局部三维表面</div>
        </div>
        <div class="media-frame" style="display:flex;align-items:center;gap:10px;padding:6px 10px">
          <img src="/media/plug-seated.jpg" alt="接触时自遮挡" style="width:92px;height:68px;object-fit:cover;border-radius:3px">
          <div style="font-size:12px;line-height:1.4"><b class="warn">接触瞬间：</b>原相机视线被挡，靠持久 4D 状态持续透视跟踪</div>
        </div>
      </div>
    </div>
    <div class="card accent-teal">
      <div class="kicker">核心创新点与展示效果</div>
      <h3>做成“零 CAD 先验的动态 SpatialHarness 2.0”</h3>
      <ul>
        <li><b>摆脱离线资产建模：</b>无需提前扫描物体 CAD 模型或手工指定桌面高度，任意未见刚体/铰接物体在操作过程中即建即用。</li>
        <li><b>克服纯 RGB 跟踪器跟丢问题：</b>在夹爪遮挡瞬间不强求纯视觉点跟踪穿墙，而是融合“遮挡前锁定的三维几何 + 本体运动学遮挡掩码 + 未遮挡局部表面约束”维持状态连续。</li>
        <li><b>直观可验证：</b>一边是腕部相机被夹爪完全挡住的原图，一边是系统实时给出的去夹爪三维透视截面，固定同一策略即可测出精细插接与遮挡任务的净提升。</li>
      </ul>
    </div>
  </div>
  <div class="foot"><span>关联基础：SpatialHarness（2610.12457）· World Tracing（多层可见与遮挡表面几何，2606.13652）· DynamicVGGT</span><span>19 / 22</span></div>
</section>

<!--
课题一直接针对第 17、18 页暴露的头号痛点：所有瞬时感知方法在夹爪靠近挡住插孔的那一刻三维坐标就丢了，而 SpatialHarness 为了抗遮挡又要求提前手工扫描全套物体 CAD。我们的核心思路非常清晰：在机械臂靠近前视线无遮挡时，用前馈三维重建锁住插孔和手持物末端的局部三维表面；到了接触遮挡瞬间，利用机械臂自身 100% 已知的 URDF 几何把挡视线的夹爪擦除掉，结合手腕运动和未遮挡边缘在持久化 4D 状态里继续追踪插头和插孔的三维相对位置，给 Agent 实时提供“去夹爪的透视正交视图”和三维间隙残差。既不需要预建 CAD，又解决了纯点跟踪器在遮挡区跟丢的硬伤。
-->

---

<section class="sheet">
  <div class="topbar">
    <span class="part">04 3D/4D 结合现状与课题方向</span>
    <span class="meta-tag">课题构想二（控制与进化接口层）· 解决“语言太粗、Python 硬编码太脆”</span>
  </div>
  <h1>课题二：以“4D 交互轨迹（Trace）”取代语言和死代码，连接 Agent 与策略</h1>
  <p class="lead"><b>核心结构矛盾：</b>上层传自然语言子任务（如 <code>Liber-0 Preview</code>）描述不出三维绕障与接触姿态；上层直接写 Python 关节控制脚本（如 <code>GO-3</code>、<code>PhysicalRSI</code>）又写死平面几何假设，一换随机布局（11.04 分）或换机械臂就失效。</p>
  <div class="cols-2 wide-l">
    <div>
      <div class="arch-canvas">
        <div class="arch-node slate" style="margin-bottom:6px;padding:8px 11px">
          <span class="nt">高层 VLM / Coding Agent（System 2）</span>
          <span class="ns">不再写死关节插值脚本，而是规划并编辑<b>稀疏 4D 交互轨迹规范</b>（未来 1–2s 手与目标关键点的三维空间曲线 + 接触开合节点）</span>
        </div>
        <div style="display:flex;justify-content:space-between;padding:2px 10px 6px;font-size:11px;font-weight:650">
          <span style="color:var(--teal)">↓ 下发目标 4D Trace 规范</span>
          <span style="color:var(--rust)">↑ 回传轨迹偏差 ΔTrace = 规划轨迹 − 实测 4D 轨迹</span>
        </div>
        <div class="arch-node teal-border" style="padding:8px 11px">
          <span class="nt" style="color:var(--teal)">底层 Trace-Conditioned 轻量策略（System 1 · 可从百万人类视频预训练）</span>
          <span class="ns" style="color:var(--ink)">无需机器人动作标签，先在海量人类操作视频上提取三维手-物轨迹预训练动力学先验，再用少量机器人数据对齐高频柔顺控制</span>
        </div>
      </div>
      <div class="card soft" style="padding:9px 12px">
        <p style="font-size:13px;color:var(--ink)"><b>为什么 4D Trace 是天然的最优中间接口？</b>对上，三维空间曲线是 Coding Agent 用几行几何变换就能精确生成和修改的对象；对下，三维点轨迹与具体机械臂构型解耦，天然打通<b>人类视频预训练</b>与<b>跨本体迁移</b>。</p>
      </div>
    </div>
    <div class="card accent-teal">
      <div class="kicker">三重技术收益</div>
      <h3>同时打通几何可控性、人类数据与跨本体 RSI</h3>
      <ul>
        <li><b>比自然语言子目标精确：</b>显式指定绕障高度、插入轴向与双臂协同交接轨迹，解决模糊语义无法约束接触过程的问题。</li>
        <li><b>比纯 Python 状态机鲁棒：</b>局部柔顺接触与高频微调交由预训练的神经网络策略完成，克服硬编码插值在随机布局和柔性物体上的脆弱性。</li>
        <li><b>同一三维坐标系下的闭环与跨本体自进化：</b>执行失败时，“规划 4D 轨迹”与“实测 4D 轨迹”直接相减即可区分是“底层跟踪偏差”还是“高层轨迹规划碰壁”；进化出的轨迹生成技能换一台机械臂仍可直接复用。</li>
      </ul>
    </div>
  </div>
  <div class="foot"><span>关联基础：PointWAM · TraceGen（2511.21690）· μ₀（3D Interaction-Trace WAM，2606.13769）· PointAction</span><span>20 / 22</span></div>
</section>

<!--
课题二从整个架构的中间接口切入。回看前面所有方法：用语言连接上下层太粗糙，直接写 Python 控制机械臂关节又太死板。如果我们把中间语言换成“4D 交互轨迹（未来一两秒手部和物体关键点在三维空间怎么走）”会怎样？往上，Agent 非常擅长在三维坐标系里生成和修改一条空间曲线；往下，以三维轨迹为条件的底层策略可以直接从百万段没有机器人标签的人类视频里提取三维手物轨迹做预训练！更妙的是做 RSI 时，规划的三维轨迹和实际跑出来的三维轨迹在同一个坐标系里一减，差在哪一目了然，而且学出来的轨迹规划技能换一台机械臂还能零样本迁移。
-->

---

<section class="sheet">
  <div class="topbar">
    <span class="part">04 3D/4D 结合现状与课题方向</span>
    <span class="meta-tag">课题构想三（接触反馈层）· 用直白实例说明“无力传感器如何靠 4D 偏差反推接触卡阻”</span>
  </div>
  <h1>课题三：对比“指令预期运动”与“实测 4D 运动”，实现无力控接触纠偏</h1>
  <p class="lead"><b>直白原理（为什么不需要六维力传感器也能知道卡在哪？）：</b>低成本双臂（如 ARX-X5、ALOHA）没有力传感器；插头没插进时单看静态图不知往哪调。但对比<b>“指令让它怎么动”</b>和<b>“它实际怎么动”</b>的微小三维差异，就能由杠杆物理直接算出卡阻方向：</p>
  <div class="cols-2">
    <div class="card accent-teal">
      <div class="kicker">具体物理实例 · 垂直插插头卡住时发生什么？</div>
      <div class="arch-canvas" style="margin:4px 0 8px;padding:8px 10px">
        <div style="display:grid;grid-template-columns:1fr 14px 1.08fr 14px 1.08fr;align-items:stretch;gap:3px">
          <div class="arch-node">
            <span class="nt" style="color:var(--slate)">① 指令预期运动</span>
            <span class="ns">控制器下发：夹爪抓插头<b>垂直下移 2.0 cm，旋转 0°</b>（由 URDF 精确已知）</span>
          </div>
          <div class="arch-arrow">vs</div>
          <div class="arch-node" style="border-color:var(--rust)">
            <span class="nt" style="color:var(--rust)">② 4D 视觉实测运动</span>
            <span class="ns">跟踪插头上半部可见表面：<b>仅下移 0.4 cm 即停滞，且向右微倾 +3°</b></span>
          </div>
          <div class="arch-arrow">→</div>
          <div class="arch-node dark-box">
            <span class="nt" style="color:#7adcd0">③ 物理反推纠偏</span>
            <span class="ns">右倾说明<b>底部左侧磕在孔左沿</b>（左顶住、右沉）→ <b>向右平移 3 mm 再插</b></span>
          </div>
        </div>
      </div>
      <ul>
        <li><b>相当于“4D 视觉虚拟力觉”：</b>即便插孔底部被挡看不见，只要对比预期运动与物体可见部分的微小三维平移/偏转差异（卡住、滑脱、偏心磕碰各有确定几何特征），即可算出精确修正方向。</li>
        <li><b>跨回合记住孔位修正量：</b>将反推成功的偏移修正绑定到目标物体三维局部坐标系，下一局直接一次对准到位。</li>
      </ul>
    </div>
    <div class="card accent-slate">
      <div class="kicker">三个新课题构想的定位与特点汇总</div>
      <table class="tbl" style="margin-top:2px;font-size:12px">
        <thead>
          <tr>
            <th>维度</th>
            <th>课题一<br>去遮挡持久 4D</th>
            <th>课题二<br>4D 轨迹中间接口</th>
            <th>课题三<br>预期-实测 4D 纠偏</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>核心痛点</b></td>
            <td>接触瞬间夹爪挡死视线且无 CAD</td>
            <td>语言太粗、Python 死代码泛化差</td>
            <td>无力传感器平台卡住后不知往哪调</td>
          </tr>
          <tr>
            <td><b>关键抓手</b></td>
            <td>遮挡前三维锁定 + URDF 擦除透视</td>
            <td>Agent 编 4D 轨迹 + 人类视频预训策略</td>
            <td>指令预期三维运动 vs 实测微偏转</td>
          </tr>
          <tr>
            <td><b>训练负担</b></td>
            <td>低（零策略重训，即插即用）</td>
            <td>中高（需训轨迹条件动作策略）</td>
            <td>中低（前馈 6D 跟踪 + 物理诊断）</td>
          </tr>
          <tr>
            <td><b>代表亮点</b></td>
            <td>零 CAD 动态版 SpatialHarness</td>
            <td>打通人类视频与跨本体 Agentic RSI</td>
            <td>纯视觉在低成本臂上做出类力控纠偏</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="foot"><span>关联基础：Robot-Factored WM（名义运动与实测接触分离，2607.22535）· MoSE3（逐像素 SE(3) 跟踪）</span><span>21 / 22</span></div>
</section>

<!--
这一页用最直白的插插头例子把第三个课题彻底讲透：大多数双臂机器人没有六维力传感器，插头没插进去时看静态图根本不知道偏左还是偏右。但我们知道刚才发给机械臂的命令是“垂直往下走 2 厘米、旋转 0 度”；同时用腕部相机跟踪插头上半截没被挡住的部分，发现它只往下走了 0.4 厘米就停了，而且往右歪了 3 度！为什么垂直往下按会往右歪？因为插头底部的左边磕在插孔左沿上了，左边被顶住、右边往下沉！根本不需要看见底下的孔，也不需要力传感器，直接就能推出“往右挪 3 毫米再按”。把这种“指令预期三维运动和实际三维运动的差值”做成通用接触诊断模块，就能在低成本纯视觉机械臂上实现类似力控的精细纠偏。右边表格汇总了这三个课题各自的亮点与投入。
-->

---

<section class="sheet dark">
  <div class="topbar">
    <span class="part">总结</span>
    <span class="meta-tag">回应四个核心问题</span>
  </div>
  <h1>汇报总结：四个核心问题的简明结论</h1>
  <p class="lead">基于 RoboDojo 榜单数据、七项代表工作源码/报告核查与 3D/4D 具身文献分析：</p>
  <div class="cols-2" style="gap:15px">
    <div class="card accent-teal">
      <div class="kicker">问题 1 · 两派表现差异与性能决定因素</div>
      <h3>开放与记忆靠高层推理，精细接触靠几何与底层控制</h3>
      <p>Agent 系统在<b>开放指令</b>（28.9–61.7 vs 4.6–20.8）和<b>跨时记忆</b>上整体占优；但剔除开放任务后，<b>精细操作与随机布局泛化</b>直接决定排名高低（纯 2D 输入的 R²SI 精细仅 23.51）。受控实验表明，<b>精确动作标注数据、闭环动作审查、接触区域空间可观测性</b>比单纯扩大参数量或无标注视频规模更关键。</p>
    </div>
    <div class="card accent-teal">
      <div class="kicker">问题 2 &amp; 3 · 机制分工及四系统局内与跨局差异</div>
      <h3>局内看控制权交接频率，跨局看代码修订与权重回流</h3>
      <p>VLM/VLA 与 WAM 通过<b>子目标引导、候选提议+价值评估、远近分阶段切换</b>三种方式配合。四个 Agent 系统中，<code>R²SI</code> 与 <code>SenseNova</code> 在局内高频交回审查并跨局回流更新模型权重；<code>GO-3</code> 与 <code>PhysicalRSI</code> 局内由本地代码主导、跨局仅迭代外部脚本。其核心贡献在于<b>外围观测/状态接口重构（Harness）与带回归门禁的跨局沉淀（RSI）</b>。</p>
    </div>
    <div class="card accent-slate">
      <div class="kicker" style="color:#9dc2e6">问题 4a · 现有 Agentic 的 3D 利用现状与真实断层</div>
      <h3>已从“不用 3D”走到“标定射线与静态 3D”，仍缺动态 4D</h3>
      <p>榜单高分 Agent（Q0、GO-3）已使用相机标定射线与平面求交，近期论文（SpatialHarness、Geometric Abstraction、RoboHarn-Evo）升级至刚体 CAD 同步或静态几何基元；但面对<b>免 CAD 接触自遮挡、跨布局/跨本体控制接口、无力控接触归因</b>仍缺乏动态 4D 机制。</p>
    </div>
    <div class="card" style="border-top:3px solid #f79b79">
      <div class="kicker" style="color:#f79b79">问题 4b · 围绕 4D 表征与模型的三个高辨识度课题</div>
      <h3>去遮挡持久透视、4D 轨迹中间语言、预期-实测运动差纠偏</h3>
      <p>（1）遮挡前锁定局部三维几何 + URDF 擦除夹爪，实现<b>零 CAD 动态透视观测</b>；（2）以<b>稀疏 4D 交互轨迹（Trace）</b>作为 Agent 与策略的中间接口，打通人类视频预训练与跨本体自进化；（3）对比<b>指令预期运动与实测三维微偏转</b>，在无力传感器平台上反推卡阻方向并跨局记忆。</p>
    </div>
  </div>
  <div class="foot"><span>汇报完毕 · 相关论文、代码仓库链接与核验数据均附于各页页脚及配套正文</span><span>22 / 22</span></div>
</section>

<!--
最后一页把最初提出的四个问题收束为四条清晰结论：第一，看清两派各自的真实长短板与三个关键性能变量；第二和第三，理清 VLA、WAM 与外层 Agent 的分工机制，以及 Harness 和门禁式 RSI 区别于简单改提示词的工程实质；第四，在核实高分仿真 Agent 已经使用解析相机几何的基础上，找准前馈稠密 4D 表征与动作条件 4D 世界模型在免标定接触核验、执行前动作后果评估和真机局部沙盒自进化上的三个具体课题切入点。
-->
