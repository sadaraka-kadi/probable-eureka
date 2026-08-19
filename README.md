# probable-eureka
**Geothermal Energy Assessment & Site Screening — Utrecht, Netherlands**

An independent refinement and extension of Team KDK's submission for the SPE Africa Datathon 2026. The project evaluates geothermal potential in Utrecht using subsurface data, reservoir characteristics, well information, and multi-criteria site screening.

Original team submission: Team KDK
Independent refinement: Kadi Sadaraka

---

## Project Overview

This repository contains Team KDK's full data pipeline and analysis for the **SPE Africa Datathon 2026**, focused on the geothermal energy project in Utrecht, Netherlands. The work covers well data preprocessing, administrative boundary extraction, ThermoGIS formation screening, and geothermal doublet simulation across four enhancement scenarios to assess Utrecht's thermal energy potential against targets of 5, 10, and 15 MWth. An LCOE analysis is provided for the recommended development scenario.

---

## Team

**Team KDK**
- Kadi Sadaraka : 5980688
- Diana Bosibori : 5618695
- Keith Muderwa : 5742016

---
## Problem Statement

Utrecht, Netherlands seeks to develop its geothermal resources to meet urban 
district heating and cooling demand. The challenge is to assess whether the 
Slochteren aquifer (ROSL_ROSLU) can deliver:

- ≥ 10 MWth for district heating
- ≥ 5 MWth for district cooling

using commercially viable doublet configurations, and to identify the optimal 
enhancement scenario and development locations that meet these targets 
economically.

---

## Repository Structure

