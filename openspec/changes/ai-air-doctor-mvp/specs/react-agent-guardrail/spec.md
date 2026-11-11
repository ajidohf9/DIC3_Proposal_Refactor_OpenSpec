## ADDED Requirements

### Requirement: LangGraph ReAct entity extraction and temporal routing
The system SHALL extract location, target timestamp, and activity intensity from natural-language user queries, prompt the user to supply missing mandatory parameters, and route queries within `current_time + 1h` to real-time IoT ingestion while routing `1–24h` future queries to the ML forecasting and SHAP pipeline.

#### Scenario: Incomplete query missing location or activity
- **WHEN** a user asks "Can I go out tomorrow morning?" without specifying location or activity intensity
- **THEN** the agent requests clarification for the missing location and activity before invoking environmental or forecasting tools

#### Scenario: Future query routed to ML forecasting
- **WHEN** a user asks about jogging at Da'an Forest Park tomorrow at 07:00
- **THEN** the agent routes execution to `forecast_pm25` and `SHAPExplainer` rather than returning current-hour observations

### Requirement: Mandatory evidence citation guardrail and self-refinement loop
The system MUST validate candidate advisory responses through `SafetyGuardrail` before delivery; if a candidate response omits monitoring station identifiers, forecast uncertainty/cache status, or clinical guideline citations, or includes unverified folk remedies, the agent SHALL trigger a self-refinement loop with strict citation constraints.

#### Scenario: Candidate response missing guideline citation or repeating folk myth
- **WHEN** a user asks whether eating wood ear mushrooms or drinking green tea clears inhaled PM2.5, or a generated draft omits a retrieved source citation
- **THEN** `SafetyGuardrail` rejects the ungrounded draft and invokes `LLM_SelfRefine` to state that no clinical evidence supports dietary clearance of alveolar PM2.5 and enforce cited physical protections (HEPA filtration, N95 masks)

### Requirement: Mandatory medical disclaimer and multi-channel delivery
The system SHALL append the standardized medical disclaimer to every advisory output and expose responses through FastAPI, the Streamlit dashboard, and the LINE Bot webhook within an end-to-end target latency of ≤ 5 seconds (streaming first-token ≤ 1.5 seconds).

#### Scenario: Delivering finalized advisory report
- **WHEN** a candidate response passes `SafetyGuardrail`
- **THEN** the gateway formats the response with personalized guidance, 24h trend/SHAP explanation, clickable station and literature citations, and the mandatory non-diagnostic medical disclaimer

