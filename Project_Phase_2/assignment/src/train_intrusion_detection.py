import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay


# 1. Loading Data and Defining Features
df = pd.read_csv('processed_data.csv')


selected_features = [
    'Packet Length Std', 'Total Length of Bwd Packets', 'Subflow Bwd Bytes',
    'Init_Win_bytes_forward', 'Total Length of Fwd Packets',
    'Packet Length Variance', 'Flow Duration',
    'Bwd Packet Length Max', 'Bwd Packet Length Mean'
]


# 2. Grouping Labels for Better Training
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
# Applying the function
df['New_Label'] = df['Label'].apply(group_labels)

# Dropping the rows that returned -1 (Heartbleed/Infiltration)
df = df[df['New_Label'] != -1]

# Define X and y using the NEW label
X = df[selected_features]
y = df['New_Label']


class_names = ['Benign', 'DoS', 'PortScan', 'Brute Force', 'Web Attack', 'Bot']


# 3. TRAINING
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Training Random Forest on Grouped Data...")
rf_model = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)


# 4. EVALUATION
y_pred = rf_model.predict(X_test)

print("\n--- Evaluation Results (Grouped) ---")
print(classification_report(y_test, y_pred, target_names=class_names))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)

fig, ax = plt.subplots(figsize=(10, 8))
disp.plot(cmap='Blues', ax=ax)
plt.title('Confusion Matrix (Reduced to 6 Classes)')
plt.show()