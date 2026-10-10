# Dataset card — UCI Beijing Multi-Site Air Quality

**Canonical source:** https://archive.ics.uci.edu/dataset/501/beijingmultisiteairqualitydata
**DOI:** https://doi.org/10.24432/C5RK5G
**Official download:** https://archive.ics.uci.edu/static/public/501/beijing+multi+site+air+quality+data.zip
**Creator:** Song Chen; original measurements from Beijing Municipal Environmental Monitoring Center; meteorology matched from China Meteorological Administration.
**License:** Creative Commons Attribution 4.0 (CC BY 4.0); attribution required.
**Coverage:** 12 sites, hourly March 2013–February 2017; 420,768 observations. PM2.5, PM10, SO2, NO2, CO, O3, TEMP, PRES, DEWP, RAIN, wind speed/direction. NA values present.

## Download
1. Visit the UCI page and download the 7.8 MB archive.
2. Unzip it; if there is a nested `PRSA2017_Data_20130301-20170228.zip`, extract that too.
3. Put all twelve `PRSA_Data_*.csv` files under `dataset/raw/` (nested subfolders also supported).
4. Execute the notebook from the repository root or notebooks folder. The loader searches recursively.

## Target / forecast contract
At forecast origin `t`, predict station PM2.5 at `t+24 hours`. Only current/historical measured pollution/weather are used. This is not a weather-forecast product and not a clinical decision system. A future observation may not be used as a predictor. Reindex to hourly timestamps before shifting target.

## Limitations
Sensor missingness may be informative. No traffic, satellite or true future meteorological forecasts are included. Two held-out stations have their own past sensor telemetry available; this is not cold-start without sensors. Observational historical data does not establish causal effect of interventions. No raw UCI files are committed even though license allows redistribution.

## Synthetic fallback
If raw CSV files are missing, the notebook generates seeded simulated pollution and weather for six synthetic stations across two years. Synthetic benchmark scores are only a pipeline smoke test, not estimates of real Beijing performance.