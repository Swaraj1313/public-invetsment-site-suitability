# 🗺️ FSTP Site Feasibility Analysis — Tikamgarh District, Madhya Pradesh

> **Automated geospatial siting of Fecal Sludge Treatment Plants using open-source GIS, OpenStreetMap data, and multi-criteria spatial exclusion modelling.**

---

## Overview

This work implements a **reproducible, open-data geospatial pipeline** for identifying technically feasible land parcels suitable for Fecal Sludge Treatment Plant (FSTP) construction — with Tikamgarh district, Madhya Pradesh as the study area. Rather than treating site selection as a simple land availability problem, the pipeline operationalises a multiple layered constraint model — systematically screening candidate land against regulatory and environmental thresholds: proximity to water bodies, separation from human settlements, and accessibility via the road network. Each layer reflects a real-world institutional or operational requirement that any public infrastructure investment must satisfy. The framework is district-agnostic and generalises beyond FSTP siting to any context where infrastructure placement must navigate overlapping land-use constraints.

### scroll down for images.

The methodology mirrors the spatial siting criteria used in sanitation infrastructure planning under urban WASH programmes (as referenced in World Bank, and CPHEEO guidelines), and is fully automatable across any Indian district boundary available on OpenStreetMap.

Using open access gepspatial data, this pipeline pulls **live, queryable OSM data** — road networks, water features, and built-up areas — and applies a **multi-layer exclusion model** to systematically rule out unsuitable land for criterion like distance from water bodies and habitation before finalising shortlisted candidate sites.

---

## Methodology

The pipeline follows a structured **negative constraint → residual suitability** approach, which is the standard framework used in land suitability analysis for sanitation infrastructure.

### Step 1 — Study Area Delineation
The administrative boundary of Tikamgarh district is fetched directly from the OSM Nominatim API via `osmnx.geocode_to_gdf()` and reprojected to EPSG:3857 (Web Mercator) for all metric calculations. The full road network is simultaneously downloaded and stored as a graph object for later proximity analysis.

### Step 2 — Water Body Extraction & Buffer Exclusion
All hydrological features — rivers, streams, ponds, lakes, and tanks — are extracted using OSM tags `waterway: True` and `natural: water`. A **200-metre setback buffer** is applied in projected CRS to create the primary exclusion zone. This prevents siting on flood-prone or ecologically sensitive land, and complies with standard separation distances from surface water sources.

### Step 3 — Settlement Extraction & Habitation Buffer Exclusion  
Residential land use polygons and individual building footprints are fetched using `landuse: residential` and `building: True` tags. A **400-metre buffer** is applied around all populated structures to account for odour dispersion, public health separation requirements, and social acceptability considerations — a threshold consistent with FSTP siting norms under India's FSSM (Faecal Sludge and Septage Management) Policy.

### Step 4 — Composite Exclusion Zone Construction
Water and settlement buffers are unioned and dissolved into a single continuous exclusion geometry using `GeoSeries.unary_union`. This ensures overlapping buffers are collapsed cleanly and the subsequent subtraction operation is topologically valid.

### Step 5 — Residual Suitable Land Identification
A geometric difference operation subtracts the composite exclusion zone from the district boundary polygon. The resulting geometry represents land that is — at minimum — free from the primary environmental and social constraints. This is the **base layer for candidate site generation**.

### Step 6 — Parcel Disaggregation & Minimum Area Filter
The residual suitable land geometry is exploded into constituent polygon parts using `GeoDataFrame.explode()`, producing discrete potential parcels. Each parcel is then filtered by computed area (sq. metres), retaining only those **exceeding 2,500 m²** — the minimum operational footprint considered viable for a functional FSTP serving a small urban area.

### Step 7 — Road Proximity Filter (Accessibility Constraint)
The full road network edge layer is unioned into a single geometry and Euclidean distance is computed from each candidate site's centroid to the nearest road. Only sites falling within **1,200 metres of a drivable road** are retained. This constraint ensures operational viability — desludging trucks and transport vehicles must be able to reach the plant without requiring significant new road infrastructure investment.

### Step 8 — Final Site Mapping & Cartographic Output
Shortlisted sites are reprojected to WGS84 (EPSG:4326) for cartographic display. A final annotated map is produced showing candidate sites against the district boundary, with numbered leader-line labels (`Site 1`, `Site 2`, ...) to enable unambiguous field identification.

### Step 9 — Coordinate Table & GeoJSON Export
Site centroids are extracted in WGS84 and tabulated as a clean `site_id / latitude / longitude` reference table. The full site polygon layer is exported as a **GeoJSON file** (`fstp_sites.geojson`) for downstream use in QGIS, ArcGIS, Google Earth Engine, or integration into project reports.

