"""Convert Markdown proposals into formatted Word documents (.docx).

Builds:
  - docs/Proposal_AI_Air_Doctor.docx from docs/proposal.md
  - docs/AI_Air_Doctor_Proposal_Analysis.docx from docs/AI_Air_Doctor_Proposal_Analysis.md

Supports: headings (H1–H4), paragraphs, bullets, numbered lists, tables, blockquotes,
code blocks, **bold**, *italic*, `code`, markdown image links, and Mermaid diagrams.
"""
import os
import re
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

BASE = os.path.join(os.path.dirname(__file__), "..")
DOCS = os.path.join(BASE, "docs")
IMG = os.path.join(DOCS, "img")
FONT = "Microsoft JhengHei"
MERMAID_IMAGES = ["architecture.png", "flowchart.png"]
TARGETS = [
    (os.path.join(DOCS, "proposal.md"), os.path.join(DOCS, "Proposal_AI_Air_Doctor.docx")),
    (os.path.join(DOCS, "AI_Air_Doctor_Proposal_Analysis.md"),
     os.path.join(DOCS, "AI_Air_Doctor_Proposal_Analysis.docx")),
]


def set_font(run, size=None, bold=None, color=None, mono=False, italic=None):
    name = "Consolas" if mono else FONT
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:eastAsia"), FONT)
    if size:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def _emit_code_runs(par, seg, size, bold, color, italic):
    for token in re.split(r"(`[^`]+`)", seg):
        if not token:
            continue
        if token.startswith("`") and token.endswith("`"):
            set_font(par.add_run(token[1:-1]), size - 1, bold, "C7254E", mono=True, italic=italic)
        else:
            set_font(par.add_run(token), size, bold, color, italic=italic)


def add_inline(par, text, size=11, color=None, italic=None):
    cleaned = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text).replace("<br>", "\n")
    pattern = r"(\*\*[^*]+\*\*|(?<!\*)\*[^*\s][^*\n]*?(?<!\s)\*(?!\*)|(?<!\*)\*[^*\s]\*(?!\*))"
    for part in re.split(pattern, cleaned):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            _emit_code_runs(par, part[2:-2], size, True, color, italic)
        elif part.startswith("*") and part.endswith("*") and len(part) >= 3:
            _emit_code_runs(par, part[1:-1], size, None, color, True)
        else:
            _emit_code_runs(par, part, size, None, color, italic)


def shade(cell, hex_color):
    tcpr = cell._element.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcpr.append(shd)


def style_callout(par, fill_hex="F0FDFA", border_hex="0E7490"):
    ppr = par._element.get_or_add_pPr()
    p_bdr = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "24")
    left.set(qn("w:space"), "8")
    left.set(qn("w:color"), border_hex)
    p_bdr.append(left)
    ppr.append(p_bdr)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    ppr.append(shd)


def _visual_len(s):
    plain = re.sub(r"\*\*|(?<!\*)\*(?!\*)|`|\[([^\]]+)\]\([^)]+\)", r"\1", s).replace("<br>", "\n")
    return max((sum(2 if ord(ch) > 127 else 1 for ch in ln.strip()) for ln in plain.split("\n")), default=1)


def _compute_col_widths(rows, total_cm=16.6):
    ncols = len(rows[0])
    weights = []
    for j in range(ncols):
        vals = sorted(_visual_len(r[j] if j < len(r) else "") for r in rows)
        p85 = vals[min(len(vals) - 1, int(0.85 * len(vals)))]
        # Smooth power curve so tiny badge cols stay compact while wide prose cols expand
        weights.append(max(4, p85) ** 0.62)
    wsum = sum(weights) or 1.0
    raw = [total_cm * w / wsum for w in weights]
    min_w = 1.35 if ncols <= 5 else 1.1
    clamped = [max(min_w, x) for x in raw]
    scale = total_cm / sum(clamped)
    return [Cm(x * scale) for x in clamped]


def add_table(doc, rows):
    header, body = rows[0], rows[1:]
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    widths = _compute_col_widths(rows)
    small = 8.5 if len(header) >= 6 else 10
    t.rows[0]._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
    for i, h in enumerate(header):
        t.columns[i].width = widths[i]
        c = t.rows[0].cells[i]
        c.width = widths[i]
        c.text = ""
        add_inline(c.paragraphs[0], h, small, "FFFFFF")
        for r in c.paragraphs[0].runs:
            r.bold = True
        shade(c, "0E7490")
    for r_i, r in enumerate(body):
        row = t.add_row()
        row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        cells = row.cells
        for i in range(len(header)):
            cells[i].width = widths[i]
            cells[i].text = ""
            add_inline(cells[i].paragraphs[0], r[i] if i < len(r) else "", small)
            if r_i % 2:
                shade(cells[i], "ECFEFF")
    doc.add_paragraph()


