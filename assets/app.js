"use strict";

const STORAGE = {
  hidden: "paper-library.hidden.v1",
  comments: "paper-library.comments.v1",
};

const LINK_LABELS = {
  paper: "论文",
  publication: "正式页",
  project: "项目",
  code: "代码",
  data: "数据",
  model: "模型",
  alphaxiv: "AlphaXiv",
};

const GROUP_PRIORITY = [
  "因果世界模型",
  "World Action Model",
  "HOI",
  "几何一致性",
  "视频生成",
  "3D/4D",
  "机器人学习",
  "交互世界模型",
];

const state = {
  papers: [],
  reports: [],
  hidden: new Set(),
  comments: {},
  selectedTags: new Set(),
  tagMode: "all",
  query: "",
  sort: "newest",
  group: "none",
  showHidden: false,
  view: "readme",
};

const elements = {};
const reportCache = new Map();
let toastTimer = null;

document.addEventListener("DOMContentLoaded", init);

async function init() {
  cacheElements();
  bindEvents();
  state.hidden = new Set(readStorage(STORAGE.hidden, []));
  state.comments = readStorage(STORAGE.comments, {});

  if (window.location.protocol === "file:") {
    renderLoadError(
      "浏览器不允许本地 HTML 读取 JSON 数据。请在仓库根目录运行 python3 -m http.server 8080，再访问 http://localhost:8080/。",
    );
    return;
  }

  try {
    const [papers, reports, overrides] = await Promise.all([
      fetchJson("data/papers.json"),
      fetchJson("data/reports.json"),
      fetchJson("data/paper_overrides.json").catch(() => ({})),
    ]);
    state.papers = papers.map((paper) => mergeOverride(paper, overrides[paper.id]));
    state.reports = reports;
    renderAll();
    openHashTarget();
  } catch (error) {
    renderLoadError(`请确认网站通过 HTTP(S) 提供，并且 data 目录已完整发布。错误：${error.message}`);
  }
}

function renderLoadError(message) {
  elements.paperResults.innerHTML = `
    <div class="empty-state">
      <strong>文献数据读取失败</strong>
      <span>${escapeHtml(message)}</span>
    </div>`;
}

function cacheElements() {
  Object.assign(elements, {
    paperTotal: document.querySelector("#paper-total"),
    reportTotal: document.querySelector("#report-total"),
    tagTotal: document.querySelector("#tag-total"),
    searchInput: document.querySelector("#search-input"),
    sortSelect: document.querySelector("#sort-select"),
    groupSelect: document.querySelector("#group-select"),
    showHidden: document.querySelector("#show-hidden"),
    clearTags: document.querySelector("#clear-tags"),
    tagList: document.querySelector("#tag-list"),
    readmeTagCloud: document.querySelector("#readme-tag-cloud"),
    resultCount: document.querySelector("#result-count"),
    activeFilterSummary: document.querySelector("#active-filter-summary"),
    paperResults: document.querySelector("#paper-results"),
    paperEmpty: document.querySelector("#paper-empty"),
    reportList: document.querySelector("#report-list"),
    maintenanceMetrics: document.querySelector("#maintenance-metrics"),
    sourceList: document.querySelector("#source-list"),
    localChangeList: document.querySelector("#local-change-list"),
    exportOverrides: document.querySelector("#export-overrides"),
    paperDialog: document.querySelector("#paper-dialog"),
    paperDialogId: document.querySelector("#paper-dialog-id"),
    paperDialogContent: document.querySelector("#paper-dialog-content"),
    reportDialog: document.querySelector("#report-dialog"),
    reportDialogContent: document.querySelector("#report-dialog-content"),
    toast: document.querySelector("#toast"),
  });
}

