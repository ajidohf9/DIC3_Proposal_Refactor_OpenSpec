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
    fig, ax = plt.subplots(figsize=(10.2, 13.6), dpi=220)
    ax.set_xlim(-0.2, 10.0)
    ax.set_ylim(0, 13.6)
    ax.axis("off")
    cx = 4.65
    W, H = 5.55, 0.72

    # Flowchart nodes aligned with proposal.md §6.3 & infographic_A4.png
    box(ax, cx, 13.0, 4.4, 0.62, "開始: 使用者自然語言提問 + 健康檔案", C_USER, shape="round,pad=0.02,rounding_size=0.35")
    box(ax, cx, 12.0, W, H, "① 意圖與實體解析: 時間 T / 地點 L / 活動強度 A", C_STEP)
    box(ax, cx, 10.9, 4.1, 0.76, "輸入參數是否完整?\n(時間 / 地點 / 活動)", C_DECISION, fs=10, shape="round,pad=0.02,rounding_size=0.45")
    box(ax, cx, 9.75, W, H, "② 檢索本機 SQLite 檔案 並載入雙軌門檻", C_STEP)
    box(ax, cx, 8.6, 4.1, 0.82, "查詢時間 T 是當前\n還是未來時段 (1–24h)?", C_DECISION, fs=10, shape="round,pad=0.02,rounding_size=0.45")

    box(ax, 2.05, 7.2, 3.8, H, "③ 抓取即時測站與微型感測\n(MOENV + Civil IoT + CWA)", C_TOOL, fs=9.5)
    box(ax, 7.25, 7.2, 3.8, H, "④ 執行時序預測管線\n(XGBoost / Bi-LSTM + SHAP)", C_TOOL, fs=9.5)

    box(ax, cx, 5.9, W + 0.2, H, "⑤ 容錯與校正: API>3s 降級 72h 快取 · RH>75% 補償 / 5km 比對", C_DATA, fs=9.4)
    box(ax, cx, 4.82, W, H, "⑥ 計算暴露劑量 = PM2.5 × 換氣係數 & 雙軌門檻分級", C_STEP, fs=9.8)
    box(ax, cx, 3.74, W + 0.25, H, "⑦ 依風險等級 RAG 檢索 ChromaDB (WHO / MOENV / TSPCCM)", C_STEP, fs=9.4)
    box(ax, cx, 2.66, W, H, "⑧ LLM 整合推理: 合成個人化處方與 SHAP 成因診斷", C_STEP, fs=9.8)

    box(ax, cx, 1.56, 4.3, 0.76, "SafetyGuardrail: 是否包含\n真實測站與文獻 Citation?", C_DECISION, fs=10, shape="round,pad=0.02,rounding_size=0.45")
    box(ax, cx, 0.52, 4.6, 0.64, "完成: 輸出結構化處方 + 24h預報 + 來源 + 免責聲明", C_OUT, fs=9.5, shape="round,pad=0.02,rounding_size=0.35")

    # Main vertical & branching arrows
    arrow(ax, (cx, 12.66), (cx, 12.38))
    arrow(ax, (cx, 11.62), (cx, 11.30))
    arrow(ax, (cx, 10.50), (cx, 10.13))
    ax.text(cx + 0.18, 10.30, "是 (完整)", fontsize=9.2, color="#10B981", fontweight="bold")
    arrow(ax, (cx, 9.37), (cx, 9.03))

    # Clarification loop on right side without overlapping boxes
    arrow(ax, (6.72, 10.9), (cx + W / 2 + 0.04, 12.0), rad=0.55, color="#D97706")
    ax.text(cx + W / 2 + 0.55, 11.45, "否: 主動追問\n補齊地點/活動", fontsize=9, color="#D97706", fontweight="bold", va="center")

    # Temporal routing arrows with cleanly offset labels
    arrow(ax, (2.75, 8.28), (2.05, 7.60))
    ax.text(1.85, 8.05, "當前 (≤1h)", ha="right", fontsize=9.5, color="#0D9488", fontweight="bold")
    arrow(ax, (6.55, 8.28), (7.25, 7.60))
    ax.text(7.45, 8.05, "未來 (1–24h)", ha="left", fontsize=9.5, color="#0D9488", fontweight="bold")

    arrow(ax, (2.05, 6.82), (3.55, 6.28))
    arrow(ax, (7.25, 6.82), (5.75, 6.28))

    arrow(ax, (cx, 5.52), (cx, 5.20))
    arrow(ax, (cx, 4.44), (cx, 4.12))
    arrow(ax, (cx, 3.36), (cx, 3.04))
    arrow(ax, (cx, 2.28), (cx, 1.96))

    arrow(ax, (cx, 1.16), (cx, 0.86))
    ax.text(cx + 0.18, 1.00, "是 (通過)", fontsize=9.5, color="#10B981", fontweight="bold")

    # Reflection loop for missing citations cleanly placed on right
    arrow(ax, (6.82, 1.56), (cx + W / 2 + 0.04, 2.66), rad=0.50, color="#DC2626")
    ax.text(cx + W / 2 + 0.62, 2.11, "否: 觸發自我反思\n補齊真實出處", fontsize=9.2, color="#DC2626", fontweight="bold", va="center")

    fig.savefig(os.path.join(OUT, "flowchart.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    architecture()
    flowchart()
    print("New numbered diagrams saved to", OUT)