def parse_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def build(md_path, out_path):
    doc = Document()
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = Cm(2.2)
    sec.top_margin = sec.bottom_margin = Cm(2.2)
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    normal.font.size = Pt(11)
    normal.paragraph_format.line_spacing = 1.3
    normal.paragraph_format.space_after = Pt(4)

    md_dir = os.path.dirname(md_path)
    lines = open(md_path, encoding="utf-8").read().splitlines()
    i, mermaid_idx, first_h1 = 0, 0, True
    while i < len(lines):
        line = lines[i]
        s = line.strip()

        if s.startswith("```"):
            lang = s[3:].strip()
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1
            if lang == "mermaid":
                if mermaid_idx < len(MERMAID_IMAGES):
                    p = doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    w = Cm(15.5) if mermaid_idx == 0 else Cm(11)
                    p.add_run().add_picture(os.path.join(IMG, MERMAID_IMAGES[mermaid_idx]), width=w)
                    cap = doc.add_paragraph()
                    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    add_inline(cap, ["圖 1:系統架構圖", "圖 2:系統流程圖"][mermaid_idx], 9.5, "475569")
                mermaid_idx += 1
            else:
                t = doc.add_table(rows=1, cols=1)
                t.style = "Table Grid"
                t.alignment = WD_TABLE_ALIGNMENT.CENTER
                t.autofit = False
                t.columns[0].width = Cm(16.6)
                t.rows[0]._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
                c = t.rows[0].cells[0]
                c.width = Cm(16.6)
                shade(c, "F1F5F9")
                c.text = ""
                p = c.paragraphs[0]
                for j, b in enumerate(block):
                    r = p.add_run(b)
                    set_font(r, 9, mono=True)
                    if j < len(block) - 1:
                        r.add_break()
                doc.add_paragraph()
            continue

        img_match = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", s)
        if img_match:
            alt_text, rel_path = img_match.groups()
            img_path = os.path.normpath(os.path.join(md_dir, rel_path))
            if os.path.exists(img_path):
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.add_run().add_picture(img_path, width=Cm(16.2))
                if alt_text:
                    cap = doc.add_paragraph()
                    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    add_inline(cap, alt_text, 9.5, "475569")
            i += 1
            continue

        if s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                r = parse_row(lines[i])
                if not all(re.fullmatch(r":?-+:?", c) for c in r):
                    rows.append(r)
                i += 1
            add_table(doc, rows)
            continue

        if s in ("", "---"):
            i += 1
            continue

        if s.startswith("# "):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(60 if first_h1 else 12)
            set_font(p.add_run(s[2:]), 20, True, "0E7490")
            first_h1 = False
        elif s.startswith("## "):
            p = doc.add_heading(level=1)
            set_font(p.add_run(s[3:]), 16, True, "0E7490")
        elif s.startswith("### "):
            p = doc.add_heading(level=2)
            set_font(p.add_run(s[4:]), 13, True, "155E75")
        elif s.startswith("#### "):
            p = doc.add_heading(level=3)
            set_font(p.add_run(s[5:]), 11.5, True, "0E7490")
        elif s.startswith("> "):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.5)
            p.paragraph_format.right_indent = Cm(0.3)
            style_callout(p)
            add_inline(p, s[2:], 10.5, "0F172A")
        elif re.match(r"^[-*] ", s):
            p = doc.add_paragraph(style="List Bullet")
            add_inline(p, s[2:])
        elif re.match(r"^\d+\. ", s):
            p = doc.add_paragraph(style="List Number")
            add_inline(p, re.sub(r"^\d+\. ", "", s))
        else:
            p = doc.add_paragraph()
            if s.startswith("**Proposal") or s.startswith("AI Air Doctor:") or s.startswith("**AI Air Doctor:"):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if line.startswith(("作者", "組員", "課程")):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_inline(p, s.rstrip("\\").strip())
            # page break after cover info
            if line.startswith("課程"):
                doc.add_page_break()
        i += 1

    doc.save(out_path)
    print("saved", os.path.abspath(out_path))


if __name__ == "__main__":
    for md_path, out_path in TARGETS:
        if os.path.exists(md_path):
            build(md_path, out_path)
