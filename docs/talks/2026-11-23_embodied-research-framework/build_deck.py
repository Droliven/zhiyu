#!/usr/bin/env python3
"""
Build native editable PowerPoint (.pptx) for:
《以 4D 交互世界表征为核心的具身智能研究规划》
Style inspired by 《4D数据及其具身世界模型》 (Tsinghua academic clean white deck).
"""

import os
from pathlib import Path
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.xmlchemy import OxmlElement

ROOT = Path("/Users/sanqilu/codes/zhiyu")
OUT_DIR = ROOT / "slides" / "embodied-research-framework-ppt"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PPTX = OUT_DIR / "课题组具身智能研究规划.pptx"

# Verified local high-res figures (self-contained in local assets/ + repo shared figures)
FIG_GAF = OUT_DIR / "assets/gaf-method.png"
FIG_GAF_WAM = OUT_DIR / "assets/gaf-wam-method.png"
FIG_GNOMON = OUT_DIR / "assets/gnomon-method.png"
FIG_PI4 = ROOT / "reports/robodojo-slidev/public/media/pi4-arch.png"
FIG_SH = ROOT / "reports/robodojo-slidev/public/media/sh-fig1.png"
FIG_PW = ROOT / "docs/talks/2026-09-15_wam_depth/assets/paper_cards/pointworld_f2.png"
FIG_XWAM = ROOT / "docs/talks/2026-09-15_wam_depth/assets/paper_cards/xwam_f2.png"
FIG_MU0 = ROOT / "docs/talks/2026-09-15_wam_depth/assets/paper_cards/mu0_f3.png"

# Color palette (Tsinghua academic report palette, crisp & restrained)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_CRIMSON = RGBColor(0xA8, 0x12, 0x12)   # Main titles, key highlights, conclusion box
C_PURPLE = RGBColor(0x66, 0x08, 0x74)    # Tsinghua purple accent, divider line, questions
C_NAVY = RGBColor(0x1F, 0x4E, 0x79)      # Methods, representative works, forward flow
C_TEAL = RGBColor(0x0F, 0x66, 0x63)      # 4D core / geometry / ICL accents
C_RUST = RGBColor(0xB8, 0x4A, 0x16)      # Limitations / bottlenecks / residual loop
C_INK = RGBColor(0x1A, 0x23, 0x28)       # Primary dark text
C_SUB = RGBColor(0x3B, 0x48, 0x50)       # Secondary body text
C_MUTED = RGBColor(0x6C, 0x78, 0x80)     # Captions, footers
C_BORDER = RGBColor(0xD5, 0xDC, 0xE2)    # Hairline card border
C_RULE = RGBColor(0xE2, 0xE6, 0xEA)      # Light divider

# Soft fills
F_GRAY = RGBColor(0xF6, 0xF7, 0xF9)
F_BLUE = RGBColor(0xF1, 0xF6, 0xFB)
F_PURPLE = RGBColor(0xF7, 0xF1, 0xF9)
F_TEAL = RGBColor(0xEE, 0xF7, 0xF6)
F_RUST = RGBColor(0xFD, 0xF4, 0xEF)
F_CRIMSON = RGBColor(0xFD, 0xF3, 0xF3)
F_DARK_BUS = RGBColor(0x1B, 0x36, 0x44)

FONT_CN = "PingFang SC"
TOTAL_SLIDES = 18


def new_prs():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def set_notes(slide, text):
    notes = slide.notes_slide
    tf = notes.notes_text_frame
    tf.text = text.strip()


def set_line_dash(shape, dash_val="dash"):
    ln = shape.line._get_or_add_ln()
    prstDash = OxmlElement("a:prstDash")
    prstDash.set("val", dash_val)
    ln.append(prstDash)


def set_cell_border(cell, color_hex="D5DCE2", width_emu="6350"):
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        old = tcPr.find(f"{{{tcPr.nsmap['a']}}}{tag.split(':')[1]}")
        if old is not None:
            tcPr.remove(old)
        ln = OxmlElement(tag)
        ln.set("w", width_emu)
        ln.set("cap", "flat")
        ln.set("cmpd", "sng")
        solidFill = OxmlElement("a:solidFill")
        srgbClr = OxmlElement("a:srgbClr")
        srgbClr.set("val", color_hex)
        solidFill.append(srgbClr)
        ln.append(solidFill)
        tcPr.append(ln)


def set_cell_margins(cell, l=0.08, r=0.08, t=0.05, b=0.05):
    cell.margin_left = Inches(l)
    cell.margin_right = Inches(r)
    cell.margin_top = Inches(t)
    cell.margin_bottom = Inches(b)


def add_rect(slide, x, y, w, h, fill=None, line=None, line_pt=1.0, rounded=False, radius=0.04):
    st = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    sh = slide.shapes.add_shape(st, Inches(x), Inches(y), Inches(w), Inches(h))
    if rounded and len(sh.adjustments) > 0:
        sh.adjustments[0] = radius
    if fill is not None:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    else:
        sh.fill.background()
    if line is not None:
        sh.line.color.rgb = line
        sh.line.width = Pt(line_pt)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    # Zero out default text margins on decorative shapes so narrow bars never expand
    if sh.has_text_frame:
        tf = sh.text_frame
        tf.margin_left = Inches(0)
        tf.margin_right = Inches(0)
        tf.margin_top = Inches(0)
        tf.margin_bottom = Inches(0)
    return sh


def add_textbox(slide, x, y, w, h, text="", size=13, bold=False, color=C_INK,
                align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP, line_spacing=1.22):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = valign
    tf.margin_left = Inches(0.02)
    tf.margin_right = Inches(0.02)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    if text:
        p = tf.paragraphs[0]
        p.alignment = align
        p.line_spacing = line_spacing
        r = p.add_run()
        r.text = text
        r.font.name = FONT_CN
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
    return tb


def add_rich_paragraphs(tf, items, default_size=12.5, default_color=C_SUB,
                        space_after=5, line_spacing=1.24, bullet_prefix=None):
    """
    items: list of list-of-tuples [(text, bold, color_or_None, size_or_None), ...]
    """
    for idx, runs in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_after = Pt(space_after)
        p.line_spacing = line_spacing
        if bullet_prefix:
            rb = p.add_run()
            rb.text = bullet_prefix
            rb.font.name = FONT_CN
            rb.font.size = Pt(default_size)
            rb.font.bold = True
            rb.font.color.rgb = C_CRIMSON if bullet_prefix.strip() in ("▸", "▪") else C_NAVY
        for spec in runs:
            txt = spec[0]
            b = spec[1] if len(spec) > 1 else False
            col = spec[2] if len(spec) > 2 and spec[2] is not None else default_color
            sz = spec[3] if len(spec) > 3 and spec[3] is not None else default_size
            r = p.add_run()
            r.text = txt
            r.font.name = FONT_CN
            r.font.size = Pt(sz)
            r.font.bold = b
            r.font.color.rgb = col


def add_picture_fit(slide, img_path, x, y, max_w, max_h, border_color=None):
    with Image.open(img_path) as im:
        iw, ih = im.size
    ratio = iw / ih
    box_ratio = max_w / max_h
    if ratio >= box_ratio:
        w = max_w
        h = max_w / ratio
    else:
        h = max_h
        w = max_h * ratio
    px = x + (max_w - w) / 2
    py = y + (max_h - h) / 2
    if border_color is not None:
        add_rect(slide, x, y, max_w, max_h, fill=C_WHITE, line=border_color, line_pt=0.8, rounded=False)
    slide.shapes.add_picture(str(img_path), Inches(px), Inches(py), width=Inches(w), height=Inches(h))
    return (px, py, w, h)


def add_arrow_shape(slide, x, y, w, h, direction="right", fill=C_NAVY):
    st_map = {
        "right": MSO_SHAPE.RIGHT_ARROW,
        "down": MSO_SHAPE.DOWN_ARROW,
        "up": MSO_SHAPE.UP_ARROW,
        "left": MSO_SHAPE.LEFT_ARROW,
        "up_down": MSO_SHAPE.UP_DOWN_ARROW,
    }
    sh = slide.shapes.add_shape(st_map[direction], Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def add_chrome(slide, section_label, title, lead_runs, footer_left, page_num, bottom_callout=None, callout_color=C_CRIMSON):
    """
    Signature Tsinghua academic layout inspired by 《4D数据及其具身世界模型》:
    - Clean white slide
    - Top crimson bold title + right purple section tag + full-width Tsinghua purple rule
    - Hollow/solid crimson square lead statement for speaker
    - Optional bottom boxed or bold conclusion strip
    - Subtle footer with source + page number
    """
    # White background
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = C_WHITE

    # Section tag top-right (high enough never to collide with title)
    add_textbox(slide, 8.70, 0.12, 4.08, 0.24, section_label, size=10.2, bold=True,
                color=C_PURPLE, align=PP_ALIGN.RIGHT)

    # Main Title
    add_textbox(slide, 0.55, 0.26, 9.80, 0.52, title, size=21.5, bold=True,
                color=C_CRIMSON, align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.MIDDLE)

    # Tsinghua purple full-width divider line
    add_rect(slide, 0.55, 0.84, 12.23, 0.038, fill=C_PURPLE, line=None)

    # Lead statement with crimson hollow square accent (signature of reference PDF)
    if lead_runs:
        add_rect(slide, 0.58, 1.07, 0.13, 0.13, fill=C_WHITE, line=C_CRIMSON, line_pt=1.8)
        tb = add_textbox(slide, 0.82, 0.94, 11.96, 0.42, "", valign=MSO_ANCHOR.MIDDLE)
        add_rich_paragraphs(tb.text_frame, [lead_runs], default_size=13.5, default_color=C_INK, space_after=0, line_spacing=1.18)

    # Optional bottom conclusion strip (like ref PDF P4 / P7 / P45)
    if bottom_callout is not None:
        fill_bg = F_CRIMSON if callout_color == C_CRIMSON else (F_PURPLE if callout_color == C_PURPLE else F_TEAL)
        box = add_rect(slide, 0.55, 6.46, 12.23, 0.54, fill=fill_bg, line=callout_color, line_pt=1.4, rounded=True, radius=0.08)
        tf = box.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = Inches(0.18)
        tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.04)
        tf.margin_bottom = Inches(0.04)
        add_rich_paragraphs(tf, [bottom_callout], default_size=12.4, default_color=C_INK, space_after=0, line_spacing=1.18)
        for p in tf.paragraphs:
            p.alignment = PP_ALIGN.LEFT

    # Footer separator & text
    add_rect(slide, 0.55, 7.10, 12.23, 0.01, fill=C_RULE, line=None)
    add_textbox(slide, 0.55, 7.14, 10.8, 0.28, footer_left, size=9.5, bold=False, color=C_MUTED)
    add_textbox(slide, 11.55, 7.14, 1.23, 0.28, f"{page_num:02d} / {TOTAL_SLIDES:02d}",
                size=10, bold=True, color=C_SUB, align=PP_ALIGN.RIGHT)


def add_card(slide, x, y, w, h, header_text, header_color=C_NAVY, fill=C_WHITE, border=C_BORDER,
             top_bar=True, header_size=13.2):
    add_rect(slide, x, y, w, h, fill=fill, line=border, line_pt=0.9, rounded=True, radius=0.03)
    if top_bar:
        add_rect(slide, x, y, w, 0.06, fill=header_color, line=None)
        ty = y + 0.11
    else:
        add_rect(slide, x, y, 0.07, h, fill=header_color, line=None)
        ty = y + 0.08
    if header_text:
        add_textbox(slide, x + 0.14, ty, w - 0.24, 0.32, header_text, size=header_size, bold=True, color=header_color)
    return ty + (0.34 if header_text else 0.04)