function bindEvents() {
  document.querySelectorAll(".view-tab").forEach((button) => {
    button.addEventListener("click", () => switchView(button.dataset.view));
  });
  document.querySelectorAll("[data-switch-view]").forEach((button) => {
    button.addEventListener("click", () => switchView(button.dataset.switchView));
  });

  elements.searchInput.addEventListener("input", (event) => {
    state.query = event.target.value.trim();
    renderPapers();
  });
  elements.sortSelect.addEventListener("change", (event) => {
    state.sort = event.target.value;
    renderPapers();
  });
  elements.groupSelect.addEventListener("change", (event) => {
    state.group = event.target.value;
    renderPapers();
  });
  elements.showHidden.addEventListener("change", (event) => {
    state.showHidden = event.target.checked;
    renderPapers();
  });
  elements.clearTags.addEventListener("click", () => {
    state.selectedTags.clear();
    renderTags();
    renderPapers();
  });

  document.querySelectorAll("[data-tag-mode]").forEach((button) => {
    button.addEventListener("click", () => {
      state.tagMode = button.dataset.tagMode;
      document.querySelectorAll("[data-tag-mode]").forEach((item) => {
        item.classList.toggle("is-active", item === button);
      });
      renderPapers();
    });
  });

  elements.tagList.addEventListener("click", (event) => {
    const button = event.target.closest("[data-tag]");
    if (!button) return;
    const tag = button.dataset.tag;
    if (state.selectedTags.has(tag)) state.selectedTags.delete(tag);
    else state.selectedTags.add(tag);
    renderTags();
    renderPapers();
  });

  elements.readmeTagCloud.addEventListener("click", (event) => {
    const button = event.target.closest("[data-cloud-tag]");
    if (!button) return;
    state.selectedTags.clear();
    state.selectedTags.add(button.dataset.cloudTag);
    renderTags();
    renderPapers();
    switchView("papers");
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  elements.paperResults.addEventListener("click", (event) => {
    const openButton = event.target.closest("[data-open-paper]");
    if (openButton) openPaper(openButton.dataset.openPaper);
    const hideButton = event.target.closest("[data-toggle-hidden]");
    if (hideButton) toggleHidden(hideButton.dataset.toggleHidden);
  });

  elements.reportList.addEventListener("click", (event) => {
    const button = event.target.closest("[data-open-report]");
    if (button) openReport(button.dataset.openReport);
  });

  document.querySelector("[data-close-dialog]").addEventListener("click", () => {
    elements.paperDialog.close();
  });
  document.querySelector("[data-close-report]").addEventListener("click", () => {
    elements.reportDialog.close();
  });
  elements.paperDialog.addEventListener("close", clearHashTarget);
  elements.reportDialog.addEventListener("close", clearHashTarget);
  elements.paperDialog.addEventListener("click", closeOnBackdrop);
  elements.reportDialog.addEventListener("click", closeOnBackdrop);
  elements.exportOverrides.addEventListener("click", exportOverrides);

  document.querySelectorAll("[data-copy-prompt]").forEach((button) => {
    button.addEventListener("click", async () => {
      const prompt = document.getElementById(button.dataset.copyPrompt)?.textContent;
      if (!prompt) return;
      try {
        await navigator.clipboard.writeText(prompt);
        showToast("提示词已复制。 ");
      } catch {
        showToast("复制失败，请手动选择提示词。 ");
      }
    });
  });

  elements.localChangeList.addEventListener("click", (event) => {
    const button = event.target.closest("[data-restore-paper]");
    if (button) toggleHidden(button.dataset.restorePaper, false);
  });

  window.addEventListener("hashchange", openHashTarget);
}

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`${url}: HTTP ${response.status}`);
  return response.json();
}

function mergeOverride(paper, override) {
  if (!override) return paper;
  return {
    ...paper,
    ...override,
    links: { ...paper.links, ...(override.links || {}) },
    pipeline: { ...paper.pipeline, ...(override.pipeline || {}) },
    tags: override.tags || paper.tags,
  };
}

function renderAll() {
  const tags = allTags();
  elements.paperTotal.textContent = String(state.papers.length);
  elements.reportTotal.textContent = String(state.reports.length);
  elements.tagTotal.textContent = String(tags.length);
  renderTags();
  renderReadmeTagCloud();
  renderPapers();
  renderReports();
  renderMaintenance();
}

