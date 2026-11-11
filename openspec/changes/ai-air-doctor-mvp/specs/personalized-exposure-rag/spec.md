## ADDED Requirements

### Requirement: Local privacy-preserving user health profile storage
The system MUST store personal health profiles (age, chronic conditions such as asthma or COPD, pregnancy status, and activity preferences) strictly in local SQLite and SHALL NOT transmit un-anonymized personal medical records to external logging services.

#### Scenario: Retrieving user health profile for risk assessment
- **WHEN** a registered user submits a query
- **THEN** the gateway loads the user's medical condition and activity preferences from local SQLite and passes only necessary risk parameters into the local reasoning pipeline

### Requirement: Activity-weighted exposure dose and dual-track risk thresholds
The system SHALL compute effective exposure dose by multiplying PM2.5 concentration by an activity ventilation intensity factor (e.g., rest `1.0`, vigorous running `1.8`) and MUST automatically apply strict WHO 2021 thresholds (low ≤ 15, moderate 16–30, high 31–50, very high > 50 μg/m³) for vulnerable groups instead of general population thresholds (low ≤ 30, moderate 31–50, high 51–70, very high > 70 μg/m³).

#### Scenario: Asthmatic user requests outdoor running advice
- **WHEN** a user with asthma queries about running at a time with forecasted PM2.5 of 38 μg/m³
- **THEN** the engine computes `effective_dose = 38 * 1.8 = 68.4` and classifies the risk level as Very High under the strict WHO 2021 vulnerable-group threshold (> 50 μg/m³)

### Requirement: Verified ChromaDB clinical guideline retrieval
The system SHALL retrieve top-k evidence snippets from a curated ChromaDB collection containing structured clinical and policy documents: WHO 2021 Global Air Quality Guidelines, Taiwan MOENV 2024/2025 AQI Clinical Action Table & 2025 Air Quality Policy White Paper (morning/evening split forecast rules), Taiwan Society of Pulmonary and Critical Care Medicine (TSPCCM) Asthma Consensus Manual, HPA Protective 3-Steps (including 5 cm ventilation gap guidance), and Indoor Ventilation & CADR Selection Guide.

#### Scenario: Retrieving protective guidance for very-high-risk asthma exposure
- **WHEN** `MedicalRAGRetriever` is queried with activity `running`, condition `asthma`, and risk `Very High`
- **THEN** it returns the top-3 matching clinical chunks with exact document identifiers, section titles, and source metadata for citation

