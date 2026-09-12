# DATASET.md — NASA C-MAPSS

Canonical source: NASA Prognostics Center of Excellence (PCoE) Data Set Repository.

https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/

Dataset entry: **6. Turbofan Engine Degradation Simulation**.

Citation: A. Saxena and K. Goebel (2008), *Turbofan Engine Degradation Simulation Data Set*, NASA Prognostics Data Repository, NASA Ames Research Center.

NASA describes four simulated sets under different operating-condition and fault-mode combinations. Classic files contain engine/unit ID, cycle, 3 operating settings and 21 sensor measurements.

## Download
Download the archive listed by NASA and place `train_FD001.txt` at:

```text
data/raw/train_FD001.txt
```

Do not commit the raw benchmark archive or extracted data.

## Target
Training trajectories run to failure, so row-level training RUL can be computed as `max_cycle_for_engine - current_cycle`; this project optionally caps early-life RUL at 125 cycles.

## Leakage warning
Never randomly split rows: rows from one engine trajectory are strongly dependent. Split by engine/unit.

## Verification note
The automation environment could read NASA metadata but could not download the linked archive directly, so the published notebook was executed end-to-end with its deterministic synthetic fallback. Those metrics are smoke/integration results only, not NASA benchmark scores.