function allTags() {
  return [...new Set(state.papers.flatMap((paper) => paper.tags || []))].sort((a, b) =>
    a.localeCompare(b, "zh-CN"),
  );
}

function renderTags() {
  const counts = new Map();
  state.papers.forEach((paper) => {
    (paper.tags || []).forEach((tag) => counts.set(tag, (counts.get(tag) || 0) + 1));
  });
  elements.tagList.innerHTML = allTags()
    .map(
      (tag) => `
        <button class="tag-chip ${state.selectedTags.has(tag) ? "is-active" : ""}"
          type="button" data-tag="${escapeAttr(tag)}" aria-pressed="${state.selectedTags.has(tag)}">
          ${escapeHtml(tag)} <small>${counts.get(tag)}</small>
        </button>`,
    )
    .join("");
}

function renderReadmeTagCloud() {
  const counts = new Map();
  state.papers.forEach((paper) => {
    (paper.tags || []).forEach((tag) => counts.set(tag, (counts.get(tag) || 0) + 1));
  });
  const maximum = Math.max(...counts.values(), 1);
  elements.readmeTagCloud.innerHTML = [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], "zh-CN"))
    .map(([tag, count]) => {
      const tier = Math.max(1, Math.min(5, Math.ceil((count / maximum) * 5)));
      return `<button type="button" class="cloud-tag tier-${tier}" data-cloud-tag="${escapeAttr(tag)}" title="${count} 篇论文">${escapeHtml(tag)}<small>${count}</small></button>`;
    })
    .join("");
}

function filteredPapers() {
  const query = state.query.toLocaleLowerCase("zh-CN");
  const tags = [...state.selectedTags];
  const papers = state.papers.filter((paper) => {
    if (!state.showHidden && isHidden(paper)) return false;
    if (tags.length) {
      const matches = tags.map((tag) => (paper.tags || []).includes(tag));
      if (state.tagMode === "all" && !matches.every(Boolean)) return false;
      if (state.tagMode === "any" && !matches.some(Boolean)) return false;
    }
    if (query) {
      const searchText = [
        paper.id,
        paper.title,
        (paper.authors || []).join(" "),
        paper.publication,
        (paper.tags || []).join(" "),
        paper.summary,
        paper.insight,
        paper.experiments,
        commentFor(paper),
      ]
        .join(" ")
        .toLocaleLowerCase("zh-CN");
      if (!searchText.includes(query)) return false;
    }
    return true;
  });
  return papers.sort(sortPapers);
}

function sortPapers(a, b) {
  const collator = new Intl.Collator(["zh-CN", "en"], { sensitivity: "base" });
  if (state.sort === "oldest") return (a.year || 0) - (b.year || 0) || collator.compare(a.title, b.title);
  if (state.sort === "title-asc") return collator.compare(a.title, b.title);
  if (state.sort === "title-desc") return collator.compare(b.title, a.title);
  if (state.sort === "updated") return String(b.updated_at || "").localeCompare(String(a.updated_at || ""));
  return (b.year || 0) - (a.year || 0) || collator.compare(a.title, b.title);
}

function renderPapers() {
  const papers = filteredPapers();
  elements.resultCount.textContent = String(papers.length);
  elements.paperEmpty.hidden = papers.length !== 0;
  const tagText = [...state.selectedTags].join(state.tagMode === "all" ? " + " : " / ");
  elements.activeFilterSummary.textContent = tagText || (state.query ? `检索：${state.query}` : "全部论文");

  if (state.group === "tag") {
    const grouped = new Map();
    papers.forEach((paper) => {
      const tag = primaryGroup(paper);
      if (!grouped.has(tag)) grouped.set(tag, []);
      grouped.get(tag).push(paper);
    });
    elements.paperResults.innerHTML = [...grouped.entries()]
      .map(
        ([tag, items]) => `
          <section class="paper-group">
            <div class="group-heading"><h3>${escapeHtml(tag)}</h3><span>${items.length} 篇</span></div>
            ${items.map(renderPaperCard).join("")}
          </section>`,
      )
      .join("");
  } else {
    elements.paperResults.innerHTML = papers.map(renderPaperCard).join("");
  }
}

