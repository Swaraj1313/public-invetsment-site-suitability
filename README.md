# fstp-site-suitability-
This project develops a constraint-based geospatial model to identify feasible sites for Faecal Sludge Treatment Plants (FSTPs) under regulatory and operational constraints in rural districts to support poblic investment decisions.

## Overview

This project develops a **constraint-based site suitability model** for identifying feasible locations for Faecal Sludge Treatment Plants (FSTPs) in resource-constrained districts.

Rather than a conventional GIS mapping exercise, the model operationalizes regulatory norms into a spatial decision-support system, enabling evidence-based infrastructure planning.

The analysis highlights trade-offs between regulatory compliance and practical feasibility in siting decentralized sanitation infrastructure.

## What This Project Demonstrates

- Translation of regulatory norms into a spatial decision system  
- Integration of environmental, social, and logistical constraints  
- Identification of feasible infrastructure sites under real-world constraints  
- Trade-offs between compliance requirements and land availability  

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
