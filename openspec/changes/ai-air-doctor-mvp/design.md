## Context

This design converts the root [DESIGN.md](../../../DESIGN.md) specification into an actionable OpenSpec `spec-driven` blueprint for **AI Air Doctor**, an 8-module Domain AI Agent integrating:
- **Client & Gateway**: Streamlit responsive dashboard / LINE Bot (`①⑧`), FastAPI Gateway + local SQLite (`②`, user profiles + 72h station telemetry cache).
- **Reasoning Core**: LangGraph ReAct orchestrator (`③`, `C-1 AgentOrchestrator`) and `C-6 SafetyGuardrail`.
- **Tool & Analytics Layer**: `C-2 MeteoDataCollector` (`④`, MOENV / Civil IoT / CWA OpenAPIs), `C-3 AeroForecastEngine` + `C-4 SHAPExplainer` (`⑤`, XGBoost / 2-layer Bi-LSTM + SHAP), and `C-5 MedicalRAGRetriever` (`⑥`, ChromaDB clinical guidelines).
- **Decision & Output**: Activity-weighted exposure matrix and dual-track threshold filtering (`⑦`), producing structured, source-cited reports (`⑧`) with mandatory medical disclaimers.

Constraints:
- Personal health records must stay strictly in local SQLite (`NFR-3`).
- End-to-end streaming first-token latency ≤ 1.5s and full report ≤ 5s (target ≤ 4.2s) (`NFR-1`, `E4`).
- OpenAPI failures > 3s must gracefully degrade to cached telemetry (`NFR-2`).

## Goals / Non-Goals

**Goals:**
- Deliver an end-to-end runnable MVP covering `src/tools/`, `src/models/`, `src/agent/`, and `src/web/` with full traceability to `specs/`.
- Achieve 24h PM2.5 forecasting RMSE ≤ 9.5 μg/m³ (≥ 35% reduction over Persistence baseline) and 6h $R^2 \ge 0.82$ on the 2025 blind test split including the Taichung representative station subset (`Zhongming/Dali/Xitun`) (`E1`).
- Reach ≥ 95–96% clinical guideline alignment, ≤ 2–3% hallucination rate, and 100% station/citation disclosure across 30 vulnerable/edge scenarios (`E2`), plus ≥ 4.5/5 expert agreement on SHAP atmospheric attributions (`E3`).
- Guarantee ≤ 4.2s average end-to-end latency (95% ≤ 5s), 100% API-timeout/high-RH safe-degradation coverage, and `SUS ≥ 80` (`E4`).
- Maintain full handover reproducibility via `README.md`, `DESIGN.md`, and OpenSpec artifacts.

**Non-Goals:**
- Providing formal clinical medical diagnoses, prescriptions, or emergency triage (explicitly excluded via non-diagnostic disclaimers).
- Replacing regulatory MOENV reference stations for legal pollution enforcement with low-cost Civil IoT sensors.
- End-to-end numerical time-series forecasting inside the LLM prompt without dedicated ML regressors.

## Decisions

### Decision 1: Decouple numerical forecasting (XGBoost / Bi-LSTM + SHAP) from LLM reasoning via Tool Calling
- **Rationale**: LLMs predict discrete text tokens rather than continuous multivariate atmospheric dynamics. Offloading 24h regression to dedicated ML models (`XGBoost` for fast tabular inference; 2-layer `Bi-LSTM` for 24h sequential dependencies, selected via chronological RMSE) and computing Shapley attributions (`SHAPExplainer`) guarantees numerical reproducibility, sub-second inference, and physically grounded explanations.
- **Alternatives Considered**: (a) Prompting GPT-4o/Gemini directly with historical JSON series for end-to-end forecasting (rejected due to numerical hallucination and latency); (b) Using pure LSTM without SHAP (rejected as an unexplainable black box).

### Decision 2: Dual-layer spatial sensing (3 km MOENV baseline + 1 km Civil IoT, 5 km fallback) with RH > 75% gating
- **Rationale**: MOENV regulatory stations offer high gravimetric/beta-attenuation accuracy (~80+ stations) at coarser spacing, whereas Civil IoT micro-sensors capture street-canyon hyper-local hotspots (e.g., 1 km radius) at 5-minute intervals. Because optical micro-sensors suffer particle hygroscopic swelling at RH > 75%, physical consistency checks and humidity weighting prevent false red-alert triggers during rain or fog.
- **Alternatives Considered**: Using MOENV stations only (misses localized traffic/neighborhood spikes) or using raw Civil IoT values uncalibrated (triggers severe false alarms under high humidity).