```
Team_KDK_Code_V1/
│
├── data/
│   ├── raw/                         # Original, unmodified input data (see data/raw/README.md)
│   └── processed/                   # Cleaned and transformed data
│
├── notebooks/
│   ├── 01_well_data_preprocessing.ipynb
│   ├── 02_utrecht_boundary_extraction.ipynb
│   ├── 03_utrecht_formation_coverage.ipynb
│   └── 04_slochteren_aquifer_simulation.ipynb
│
├── outputs/
│   ├── baseline_results.nc          # Baseline — full spatial grid
│   ├── baseline_viable.csv          # Baseline — viable doublet locations
│   ├── hp_results.nc                # Heat Pump — full spatial grid
│   ├── hp_viable.csv                # Heat Pump — viable doublet locations
│   ├── stim_results.nc              # Stimulation — full spatial grid
│   ├── stim_viable.csv              # Stimulation — viable doublet locations
│   ├── stim_hp_results.nc           # STIM+HP — full spatial grid
│   ├── stim_hp_viable.csv           # STIM+HP — viable doublet locations
│   ├── nearby_stim_hp.csv           # STIM+HP — viable locations near Utrecht city
│   └── power_and_npv_map.png        # STIM+HP — top 3 locations map
│
├── reports/
│   ├── Team_KDK_LCOE.xlsx             # LCOE spreadsheet
|   ├── lcoe_parameters.md             # LCOE parameter justifications
|   ├── nearby_stim_hp.csv             # STIM+HP — viable locations near Utrecht city
|   ├── power_and_npv_map.png          # STIM+HP — top 3 locations map
|   ├── stim_hp_viable.csv             # STIM+HP — viable doublet locations
│   └── surface_facilities.md          # Surface facilities for Utrecht
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## Data

> ⚠️ Some raw data files are too large to include in this repo. See [`data/raw/README.md`](data/raw/README.md).

## Large files — download manually before running notebooks

### 1. Participant Data Pack
- **Used by:** `well_data_preprocessing.ipynb`
- **Download:** https://drive.google.com/drive/folders/1fGN5C8G8wzzxA7wULrz1Wn-xCw1eKTku
- Unzip and place files in this folder (`data/raw`)

### 2. Administrative Boundaries (`administrativeunits.gml`)
- **Used by:** `utrecht_boundary_extraction.ipynb`
- **Download:** https://service.pdok.nl/kadaster/brk-administratieve-eenheden/atom/downloads/administrativeunits.zip
- Unzip and place `administrativeunits.gml` in this folder (`data/raw/`)

### 3. ThermoGIS Grids (`.nc` files)
- **Used by:** `utrecht_formation_coverage.ipynb`
- **Download:** https://www.thermogis.nl/sites/default/files/2026-05/for_external_use.zip)
- Navigate to: `ThermoGIS_grids_2_5_1 > 6_Permian > Slochteren Fm & Upper Slochteren Mb (ROSL&ROSLU) > BaseCase`
- Place all `.nc` files in this folder (`data/raw/`)

>
> 📝 Processed data and simulation outputs are not included — run notebooks 01–04 in order to regenerate all files in `data/processed/` and `outputs/`.

### Raw Data (`data/raw/`)

**Well Log & Lithology Data**
| File | Description |
|---|---|
| `BLT-01.las` | Well log — BLT-01 |
| `EVD-01.las` | Well log — EVD-01 |
| `JUT-01.las` | Well log — JUT-01 |
| `PKP-01.las` | Well log — PKP-01 |
| `target_lithologies.csv` | Main dataset (3,455 rows, 13 columns) |
| `Well Path Data.xlsx` | Well path/trajectory data for all 4 wells |

**Administrative Boundaries**
| File | Description |
|---|---|
| `administrativeunits.gml` | Dutch administrative boundaries — download separately (see `data/raw/README.md`) |

**ThermoGIS Grids** — 11 variables × 4 scenarios = 44 `.nc` files — download separately (see `data/raw/README.md`)

| Variable | Description |
|---|---|
| `ROSL_ROSLU_depth` | Formation depth |
| `ROSL_ROSLU_temperature` | Temperature |
| `ROSL_ROSLU_porosity` | Porosity |
| `ROSL_ROSLU_permeability_p50` | Permeability (p50) |
| `ROSL_ROSLU_net_to_gross` | Net-to-gross ratio |
| `ROSL_ROSLU_thickness_p50` | Formation thickness (p50) |
| `ROSL_ROSLU_heat_in_place` | Heat in place |
| `ROSL_ROSLU_potential_recoverable_heat` | Potential recoverable heat |
| `ROSL_ROSLU_economic_potential` | Economic potential |
| `ROSL_ROSLU_flow_rate_p50` | Flow rate (p50) |
| `ROSL_ROSLU_power_p50` | Power (p50) |

Scenarios: `BaseCase` (no suffix), `_HP`, `_STIM`, `_STIM_HP`

### Processed Data (`data/processed/`)

| File | Generated by | Description |
|---|---|---|
| `BLT-01log.csv` | `01_well_data_preprocessing.ipynb` | LAS converted to CSV |
| `EVD-01log.csv` | `01_well_data_preprocessing.ipynb` | LAS converted to CSV |
| `JUT-01log.csv` | `01_well_data_preprocessing.ipynb` | LAS converted to CSV |
| `PKP-01log.csv` | `01_well_data_preprocessing.ipynb` | LAS converted to CSV |
| `target_lithologies_filled.csv` | `01_well_data_preprocessing.ipynb` | Cleaned dataset with imputed values |
| `utrecht_province.shp` (+ sidecar files) | `02_utrecht_boundary_extraction.ipynb` | Utrecht province boundary |
| `utrecht_city.shp` (+ sidecar files) | `02_utrecht_boundary_extraction.ipynb` | Utrecht city boundary |

### Simulation Outputs (`outputs/`)

| File | Scenario | Description |
|---|---|---|
| `baseline_results.nc` | Baseline | Full spatial grid |
| `baseline_viable.csv` | Baseline | Viable doublet locations |
| `hp_results.nc` | Heat Pump | Full spatial grid |
| `hp_viable.csv` | Heat Pump | Viable doublet locations |
| `stim_results.nc` | Stimulation | Full spatial grid |
| `stim_viable.csv` | Stimulation | Viable doublet locations |
| `stim_hp_results.nc` | STIM+HP | Full spatial grid |
| `stim_hp_viable.csv` | STIM+HP | Viable doublet locations |
| `nearby_stim_hp.csv` | STIM+HP | Viable doublet locations close to Utrecht city |
| `power_and_npv_map` | STIM+HP | Top 3 locations map |

---

## Notebooks

Run notebooks in order:

| # | Notebook | Description |
|---|---|---|
| 1 | `01_well_data_preprocessing.ipynb` | Loads LAS files, imputes missing well log values, prepares final dataset |
| 2 | `02_utrecht_boundary_extraction.ipynb` | Extracts Utrecht province and city boundaries from Dutch administrative GML data |
| 3 | `03_utrecht_formation_coverage.ipynb` | Screens ThermoGIS Permian formations for Utrecht spatial coverage |
| 4 | `04_slochteren_aquifer_simulation.ipynb` | Runs ThermoGIS geothermal doublet simulation across all four scenarios |

---

## Methods

### Data Preprocessing
- Loaded well log data from LAS files and converted to CSV format
- Identified and filled missing values in three key columns:
  - **`depth_tvd_m`** — interpolated from well path trajectory data
  - **`bulk_density_gcc`** — predicted using a Random Forest Regressor (MAE: 0.0065 g/cc)
  - **`porosity_pct`** — computed via the Porosity-Density equation for EVD-01; predicted using Random Forest for JUT-01 (MAE: 0.3128%)
- Extracted Utrecht province and city boundaries from Dutch administrative data (`administrativeunits.gml`)
- Screened all Permian ThermoGIS formations for spatial coverage over Utrecht
- Identified Slochteren Fm & Upper Slochteren Mb (ROSL_ROSLU) as the target formation

### Simulation Scenarios
Four doublet scenarios were modelled using `pythermogis`, with results assessed against thermal power targets of **5, 10, and 15 MWth** for Utrecht city:

| Scenario | Description |
|---|---|
| **Baseline** | Standard doublet, no enhancement |
| **Heat Pump (HP)** | Heat pump added to boost thermal output |
| **Stimulation (STIM)** | Well stimulation to improve flow rates |
| **STIM+HP** | Combined stimulation and heat pump — recommended scenario |

### Models Used
- **Random Forest Regressor** (`scikit-learn`) — for imputing missing bulk density and porosity values
- **Porosity-Density Equation** — physics-based formula using Slochteren Sandstone constants

  $$\phi = \frac{\rho_{ma} - \rho_b}{\rho_{ma} - \rho_{fl}} \times 100$$

  Where:
  - $\rho_{ma}$ = 2.65 g/cc (quartz sandstone matrix density)
  - $\rho_{fl}$ = 1.07 g/cc (saline formation brine density)

- **ThermoGIS Doublet Simulation** (`pythermogis`) — geothermal energy potential modelling across Utrecht

---

## Results Summary

| Scenario | Viable Sites | Max Power | Max NPV | ≥5 MWth | ≥10 MWth | ≥15 MWth |
|---|---|---|---|---|---|---|
| Baseline | 4,971 | 6.8 MWth | -3.1 M€ | ✅ | ❌ | ❌ |
| Heat Pump | 4,971 | 7.3 MWth | +5.5 M€ | ✅ | ❌ | ❌ |
| Stimulation | 4,971 | 11.2 MWth | -1.8 M€ | ✅ | ✅ | ❌ |
| **STIM+HP** | **4,971** | **9.4 MWth** | **+10.4 M€** | ✅ | ✅ | ❌ |

### Key Findings
- **STIM+HP is the recommended strategy** — the only scenario almost meeting the 10 MWth target with a positive NPV
- **15 MWth target (10 MWth heating + 5 MWth cooling) requires multi-doublet development** — a single doublet cannot reach this threshold under any scenario tested
- **Proposed well sites KDK-01, KDK-02, KDK-03** fall within the high-performance STIM+HP zone near Utrecht city

### Proposed Development — Two Doublet STIM+HP

| Site | Coordinates (x, y) | Power (MWth) | NPV (M€) | Distance to city |
|---|---|---|---|---|
| KDK-01 | (142000, 459000) | 9.12 | +9.91 | 2.8 km |
| KDK-02 | (138000, 465000) | 9.20 | +9.83 | 4.9 km |
| KDK-03 *(contingency)* | (151000, 455000) | 8.46 | +8.15 | 9.2 km |
| **Combined (KDK-01 + KDK-02)** | — | **18.32 MWth** | — | — |

### Surface Facilities Design — Utrecht Geothermal District System

---

#### Overview

The surface facilities are designed to serve Utrecht's mixed-use urban district with a combined heating and cooling system powered by two STIM+HP geothermal doublets (KDK-01 and KDK-02). The system delivers **≥10 MWth heating** and **≥5 MWth cooling** from a single integrated geothermal loop.

---

#### System Configuration

```
                    SUBSURFACE
            ┌──────────────────────┐
            │  KDK-01 + KDK-02     │
            │  Slochteren Aquifer  │
            │  66°C | 298 m³/h     │
            └────────┬─────────────┘
                     │ Hot brine (66°C)
                     ▼
            ┌─────────────────────┐
            │   Heat Exchanger    │  Separates geothermal brine
            │                     │  from district heating loop
            └────────┬────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
   ┌─────────────┐      ┌──────────────────┐
   │  Heat Pump  │      │ Absorption       │
   │  (STIM+HP)  │      │ Chiller          │
   │  10 MWth    │      │  5 MWth cooling  │
   └──────┬──────┘      └────────┬─────────┘
          │                      │
          ▼                      ▼
   ┌─────────────────────────────────────┐
   │           Buffer Tank               │
   │      Thermal Storage (1–2 MWh)      │
   │    Handles peak demand fluctuations │
   └──────────────┬──────────────────────┘
                  │
                  ▼
   ┌─────────────────────────────────────┐
   │      District Heating & Cooling     │
   │           Network (Utrecht)         │
   │                                     │
   │  🏘 Residential  — comfort heating  │
   │  🏢 Offices      — heating/cooling │
   │  🏛 Public       — schools/hospitals│
   └─────────────────────────────────────┘
                  │
                  ▼
   ┌─────────────────────────────────────┐
   │         Injection Well              │
   │      Return brine at 40°C           │
   └─────────────────────────────────────┘
