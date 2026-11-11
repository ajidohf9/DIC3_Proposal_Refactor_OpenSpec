"""Build the proposal slide deck (docs/Proposal_AI_Air_Doctor.pptx)."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

BASE = os.path.join(os.path.dirname(__file__), "..")
IMG = os.path.join(BASE, "docs", "img")
OUT = os.path.join(BASE, "docs", "Proposal_AI_Air_Doctor.pptx")
FONT = "Microsoft JhengHei"

BG = RGBColor(0x0B, 0x12, 0x20)
CARD = RGBColor(0x15, 0x20, 0x33)
CARD2 = RGBColor(0x1E, 0x2B, 0x42)
CYAN = RGBColor(0x22, 0xD3, 0xEE)
GREEN = RGBColor(0x34, 0xD3, 0x99)
AMBER = RGBColor(0xFB, 0xBF, 0x24)
RED = RGBColor(0xF8, 0x71, 0x71)
VIOLET = RGBColor(0xA7, 0x8B, 0xFA)
WHITE = RGBColor(0xF8, 0xFA, 0xFC)
MUTED = RGBColor(0x94, 0xA3, 0xB8)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
TOTAL = 21
_page = [0]


def _font(run, size, color=WHITE, bold=False, mono=False):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    name = "Consolas" if mono else FONT
    run.font.name = name
    rpr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rpr.find(qn(tag))
        if el is None:
            el = rpr.makeelement(qn(tag), {})
            rpr.append(el)
        el.set("typeface", FONT if not mono else "Consolas")


def text(slide, x, y, w, h, lines, size=16, color=WHITE, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, mono=False, spacing=1.15):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.05)
    if isinstance(lines, str):
        lines = [lines]
    for i, ln in enumerate(lines):
        opts = {}
        if isinstance(ln, tuple):
            ln, opts = ln
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = opts.get("align", align)
        p.line_spacing = spacing
        p.space_after = Pt(opts.get("after", 4))
        _font(p.add_run(), 1)
        p.runs[0].text = ln
        _font(p.runs[0], opts.get("size", size), opts.get("color", color),
              opts.get("bold", bold), mono)


def rect(slide, x, y, w, h, fill, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    sh = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if line:
        sh.line.color.rgb = line
        sh.line.width = Pt(1.5)
    else:
        sh.line.fill.background()
    return sh


def new_slide(title, subtitle=None):
    _page[0] += 1
    s = prs.slides.add_slide(BLANK)
    rect(s, 0, 0, 13.333, 7.5, BG, shape=MSO_SHAPE.RECTANGLE)
    if title:
        rect(s, 0.6, 0.45, 0.1, 0.65, CYAN, shape=MSO_SHAPE.RECTANGLE)
        text(s, 0.85, 0.45, 10.5, 0.4, title, 22, WHITE, True)
        if subtitle:
            text(s, 0.85, 0.88, 10.5, 0.35, subtitle, 13, MUTED)
        text(s, 11.5, 0.5, 1.2, 0.4, f"{_page[0]} / {TOTAL}", 13, MUTED, align=PP_ALIGN.RIGHT)
        text(s, 0.6, 6.95, 6, 0.35, "AI Air Doctor · Final Project Proposal", 11, MUTED)
    return s


def card(slide, x, y, w, h, title, body, accent=CYAN, title_size=17, body_size=13):
    rect(slide, x, y, w, h, CARD)
    rect(slide, x, y, w, 0.07, accent, shape=MSO_SHAPE.RECTANGLE)
    text(slide, x + 0.2, y + 0.2, w - 0.4, 0.5, title, title_size, accent, True)
    text(slide, x + 0.2, y + 0.72, w - 0.4, h - 0.85, body, body_size, WHITE)


def table(slide, x, y, w, rows, col_w, size=12, row_h=0.5, header_fill=RGBColor(0x0E, 0x74, 0x90)):
    shp = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y),
                                 Inches(w), Inches(row_h * len(rows)))
    tbl = shp.table
    for j, cw in enumerate(col_w):
        tbl.columns[j].width = Inches(cw)
    for i, r in enumerate(rows):
        for j, val in enumerate(r):
            c = tbl.cell(i, j)
            c.fill.solid()
            c.fill.fore_color.rgb = header_fill if i == 0 else (CARD if i % 2 else CARD2)
            c.margin_left = c.margin_right = Inches(0.08)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = c.text_frame
            tf.word_wrap = True
            tf.paragraphs[0].text = ""
            run = tf.paragraphs[0].add_run()
            run.text = val
            color = WHITE
            if val.startswith("✓"):
                color = GREEN
            elif val.startswith("✗"):
                color = RED
            elif val.startswith("△"):
                color = AMBER
            _font(run, size, color, i == 0)
    return tbl


# ---------------- 1. Title ----------------
s = new_slide(None)
rect(s, 0, 0, 13.333, 7.5, BG, shape=MSO_SHAPE.RECTANGLE)
for i, (c, x, y, d) in enumerate([(CYAN, 9.6, -1.2, 4.5), (VIOLET, 10.9, 3.6, 3.2), (GREEN, 8.4, 4.9, 1.6)]):
    o = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    o.fill.solid()
    o.fill.fore_color.rgb = c
    o.fill.transparency = 0.0
    o.line.fill.background()
    sf = o.fill._xPr.find(qn("a:solidFill"))
    clr = sf[0]
    a = clr.makeelement(qn("a:alpha"), {"val": "22000"})
    clr.append(a)
text(s, 0.9, 1.5, 9, 0.5, "FINAL PROJECT PROPOSAL", 16, CYAN, True)
text(s, 0.9, 2.0, 10, 1.2, "AI Air Doctor", 60, WHITE, True)
text(s, 0.9, 3.2, 10, 1.0, "結合 IoT 空品數據與環境醫學知識的\n個人化空氣品質健康代理人", 26, WHITE)
rect(s, 0.9, 4.65, 1.2, 0.06, CYAN, shape=MSO_SHAPE.RECTANGLE)
text(s, 0.9, 4.9, 10, 0.5, "AI Agent  +  Domain Knowledge  +  Data Analytics  +  Real-World Application", 15, MUTED)
text(s, 0.9, 5.8, 11, 0.8, ["組員: 7115093066_楊禾睿、7115093063_徐崇皓、7115064183_謝秉樺、7115064202_譚人傑", "課程: 物聯網與智慧系統應用專題    指導教授: 陳煥 教授"], 14, MUTED)

# ---------------- 2. Motivation ----------------
s = new_slide("研究動機 Motivation", "空氣污染是全球第二大早逝風險因子 (WHO & HEI 2025)")
stats = [("790 萬", "2023 年全球\n空污致死人數", CYAN), ("1 / 8", "全球每 8 位死者\n就有 1 位與空污有關", VIOLET),
         ("86%", "空污死亡來自心血管、\n中風與呼吸道慢性病", AMBER), ("No.2", "僅次於高血壓的\n全球第二大早逝風險", RED)]
for i, (num, desc, c) in enumerate(stats):
    x = 0.7 + i * 3.05
    rect(s, x, 1.75, 2.8, 2.6, CARD)
    text(s, x, 1.95, 2.8, 1.0, num, 44, c, True, PP_ALIGN.CENTER)
    text(s, x + 0.15, 3.05, 2.5, 1.2, desc, 14, WHITE, align=PP_ALIGN.CENTER)
text(s, 0.7, 4.45, 12, 0.4, "資料來源: Health Effects Institute, State of Global Air 2025 & The Lancet", 11, MUTED)
rect(s, 0.7, 5.0, 11.9, 1.7, CARD2)
text(s, 1.0, 5.15, 11.4, 1.5, [
    ("台灣情境挑戰 (MOENV 2024/2025 & NCHU 2025 實證)", {"bold": True, "color": CYAN, "size": 17}),
    "台灣 2024 年 PM2.5 全國年均降至 12.8 μg/m³ 且環境部於 2024/09 修訂嚴格標準 (年均 12 / 日均 30 μg/m³)，"
    "但秋冬中南部逆溫滯留仍頻繁超標，影響約 140–200 萬氣喘族群；NCHU 團隊 152 萬人研究 (BMC Med. 2025) 更證實 PM2.5 ≥ 25 μg/m³ 使運動保護力減半。"], 14)

# ---------------- 3. Abstract & Introduction Structure Alignment ----------------
s = new_slide("Abstract（摘要）與 Introduction（緒論）結構對照", "六段式 (A–F) 嚴密呼應 · 嚴格遵循「未實驗者僅列 Expected Outcomes，不虛構數據」")
rect(s, 0.6, 1.55, 6.2, 5.2, CARD)
text(s, 0.85, 1.7, 5.7, 0.4, "📋 Abstract 六段式（A–F）對照", 16, CYAN, True)
af_items = [
    ("A. Attention Getter：", "引用 HEI 2025 全球 790 萬早逝、台灣 2024 年均 12.8 / 新標 12·30 μg/m³、140–200 萬氣喘與 152 萬人運動閾值引題 [1,3,16,21]。"),
    ("B. But（挑戰）：", "現有 App 僅單點數值無個人化；純 ML 缺語意轉譯；通用 LLM 缺即時感測與護欄易生幻覺；微感測 RH>75% 易虛高 [9–15,20]。"),
    ("C. Cure（解藥）：", "提出 AI Air Doctor 個人化 Domain AI Agent，並以 OpenSpec 規格驅動實作。"),
    ("D. Development（方法）：", "整合 LangGraph ReAct、MOENV+Civil IoT+CWA、XGBoost/Bi-LSTM+SHAP、換氣劑量×雙軌門檻、ChromaDB RAG 與護欄 [2–8,17–23]。"),
    ("E. Experiments（評估）：", "規劃 2022–2025 盲測對比 Persistence/MLR (E1)、30 組醫師情境對比 GPT-4o (E2)、10 場 SHAP 專家評核 (E3) 與 100 併發/SUS (E4)。"),
    ("F. Findings（預期產出）：", "不虛構數據，預期 RMSE ≤9.5 μg/m³ (降35%+)、對齊率 ≥95–96%、幻覺率 ≤2–3%、100% 可追溯引用、延遲 ≤4.2s、SUS ≥80。"),
]
for i, (k, v) in enumerate(af_items):
    tb = s.shapes.add_textbox(Inches(0.85), Inches(2.15 + i * 0.75), Inches(5.7), Inches(0.72))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.line_spacing = 1.08
    r1 = p.add_run()
    r1.text = k
    _font(r1, 11.5, GREEN, True)
    r2 = p.add_run()
    r2.text = v
    _font(r2, 11.5, WHITE, False)

table(s, 7.05, 1.55, 5.65, [
    ["Abstract (A–F)", "對應 Introduction", "核心對照關係"],
    ["A. Attention Getter", "A. Attention Getter", "同一組權威統計引題，Intro 展開台灣季風地形衝擊"],
    ["B. But（挑戰）", "B. Background\nC. Problem\nD. Limitations", "Intro 補齊台灣 IoT 背景、晨跑四大支柱與四類系統瓶頸"],
    ["C. Cure（解藥）\nD. Development", "E. Innovation", "Intro 聚焦三閉環、RH>75% 校準、雙軌與 OpenSpec 創新"],
    ["E. Experiments\nF. Findings", "F. Contributions", "統一 E1–E4 預計指標並歸納架構/技術/知識/應用貢獻"],
], [1.65, 1.55, 2.45], 11.5, 0.96)

# ---------------- 4. Final Project Spec Compliance ----------------
s = new_slide("期末專題規範符合度總覽 (1.1–1.4 × OpenSpec)", "超越單一 Model 與 Chatbot · 規格驅動之 Domain AI Agent 雙軌對齊")
table(s, 0.6, 1.55, 12.1, [
    ["編號", "規範評估維度", "AI Air Doctor 設計實踐", "OpenSpec / 文件對應", "符合度"],
    ["1.1", "AI Agent\n(推理與調度)", "LangGraph ReAct 狀態機、參數追問迴圈、時態路由與 Tool Calling，搭配強制引用反思護欄", "react-agent-guardrail\nAlgorithm 1 (L01–29)", "✓ 高"],
    ["1.2", "Domain Knowledge\n(領域知識)", "WHO 2021 (15) 與 MOENV 2024 (12/30)、運動換氣係數 (1.0–1.8×)、RH>75% 校正與 CO₂ 換氣權衡", "personalized-exposure-rag\nDeep Research §5", "✓ 高"],
    ["1.3", "Data Analytics\n(數據分析)", "MOENV (3km) + Civil IoT (1km/5km) + CWA、時空 KNN 補值、風向量 (u,v)、XGBoost/Bi-LSTM + SHAP", "realtime-iot-ingestion\npm25-forecast-shap", "✓ 高"],
    ["1.4", "Real-World App\n(真實應用)", "鎖定台灣 140–200 萬氣喘族群 [21] 與 152 萬人運動閾值 [16]，支援 Streamlit 與 LINE Bot 雙介面", "Proposal §1–§3\nDESIGN.md §1–§12", "✓ 高"],
], [0.7, 2.15, 5.2, 2.95, 1.1], 12, 0.72)
card(s, 0.6, 5.3, 5.9, 1.45, "OpenSpec Spec-Driven 驗證狀態 (v1.2.0)",
     "openspec validate ai-air-doctor-mvp → Valid | Progress: 4/4 artifacts complete\n(proposal.md · design.md · tasks.md · 4 Capability Specs)", CYAN, 15, 12.5)
card(s, 6.8, 5.3, 5.9, 1.45, "核心評量準則檢核",
     "✓ 完整整合「懂大氣與環境醫學 + 會取台灣即時數據 + 能定量預報 + 有客觀實證出處」\n✓ 嚴禁虛構數據：E1–E4 全面採 Expected Outcomes 標示", GREEN, 15, 12.5)

# ---------------- 5. Problem ----------------
s = new_slide("問題定義 Problem", "民眾真正想問的，不是「AQI 多少」，而是「我該怎麼做」")
rect(s, 0.7, 1.75, 5.6, 1.6, CARD2, line=VIOLET)
text(s, 0.95, 1.9, 5.2, 0.4, "💬 使用者提問情境", 15, VIOLET, True)
text(s, 0.95, 2.35, 5.2, 1.0, "「我有慢性氣喘，明天早上 7 點\n想去大安森林公園跑步，可以嗎？」", 19, WHITE, True)
text(s, 0.7, 3.65, 5.6, 0.5, "回答這個問題，系統必須同時具備四大支柱:", 16, MUTED)
needs = [("① 即時微環境感測 (環境部標準站 + Civil IoT 微型感測)", CYAN),
         ("② 24h 前瞻氣象預測 (風速、逆溫潛勢、濕度預報)", GREEN),
         ("③ 個人健康檔案換算 (運動換氣量加權劑量計算)", AMBER),
         ("④ 臨床環境醫學指引 (WHO 2021 與台灣 AQI 臨床對策)", RED)]
for i, (n, c) in enumerate(needs):
    rect(s, 0.7, 4.15 + i * 0.62, 5.6, 0.52, CARD)
    rect(s, 0.7, 4.15 + i * 0.62, 0.08, 0.52, c, shape=MSO_SHAPE.RECTANGLE)
    text(s, 0.95, 4.2 + i * 0.62, 5.2, 0.45, n, 14, WHITE, anchor=MSO_ANCHOR.MIDDLE)
table(s, 6.8, 1.75, 5.85, [
    ["現有方案", "能做到", "做不到"],
    ["空品 App\n(環境即時通)", "顯示即時單點數值", "✗ 無個人化建議與成因"],
    ["PM2.5 預測研究", "預測未來數值矩陣", "✗ 缺乏語意解釋與行動處方"],
    ["一般 LLM\n(ChatGPT)", "自然語言對話", "✗ 無即時數據、易生醫療幻覺"],
    ["近期空品 Agent 研究", "LLM + 政策資料分析", "△ 偏宏觀政策、缺乏個人化"],
], [1.95, 1.85, 2.05], 13, 0.85)

# ---------------- 4. Related Work ----------------
s = new_slide("文獻回顧 Related Work", "½ AI Technology + ½ Domain Know-how (經查證之 2024–2026 前沿研究)")
table(s, 0.6, 1.65, 12.1, [
    ["Ref", "Year", "Problem", "AI Method", "Domain Knowledge", "Dataset", "Findings", "Limitation"],
    ["[9]", "2025", "洛杉磯野火空品與政策", "Instructor-Worker LLM", "野火煙霧、公衛分級", "2025 LA 野火監測", "多代理協作產出政策通報", "偏宏觀政策無個人化預報"],
    ["[10]", "2025", "非專家難解讀即時感測", "LLM + MCP 伺服器", "PM2.5/PM10/VOCs 規範", "即時空品感測串流", "MCP 工具調用顯著降幻覺", "缺少 24h 預測與醫療 RAG"],
    ["[14]", "2024", "台灣尖峰 PM2.5 時空變異", "Geo-AI 集成 + SHAP", "交通排放、微氣象擴散", "台灣測站與地理資料", "量化氣象與空間關鍵因子", "純估計模型無互動處方"],
    ["[15]", "2026", "台灣微感測高濕校正建模", "ML 融合 + RH 補償", "光散射吸濕成長機制", "台灣微感測網 + AOD", "納入 RH 大幅提升精度", "僅網格製圖無前瞻建議"],
    ["[16]", "2025", "空污下運動健康淨效益", "統合分析與世代匯集", "運動效益 vs PM2.5 劑量", "7 世代 152 萬成人", "≥25μg/m³ 保護效益減半", "需智慧 Agent 落實排程"],
], [0.55, 0.65, 1.85, 1.95, 1.75, 1.65, 1.9, 1.8], 11, 0.62)
card(s, 0.6, 5.55, 5.9, 1.25, "AI Technology", "XGBoost / Bi-LSTM · SHAP 可解釋 [14] · MCP / Instructor-Worker [9,10] · ReAct & Health-LLM RAG [13]", CYAN, 15, 12)
card(s, 6.8, 5.55, 5.9, 1.25, "Domain Knowledge", "WHO 2021 & MOENV 2024 [2,3] · RH>75% 感測物理校正 [15,20] · 152萬人運動劑量 [16,23] · CO₂ 認知 [22]", GREEN, 15, 12)

# ---------------- 5. Research Gap ----------------
s = new_slide("研究缺口 Research Gap", "Existing Research → Limitations → Research Gap → Our Project")
steps = [("Existing Research", "PM2.5 預測模型 (LSTM)\nLLM 空品代理人 (政策)", CYAN),
         ("Limitations", "預測只輸出數字黑盒子\nAgent 缺乏即時感測與個人化", AMBER),
         ("Research Gap", "缺少整合即時 IoT + 24h 預測 +\n環境醫學 RAG 的個人化 Agent", RED),
         ("Our Project", "AI Air Doctor\n領域智慧代理人", GREEN)]
for i, (t, b, c) in enumerate(steps):
    x = 0.6 + i * 3.1
    sh = s.shapes.add_shape(MSO_SHAPE.CHEVRON if i else MSO_SHAPE.PENTAGON, Inches(x), Inches(1.75), Inches(3.0), Inches(0.75))
    sh.fill.solid(); sh.fill.fore_color.rgb = c; sh.line.fill.background()
    tf = sh.text_frame; tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    r = tf.paragraphs[0].add_run(); r.text = t; _font(r, 15, BG, True)
    text(s, x + 0.1, 2.65, 2.8, 1.0, b, 14, WHITE, align=PP_ALIGN.CENTER)
table(s, 0.6, 3.85, 12.1, [
    ["核心能力矩陣", "空品 App", "PM2.5 預測模型", "一般 LLM", "近期空品 Agent", "AI Air Doctor"],
    ["即時多源 IoT 數據 (環境部 + Civil IoT)", "✓", "✓", "✗", "✓", "✓"],
    ["24h 機器學習污染趨勢預測", "✗", "✓", "✗", "△", "✓"],
    ["SHAP 大氣特徵歸因 (逆溫/風速解釋)", "✗", "△", "✗", "✗", "✓"],
    ["環境醫學臨床指引 (WHO / AQI RAG)", "✗", "✗", "△ 易生幻覺", "△", "✓ (100% 來源回溯)"],
    ["個人健康檔案與運動暴露換算", "✗", "✗", "✗", "△", "✓ (係數加權)"],
], [3.2, 1.7, 1.8, 1.8, 1.8, 1.8], 13, 0.48)

# ---------------- 6. Deep Research: 5 Mindsets (New Slide!) ----------------
s = new_slide("領域深度研究：五大專家核心思維 (佔比 20%)", "大氣科學與環境醫學專家普遍認同之 5 Core Mindsets")
m_data = [
    ("1. 暴露劑量 ≠ 環境濃度", "跑步換氣量由 6–8 升至 50–100+ L/min (8–15 倍) 且口呼吸；PM2.5 ≥25μg/m³ 使運動保護力減半 [16,23]。", "personalized-exposure-rag 換氣加權"),
    ("2. 敏感族群無安全閾值", "WHO 證實低濃度仍呈無閾值線性風險，台灣約 140–200 萬氣喘族群耐受度遠低於常人。", "氣喘者自動切換 WHO 2021 (15μg/m³)"),
    ("3. 微環境異質與感測物理", "街谷微區濃度差異大，但光散射感測器在 RH>75% 易吸濕膨脹虛高，需氣象校正與標準站比對。", "3km 標準站 + 1km 微感測 + RH 閘門"),
    ("4. 大氣動力學非線性主導", "高污染主因多為輻射逆溫、混合層下壓與靜風停滯，而非排放源突增，須納入氣象動力場。", "特徵工程含風向量(u,v)與溫差 ΔT"),
    ("5. 前瞻預警重於事後確認", "氣道發炎具滯後與不可逆性，需於高峰前 1–6 小時啟動關窗、HEPA 或調整戶外訓練窗口。", "時態路由優先 24h 預報與開窗推薦"),
]
for i, (m_title, m_exp, m_sys) in enumerate(m_data):
    y = 1.65 + i * 1.02
    rect(s, 0.6, y, 12.1, 0.92, CARD)
    rect(s, 0.6, y, 0.08, 0.92, CYAN, shape=MSO_SHAPE.RECTANGLE)
    text(s, 0.85, y + 0.1, 3.4, 0.35, m_title, 15, CYAN, True)
    text(s, 0.85, y + 0.45, 6.2, 0.4, m_exp, 12, WHITE)
    rect(s, 7.3, y + 0.15, 5.2, 0.62, CARD2)
    text(s, 7.45, y + 0.23, 5.0, 0.5, f"💡 系統架構落地: {m_sys}", 13, GREEN, True)

# ---------------- 7. Deep Research: Controversies & Questions (New Slide!) ----------------
s = new_slide("領域深度研究：三大專業爭論與十個深度問題", "Controversies (觀點 A ↔ 觀點 B) · 10 Deep Reasoning Questions")
rect(s, 0.6, 1.6, 6.0, 5.2, CARD)
text(s, 0.85, 1.75, 5.5, 0.4, "⚖️ 三大核心專業爭論", 16, AMBER, True)
controvs = [
    ("Trade-off 1: 微型感測器空間密度 vs 高濕度誤差",
     "A: 捕捉 1km 局部熱點  ↔  B: RH>75% 吸濕膨脹易虛高漂移\n→ 共識: 經 RH 非線性校正並交叉比對 5km 標準站作為輔助預警"),
    ("Trade-off 2: 室外紅害防滲透密閉 vs 室內 CO₂ 認知衰退",
     "A: 緊閉門窗阻隔 PM2.5  ↔  B: CO₂ 達 1000–1400+ppm 顯著降認知 [22]\n→ 共識: 依風場調度 10–15 分鐘「脈衝式換氣」+ HEPA 最大風速"),
    ("Trade-off 3: WHO 嚴格標準 (15) vs 國家標準 (30) 與警報疲勞",
     "A: 依 WHO 全面警示  ↔  B: 過度警示引發警報疲勞與麻木\n→ 共識: 法規採 MOENV 2024 (12/30)，Agent 依族群雙軌揭露"),
]
for i, (ct, cb) in enumerate(controvs):
    y = 2.2 + i * 1.45
    rect(s, 0.8, y, 5.6, 1.35, CARD2)
    text(s, 0.95, y + 0.08, 5.3, 0.35, ct, 13, CYAN, True)
    text(s, 0.95, y + 0.42, 5.3, 0.85, cb, 11, WHITE)

rect(s, 6.8, 1.6, 5.9, 5.2, CARD)
text(s, 7.05, 1.75, 5.4, 0.4, "🧠 十大深度理解問題 (10 Details 推理覆蓋)", 16, VIOLET, True)
qs = [
    ("Why / 大氣光化學", "夏季萬里無雲、PM2.5 僅 8μg/m³，為何體育課需中止？ (紫外線催化 O₃ 二次光化)"),
    ("What-if / 逆溫層物理", "清晨風速 0.3m/s 伴隨輻射逆溫，對通勤排放有何後果？ (低混合層鎖死廢氣)"),
    ("Trade-off / 微環境平衡", "室外 PM2.5 85 且室內 CO₂ 達 1400–1700ppm，如何權衡？ (10–15m 脈衝對流 + HEPA)"),
    ("Failure / 感測物理", "陰雨 RH 95% 微感測報 110 但標準站僅 18，成因何在？ (RH>75% 吸濕膨脹誤判)"),
    ("Design / 時序防漏", "預測模型為何嚴禁 Random K-Fold？ (強時序自相關造成未來 Data Leakage 虛高)"),
    ("Evidence / 生理與世代", "為何 38μg/m³ 跑步風險大增？ (換氣 8–15 倍且 ≥25μg/m³ 運動保護力減半 [16,23])"),
]
for i, (ql, qd) in enumerate(qs):
    y = 2.2 + i * 0.73
    text(s, 7.05, y, 5.4, 0.65, [(ql, {"bold": True, "color": GREEN, "size": 12}), f"：{qd}"], 11)

# ---------------- 8. Solution overview ----------------
s = new_slide("提出方案 Proposed Solution", "AI Air Doctor — 具備環境醫學專業能力的 Domain AI Agent")
pillars = [("🤖  AI Agent (ReAct)", "LangGraph 狀態機，解析自然語言意圖、動態調度 4 大工具組，支援反思護欄機制", CYAN),
           ("📚  Domain Knowledge", "WHO 2021 指引、台灣 AQI 臨床防護規範、各級口罩過濾手冊向量知識庫", GREEN),
           ("📈  Data Analytics", "XGBoost + LSTM 時序回歸，SHAP 解釋風速、溫濕度與逆溫層影響因子", AMBER),
           ("🌏  Real-World Application", "敏感族群個人化健康防護處方、戶外活動安全時段推薦、智慧通風指引", VIOLET)]
for i, (t, b, c) in enumerate(pillars):
    x = 0.6 + (i % 2) * 6.15
    y = 1.75 + (i // 2) * 2.1
    card(s, x, y, 5.95, 1.9, t, b, c, 19, 15)
rect(s, 0.6, 6.0, 12.1, 0.75, CARD2, line=CYAN)
text(s, 0.8, 6.05, 11.7, 0.65, "核心原則: 每一則建議都附上「測站來源 + 預測信心 + 醫學指引出處」，拒絕偽建議",
     16, WHITE, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

# ---------------- 9. Agent design ----------------
s = new_slide("Agent 設計 Agent Design", "Role · Tools · Decision Logic · 暴露劑量矩陣")
rect(s, 0.6, 1.7, 4.6, 5.05, CARD)
text(s, 0.85, 1.85, 4.2, 0.45, "🩺 Agent 角色 (System Prompt)", 16, CYAN, True)
text(s, 0.85, 2.35, 4.2, 2.3, [
    "• 結合大氣科學與環境醫學的專業顧問",
    "• 必須先用工具取得數據，禁止憑空猜測",
    "• 醫療建議必須 100% 引用知識庫出處",
    "• 敏感族群自動啟用嚴格 WHO 2021 門檻",
    "• 結尾強制附上醫療免責聲明"], 13)
text(s, 0.85, 4.6, 4.2, 0.45, "🧠 決策推理核心", 16, GREEN, True)
text(s, 0.85, 5.05, 4.2, 1.7, [
    "1. 實體辨識: 時間、地點、活動強度",
    "2. 個人健康檔案比對 (氣喘/長者/一般)",
    "3. 時態路由: 即時觀測 vs ML 預測",
    "4. 暴露評估: 濃度 × 運動換氣係數",
    "5. RAG 檢索臨床對策 → 護欄驗證"], 13)
table(s, 5.5, 1.7, 7.2, [
    ["Tool", "輸入", "輸出", "資料來源"],
    ["get_realtime_aq", "location", "PM2.5、O₃、AQI、測站", "環境部 OpenAPI / Civil IoT"],
    ["get_weather", "location", "溫濕度、風向風速、雨量", "中央氣象署 OpenAPI"],
    ["forecast_pm25", "station, horizon", "24h 預測值、信賴區間、SHAP", "XGBoost / LSTM 引擎"],
    ["search_health_kb", "risk, condition", "Top-k 處方段落 + 文獻出處", "ChromaDB 向量庫"],
    ["get_user_profile", "user_id", "年齡、慢性病史、活動偏好", "SQLite 本機庫"],
], [1.85, 1.35, 2.2, 1.8], 12, 0.62)
table(s, 5.5, 5.6, 7.2, [
    ["族群分類 (PM2.5 μg/m³)", "🟢 低風險", "🟡 中風險", "🟠 高風險", "🔴 極高風險"],
    ["一般民眾 (MOENV 2024)", "≤ 30", "31–50", "51–70", "> 70"],
    ["敏感族群 (WHO 2021 對齊)", "≤ 15", "16–30", "31–50", "> 50"],
], [2.2, 1.25, 1.25, 1.25, 1.25], 12, 0.38)

# ---------------- 10. Architecture ----------------
s = new_slide("系統架構 Architecture (8 大模組編號)", "① User ──> ② Input ──> ③ Agent ──> ④ Data ──> ⑤ ML ──> ⑥ KB ──> ⑦ Decision ──> ⑧ Output")
rect(s, 0.6, 1.6, 12.1, 5.2, WHITE)
s.shapes.add_picture(os.path.join(IMG, "architecture.png"), Inches(1.15), Inches(1.7), height=Inches(5.0))

# ---------------- 11. Flowchart ----------------
s = new_slide("處理流程 Flowchart", "完整輸入、條件分支、例外補償與護欄反思迴圈")
rect(s, 0.6, 1.55, 4.6, 5.25, WHITE)
s.shapes.add_picture(os.path.join(IMG, "flowchart.png"), Inches(1.0), Inches(1.6), height=Inches(5.15))
rect(s, 5.5, 1.55, 7.2, 5.25, CARD)
text(s, 5.8, 1.7, 6.7, 0.5, "📍 推理實例: 氣喘跑者明早運動諮詢", 18, CYAN, True)
text(s, 5.8, 2.3, 6.7, 4.4, [
    ("1  解析意圖: 大安森林公園 · 明早 07:00 · 跑步", {}),
    ("2  健康檔案: 氣喘病史 → 自動採用 WHO 嚴格門檻", {}),
    ("3  時態判定為未來 → 調用 forecast_pm25 工具", {}),
    ("     預測 PM2.5 = 38 μg/m³ (SHAP: 夜間輻射逆溫滯留主導)", {"color": MUTED, "size": 13}),
    ("4  計算暴露量: 38 × 1.8 (跑步換氣係數) = 68.4 → 🔴 極高風險", {}),
    ("5  RAG 檢索: WHO 2021 指南與胸腔醫學會氣喘運動處方", {}),
    ("6  Guardrail 驗證: 確認包含數據測站與文獻標註", {}),
    ("", {}),
    ("💡 輸出處方:「強烈建議取消戶外跑步改為室內運動；", {"color": GREEN, "bold": True}),
    ("     預估上午 10 點逆溫打破後好轉，外出請配戴 N95。」", {"color": GREEN, "bold": True}),
    ("     [依據: 台灣環境部古亭站預測 / WHO 2021 Air Guidelines]", {"color": CYAN, "size": 12}),
], 14)

# ---------------- 12. Pseudocode ----------------
s = new_slide("核心演算法 Pseudocode", "Algorithm 1 — AI Air Doctor Agent 推理與安全護欄管線")
rect(s, 0.6, 1.55, 12.1, 5.25, RGBColor(0x02, 0x06, 0x17), line=CARD2)
code = """Algorithm 1: AI Air Doctor Reasoning and Advisory Pipeline
Input : User query string Q, User profile record U
Output: Verified advisory report R, Risk level score S, Citation list C