function primaryGroup(paper) {
  const selected = [...state.selectedTags].find((tag) => paper.tags.includes(tag));
  if (selected) return selected;
  return GROUP_PRIORITY.find((tag) => paper.tags.includes(tag)) || paper.tags[0] || "未分类";
}

function renderPaperCard(paper) {
  const hidden = isHidden(paper);
  const authors = shortAuthors(paper.authors || []);
  const links = ["paper", "project", "code", "alphaxiv"]
    .filter((key) => paper.links?.[key])
    .slice(0, 4)
    .map(
      (key) => `<a href="${escapeAttr(paper.links[key])}" target="_blank" rel="noreferrer">${LINK_LABELS[key]}</a>`,
    )
    .join("");
  const commentBadge = commentFor(paper) ? " · 有评论" : "";
  return `
    <article class="paper-card ${hidden ? "is-hidden" : ""}">
      <div class="card-meta">
        <span class="paper-id" title="${escapeAttr(paper.id)}">${escapeHtml(paper.id)}</span>
        <span class="year-badge">${paper.year || "—"}</span>
        <span class="quality-score">${qualityScore(paper)}/10${commentBadge}</span>
      </div>
      <h3>${escapeHtml(paper.title)}</h3>
      <p class="authors">${escapeHtml(authors || "作者待补充")}</p>
      <p class="publication">${escapeHtml(paper.publication || "发表状态待核验")}</p>
      <div class="card-tags">${(paper.tags || []).slice(0, 5).map((tag) => `<span class="paper-tag">${escapeHtml(tag)}</span>`).join("")}</div>
      <p class="insight-preview"><strong>Insight.</strong> ${escapeHtml(paper.summary || "当前报告未提供摘要。")}</p>
      <div class="card-actions">
        <div class="card-link-row">${links}</div>
        <div class="card-command-row">
          <button class="hide-paper" type="button" data-toggle-hidden="${escapeAttr(paper.id)}">${hidden ? "恢复" : "隐藏"}</button>
          <button class="open-paper" type="button" data-open-paper="${escapeAttr(paper.id)}">阅读详情</button>
        </div>
      </div>
    </article>`;
}

function renderReports() {
  elements.reportList.innerHTML = state.reports
    .map(
      (report) => `
        <article class="report-item">
          <time class="report-date" datetime="${escapeAttr(report.date)}">${escapeHtml(report.date)}</time>
          <div>
            <h3>${escapeHtml(report.title)}</h3>
            <p>${escapeHtml(report.summary || "专题论文梳理与趋势分析。")}</p>
            <div class="report-meta">
              <span>${report.paper_ids.length} 篇关联论文</span>
              ${(report.tags || []).map((tag) => `<span class="paper-tag">${escapeHtml(tag)}</span>`).join("")}
            </div>
          </div>
          <button class="button secondary" type="button" data-open-report="${escapeAttr(report.id)}">打开报告</button>
        </article>`,
    )
    .join("");
}

