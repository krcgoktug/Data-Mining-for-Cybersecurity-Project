import pandas as pd
from sklearn.model_selection import train_test_split
import time

# ==============================================================================
# SCRIPT: Stratified Raw Data Sampler
# PURPOSE: Generating a representative subset (sample_data.csv) from the raw 
#          Wednesday dataset while maintaining the original class distribution.
# ==============================================================================

start_time = time.time()

# 1. LOADING THE RAW DATASET
# ------------------------------------------------------------------------------
# We use the 'Wednesday-workingHours.pcap_ISCX.csv' as it contains a rich 
# variety of attack vectors including DoS (Hulk, GoldenEye, Slowloris) and 
# Heartbleed. This ensures the sample is representative of complex attack patterns.
# ------------------------------------------------------------------------------
print("[1/5] Loading raw Wednesday dataset... Please wait, do not close the terminal.")
raw_data_path = 'Wednesday-workingHours.pcap_ISCX.csv' 

# Using 'low_memory=False' to handle mixed types in large network logs
df = pd.read_csv(raw_data_path, low_memory=False)
print(f"--- Data loaded successfully in {round(time.time() - start_time, 2)} seconds.")

# 2. STRUCTURAL CLEANING
# ------------------------------------------------------------------------------
# Raw CIC-IDS2017 files often contain leading/trailing white spaces in column 
# names (e.g., ' Label' instead of 'Label'). We must strip these spaces to 
# ensure programmatic access to the target column for stratified sampling.
# ------------------------------------------------------------------------------
print("[2/5] Cleaning column headers...")
df.columns = df.columns.str.strip()

# 3. PREPARING FOR STRATIFICATION
# ------------------------------------------------------------------------------
# Stratified sampling requires a valid label for every row. We drop rows where 
# the 'Label' is missing (NaN) to prevent the sampling algorithm from failing.
# ------------------------------------------------------------------------------
print("[3/5] Checking for data integrity...")
df = df.dropna(subset=['Label'])

# 4. STRATIFIED SAMPLING
# ------------------------------------------------------------------------------
# RATIONALE: A simple random sample might miss rare attack classes (like Heartbleed).
# By using 'Stratified Sampling', we ensure that the 'sample_data.csv' maintains 
# the EXACT same percentage of Benign vs. Malicious traffic as the original source.
#
# SAMPLE SIZE: 20,000 rows is chosen as it is large enough to capture rare 
# attacks but small enough for quick processing during the pipeline verification.
# ------------------------------------------------------------------------------
print("[4/5] Executing Stratified Sampling (Preserving attack distributions)...")
_, sample_df = train_test_split(
    df, 
    test_size=20000, 
    stratify=df['Label'], 
    random_state=42
)

# 5. WRITING TO DISK
# ------------------------------------------------------------------------------
# The resulting CSV is the RAW starting point for the project pipeline.
# It includes the original noise (Inf, NaN, spaces) to test the robustness 
# of our cleaning.py script.
# ------------------------------------------------------------------------------
print("[5/5] Saving 'sample_data.csv' to disk...")
output_path = 'sample_data.csv'
sample_df.to_csv(output_path, index=False)

end_time = time.time()
print(f"\n✅ SUCCESS: Process completed in {round(end_time - start_time, 2)} seconds.")

# 6. VERIFICATION REPORT
# ------------------------------------------------------------------------------
# Visualizing the final distribution to confirm that multiple attack categories 
# are present in the sample.
# ------------------------------------------------------------------------------
print("\n--- Final Sample Distribution Summary ---")
print(sample_df['Label'].value_counts(normalize=True) * 100)