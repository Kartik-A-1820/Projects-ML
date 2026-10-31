# Dataset card — UCI Human Activity Recognition Using Smartphones

**Canonical source:** https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones

**DOI:** 10.24432/C54S4K. Reyes-Ortiz et al., UCI Machine Learning Repository, 2013.

**License:** CC BY 4.0 (attribution required). Original records are not committed. The dataset has 10,299 windows from 30 subjects, 6 classes, 128 samples per window at 50 Hz, 9 inertial channels (body acceleration, body gyroscope, total acceleration, xyz). Subjects are partitioned into 21 training and 9 testing volunteers. The 2.56-second windows overlap by 50%, making row-random splitting invalid.

**Download:** run `python -c "from src.har import download; print(download())"` from project root (internet required). Source archive ~58.2 MB. Alternatively download the archive manually from the UCI page and extract to `data/UCI HAR Dataset/`. The notebook automatically selects real data if this folder exists; otherwise runs a clearly marked synthetic smoke test. To require real data, set `REQUIRE_REAL=True` in the notebook.

**Targets:** 1 WALKING, 2 WALKING_UPSTAIRS, 3 WALKING_DOWNSTAIRS, 4 SITTING, 5 STANDING, 6 LAYING (converted to zero-based). No medical diagnoses or health outcomes are inferred.

**Leakage:** subject ID is used exclusively for splitting/bootstrap, not as a feature. No windows from a held-out subject enter fitting, SSL pretraining, validation, calibration, or tuning. Original test volunteers remain untouched until final evaluation. Features use only data within each window, and no future windows. Overlapping windows within the same subject are correlated; subject-cluster bootstrap reflects this.

**Synthetic fallback:** deterministic, deliberately simplistic six-activity waveforms for verifying execution; NOT a real-world performance benchmark. No synthetic numbers should appear as research claims.