### Decision 3: Strict chronological splitting (`split_date = 2025-01-01`) for forecasting validation
- **Rationale**: Hourly PM2.5 series exhibit strong temporal autocorrelation; random K-Fold cross-validation leaks adjacent future timestamps into training folds, inflating offline $R^2$ while failing in live deployment. Chronological time-series rolling splits preserve causal forecasting integrity.
- **Alternatives Considered**: Standard 5-fold random CV (rejected due to severe temporal data leakage).

### Decision 4: Local SQLite storage + RAG citation `SafetyGuardrail` with self-refinement
- **Rationale**: Sensitive health attributes (asthma, COPD, pregnancy) remain local in SQLite rather than third-party logs. `SafetyGuardrail` enforces deterministic regex/semantic verification that every recommendation links to a retrieved ChromaDB guideline chunk and monitoring station ID; failures loop back to `LLM_SelfRefine` rather than leaking unverified claims or folk remedies.
- **Alternatives Considered**: Stateless cloud profile storage (rejected on privacy grounds) or unguarded single-pass LLM generation (high hallucination risk ~22% in ungrounded baselines).

## Risks / Trade-offs

- **[Trade-off 1: Micro-sensor density vs. optical humidity bias]** Low-cost sensors reveal hyper-local spikes but inflate readings under RH > 75% (hygroscopic growth) and age over time → **Mitigation**: Apply RH-gated correction weights and cross-check against MOENV stations within 5 km; flag calibrated readings in output metadata.
- **[Trade-off 2: Indoor airtightness vs. CO2 cognitive buildup]** Sealing windows during outdoor red-alert events lowers PM2.5 ingress but drives indoor CO2 above 1,000–1,800 ppm, degrading cognition → **Mitigation**: Recommend pulsed 10–15 minute cross-ventilation during forecasted wind/dispersion windows paired with max-CADR HEPA purification afterward.
- **[Trade-off 3: Strict WHO 2021 limits (15 μg/m³) vs. National MOENV 2024 standards (30 μg/m³) & alert fatigue]** Applying WHO limits universally causes excessive alerts for healthy users, whereas national limits under-protect asthmatics → **Mitigation**: Dual-track thresholding switching automatically by `user_profile.medical_condition`, displaying official AQI alongside personalized WHO risk tiers.
- **[Risk: Government OpenAPI downtime or > 3s latency]** Upstream MOENV/Civil IoT/CWA endpoints may stall during peak traffic → **Mitigation**: Enforce 3s HTTP timeout (`tenacity` retries) and degrade automatically to 72h SQLite cache with an explicit offline banner.
- **[Risk: User over-reliance delaying emergency care]** Users with acute dyspnea might rely on the agent instead of urgent medical care → **Mitigation**: Render fixed non-diagnostic emergency disclaimers at top and bottom of every card.

## Verification & Rollout Plan

1. **Phase 1 (Data & Specs)**: Initialize OpenAPI ingestion (`C-2`), RH calibration, and 72h SQLite cache; verify offline fallback and station radius tests.
2. **Phase 2 (ML & SHAP)**: Run `Algorithm 2` on 2022–2025 MOENV + CWA data (`split_date = 2025-01-01`, including the Taichung `Zhongming/Dali/Xitun` subset); benchmark `E1` (XGBoost vs. Bi-LSTM vs. Persistence/MLR) and `E3` (10 episode SHAP reviews).
3. **Phase 3 (RAG & Agent)**: Index WHO 2021, MOENV 2024/2025 & 2025 White Paper morning/evening split, TSPCCM Asthma Manual, HPA Protective 3-Steps, and CADR guidelines into ChromaDB (`C-5`), wire LangGraph ReAct (`C-1`) and `SafetyGuardrail` (`C-6`), and evaluate `E2` on 30 clinician/edge scenarios (≥ 95–96% alignment, 100% citation disclosure).
4. **Phase 4 (Gateway & UI)**: Deploy FastAPI, Streamlit, and LINE Bot (`NFR-1`, `E4` 100 concurrent query load test with timeout/RH fault-injection verifying 100% safe-degradation coverage, ≤ 4.2s avg latency, and `SUS ≥ 80` survey).
5. **Rollback**: Any runtime failure in ML forecasting or ChromaDB falls back cleanly to real-time calibrated MOENV observations + static WHO/MOENV lookup tables with degraded-mode notice.

## Open Questions

- How should pulsed indoor ventilation duration (e.g., 10 vs. 15 min) be dynamically estimated when a household lacks an indoor CO2 sensor (room volume & occupancy heuristic vs. user input)?
- Which primary hosted/local LLM backend (`Gemini` vs. `GPT-4o`) yields the best Chinese medical citation adherence within the ≤ 4.2s latency budget?

