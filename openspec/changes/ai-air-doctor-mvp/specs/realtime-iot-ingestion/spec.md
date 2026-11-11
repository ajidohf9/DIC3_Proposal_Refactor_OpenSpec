## ADDED Requirements

### Requirement: Dual-layer spatial station and micro-sensor retrieval
The system SHALL retrieve real-time air quality and meteorological telemetry for a queried coordinate or landmark by matching Taiwan MOENV regulatory stations within 3 km as the baseline, Civil IoT micro-sensors within 1 km for hyper-local spatial resolution, and CWA weather stations for ambient temperature, relative humidity, wind speed, wind direction, and rainfall.

#### Scenario: Normal multi-source retrieval within radius
- **WHEN** a user queries air quality for a Taiwan location with available nearby stations
- **THEN** the collector returns the nearest MOENV regulatory measurements (PM2.5, PM10, O3, NO2, SO2, CO, AQI), weighted Civil IoT micro-sensor readings within 1 km, and CWA meteorological observations together with station identifiers and observation timestamps

### Requirement: Relative-humidity hygroscopic bias compensation
The system MUST apply physical/algorithmic humidity gating and spatial outlier validation when ambient relative humidity (RH) exceeds 75% or when micro-sensor readings spike anomalously relative to nearby stations within 5 km.

#### Scenario: Rainy or high-humidity micro-sensor spike
- **WHEN** a Civil IoT optical micro-sensor reports a sudden PM2.5 surge while ambient RH is above 85% and a nearby MOENV regulatory station within 5 km reports significantly lower concentration
- **THEN** the calibration module applies humidity correction weights or excludes the hygroscopic outlier and flags the micro-sensor calibration adjustment in the telemetry metadata

### Requirement: OpenAPI timeout degradation to local SQLite cache
The system SHALL enforce a 3-second request timeout on external government OpenAPIs and fall back to the latest valid telemetry cached within the preceding 72 hours in local SQLite when an upstream API times out or fails.

#### Scenario: Upstream OpenAPI timeout beyond 3 seconds
- **WHEN** a call to MOENV, Civil IoT, or CWA OpenAPI fails or exceeds 3 seconds
- **THEN** the collector retrieves the most recent valid station record from the 72-hour SQLite cache and attaches an explicit offline-cache warning flag to the returned payload

