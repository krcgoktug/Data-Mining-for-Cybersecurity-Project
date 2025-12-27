#  Data Mining for Cybersecurity - Phase 2   

This folder contains the end-to-end implementation for **Phase 2: Data Pre-processing, EDA, and Machine Learning Modeling** using the **CIC-IDS2017** dataset.

---


##  Pipeline Architecture

###  Data Cleaning Stage (`src/cyber_cleaner.py`)
The initial stage focuses on data integrity and standardization:
* **Dataset Ingestion:** Merges daily CSV files (Monday through Friday) to capture comprehensive weekly traffic patterns.
* **Structural Cleaning:** Strips hidden white spaces from column names to prevent indexing errors.
* **Integrity Management:** Detects and removes missing (`NaN`) and infinite (`inf`) values—commonly caused by zero-division in flow calculations—to ensure mathematical stability.
* **Label Encoding:** Categorical attack labels are converted into numerical integers for algorithmic compatibility.
* **Cleaned Data:** https://drive.google.com/file/d/1b-vDPkMnmaVEVoMGjYCrqQdcSeEegC6F/view?usp=sharing

###  Feature Engineering Stage (`src/feature_engineering.py`)
Based on Information Gain analysis, this script refines the dataset for a Random Forest model:
* **Host De-memorization:** Automatically drops identifier columns (`Flow ID`, `Source IP`, `Source Port`, etc.) to ensure the model learns attack patterns rather than specific host addresses.
* **Strategic Selection:** Retains 9 high-impact features selected via **Information Gain analysis (Table B.4)** plus the target `Label`.
* **Statistical Normalization:** Utilizes `StandardScaler` to ensure all features contribute equally to the model, regardless of their original scale (e.g., Duration vs. Packet Length).
* **Optimized Export:** Produces a standardized CSV file ready for the modeling phase.
* **Feature Engineered Data:** https://drive.google.com/file/d/1aiMiYLPZClOwJ13Yw9Hyh1hYHJ9yYado/view?usp=sharing


### Exploratory Data Analysis (`notebooks/01_eda_overview.ipynb`)
Detailed investigation of the dataset's statistical properties:
* **Class Distribution:** Visualizes the extreme imbalance between benign traffic ( > 80%) and various attack types, highlighting the need for specialized evaluation metrics.
* **Feature Distribution:** Histogram analysis for the 9 selected cybersecurity features to understand their statistical range and spread.
* **Correlation Analysis:** Features a heatmap identifying linear relationships between flow metrics to analyze feature dependencies.


###  IDS Model Prototype (`src/train_intrusion_detection.py`)
This module implements a Random Forest classifier for the CIC-IDS2017 dataset to detect network intrusions.
* **Label Grouping:** Aggregated the original 15 labels into 6 broad categories (Benign, DoS, PortScan, Brute Force, Web Attack, Bot) to resolve low-support class issues.
* **Imbalance Handling:** Utilized `class_weight='balanced'` to automatically adjust penalties for minority attack classes.
* **Performance:** Achieved **99% accuracy**, with high recall for volumetric attacks (DoS/PortScan).
* **Limitations:** Lower detection rates for Web Attacks due to the lack of payload content analysis in flow-based features.

---

##  Execution & Usage Guide

####  Prerequisites
Install the required analytical libraries:
```bash
pip install -r requirements.txt
```

###  Running the Pipeline
The scripts must be executed in order to maintain the data flow:

**Step A: Clean the Raw Data**
```bash
python src/cyber_cleaner.py
```
* **Input:** Raw CSV files in the directory.
* **Output:** `clean_cyber_data.csv`

**Step B: Apply Feature Engineering**
```bash
python src/feature_engineering.py --input src/clean_cyber_data.csv --output processed_data.csv
```
* **Arguments:** Use `--input` to specify the cleaned file and `--output` for the final processed path.

**Step C: Exploratory Data Analysis (EDA)**
```bash
jupyter notebook notebooks/01_eda_overview.ipynb
```
* **Action:** Run all cells in the notebook to visualize data distributions and correlations.
* **Input:** \`clean_cyber_data.csv\`
* **Insight:** Confirms class imbalance and justifies the choice of evaluation metrics.


**Step D: Train and Evaluate Model**
```bash
python src/train_intrusion_detection.py
```
* **Input:** \`processed_data.csv\`.
* **Output:** Detailed model performance metrics, including precision/recall for each attack family, can be found in \`report/Training_Outputs.txt\`.

---

##  Repository Structure
* **`src/`**: Contains Python scripts for cleaning and engineering.
* **`notebooks/`**: Contains the **\`01_eda_overview.ipynb\`** notebook.
* **`data/`**: Holds **sample dataset** subsets for input and verification.
* **`report/`**: Contains the final PDF report and static EDA outputs (\`html\`, \`txt\`).
* **\`requirements.txt\`**: Listing of all Python dependencies.
> **Note on EDA Results:** Due to GitHub's private repository policy, the \`EDA_Notebook_Output.html\` cannot be previewed directly. Please **download** it and open it in a web browser.

---

> **Note:** Detailed justifications for pre-processing techniques, exploratory data analysis and select-apply data mining technique are documented in the final PDF report.

---