function renderMaintenance() {
  const missingAuthors = state.papers.filter((paper) => !(paper.authors || []).length).length;
  const missingLimits = state.papers.filter((paper) => !paper.limitations).length;
  const localCount = state.hidden.size + Object.keys(state.comments).length;
  const withFigures = state.papers.filter((paper) => paper.figure).length;
  const metrics = [
    [state.papers.length, "合并后论文"],
    [withFigures, "可靠配图记录"],
    [missingAuthors + missingLimits, "待补字段"],
    [localCount, "本地修改"],
  ];
  elements.maintenanceMetrics.innerHTML = metrics
    .map(([value, label]) => `<div class="maintenance-metric"><strong>${value}</strong><span>${label}</span></div>`)
    .join("");

  elements.sourceList.innerHTML = state.reports
    .map(
      (report) => `
        <div class="source-item">
          <div><strong>${escapeHtml(report.title)}</strong><span>${report.paper_ids.length} 篇 · ${escapeHtml(report.source_file)}</span></div>
          <a href="${escapeAttr(report.path)}" target="_blank">Markdown</a>
        </div>`,
    )
    .join("");

  const localIds = new Set([...state.hidden, ...Object.keys(state.comments)]);
  elements.localChangeList.innerHTML = localIds.size
    ? [...localIds]
        .map((id) => {
          const paper = state.papers.find((item) => item.id === id);
          if (!paper) return "";
          const labels = [state.hidden.has(id) ? "已隐藏" : "", state.comments[id] ? "有评论" : ""].filter(Boolean);
          return `
            <div class="local-change-item">
              <div><strong>${escapeHtml(paper.title)}</strong><span>${labels.join(" · ")}</span></div>
              ${state.hidden.has(id) ? `<button class="text-button" type="button" data-restore-paper="${escapeAttr(id)}">恢复</button>` : ""}
            </div>`;
        })
        .join("")
    : '<p class="missing-note">当前设备没有尚未导出的修改。</p>';
}

function switchView(view) {
  state.view = view;
  document.querySelectorAll(".view-tab").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.view === view);
  });
  document.querySelectorAll("main > .view").forEach((section) => {
    const active = section.id === `${view}-view`;
    section.hidden = !active;
    section.classList.toggle("is-active", active);
  });
}

function openPaper(id) {
  const paper = state.papers.find((item) => item.id === id);
  if (!paper) return;
  elements.paperDialogId.textContent = paper.id;
  elements.paperDialogContent.innerHTML = renderPaperDetail(paper);
  if (!elements.paperDialog.open) elements.paperDialog.showModal();
  typesetMath(elements.paperDialogContent);
  setHash(`paper=${encodeURIComponent(id)}`);

  const figure = elements.paperDialogContent.querySelector(".detail-figure img");
  if (figure) {
    figure.addEventListener("error", () => figure.closest(".detail-figure").classList.add("is-broken"));
  }
  elements.paperDialogContent.querySelector("[data-save-comment]").addEventListener("click", () => {
    const textarea = elements.paperDialogContent.querySelector("#paper-comment");
    saveComment(id, textarea.value.trim());
  });
  elements.paperDialogContent.querySelector("[data-dialog-hidden]").addEventListener("click", () => {
    toggleHidden(id);
    elements.paperDialog.close();
  });
}