def add_styled_table(slide, x, y, w, h, headers, rows, col_widths, header_fill=C_NAVY, font_size=11.0, hl_row=None):
    n_rows = len(rows) + 1
    n_cols = len(headers)
    shape = slide.shapes.add_table(n_rows, n_cols, Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = shape.table
    for ci, cw in enumerate(col_widths):
        tbl.columns[ci].width = Inches(cw)

    # Header row
    for ci, htxt in enumerate(headers):
        cell = tbl.cell(0, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_fill
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        set_cell_margins(cell, 0.08, 0.08, 0.05, 0.05)
        set_cell_border(cell, "B8C4CE", "6350")
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run()
        r.text = htxt
        r.font.name = FONT_CN
        r.font.size = Pt(font_size + 0.5)
        r.font.bold = True
        r.font.color.rgb = C_WHITE

    # Data rows
    for ri, rdata in enumerate(rows):
        row_bg = F_TEAL if (hl_row is not None and ri == hl_row) else (C_WHITE if ri % 2 == 0 else F_GRAY)
        for ci, val in enumerate(rdata):
            cell = tbl.cell(ri + 1, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            set_cell_margins(cell, 0.08, 0.08, 0.05, 0.05)
            set_cell_border(cell, "D5DCE2", "6350")
            tf = cell.text_frame
            tf.word_wrap = True
            if isinstance(val, list):
                add_rich_paragraphs(tf, [val], default_size=font_size, default_color=C_SUB, space_after=0, line_spacing=1.18)
            else:
                p = tf.paragraphs[0]
                p.line_spacing = 1.18
                r = p.add_run()
                r.text = val
                r.font.name = FONT_CN
                r.font.size = Pt(font_size)
                r.font.bold = (ci == 0)
                r.font.color.rgb = C_INK if ci == 0 else C_SUB
    return shape


# ==============================================================================
# SLIDE BUILDERS (18 SLIDES)
# ==============================================================================

def build_p01_cover(prs):
    s = blank_slide(prs)
    bg = s.background.fill
    bg.solid()
    bg.fore_color.rgb = C_WHITE

    # Subtle top academic bar (Tsinghua purple)
    add_rect(s, 0, 0, 13.333, 0.14, fill=C_PURPLE)

    # Top tag
    add_textbox(s, 0.8, 0.65, 11.73, 0.35, "课题组具身智能研究规划与科研课题布局 · 汇报稿",
                size=13.5, bold=True, color=C_PURPLE, align=PP_ALIGN.CENTER)

    # Main centered crimson title (directly echoing reference PDF cover)
    add_textbox(s, 0.7, 1.55, 11.93, 1.35, "以 4D 交互世界表征为核心的\n具身智能研究体系与课题规划",
                size=36, bold=True, color=C_CRIMSON, align=PP_ALIGN.CENTER, line_spacing=1.22)

    # Signature full-width crimson rule (echoing reference PDF P1)
    add_rect(s, 0.0, 3.22, 13.333, 0.075, fill=C_CRIMSON)
    add_rect(s, 0.0, 3.31, 13.333, 0.025, fill=C_PURPLE)

    # Subtitle
    add_textbox(s, 1.2, 3.65, 10.93, 0.68,
                "立足组内 4D 几何 WAM 与手物交互重建优势，围绕“几何表征、物理因果、动态操作、\n人类示教迁移与 4D Agent 自进化”五大板块，梳理前沿缺口与可行科研切入点",
                size=15, bold=False, color=C_SUB, align=PP_ALIGN.CENTER, line_spacing=1.35)

    # Five clean pillar chips
    pillars = [
        ("板块一", "4D 几何与持久表征", C_TEAL),
        ("板块二", "物理因果动力学", C_NAVY),
        ("板块三", "动态操作实时闭环", C_RUST),
        ("板块四", "人类示教 ICL 迁移", C_TEAL),
        ("板块五", "4D Agent 与自进化", C_PURPLE),
    ]
    px0 = 0.78
    pw = 2.22
    gap = 0.165
    for i, (k, v, col) in enumerate(pillars):
        x = px0 + i * (pw + gap)
        add_rect(s, x, 4.72, pw, 0.92, fill=F_GRAY, line=C_BORDER, line_pt=0.9, rounded=True, radius=0.06)
        add_rect(s, x, 4.72, pw, 0.06, fill=col)
        add_textbox(s, x + 0.10, 4.86, pw - 0.20, 0.26, k, size=11, bold=True, color=col, align=PP_ALIGN.CENTER)
        add_textbox(s, x + 0.08, 5.14, pw - 0.16, 0.36, v, size=13.5, bold=True, color=C_INK, align=PP_ALIGN.CENTER)

    # Bottom metadata
    add_textbox(s, 0.8, 6.28, 11.73, 0.42,
                "已有基础：GAF · GAF-WAM · Gnomon4D · 4D 重建与 HOI 数据底座",
                size=13.5, bold=True, color=C_INK, align=PP_ALIGN.CENTER)
    add_textbox(s, 0.8, 6.72, 11.73, 0.32, "2026 年 11 月  |  内部战略规划汇报",
                size=12, bold=False, color=C_MUTED, align=PP_ALIGN.CENTER)

    set_notes(s, "老师好，本次汇报采用总—分结构，围绕课题组具身智能的整体科研规划展开。先交代五大方向的宏观背景和总体框架，再逐一进入五个板块，分别汇报当前研究进展、代表性工作、核心局限以及我们具备可行性的科研切入点，最后落到数据底座、协同方式与推进优先级。")


def build_p02_toc(prs):
    s = blank_slide(prs)
    add_chrome(
        s, "汇报目录", "汇报目录：总—分架构与五大科研板块",
        [("按", False), ("“宏观背景与总体框架（总） → 五大核心板块深挖（分） → 底座协同与推进路线（合）”", True, C_CRIMSON), ("三部分展开：", False)],
        "整份汇报共 18 页；每个核心板块均按“研究进展与代表工作 → 现存局限 → 可行科研切入点”两页拆解", 2
    )

    # Left column: Part 1 & Part 3
    y1 = add_card(s, 0.55, 1.56, 4.45, 2.38, "第一部分 · 总体背景与规划框架（P03–P05）", C_CRIMSON, F_CRIMSON, C_CRIMSON, top_bar=True, header_size=13.5)
    tb1 = add_textbox(s, 0.68, y1 + 0.02, 4.18, 1.80)
    add_rich_paragraphs(tb1.text_frame, [
        [("P03 · 顶层洞察：", True, C_INK), ("为何以 4D 表征作为具身“空间中间语言”", False)],
        [("P04 · 演进背景：", True, C_INK), ("五大方向的宏观动因与真实部署四重瓶颈", False)],
        [("P05 · 总体框架：", True, C_INK), ("上→中→下研究体系全景与闭环回流机制", False)],
    ], default_size=12.6, space_after=9, bullet_prefix="▪ ")

    y3 = add_card(s, 0.55, 4.16, 4.45, 2.66, "第三部分 · 协同底座与推进路线（P16–P18）", C_PURPLE, F_PURPLE, C_PURPLE, top_bar=True, header_size=13.5)
    tb3 = add_textbox(s, 0.68, y3 + 0.02, 4.18, 2.08)
    add_rich_paragraphs(tb3.text_frame, [
        [("P16 · 横向贯通：", True, C_INK), ("同一精细插接任务上五大板块如何解耦协同", False)],
        [("P17 · 公共底座：", True, C_INK), ("4D 数据飞轮、四层诊断评测尺与触觉延伸", False)],
        [("P18 · 推进路线：", True, C_INK), ("三阶段科研优先级与 2×2 交叉验证门槛", False)],
    ], default_size=12.6, space_after=9, bullet_prefix="▪ ")

    # Right column: Part 2 (5 modules)
    y2 = add_card(s, 5.25, 1.56, 7.53, 5.26, "第二部分 · 五大核心板块逐一深挖（P06–P15，每板块 2 页）", C_NAVY, C_WHITE, C_NAVY, top_bar=True, header_size=13.5)
    mods = [
        ("板块一", "P06–P07", "4D 几何增强 → 原生持久 4D 场景 Token", "立足 GAF / GAF-WAM / Gnomon4D，结合 π⁴ 攻克重遮挡与尺度畸变", C_TEAL),
        ("板块二", "P08–P09", "物理增强与动作条件因果世界建模", "破除视觉对摩擦/质量欠定：VLM 先验 + 主动探测 + 因果动力学", C_NAVY),
        ("板块三", "P10–P11", "动态操作与事件驱动实时闭环", "针对 42% timing 失败：接触事件与不确定性调度执行时域 + 异步 RTC", C_RUST),
        ("板块四", "P12–P13", "人类示教 ICL 高效跨本体迁移", "联动组内 HOI 4D 重建，抽取 4D 交互关系不变量解耦意图与本体", C_TEAL),
        ("板块五", "P14–P15", "4D-Grounded Agent / Harness 与自进化", "以“预测 4D vs 实测 4D 残差”替代纯 2D 看图与预建 CAD，贯通恢复与进化", C_PURPLE),
    ]
    my = y2 + 0.05
    for tag, pgs, mtitle, mdesc, col in mods:
        add_rect(s, 5.42, my, 7.18, 0.84, fill=F_GRAY, line=C_BORDER, line_pt=0.75, rounded=True, radius=0.05)
        add_rect(s, 5.42, my, 0.08, 0.84, fill=col)
        # Badge
        bsh = add_rect(s, 5.60, my + 0.14, 0.92, 0.28, fill=col, rounded=True, radius=0.15)
        add_textbox(s, 5.60, my + 0.14, 0.92, 0.28, tag, size=10.5, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        add_textbox(s, 5.60, my + 0.48, 0.92, 0.24, pgs, size=10.0, bold=True, color=C_MUTED, align=PP_ALIGN.CENTER)
        add_textbox(s, 6.66, my + 0.10, 5.80, 0.30, mtitle, size=13.2, bold=True, color=C_INK)
        add_textbox(s, 6.66, my + 0.44, 5.80, 0.32, mdesc, size=11.3, bold=False, color=C_SUB)
        my += 0.93

    set_notes(s, "目录一目了然：第一部分 3 页立住大背景和总体框架；第二部分 10 页，五个板块每个板块固定 2 页——第一页梳理最新进展、代表性工作和存在局限，第二页给出我们具体可落地的科研课题；第三部分 3 页讲清横向协同、数据评测底座与分阶段推进节奏。")


def build_p03_background_paradigm(prs):
    s = blank_slide(prs)
    add_chrome(
        s, "一、总体背景 · 顶层逻辑", "宏观背景：具身智能从 VLA 走向 WAM，仍缺“空间中间语言”",
        [("如果", False), ("“代码（Code）”", True, C_NAVY), ("是软件智能可检查、可组合、可执行的中间语言，那么", False),
         ("“4D 交互世界表征”", True, C_CRIMSON), ("正是具身智能急需的空间中间层。", False)],
        "顶层视角承接《4D数据及其具身世界模型》（P4, P47）及 World Labs “3D as Code” 思路", 3,
        bottom_callout=[("课题组战略定位：", True, C_CRIMSON), ("不与工业界盲目拼纯端到端 VLA 参数量，而是发挥大组 ", False),
                        ("3D/4D 重建、HOI 与几何 WAM 优势", True, C_PURPLE), ("，将 4D 交互世界表征做成贯通感知、物理、控制与 Agent 的统一中间层。", False)],
        callout_color=C_CRIMSON
    )

    # Top half: Direct visual echo of ref PDF P4 (Software stack vs Embodied stack)
    # Left stack: Software
    add_rect(s, 0.55, 1.56, 3.15, 0.40, fill=F_GRAY, line=C_BORDER, line_pt=1.0, rounded=True, radius=0.12)
    add_textbox(s, 0.55, 1.56, 3.15, 0.40, "Software Stack（已成熟）", size=13, bold=True, color=C_SUB, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    sw_items = [
        ("人类意图 / Prompt", F_GRAY, C_BORDER, C_INK, False),
        ("Code（代码中间语言）", F_BLUE, C_NAVY, C_NAVY, True),
        ("Runtime / Compiler / 单测验证", F_GRAY, C_BORDER, C_INK, False),
        ("可靠软件行为 & 自主迭代", F_GRAY, C_BORDER, C_INK, False),
    ]
    sy = 2.08
    for idx, (txt, fl, bd, tc, bld) in enumerate(sw_items):
        add_rect(s, 0.68, sy, 2.89, 0.44, fill=fl, line=bd, line_pt=1.6 if bld else 0.9, rounded=True, radius=0.12)
        add_textbox(s, 0.68, sy, 2.89, 0.44, txt, size=12.2, bold=bld, color=tc, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        if idx < 3:
            add_arrow_shape(s, 2.06, sy + 0.47, 0.13, 0.14, "down", C_MUTED)
        sy += 0.64

    # Center shared properties card
    add_rect(s, 3.92, 2.15, 1.66, 2.28, fill=F_RUST, line=C_RUST, line_pt=1.4, rounded=True, radius=0.10)
    add_textbox(s, 3.92, 2.26, 1.66, 0.30, "中间层共同特征", size=12.2, bold=True, color=C_RUST, align=PP_ALIGN.CENTER)
    tb_m = add_textbox(s, 3.98, 2.62, 1.54, 1.72)
    add_rich_paragraphs(tb_m.text_frame, [
        [("可检查", True, C_INK), ("  Verifiable", False, C_MUTED, 10.5)],
        [("可推演", True, C_INK), ("  Predictable", False, C_MUTED, 10.5)],
        [("可组合", True, C_INK), ("  Composable", False, C_MUTED, 10.5)],
        [("可执行", True, C_INK), ("  Executable", False, C_MUTED, 10.5)],
    ], default_size=12.5, space_after=8)

    # Horizontal connector bars at level 2
    add_rect(s, 3.58, 2.93, 0.33, 0.025, fill=C_NAVY)
    add_rect(s, 5.59, 2.93, 0.33, 0.025, fill=C_TEAL)

    # Right stack: Embodied
    add_rect(s, 5.80, 1.56, 3.25, 0.40, fill=F_TEAL, line=C_TEAL, line_pt=1.2, rounded=True, radius=0.12)
    add_textbox(s, 5.80, 1.56, 3.25, 0.40, "Embodied Stack（本组核心范式）", size=13, bold=True, color=C_TEAL, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    emb_items = [
        ("多视角观测 / 任务指令 / 人类示范", F_GRAY, C_BORDER, C_INK, False),
        ("4D 交互世界表征（几何·物理·接触）", F_TEAL, C_TEAL, C_TEAL, True),
        ("4D 前向推演 / 实时控制 / 残差验证", F_GRAY, C_BORDER, C_INK, False),
        ("精细动态操作 & 跨本体闭环进化", F_GRAY, C_BORDER, C_INK, False),
    ]
    sy = 2.08
    for idx, (txt, fl, bd, tc, bld) in enumerate(emb_items):
        add_rect(s, 5.93, sy, 2.99, 0.44, fill=fl, line=bd, line_pt=1.8 if bld else 0.9, rounded=True, radius=0.12)
        add_textbox(s, 5.93, sy, 2.99, 0.44, txt, size=12.0, bold=bld, color=tc, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        if idx < 3:
            add_arrow_shape(s, 7.36, sy + 0.47, 0.13, 0.14, "down", C_TEAL)
        sy += 0.64

    # Right sidebar: Why 3 mainstream routes stall without this middle layer
    add_textbox(s, 9.28, 1.52, 3.50, 0.30, "为何现有三条主流路线各自撞墙？", size=13.2, bold=True, color=C_CRIMSON)

    stalls = [
        ("① 纯端到端 VLA（像素 → 关节）",
         "跳过显式世界状态，黑盒拟合动作；无法预判后果，换视角、换本体或换任务高度依赖重采重训。", C_NAVY, F_BLUE),
        ("② 2D 视频 WAM（像素 → 像素未来）",
         "在二维外观空间想象未来，缺三维尺度、遮挡持久性与接触力学；精细灵巧操作易穿模、断裂。", C_RUST, F_RUST),
        ("③ 2D VLM Agent / 静态 CAD Harness",
         "纯 2D 逐帧审查精细失明且 token 极贵；依赖预建刚体 CAD 的方案难以泛化至未知与动态物体。", C_PURPLE, F_PURPLE),
    ]
    cy = 1.92
    for stitle, sdesc, col, fl in stalls:
        add_rect(s, 9.28, cy, 3.50, 1.32, fill=fl, line=col, line_pt=1.0, rounded=True, radius=0.05)
        add_rect(s, 9.28, cy, 0.08, 1.32, fill=col)
        add_textbox(s, 9.45, cy + 0.08, 3.24, 0.28, stitle, size=11.8, bold=True, color=col)
        add_textbox(s, 9.45, cy + 0.38, 3.24, 0.86, sdesc, size=11.2, bold=False, color=C_SUB, line_spacing=1.22)
        cy += 1.44

    # Bottom subtle note under stacks
    add_rect(s, 0.55, 4.78, 8.50, 1.46, fill=F_GRAY, line=C_BORDER, line_pt=0.9, rounded=True, radius=0.05)
    add_textbox(s, 0.72, 4.88, 8.18, 0.28, "从“数据与感知”走向“行动与系统”的共同缺口", size=12.8, bold=True, color=C_PURPLE)
    tb_b = add_textbox(s, 0.72, 5.18, 8.18, 0.96)
    add_rich_paragraphs(tb_b.text_frame, [
        [("3D/4D 感知前端已迅速成熟", True, C_INK), ("（如 VGGT、π⁴ 已能免标定重建几何与运动），但大多止步于被动观测；", False)],
        [("具身控制与 Agent 迫切需要可查询、可干预、可验证的 4D 交互状态", True, C_CRIMSON), ("——这正是本组五个研究方向共同锚定的科学问题。", False)],
    ], default_size=12.2, space_after=6, bullet_prefix="▸ ")

    set_notes(s, "这一页直接承接刘老师报告里的核心类比：软件栈因为有了 Code 作为可检查、可组合、可执行的中间语言才迎来爆发；而具身智能今天无论纯 VLA、2D 视频 WAM 还是 2D VLM Agent，撞墙的根源都在于缺少等价的 4D 交互世界中间层。这也是我们大组区别于工业界拼算力拼参数的根本差异化定位。")


def build_p04_five_backgrounds(prs):
    s = blank_slide(prs)
    add_chrome(
        s, "一、总体背景 · 五大方向动因", "五大方向的演进背景：从“表观运动学”走向真实交互的四重瓶颈",
        [("五大方向不是外部热点的平行拼盘：在已建立的", False), (" 4D 几何运动学基础", True, C_TEAL),
         ("上，真实物理操作必然依次撞上", False), ("因果、时间、本体、长程", True, C_CRIMSON), ("四堵高墙。", False)],
        "依据：组内 GAF / GAF-WAM / Gnomon4D 实验观察，结合 2026 年前沿（PointWorld, DynamicWAM, Zero-WAM, SpatialHarness, PhyDEX）", 4,
        bottom_callout=[("逻辑自洽性：", True, C_PURPLE), ("几何解决“看见怎么动”，物理解决“为何动及行动后果”，动态解决“何时出手”，ICL 解决“少示范跨本体泛化”，Agent/RSI 解决“长程校验与进化”。", False)],
        callout_color=C_PURPLE
    )

    # Top foundation bar: Direction 1
    add_rect(s, 0.55, 1.54, 12.23, 1.12, fill=F_TEAL, line=C_TEAL, line_pt=1.4, rounded=True, radius=0.05)
    add_rect(s, 0.55, 1.54, 0.12, 1.12, fill=C_TEAL)
    b1 = add_rect(s, 0.80, 1.68, 1.32, 0.30, fill=C_TEAL, rounded=True, radius=0.14)
    add_textbox(s, 0.80, 1.68, 1.32, 0.30, "起点 · 板块一", size=11, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    add_textbox(s, 2.24, 1.66, 9.8, 0.34, "3D/4D 几何增强 WAM —— 已验证“几何运动进入动作路径”的显著价值，但仍属表观运动学",
                size=14.2, bold=True, color=C_INK)
    tb0 = add_textbox(s, 0.80, 2.04, 11.78, 0.56)
    add_rich_paragraphs(tb0.text_frame, [[
        ("已有基础（GAF / GAF-WAM / Gnomon4D）：", True, C_TEAL),
        ("已证明显式高斯场、预测空间记忆与像素对齐运动场能显著提升精细对位与视觉 OOD（如 Gnomon4D 真机视觉 OOD 78.0%, +16pp）。", False),
        ("但当前仍局限在逐帧、准静态、任务条件、单回合开环。", True, C_CRIMSON)
    ]], default_size=12.0, space_after=0)

    # Downward branching arrows to 4 walls
    for cx in (2.02, 5.14, 8.26, 11.30):
        add_arrow_shape(s, cx - 0.11, 2.72, 0.22, 0.22, "down", C_CRIMSON)

    # Four walls in 2x2 grid -> or 4 vertical sleek cards! 4 vertical cards align directly under the 4 arrows!
    walls = [
        ("瓶颈 1 · 因果与物理之墙", "→ 板块二 · 物理增强", C_NAVY, F_BLUE,
         "看得清“怎么动”，\n不懂“为何这么动”",
         [
             [("观测欠定：", True, C_INK), ("外观相同物体，质量、摩擦、刚度与铰链约束可截然不同。", False)],
             [("非反事实：", True, C_INK), ("联合生成期望未来 ≠ 给定任意候选动作的因果后果。", False)],
             [("行业现状：", True, C_NAVY), ("PhyDEX 等评测显示纯 VLA 隐藏物理推演近乎失效。", False)],
         ]),
        ("瓶颈 2 · 时间与延迟之墙", "→ 板块三 · 动态操作", C_RUST, F_RUST,
         "算得准，但世界不等你\n状态在延迟中过期",
         [
             [("准静态假设：", True, C_INK), ("现有 WAM 多采用推理期保持静止 + 固定长块开环执行。", False)],
             [("时机成死因：", True, C_INK), ("DynamicWAM 统计真实动态失败中 timing 误差高达 42%。", False)],
             [("行业现状：", True, C_RUST), ("仅加光流/提帧率无法在接触突变瞬间中断重规划。", False)],
         ]),
        ("瓶颈 3 · 任务与本体之墙", "→ 板块四 · 示教 ICL", C_TEAL, F_TEAL,
         "换任务就要重采重训\n人类示教轨迹难直搬",
         [
             [("构型鸿沟：", True, C_INK), ("人手与机械臂自由度/可达性不同，照搬末端轨迹常失败。", False)],
             [("概念混淆：", True, C_INK), ("人类视频预训练 ≠ 推理期少样本适应，缺跨本体上下文。", False)],
             [("行业现状：", True, C_TEAL), ("Zero-WAM / WICL 依赖配对数据或昂贵离线仿真排练。", False)],
         ]),
        ("瓶颈 4 · 长程与演进之墙", "→ 板块五 · Agent / RSI", C_PURPLE, F_PURPLE,
         "WAM 预测却不核对\n2D Agent 会查却盲",
         [
             [("开环累积错：", True, C_INK), ("端到端策略出错即死，长程多阶段成功率急剧衰减。", False)],
             [("2D 审查瓶颈：", True, C_INK), ("纯 2D Agent 精细极差且 token 昂贵；CAD 方案难泛化。", False)],
             [("行业现状：", True, C_PURPLE), ("跨局自改进缺稠密可定位误差，难区分错在哪一步。", False)],
         ]),
    ]

    wx0 = 0.55
    ww = 2.94
    wgap = 0.156
    for i, (wtag, dirtag, col, fl, whead, bullets) in enumerate(walls):
        x = wx0 + i * (ww + wgap)
        add_rect(s, x, 3.00, ww, 3.30, fill=C_WHITE, line=col, line_pt=1.2, rounded=True, radius=0.04)
        add_rect(s, x, 3.00, ww, 0.38, fill=col)
        add_textbox(s, x + 0.10, 3.03, ww - 0.20, 0.32, wtag, size=11.5, bold=True, color=C_WHITE, valign=MSO_ANCHOR.MIDDLE)
        # Direction badge
        add_rect(s, x + 0.12, 3.47, ww - 0.24, 0.28, fill=fl, rounded=True, radius=0.14)
        add_textbox(s, x + 0.12, 3.47, ww - 0.24, 0.28, dirtag, size=11.0, bold=True, color=col, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        # Headline
        add_textbox(s, x + 0.12, 3.82, ww - 0.24, 0.54, whead, size=13.0, bold=True, color=C_INK, line_spacing=1.18)
        # Divider
        add_rect(s, x + 0.12, 4.40, ww - 0.24, 0.015, fill=C_RULE)
        # Bullets
        tb = add_textbox(s, x + 0.10, 4.48, ww - 0.20, 1.76)
        add_rich_paragraphs(tb.text_frame, bullets, default_size=11.0, space_after=6, line_spacing=1.2, bullet_prefix="▪ ")

    set_notes(s, "这一页向领导讲清五个方向之间的必然逻辑关系。我们从最擅长的板块一 4D 几何出发，但表观运动学在真实场景里会必然撞上四堵墙：物理因果墙、时间延迟墙、跨本体任务墙和长程闭环演进墙。这四堵墙恰好一一导出板块二到板块五，没有一个是硬凑的。")


def build_p05_overall_framework(prs):
    """
    100% NATIVE EDITABLE Top -> Middle -> Bottom framework diagram in PowerPoint!
    """
    s = blank_slide(prs)
    add_chrome(
        s, "一、总体规划 · 全景框架", "总体规划框架：自上而下，由 4D 数据与世界内核驱动三条跃迁",
        [("上层提供 ", False), ("4D 数据与评测", True, C_INK), ("，中核深化", False),
         ("“几何 → 物理”世界模型", True, C_TEAL), ("，经最小 4D 接口驱动三条正交跃迁并", False),
         ("自下而上残差回流", True, C_RUST), ("。", False)],
        "本页全部框图与连线均为 PowerPoint 原生可编辑对象；各板块通过共享 4D 接口解耦，支持独立发论文与渐进融合", 5
    )

    # ===== TOP LAYER: DATA FLYWHEEL & EVAL (y=1.50 .. 2.48) =====
    add_rect(s, 0.55, 1.50, 11.12, 0.98, fill=F_GRAY, line=C_BORDER, line_pt=1.1, rounded=True, radius=0.04)
    add_textbox(s, 0.70, 1.54, 10.8, 0.25, "上层底座 · 4D 数据飞轮与诊断式评测（监督可靠度分层 · 失败驱动闭环）",
                size=11.5, bold=True, color=C_INK)

    top_cols = [
        ("① 人类第一视角 4D 视频 + 组内 HOI 重建", "提供任务规模、手物接触结构与跨本体意图先验"),
        ("② 物理仿真受控干预（Coding Agent 驱动）", "提供反事实动作、失败/滑移样本与精确物理真值"),
        ("③ 高精度光场/真机 4D 采集 & 诊断评测尺", "度量校准与力学锚定；测动作响应、延迟与净收益"),
    ]
    tx = 0.70
    tw = 3.50
    for i, (t1, t2) in enumerate(top_cols):
        add_rect(s, tx, 1.82, tw, 0.56, fill=C_WHITE, line=C_BORDER, line_pt=0.8, rounded=True, radius=0.06)
        add_textbox(s, tx + 0.08, 1.85, tw - 0.16, 0.24, t1, size=10.8, bold=True, color=C_NAVY)
        add_textbox(s, tx + 0.08, 2.10, tw - 0.16, 0.24, t2, size=9.8, bold=False, color=C_SUB)
        tx += tw + 0.16

    # Down arrow Top -> Middle
    add_arrow_shape(s, 5.99, 2.50, 0.24, 0.18, "down", C_TEAL)

    # ===== MIDDLE LAYER: CORE 4D WORLD MODEL DEPTH (y=2.70 .. 4.18) =====
    add_rect(s, 0.55, 2.70, 11.12, 1.48, fill=F_TEAL, line=C_TEAL, line_pt=1.3, rounded=True, radius=0.04)
    add_textbox(s, 0.70, 2.74, 10.8, 0.25, "中核 · 4D 物理世界动作模型纵深（从“看见怎么动”深化到“理解为何动与行动后果”）",
                size=11.5, bold=True, color=C_TEAL)

    # Dir 1 card
    add_rect(s, 0.70, 3.04, 4.82, 1.02, fill=C_WHITE, line=C_TEAL, line_pt=1.2, rounded=True, radius=0.04)
    add_rect(s, 0.70, 3.04, 0.08, 1.02, fill=C_TEAL)
    add_textbox(s, 0.86, 3.07, 4.58, 0.22, "板块一 · 已有护城河与表征升级（运动学 Kinematics）", size=10.2, bold=True, color=C_TEAL)
    add_textbox(s, 0.86, 3.29, 4.58, 0.26, "3D/4D 几何增强 WAM → 原生持久 4D 场景 Token", size=12.2, bold=True, color=C_INK)
    tb_d1 = add_textbox(s, 0.86, 3.55, 4.58, 0.48)
    add_rich_paragraphs(tb_d1.text_frame, [
        [("已有：", True, C_INK), ("GAF · GAF-WAM · Gnomon4D（GeoDelta + 时空读取）", False)],
        [("升级：", True, C_INK), ("免标定感知（π⁴ 路线）+ 跨遮挡持久实体状态", False)],
    ], default_size=10.2, space_after=1, line_spacing=1.15)

    # Arrow Dir 1 -> Dir 2
    add_textbox(s, 5.54, 3.16, 1.12, 0.22, "运动学 → 动力学", size=9.8, bold=True, color=C_CRIMSON, align=PP_ALIGN.CENTER)
    add_arrow_shape(s, 5.66, 3.40, 0.88, 0.22, "right", C_CRIMSON)
    add_textbox(s, 5.54, 3.65, 1.12, 0.36, "外观难分质量\n摩擦与接触力", size=9.0, bold=False, color=C_RUST, align=PP_ALIGN.CENTER, line_spacing=1.12)

    # Dir 2 card
    add_rect(s, 6.68, 3.04, 4.84, 1.02, fill=C_WHITE, line=C_NAVY, line_pt=1.2, rounded=True, radius=0.04)
    add_rect(s, 6.68, 3.04, 0.08, 1.02, fill=C_NAVY)
    add_textbox(s, 6.84, 3.07, 4.60, 0.22, "板块二 · 物理与因果增强（动力学 Dynamics）", size=10.2, bold=True, color=C_NAVY)
    add_textbox(s, 6.84, 3.29, 4.60, 0.26, "动作条件因果预测与隐藏物理辨识", size=12.2, bold=True, color=C_INK)
    tb_d2 = add_textbox(s, 6.84, 3.55, 4.60, 0.48)
    add_rich_paragraphs(tb_d2.text_frame, [
        [("因果：", True, C_INK), ("从期望未来 p(s',a|o,l) 升级为可查询 p(s'|s,a,φ)", False)],
        [("物理：", True, C_INK), ("VLM 材质先验 + 主动轻推探测（远期融触觉力觉）", False)],
    ], default_size=10.2, space_after=1, line_spacing=1.15)

    # Down arrows Middle -> Bus
    add_arrow_shape(s, 2.98, 4.20, 0.20, 0.16, "down", C_TEAL)
    add_arrow_shape(s, 9.00, 4.20, 0.20, 0.16, "down", C_NAVY)

    # ===== SHARED INTERFACE BUS (y=4.38 .. 4.76) =====
    add_rect(s, 0.55, 4.38, 11.12, 0.38, fill=F_DARK_BUS, line=None, rounded=True, radius=0.08)
    tb_bus = add_textbox(s, 0.72, 4.39, 10.80, 0.36, "", valign=MSO_ANCHOR.MIDDLE)
    add_rich_paragraphs(tb_bus.text_frame, [[
        ("共享最小 4D 交互状态接口（中间语言）   ", True, C_WHITE, 11.5),
        ("实体 ID & 坐标系  ·  度量几何与相对运动  ·  接触事件与物理信念  ·  可见性与估计置信度", False, RGBColor(0xD8, 0xEC, 0xE9), 10.8)
    ]], space_after=0)

    # Up-down arrows Bus <-> Bottom
    add_arrow_shape(s, 2.30, 4.78, 0.18, 0.22, "up_down", C_RUST)
    add_arrow_shape(s, 6.02, 4.78, 0.18, 0.22, "up_down", C_TEAL)
    add_arrow_shape(s, 9.74, 4.78, 0.18, 0.22, "up_down", C_PURPLE)

    # ===== BOTTOM LAYER: 3 ORTHOGONAL CAPABILITY BREAKTHROUGHS (y=5.02 .. 6.98) =====
    add_rect(s, 0.55, 5.02, 11.12, 1.96, fill=F_GRAY, line=C_BORDER, line_pt=1.1, rounded=True, radius=0.04)
    add_textbox(s, 0.70, 5.06, 10.8, 0.24, "下层 · 三条正交能力跃迁（基于统一 4D 交互中间层，可独立攻关、按接口对接）",
                size=11.5, bold=True, color=C_NAVY)

    bot_cards = [
        ("板块三 · 时间轴（快与准）", "动态操作与实时闭环", C_RUST, F_RUST, [
            "• 运动学与接触事件驱动自适应执行时域",
            "• 异步实时块执行 (RTC) 抵消感知/推理延迟",
            "• 接触临界与滑移突变触发毫秒级重规划",
        ], "破除：准静态执行在移动/滑移下状态过期"),
        ("板块四 · 任务与本体轴（泛与省）", "人类示教 ICL 高效迁移", C_TEAL, F_TEAL, [
            "• 抽取跨本体不变的 4D 交互关系与接触顺序",
            "• 推理期少样本上下文 / 轻量记忆定义新任务",
            "• 联动组内 HOI 4D 重建，解耦意图与控制",
        ], "破除：新任务依赖重采重训，轨迹难直搬"),
        ("板块五 · 长程与演进轴（长与稳）", "4D Agent / Harness 与自进化", C_PURPLE, F_PURPLE, [
            "• 执行前：4D 世界模型推演筛选候选动作",
            "• 执行后：预测 vs 实测 4D 残差诊断恢复",
            "• 跨回合：高残差定向更新模型与技能库",
        ], "破除：端到端开环不校验，2D Agent 盲"),
    ]
    bx = 0.70
    bw = 3.50
    for axis, btitle, col, fl, blines, wall_txt in bot_cards:
        add_rect(s, bx, 5.33, bw, 1.54, fill=C_WHITE, line=col, line_pt=1.2, rounded=True, radius=0.04)
        add_rect(s, bx, 5.33, bw, 0.055, fill=col)
        add_textbox(s, bx + 0.10, 5.41, bw - 0.20, 0.20, axis, size=10.0, bold=True, color=col)
        add_textbox(s, bx + 0.10, 5.61, bw - 0.20, 0.26, btitle, size=12.4, bold=True, color=C_INK)
        tb = add_textbox(s, bx + 0.10, 5.88, bw - 0.20, 0.66)
        add_rich_paragraphs(tb.text_frame, [[(ln, False)] for ln in blines], default_size=9.9, space_after=1.5, line_spacing=1.15)
        add_rect(s, bx + 0.08, 6.56, bw - 0.16, 0.24, fill=fl, rounded=True, radius=0.08)
        add_textbox(s, bx + 0.12, 6.57, bw - 0.24, 0.22, wall_txt, size=9.4, bold=True, color=col, valign=MSO_ANCHOR.MIDDLE)
        bx += bw + 0.16

    # ===== RIGHT FEEDBACK LOOP (BOTTOM -> MIDDLE & TOP, NATIVE SHAPES) =====
    # Vertical dashed feedback rail
    rail_x = 11.86
    # Bottom horizontal tap from Dir 5 card
    h_bot = add_rect(s, 11.54, 6.08, 0.34, 0.025, fill=C_RUST)
    # Vertical rail line
    v_rail = add_rect(s, rail_x, 1.97, 0.028, 4.135, fill=C_RUST)
    # Left arrows into Middle Core and Top Base
    add_arrow_shape(s, 11.68, 3.44, 0.20, 0.16, "left", C_RUST)
    add_arrow_shape(s, 11.68, 1.91, 0.20, 0.16, "left", C_RUST)

    # Vertical callout box for feedback loop
    add_rect(s, 11.98, 2.15, 0.80, 3.62, fill=F_RUST, line=C_RUST, line_pt=1.0, rounded=True, radius=0.06)
    tb_fb = add_textbox(s, 12.00, 2.24, 0.76, 3.44, "", align=PP_ALIGN.CENTER)
    add_rich_paragraphs(tb_fb.text_frame, [
        [("闭环回流", True, C_CRIMSON, 11.2)],
        [("驱动仿真\n针对补采", False, C_RUST, 10.0)],
        [("↑", True, C_CRIMSON, 13.0)],
        [("定向更新\n世界模型", False, C_RUST, 10.0)],
        [("↑", True, C_CRIMSON, 13.0)],
        [("高 4D 残差\n真机失败", False, C_RUST, 10.0)],
        [("自下而上", True, C_CRIMSON, 9.6)],
    ], space_after=6, line_spacing=1.12)
    for p in tb_fb.text_frame.paragraphs:
        p.alignment = PP_ALIGN.CENTER

    set_notes(s, "这是我们整套研究体系的全景总图，采用自上而下的流动结构：上层是课题组最具壁垒的 4D 数据飞轮与诊断评测；中核完成从 4D 几何运动学到物理因果动力学的纵深演进；通过深色的共享最小 4D 状态接口，向下解耦驱动动态操作、人类示教 ICL 和 4D Agent 自进化三条正交主轴；右侧赤陶箭头则表示运行时的高 4D 残差与真机失败自下而上回流，持续反哺模型和定向补采数据。")


# ------------------------------------------------------------------------------
# MODULE 1: 4D GEOMETRY (P06-P07)
# ------------------------------------------------------------------------------

def build_p06_m1_progress(prs):
    s = blank_slide(prs)
    add_chrome(
        s, "二、板块一 · 4D 几何增强（1/2）", "板块一（进展与局限）：几何 WAM 三条路线与组内已有积累",
        [("组内 ", False), ("GAF / GAF-WAM / Gnomon4D ", True, C_TEAL),
         ("已验证三类几何动作接口；结合 2026 前沿，共同瓶颈在于", False),
         ("像素绑定与重遮挡失锁", True, C_CRIMSON), ("。", False)],
        "来源：组内论文 GAF (arXiv:2506.14135v5)、GAF-WAM (研究稿)、Gnomon4D (arXiv:2611.02474) 及 WAM4D / GAM / GeomVLA / π⁴ 调研", 6,
        bottom_callout=[("共同局限：", True, C_CRIMSON),
                        ("① 绑定图像平面网格，重遮挡即丢身份；② 缺乏跨视角局部度量校准；③ 多为瞬时运动学，缺持续 3D 实体状态与置信度。", False)],
        callout_color=C_CRIMSON
    )

    # Top 3 cards: Lab's 3 real works with original figures
    works = [
        ("① 显式几何场接口 · GAF (arXiv 2506)", FIG_GAF, C_NAVY,
         "4D 高斯场 + ICP 动作初始化",
         [
             [("机制：", True, C_INK), ("前馈预测当前/未来 Gaussian 位移，夹爪 ICP 给 SE(3) 初值再扩散细化。", False)],
             [("验证：", True, C_NAVY), ("RLBench 9 任务 60.4%（无 GAF 51.3%）；显式可渲染，但细化仍需外参。", False)],
         ]),
        ("② 预测空间记忆 · GAF-WAM (研究稿)", FIG_GAF_WAM, C_TEAL,
         "未来 VGGT 对齐 + 双记忆条件化",
         [
             [("机制：", True, C_INK), ("预测视频对齐未来 VGGT，动作并行 cross-attn 读取当前/预测双记忆。", False)],
             [("验证：", True, C_TEAL), ("LIBERO 99.15%、RoboTwin 92.37%；验证“先几何初始化再动作适应”。", False)],
         ]),
        ("③ 时空交互运动场 · Gnomon4D (2611)", FIG_GNOMON, C_PURPLE,
         "GeoDelta + InSAttn / TransAgg",
         [
             [("机制：", True, C_INK), ("联合生成视频、像素对齐 4D 运动场与动作，聚焦接触区与抓放转折。", False)],
             [("验证：", True, C_PURPLE), ("RoboTwin 94.33%；UR5e 真机 ID 82.5% / OOD 78.0%（+16pp）。", False)],
         ]),
    ]
    wx = 0.55
    ww = 3.95
    wgap = 0.19
    for wtitle, wfig, col, wsub, wbuls in works:
        add_rect(s, wx, 1.54, ww, 3.60, fill=C_WHITE, line=C_BORDER, line_pt=0.9, rounded=True, radius=0.04)
        add_rect(s, wx, 1.54, ww, 0.06, fill=col)
        add_textbox(s, wx + 0.12, 1.64, ww - 0.24, 0.28, wtitle, size=11.6, bold=True, color=col)
        add_picture_fit(s, wfig, wx + 0.10, 1.94, ww - 0.20, 1.52, border_color=C_RULE)
        add_textbox(s, wx + 0.12, 3.52, ww - 0.24, 0.26, wsub, size=12.4, bold=True, color=C_INK)
        tb = add_textbox(s, wx + 0.10, 3.80, ww - 0.20, 1.28)
        add_rich_paragraphs(tb.text_frame, wbuls, default_size=10.8, space_after=5, line_spacing=1.20, bullet_prefix="▪ ")
        wx += ww + wgap

    # Bottom strip: External frontier map (compact horizontal bar)
    add_rect(s, 0.55, 5.26, 12.23, 1.08, fill=F_GRAY, line=C_BORDER, line_pt=0.9, rounded=True, radius=0.04)
    add_textbox(s, 0.72, 5.33, 11.9, 0.26, "同期外部前沿脉络与遗留空白（2026 年代表工作）", size=12.0, bold=True, color=C_NAVY)
    tb_f = add_textbox(s, 0.72, 5.61, 11.9, 0.68)
    add_rich_paragraphs(tb_f.text_frame, [
        [("几何蒸馏（WAM4D / Spatial Forcing / Track4Action）：", True, C_INK),
         ("推理期丢弃几何分支，仅靠特征对齐隐式提分，无法向下游提供可检验的 4D 状态；", False)],
        [("几何骨干与统一 4D 感知（GAM / GeomVLA / 3DPWM / π⁴）：", True, C_INK),
         ("GeomVLA 仍需标定深度；π⁴ 已实现 0.5B 免标定统一 4D 几何与轨迹，但仍属被动感知器，未压缩为面向控制的持久实体 Token。", False)],
    ], default_size=11.0, space_after=4, line_spacing=1.18, bullet_prefix="▸ ")

    set_notes(s, "进入板块一。先晒出课题组已经做扎实的三块积木：GAF、GAF-WAM 和 Gnomon4D，它们分别代表显式几何场、预测空间记忆和时空交互运动场三种接口。结合外部 WAM4D、GeomVLA 和最新的 π⁴，可以看到当前几何线的共同天花板非常清楚：绑定 2D 网格、重遮挡丢身份、局部尺度畸变以及缺乏可验证的不确定性估计。")


def build_p07_m1_proposal(prs):
    s = blank_slide(prs)
    add_chrome(
        s, "二、板块一 · 4D 几何增强（2/2）", "板块一（可研课题）：免标定、跨遮挡持久的原生 4D 场景 Token",
        [("立足", False), ("“更原生的 4D 场景 token 表征”", True, C_PURPLE),
         ("目标：借力免标定 4D 前端，将逐帧几何升级为", False),
         ("实体级持久记忆 + 度量锚定 + 可见性置信度", True, C_TEAL), ("。", False)],
        "参考：π⁴ (arXiv:2611.23144) · 《4D数据及其具身世界模型》(P36–38 手部度量标尺, P47) · 3DPWM (arXiv:2607.00148)", 7,
        bottom_callout=[("独立科学贡献：", True, C_TEAL),
                        ("回答“控制究竟需要记住哪些 4D 几何关系”——不以离线重建 PSNR 代替控制收益，而是在相同策略与 token 预算下验证重遮挡操作的真实提升。", False)],
        callout_color=C_TEAL
    )

    # Top visual: pi4 figure showing what perception has solved vs what embodied needs
    add_rect(s, 0.55, 1.54, 12.23, 2.24, fill=C_WHITE, line=C_BORDER, line_pt=0.9, rounded=True, radius=0.04)
    add_textbox(s, 0.72, 1.60, 7.2, 0.26, "前沿基石参照：π⁴（0.5B 单次前向免标定统一 4D 几何与运动，开源权重可用）", size=11.8, bold=True, color=C_NAVY)
    add_textbox(s, 8.20, 1.60, 4.45, 0.26, "→ 对具身控制的直接缺口：被动感知 · 无持久实体记忆", size=11.0, bold=True, color=C_CRIMSON, align=PP_ALIGN.RIGHT)
    add_picture_fit(s, FIG_PI4, 0.70, 1.90, 11.93, 1.80, border_color=None)

    # Bottom 2 cards: Concrete Research Topics & Feasibility
    y_l = add_card(s, 0.55, 3.92, 6.02, 2.40, "可研课题切入点（两个紧密衔接的科学问题）", C_TEAL, F_TEAL, C_TEAL, top_bar=True, header_size=13.0)
    tb_l = add_textbox(s, 0.68, y_l + 0.02, 5.76, 1.86)
    add_rich_paragraphs(tb_l.text_frame, [
        [("课题 1A · 本体/手部锚定的局部度量 4D 表征：", True, C_INK),
         ("全局尺度无法消除局部畸变（刘老师 P36）；以已知尺寸的机械臂/人手为自然标尺，将 π⁴ 类免标定前端实时锚定到机器人基坐标系。", False)],
        [("课题 1B · 跨遮挡持久的实体级 4D 场景 Token：", True, C_INK),
         ("在 Gnomon4D / GAF-WAM 上引入实体级状态槽与可见性管理（可见帧建立对应 → 遮挡期传播信念 → 重现后校正身份），仅高分辨率保留任务交互区。", False)],
    ], default_size=11.8, space_after=8, line_spacing=1.22, bullet_prefix="▪ ")

    y_r = add_card(s, 6.76, 3.92, 6.02, 2.40, "科研可行性与严格对照实验设计", C_NAVY, C_WHITE, C_NAVY, top_bar=True, header_size=13.0)
    tb_r = add_textbox(s, 6.89, y_r + 0.02, 5.76, 1.86)
    add_rich_paragraphs(tb_r.text_frame, [
        [("工程可行性高：", True, C_NAVY),
         ("π⁴（0.5B）与 Gnomon4D / GAF-WAM 代码底座均已就绪，首阶段可冻结下游动作专家，单独训练持久状态读写模块。", False)],
        [("严格控制变量对照：", True, C_INK),
         ("同策略、同训练数据、同 token 预算，对比“逐帧几何 / 时序隐状态 / 显式持久 4D 实体 Token”。", False)],
        [("量化验收指标：", True, C_INK),
         ("重遮挡后身份切换率、重现位姿误差、遮挡插接/抓取成功率与端到端推理延迟。", False)],
    ], default_size=11.8, space_after=7, line_spacing=1.22, bullet_prefix="▸ ")

    set_notes(s, "基于上面的缺口，板块一的具体科研切入点非常扎实可行：前端直接借力 π⁴ 这类免标定 4D 模型，结合刘老师团队已经验证的手部/本体尺度锚定思路解决局部尺度畸变，再在 Gnomon4D 的基础上做出实体级跨遮挡持久 4D 场景 Token。可行性很强，因为可以冻结动作头先做干净的表示对照实验。")


# ------------------------------------------------------------------------------
# MODULE 2: PHYSICS & CAUSAL DYNAMICS (P08-P09)
# ------------------------------------------------------------------------------

def build_p08_m2_progress(prs):
    s = blank_slide(prs)
    add_chrome(
        s, "二、板块二 · 物理与因果增强（1/2）", "板块二（进展与局限）：从“期望未来”走向物理感知与因果世界模型",
        [("前沿正从“生成好看的视频”转向", False), ("动作条件点流与物理评测", True, C_NAVY),
         ("；但", False), ("视觉对隐藏物理属性天生欠定", True, C_CRIMSON), ("，VLM 物理理解亦不等于闭环物理控制。", False)],
        "来源：PointWorld (CVPR 2026) · PhysWorld (2511) · PhysBrain 1.5 (2609) · PhyDEX (2611) · WorldSimProbe (2608)", 8,
        bottom_callout=[("核心诊断：", True, C_CRIMSON),
                        ("① 联合预测 p(未来,动作|观测) 不是可查询的反事实模拟器；② 仅靠被动视频/VQA 无法唯一辨识同外观物体的摩擦、质量与刚度；③ 缺乏接触模式与失败样本。", False)],
        callout_color=C_CRIMSON
    )

    # Left: PointWorld original figure
    add_rect(s, 0.55, 1.54, 4.45, 4.76, fill=C_WHITE, line=C_BORDER, line_pt=0.9, rounded=True, radius=0.04)
    add_rect(s, 0.55, 1.54, 4.45, 0.06, fill=C_NAVY)
    add_textbox(s, 0.68, 1.65, 4.20, 0.30, "代表性工作：PointWorld（CVPR 2026）", size=12.5, bold=True, color=C_NAVY)
    add_picture_fit(s, FIG_PW, 0.68, 1.98, 4.19, 3.16, border_color=C_RULE)
    tb_pw = add_textbox(s, 0.68, 5.20, 4.19, 1.02)
    add_rich_paragraphs(tb_pw.text_frame, [[
        ("机制与启示：", True, C_NAVY),
        ("将机器人候选动作转为 3D 点流，与场景点云同空间预测动作条件位移（~0.1s 推理接 MPC）。证明“动作条件可查询动力学”完全可行，但仍缺隐藏物理参数与接触切换建模。", False)
    ]], default_size=10.6, space_after=0, line_spacing=1.20)

    # Right: Table of 4 representative works & limitations
    add_textbox(s, 5.20, 1.54, 7.58, 0.30, "物理与因果世界建模代表性工作对比", size=13.0, bold=True, color=C_INK)
    headers = ["代表工作", "核心机制与已达成能力", "核心局限与科研空白"]
    rows = [
        ["PointWorld\n(CVPR 2026)",
         "RGB-D + 候选动作点流 → 逐点 3D 位移预测，支持在线 MPC 规划（2M 轨迹）",
         "依赖单帧 RGB-D，未建模隐藏物理参数（摩擦/质量）与遮挡下持久实体"],
        ["PhysWorld\n(2025.11)",
         "视频生成 + 物理重建 + 残差控制，显式引入物理仿真约束",
         "管线重、实时性弱，强依赖可重建刚体资产与离线仿真初始化"],
        ["PhysBrain 1.5\n(2026.09)",
         "统一离散 token 预训练；8B 在 28 个具身物理理解榜均分 72.5",
         "理解均分不等于闭环物理控制能力；被动观察无法消解物理歧义"],
        ["PhyDEX / WorldSimProbe\n(2026.08–11)",
         "动态投掷物理评测（35K 轨迹）与 18K 动作遵循/动力学忠实度诊断",
         "暴露主流 VLA 在未知质量/摩擦下大幅崩溃，急需交互式辨识方法"],
    ]
    add_styled_table(s, 5.20, 1.88, 7.58, 3.24, headers, rows, [1.58, 3.05, 2.95], header_fill=C_NAVY, font_size=10.4)

    # Bottom right insight card
    add_rect(s, 5.20, 5.26, 7.58, 1.04, fill=F_RUST, line=C_RUST, line_pt=1.0, rounded=True, radius=0.05)
    add_textbox(s, 5.36, 5.33, 7.26, 0.24, "关键方法论误区警示", size=11.6, bold=True, color=C_RUST)
    tb_w = add_textbox(s, 5.36, 5.58, 7.26, 0.66)
    add_rich_paragraphs(tb_w.text_frame, [[
        ("“物理增强” ≠ 给 VLM 多喂物理问答数据：", True, C_CRIMSON),
        ("物理隐变量（质量分布、摩擦系数、铰链阻尼）仅靠静态画面不可观测，必须把", False),
        (" VLM 语义先验", True, C_NAVY), (" 与 ", False), ("交互后的物理响应检验", True, C_NAVY), (" 耦合起来。", False)
    ]], default_size=11.2, space_after=0, line_spacing=1.20)

    set_notes(s, "板块二聚焦物理与因果增强。左侧 PointWorld 是 2026 年非常有代表性的动作条件 3D 世界模型；右侧梳理了 PhysWorld、PhysBrain 1.5 和 PhyDEX / WorldSimProbe。这里最想提醒的一个判断是：物理增强绝对不是去刷 VLM 的物理问答榜，因为外观相同的物体质量摩擦不同，被动看图在数学上就是欠定的。")


def build_p09_m2_proposal(prs):
    s = blank_slide(prs)
    add_chrome(
        s, "二、板块二 · 物理与因果增强（2/2）", "板块二（可研课题）：VLM 先验 + 主动交互探测的因果 4D 动力学",
        [("核心思路：动作兼具", False), ("“完成任务”与“探测物理”", True, C_NAVY),
         ("双重角色——VLM 提假设，少量主动轻推校正物理信念", False), (" φ", True, C_CRIMSON),
         ("，支撑可查询动作后果预测。", False)],
        "参考：JanusAct4D 前期设想 · PointWorld (2601) · WorldEcho/WorldSync (2608.24885) · PhyDEX (2611.26565)", 9,
        bottom_callout=[("可证伪核心假设：", True, C_NAVY),
                        ("在外观相同、摩擦/质量不同的受控操作中，1–2 次信息量驱动的主动试探更新物理潜变量，比扩充描述性物理 VQA 更显著提升动作后果校准与成功率。", False)],
        callout_color=C_NAVY
    )

    # Top native 3-stage mechanism pipeline
    add_rect(s, 0.55, 1.54, 12.23, 1.98, fill=F_GRAY, line=C_BORDER, line_pt=0.9, rounded=True, radius=0.04)
    add_textbox(s, 0.72, 1.60, 11.8, 0.26, "拟研机制：双向耦合的物理感知 4D 世界动作模型（JanusAct4D 物理深化）", size=12.2, bold=True, color=C_NAVY)

    stages = [
        ("① VLM 语义物理先验", C_PURPLE, F_PURPLE,
         "从视觉与语言提取初始假设：\n材质类别、可动关节结构、\n粗粒度质量/摩擦先验分布 p(φ₀)"),
        ("② 主动探测与物理信念更新", C_RUST, F_RUST,
         "当物理不确定性超阈值时：\n执行低代价轻推 / 试提 / 微滑，\n按 4D 实测响应贝叶斯更新后验 φ"),
        ("③ 动作条件因果推演与控制", C_TEAL, F_TEAL,
         "前向动力学 p(s' | s, a, φ)：\n比较候选动作后果与滑移风险；\n逆向策略共享 4D 物理状态解码动作"),
    ]
    sx = 0.72
    sw = 3.70
    for idx, (st, col, fl, sd) in enumerate(stages):
        add_rect(s, sx, 1.94, sw, 1.42, fill=fl, line=col, line_pt=1.3, rounded=True, radius=0.05)
        add_textbox(s, sx + 0.12, 2.02, sw - 0.24, 0.28, st, size=12.4, bold=True, color=col)
        add_textbox(s, sx + 0.12, 2.34, sw - 0.24, 0.96, sd, size=11.3, bold=False, color=C_INK, line_spacing=1.25)
        if idx < 2:
            add_arrow_shape(s, sx + sw + 0.08, 2.52, 0.26, 0.22, "right", C_NAVY)
        sx += sw + 0.42

    # Bottom 2 cards: Concrete topics + Scope & Feasibility
    y1 = add_card(s, 0.55, 3.68, 6.02, 2.62, "可落地科研课题（从易到难分步推进）", C_NAVY, C_WHITE, C_NAVY, top_bar=True, header_size=13.0)
    tb1 = add_textbox(s, 0.68, y1 + 0.02, 5.76, 2.06)
    add_rich_paragraphs(tb1.text_frame, [
        [("课题 2A · 动作条件 4D 因果世界模型：", True, C_INK),
         ("在仿真中构造“同初态 + 反事实动作/失败动作”干预对（呼应 WorldEcho），打破联合生成只记专家捷径的顽疾。", False)],
        [("课题 2B · VLM 先验 + 主动交互辨识：", True, C_INK),
         ("不强求恢复全部精确物理参数，而学习“任务相关的低维物理信念 φ”，优先聚焦刚体接触、摩擦突变与关节阻尼。", False)],
        [("远期延伸 · 视觉 4D + 触觉/力觉融合：", True, C_PURPLE),
         ("无力传感时先以视觉微位移更新 φ；真机接入腕部力矩/触觉后无缝并入同一物理信念接口。", False)],
    ], default_size=11.5, space_after=7, line_spacing=1.20, bullet_prefix="▪ ")

    y2 = add_card(s, 6.76, 3.68, 6.02, 2.62, "可行性边界与严格归因实验", C_TEAL, F_TEAL, C_TEAL, top_bar=True, header_size=13.0)
    tb2 = add_textbox(s, 6.89, y2 + 0.02, 5.76, 2.06)
    add_rich_paragraphs(tb2.text_frame, [
        [("仿真先行降低真机门槛：", True, C_TEAL),
         ("先在 Isaac / ManiSkill / RoboTwin 搭建可控刚体摩擦与质量变化子集，用仿真真值验证辨识收敛与干预忠实度。", False)],
        [("四组严格对照：", True, C_INK),
         ("对比“无探测 / VLM 纯先验 / 固定随机探测 / 信息量驱动探测”，严格匹配总交互步数与时间预算。", False)],
        [("避开 PhyDEX 混杂陷阱：", True, C_INK),
         ("将到达抓取阶段与物理推演阶段拆开汇报条件成功率，确保收益真实归因于物理辨识而非抓取精度。", False)],
    ], default_size=11.5, space_after=7, line_spacing=1.20, bullet_prefix="▸ ")

    set_notes(s, "因此板块二给出的科研切入点很克制也很可行：先做刚体摩擦、质量和铰链阻尼，不一口吃成柔性流体；方法上把 VLM 放回最擅长的材质先验位置，靠 1 到 2 次信息量驱动的轻推试探在 4D 空间里校正任务相关的物理潜变量 φ，并构造反事实动作干预数据，让模型真正学出动作条件因果动力学。")


# ------------------------------------------------------------------------------
# MODULE 3: DYNAMIC MANIPULATION (P10-P11)
# ------------------------------------------------------------------------------

def build_p10_m3_progress(prs):
    s = blank_slide(prs)
    add_chrome(
        s, "二、板块三 · 动态操作（1/2）", "板块三（进展与局限）：动态 WAM 的异步去噪与真实时序失败瓶颈",
        [("前沿已通过", False), ("异步去噪（X-WAM）与历史光流/RTC（DynamicWAM）", True, C_NAVY),
         ("迈向动态控制，但实测表明", False), ("时机偏差（42%）仍是首要死因", True, C_CRIMSON), ("。", False)],
        "来源：X-WAM (arXiv:2604.26694) · DynamicWAM (arXiv:2608.00793, App. D.8 50例失败拆解) · Gnomon4D 补充材料 p8", 10,
        bottom_callout=[("现存核心局限：", True, C_CRIMSON),
                        ("① 固定动作块长度无法适配“自由接近”与“接触临界”的巨大频率差异；② 遮挡导致历史光流过期；③ 单靠压缩去噪步数无法在接触突变瞬间中断旧计划。", False)],
        callout_color=C_CRIMSON
    )

    # Left: X-WAM original figure (asynchronous denoising)
    add_rect(s, 0.55, 1.54, 6.25, 4.76, fill=C_WHITE, line=C_BORDER, line_pt=0.9, rounded=True, radius=0.04)
    add_rect(s, 0.55, 1.54, 6.25, 0.06, fill=C_NAVY)
    add_textbox(s, 0.68, 1.64, 6.00, 0.28, "代表进展 ①：X-WAM（2026.04）异步噪声采样解耦动作与视频延迟", size=11.8, bold=True, color=C_NAVY)
    add_picture_fit(s, FIG_XWAM, 0.68, 1.96, 5.99, 3.30, border_color=C_RULE)
    tb_x = add_textbox(s, 0.68, 5.32, 5.99, 0.90)
    add_rich_paragraphs(tb_x.text_frame, [[
        ("核心启示：", True, C_NAVY),
        ("动作采用少步先去噪（RTX 3090 延迟由 4665ms 降至 1033ms；真机 5090D + RTC 约 300ms/chunk），显著缓解高维视频拖慢控制；但对高速动态交互仍显笨重且固定时域。", False)
    ]], default_size=10.6, space_after=0, line_spacing=1.20)

    # Right top: DynamicWAM summary + native horizontal bar chart of failure breakdown!
    add_rect(s, 7.00, 1.54, 5.78, 2.86, fill=C_WHITE, line=C_RUST, line_pt=1.1, rounded=True, radius=0.04)
    add_rect(s, 7.00, 1.54, 5.78, 0.06, fill=C_RUST)
    add_textbox(s, 7.14, 1.65, 5.50, 0.28, "代表进展 ②：DynamicWAM（2026.08）真实动态失败拆解", size=12.0, bold=True, color=C_RUST)
    add_textbox(s, 7.14, 1.95, 5.50, 0.52,
                "引入历史光流 + 运动学 token（位移/速度/加速度）+ 真机 RTC，12 项真实动态任务 SR 46.7%。但 50 例失败拆解暴露致命短板：",
                size=10.8, bold=False, color=C_SUB, line_spacing=1.20)

    # Native bar chart (4 bars)
    bars = [
        ("时机偏差 (Timing)", 42, C_CRIMSON),
        ("空间位置误差", 26, C_RUST),
        ("遮挡与跟踪丢失", 18, C_NAVY),
        ("接触后滑移", 10, C_MUTED),
    ]
    by = 2.58
    for label, pct, bcol in bars:
        add_textbox(s, 7.14, by, 1.68, 0.30, label, size=10.8, bold=(pct == 42), color=C_INK if pct == 42 else C_SUB, valign=MSO_ANCHOR.MIDDLE)
        # Track background
        add_rect(s, 8.86, by + 0.05, 3.10, 0.22, fill=F_GRAY, line=C_RULE, line_pt=0.6, rounded=True, radius=0.12)
        # Fill bar (max 50% scale so 42% looks impactful and proportionate)
        bw = 3.10 * (pct / 50.0)
        add_rect(s, 8.86, by + 0.05, bw, 0.22, fill=bcol, rounded=True, radius=0.12)
        add_textbox(s, 12.02, by, 0.65, 0.30, f"{pct}%", size=11.5, bold=True, color=bcol, valign=MSO_ANCHOR.MIDDLE)
        by += 0.42

    # Right bottom: Lab's current gap
    add_rect(s, 7.00, 4.54, 5.78, 1.76, fill=F_RUST, line=C_RUST, line_pt=1.0, rounded=True, radius=0.04)
    add_textbox(s, 7.14, 4.62, 5.50, 0.26, "组内现状与差异化思考（避免重复造轮子）", size=12.0, bold=True, color=C_RUST)
    tb_g = add_textbox(s, 7.14, 4.92, 5.50, 1.30)
    add_rich_paragraphs(tb_g.text_frame, [
        [("现状边界：", True, C_INK), ("Gnomon4D 虽采用 10Hz 动作网格，但推理期机械臂保持静止、每次执行固定 16 步，本质属准静态协议。", False)],
        [("破局关键：", True, C_CRIMSON), ("DynamicWAM 已占领“加历史光流 + 运动 token”，我们不能简单复刻，而必须直击 42% timing 失败根因——把时间调度做成核心机制。", False)],
    ], default_size=11.0, space_after=6, line_spacing=1.20, bullet_prefix="▸ ")

    set_notes(s, "板块三看动态操作。X-WAM 做了异步去噪来解耦动作与视频延迟，DynamicWAM 做了历史光流、运动学 token 和真机 RTC。但仔细看 DynamicWAM 附录的失败拆解图，42% 的失败来自时机偏差。这提醒我们，跟在后面再做一遍运动 token 创新性不够，真正的硬骨头在于接触时机与自适应时间调度。")


def build_p11_m3_proposal(prs):
    s = blank_slide(prs)
    add_chrome(
        s, "二、板块三 · 动态操作（2/2）", "板块三（可研课题）：接触事件与不确定性驱动的自适应实时闭环",
        [("将 Gnomon4D 的", False), ("时空交互转折感知（TransAgg）", True, C_TEAL),
         ("升级为", False), ("事件触发自适应执行时域 + 异步 RTC", True, C_CRIMSON),
         ("，把控制从空间扩展到时间。", False)],
        "参考：DynamicWAM (2608.00793) · Gnomon4D 交互转折机制 (TransAgg) · 异步块执行 RTC 范式", 11,
        bottom_callout=[("科研定位与价值：", True, C_RUST),
                        ("先在严格等延迟预算下分离“预测更准”与“反应更快”的净贡献，解决动态抓取、移动装配与防滑移的真实时序瓶颈。", False)],
        callout_color=C_CRIMSON
    )

    # Top native timeline comparison diagram
    add_rect(s, 0.55, 1.54, 12.23, 2.08, fill=C_WHITE, line=C_BORDER, line_pt=1.0, rounded=True, radius=0.04)
    add_textbox(s, 0.72, 1.62, 11.8, 0.28, "执行机制对比：传统固定块准静态执行 vs 4D 接触事件驱动的异步实时闭环", size=12.6, bold=True, color=C_INK)

    # Row 1: Quasi-static
    add_textbox(s, 0.72, 2.04, 1.90, 0.52, "现有准静态 WAM\n固定 chunk · 推理保持", size=11.2, bold=True, color=C_SUB, valign=MSO_ANCHOR.MIDDLE)
    segs1 = [
        (2.70, 2.05, "推理阻塞 (机械臂保持)", F_RUST, C_RUST, C_RUST, True),
        (4.82, 3.15, "开环执行固定长块 H=16（目标已移位）", F_BLUE, C_NAVY, C_NAVY, False),
        (8.04, 1.65, "推理阻塞", F_RUST, C_RUST, C_RUST, True),
        (9.76, 2.84, "开环执行（错过接触窗口）", F_BLUE, C_NAVY, C_NAVY, False),
    ]
    for sx, sw, txt, fl, bd, tc, dash in segs1:
        sh = add_rect(s, sx, 2.08, sw, 0.44, fill=fl, line=bd, line_pt=1.1, rounded=True, radius=0.10)
        if dash:
            set_line_dash(sh, "dash")
        add_textbox(s, sx, 2.08, sw, 0.44, txt, size=10.6, bold=True, color=tc, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # Row 2: Event-driven dynamic
    add_textbox(s, 0.72, 2.74, 1.90, 0.52, "拟研 4D 事件驱动闭环\n异步 RTC + 自适应时域", size=11.2, bold=True, color=C_TEAL, valign=MSO_ANCHOR.MIDDLE)
    segs2 = [
        (2.70, 3.05, "自由接近：长块高吞吐 + 运动趋势外推", F_TEAL, C_TEAL, C_TEAL, False),
        (5.82, 2.05, "接触临界：短块高频修正", F_PURPLE, C_PURPLE, C_PURPLE, False),
        (7.94, 1.15, "滑移中断!", C_CRIMSON, C_CRIMSON, C_WHITE, False),
        (9.16, 2.00, "异步重规划 (不阻塞)", F_PURPLE, C_PURPLE, C_PURPLE, False),
        (11.23, 1.37, "稳态完成", F_TEAL, C_TEAL, C_TEAL, False),
    ]
    for sx, sw, txt, fl, bd, tc, _ in segs2:
        add_rect(s, sx, 2.78, sw, 0.44, fill=fl, line=bd, line_pt=1.3, rounded=True, radius=0.10)
        add_textbox(s, sx, 2.78, sw, 0.44, txt, size=10.5, bold=True, color=tc, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # Bottom 2 cards: Research Topics & Evaluation Protocol
    y1 = add_card(s, 0.55, 3.80, 6.02, 2.50, "拟解科学问题与可行技术路线", C_RUST, F_RUST, C_RUST, top_bar=True, header_size=13.0)
    tb1 = add_textbox(s, 0.68, y1 + 0.02, 5.76, 1.94)
    add_rich_paragraphs(tb1.text_frame, [
        [("课题 3A · 接触事件与置信度驱动的自适应执行时域：", True, C_INK),
         ("利用 4D 交互状态的相对速度、接触事件概率与估计方差，动态决定动作块执行长度——自由空间省算力，接触临界高频纠偏。", False)],
        [("课题 3B · 到达时刻—空间位置联合预测 + 异步中断：", True, C_INK),
         ("显式将系统测量延迟 Δt 作为条件输入动作头，预测“动作到达时刻”的目标 4D 位置；遇滑移/外力突变立即打断旧块。", False)],
    ], default_size=11.6, space_after=8, line_spacing=1.22, bullet_prefix="▪ ")

    y2 = add_card(s, 6.76, 3.80, 6.02, 2.50, "严谨对照设计与可行性验证", C_NAVY, C_WHITE, C_NAVY, top_bar=True, header_size=13.0)
    tb2 = add_textbox(s, 6.89, y2 + 0.02, 5.76, 1.94)
    add_rich_paragraphs(tb2.text_frame, [
        [("五组公平调度对照：", True, C_NAVY),
         ("固定时域 / 定周期重规划 / 随机触发 / 仅置信度触发 / 接触事件+置信度触发（同骨干、同 GPU 算力预算）。", False)],
        [("核心定量曲线：", True, C_INK),
         ("扫描目标运动速度与人工注入延迟，汇报“成功率—延迟曲线”、错过接触事件率、动作平滑度与每任务推理次数。", False)],
        [("渐进落地：", True, C_INK),
         ("先冻结现有几何预测器验证时间调度增益，再考虑轻量快速动作头或单步蒸馏进一步压低延迟。", False)],
    ], default_size=11.6, space_after=6, line_spacing=1.20, bullet_prefix="▸ ")

    set_notes(s, "板块三的可行课题非常聚焦：直接把我们 Gnomon4D 里已有的交互转折感知延伸为动态执行调度器。上方时序图直观对比了准静态固定块和 4D 事件驱动闭环的区别。实验上也非常干净，先冻结预测器做五组调度对照，直接拉出成功率对速度和延迟的曲线。")


# ------------------------------------------------------------------------------
# MODULE 4: HUMAN DEMO ICL (P12-P13)
# ------------------------------------------------------------------------------

def build_p12_m4_progress(prs):
    s = blank_slide(prs)
    add_chrome(
        s, "二、板块四 · 人类示教 ICL 迁移（1/2）", "板块四（进展与局限）：人类视频迁移与上下文学习的四条路线",
        [("2026 年人类示教迁移快速升温，但必须严格区分", False),
         ("预训练、纯 ICL、测试期快记忆与仿真排练", True, C_TEAL),
         ("四条路线及其真实代价。", False)],
        "来源：μ₀ (2606.13769) · EgoWAM (CoRL 2026) · Zero-WAM (2608.26103) · WAM-TTT (2607.06988) · WICL/RoboScript (2611.12885)", 12,
        bottom_callout=[("核心局限：", True, C_CRIMSON),
                        ("① 像素视频直接作示范上下文易受视角、背景与人手外观干扰；② 少示范常含意图歧义或超出机器人可达性；③ 排练型方案推理开销巨大且偏离线。", False)],
        callout_color=C_CRIMSON
    )

    # Left: mu0 original figure
    add_rect(s, 0.55, 1.54, 5.40, 4.76, fill=C_WHITE, line=C_BORDER, line_pt=0.9, rounded=True, radius=0.04)
    add_rect(s, 0.55, 1.54, 5.40, 0.06, fill=C_TEAL)
    add_textbox(s, 0.68, 1.64, 5.15, 0.28, "代表思路：μ₀（2026.06）以 3D 交互轨迹解耦视频与本体", size=11.6, bold=True, color=C_TEAL)
    add_picture_fit(s, FIG_MU0, 0.68, 1.96, 5.14, 3.24, border_color=C_RULE)
    tb_m = add_textbox(s, 0.68, 5.26, 5.14, 0.96)
    add_rich_paragraphs(tb_m.text_frame, [[
        ("启发与边界：", True, C_TEAL),
        ("用语义交互点的 3D B-spline 轨迹作为视频预训练与机器人动作专家的桥梁，验证“交互中心运动”跨本体共享有效；但仍属视频预训练，而非推理期零微调的新任务 ICL。", False)
    ]], default_size=10.6, space_after=0, line_spacing=1.20)

    # Right: Table clearly separating 4 routes
    add_textbox(s, 6.15, 1.54, 6.63, 0.30, "四条人类示教迁移路线的机制对比与真实边界", size=12.8, bold=True, color=C_INK)
    headers = ["路线类别", "代表工作", "核心机制与数据/代价边界"]
    rows = [
        ["视频预训练\n(非 ICL)",
         "EgoWAM / μ₀ /\nGnomon4D",
         "利用海量第一视角人类视频学习通用运动先验；换新任务仍需目标机器人微调，不能称为测试期 ICL"],
        ["纯上下文 ICL\n(冻结权重)",
         "Zero-WAM\n(2026.08)",
         "以人类视频为上下文条件（RoboTwin 未见 7 任务 46.95%）；但预训练仍需 74.2K 人机配对与任务适配数据"],
        ["测试期快记忆\n(TTT 适配)",
         "WAM-TTT\n(2026.07)",
         "冻结主干，以自监督视频预测将人类视频写入轻量 KV 记忆；测试期有记忆适配，介于纯 ICL 与微调之间"],
        ["模拟排练型 ICL\n(Agentic)",
         "WICL / RoboScript\n(2026.11)",
         "1 条示教 + 模拟排练写入 Task Memory（RoboTwin 83.4%）；平均 54.7 次模型调用/局，真机偏离线序列执行"],
    ]
    add_styled_table(s, 6.15, 1.88, 6.63, 4.42, headers, rows, [1.35, 1.38, 3.90], header_fill=C_TEAL, font_size=10.3)

    set_notes(s, "板块四梳理人类示教 ICL。文献里很容易把视频预训练、纯 ICL、测试期快记忆和仿真排练混为一谈，所以右边这张表特意帮大家划清了界限。同时左图 μ₀ 给了一个很好的启发：3D 交互轨迹天然比原始像素更容易跨本体共享。")


def build_p13_m4_proposal(prs):
    s = blank_slide(prs)
    add_chrome(
        s, "二、板块四 · 人类示教 ICL 迁移（2/2）", "板块四（可研课题）：联动 HOI 4D 重建的少示教跨本体迁移",
        [("不照搬人手轨迹，而是抽取", False),
         ("跨本体不变的 4D 交互关系与接触顺序", True, C_TEAL), ("，直接打通大组", False),
         (" HOI 重建线与具身策略线", True, C_PURPLE), ("。", False)],
        "联动组内基础：RealHOI / EgoMetriCap / HandCrafter / 像素对齐遮挡鲁棒 HOI 重建 + 具身 WAM 策略线", 13,
        bottom_callout=[("大组独有壁垒：", True, C_PURPLE),
                        ("外界多用原始 2D 视频或粗糙点云做示教提示，我们可将大组长期积累的高精度手-物 4D 重建与接触理解直接转化为高信噪比 ICL 示范编码器。", False)],
        callout_color=C_PURPLE
    )

    # Top 3-stage cross-embodiment pipeline
    add_rect(s, 0.55, 1.54, 12.23, 1.98, fill=F_GRAY, line=C_BORDER, line_pt=0.9, rounded=True, radius=0.04)
    add_textbox(s, 0.72, 1.60, 11.8, 0.26, "拟研机制：基于 4D 交互不变量的跨本体少示范上下文迁移（Intent–Embodiment Decoupling）",
                size=12.2, bold=True, color=C_TEAL)

    steps = [
        ("① 少量人类示范 + 组内 HOI 重建", C_NAVY, F_BLUE,
         "输入 1–5 段任意视角人类操作视频\n经组内第一视角/单视角 4D HOI 重建：\n恢复度量手-物位姿与接触区域分割"),
        ("② 抽取 4D 交互不变量上下文", C_TEAL, F_TEAL,
         "彻底剥离人手形态、衣着与背景：\n保留物体-物体目标关系 g、接触阶段顺序 c\n及关键交互相对运动（与本体无关）"),
        ("③ 机器人按自身动力学重实现", C_PURPLE, F_PURPLE,
         "冻结策略主干，以 4D 关系上下文条件化\n读取当前机器人场景 4D 状态；\n检验可达性并生成本体专属可执行动作"),
    ]
    sx = 0.72
    sw = 3.70
    for idx, (st, col, fl, sd) in enumerate(steps):
        add_rect(s, sx, 1.94, sw, 1.42, fill=fl, line=col, line_pt=1.3, rounded=True, radius=0.05)
        add_textbox(s, sx + 0.12, 2.02, sw - 0.24, 0.28, st, size=12.0, bold=True, color=col)
        add_textbox(s, sx + 0.12, 2.34, sw - 0.24, 0.96, sd, size=11.1, bold=False, color=C_INK, line_spacing=1.24)
        if idx < 2:
            add_arrow_shape(s, sx + sw + 0.08, 2.52, 0.26, 0.22, "right", C_TEAL)
        sx += sw + 0.42

    # Bottom 2 cards
    y1 = add_card(s, 0.55, 3.68, 6.02, 2.62, "可研核心课题与创新切入点", C_TEAL, C_WHITE, C_TEAL, top_bar=True, header_size=13.0)
    tb1 = add_textbox(s, 0.68, y1 + 0.02, 5.76, 2.06)
    add_rich_paragraphs(tb1.text_frame, [
        [("课题 4A · 4D 交互关系上下文 vs 原始视频上下文：", True, C_INK),
         ("验证将人类示范压缩为“目标关系 + 接触阶段 + 相对运动”后，在跨视角、跨物体、跨本体未见任务上的 1/3/5-shot 泛化优势。", False)],
        [("课题 4B · 示教意图歧义与可实现性判断：", True, C_INK),
         ("并非所有人类灵巧动作都可由二指夹爪直接实现；研究基于机器人运动学约束的可达性判别，以及意图不明时的主动补示范请求。", False)],
    ], default_size=11.6, space_after=8, line_spacing=1.22, bullet_prefix="▪ ")

    y2 = add_card(s, 6.76, 3.68, 6.02, 2.62, "严格评测协议与可行性保障", C_NAVY, F_BLUE, C_NAVY, top_bar=True, header_size=13.0)
    tb2 = add_textbox(s, 6.89, y2 + 0.02, 5.76, 2.06)
    add_rich_paragraphs(tb2.text_frame, [
        [("拆开“任务迁移”与“本体学习”：", True, C_NAVY),
         ("先固定目标机器人的基础操作原语/策略能力，单独评测不同示范上下文表示带来的新任务迁移净收益。", False)],
        [("四维严格隔离切分：", True, C_INK),
         ("隔离未见任务族、未见物体、未见视角与未见演示者；分别对比 0/1/3/5 示范，并将快记忆适配与模拟排练算力单列计入预算。", False)],
        [("内部协同低成本启动：", True, C_INK),
         ("直接复用组内现有 HOI 4D 重建流水线处理人类示范视频，无需另起炉灶采集海量配对遥操作数据。", False)],
    ], default_size=11.6, space_after=6, line_spacing=1.20, bullet_prefix="▸ ")

    set_notes(s, "这一页把大组两大主力——HOI 手物交互 4D 重建和具身智能——真正拧在了一起。我们不用原始视频直接喂给策略，而是用组内 HOI 4D 重建把人类示范压缩成与本体无关的 4D 交互关系上下文。这既能回答学术界非常硬核的表示问题，又有大组独一无二的技术积累做支撑。")


# ------------------------------------------------------------------------------
# MODULE 5: 4D AGENT / HARNESS / RSI (P14-P15)
# ------------------------------------------------------------------------------

def build_p14_m5_progress(prs):
    s = blank_slide(prs)
    add_chrome(
        s, "二、板块五 · 4D Agent / Harness / RSI（1/2）", "板块五（进展与局限）：具身 Agent、Harness 与自进化盲区",
        [("RoboDojo 与 SpatialHarness 验证了", False), ("运行时闭环与 3D 接口", True, C_PURPLE),
         ("威力，但卡在 ", False), ("2D 精细失明、CAD 依赖与稀疏成败信号", True, C_CRIMSON), ("。", False)],
        "来源：SpatialHarness (2610.12457) · RoboDojo 调研 (GO-3 / SenseNova-RoboRSI / R²SI) · LAW (2610.23334) · Physical RSI 综述 (2610.29677)", 14,
        bottom_callout=[("关键洞察：", True, C_PURPLE),
                        ("Agentic 路线不是“改提示词循环重试”，真正拉开差距的是 Harness（决定看多清、查多准）与跨局进化机制（决定经验能否真正沉淀并泛化）。", False)],
        callout_color=C_PURPLE
    )

    # Left: SpatialHarness Fig 1
    add_rect(s, 0.55, 1.54, 5.25, 4.76, fill=C_WHITE, line=C_BORDER, line_pt=0.9, rounded=True, radius=0.04)
    add_rect(s, 0.55, 1.54, 5.25, 0.06, fill=C_PURPLE)
    add_textbox(s, 0.68, 1.64, 5.00, 0.28, "标杆证据：SpatialHarness（2026.10）暴露 3D 接触区 +65pp", size=11.5, bold=True, color=C_PURPLE)
    add_picture_fit(s, FIG_SH, 0.68, 1.96, 4.99, 3.22, border_color=C_RULE)
    tb_sh = add_textbox(s, 0.68, 5.24, 4.99, 0.98)
    add_rich_paragraphs(tb_sh.text_frame, [[
        ("实验启示与硬伤：", True, C_PURPLE),
        ("不改策略权重，仅靠在线同步 3D 场景与无遮挡虚拟视角，四项真机任务均值 18.3% → 83.3%（插头 26.7% → 66.7%）。但强依赖预建刚体 CAD、标定外参且同步耗时高。", False)
    ]], default_size=10.5, space_after=0, line_spacing=1.20)

    # Right: Table of 4 representative tracks
    add_textbox(s, 6.00, 1.54, 6.78, 0.30, "具身 Agent / Harness / RSI 代表性工作拆解", size=12.8, bold=True, color=C_INK)
    headers = ["系统 / 文献", "核心机制与成绩", "存在的问题与局限"]
    rows = [
        ["SenseNova-RoboRSI /\nWorldScape-R²SI",
         "高频 VLM 审查（每 4 步/每 chunk）+ 经验包或权重回流；开放与长程强",
         "单任务耗千万级 token；纯 2D 审查致精细操作极差（R²SI 精细仅 23.51）"],
        ["GO-3 Nano /\nPhysicalRSI",
         "Python 状态机主控 + 失败兜底切 WAM/VLA（GO-3 精细 78.65）",
         "任务级脚本高度特化，换随机布局急剧退化（PhysicalRSI 随机仅 11.04）"],
        ["LAW / Geometric\nAbstraction (2610–11)",
         "语义子任务进度 + 异步验证；或结构化程序 + 实时几何重绑定",
         "语义进度难定位毫米级几何偏差；几何残差未认证物理接触与稳定性"],
        ["Physical RSI 综述 /\n123 Rounds (2609–10)",
         "严格区分局内重试、跨局自改进与改进机制自身的递归增益",
         "现有物理 AI 尚无严格归因于“递归”的收益；依赖稀疏成败易致记忆误导"],
    ]
    add_styled_table(s, 6.00, 1.88, 6.78, 4.42, headers, rows, [1.62, 2.52, 2.64], header_fill=C_PURPLE, font_size=10.2)

    set_notes(s, "板块五分析 Agent、Harness 和 RSI。左图 SpatialHarness 给了一个极具说服力的证据：同一冻结策略，只要把接触区 3D 视角暴露清楚，四项真机任务暴涨 65 个百分点。但右侧汇总了 RoboDojo 和 10 月最新前沿，三大盲区清晰可见：2D 审查又贵又盲、CAD 方案难泛化、跨局改进只有稀疏成败信号不知道具体错在哪。")


def build_p15_m5_proposal(prs):
    s = blank_slide(prs)
    add_chrome(
        s, "二、板块五 · 4D Agent / Harness / RSI（2/2）", "板块五（可研课题）：Verify in 4D 残差验证与闭环进化",
        [("核心创新：将", False), ("“对齐后的预测 4D 与实测 4D 之差”", True, C_CRIMSON),
         ("作为统一反馈信号，同时驱动", False), ("执行前筛选、执行后恢复与跨局自改进", True, C_PURPLE), ("。", False)],
        "参考：SpatialHarness (2610) · LAW (2610) · Geometric Abstraction (2611) · Physical RSI 综述 (2610.29677)", 15,
        bottom_callout=[("相对前沿的差异化：", True, C_PURPLE),
                        ("免 CAD 替代 SpatialHarness 的刚体同步；用稠密可定位的 4D 残差替代 LAW 的纯语义进度和 RSI 的稀疏 0/1 成败门禁。", False)],
        callout_color=C_PURPLE
    )

    # Top: Native 4-step Verify in 4D closed loop
    add_rect(s, 0.55, 1.54, 12.23, 2.08, fill=F_GRAY, line=C_BORDER, line_pt=0.9, rounded=True, radius=0.04)
    add_textbox(s, 0.72, 1.60, 11.8, 0.26, "核心机制 · Verify in 4D 运行时 Harness 与跨回合进化闭环", size=12.2, bold=True, color=C_PURPLE)

    vsteps = [
        ("1. 可检 4D 子目标", C_NAVY, F_BLUE,
         "VLM 仅在开局/异常时介入：\n将长程任务拆解为绑定到\n实体 Token 的 4D 子目标"),
        ("2. 执行前 4D 推演筛选", C_TEAL, F_TEAL,
         "4D WAM 采样候选动作块\n预测未来 4D 状态，\n提前剔除碰撞与偏斜方案"),
        ("3. 对齐实测算 4D 残差", C_PURPLE, F_PURPLE,
         "同实体 / 同坐标 / 同时刻\n屏蔽遮挡后比对预测与实测：\n区分“真失败”与“观测不足”"),
        ("4. 精准恢复与门禁进化", C_RUST, F_RUST,
         "卡阻/漏抓 → 定向触发恢复；\n高残差片段回流微调 WAM，\n已验证修复过留出门禁入库"),
    ]
    vx = 0.70
    vw = 2.74
    for idx, (vt, col, fl, vd) in enumerate(vsteps):
        add_rect(s, vx, 1.94, vw, 1.48, fill=fl, line=col, line_pt=1.3, rounded=True, radius=0.05)
        add_textbox(s, vx + 0.10, 2.02, vw - 0.20, 0.26, vt, size=11.6, bold=True, color=col)
        add_textbox(s, vx + 0.10, 2.32, vw - 0.20, 1.02, vd, size=10.7, bold=False, color=C_INK, line_spacing=1.22)
        if idx < 3:
            add_arrow_shape(s, vx + vw + 0.06, 2.55, 0.20, 0.20, "right", C_PURPLE)
        vx += vw + 0.32

    # Bottom 2 cards: Concrete feasible topics + Rigorous naming & ablation
    y1 = add_card(s, 0.55, 3.76, 6.02, 2.54, "分步可落地课题（先打穿最硬的一环）", C_PURPLE, C_WHITE, C_PURPLE, top_bar=True, header_size=13.0)
    tb1 = add_textbox(s, 0.68, y1 + 0.02, 5.76, 1.98)
    add_rich_paragraphs(tb1.text_frame, [
        [("课题 5A（近期最优先）· 预测残差驱动的免 CAD 失败诊断与恢复：", True, C_CRIMSON),
         ("攻克“两个 4D 张量不能直接相减”的硬技术点——实体/尺度/时刻对齐 + 遮挡可见性掩码，冻结底层策略即可验证恢复净收益。", False)],
        [("课题 5B（中期）· 残差引导的跨回合 Self-Improvement：", True, C_INK),
         ("用高 4D 残差定位具体错误步骤，定向微调 WAM 或固化恢复技能，并在严格留出场景集上检验泛化与防遗忘。", False)],
        [("课题 5C（长期探索）· 严格意义 RSI：", True, C_NAVY),
         ("在跨局收益稳定后，进一步研究诊断与数据筛选策略本身的递归优化。", False)],
    ], default_size=11.3, space_after=6, line_spacing=1.19, bullet_prefix="▪ ")

    y2 = add_card(s, 6.76, 3.76, 6.02, 2.54, "严格归因实验与可行性把控", C_TEAL, F_TEAL, C_TEAL, top_bar=True, header_size=13.0)
    tb2 = add_textbox(s, 6.89, y2 + 0.02, 5.76, 1.98)
    add_rich_paragraphs(tb2.text_frame, [
        [("四级验证信号对照（同 Agent 与技能库）：", True, C_TEAL),
         ("① 纯语义进度（LAW 类） / ② 仅实测几何目标残差（无未来预测） / ③ 未校准预测残差 / ④ 对齐校准的 4D 预测残差。", False)],
        [("避免伪改进与盲目重试：", True, C_INK),
         ("固定总执行时间与 VLM token 预算，同步汇报误报率、失败检测延迟、恢复成功率与最终任务成功率。", False)],
        [("极低启动门槛：", True, C_INK),
         ("首轮完全不需要等待新物理大模型，用冻结 Gnomon4D / PointWorld 即可率先跑通完整归因闭环。", False)],
    ], default_size=11.3, space_after=6, line_spacing=1.19, bullet_prefix="▸ ")

    set_notes(s, "板块五的科研方案非常聚焦，叫 Verify in 4D。它不把 4D WAM 和 Agent 割裂开，而是把预测 4D 与实测 4D 对齐后的残差变成同一个闭环信号。同时我们非常严谨地把跨局 Self-Improvement 和长期 RSI 拆开，第一步先冻结策略把“对齐残差驱动恢复”这一课题干净打穿，门槛低、创新强、最容易先出顶会成果。")


# ------------------------------------------------------------------------------
# PART 3: SYNERGY, DATA BASE & ROADMAP (P16-P18)
# ------------------------------------------------------------------------------

def build_p16_synergy_case(prs):
    s = blank_slide(prs)
    add_chrome(
        s, "三、底座协同 · 横向贯通", "横向协同：同一精细插接任务贯通五板块，共享接口解耦并行",
        [("以", False), ("“动态托盘多型号精密插接”", True, C_NAVY),
         ("为全组共享锚定任务：逐项引入扰动，五板块各解一类失败，", False),
         ("既独立发论文又可拼装", True, C_CRIMSON), ("。", False)],
        "设计原则：内部模型可自由选择点云、高斯或 Token，对外统一遵守最小 4D 交互状态接口；同时保留 RoboTwin / 真机标准任务", 16,
        bottom_callout=[("解耦协作机制：", True, C_TEAL),
                        ("不要求全组第一天共训一个大一统模型——每个方向可用冻结上下游代理模块独立发论文，再在共享锚定任务上做 2×2 交叉验证。", False)],
        callout_color=C_TEAL
    )

    headers = ["真实场景扰动", "现有基线为何失败？", "负责响应的板块与机制", "通过共享 4D 接口交付什么？"]
    rows = [
        ["① 夹爪遮挡 /\n相机微移",
         "逐帧几何失锁、插孔身份丢失、尺度漂移导致对位偏斜",
         [("板块一 · 4D 几何：", True, C_TEAL), ("持久实体 Token 跨遮挡保持位姿与身份", False)],
         "带实体 ID、度量位姿与可见性掩码的 4D 状态"],
        ["② 外观相同但\n阻尼/摩擦突变",
         "视觉看不出过盈配合或高摩擦，仍按默认力道推入卡死",
         [("板块二 · 物理因果：", True, C_NAVY), ("VLM 材质先验 + 轻触试探更新信念 φ", False)],
         "动作条件后果分布 p(s'|s,a,φ) 与接触状态"],
        ["③ 托盘缓慢移动 /\n感知计算延迟",
         "固定长块开环执行中目标移位，插脚到达时错过对准窗口",
         [("板块三 · 动态操作：", True, C_RUST), ("接触临界切短块 + 异步 RTC 实时追踪", False)],
         "带时间戳的可执行动作块与事件重规划触发"],
        ["④ 临时换新型号\n插接顺序",
         "未见过新组合，策略不知需先拔保护盖再斜插卡扣",
         [("板块四 · 示教 ICL：", True, C_TEAL), ("从 1 段人类示范经 HOI 抽取 4D 接触顺序", False)],
         "跨本体目标关系与阶段约束上下文"],
        ["⑤ 插歪卡阻需\n退回并重试",
         "开环策略继续硬推；纯 2D VLM 看不出 3mm 横向偏心",
         [("板块五 · 4D Agent：", True, C_PURPLE), ("对齐预测与实测 4D 残差精准定位偏移", False)],
         "触发“微退 + 偏置重插”，高残差片段入库进化"],
    ]
    add_styled_table(s, 0.55, 1.56, 12.23, 4.74, headers, rows, [1.85, 3.15, 3.65, 3.58],
                     header_fill=C_NAVY, font_size=11.0, hl_row=4)

    set_notes(s, "这一页回答领导最关心的一个管理问题：五个板块铺开后，学生们会不会互相等待、或者变成毫无关系的五摊子？我们设计了同一个精密插接锚定任务族，五种扰动精准对应五个板块的独立贡献，通过共享最小 4D 状态接口，既能各自独立发文章，又能随时拼接验证协同增益。")


def build_p17_data_and_extensions(prs):
    s = blank_slide(prs)
    add_chrome(
        s, "三、底座协同 · 数据与延伸", "公共底座与延伸布局：4D 数据飞轮、诊断评测尺与触觉力觉",
        [("数据与评测本身即是独立科学问题；围绕", False), ("“生成规模 + 真实校准 + 失败回流”", True, C_TEAL),
         ("构建大组 4D 数据飞轮，并提前预留", False), ("触觉/力觉", True, C_RUST), ("多模态接口。", False)],
        "承接《4D数据及其具身世界模型》(P18 监督分层, P24–26 三源互补, P45–47 失败回流与触觉 4D 光场采集)", 17,
        bottom_callout=[("大组核心护城河：", True, C_CRIMSON),
                        ("数据生成负责规模与覆盖，真实 4D 重建负责约束、校准与纠错；统一四层诊断评测尺确保每一项增益都可归因、可复现。", False)],
        callout_color=C_CRIMSON
    )

    # Left: 4D Data Flywheel
    y_l = add_card(s, 0.55, 1.54, 6.28, 4.76, "贯穿底座 · 4D 数据飞轮（承接大组重建与 HOI 优势）", C_TEAL, C_WHITE, C_TEAL, top_bar=True, header_size=13.0)

    # 3 mini source boxes
    srcs = [
        ("① 人类 4D / HOI", "海量任务与交互意图\n伪标签分层监督", C_NAVY, F_BLUE),
        ("② 仿真受控干预", "Coding Agent 构造\n反事实与失败样本", C_PURPLE, F_PURPLE),
        ("③ 光场 / 真机 4D", "高精度度量校准与\n真实接触力学锚定", C_TEAL, F_TEAL),
    ]
    sx = 0.70
    sw = 1.88
    for idx, (st, sd, col, fl) in enumerate(srcs):
        add_rect(s, sx, y_l + 0.04, sw, 1.12, fill=fl, line=col, line_pt=1.1, rounded=True, radius=0.06)
        add_textbox(s, sx + 0.06, y_l + 0.12, sw - 0.12, 0.28, st, size=11.0, bold=True, color=col, align=PP_ALIGN.CENTER)
        add_textbox(s, sx + 0.06, y_l + 0.44, sw - 0.12, 0.64, sd, size=10.2, bold=False, color=C_SUB, align=PP_ALIGN.CENTER, line_spacing=1.22)
        if idx < 2:
            add_textbox(s, sx + sw, y_l + 0.40, 0.17, 0.30, "+", size=14, bold=True, color=C_MUTED, align=PP_ALIGN.CENTER)
        sx += sw + 0.17

    tb_d = add_textbox(s, 0.70, y_l + 1.32, 5.98, 2.86)
    add_rich_paragraphs(tb_d.text_frame, [
        [("原则 1 · 监督可靠度严格分层（P18）：", True, C_INK),
         ("无可靠手标视频仅训视频预测；可见交互训几何；带机器人真实动作与成败的数据才训动力学与策略——绝不将估计伪标签当无误差真值。", False)],
        [("原则 2 · 真机失败驱动定向补采（P45–46）：", True, C_INK),
         ("真机运行中捕获的高 4D 残差暴露模型短板 → 驱动 Coding Agent 在仿真中针对性生成长尾、滑移与卡阻样本，打破盲目堆同质轨迹。", False)],
        [("原则 3 · 统一最小数据契约：", True, C_INK),
         ("所有子线共享基础字段：实体 ID、坐标系、时间戳、标签来源与置信度、标定版本与失败/恢复标记。", False)],
    ], default_size=11.2, space_after=8, line_spacing=1.22, bullet_prefix="▪ ")

    # Right Top: Diagnostic Evaluation Ruler
    y_rt = add_card(s, 7.04, 1.54, 5.74, 2.88, "补全拼图 ① · 统一四层诊断式评测尺（超越单一成功率）", C_NAVY, F_BLUE, C_NAVY, top_bar=True, header_size=12.6)
    tb_rt = add_textbox(s, 7.18, y_rt + 0.02, 5.46, 2.30)
    add_rich_paragraphs(tb_rt.text_frame, [
        [("状态层：", True, C_NAVY), ("重遮挡身份保持率、接触事件检出率与置信度校准误差；", False)],
        [("因果层：", True, C_NAVY), ("参照 WorldSimProbe，测同初态换动作/换物理参数的响应忠实度；", False)],
        [("闭环层：", True, C_NAVY), ("成功率—延迟/速度曲线、误报率、恢复率与每任务算力/token 预算；", False)],
        [("迁移层：", True, C_NAVY), ("严格隔离任务族上的少示教净增益，以及跨回合更新后的防遗忘表现。", False)],
    ], default_size=11.2, space_after=7, line_spacing=1.20, bullet_prefix="▸ ")

    # Right Bottom: Tactile / Force extension
    y_rb = add_card(s, 7.04, 4.58, 5.74, 1.72, "补全拼图 ② · 视觉 4D + 触觉 / 力觉多模态延伸", C_RUST, F_RUST, C_RUST, top_bar=True, header_size=12.6)
    tb_rb = add_textbox(s, 7.18, y_rb + 0.02, 5.46, 1.18)
    add_rich_paragraphs(tb_rb.text_frame, [[
        ("物理盲区边界：", True, C_RUST),
        ("在强接触遮挡（紧密插拔、拧盖、柔性织物整理）下，纯视觉 4D 与 VLM 先验存在不可消除的物理观测盲区。", False),
        ("中长期直接承接大组“融入触觉与力学的 4D 光场数据采集”（P47），将力矩/触觉接入统一 4D 物理信念接口。", True, C_INK)
    ]], default_size=11.2, space_after=0, line_spacing=1.22)

    set_notes(s, "这一页补全整个科研体系不可缺少的两块拼图：左侧把 4D 数据建设本身上升为“三源互补、可靠度分层、失败驱动回流”的数据飞轮，把组内 HOI 和光场 4D 重建优势吃透；右侧补充了四层诊断式评测尺，以及为强接触操作提前预留的触觉/力觉融合接口。")


def build_p18_roadmap(prs):
    s = blank_slide(prs)
    add_chrome(
        s, "三、底座协同 · 推进路线", "分阶段科研推进路线：先打穿最小闭环，再按证据收敛统一体系",
        [("不把“大一统模型”设为前置门槛；每一阶段均产出", False),
         ("独立可发表的顶会级成果与干净对照证据", True, C_CRIMSON), ("，由实验结果决定后续融合范围。", False)],
        "注：具体人员分配、真机机时与算力预算将结合课题组实际构成与首轮验证结果进一步细化落位", 18,
        bottom_callout=[("汇报总结：", True, C_CRIMSON),
                        ("以 4D 交互表征为脊柱，近期优先打穿“持久 4D 状态 × 4D 残差恢复”标杆闭环，同步推进物理、动态与 HOI-ICL 三条独立主线，稳步形成大组不可替代的学术标签。", False)],
        callout_color=C_CRIMSON
    )

    phases = [
        ("Phase 1 · 近期优先", "接口贯通与首轮标杆突破", C_TEAL, F_TEAL, [
            [("主攻优先闭环（板块一 × 板块五）：", True, C_CRIMSON),
             ("最直接承接 Gnomon4D/GAF 积累与 Agent 热点——冻结底座策略，验证“持久 4D 状态 + 对齐残差恢复”在遮挡精细任务上的净收益。", False)],
            [("三条独立并行线：", True, C_INK),
             ("物理线搭建同外观不同摩擦/质量仿真干预基线；动态线补全真实延迟与事件调度对照；ICL 线打通组内 HOI 示范编码与隔离任务评测。", False)],
        ], "阶段出口：各板块产出独立方法与可复现基线，最小 4D 状态接口在精密插接任务跑通。"),

        ("Phase 2 · 中期交叉", "三组 2×2 因子对照验证 1+1>2", C_NAVY, F_BLUE, [
            [("几何 × Agent（1 × 5）：", True, C_NAVY),
             ("逐帧 vs 持久 4D × 有/无残差恢复，证明恢复收益源自状态一致性而非盲目重试。", False)],
            [("物理 × 动态（2 × 3）：", True, C_NAVY),
             ("在线物理探测 × 事件自适应时域，证明高速/未知物理下收益超过额外计算开销。", False)],
            [("几何/HOI × ICL（1 × 4）：", True, C_NAVY),
             ("像素视频 vs 4D 交互关系上下文，证明跨本体少示教存在显著组合增益。", False)],
        ], "阶段出口：仅将验证有净交叉增益的模块并入统一主干，无协同收益者保持独立深耕。"),

        ("Phase 3 · 远期愿景", "原生 4D 物理世界模型与自进化", C_PURPLE, F_PURPLE, [
            [("原生统一 4D 物理世界模型：", True, C_PURPLE),
             ("融合原生 4D 场景 Token、动作条件因果动力学与触觉/力觉，原生支撑反事实推演与高频实时控制。", False)],
            [("数据飞轮与严格 RSI 探索：", True, C_INK),
             ("真机高 4D 残差自动触发仿真补采与门禁更新，在严格留出任务集上检验跨任务持续净收益，再进一步探索改进机制自身的递归优化。", False)],
        ], "最终特色：打造课题组鲜明且难以复制的“4D 中间语言 + 物理可信 + 闭环自进化”科研体系。"),
    ]

    px = 0.55
    pw = 3.95
    pgap = 0.19
    for ptag, ptitle, col, fl, pbuls, pexit in phases:
        add_rect(s, px, 1.54, pw, 4.76, fill=C_WHITE, line=col, line_pt=1.2, rounded=True, radius=0.04)
        add_rect(s, px, 1.54, pw, 0.42, fill=col)
        add_textbox(s, px + 0.14, 1.57, pw - 0.28, 0.36, ptag, size=12.5, bold=True, color=C_WHITE, valign=MSO_ANCHOR.MIDDLE)
        add_textbox(s, px + 0.14, 2.04, pw - 0.28, 0.34, ptitle, size=13.5, bold=True, color=col)
        add_rect(s, px + 0.14, 2.40, pw - 0.28, 0.015, fill=C_RULE)

        tb = add_textbox(s, px + 0.12, 2.48, pw - 0.24, 2.86)
        add_rich_paragraphs(tb.text_frame, pbuls, default_size=11.3, space_after=8, line_spacing=1.22, bullet_prefix="▪ ")

        add_rect(s, px + 0.12, 5.42, pw - 0.24, 0.76, fill=fl, line=col, line_pt=0.9, rounded=True, radius=0.06)
        add_textbox(s, px + 0.20, 5.46, pw - 0.40, 0.68, pexit, size=10.4, bold=True, color=C_INK, valign=MSO_ANCHOR.MIDDLE, line_spacing=1.20)
        px += pw + pgap

    set_notes(s, "最后汇报推进路线。我们刻意不设拍脑袋的时间表，而是按科学证据门禁分三步走：近期优先把 4D 持久状态和 4D 残差恢复这条最贴合我们优势、最容易先出成果的闭环打穿，同时并行推进物理、动态和 HOI-ICL 三条独立线；中期用三组 2×2 交叉实验拿硬数据决定哪些模块该合；远期汇聚到原生 4D 物理世界模型与闭环自进化飞轮。以上是全部汇报，请老师批评指正！")


def main():
    prs = new_prs()
    builders = [
        build_p01_cover,
        build_p02_toc,
        build_p03_background_paradigm,
        build_p04_five_backgrounds,
        build_p05_overall_framework,
        build_p06_m1_progress,
        build_p07_m1_proposal,
        build_p08_m2_progress,
        build_p09_m2_proposal,
        build_p10_m3_progress,
        build_p11_m3_proposal,
        build_p12_m4_progress,
        build_p13_m4_proposal,
        build_p14_m5_progress,
        build_p15_m5_proposal,
        build_p16_synergy_case,
        build_p17_data_and_extensions,
        build_p18_roadmap,
    ]
    assert len(builders) == TOTAL_SLIDES
    for fn in builders:
        fn(prs)
    prs.save(str(OUT_PPTX))
    print(f"Successfully built native PPTX: {OUT_PPTX} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
