import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay


# 1. Loading Data and Defining Features

# Load the pre-processed CSV file into a pandas DataFrame.
df = pd.read_csv('processed_data.csv')

# Define the list of feature columns to use for training.
# These specific features focus on statistical properties of the traffic flow:
selected_features = [
    'Packet Length Std', # Standard deviation of packet lengths
    'Total Length of Bwd Packets', # Total size of packets sent by the server/destination
    'Subflow Bwd Bytes', # Bytes in the backward direction for the subflow
    'Init_Win_bytes_forward', # TCP Window size
    'Total Length of Fwd Packets', # Total size of packets sent by the attacker/source
    'Packet Length Variance', # Variance of packet size
    'Flow Duration', # How long the connection lasted
    'Bwd Packet Length Max', # Largest packet sent backward
    'Bwd Packet Length Mean' # Average packet size sent backward
]


# Define a helper function to reduce the number of target classes.
# Some classes are very similar (e.g., DoS Hulk vs DoS GoldenEye), so we group them
# to make the model more robust and easier to interpret.
def group_labels(label):
    # Mapping 0-14 to New Groups
    if label == 0:
        return 0 # Benign
    elif label in [2, 3, 4, 5, 6]:
        return 1 # DoS (Grouped)
    elif label == 10:
        return 2 # PortScan
    elif label in [7, 11]:
        return 3 # Brute Force (FTP/SSH)
    elif label in [12, 13, 14]:
        return 4 # Web Attack (Grouped)
    elif label == 1:
        return 5 # Bot
    else:
        return -1 # Drop (Heartbleed/Infiltration)

print("Grouping labels...")
# Apply the grouping logic to the original 'Label' column to create 'New_Label'
df['New_Label'] = df['Label'].apply(group_labels)

# Filter the DataFrame:
# We remove rows where New_Label is -1. This cleans the dataset of
# rare attack types that we chose not to classify.
df = df[df['New_Label'] != -1]

# Define X and y using the NEW label
X = df[selected_features]
y = df['New_Label']

# Define human-readable names corresponding to 0, 1, 2, 3, 4, 5 for plotting later.
class_names = ['Benign', 'DoS', 'PortScan', 'Brute Force', 'Web Attack', 'Bot']


# Split data into Training and Testing sets.
# test_size=0.2: 80% of data for training, 20% for testing.
# random_state=42: Ensures the split is reproducible (same rows every time you run it).
# stratify=y: important for Intrusion Detection.
# It ensures that the proportion of attacks (e.g., 1% Botnets) is preserved
# in both the training set and the test set. Without this, the test set might
# miss a rare attack entirely.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Training Random Forest on Grouped Data...")

# Initialize the Random Forest Classifier
rf_model = RandomForestClassifier(  
    n_estimators=100, # Create 100 decision trees (standard starting point)
    class_weight='balanced', # Adjusts weights inversely proportional to class frequencies.
                             # This helps the model pay more attention to rare attacks (like Web Attacks)
                             # and not just bias towards 'Benign' traffic which is usually the majority.
    random_state=42,         # Ensures reproducible results
    n_jobs=-1                # Uses all available CPU cores for faster training
)
rf_model.fit(X_train, y_train)


# Use the trained model to predict labels for the unseen test set
y_pred = rf_model.predict(X_test)

print("\n--- Evaluation Results (Grouped) ---")

# Classification Report:
# Shows Precision (accuracy of positive predictions), Recall (sensitivity), and F1-Score.
# We use target_names so the report shows 'DoS', 'Benign' etc., instead of 0, 1.
print(classification_report(y_test, y_pred, target_names=class_names))

# Plotting the confusion matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)

fig, ax = plt.subplots(figsize=(10, 8))
disp.plot(cmap='Blues', ax=ax)
plt.title('Confusion Matrix (Reduced to 6 Classes)')

# Display the plot window
plt.show()
