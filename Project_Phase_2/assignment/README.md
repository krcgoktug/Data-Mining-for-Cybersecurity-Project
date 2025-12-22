# Phase 2: Data Mining for Cybersecurity Project

## Feature Engineering (CIC-IDS2017)
This script prepares cleaned CIC-IDS2017 data for a Random Forest model:
- drops identifier columns to prevent host memorization
- keeps Information Gain-selected features (Table B.4) plus `Label`
- standardizes features with `StandardScaler`
- writes a processed CSV for modeling

### Run
From `Project_Phase_2/assignment`:
```bash
python src/feature_engineering.py --input data/sample_data.csv --output processed_data.csv
```

Notes:
- The `data/` folder contains sample data for input only. Do not modify it.
- Use `--input` and `--output` to point to your cleaned CSV and desired output path.