function renderPaperDetail(paper) {
  const figure = paper.figure
    ? `<figure class="detail-figure">
        <img src="${escapeAttr(paper.figure.url)}" alt="${escapeAttr(paper.figure.alt || paper.title)}" loading="lazy" />
        <figcaption>
          ${escapeHtml(paper.figure.paper_title || paper.title)} · ${escapeHtml(paper.figure.label || "代表图")}
          ${paper.figure.source_url ? ` · <a href="${escapeAttr(paper.figure.source_url)}" target="_blank" rel="noreferrer">来源</a>` : ""}
        </figcaption>
      </figure>`
    : "";
  const links = Object.entries(LINK_LABELS)
    .filter(([key]) => paper.links?.[key])
    .map(
      ([key, label]) => `<a class="detail-link" href="${escapeAttr(paper.links[key])}" target="_blank" rel="noreferrer">${label}</a>`,
    )
    .join("");
  const pipeline = paper.pipeline || {};
  const pipelineStrip = [
    ["Input", pipeline.input],
    ["Process", pipeline.process],
    ["Output", pipeline.output],
  ]
    .map(
      ([label, value]) => `<div class="pipeline-step"><span>${label}</span><strong>${escapeHtml(value || "待补充核验")}</strong></div>`,
    )
    .join("");
  return `
    <h1>${escapeHtml(paper.title)}</h1>
    <div class="detail-meta">
      <span>${paper.year || "年份待核验"}</span>
      <span>${escapeHtml(paper.publication || "发表状态待核验")}</span>
      ${paper.arxiv_id ? `<span>arXiv:${escapeHtml(paper.arxiv_id)}</span>` : ""}
      <span>完整度 ${qualityScore(paper)}/10</span>
    </div>
    <p class="detail-authors">${escapeHtml((paper.authors || []).join(", ") || "作者待补充核验")}</p>
    <div class="card-tags">${(paper.tags || []).map((tag) => `<span class="paper-tag">${escapeHtml(tag)}</span>`).join("")}</div>
    <div class="detail-links">${links}</div>
    ${figure}
    ${detailSection("核心内容与 Insight", paper.insight || paper.summary)}
    <section class="detail-section">
      <h2>Pipeline</h2>
      <div class="pipeline-strip">${pipelineStrip}</div>
      ${pipeline.details ? renderMarkdown(pipeline.details) : missingField()}
    </section>
    ${detailSection("实验与证据", paper.experiments)}
    ${paper.evidence_notes ? detailSection("主张、证据与阅读判断", paper.evidence_notes) : ""}
    ${detailSection("代码与数据开放情况", paper.code_data_status)}
    ${detailSection("局限、失败案例与开放问题", paper.limitations)}
    <section class="detail-section">
      <h2>读者 Comments</h2>
      <textarea class="comment-box" id="paper-comment" placeholder="记录你的判断、疑问或复现备注…">${escapeHtml(commentFor(paper))}</textarea>
      <div class="comment-actions">
        <button class="button ${isHidden(paper) ? "secondary" : "danger"}" type="button" data-dialog-hidden>${isHidden(paper) ? "恢复此论文" : "隐藏此论文"}</button>
        <button class="button primary" type="button" data-save-comment>保存评论</button>
      </div>
    </section>`;
}

function detailSection(title, markdown) {
  return `<section class="detail-section"><h2>${escapeHtml(title)}</h2>${markdown ? renderMarkdown(markdown) : missingField()}</section>`;
}

function missingField() {
  return '<p class="missing-note">当前报告未单独记录，需回到原论文补充核验。</p>';
}

async function openReport(id) {
  const report = state.reports.find((item) => item.id === id);
  if (!report) return;
  elements.reportDialogContent.innerHTML = '<div class="report-loading">正在读取报告…</div>';
  if (!elements.reportDialog.open) elements.reportDialog.showModal();
  setHash(`report=${encodeURIComponent(id)}`);
  try {
    let markdown = reportCache.get(report.path);
    if (!markdown) {
      const response = await fetch(report.path);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      markdown = await response.text();
      reportCache.set(report.path, markdown);
    }
    elements.reportDialogContent.innerHTML = `
      <div class="report-meta"><span>${escapeHtml(report.date)}</span><span>${report.paper_ids.length} 篇关联论文</span></div>
      ${renderMarkdown(markdown, report.path)}`;
    typesetMath(elements.reportDialogContent);
  } catch (error) {
    elements.reportDialogContent.innerHTML = `<div class="report-loading">报告读取失败：${escapeHtml(error.message)}</div>`;
  }
}

function typesetMath(container) {
  if (!window.MathJax?.typesetPromise) return;
  window.MathJax.typesetClear?.([container]);
  window.MathJax.typesetPromise([container]).catch((error) => {
    console.warn("MathJax rendering failed", error);
  });
}

function toggleHidden(id, force) {
  const paper = state.papers.find((item) => item.id === id);
  if (!paper) return;
  if (paper.deleted) {
    showToast("该条目由仓库覆盖文件隐藏，需要在 paper_overrides.json 中恢复。");
    return;
  }
  const shouldHide = typeof force === "boolean" ? force : !state.hidden.has(id);
  if (shouldHide) state.hidden.add(id);
  else state.hidden.delete(id);
  writeStorage(STORAGE.hidden, [...state.hidden]);
  renderPapers();
  renderMaintenance();
  showToast(shouldHide ? "已在此设备隐藏。" : "已恢复到论文库。 ");
}

function isHidden(paper) {
  return Boolean(paper.deleted || state.hidden.has(paper.id));
}

