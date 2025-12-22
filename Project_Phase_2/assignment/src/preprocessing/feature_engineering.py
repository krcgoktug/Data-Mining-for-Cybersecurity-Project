"""
Feature engineering pipeline for CIC-IDS2017 cleaned data.

Pipeline summary:
1) Load the cleaned CSV produced by the data cleaning step.
2) Remove identifier columns to reduce leakage/host memorization.
3) Keep the Information Gain-selected features plus the label.
4) Standardize features with StandardScaler (label is untouched).
5) Save the processed CSV for downstream modeling.
"""

import argparse
import sys
from pathlib import Path

import pandas as pd
from sklearn.preprocessing import StandardScaler


# Identifier columns to drop to prevent host memorization
IDENTIFIER_COLUMNS = [
    "Flow ID",
    "Source IP",
    "Source Port",
    "Destination IP",
    "Destination Port",
    "Timestamp",
]

# Selected features from Information Gain analysis
FEATURE_COLUMNS = [
    "Packet Length Std",
    "Total Length of Bwd Packets",
    "Subflow Bwd Bytes",
    "Init_Win_bytes_forward",
    "Total Length of Fwd Packets",
    "Packet Length Variance",
    "Flow Duration",
    "Bwd Packet Length Max",
    "Bwd Packet Length Mean",
]

LABEL_COLUMN = "Label"


def parse_args() -> argparse.Namespace:
    # CLI args allow running on sample data or full cleaned data without code edits.
    parser = argparse.ArgumentParser(
        description="Feature engineering for CIC-IDS2017 cleaned data."
    )
    parser.add_argument(
        "--input",
        "-i",
        default="clean_cyber_data.csv",
        help="Path to cleaned CSV (default: cleaned_data.csv).",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="processed_data.csv",
        help="Path to write processed CSV (default: processed_data.csv).",
    )
    return parser.parse_args()


def main() -> None:
    # Parse CLI arguments first so paths are configurable from the terminal.
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    # Load cleaned data and fail fast if the input path is invalid.
    if not input_path.exists():
        print(f"Error: '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(input_path)

    # Drop identifier columns to avoid leaking host-specific information.
    # errors="ignore" keeps the script robust if some columns are missing.
    columns_to_drop = [col for col in IDENTIFIER_COLUMNS if col in df.columns]
    df = df.drop(columns=columns_to_drop, errors="ignore")

    # Validate the Information Gain-selected features and Label are present.
    # This prevents silent failures or accidental column mismatches.
    required_columns = set(FEATURE_COLUMNS + [LABEL_COLUMN])
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        missing_list = ", ".join(sorted(missing_columns))
        print(f"Error: Missing required columns: {missing_list}", file=sys.stderr)
        sys.exit(1)

    # Keep only the selected features (ordered) plus the Label column.
    df = df[FEATURE_COLUMNS + [LABEL_COLUMN]]

    # Standardize numeric features to zero mean and unit variance.
    # The Label column is excluded to preserve class targets.
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[FEATURE_COLUMNS])
    scaled_df = pd.DataFrame(scaled_features, columns=FEATURE_COLUMNS, index=df.index)

    # Re-attach the Label column so downstream models can train on it directly.
    processed_df = pd.concat([scaled_df, df[[LABEL_COLUMN]]], axis=1)

    # Save the processed dataset; create the output folder if needed.
    if output_path.parent != Path("."):
        output_path.parent.mkdir(parents=True, exist_ok=True)
    processed_df.to_csv(output_path, index=False)
    print(f"Saved processed data to '{output_path}'.")


if __name__ == "__main__":
    main()
