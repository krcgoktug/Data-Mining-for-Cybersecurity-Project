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
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    # Load cleaned data
    if not input_path.exists():
        print(f"Error: '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(input_path)

    # Drop identifier columns if present
    columns_to_drop = [col for col in IDENTIFIER_COLUMNS if col in df.columns]
    df = df.drop(columns=columns_to_drop, errors="ignore")

    # Validate required columns exist
    required_columns = set(FEATURE_COLUMNS + [LABEL_COLUMN])
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        missing_list = ", ".join(sorted(missing_columns))
        print(f"Error: Missing required columns: {missing_list}", file=sys.stderr)
        sys.exit(1)

    # Select only the engineered feature set plus the label
    df = df[FEATURE_COLUMNS + [LABEL_COLUMN]]

    # Scale features with StandardScaler (label is excluded)
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[FEATURE_COLUMNS])
    scaled_df = pd.DataFrame(scaled_features, columns=FEATURE_COLUMNS, index=df.index)

    # Combine scaled features with the original label
    processed_df = pd.concat([scaled_df, df[[LABEL_COLUMN]]], axis=1)

    # Save the processed dataset
    if output_path.parent != Path("."):
        output_path.parent.mkdir(parents=True, exist_ok=True)
    processed_df.to_csv(output_path, index=False)
    print(f"Saved processed data to '{output_path}'.")


if __name__ == "__main__":
    main()
