"""Render the A4-landscape high-density numbered infographic (docs/img/infographic_A4.png)."""
import os
import subprocess
import tempfile
from pathlib import Path
from PIL import Image

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "docs" / "img" / "infographic_A4.png"

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

HTML = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8" />
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body {
    width: 1754px;
    height: 1240px;
    overflow: hidden;
    background: #eef3f8;
    font-family: "Microsoft JhengHei", "PingFang TC", "Noto Sans TC", sans-serif;
    color: #0f172a;
    -webkit-font-smoothing: antialiased;
  }
  .page {
    width: 1754px;
    height: 1240px;
    padding: 13px 16px 11px 16px;
    display: flex;
    flex-direction: column;
    gap: 9px;
    background: linear-gradient(180deg, #f1f5f9 0%, #e7eef6 100%);
  }

  /* Header */
  .header {
    background: linear-gradient(90deg, #0b2545 0%, #0e4a6f 52%, #0e7490 100%);
    color: #ffffff;
    border-radius: 10px;
    padding: 9px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 3px 10px rgba(15, 23, 42, 0.14);
    height: 60px;
    flex-shrink: 0;
  }
  .header-left {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .logo-badge {
    width: 40px;
    height: 40px;
    border-radius: 9px;
    background: rgba(34, 211, 238, 0.18);
    border: 1.5px solid #22d3ee;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    font-size: 15px;
    line-height: 1.05;
    text-align: center;
    color: #67e8f9;
  }
  .header h1 {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: 0.4px;
    line-height: 1.15;
  }
  .header h1 span {
    color: #67e8f9;
  }
  .header-sub {
    text-align: right;
    font-size: 11.8px;
    line-height: 1.42;
    color: #e2e8f0;
  }
  .header-sub strong {
    color: #67e8f9;
  }

  /* 3-column grid */
  .grid {
    display: grid;
    grid-template-columns: 545px 606px 551px;
    gap: 10px;
    flex: 1;
    min-height: 0;
  }
  .col {
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-height: 0;
  }

  /* Section panel */
  .panel {
    background: #ffffff;
    border: 1.5px solid #cbd5e1;
    border-radius: 9px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.05);
  }
  .panel-head {
    background: #0f365c;
    color: #ffffff;
    padding: 5px 11px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14.5px;
    font-weight: 700;
    flex-shrink: 0;
  }
  .panel-head.teal { background: #0e7490; }
  .panel-head.emerald { background: #047857; }
  .panel-head.indigo { background: #3730a3; }
  .panel-head.slate { background: #1e293b; }
  .num-pill {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: #f8fafc;
    color: #0f172a;
    font-size: 13px;
    font-weight: 900;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  .panel-body {
    padding: 7px 10px;
    display: flex;
    flex-direction: column;
    gap: 5px;
    flex: 1;
  }

  .subhead {
    font-size: 11.8px;
    font-weight: 800;
    color: #0e7490;
    display: flex;
    align-items: center;
    gap: 5px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 2px;
    margin-top: 1px;
  }
  .subnum {
    background: #0e7490;
    color: #fff;
    border-radius: 4px;
    padding: 0 5px;
    font-size: 10.2px;
    font-weight: 800;
  }
  .subnum.green { background: #047857; }
  .subnum.amber { background: #b45309; }
  .subnum.indigo { background: #3730a3; }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 10.4px;
    line-height: 1.28;
  }
  th, td {
    border: 1px solid #cbd5e1;
    padding: 3px 5px;
    vertical-align: middle;
  }
  th {
    background: #1e3a5f;
    color: #ffffff;
    font-weight: 700;
    text-align: left;
  }
  tr:nth-child(even) td { background: #f8fafc; }
  .ok-badge {
    display: inline-block;
    background: #16a34a;
    color: #ffffff;
    font-weight: 800;
    font-size: 10px;
    padding: 1px 6px;
    border-radius: 10px;
    white-space: nowrap;
  }
  .tag-code {
    font-family: Consolas, monospace;
    background: #e2e8f0;
    color: #0f172a;
    padding: 0 4px;
    border-radius: 3px;
    font-size: 9.7px;
  }

  /* Abstract A-F rows */
  .af-list {
    display: flex;
    flex-direction: column;
    gap: 3px;
  }
  .af-row {
    display: grid;
    grid-template-columns: 22px 92px 1fr;
    align-items: start;
    gap: 5px;
    font-size: 10.3px;
    line-height: 1.26;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 3px 6px;
  }
  .af-letter {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    color: #fff;
    font-weight: 900;
    font-size: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 1px;
  }
  .l-a { background: #0284c7; }
  .l-b { background: #dc2626; }
  .l-c { background: #059669; }
  .l-d { background: #4f46e5; }
  .l-e { background: #d97706; }
  .l-f { background: #0d9488; }
  .af-key { font-weight: 800; color: #1e293b; }
  .af-val { color: #334155; }

  .intro-box {
    background: #ecfeff;
    border: 1px solid #a5f3fc;
    border-left: 4px solid #0891b2;
    border-radius: 5px;
    padding: 4px 7px;
    font-size: 10.3px;
    line-height: 1.3;
  }

  /* Related Work & Deep Research */
  .kv-row {
    font-size: 10.2px;
    line-height: 1.29;
    padding: 3px 6px;
    background: #f8fafc;
    border-left: 3px solid #0e7490;
    border-radius: 3px;
  }
  .kv-row.green { border-left-color: #059669; }
  .kv-row.indigo { border-left-color: #4f46e5; }
  .kv-row strong { color: #0f172a; }

  .dr-box {
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 5px 7px;
    background: #faf5ff;
    font-size: 10.1px;
    line-height: 1.34;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .dr-box b { color: #4338ca; }

  /* Center Column: Architecture, Flowchart, Pseudocode */
  .mod-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 5px;
  }
  .mod-card {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 3.5px solid #0e7490;
    border-radius: 5px;
    padding: 4px 7px;
    font-size: 10px;
    line-height: 1.26;
  }
  .mod-card.agent { border-left-color: #4f46e5; background: #eef2ff; }
  .mod-card.ml { border-left-color: #d97706; }
  .mod-card.rag { border-left-color: #059669; }
  .mod-title { font-weight: 800; color: #0f172a; font-size: 10.5px; }

  .mid-split {
    display: grid;
    grid-template-columns: 266px 1fr;
    gap: 7px;
    align-items: stretch;
  }
  .flow-wrap {
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    background: #f8fafc;
    padding: 4px 2px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .pseudo-wrap {
    border: 1px solid #1e293b;
    border-radius: 6px;
    background: #0f172a;
    color: #e2e8f0;
    padding: 6px 8px;
    font-family: Consolas, "Courier New", monospace;
    font-size: 9.25px;
    line-height: 1.32;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .pseudo-title {
    color: #38bdf8;
    font-weight: 700;
    font-family: "Microsoft JhengHei", sans-serif;
    font-size: 10.3px;
    margin-bottom: 2px;
    border-bottom: 1px solid #334155;
    padding-bottom: 2px;
  }
  .pseudo-line span.ln { color: #64748b; }
  .pseudo-line span.kw { color: #38bdf8; font-weight: 700; }
  .pseudo-line span.fn { color: #34d399; }
  .pseudo-line span.cm { color: #94a3b8; }

  .badge-strip {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 5px;
  }
  .feat-badge {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    border-radius: 5px;
    padding: 4px 5px;
    font-size: 9.9px;
    font-weight: 700;
    color: #065f46;
    text-align: center;
  }

  /* Right Column: A2Z Table, Eval, Conclusion */
  .a2z-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5px;
  }
  .a2z-table {
    font-size: 9.2px;
    line-height: 1.2;
  }
  .a2z-table th, .a2z-table td {
    padding: 2px 3.5px;
  }
  .a2z-let {
    font-weight: 900;
    color: #1e3a8a;
    text-align: center;
    width: 24px;
    background: #dbeafe !important;
  }

  .eval-mini {
    font-size: 9.5px;
    line-height: 1.2;
  }
  .eval-mini th, .eval-mini td {
    padding: 2px 4px;
  }
  .kpi-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 5px;
  }
  .kpi-card {
    background: #fff7ed;
    border: 1px solid #fed7aa;
    border-radius: 6px;
    padding: 4px 4px;
    text-align: center;
  }
  .kpi-card.teal { background: #ecfeff; border-color: #a5f3fc; }
  .kpi-card.green { background: #ecfdf5; border-color: #a7f3d0; }
  .kpi-val {
    font-size: 13.5px;
    font-weight: 900;
    color: #c2410c;
    line-height: 1.1;
  }
  .kpi-card.teal .kpi-val { color: #0e7490; }
  .kpi-card.green .kpi-val { color: #047857; }
  .kpi-lbl {
    font-size: 9.2px;
    color: #334155;
    margin-top: 2px;
    line-height: 1.15;
  }

  .concl-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 5px;
  }
  .concl-card {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 6px;
    padding: 4px 6px;
    font-size: 9.8px;
    line-height: 1.26;
  }
  .concl-card b {
    color: #065f46;
    display: block;
    margin-bottom: 2px;
    font-size: 10.4px;
  }

  .footer {
    height: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 10.5px;
    color: #475569;
    padding: 0 4px;
    flex-shrink: 0;
  }
</style>
</head>
<body>
<div class="page">

  <!-- TOP BANNER -->
  <div class="header">
    <div class="header-left">
      <div class="logo-badge">AI<br/>AIR</div>
      <div>
        <h1><span>AI Air Doctor</span> 專題提案系統性解析資訊圖表</h1>
      </div>
    </div>
    <div class="header-sub">
      <div><strong>對照基準：</strong>《期末專題提案作業規範》×《2020 A-Z SOP》× OpenSpec 1.2.0 Spec-Driven Workflow</div>
      <div><strong>分析對象：</strong>docs/proposal.md · DESIGN.md · Proposal_AI_Air_Doctor.pptx（21 頁）· openspec/changes/ai-air-doctor-mvp</div>
    </div>
  </div>

  <!-- MAIN 3-COLUMN GRID -->
  <div class="grid">

    <!-- LEFT COLUMN: 1, 2, 3 -->
    <div class="col">
      <!-- 1. Compliance Overview -->
      <div class="panel">
        <div class="panel-head"><span class="num-pill">1</span> 符合度總覽：期末專題規範核心維度（1.1–1.4）</div>
        <div class="panel-body">
          <table>
            <thead>
              <tr><th style="width:36px;">編號</th><th style="width:76px;">評估維度</th><th>AI Air Doctor 實作對應與 OpenSpec 規格</th><th style="width:52px;text-align:center;">符合</th></tr>
            </thead>
            <tbody>
              <tr>
                <td><b>1.1</b></td><td><b>AI Agent</b></td>
                <td>LangGraph ReAct 狀態機、參數追問、時態路由、Tool Calling 與 <span class="tag-code">react-agent-guardrail</span> 反思</td>
                <td style="text-align:center;"><span class="ok-badge">✓ 高</span></td>
              </tr>
              <tr>
                <td><b>1.2</b></td><td><b>領域知識</b></td>
                <td>WHO 2021 (15 μg/m³)、MOENV 2024 (12/30)、運動換氣係數 (1.0–1.8×)、RH&gt;75% 吸濕補償與 CO₂ 換氣</td>
                <td style="text-align:center;"><span class="ok-badge">✓ 高</span></td>
              </tr>
              <tr>
                <td><b>1.3</b></td><td><b>數據分析</b></td>
                <td>MOENV (3km) + Civil IoT (1km/5km) + CWA、時空 KNN 補值、風向量 (u,v)、XGBoost/Bi-LSTM + SHAP</td>
                <td style="text-align:center;"><span class="ok-badge">✓ 高</span></td>
              </tr>
              <tr>
                <td><b>1.4</b></td><td><b>真實應用</b></td>
                <td>鎖定台灣 140–200 萬氣喘族群 [21] 與 152 萬人運動閾值 (≥25 μg/m³ 護心減半 [16]) 之個人決策</td>
                <td style="text-align:center;"><span class="ok-badge">✓ 高</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 2. Abstract & Introduction -->
      <div class="panel">
        <div class="panel-head teal"><span class="num-pill">2</span> Abstract 六段式（A–F）與 Introduction（2.1–2.2）</div>
        <div class="panel-body">
          <div class="subhead"><span class="subnum">2.1</span> Abstract A–F 對照與結構分工（對應 Proposal §1–§3）</div>
          <div class="af-list">
            <div class="af-row"><div class="af-letter l-a">A</div><div class="af-key">Attention 引題</div><div class="af-val">HEI 2025 全球 790 萬早逝（PM2.5 佔 490 萬）[1]、台 2024 年均 12.8 / 新標 12·30 [3]、140–200 萬氣喘 [21]、152 萬人 ≥25 μg/m³ 運動效益減半 [16]。</div></div>
            <div class="af-row"><div class="af-letter l-b">B</div><div class="af-key">But 挑戰缺口</div><div class="af-val">現有 App 缺個人暴露與預報；純 ML 缺語意轉譯；通用 LLM 缺即時連線易幻覺；微感測 RH&gt;75% 易虛高 [9–15,20]。</div></div>
            <div class="af-row"><div class="af-letter l-c">C</div><div class="af-key">Cure 核心解藥</div><div class="af-val">提出 <b>AI Air Doctor</b> 個人化 Domain AI Agent，並以 OpenSpec <span class="tag-code">spec-driven</span>（4/4 artifacts）規格驅動實作。</div></div>
            <div class="af-row"><div class="af-letter l-d">D</div><div class="af-key">Development 方法</div><div class="af-val">LangGraph ReAct + MOENV/Civil IoT/CWA + XGBoost/Bi-LSTM + SHAP + 換氣劑量雙軌門檻 + ChromaDB RAG 與護欄 [2–8,17–23]。</div></div>
            <div class="af-row"><div class="af-letter l-e">E</div><div class="af-key">Experiments 評估</div><div class="af-val">E1 2022–2025 盲測 vs Persistence/MLR；E2 30 醫師情境 vs GPT-4o；E3 10 場 SHAP；E4 100 併發/SUS。</div></div>
            <div class="af-row"><div class="af-letter l-f">F</div><div class="af-key">Findings 預期</div><div class="af-val"><b>不虛構數據（僅 Expected）</b>：RMSE ≤9.5 (降35%+)、對齊 ≥95–96%、幻覺 ≤2–3%、100% 引用、延遲 ≤4.2s、SUS ≥80。</div></div>
          </div>
          <div class="subhead"><span class="subnum">2.2</span> Introduction 論證精神（Why is this project worth doing?）</div>
          <div class="intro-box">
            <b>晨跑決策痛點</b>（65 歲氣喘者大安森林公園 07:00 慢跑）：必須同時打通 ① 即時微感測校準、② 24h 前瞻逆溫預報、③ 運動換氣 8–15 倍劑量換算 [23]、④ 雙軌臨床 RAG；完整界定官方 App、ML 黑盒、通用 LLM 與近年政策 Agent [9–12] 之 4 大限制。
          </div>
        </div>
      </div>

      <!-- 3. Related Work & Deep Research -->
      <div class="panel" style="flex:1;">
        <div class="panel-head indigo"><span class="num-pill">3</span> Related Work 與 Deep Research 三大核心問題（3.1–3.5）</div>
        <div class="panel-body">
          <div class="kv-row"><b>3.1 AI × Domain 平衡（1/2 AI + 1/2 Domain）</b>：§4 涵蓋 23 篇經 arXiv/DOI 核實文獻，拒絕單一模型或未驗證引用。</div>
          <div class="kv-row"><b>3.2 AI 技術面</b>：XGBoost [17] / Bi-LSTM + SHAP [14,18,19]；ReAct [7]、RAG [8]、Multi-Agent [9]、MCP [10]、EnQyMo [11]、GPT4AP [12]、Health-LLM [13]。</div>
          <div class="kv-row green"><b>3.3 Domain 面</b>：WHO 2021 [2] 與 MOENV 2024 [3]；RH&gt;75% 吸濕膨脹物理校正 [15,20]；通氣量 <i>V</i><sub>E</sub> 6–8→50–100+ L/min [23]；CO₂ 認知衰退 [22]。</div>
          <div class="kv-row indigo"><b>3.4 Article Summary Table（§4.3）</b>：8 篇 2024–2026 核心研究 [9–16] 對比 Table → 收斂台灣在地整合 Research Gap。</div>
          <div class="subhead"><span class="subnum indigo">3.5</span> Deep Research：5 Cores · 3 Trade-offs · 10 Details（§5）</div>
          <div class="dr-box">
            <div><b>Q1（5 Cores）：</b>① 暴露劑量≠濃度 (C × <i>V</i><sub>E</sub> × T) ② 敏感族群無安全閾值 (WHO 15 μg/m³) ③ 微感測 RH&gt;75% 物理邊界 ④ 大氣逆溫動力主導 ⑤ 前瞻預警重於事後確認 → 全數落實於 OpenSpec 4 項規格。</div>
            <div><b>Q2（3 Trade-offs）：</b>① 1km 微感測密度 ↔ RH&gt;75% 誤差（5km 標準站比對） ② 室外紅害密閉 ↔ 室內 CO₂ &gt;1000ppm 認知降（10–15m 脈衝換氣+HEPA） ③ WHO 嚴標 ↔ 法定標準警報疲勞（雙軌揭露）。</div>
            <div><b>Q3（10 Details）：</b>涵蓋夏季 O₃ 光化學、清晨 200m 輻射逆溫、RH 95% 假警報、PM2.5/PM10 沙塵溯源、嚴禁 Random K-Fold 防洩漏、黑木耳偏方護欄、ML 與 LLM 解耦等 10 道深層領域推理。</div>
          </div>
        </div>
      </div>
    </div>

    <!-- CENTER COLUMN: 4 -->
    <div class="col">
      <div class="panel" style="flex:1;">
        <div class="panel-head slate"><span class="num-pill">4</span> Proposed Scheme：系統架構與技術表示（4.1–4.4）</div>
        <div class="panel-body">
          <div class="subhead"><span class="subnum">4.1</span> 八大核心模組架構（對應規範 ①～⑧ × OpenSpec Capabilities）</div>
          <div class="mod-grid">
            <div class="mod-card"><div class="mod-title">① User/Scenario</div>氣喘/COPD、跑者、長者與校園戶外活動情境</div>
            <div class="mod-card"><div class="mod-title">② Query/Profile</div>解析時間/地點/活動；本機 SQLite 隱私健康檔</div>
            <div class="mod-card agent"><div class="mod-title">③ Planner Agent [react-agent-guardrail]</div>LangGraph ReAct 追問、時態路由與工具調度</div>
            <div class="mod-card"><div class="mod-title">④ Data Acquisition [realtime-iot-ingestion]</div>MOENV 3km + Civil IoT 1km(RH補償/5km比對)+72h快取</div>
            <div class="mod-card ml"><div class="mod-title">⑤ Analytics Engine [pm25-forecast-shap]</div>時空KNN、風(u,v)、XGBoost/Bi-LSTM 24h預報+SHAP</div>
            <div class="mod-card rag"><div class="mod-title">⑥ Domain KB [personalized-exposure-rag]</div>ChromaDB 臨床指引：WHO 2021、MOENV 2024、TSPCCM</div>
            <div class="mod-card rag"><div class="mod-title">⑦ Decision &amp; Guardrail</div>暴露劑量×雙軌門檻；檢查測站/RAG出處否則自我反思</div>
            <div class="mod-card"><div class="mod-title">⑧ Output &amp; Interaction</div>FastAPI · Streamlit / LINE Bot，結構化建議+免責聲明</div>
          </div>

          <div class="subhead"><span class="subnum">4.2</span> 核心處理流程圖 &amp; <span class="subnum green" style="margin-left:4px;">4.3</span> 雙演算法虛擬碼（§6.3–§6.4）</div>
          <div class="mid-split" style="flex:1;">
            <!-- SVG Flowchart -->
            <div class="flow-wrap">
              <svg viewBox="0 0 264 565" width="260" height="560" xmlns="http://www.w3.org/2000/svg" style="font-family:'Microsoft JhengHei',sans-serif;">
                <defs>
                  <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1 L 10 5 L 0 9 z" fill="#334155"/>
                  </marker>
                  <marker id="arrRed" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626"/>
                  </marker>
                  <marker id="arrAmb" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1 L 10 5 L 0 9 z" fill="#d97706"/>
                  </marker>
                </defs>
                <!-- Start -->
                <rect x="47" y="8" width="170" height="29" rx="14.5" fill="#0f766e"/>
                <text x="132" y="26" text-anchor="middle" fill="#fff" font-size="10.5" font-weight="700">開始：輸入查詢 Q + 健康檔 U</text>
                <line x1="132" y1="37" x2="132" y2="54" stroke="#334155" stroke-width="1.5" marker-end="url(#arr)"/>

                <!-- Step 1 -->
                <rect x="42" y="56" width="180" height="31" rx="5" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.3"/>
                <text x="132" y="75" text-anchor="middle" fill="#0c4a6e" font-size="10.2" font-weight="700">語意抽取 (時間 T, 地點 L, 活動 A)</text>
                <line x1="132" y1="87" x2="132" y2="104" stroke="#334155" stroke-width="1.5" marker-end="url(#arr)"/>

                <!-- Valid? Diamond -->
                <polygon points="132,106 202,131 132,156 62,131" fill="#fef3c7" stroke="#d97706" stroke-width="1.3"/>
                <text x="132" y="134" text-anchor="middle" fill="#78350f" font-size="10" font-weight="700">參數是否完整?</text>
                <!-- Clarification loop -->
                <line x1="202" y1="131" x2="236" y2="131" stroke="#d97706" stroke-width="1.4"/>
                <line x1="236" y1="131" x2="236" y2="71" stroke="#d97706" stroke-width="1.4"/>
                <line x1="236" y1="71" x2="225" y2="71" stroke="#d97706" stroke-width="1.4" marker-end="url(#arrAmb)"/>
                <text x="247" y="106" text-anchor="middle" fill="#b45309" font-size="8.6" font-weight="700" transform="rotate(-90 247 106)">否：追問</text>

                <line x1="132" y1="156" x2="132" y2="174" stroke="#334155" stroke-width="1.5" marker-end="url(#arr)"/>
                <text x="139" y="169" fill="#15803d" font-size="9" font-weight="700">是</text>

                <!-- Time split -->
                <polygon points="132,176 206,201 132,226 58,201" fill="#ede9fe" stroke="#6d28d9" stroke-width="1.3"/>
                <text x="132" y="204" text-anchor="middle" fill="#4c1d95" font-size="10" font-weight="700">未來時段 (1–24h)?</text>

                <!-- Left: Realtime | Right: Forecast -->
                <path d="M 58 201 L 34 201 L 34 239" fill="none" stroke="#334155" stroke-width="1.3" marker-end="url(#arr)"/>
                <path d="M 206 201 L 230 201 L 230 239" fill="none" stroke="#334155" stroke-width="1.3" marker-end="url(#arr)"/>
                <text x="41" y="220" fill="#0369a1" font-size="8.8" font-weight="700">即時</text>
                <text x="206" y="220" fill="#6d28d9" font-size="8.8" font-weight="700">未來</text>

                <rect x="10" y="242" width="114" height="35" rx="5" fill="#ffffff" stroke="#0284c7" stroke-width="1.2"/>
                <text x="67" y="257" text-anchor="middle" fill="#0f172a" font-size="9" font-weight="700">get_realtime_aq</text>
                <text x="67" y="270" text-anchor="middle" fill="#475569" font-size="8.2">MOENV+Civil IoT+CWA</text>

                <rect x="136" y="242" width="120" height="35" rx="5" fill="#ffffff" stroke="#6d28d9" stroke-width="1.2"/>
                <text x="196" y="257" text-anchor="middle" fill="#0f172a" font-size="9" font-weight="700">forecast_pm25</text>
                <text x="196" y="270" text-anchor="middle" fill="#475569" font-size="8.2">XGBoost/Bi-LSTM+SHAP</text>

                <!-- Exception / RH calibration -->
                <path d="M 67 277 L 67 292 L 132 292 L 132 303" fill="none" stroke="#334155" stroke-width="1.3"/>
                <path d="M 196 277 L 196 292 L 132 292" fill="none" stroke="#334155" stroke-width="1.3"/>
                <rect x="18" y="303" width="228" height="34" rx="5" fill="#fff7ed" stroke="#ea580c" stroke-width="1.2"/>
                <text x="132" y="317" text-anchor="middle" fill="#9a3412" font-size="9.2" font-weight="700">容錯檢查：API&gt;3s 降級 72h 快取</text>
                <text x="132" y="330" text-anchor="middle" fill="#9a3412" font-size="8.5">RH&gt;75% 吸濕補償 / 異常擴至 5km 比對</text>
                <line x1="132" y1="337" x2="132" y2="352" stroke="#334155" stroke-width="1.5" marker-end="url(#arr)"/>

                <!-- Dose & Threshold -->
                <rect x="22" y="354" width="220" height="33" rx="5" fill="#ecfdf5" stroke="#059669" stroke-width="1.2"/>
                <text x="132" y="368" text-anchor="middle" fill="#065f46" font-size="9.4" font-weight="700">暴露劑量 = PM2.5 × 換氣係數 (1.0–1.8)</text>
                <text x="132" y="381" text-anchor="middle" fill="#047857" font-size="8.4">雙軌門檻：一般(30) vs 敏感 WHO(15)</text>
                <line x1="132" y1="387" x2="132" y2="402" stroke="#334155" stroke-width="1.5" marker-end="url(#arr)"/>

                <!-- RAG + LLM -->
                <rect x="28" y="404" width="208" height="33" rx="5" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.2"/>
                <text x="132" y="418" text-anchor="middle" fill="#0c4a6e" font-size="9.4" font-weight="700">ChromaDB RAG 檢索 + LLM 合成處方</text>
                <text x="132" y="431" text-anchor="middle" fill="#0369a1" font-size="8.4">整合 SHAP 成因與醫學指引段落</text>
                <line x1="132" y1="437" x2="132" y2="452" stroke="#334155" stroke-width="1.5" marker-end="url(#arr)"/>

                <!-- Guardrail diamond -->
                <polygon points="132,454 214,481 132,508 50,481" fill="#fee2e2" stroke="#dc2626" stroke-width="1.3"/>
                <text x="132" y="478" text-anchor="middle" fill="#7f1d1d" font-size="9.3" font-weight="700">SafetyGuardrail:</text>
                <text x="132" y="490" text-anchor="middle" fill="#7f1d1d" font-size="8.6">含測站 &amp; Citation?</text>
                <!-- Reflect loop cleanly separated from left text -->
                <path d="M 50 481 L 20 481 L 20 420 L 25 420" fill="none" stroke="#dc2626" stroke-width="1.4" marker-end="url(#arrRed)"/>
                <text x="11" y="451" text-anchor="middle" fill="#b91c1c" font-size="8.4" font-weight="700" transform="rotate(-90 11 451)">否：自我反思</text>

                <line x1="132" y1="508" x2="132" y2="525" stroke="#334155" stroke-width="1.5" marker-end="url(#arr)"/>
                <text x="139" y="521" fill="#15803d" font-size="9" font-weight="700">是</text>

                <!-- Final -->
                <rect x="24" y="527" width="216" height="30" rx="15" fill="#0f365c"/>
                <text x="132" y="545" text-anchor="middle" fill="#fff" font-size="9.6" font-weight="700">輸出：處方 + 24h預報 + 出處 + 免責聲明</text>
              </svg>
            </div>

            <!-- Pseudocode Box -->
            <div class="pseudo-wrap">
              <div>
                <div class="pseudo-title">Algorithm 1：AI Air Doctor 主代理人推理管線（L01–L29）</div>
                <div class="pseudo-line"><span class="ln">01:</span> B ← ∅ ; (loc, T, act) ← <span class="fn">LLM_EntityExtractor</span>(Q)</div>
                <div class="pseudo-line"><span class="ln">03:</span> <span class="kw">while</span> missing(loc) <span class="kw">or</span> missing(act) <span class="kw">do</span></div>
                <div class="pseudo-line"><span class="ln">04:</span> &nbsp;&nbsp;(loc, act) ← <span class="fn">PromptUserClarification</span>(loc, act)</div>
                <div class="pseudo-line"><span class="ln">06:</span> grp ← U.medical_condition ; w ← <span class="fn">ActivityFactor</span>(act)</div>
                <div class="pseudo-line"><span class="ln">08:</span> <span class="kw">if</span> T ≤ CurrentTimestamp() + 1h <span class="kw">then</span></div>
                <div class="pseudo-line"><span class="ln">09:</span> &nbsp;&nbsp;raw_aq ← <span class="fn">FetchRealtimeAQ</span>(loc, timeout=3s, ttl=72h)</div>
                <div class="pseudo-line"><span class="ln">10:</span> &nbsp;&nbsp;raw_wx ← <span class="fn">FetchRealtimeWeather</span>(loc, timeout=3s)</div>
                <div class="pseudo-line"><span class="ln">11:</span> &nbsp;&nbsp;pm25 ← <span class="fn">CalibrateMicroSensor</span>(raw_aq, raw_wx.RH, 5km)</div>
                <div class="pseudo-line"><span class="ln">13:</span> &nbsp;&nbsp;shap ← "Direct Real-time Observation"</div>
                <div class="pseudo-line"><span class="ln">14:</span> <span class="kw">else</span></div>
                <div class="pseudo-line"><span class="ln">15:</span> &nbsp;&nbsp;feat ← <span class="fn">BuildLagAndMeteoFeatures</span>(loc, horizon=T)</div>
                <div class="pseudo-line"><span class="ln">16:</span> &nbsp;&nbsp;(pm25, CI) ← <span class="fn">Tool_RunForecastModel</span>(feat)</div>
                <div class="pseudo-line"><span class="ln">17:</span> &nbsp;&nbsp;shap ← <span class="fn">Tool_RunSHAPExplainer</span>(feat, top_k=3)</div>
                <div class="pseudo-line"><span class="ln">19:</span> dose ← pm25 * w ; th ← <span class="fn">GetDynamicThreshold</span>(grp)</div>
                <div class="pseudo-line"><span class="ln">21:</span> S ← <span class="fn">ComputeRiskLevel</span>(dose, th) <span class="cm">// WHO(15)/MOENV(30)</span></div>
                <div class="pseudo-line"><span class="ln">22:</span> docs ← <span class="fn">Tool_RAGSearch</span>(act, grp, risk=S, top_k=3)</div>
                <div class="pseudo-line"><span class="ln">23:</span> R ← <span class="fn">LLM_Synthesize</span>(Q, pm25, S, shap, docs, U)</div>
                <div class="pseudo-line"><span class="ln">24:</span> <span class="kw">while</span> !<span class="fn">CheckEvidenceGuardrail</span>(R, docs, raw_aq) <span class="kw">do</span></div>
                <div class="pseudo-line"><span class="ln">25:</span> &nbsp;&nbsp;R ← <span class="fn">LLM_SelfRefine</span>(R, docs, mode="strict_citations")</div>
                <div class="pseudo-line"><span class="ln">27:</span> <span class="kw">return</span> (<span class="fn">FormatWithDisclaimers</span>(R), S, <span class="fn">ExtractMeta</span>(docs))</div>
              </div>
              <div style="border-top:1px solid #334155; padding-top:6px;">
                <div class="pseudo-title">Algorithm 2：時空防漏預測管線（2022–2025, H=24h）</div>
                <div class="pseudo-line"><span class="ln">01:</span> D ← <span class="fn">ImputeGapsLinearAndKNN</span>(D, gap=3h, k=5)</div>
                <div class="pseudo-line"><span class="ln">02:</span> D ← <span class="fn">FilterHumidityAnomalies</span>(D, threshold_RH=95%)</div>
                <div class="pseudo-line"><span class="ln">04:</span> <span class="kw">for</span> each t in D <span class="kw">do</span></div>
                <div class="pseudo-line"><span class="ln">05:</span> &nbsp;&nbsp;u ← -spd*sin(dir*π/180); v ← -spd*cos(dir*π/180)</div>
                <div class="pseudo-line"><span class="ln">07:</span> &nbsp;&nbsp;lags ← <span class="fn">ExtractLags</span>(pm25, t, [1,2,3,6,12,24])</div>
                <div class="pseudo-line"><span class="ln">08:</span> &nbsp;&nbsp;diurnal ← [sin(2π*t.h/24), cos(2π*t.h/24)]</div>
                <div class="pseudo-line"><span class="ln">09:</span> &nbsp;&nbsp;inv_pot ← T_surface - T_dewpoint</div>
                <div class="pseudo-line"><span class="ln">10:</span> &nbsp;&nbsp;F.append([lags, u, v, diurnal, inv_pot, RH])</div>
                <div class="pseudo-line"><span class="ln">12:</span> (Tr, Te) ← <span class="fn">TimeBasedRollingSplit</span>(F, "2025-01-01")</div>
                <div class="pseudo-line"><span class="ln">13:</span> M_base ← <span class="fn">Persistence</span>(Tr); M_xgb ← <span class="fn">XGBoost</span>(Tr, n=500)</div>
                <div class="pseudo-line"><span class="ln">15:</span> M_lstm ← <span class="fn">BiLSTM</span>(Tr, seq=24, hidden=128, drop=0.2)</div>
                <div class="pseudo-line"><span class="ln">19:</span> <span class="kw">return</span> <span class="fn">SelectBestByRMSE</span>(M_base, M_xgb, M_lstm, Te)</div>
              </div>
            </div>
          </div>

          <div class="subhead"><span class="subnum green">4.4</span> 系統關鍵工程特色總結</div>
          <div class="badge-strip">
            <div class="feat-badge">✓ 雙層感知 3km + 1km/5km</div>
            <div class="feat-badge">✓ RH&gt;75% 物理校準 + 72h快取</div>
            <div class="feat-badge">✓ 時間嚴格切分防 Data Leakage</div>
            <div class="feat-badge">✓ 換氣係數 × WHO/MOENV 雙軌</div>
            <div class="feat-badge">✓ SafetyGuardrail 反思強制引用</div>
            <div class="feat-badge">✓ OpenSpec 4/4 Artifacts 驗證</div>
          </div>
        </div>
      </div>
    </div>

    <!-- RIGHT COLUMN: 5, 6, 7 -->
    <div class="col">
      <!-- 5. A2Z SOP Outline -->
      <div class="panel">
        <div class="panel-head"><span class="num-pill">5</span> A2Z SOP Outline：26+ 字母結構映射（5.1）</div>
        <div class="panel-body">
          <div class="a2z-grid">
            <table class="a2z-table">
              <thead><tr><th>#</th><th>A2Z 定義 → AI Air Doctor 落實映射</th></tr></thead>
              <tbody>
                <tr><td class="a2z-let">A</td><td><b>引題</b>：HEI 790萬早逝、台年均12.8、152萬人運動研究</td></tr>
                <tr><td class="a2z-let">B</td><td><b>挑戰</b>：缺個人暴露預報、RH&gt;75%誤差、LLM醫療幻覺</td></tr>
                <tr><td class="a2z-let">C</td><td><b>解藥</b>：AI Air Doctor Domain Agent + OpenSpec SDD</td></tr>
                <tr><td class="a2z-let">D</td><td><b>方法</b>：ReAct+雙層IoT+XGBoost/Bi-LSTM+SHAP+RAG</td></tr>
                <tr><td class="a2z-let">E</td><td><b>評估</b>：2022–25盲測(E1)、30情境(E2)、10 SHAP(E3)、E4</td></tr>
                <tr><td class="a2z-let">F</td><td><b>成果</b>：不虛構；RMSE≤9.5、對齊≥95%、幻覺≤2–3%</td></tr>
                <tr><td class="a2z-let">G</td><td><b>背景</b>：80+MOENV站、上萬Civil IoT、CWA、MCP/OpenSpec</td></tr>
                <tr><td class="a2z-let">H</td><td><b>瓶頸</b>：公式數值無法轉譯、LLM脫離台灣感測與醫學約束</td></tr>
                <tr><td class="a2z-let">I</td><td><b>文獻</b>：XGBoost/Geo-AI [14,19]→MCP/Policy Agent [9–12]</td></tr>
                <tr><td class="a2z-let">J</td><td><b>評析</b>：App被動、ML缺語言、LLM幻覺、近年缺雙軌校正</td></tr>
                <tr><td class="a2z-let">K</td><td><b>貢獻</b>：OpenSpec規格、台灣時序管線、向量指南、雙端UI</td></tr>
                <tr><td class="a2z-let">L</td><td><b>導覽</b>：摘要↔緒論對照、文獻、5/3/10深研、8模組、指標</td></tr>
                <tr><td class="a2z-let">M</td><td><b>分類</b>：1/2 AI（ML/SHAP/Agent/RAG）+ 1/2 Domain（物/醫）</td></tr>
                <tr><td class="a2z-let">N</td><td><b>創新</b>：感測+預測+RAG閉環、RH補償、雙軌門檻與護欄</td></tr>
                <tr><td class="a2z-let">O</td><td><b>歸納</b>：§4.3 8篇2024–26比較表 → §4.4 Research Gap</td></tr>
                <tr><td class="a2z-let">PA</td><td><b>目標</b>：實現有測站與醫學實證可追溯的個人空品健康代理人</td></tr>
                <tr><td class="a2z-let">PB</td><td><b>基礎</b>：WHO 2021、MOENV 2024、Civil IoT、TSPCCM、COGfx</td></tr>
                <tr><td class="a2z-let">PC</td><td><b>有效</b>：以確定性劑量×RAG×Guardrail替代黑盒生成</td></tr>
              </tbody>
            </table>
            <table class="a2z-table">
              <thead><tr><th>#</th><th>A2Z 定義 → AI Air Doctor 落實映射</th></tr></thead>
              <tbody>
                <tr><td class="a2z-let">PD</td><td><b>典範</b>：由「看AQI數字」轉為「主動推演個人安全處方」</td></tr>
                <tr><td class="a2z-let">PE</td><td><b>元件</b>：①–⑧ 八模組對應 4 大 OpenSpec Capabilities</td></tr>
                <tr><td class="a2z-let">PF</td><td><b>公式</b>：Dose=C×w_act；風(u,v)；逆溫潛勢ΔT=Ts−Td</td></tr>
                <tr><td class="a2z-let">PG</td><td><b>圖示</b>：architecture.png (8模組) + flowchart.png (雙迴圈)</td></tr>
                <tr><td class="a2z-let">PH</td><td><b>達成</b>：時態路由、RH&gt;75%校正、時序雙軌模型+SHAP</td></tr>
                <tr><td class="a2z-let">PI</td><td><b>實作</b>：Algo 1 (L01–29) + Algo 2 (L01–20) 具行號虛擬碼</td></tr>
                <tr><td class="a2z-let">PJ</td><td><b>範例</b>：65歲氣喘者07:00大安公園跑步(38×1.8=68.4紅害)</td></tr>
                <tr><td class="a2z-let">PK</td><td><b>亮點</b>：Specs驗證、防洩漏預測、結構化臨床庫、開源互動</td></tr>
                <tr><td class="a2z-let">PL</td><td><b>後續</b>：2025盲測、30組醫師案例對比、10場專家SHAP評核</td></tr>
                <tr><td class="a2z-let">PM</td><td><b>邏輯</b>：TimeBasedRollingSplit 防洩漏與雙軌門檻不變式</td></tr>
                <tr><td class="a2z-let">Q</td><td><b>指標</b>：MAE/RMSE/R²、對齊率、幻覺率、Likert、延遲/SUS</td></tr>
                <tr><td class="a2z-let">R</td><td><b>比較</b>：Persistence/MLR、無工具GPT-4o、純RAG、無SHAP</td></tr>
                <tr><td class="a2z-let">S</td><td><b>環境</b>：2022–25台測站全量、ChromaDB、SQLite 72h快取</td></tr>
                <tr><td class="a2z-let">T</td><td><b>調參</b>：RH 75%/85%閘門、XGB n=500/lr=0.03、LSTM d=0.2</td></tr>
                <tr><td class="a2z-let">U</td><td><b>產出</b>：防護處方+24h趨勢+Top-3 SHAP+測站/文獻Citation</td></tr>
                <tr><td class="a2z-let">V</td><td><b>驗證</b>：OpenSpec Scenarios + E1–E4 預計量化驗收標準</td></tr>
                <tr><td class="a2z-let">W</td><td><b>總結</b>：打通感測、預報、暴露生理與臨床RAG四道關鍵關卡</td></tr>
                <tr><td class="a2z-let">X</td><td><b>專精</b>：台灣季風逆溫、高濕微感測網與氣喘戶外運動場景</td></tr>
                <tr><td class="a2z-let">Y</td><td><b>交付</b>：GitHub Repo + README + DESIGN.md + OpenSpec + PPT</td></tr>
                <tr><td class="a2z-let">Z</td><td><b>展望</b>：實作 W1–W8 與無 CO₂ 感測推估換氣擴充議題</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- 6. Evaluation & Expected Outcomes -->
      <div class="panel">
        <div class="panel-head"><span class="num-pill">6</span> 評估規劃與預期成效（6.1–6.3，嚴禁虛構實驗數據）</div>
        <div class="panel-body">
          <div class="subhead"><span class="subnum amber">6.1</span> 實驗設計矩陣（§6.5 E1–E4）</div>
          <table class="eval-mini">
            <thead><tr><th style="width:28px;">#</th><th>資料集 / 對象</th><th>Baseline 對比基準</th><th>評估指標</th></tr></thead>
            <tbody>
              <tr><td><b>E1</b></td><td>MOENV 2022–25 (2025 盲測)</td><td>Persistence · 多元線性回歸</td><td>MAE / RMSE / R²</td></tr>
              <tr><td><b>E2</b></td><td>30 組醫師審定合成情境</td><td>無工具 GPT-4o · 純 RAG</td><td>對齊率 / 幻覺率</td></tr>
              <tr><td><b>E3</b></td><td>10 場台灣典型紅害事件</td><td>無 SHAP 之純文字預測</td><td>Likert (1–5) 一致</td></tr>
              <tr><td><b>E4</b></td><td>100 次並行自然語言查詢</td><td>傳統多層雲端推理架構</td><td>延遲 · SUS 分數</td></tr>
            </tbody>
          </table>
          <div class="subhead"><span class="subnum amber">6.2</span> 預期成效（Expected Outcomes Only）</div>
          <div class="kpi-row">
            <div class="kpi-card"><div class="kpi-val">≤ 9.5 μg/m³</div><div class="kpi-lbl">E1: 24h RMSE<br/>降35%+ / 6h R²≥0.82</div></div>
            <div class="kpi-card green"><div class="kpi-val">≥ 95–96%</div><div class="kpi-lbl">E2: 指引對齊率<br/>幻覺率 ≤ 2–3%</div></div>
            <div class="kpi-card teal"><div class="kpi-val">≥ 4.5 / 5</div><div class="kpi-lbl">E3: SHAP 歸因<br/>10場專家吻合度</div></div>
            <div class="kpi-card teal"><div class="kpi-val">≤ 4.2s / ≥80</div><div class="kpi-lbl">E4: 平均延遲<br/>SUS 系統易用性</div></div>
          </div>
          <div class="kv-row green"><b>6.3 實證與容錯成果價值</b>：100% 測站與 RAG 出處追溯；API&gt;3s 自動降級 72h 本地快取；固定渲染免責聲明。</div>
        </div>
      </div>

      <!-- 7. Conclusion & Handover -->
      <div class="panel" style="flex:1;">
        <div class="panel-head emerald"><span class="num-pill">7</span> 整體結論：符合度、方法完整性與交接亮點（7.1–7.3）</div>
        <div class="panel-body" style="justify-content:space-between;">
          <div class="concl-grid">
            <div class="concl-card">
              <b>7.1 規範 × OpenSpec 雙合規</b>
              完整滿足 4 大核心維度；OpenSpec <span class="tag-code">ai-air-doctor-mvp</span> 通過驗證（4/4 Artifacts Complete）。
            </div>
            <div class="concl-card">
              <b>7.2 A2Z 完整論證閉環</b>
              具備 Abstract↔Intro (A–F)、5 Cores / 3 Trade-offs / 10 Details 及 A2Z 全 26+ 字母映射。
            </div>
            <div class="concl-card">
              <b>7.3 學術誠實與工程移交</b>
              嚴守「未實驗不虛構數據」、23 篇查證文獻 [1–23]、DESIGN.md × GitHub W1–W8 移交標準。
            </div>
          </div>
          <div style="background:#0f365c;color:#e2e8f0;border-radius:6px;padding:4px 9px;font-size:10px;display:flex;justify-content:space-between;align-items:center;">
            <span><b>GitHub Repo:</b> ajidohf9/DIC3_Proposal_Refactor_OpenSpec (Branch: refactor/openspec-proposal)</span>
            <span style="color:#67e8f9;font-weight:700;">No Fabricated Data · Verified Citations [1–23]</span>
          </div>
        </div>
      </div>
    </div>

  </div>

  <div class="footer">
    <span>AI Air Doctor · 國立中興大學 物聯網與智慧系統應用專題 (OpenSpec Spec-Driven Refactor)</span>
    <span>組員：7115093066 楊禾睿 · 7115093063 徐崇皓 · 7115064183 謝秉樺 · 7115064202 譚人傑 ｜ 指導教授：陳煥 教授</span>
  </div>
</div>
</body>
</html>
"""


def find_browser():
    for path in CHROME_PATHS:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("Neither Chrome nor Edge found for headless rendering.")


def render():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    browser = find_browser()
    with tempfile.TemporaryDirectory() as tmp:
        html_path = Path(tmp) / "infographic_A4.html"
        html_path.write_text(HTML, encoding="utf-8")
        cmd = [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--no-first-run",
            "--disable-extensions",
            "--force-device-scale-factor=2",
            "--window-size=1754,1240",
            f"--screenshot={OUT}",
            html_path.as_uri(),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode != 0 or not OUT.exists():
            raise RuntimeError(f"Browser render failed ({res.returncode}): {res.stderr}")
    with Image.open(OUT) as im:
        print("saved", OUT, "size:", im.size)


if __name__ == "__main__":
    render()
