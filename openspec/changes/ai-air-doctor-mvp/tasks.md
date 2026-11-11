## 1. Repository Setup & Environment

- [ ] 1.1 Create `requirements.txt` and source directories (`src/agent/`, `src/models/`, `src/tools/`, `src/web/`, `data/`, `tests/`) matching `DESIGN.md`.
- [ ] 1.2 Configure `.env.example` for MOENV, CWA, Civil IoT API keys and LLM credentials without storing secrets in git.

## 2. Multi-Source IoT & Weather Ingestion (`realtime-iot-ingestion`)

- [ ] 2.1 Implement `MeteoDataCollector` in `src/tools/` using `requests`, `geopy`, and `tenacity` to fetch nearest MOENV stations (≤ 3 km), Civil IoT micro-sensors (≤ 1 km), and CWA weather observations.
- [ ] 2.2 Implement RH > 75% optical hygroscopic calibration and 5 km regulatory outlier cross-check filter (`CalibrateMicroSensor`).
- [ ] 2.3 Implement local SQLite 72-hour telemetry cache with 3-second OpenAPI timeout fallback and offline-cache warning metadata.
- [ ] 2.4 Write unit tests verifying station matching, RH > 85% outlier filtering, and 3-second timeout cache fallback.

## 3. Spatiotemporal Forecasting & SHAP Engine (`pm25-forecast-shap`)

- [ ] 3.1 Build historical data loader and preprocessing pipeline (`≤ 3h` linear interpolation, `> 3h` spatiotemporal KNN/IDW imputation, `RH > 95%` anomaly filtering).
- [ ] 3.2 Implement feature engineering (`u`/`v` wind orthogonal decomposition, lag 1–24h, diurnal `sin`/`cos`, inversion potential `T_surface - T_dewpoint`).
- [ ] 3.3 Train and serialize `XGBoost` (`n_estimators=500, max_depth=6, learning_rate=0.03`) and 2-layer `Bi-LSTM` (`seq_length=24, hidden_units=128, dropout=0.2`) using strict chronological split (`split_date = 2025-01-01`).
- [ ] 3.4 Implement `AeroForecastEngine` (24h prediction + 95% CI) and `SHAPExplainer` returning top-3 human-readable atmospheric factors.
- [ ] 3.5 Run Experiment `E1` (1h/6h/24h MAE, RMSE, $R^2$ vs. Persistence & MLR, including the Taichung `Zhongming/Dali/Xitun` blind-test subset) and Experiment `E3` (10 historical pollution episode SHAP evaluations).

## 4. Personalized Exposure & Medical RAG (`personalized-exposure-rag`)

- [ ] 4.1 Implement local SQLite `UserProfile` store (age, chronic condition, pregnancy, activity preferences) ensuring zero un-anonymized external logging.
- [ ] 4.2 Implement `ExposureCalculator` (`effective_dose = PM2.5 * activity_factor`) and dual-track threshold classifier (General AQI vs. Sensitive WHO 2021 limits).
- [ ] 4.3 Curate and index the curated clinical & policy guideline corpus (WHO 2021, MOENV 2024/2025 AQI & 2025 White Paper morning/evening split rules, TSPCCM Asthma Manual, HPA Protective 3-Steps & 5cm ventilation gap, Indoor Ventilation & CADR Guide) into ChromaDB.
- [ ] 4.4 Implement `MedicalRAGRetriever` returning top-k snippets with verifiable document title, section, and citation metadata.

## 5. LangGraph ReAct Agent, Guardrails & UI (`react-agent-guardrail`)

- [ ] 5.1 Implement `AgentOrchestrator` in `src/agent/` using LangGraph ReAct state machine for entity extraction, missing-slot clarification, and temporal routing (`≤ 1h` real-time vs. `1–24h` forecast).
- [ ] 5.2 Implement `SafetyGuardrail` (`CheckEvidenceGuardrail` + `LLM_SelfRefine` loop) enforcing station/guideline citations, debunking unverified folk remedies, and appending fixed medical disclaimers.
- [ ] 5.3 Build FastAPI gateway (`src/web/api.py`), Streamlit interactive dashboard (`src/web/app.py`), and LINE Bot webhook integration.
- [ ] 5.4 Run Experiment `E2` (30 clinician-reviewed & edge scenarios verifying ≥ 95–96% alignment, ≤ 2–3% hallucination, 100% station/citation disclosure) and Experiment `E4` (100 concurrent requests + API/RH fault-injection verifying 100% safe-degradation coverage, ≤ 4.2s avg latency, and `SUS ≥ 80`).