```

---

#### Component Specifications

#### 1. Heat Exchanger
| Parameter | Value |
|---|---|
| Purpose | Separates geothermal brine from district heating water |
| Type | Plate heat exchanger |
| Capacity | 18.32 MWth (full doublet output) |
| Inlet temp (brine) | 66°C |
| Outlet temp (brine) | 40°C (reinjection) |
| Estimated cost | Included in CAPEX (14.28 M€) |

#### 2. Heat Pump
| Parameter | Value |
|---|---|
| Purpose | Boosts geothermal heat to district heating supply temperature |
| Mode | Heating |
| Output | 10 MWth district heating |
| COP | 5.32 (average KDK-01 + KDK-02) |
| Supply temperature | 70°C |
| Return temperature | 40°C |
| Estimated cost | Included in CAPEX (600 €/kWth) |

#### 3. Absorption Chiller
| Parameter | Value |
|---|---|
| Purpose | Provides district cooling using waste geothermal heat |
| Mode | Cooling |
| Output | 5 MWth cooling |
| Type | Heat-driven (no additional electricity required) |
| Cooling COP | ~0.7 (typical for single-effect absorption chiller) |
| Estimated CAPEX | 1.5–2.0 M€ |
| Note | Not included in LCOE base case — improves economics if added |

#### 4. Buffer Tank
| Parameter | Value |
|---|---|
| Purpose | Thermal storage to handle peak demand fluctuations |
| Capacity | 1–2 MWh |
| Benefit | Allows doublet to run at steady state — maximises efficiency |
| Estimated CAPEX | 0.3–0.5 M€ |

---

### Energy Balance

```
Geothermal input (KDK-01 + KDK-02):   18.32 MWth
        │
        ├── Heating allocation:  10 MWth  → district heating
        ├── Cooling allocation:   5 MWth  → absorption chiller
        └── Buffer / margin:            3.32 MWth → storage / losses
