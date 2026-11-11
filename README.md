# 🌫️ AI Air Doctor: 領域智慧空品健康代理人

**結合多源 IoT 感測數據、大氣物理機器學習預測與環境醫學知識的個人化 Domain AI Agent**

> **專案定位核心公式**：  
> `AI Agent (ReAct) + Domain Knowledge (WHO & AQI) + Data Analytics (XGBoost/LSTM + SHAP) + Real-World Application`

---

## 專題簡介
**AI Air Doctor** 是一個專為空氣品質與呼吸健康打造的垂直領域智慧代理人（Domain AI Agent）。  
有別於傳統「僅顯示冷冰冰數值的 App」或「無即時感知、易生幻覺的通用 Chatbot」，本系統深度整合台灣環境監測物聯網與大氣醫學知識：

1. **即時微環境感知**：呼叫 OpenAPI 整合環境部國家標準測站、民生公共物聯網（Civil IoT）微型感測器與氣象署數據。
2. **前瞻趨勢預報**：以 XGBoost 與 LSTM 預測未來 24 小時 PM2.5 濃度，並透過 SHAP 值解析逆溫層與風速成因。
3. **暴露劑量換算**：依據個體健康檔案（氣喘、長者、孕婦）與活動強度換氣係數（靜態 vs 跑步），動態計算實際生理負擔。
4. **臨床指南檢索**：運用 RAG 技術檢索 WHO 2021 與台灣 AQI 臨床防護規範。
5. **安全護欄驗證**：產出 100% 標註數據來源與文獻依據之個人化防護處方，杜絕醫療偏方幻覺。

---

## 提案階段核心交付物（Proposal Package）
- 📄 **主提案文件**：[docs/proposal.md](docs/proposal.md)（完整 A–F 摘要與緒論對照、A2Z SOP 映射總表、1/2 AI + 1/2 Domain 文獻摘要表、Deep Research 與演算法虛擬碼）
- 📑 **Word 正式提案書**：[docs/Proposal_AI_Air_Doctor.docx](docs/Proposal_AI_Air_Doctor.docx)
- 📋 **系統性解析報告（對標《期末專題規範》×《2020 A-Z SOP》）**：[docs/AI_Air_Doctor_Proposal_Analysis.md](docs/AI_Air_Doctor_Proposal_Analysis.md) / [Word 版](docs/AI_Air_Doctor_Proposal_Analysis.docx)
- 🗺️ **A4 橫式高密度編號資訊圖表**：[docs/img/infographic_A4.png](docs/img/infographic_A4.png)（`3508×2480` 300 DPI，涵蓋 `1.1–7.3` 全編號總覽）
- 📊 **簡報投影片**：[docs/Proposal_AI_Air_Doctor.pptx](docs/Proposal_AI_Air_Doctor.pptx)（22 頁專業簡報，涵蓋規範符合度、A–F 結構對照、Deep Research 5/3/10、8 大模組、雙演算法與 A2Z SOP 總覽）
- 🧩 **系統設計與移交文件**：[DESIGN.md](DESIGN.md)（依據 11 步移交鏈條編寫）
- 📐 **OpenSpec 規格驅動工作流**：[openspec/changes/ai-air-doctor-mvp/](openspec/changes/ai-air-doctor-mvp/)（由 `DESIGN.md` 轉換之 `proposal.md`、`specs/*/spec.md`、`design.md` 與 `tasks.md`）

---

## 小組成員與分工

> **指導教授**：陳煥 教授

| 姓名與學號 | 負責角色與模組 | 核心工作項目 |
|---|---|---|
| **7115093066_楊禾睿** (組長) | Agent 核心調度與推理架構 (Agent & Planner) | LangGraph 狀態機、ReAct 工具呼叫管線、例外處理與反思機制 |
| **7115093063_徐崇皓** | 資料工程與時序分析引擎 (Data & ML) | 環境部/氣象署 API 串接、特徵工程、XGBoost/LSTM 模型與 SHAP 歸因 |
| **7115064183_謝秉樺** | 領域知識與 RAG 系統 (Domain Knowledge) | WHO 2021/AQI 規範整理、ChromaDB 向量庫建置、安全護欄 |
| **7115064202_譚人傑** | 架構設計與文件交付 (Architecture & Handover) | 系統架構圖/流程圖、DESIGN.md 維護、Word/PPT 自動生成腳本 |

---

## 資料來源（100% 台灣官方開放資料）
- 🏛️ **環境部環境資料開放平臺**：https://data.moenv.gov.tw (全台標準測站時序)
- 🌐 **民生公共物聯網 Civil IoT Taiwan**：https://ci.taiwan.gov.tw (社區微型空氣盒子 SensorThings API)
- 🌦️ **交通部中央氣象署開放資料平臺**：https://opendata.cwa.gov.tw (溫濕度、風向風速觀測)

---

## 本機重現與執行方式

```bash
# 1. 建立並啟動虛擬環境
python -m venv venv
.\venv\Scripts\activate   # Windows

# 2. 安裝必要套件
pip install python-docx python-pptx matplotlib pillow requests

# 3. 檢查並驗證 OpenSpec 規格與任務進度
openspec.cmd status --change ai-air-doctor-mvp
openspec.cmd validate ai-air-doctor-mvp

# 4. 重新產出架構圖、流程圖與 A4 橫式高密度資訊圖表 (PNG)
python scripts/diagrams.py
python scripts/render_infographic.py

# 5. 自動編譯輸出最新 Word 報告與 PPT 簡報
python scripts/build_docx.py
python scripts/build_pptx.py
```

---

## 免責聲明
本系統僅供個人化環境暴露評估與生活防護參考，不具備臨床醫師醫療診斷或處方效力。如有胸悶、氣喘加劇等急性症狀，請立即就醫。