function saveComment(id, value) {
  if (value) state.comments[id] = value;
  else delete state.comments[id];
  writeStorage(STORAGE.comments, state.comments);
  renderPapers();
  renderMaintenance();
  showToast("评论已保存在此设备。 ");
}

function commentFor(paper) {
  return Object.prototype.hasOwnProperty.call(state.comments, paper.id)
    ? state.comments[paper.id]
    : paper.comments || "";
}

function exportOverrides() {
  const ids = new Set([...state.hidden, ...Object.keys(state.comments)]);
  const overrides = {};
  ids.forEach((id) => {
    overrides[id] = {};
    if (state.hidden.has(id)) overrides[id].deleted = true;
    if (state.comments[id]) overrides[id].comments = state.comments[id];
  });
  downloadJson("paper_overrides.json", overrides);
  showToast(`已导出 ${ids.size} 条本地修改。`);
}

function downloadJson(filename, value) {
  const blob = new Blob([JSON.stringify(value, null, 2) + "\n"], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

function qualityScore(paper) {
  const checks = [
    (paper.authors || []).length,
    paper.year,
    paper.publication,
    paper.links?.paper || paper.links?.publication,
    (paper.tags || []).length,
    paper.insight || paper.summary,
    paper.pipeline?.details,
    paper.experiments,
    paper.code_data_status,
    paper.limitations,
  ];
  return checks.filter(Boolean).length;
}

function shortAuthors(authors) {
  if (authors.length <= 3) return authors.join(", ");
  return `${authors.slice(0, 3).join(", ")} et al.`;
}

function renderMarkdown(markdown, basePath = "") {
  const lines = String(markdown || "").replace(/\r\n/g, "\n").split("\n");
  const html = [];
  let index = 0;

  while (index < lines.length) {
    const line = lines[index];
    if (!line.trim()) {
      index += 1;
      continue;
    }

    if (line.trim().startsWith("```")) {
      const language = line.trim().slice(3).trim();
      const code = [];
      index += 1;
      while (index < lines.length && !lines[index].trim().startsWith("```")) {
        code.push(lines[index]);
        index += 1;
      }
      index += 1;
      html.push(`<pre><code${language ? ` data-language="${escapeAttr(language)}"` : ""}>${escapeHtml(code.join("\n"))}</code></pre>`);
      continue;
    }

    const heading = line.match(/^(#{1,5})\s+(.+)$/);
    if (heading) {
      const level = Math.min(heading[1].length, 4);
      html.push(`<h${level}>${inlineMarkdown(heading[2], basePath)}</h${level}>`);
      index += 1;
      continue;
    }

    if (/^\s*(---+|___+)\s*$/.test(line)) {
      html.push("<hr>");
      index += 1;
      continue;
    }

    if (line.trim().startsWith(">")) {
      const quote = [];
      while (index < lines.length && lines[index].trim().startsWith(">")) {
        quote.push(lines[index].replace(/^\s*>\s?/, ""));
        index += 1;
      }
      html.push(`<blockquote>${renderMarkdown(quote.join("\n"), basePath)}</blockquote>`);
      continue;
    }

    if (line.trim().startsWith("|") && index + 1 < lines.length && /^\s*\|?[\s:|-]+\|/.test(lines[index + 1])) {
      const rows = [];
      while (index < lines.length && lines[index].trim().startsWith("|")) {
        if (!/^\s*\|?[\s:|-]+\|/.test(lines[index])) {
          rows.push(lines[index].trim().replace(/^\||\|$/g, "").split("|").map((cell) => cell.trim()));
        }
        index += 1;
      }
      const [head, ...body] = rows;
      html.push(`<table><thead><tr>${head.map((cell) => `<th>${inlineMarkdown(cell, basePath)}</th>`).join("")}</tr></thead><tbody>${body.map((row) => `<tr>${row.map((cell) => `<td>${inlineMarkdown(cell, basePath)}</td>`).join("")}</tr>`).join("")}</tbody></table>`);
      continue;
    }

    const listMatch = line.match(/^\s*(-|\*|\d+\.)\s+(.+)$/);
    if (listMatch) {
      const ordered = /\d+\./.test(listMatch[1]);
      const items = [];
      while (index < lines.length) {
        const match = lines[index].match(/^\s*(-|\*|\d+\.)\s+(.+)$/);
        if (!match || /\d+\./.test(match[1]) !== ordered) break;
        items.push(match[2]);
        index += 1;
      }
      const tag = ordered ? "ol" : "ul";
      html.push(`<${tag}>${items.map((item) => `<li>${inlineMarkdown(item, basePath)}</li>`).join("")}</${tag}>`);
      continue;
    }

    const paragraph = [line.trim()];
    index += 1;
    while (
      index < lines.length &&
      lines[index].trim() &&
      !/^(#{1,5})\s+/.test(lines[index]) &&
      !/^\s*(---+|___+)\s*$/.test(lines[index]) &&
      !/^\s*>/.test(lines[index]) &&
      !/^\s*(-|\*|\d+\.)\s+/.test(lines[index]) &&
      !lines[index].trim().startsWith("```") &&
      !(lines[index].trim().startsWith("|") && index + 1 < lines.length && /^\s*\|?[\s:|-]+\|/.test(lines[index + 1]))
    ) {
      paragraph.push(lines[index].trim());
      index += 1;
    }
    html.push(`<p>${inlineMarkdown(paragraph.join(" "), basePath)}</p>`);
  }
  return html.join("");
}

function inlineMarkdown(text, basePath) {
  let value = escapeHtml(text);
  value = value.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (_, alt, url) => {
    const resolved = resolveUrl(decodeEntities(url), basePath);
    return `<img src="${escapeAttr(resolved)}" alt="${escapeAttr(decodeEntities(alt))}" loading="lazy">`;
  });
  value = value.replace(/\[([^\]]+)\]\((https?:\/\/[^)]+|[^)\s]+)\)/g, (_, label, url) => {
    const resolved = resolveUrl(decodeEntities(url), basePath);
    const external = /^https?:\/\//.test(resolved);
    return `<a href="${escapeAttr(resolved)}"${external ? ' target="_blank" rel="noreferrer"' : ""}>${label}</a>`;
  });
  value = value.replace(/`([^`]+)`/g, "<code>$1</code>");
  value = value.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  value = value.replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, "<em>$1</em>");
  return value;
}

function resolveUrl(url, basePath) {
  if (/^(https?:|data:)/i.test(url) || !basePath) return url;
  try {
    return new URL(url, new URL(basePath, window.location.href)).href;
  } catch {
    return url;
  }
}

function decodeEntities(value) {
  const textarea = document.createElement("textarea");
  textarea.innerHTML = value;
  return textarea.value;
}

function openHashTarget() {
  if (!state.papers.length) return;
  const hash = window.location.hash.slice(1);
  const [kind, encodedId] = hash.split("=");
  const id = encodedId ? decodeURIComponent(encodedId) : "";
  if (kind === "paper" && id && !elements.paperDialog.open) openPaper(id);
  if (kind === "report" && id && !elements.reportDialog.open) {
    switchView("reports");
    openReport(id);
  }
}

function setHash(value) {
  if (window.location.hash.slice(1) !== value) history.pushState(null, "", `#${value}`);
}

function clearHashTarget() {
  if (/^#(paper|report)=/.test(window.location.hash)) history.replaceState(null, "", window.location.pathname + window.location.search);
}

function closeOnBackdrop(event) {
  if (event.target === event.currentTarget) event.currentTarget.close();
}

function readStorage(key, fallback) {
  try {
    const value = JSON.parse(localStorage.getItem(key));
    return value ?? fallback;
  } catch {
    return fallback;
  }
}

function writeStorage(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function showToast(message) {
  elements.toast.textContent = message;
  elements.toast.classList.add("is-visible");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => elements.toast.classList.remove("is-visible"), 2200);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttr(value) {
  return escapeHtml(value);
}