```

---

#### Additional CAPEX Estimate (surface facilities beyond LCOE base case)

| Component | Estimated Cost |
|---|---|
| Absorption chiller (5 MWth) | 1.5–2.0 M€ |
| Buffer tank (1–2 MWh) | 0.3–0.5 M€ |
| Pipework, controls & connection | 0.5 M€ |
| **Total additional CAPEX** | **~2.5–3.0 M€** |

> **Note:** The LCOE of 14.11 €/GJ covers the heat pump and heat exchanger only. The absorption chiller and buffer tank represent additional investment.

---

#### Compliance with Datathon Targets

| Target | Required | Achieved | Facility |
|---|---|---|---|
| Heating demand | ≥ 10 MWth | **10 MWth** ✅ | Heat pump (STIM+HP) |
| Cooling demand | ≥ 5 MWth | **5 MWth** ✅ | Absorption chiller |
| **Combined** | **≥ 15 MWth** | **18.32 MWth** ✅ | Two doublets combined |

### LCOE Analysis

| Parameter | Value |
|---|---|
| Scenarios | 2 × STIM+HP doublets (KDK-01 + KDK-02) |
| Annual heat production | 430,319 GJ/yr |
| Total CAPEX | 14.28 M€ |
| **LCOE** | **14.11 €/GJ (50.8 €/MWh)** |

> See [`reports/lcoe_parameters.md`](reports/lcoe_parameters.md)

### LCOE Parameter Justifications

---

#### Subsurface Parameters

| Parameter | Value | Unit | Justification |
|---|---|---|---|
| Flow rate | 165.59 | L/s | Combined flow rate of two doublets (KDK-01: 296.9 m³/h + KDK-02: 299.2 m³/h = 596.1 m³/h ÷ 3.6 = 165.6 L/s), derived directly from ThermoGIS STIM+HP simulation results |
| Along hole depth | 1,300 | m | Depth to top of Slochteren formation (avg 1,102 m from simulation `welld` field) plus formation penetration (~140 m average thickness) plus 10% directional drilling margin |
| Surface temperature | 10 | °C | Long-term average annual surface temperature for the Netherlands (KNMI reference value) |
| Production temperature | 66.26 | °C | Average production temperature of KDK-01 (66.3°C) and KDK-02 (65.6°C) from ThermoGIS STIM+HP simulation |
| Economic lifetime | 30 | Years | Standard design lifetime for geothermal doublet systems in the Netherlands, consistent with TNO/ThermoGIS guidelines |

---

#### Well & Surface Costs

| Parameter | Value | Unit | Justification |
|---|---|---|---|
| Well cost scaling factor | 1.5 | — | Standard scaling factor for the Netherlands, accounting for local drilling market premiums and mobilisation costs relative to global benchmarks |
| Well costs | 2.247 | M€/well | Calculated using the standard ThermoGIS well cost formula: `1.5 × (0.2 × depth² + 700 × depth + 250,000) × 10⁻⁶` at 1,300 m depth |
| Stimulation cost | 0.5 | M€/well | Representative cost for hydraulic well stimulation in the Slochteren sandstone formation, consistent with Dutch geothermal practice |
| Pump investment | 0.3 | M€/pump | Standard downhole pump installation cost for geothermal wells at this depth and flow rate range |
| Number of wells | 4 | — | Two doublets (KDK-01 and KDK-02), each comprising one production well and one injection well |

---

#### Heat System Parameters

| Parameter | Value | Unit | Justification |
|---|---|---|---|
| Reinjection temperature | 40 | °C | District heating return temperature (`dh_return_temp`) set in ThermoGIS STIM+HP simulation settings, consistent with Dutch district heating network standards |
| Direct heat production | 19.92 | MWth | Auto-calculated by ThermoGIS LCOE model from flow rate, production temperature, and reinjection temperature; includes heat pump contribution (KDK-01: 9.12 MWth + KDK-02: 9.20 MWth = 18.32 MWth geothermal + HP uplift) |
| Load hours | 6,000 | hr/yr | Effective annual operating hours set in ThermoGIS simulation settings; equivalent to ~68% capacity factor, consistent with Dutch district heating demand patterns |
| Direct heat plant investment | 150 | k€/MWth | Standard surface heat installation cost per unit of thermal capacity for geothermal district heating systems in the Netherlands |
| (co) heat relative starting temp | 0.99 | — | Set to maximum (99%) to utilise the full available temperature range from production temperature (66.26°C) down to reinjection temperature (40°C), maximising heat extraction |
| COP (heat pump) | 5.32 | — | Average heat pump coefficient of performance from ThermoGIS simulation: KDK-01 `cophp` = 5.369, KDK-02 `cophp` = 5.274 |
| Pressure of water loop | 6 | bar | Standard operating pressure for a medium-scale Dutch district heating network serving an urban area the size of Utrecht |
| Electricity price (pumps) | 150 | €/MWhe | Conservative industrial electricity price assumption for the Netherlands; actual large-scale geothermal operators may negotiate lower rates (~€100/MWhe) |

---

#### Rock & Fluid Properties

| Parameter | Value | Unit | Justification |
|---|---|---|---|
| Cp water | 4,250 | J/kg·K | Specific heat capacity of saline formation brine, slightly higher than pure water (4,182 J/kg·K) due to dissolved salts in the Slochteren formation |
| ρ water | 1,078 | kg/m³ | Density of saline formation brine typical for the Slochteren aquifer at Utrecht conditions |
| Cp rock | 1,000 | J/kg·K | Specific heat capacity of Slochteren sandstone, consistent with TNO/ThermoGIS default values for this formation |
| ρ rock | 2,700 | kg/m³ | Bulk density of Slochteren sandstone, consistent with TNO/ThermoGIS default values |

---

#### Ultimate Recovery

| Parameter | Value | Unit | Justification |
|---|---|---|---|
| Subsurface area | 10 | km² | Estimated combined drainage area of two doublets. Each doublet drains approximately π × 1,500² ≈ 7 km², with a 0.7 overlap factor applied for the two sites spaced ~6.4 km apart: 2 × 7 × 0.7 ≈ 10 km² |
| Subsurface thickness | 140 | m | Average net formation thickness from ThermoGIS simulation transmissivity data for KDK-01 (~134 m) and KDK-02 (~141 m) |

---

#### Financial Parameters

| Parameter | Value | Unit | Justification |
|---|---|---|---|
| Inflation | 3 | % | Representative of current Dutch inflation environment; consistent with ECB medium-term inflation target and recent Netherlands CPI trends |
| Loan rate | 6.0 | % | Typical interest rate for infrastructure project finance in the Netherlands for geothermal developments at current market conditions |
| Required return on equity | 15 | % | Standard required return for renewable energy infrastructure projects reflecting moderate-to-high subsurface risk profile |
| Equity share | 20 | % | Typical equity contribution for capital-intensive infrastructure projects; the majority of financing is debt-funded |
| Debt share | 80 | % | Follows from 20% equity; standard for geothermal infrastructure projects with long operational lifetimes and stable cash flows |
| Tax rate | 25 | % | Approximation of Dutch corporate income tax rate (25.8% for profits above €200,000) |
| Term loan | 15 | Years | Standard loan term for geothermal infrastructure, covering the initial capital recovery period within the 30-year project lifetime |
| Depreciation period | 15 | Years | Linear depreciation over the loan term, consistent with Dutch fiscal treatment of geothermal assets |
| Fiscal stimulus | None | — | No fiscal stimulus applied in the base case. Note: Dutch SDE++ subsidies for renewable heat, if applied, would further improve project economics |

---

### Result

| Metric | Value | Unit |
|---|---|---|
| **LCOE** | **14.11** | **€/GJ** |
| Equivalent LCOE | 50.8 | €/MWh |
| Annual heat production | 430,319 | GJ/yr |
| Total CAPEX | 14.28 | M€ |

---

## Setup & Usage

### Requirements
- Python 3.11.2

### Installation

1. Clone or download the repository:
```bash
git clone https://github.com/sadaraka-kadi/Team_KDK_Code_V1.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install pythermogis --index-url https://ci.tno.nl/gitlab/api/v4/projects/18271/packages/pypi/simple
```

3. Download large data files — see [`data/raw/README.md`](data/raw/README.md) for instructions

4. Run notebooks in order from the `notebooks/` folder:
```
01_well_data_preprocessing.ipynb
02_utrecht_boundary_extraction.ipynb
03_utrecht_formation_coverage.ipynb
04_slochteren_aquifer_simulation.ipynb
```

> **Note:** Run cells in order within each notebook. Processed files will be automatically saved to `data/processed/` and simulation outputs to `outputs/`.

---

## Dependencies

See [`requirements.txt`](requirements.txt) for the full list. Key libraries:

| Library | Purpose |
|---|---|
| `pandas` | Data manipulation |
| `numpy` | Numerical computing |
| `lasio` | Reading LAS well log files |
| `scikit-learn` | Machine learning (Random Forest) |
| `openpyxl` | Reading Excel well path data |
| `geopandas` | Geospatial data processing |
| `xarray` | Reading NetCDF grid files |
| `matplotlib` | Plotting and figures |
| `pythermogis` | ThermoGIS geothermal simulation |
| `pygridsio` | Reading ThermoGIS grid files |
| `rioxarray` | Raster clipping and CRS handling |
| `shapely` | Geometric operations |

---

## AI Assistance Disclosure

This project used Claude (by Anthropic) as an AI assistant to support code 
development. All simulation results, parameter selections, subsurface interpretations, and conclusions were independently verified and validated by the team. The analysis, findings, and recommendations represent the original work of Team KDK.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
