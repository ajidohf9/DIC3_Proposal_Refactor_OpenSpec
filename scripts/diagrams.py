"""Generate architecture & flowchart diagrams (PNG) for the proposal and PPT."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.family"] = ["Microsoft JhengHei", "Microsoft YaHei", "sans-serif"]
OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "img")
os.makedirs(OUT, exist_ok=True)

C_USER = "#7C3AED"
C_AGENT = "#0284C7"
C_TOOL = "#0D9488"
C_DATA = "#D97706"
C_OUT = "#DC2626"
C_STEP = "#334155"
C_DECISION = "#4F46E5"


def box(ax, x, y, w, h, text, color, fs=10.5, tc="white", shape="round,pad=0.02,rounding_size=0.12"):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=shape,
                                fc=color, ec="none", zorder=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc, zorder=3, fontweight="bold")


def arrow(ax, p1, p2, color="#64748B", text=None, rad=0.0, lw=1.8):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=14, lw=lw,
                                 color=color, zorder=1, connectionstyle=f"arc3,rad={rad}"))
    if text:
        ax.text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 0.15, text, ha="center",
                fontsize=9.5, color=color, fontweight="bold")


def architecture():
    fig, ax = plt.subplots(figsize=(13.5, 7.4), dpi=220)
    ax.set_xlim(0, 13.5)
    ax.set_ylim(-0.45, 7.2)
    ax.axis("off")

    # Title
    ax.text(6.75, 6.82, "AI Air Doctor 系統總體架構圖 (System Architecture)",
            ha="center", fontsize=16, fontweight="bold", color="#0F172A")
    ax.text(6.75, 6.48, "8 大功能模組以 ①②③④⑤⑥⑦⑧ 統一編號 · OpenSpec Spec-Driven 可追溯推理管線",
            ha="center", fontsize=11, color="#64748B")

    # Layer 1 & 2: User Scenario and Query Input
    box(ax, 1.4, 4.95, 2.35, 1.1, "① User & Scenario\n氣喘病患 · 戶外跑者 · 長者", C_USER, fs=9.5)
    box(ax, 1.4, 3.35, 2.35, 1.15, "② Query & Profile\n自然語言提問\n+ 本機健康檔案 (SQLite)", "#6D28D9", fs=9.5)
    arrow(ax, (1.4, 4.38), (1.4, 3.95))

    # Layer 3: Planner & Reasoning Agent
    box(ax, 4.95, 4.05, 2.55, 2.0, "③ Planner & Reasoning\nAgent 大腦 (ReAct)\n━━━━━━━━━━\n意圖解析 · 工具調度\n反思校驗護欄", C_AGENT, fs=10)
    arrow(ax, (2.6, 3.5), (3.65, 3.95))
    ax.text(3.12, 3.95, "傳入查詢", ha="center", fontsize=9, color="#475569", fontweight="bold")

    # Right side: Modules 4, 5, 6
    # Module 4: Data Acquisition
    box(ax, 8.55, 5.5, 2.6, 0.9, "Tool: 即時微環境感測\nMOENV + Civil IoT + CWA", C_TOOL, fs=9.5)
    box(ax, 11.9, 5.5, 2.45, 0.9, "④ Data Acquisition\n環境部 (≤3km) · 微感測 (≤1km)\nRH>75% 校正 · 72h 快取", C_DATA, fs=8.8)
    arrow(ax, (6.25, 4.65), (7.23, 5.5))
    arrow(ax, (9.88, 5.5), (10.65, 5.5))

    # Module 5: Analytics Engine
    box(ax, 8.55, 4.05, 2.6, 0.9, "Tool: PM2.5 預測模型\nXGBoost + 2-Layer Bi-LSTM", C_TOOL, fs=9.2)
    box(ax, 11.9, 4.05, 2.45, 0.9, "⑤ Analytics Engine\n24h 時序預測引擎\n+ SHAP 大氣因果歸因", C_DATA, fs=9)
    arrow(ax, (6.25, 4.05), (7.23, 4.05))
    arrow(ax, (9.88, 4.05), (10.65, 4.05))

    # Module 6: Domain Knowledge
    box(ax, 8.55, 2.6, 2.6, 0.9, "Tool: 醫療指引檢索\nRAG 語意搜尋", C_TOOL, fs=9.5)
    box(ax, 11.9, 2.6, 2.45, 0.9, "⑥ Domain Knowledge\nChromaDB 向量專家庫\nWHO 2021 + MOENV 2024", C_DATA, fs=8.8)
    arrow(ax, (6.25, 3.45), (7.23, 2.6))
    arrow(ax, (9.88, 2.6), (10.65, 2.6))

    # Module 7: Decision Engine
    box(ax, 4.95, 1.35, 3.6, 1.05, "⑦ Decision & Recommendation\n暴露劑量換算 (濃度 × 運動係數)\n+ 敏感族群雙軌門檻 + SafetyGuardrail", C_DECISION, fs=9.2)
    arrow(ax, (4.95, 3.03), (4.95, 1.9))
    ax.text(5.45, 2.45, "推理合成", ha="left", fontsize=9.5, color="#475569", fontweight="bold")

    # Module 8: Output & Interaction
    box(ax, 10.05, 1.35, 3.8, 1.05, "⑧ Output & Interaction\n個人化處方 + 24h 走勢預報\n+ 測站與醫學文獻可追溯 Citation", C_OUT, fs=9.2)
    arrow(ax, (6.78, 1.35), (8.12, 1.35))
    ax.text(7.45, 1.52, "結構化報告", ha="center", fontsize=9, color="#475569", fontweight="bold")

    # Clean bottom return loop from Module 8 to Module 2 without crossing boxes
    arrow(ax, (10.05, 0.8), (1.4, 2.75), rad=-0.28, color="#7C3AED")
    ax.text(5.7, -0.18, "交付使用者介面 (FastAPI · Streamlit / LINE Bot)", ha="center",
            fontsize=9.5, color="#7C3AED", fontweight="bold")

    fig.savefig(os.path.join(OUT, "architecture.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


def flowchart():
    fig, ax = plt.subplots(figsize=(9.5, 12.5), dpi=220)
    ax.set_xlim(0, 9.5)
    ax.set_ylim(0, 12.5)
    ax.axis("off")
    cx = 4.75
    W, H = 4.8, 0.72

    # Flowchart nodes
    box(ax, cx, 11.8, 3.8, 0.65, "開始: 使用者自然語言提問", C_USER, shape="round,pad=0.02,rounding_size=0.35")
    box(ax, cx, 10.75, W, H, "① 意圖實體解析: 地點 / 時間 / 活動強度", C_STEP)
    box(ax, cx, 9.7, W, H, "② 檢索個體檔案 (年齡/氣喘病史) 並載入門檻", C_STEP)
    box(ax, cx, 8.55, 4.0, 0.85, "查詢時間是當前\n還是未來時段 (1~24h)?", C_DECISION, shape="round,pad=0.02,rounding_size=0.45")

    box(ax, 2.2, 7.15, 3.6, H, "③ 抓取即時測站與微型感測\n(環境部 + Civil IoT API)", C_TOOL, fs=9.5)
    box(ax, 7.3, 7.15, 3.6, H, "④ 執行時序預測管線\n(XGBoost / LSTM + SHAP)", C_TOOL, fs=9.5)

    box(ax, cx, 5.85, W, H, "⑤ 感測資料校準與時空補償 (過濾水氣雜訊)", C_STEP)
    box(ax, cx, 4.8, W, H, "⑥ 計算暴露劑量 = PM2.5 × 活動換氣係數", C_STEP)
    box(ax, cx, 3.75, W, H, "⑦ 依風險等級 RAG 檢索 WHO / AQI 臨床處方", C_STEP)
    box(ax, cx, 2.7, W, H, "⑧ LLM 整合推理: 生成處方建議與成因診斷", C_STEP)

    box(ax, cx, 1.6, 4.2, 0.75, "安全護欄: 是否包含\n真實測站與文獻 Citation?", C_DECISION, shape="round,pad=0.02,rounding_size=0.45")
    box(ax, cx, 0.55, 3.6, 0.65, "完成: 輸出結構化報告 + 依據", C_OUT, shape="round,pad=0.02,rounding_size=0.35")

    # Arrows
    arrow(ax, (cx, 11.45), (cx, 11.12))
    arrow(ax, (cx, 10.38), (cx, 10.07))
    arrow(ax, (cx, 9.32), (cx, 9.0))

    arrow(ax, (2.8, 8.2), (2.2, 7.55), text="當前")
    arrow(ax, (6.7, 8.2), (7.3, 7.55), text="未來 (預測)")

    arrow(ax, (2.2, 6.75), (3.6, 6.22))
    arrow(ax, (7.3, 6.75), (5.9, 6.22))

    arrow(ax, (cx, 5.48), (cx, 5.17))
    arrow(ax, (cx, 4.43), (cx, 4.12))
    arrow(ax, (cx, 3.38), (cx, 3.07))
    arrow(ax, (cx, 2.33), (cx, 2.0))

    arrow(ax, (cx, 1.2), (cx, 0.9))
    ax.text(cx + 0.25, 1.05, "是 (通過)", fontsize=9.5, color="#10B981", fontweight="bold")

    # Reflection loop for missing citations
    arrow(ax, (6.85, 1.6), (7.4, 2.7), rad=0.45, color="#DC2626")
    ax.text(8.4, 2.1, "否: 觸發反思重新生成", fontsize=9.5, color="#DC2626", fontweight="bold")

    fig.savefig(os.path.join(OUT, "flowchart.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    architecture()
    flowchart()
    print("New numbered diagrams saved to", OUT)
