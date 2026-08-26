# probable-eureka
**Geothermal Energy Assessment & Site Screening — Utrecht, Netherlands**

This repository contains Kadi Sadaraka's independent refinement and further development of Team KDK's submission for the SPE Africa Datathon 2026, analysing geothermal energy data from Utrecht, Netherlands.

The work builds upon the team's original submission while extending and refining selected aspects of the analysis, modelling, and interpretation.

Original team submission: Team KDK

---

## Project Overview

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
| 1 | `01_data_exploration.ipynb` | Loads LAS files, imputes missing well log values, prepares final dataset |

---

## Setup & Usage

### Requirements
- Python 3.11.2

### Installation

1. Clone or download the repository:
```bash
git clone 
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
## Acknowledgements / Technical recommendations

- Dr. Daniel Wamriew
- Elias Drescher

## AI Assistance Disclosure

This project used Claude (by Anthropic) as an AI assistant to support code 
development. All simulation results, parameter selections, subsurface interpretations, and conclusions were independently verified and validated by the team. The analysis, findings, and recommendations represent the original work of Team KDK.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
