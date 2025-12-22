
import pandas as pd
import numpy as np
import glob
from sklearn.preprocessing import LabelEncoder

# --- STEP 1: DATA INGESTION AND MERGING ---
# Searching for all CSV files (Monday to Friday) in the folder and merging them into one table.
print("Merging datasets, please wait...")
all_files = glob.glob("*.csv")
li = []

for filename in all_files:
    # Using 'cp1252' encoding to prevent character errors during data ingestion.
    df_temp = pd.read_csv(filename, index_col=None, header=0, encoding='cp1252')
    li.append(df_temp)

# Combining all separate files into a single master dataframe.
df = pd.concat(li, axis=0, ignore_index=True)
print(f"Total {len(df)} rows of raw data loaded successfully.")

# --- STEP 2: DATA CLEANING AND STANDARDIZATION ---
# Stripping hidden white spaces from column names to prevent KeyError.
df.columns = df.columns.str.strip()

# Dropping missing (NaN) values to maintain data integrity.
df.dropna(inplace=True)

# Replacing 'Infinite' (inf) values often found in cybersecurity logs with NaN and removing them.
# This step is critical to prevent the machine learning model from crashing.
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

print("Data cleaning completed: Missing and infinite values have been removed.")

# --- STEP 3: CATEGORICAL TO NUMERICAL TRANSFORMATION ---
# Transforming text labels (e.g., 'DDoS', 'Benign') into numerical values using LabelEncoder.
le = LabelEncoder()
df['Label'] = le.fit_transform(df['Label'])

print("Feature encoding completed successfully!")
print("Encoded Label Mapping:")
print(dict(zip(le.classes_, le.transform(le.classes_))))

# --- STEP 4: FINAL DATA EXPORT ---
# Saving the cleaned and processed dataset as 'clean_cyber_data.csv' for the next phase.
print("Preparing the finalized file...")
df.to_csv('clean_cyber_data.csv', index=False)

print("SUCCESS: File saved as 'clean_cyber_data.csv'.")
print("You can now find the processed dataset in your project folder.")

