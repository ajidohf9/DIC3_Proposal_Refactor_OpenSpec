## ADDED Requirements

### Requirement: Spatiotemporal imputation and meteorological feature engineering
The system SHALL preprocess historical station telemetry (2022–2025) by imputing gaps ≤ 3 hours via linear interpolation and gaps > 3 hours via spatiotemporal KNN (k=5) or inverse distance weighting (IDW), filtering RH > 95% anomalies, decomposing wind into orthogonal vectors `(u, v)`, and computing lag features (`1, 2, 3, 6, 12, 24h`), diurnal `sin/cos` encodings, and inversion potential (`T_surface - T_dewpoint`).

#### Scenario: Feature matrix construction for target forecast horizon
- **WHEN** historical telemetry contains a 2-hour gap and wind direction/speed observations
- **THEN** the pipeline linearly interpolates the 2-hour gap, computes orthogonal `(u, v)` wind components, generates lag and diurnal features without future data leakage, and produces a normalized feature vector

### Requirement: Strict time-based rolling split and dual-track 24h forecasting
The system MUST partition training and blind evaluation data strictly chronologically (`split_date = 2025-01-01`, prohibiting random K-Fold splitting) and support both XGBoost (`n_estimators=500, max_depth=6, learning_rate=0.03`) and 2-layer Bi-LSTM (`seq_length=24, hidden_units=128, dropout=0.2`) to output 1–24 hour PM2.5 forecasts with 95% confidence intervals, selecting the best model by RMSE.

#### Scenario: Future horizon forecast request (1–24h)
- **WHEN** the agent requests a PM2.5 forecast for a target time between 1 and 24 hours ahead
- **THEN** the forecast engine executes the selected model on lagged and meteorological features and returns hourly predicted PM2.5 concentrations with 95% confidence intervals

### Requirement: SHAP atmospheric causal attribution
The system SHALL compute Shapley additive values via `SHAPExplainer` for forecasted timestamps and translate the top-3 contributing meteorological/lag factors into human-readable atmospheric diagnoses (e.g., weak wind stagnation, inversion potential, or high relative humidity).

#### Scenario: Elevated PM2.5 forecast explanation
- **WHEN** a 24-hour forecast predicts elevated PM2.5 concentration during weak wind (< 1.5 m/s) and high diurnal temperature contrast
- **THEN** the explainer outputs the top-3 SHAP feature contributions in μg/m³ alongside readable atmospheric dispersion causes

