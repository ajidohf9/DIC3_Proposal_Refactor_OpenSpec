## Why

Air pollution remains the second-leading global risk factor for premature mortality (7.9 million deaths in 2023, including 4.9 million from ambient PM2.5), and seasonal leeward accumulation plus radiation inversions in central and southern Taiwan still expose roughly 1.4–2.0 million residents with asthma and other vulnerable groups to acute respiratory hazards. Existing tools fail to bridge raw monitoring data and actionable medical guidance: official AQI apps only broadcast static point values, academic ML/DL predictors output black-box numbers without causal explanations or personal risk translation, and generic LLMs lack live local IoT grounding while hallucinating unverified health remedies. This change establishes the full end-to-end **AI Air Doctor** Domain AI Agent MVP specified in `DESIGN.md` using a spec-driven workflow.

## What Changes

- Introduce a **dual-layer Taiwan environmental ingestion pipeline** integrating MOENV regulatory hourly stations, Civil IoT Taiwan 5-minute micro-sensors, and CWA meteorological observations with relative-humidity (RH > 75%) hygroscopic bias calibration and SQLite 72-hour offline cache fallback.
- Introduce a **24-hour spatiotemporal PM2.5 forecasting and SHAP attribution engine** comparing XGBoost and 2-layer Bi-LSTM on strictly time-split historical data (2022–2025) with orthogonal wind vectors `(u, v)`, diurnal encodings, and surface-dewpoint inversion potential.
- Introduce a **personalized exposure dose and Clinical RAG subsystem** weighting concentration by activity ventilation factors and switching vulnerable users (asthma, COPD, elderly, pregnant) to strict WHO 2021 thresholds (15 μg/m³ 24h) backed by a ChromaDB vector store of clinical guidelines.
- Introduce a **LangGraph ReAct agent orchestrator with `SafetyGuardrail`** that routes queries between real-time observation and 1–24h forecasting, enforces 100% station and guideline citations via self-refinement, preserves health profiles locally in SQLite, and delivers responses via FastAPI, Streamlit, and LINE Bot.

## Capabilities

### New Capabilities
- `realtime-iot-ingestion`: Multi-source retrieval from MOENV, Civil IoT, and CWA OpenAPIs, spatial station matching (3 km regulatory baseline + 1 km micro-sensor priority, expanding to 5 km outlier fallback), RH > 75% optical hygroscopic compensation, and 3-second timeout fallback to local 72-hour SQLite cache.
- `pm25-forecast-shap`: Spatiotemporal missing-data imputation (≤ 3h linear, > 3h KNN/IDW), meteorological feature engineering, time-based rolling split training/inference for XGBoost and Bi-LSTM (1–24h horizon + 95% confidence interval), and top-3 SHAP atmospheric attribution.
- `personalized-exposure-rag`: Local SQLite user health profile management, dynamic activity ventilation dose calculation (`effective_dose = PM2.5 * activity_factor`), dual-track threshold classification (WHO 2021 vs. MOENV 2024/2025), and ChromaDB clinical guideline retrieval.
- `react-agent-guardrail`: LangGraph ReAct intent/entity extraction, temporal routing (real-time vs. 1–24h forecast), `SafetyGuardrail` citation verification and self-refinement loop, mandatory medical disclaimer rendering, and FastAPI/Streamlit/LINE Bot delivery.

### Modified Capabilities
<!-- None: this is the initial spec-driven MVP baseline derived from DESIGN.md. -->

## Impact

- **Planned Source Modules (`src/`)**: `src/tools/` (OpenAPI collectors, RH calibration, ChromaDB RAG), `src/models/` (feature pipeline, XGBoost/LSTM training & inference, SHAP explainer), `src/agent/` (LangGraph state machine, exposure matrix, `SafetyGuardrail`), and `src/web/` (FastAPI gateway, Streamlit dashboard, LINE Bot webhook).
- **Data & Storage**: Local SQLite database for user health profiles and 72-hour station telemetry cache; ChromaDB vector collection populated from WHO 2021, MOENV 2024/2025 AQI, TSPCCM asthma consensus, and indoor ventilation/CADR guidelines.
- **External Dependencies**: `langgraph`, `langchain-core`, `xgboost`, `torch`, `shap`, `scikit-learn`, `chromadb`, `sentence-transformers`, `fastapi`, `streamlit`, `geopy`, `tenacity`, `requests`.
- **Verification**: Covers experiments E1 (2025 blind forecasting benchmark), E2 (30 clinician-reviewed scenarios), E3 (10 historical pollution episode SHAP evaluations), and E4 (100 concurrent query latency & SUS usability tests).