---

## Tech Stack

| Library | Purpose |
|---|---|
| `osmnx` | OSM data extraction — road networks, district boundaries, land use & water features |
| `geopandas` | Spatial dataframe operations — projections, buffers, dissolves, spatial joins |
| `shapely` | Geometric operations — union, difference, centroid extraction |
| `matplotlib` | Cartographic output and map figure generation |

All data sourced exclusively from **OpenStreetMap** — no proprietary datasets, no licensing constraints, fully replicable.

---

## Outputs

| File | Description |
|---|---|
| `outputs/road_network.png` | District road network graph |
| `outputs/district_boundary.png` | District boundary overlay on road network |
| `outputs/water_bodies.png` | Extracted water features |
| `outputs/water_buffer.png` | 200m exclusion buffer around water |
| `outputs/settlement_buffer.png` | 400m exclusion buffer around built-up areas |
| `outputs/combined_exclusion.png` | Composite no-go zone |
| `outputs/suitable_land.png` | Residual land after exclusion |
| `outputs/candidate_sites_raw.png` | Sites passing area threshold |
| `outputs/final_sites_filtered.png` | Sites passing road proximity filter |
| `outputs/final_fstp_sites_map.png` | Final annotated candidate site map |
| `outputs/fstp_sites.geojson` | GeoJSON export of all candidate sites |

---

## Replicability

The pipeline is district-agnostic. To run for any other district, change the `place_name` string in Cell 2:

```python
place_name = "Tikamgarh, Madhya Pradesh, India"
```

Any district with OSM coverage will work. Buffer distances and area thresholds can be adjusted in Cells 7, 8, 11, and 13 to match local FSTP design standards.

---

## Analytical Workflow and Outputs

| Step | Output | Purpose |
|------|--------|--------|
| Road Network Extraction | ![](outputs/Cell_3_road_network.png) | Captures transport infrastructure used to assess accessibility of candidate sites |
| District Boundary Validation | ![](outputs/Cell_4_district_boundary.png) | Ensures all analysis is spatially aligned with administrative boundaries |
| Water Bodies Mapping | ![](outputs/Cell_6_water_bodies.png) | Identifies environmentally sensitive zones |
| Water Buffer (400m) | ![](outputs/Cell_7_water_buffer.png) | Applies environmental regulatory exclusion |
| Settlement Buffer (400m) | ![](outputs/Cell_8_settlement_buffer.png) | Ensures social acceptability and avoids habitation proximity |
| Combined Exclusion Zone | ![](outputs/Cell_9_combined_exclusion.png) | Aggregates all regulatory constraints into a unified exclusion layer |
| Suitable Land | ![](outputs/Cell_10_suitable_land.png) | Identifies feasible land after applying all constraints |
| Candidate Parcels | ![](outputs/Cell_11_candidate_sites_raw.png) | Segments feasible land into discrete parcels |
| Road Overlay | ![](outputs/Cell_12_sites_with_roads_overlay.png) | Evaluates proximity of sites to transport network |
| Filtered Sites | ![](outputs/Cell_13_final_sites_filtered.png) | Applies accessibility constraint (≤1200m from roads) |
| Final Candidate Sites | ![](outputs/Cell_14_final_fstp_sites.png) | Final recommended locations for FSTP development |


### Geospatial Output
- `fstp_sites.geojson` → Can be opened in QGIS / GIS tools

### Coordinates
- CSV file containing site-wise latitude and longitude for validation in Google Maps

- ## Project Workflow (Step-by-Step Outputs)

### Road Network
![Road Network](outputs/Cell_3_road_network.png)

### District Boundaries
![District Boundary](outputs/Cell_4_district_boundary.png)

### Water Bodies
![Water Bodies](outputs/Cell_6_water_bodies.png)

### Water Buffer
![Water Buffer](outputs/Cell_7_water_buffer.png)

### Settlement Buffer
![Settlement Buffer](outputs/Cell_8_settlement_buffer.png)

### Combined Exclusion Zones
![Exclusion](outputs/Cell_9_combined_exclusion.png)

### Suitable Land
![Suitable Land](outputs/Cell_10_suitable_land.png)

### Candidate Sites (Raw)
![Candidate Sites](outputs/Cell_11_candidate_sites_raw.png)

### Sites with Road Overlay
![Sites Roads](outputs/Cell_12_sites_with_roads_overlay.png)

### Filtered Sites
![Filtered Sites](outputs/Cell_13_final_sites_filtered.png)

### Final FSTP Sites
![Final Sites](outputs/Cell_14_final_fstp_sites.png)