01: (location, target_time, activity) ← LLM_EntityExtractor(Q)
02: user_group ← U.medical_condition ;  activity_weight ← LookupActivityFactor(activity)
03: if target_time ≤ CurrentTimestamp() + 1h then
04:     raw_aq ← Tool_FetchRealtimeAQ(location) ;  raw_wx ← Tool_FetchRealtimeWeather(location)
05:     pm25_val ← CalibrateMicroSensor(raw_aq, raw_wx.humidity).pm25
06:     shap_explanations ← "Direct Real-time Observation"
07: else
08:     features ← BuildLagAndMeteoFeatures(location, horizon=target_time)
09:     pm25_val ← Tool_RunForecastModel(features) ;  shap_explanations ← Tool_RunSHAPExplainer(features)
10: end if
11: effective_dose ← pm25_val * activity_weight
12: S ← ComputeRiskLevel(effective_dose, threshold=GetDynamicThreshold(user_group))
13: knowledge_docs ← Tool_RAGSearch(query=activity, condition=user_group, risk=S, top_k=3)
14: R_candidate ← LLM_Synthesize(Q, pm25_val, S, shap_explanations, knowledge_docs, U)
15: if CheckEvidenceGuardrail(R_candidate, knowledge_docs) is False then
16:     R_candidate ← LLM_SelfRefine(R_candidate, knowledge_docs, mode="strict_citations")
17: end if
18: return FormatResponseWithDisclaimers(R_candidate), S, ExtractSourceMetadata(knowledge_docs)"""
text(s, 0.9, 1.65, 11.6, 5.1, code.split("\n"), 12.5, RGBColor(0xA5, 0xF3, 0xFC), mono=True, spacing=1.0)

# ---------------- 13. Data & Model ----------------
s = new_slide("資料來源與預測模型 Data & ML Pipeline", "100% 台灣官方開放資料 · 民生公共物聯網 · 可解釋時序預測")
table(s, 0.6, 1.65, 7.0, [
    ["資料來源", "核心特徵欄位", "更新頻率"],
    ["環境部標準測站", "PM2.5、PM10、O₃、NO₂、SO₂、AQI", "每小時"],
    ["民生公共物聯網", "社區空氣盒子 PM2.5、溫濕度", "~5 分鐘"],
    ["中央氣象署開放台", "氣溫、相對濕度、風向、風速、雨量", "每小時"],
    ["自建 ESP32 (選做)", "PMS5003 + SHT31 室內微粒感測", "每分鐘"],
], [2.2, 3.3, 1.5], 13, 0.62)
card(s, 7.9, 1.65, 4.8, 3.1, "Algorithm 2 · 時序特徵與模型", [
    "• 資料跨度: 2022–2025 年逐時資料",
    "• 補值機制: 時空 KNN 反距離加權補值",
    "• 特徵工程: Lag 1–24h、風向量分解(u, v)、日夜溫差逆溫指標",
    "• 資料切分: 嚴格 Time-Series Split (2025 為盲測集)",
    "• 預測模型: XGBoost + 2-Layer Bi-LSTM 雙軌，SHAP 歸因"], AMBER, 16, 12.5)
card(s, 0.6, 5.0, 12.1, 1.75, "系統技術選型與 OpenSpec 架構", "Spec-Driven: OpenSpec 1.2.0 (4 Capabilities)   ·   LLM: Gemini / GPT-4o   ·   Agent: LangGraph   ·   "
     "時序 ML: XGBoost、PyTorch、SHAP   ·   向量庫: ChromaDB   ·   介面: FastAPI + Streamlit / LINE Bot", CYAN, 16, 13.5)

# ---------------- 14. Experiments ----------------
s = new_slide("實驗設計與預期成果 Experiments & Expected Findings")
table(s, 0.6, 1.5, 12.1, [
    ["實驗編號", "測試項目", "對比基準 (Baseline)", "評估指標 (Metrics)", "預期達成目標 (統一口徑)"],
    ["E1 數值預測效能", "24h PM2.5 預測", "Persistence (恆常) / 線性回歸", "MAE, RMSE, R² (1h/6h/24h)", "RMSE 降 35%+ (≤9.5), 6h R² ≥ 0.82"],
    ["E2 醫療處方正確性", "30 組醫師審定情境", "原始 GPT-4o / 無時序 RAG", "醫學指引對齊率、幻覺率", "幻覺率 ≤ 2–3%，對齊率 ≥ 95–96%"],
    ["E3 成因可解釋性", "10 場歷史紅害事件", "無 SHAP 之純文字預測", "專家成因歸因評分 (1–5)", "大氣成因吻合度 ≥ 4.5 分"],
    ["E4 系統可用性", "100 次連續併發請求", "傳統多層雲端架構", "端到端延遲、SUS 滿意度問卷", "平均延遲 ≤ 4.2s (95% ≤ 5s), SUS ≥ 80"],
], [1.8, 2.2, 2.7, 2.7, 2.7], 13, 0.6)
text(s, 0.6, 4.75, 6, 0.5, "🎯 Expected Findings (嚴格依據作業規範，不虛構實驗數據)", 17, GREEN, True)
for i, t in enumerate(["24h PM2.5 預測誤差明顯低於 Persistence Baseline，捕捉逆溫驟增能力顯著提升",
                       "Agent 建議正確性與可引用依據達 95% 以上，有效消弭醫療偏方幻覺",
                       "能針對氣喘、孕幼等敏感族群精準換算個人暴露量，提供可執行的生活防護"]):
    rect(s, 0.6 + i * 4.07, 5.3, 3.9, 1.45, CARD)
    text(s, 0.8 + i * 4.07, 5.4, 3.5, 1.3, t, 14, WHITE, anchor=MSO_ANCHOR.MIDDLE)

# ---------------- 17. A2Z SOP Part I (A-O, PA-PM) ----------------
s = new_slide("A2Z SOP 全結構映射總覽 (I)：A–O & PA–PM", "對標《2020 A-Z SOP》完整論文與提案邏輯映射 (docs/AI_Air_Doctor_Proposal_Analysis.md)")
table(s, 0.6, 1.5, 5.95, [
    ["區段", "字母", "A2Z 定義 → AI Air Doctor 落實映射"],
    ["Abstract", "A–C", "A: 790萬/台12.8/152萬人  B: 單點/無預報/RH>75%/幻覺  C: AI Air Doctor"],
    ["Abstract", "D–F", "D: ReAct+IoT+ML+SHAP+RAG  E: E1–E4 規劃  F: Expected Outcomes 不虛構"],
    ["Intro", "G–I", "G: 80+MOENV+萬顆Civil IoT+OpenSpec  H: 晨跑四大關卡  I: ML→MCP/Agent演進"],
    ["Intro", "J–L", "J: 四類系統瓶頸表  K: 工程/技術/知識/應用貢獻  L: 全文 §1–§7 章節導覽"],
    ["Related", "M–O", "M: 1/2 AI + 1/2 Domain  N: 三閉環+RH校正+雙軌護欄  O: §4.3 8篇表→缺口"],
], [1.05, 0.75, 4.15], 11, 0.86)

table(s, 6.75, 1.5, 5.95, [
    ["元件", "A2Z 定義 → Proposed Scheme (PA–PM) 落實映射"],
    ["PA–PB", "目標與基礎：以 WHO 2021 / MOENV 2024 / Civil IoT / TSPCCM 打造可追溯 Agent"],
    ["PC–PD", "有效與典範轉移：用確定性劑量×RAG 取代猜測；由看 AQI 轉為主動處方推演"],
    ["PE–PF", "①–⑧ 模組對應 OpenSpec 4 能力；公式 Dose=C×w_act、風(u,v)、ΔT=Ts−Td"],
    ["PG–PI", "architecture/flowchart 雙圖 + Algo 1 (L01–29) 與 Algo 2 (L01–20) 行號虛擬碼"],
    ["PJ–PM", "65歲氣喘跑者案例 (38×1.8=68.4)；TimeBasedRollingSplit 防洩漏與雙軌不變式"],
], [0.95, 5.0], 11, 0.86)

# ---------------- 18. A2Z SOP Part II (Q-Z) & Review Highlights ----------------
s = new_slide("A2Z SOP 全結構映射 (II)：Q–Z 與綜合審查總檢", "Simulation (Q–V) · Conclusion (W–Z) · 學術誠實度與文獻 DOI 查核")
table(s, 0.6, 1.55, 6.45, [
    ["字母", "A2Z 定義", "AI Air Doctor 驗證與交付落實"],
    ["Q. 指標", "評估指標", "MAE/RMSE/R² (1h/6h/24h)、指引對齊率、幻覺率、Likert、延遲/SUS"],
    ["R. 基準", "比較對象", "Persistence/MLR (E1)、無工具 GPT-4o & 純 RAG (E2)、無 SHAP (E3)"],
    ["S–T", "環境調參", "2022–25 全台逐時、72h SQLite 快取、RH 75/85%閘門、XGB n=500/Bi-LSTM"],
    ["U–V", "產出驗證", "處方+24h趨勢+Top-3 SHAP+Citation；RMSE ≤9.5、對齊 ≥95%、SUS ≥80"],
    ["W–X", "總結專精", "打通感測/預報/暴露/RAG 關卡；專精台灣高濕校正與逆溫預警"],
    ["Y–Z", "交付展望", "GitHub + README + DESIGN.md + OpenSpec + 21頁簡報；無CO₂感測推估展望"],
], [0.95, 1.15, 4.35], 11, 0.72)

review_cards = [
    ("1. 結構完備度：雙規範 × OpenSpec", "完整涵蓋 A–F 摘要與緒論對照、A2Z 26+ 字母映射、8 模組/流程圖/行號虛擬碼，以及 Deep Research (5/3/10)，並以 OpenSpec v1.2.0 驗證 4/4 artifacts。", CYAN),
    ("2. 學術誠實度：嚴守零虛構原則", "所有指標皆明確標註為 Proposed Expected Outcomes，絕不將預期值偽稱為實測結果，且與 DESIGN.md 及 OpenSpec 數值 100% 統一。", GREEN),
    ("3. 文獻查核 & W1–W8 移交標準", "已淘汰 5 筆舊草稿無效引文，確認 [1]–[23] 全數具備 arXiv ID / DOI / 官方來源；後續依 tasks.md 實作並同步回寫 DESIGN.md。", AMBER),
]
for i, (rt, rb, rc) in enumerate(review_cards):
    card(s, 7.25, 1.55 + i * 1.75, 5.45, 1.62, rt, rb, rc, 14.5, 11.5)

# ---------------- 19. A4 High-Density Numbered Infographic ----------------
s = new_slide("系統全覽資訊圖表（A4 橫式高密度編號）", "依據課程 Prompt 製作 (1.1–7.3 全編號 · 3508×2480 300 DPI · docs/img/infographic_A4.png)")
rect(s, 0.55, 1.45, 7.62, 5.38, WHITE)
s.shapes.add_picture(os.path.join(IMG, "infographic_A4.png"), Inches(0.62), Inches(1.51), height=Inches(5.26))
card(s, 8.35, 1.45, 4.38, 5.38, "📐 圖表結構導讀 (1–7)", [
    "1 符合度總覽 (1.1–1.4)：AI Agent、領域知識、數據分析、真實應用。",
    "2 Abstract ↔ Intro (2.1–2.2)：A–F 六段對照與晨跑四支柱痛點。",
    "3 文獻與深研 (3.1–3.5)：1/2 AI + 1/2 Domain 23 篇查證文獻，5 Cores / 3 Trade-offs / 10 Details。",
    "4 Proposed Scheme (4.1–4.4)：①–⑧ 模組、SVG 雙迴圈流程圖、Algo 1 & 2 行號虛擬碼。",
    "5 A2Z SOP Outline (5.1)：A–Z 暨 PA–PM 全 38 項映射。",
    "6–7 評估與結論 (6.1–7.3)：E1–E4 Expected Outcomes 與 OpenSpec 移交。",
], CYAN, 15.5, 12)

# ---------------- 20. Timeline & Handover ----------------
s = new_slide("時程規劃與交接規範 Timeline & Handover Package")
tl = [("W1–2", "Proposal 提案\n文獻 · API 串接", CYAN), ("W3–4", "特徵工程\n預測模型訓練", GREEN),
      ("W5–6", "知識庫 RAG\nAgent 工具開發", AMBER), ("W7", "前端 UI 整合\nStreamlit / LINE", VIOLET),
      ("W8", "四大實驗評估\n期末移交與展示", RED)]
rect(s, 0.9, 3.35, 11.5, 0.08, CARD2, shape=MSO_SHAPE.RECTANGLE)
for i, (w, t, c) in enumerate(tl):
    x = 0.9 + i * 2.6
    o = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x + 0.85), Inches(3.1), Inches(0.55), Inches(0.55))
    o.fill.solid(); o.fill.fore_color.rgb = c; o.line.fill.background()
    text(s, x, 2.3, 2.3, 0.6, w, 22, c, True, PP_ALIGN.CENTER)
    rect(s, x, 4.0, 2.3, 1.5, CARD)
    text(s, x + 0.1, 4.1, 2.1, 1.3, t, 15, WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
rect(s, 0.9, 5.85, 11.5, 0.9, CARD2, line=GREEN)
text(s, 0.9, 5.95, 11.5, 0.8,
     "📦 OpenSpec + Final Handover: 已完成 openspec/changes/ai-air-doctor-mvp/ (proposal/specs/design/tasks) "
     "與 GitHub + README.md + DESIGN.md 雙軌維護，確保下一位開發者無縫執行、驗證與開發。",
     14, WHITE, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

# ---------------- 16. References ----------------
s = new_slide("參考文獻 References (經查證之 2024–2026 核心研究)")
refs = [
    "[1] Health Effects Institute (2025). State of Global Air 2025. Boston, MA: HEI. stateofglobalair.org",
    "[2] WHO (2021). WHO Global Air Quality Guidelines (PM2.5 24h: 15 μg/m³, annual: 5 μg/m³).",
    "[3] 中華民國環境部 (MOENV) (2024/2025). 空氣品質標準修正 (12/30 μg/m³) 與開放資料平台 data.moenv.gov.tw",
    "[4][5] 國科會與環境部 (2025). 民生公共物聯網 (Civil IoT Taiwan) & Chen et al. (2020) IEEE Commun. Mag.",
    "[6][7][8] 中央氣象署 CWA API (2025); Yao et al. (2023) ReAct (ICLR); Lewis et al. (2020) RAG (NeurIPS).",
    "[9] Gao, K. et al. (2025). Instructor-Worker LLM System for LA Wildfires Air Quality. arXiv:2503.00566.",
    "[10] Pan, Y.-E. & Nipu, A. S. (2025). LLM-enhanced Air Quality Monitoring Interface via MCP. arXiv:2511.03706.",
    "[11] Vieira, R. et al. (2026). LLM-based air quality monitoring & alerts (EnQyMo). arXiv:2609.17954.",
    "[12] Dey, P. et al. (2026). Meteorology-Driven GPT4AP for Atmospheric Pollution. arXiv:2603.29974.",
    "[13] Yu, Q. et al. (2024/2025). Health-LLM: Personalized RAG Disease Prediction. arXiv:2402.00746.",
    "[14] Wong, P.-Y. et al. (2024). Explainable Geo-AI + SHAP for PM2.5 in Taiwan. Environ. Pollut. 123974.",
    "[15] Jung, C.-R. et al. (2026). High-res PM2.5 in Taiwan w/ LCS & AOD. J. Expo. Sci. Environ. Epidemiol.",
    "[16] Ku, P.-W. et al. (2025). Ambient PM2.5 & physical activity (1.5M adults). BMC Medicine. (NCHU 團隊)",
    "[17][18][20][22][23] XGBoost (2016); SHAP (2017); Hua (2021)/Jayaratne (2018) RH; Allen (2016) CO₂; Daigle (2003).",
]
text(s, 0.7, 1.4, 12, 4.75, refs, 11.5, WHITE, spacing=1.1)
text(s, 0.7, 6.25, 12, 0.5, "Thank you!  Q & A", 24, CYAN, True, PP_ALIGN.CENTER)

prs.save(OUT)
print("saved", os.path.abspath(OUT))
