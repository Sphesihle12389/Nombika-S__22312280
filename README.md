# TLPR200
## A Machine Learning Solution for Identifying Women-Safety Hotspots and Patterns in Ekurhuleni

* **Student Surname & Initials:** Nombika, S.
* **Student Number:** `22312280`

---

### Repository Contents
* `S_Nombika_22312280.ipynb` — Complete Jupyter Notebook containing data acquisition, quality checks, spatial projection (`EPSG:32735`), OpenStreetMap (`OSMnx`) feature extraction, Exploratory Data Analysis (EDA), Random Forest hotspot classification, PCA + K-Means pattern discovery, 3-hotspot deep comparison (*Tembisa, Katlehong, Kempton Park*), complexity analysis, and AI prompts log.
* `app.py` — Interactive Streamlit dashboard presenting spatial choropleth maps, dynamic filters (precinct, crime category, and quarterly time period), EDA & seasonal visualisations, Random Forest confusion matrices & ROC curves, 3-area comparison, and prevention insights.
* `ekurhuleni_station_summary.csv`, `ekurhuleni_quarterly_long.csv`, `ekurhuleni_precincts.geojson`, `model_evaluation.json` — Cleaned datasets and model evaluation artifacts exported by the notebook and consumed by `app.py`.
* `station_boundaries/` — Official SAPS Police Station Boundaries GIS shapefile (`Police_bounds.shp`, `.dbf`, `.prj`, `.shx`).
* `2025-2026_-_1st_Quarter_WEB.xlsx` to `4th_Quarter_WEB.xlsx` & `2026-2027_-_1st_Quarter_WEB.xlsm` — Official SAPS quarterly crime statistics workbooks covering 21 quarters (`April 2021 – June 2026`).
* `requirements.txt` — Python package dependencies.

---

### Data Sources
1. **South African Police Service (SAPS) Quarterly Crime Statistics:** [https://www.saps.gov.za/services/crimestats.php](https://www.saps.gov.za/services/crimestats.php)
2. **South African Police Service (SAPS) Station Boundary GIS Shapefiles:** [https://www.saps.gov.za/services/boundary.php](https://www.saps.gov.za/services/boundary.php)
3. **OpenStreetMap (OSM) Transport & Infrastructure Data (`OSMnx`):** [https://www.openstreetmap.org](https://www.openstreetmap.org)

---

### Running Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
