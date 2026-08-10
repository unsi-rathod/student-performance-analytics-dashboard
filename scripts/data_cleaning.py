"""
==========================================================
Student Performance Analytics Dashboard
Phase 2 - Data Cleaning

Author : Unsi Rathod
Project: Student Performance Analytics Dashboard

Description:
Reads the raw student performance dataset, validates data,
standardizes text formatting, recalculates derived columns,
and exports a cleaned dataset without modifying the original.

==========================================================
"""

from pathlib import Path
import pandas as pd
import logging

# ---------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

# ---------------------------------------------------------
# Project Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "Data"
    / "Raw_Data"
    / "SECTION_WISE_STUDENT_PERFORMANCE_FINAL_150.csv"
)

OUTPUT_FOLDER = (
    PROJECT_ROOT
    / "Data"
    / "Cleaned_Data"
)

OUTPUT_FILE = (
    OUTPUT_FOLDER
    / "student_performance_cleaned.csv"
)

# ---------------------------------------------------------
# Required Columns
# ---------------------------------------------------------

REQUIRED_COLUMNS = [
    "SECTION",
    "NAME",
    "HY_Q1",
    "HY_Q2",
    "HY_Q3",
    "HY_Q4",
    "HY_Q5",
    "HY",
    "PASS_FAIL_HY",
    "HY_GRADE",
    "Y_Q1",
    "Y_Q2",
    "Y_Q3",
    "Y_Q4",
    "Y_Q5",
    "Y",
    "PASS_FAIL_ANNUAL",
    "Y_GRADE",
    "Y_GRADE_ORIGINAL",
    "IMPROVEMENT",
    "PERFORMANCE SEGMENT"
]

TEXT_COLUMNS = [
    "SECTION",
    "NAME",
    "PASS_FAIL_HY",
    "HY_GRADE",
    "PASS_FAIL_ANNUAL",
    "Y_GRADE",
    "Y_GRADE_ORIGINAL",
    "PERFORMANCE SEGMENT"
]

MARK_COLUMNS = [
    "HY_Q1",
    "HY_Q2",
    "HY_Q3",
    "HY_Q4",
    "HY_Q5",
    "Y_Q1",
    "Y_Q2",
    "Y_Q3",
    "Y_Q4",
    "Y_Q5"
]

# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

def load_dataset():

    logging.info("Reading raw dataset...")

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Raw dataset not found:\n{RAW_DATA_PATH}"
        )

    return pd.read_csv(RAW_DATA_PATH)

# ---------------------------------------------------------
# Validate Columns
# ---------------------------------------------------------

def validate_columns(df):

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns:\n{missing}"
        )

    logging.info("Dataset structure validated.")

# ---------------------------------------------------------
# Clean Text Columns
# ---------------------------------------------------------

def clean_text_columns(df):

    logging.info("Cleaning text columns...")

    for column in TEXT_COLUMNS:

        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )

    return df

# ---------------------------------------------------------
# Convert Numeric Columns
# ---------------------------------------------------------

def convert_numeric_columns(df):

    logging.info("Validating numeric columns...")

    numeric_columns = MARK_COLUMNS + [
        "HY",
        "Y",
        "IMPROVEMENT"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="raise"
        )

    return df

# ---------------------------------------------------------
# Recalculate Totals
# ---------------------------------------------------------

def recalculate_totals(df):

    logging.info("Recalculating totals...")

    df["HY"] = (
        df[
            [
                "HY_Q1",
                "HY_Q2",
                "HY_Q3",
                "HY_Q4",
                "HY_Q5"
            ]
        ]
        .sum(axis=1)
    )

    df["Y"] = (
        df[
            [
                "Y_Q1",
                "Y_Q2",
                "Y_Q3",
                "Y_Q4",
                "Y_Q5"
            ]
        ]
        .sum(axis=1)
    )

    return df

# ---------------------------------------------------------
# Recalculate Improvement
# ---------------------------------------------------------

def recalculate_improvement(df):

    logging.info("Updating improvement values...")

    df["IMPROVEMENT"] = (
        df["Y"] - df["HY"]
    )

    return df

# ---------------------------------------------------------
# Remove Duplicates
# ---------------------------------------------------------

def remove_duplicates(df):

    before = len(df)

    df = df.drop_duplicates()

    removed = before - len(df)

    logging.info(
        f"Duplicate rows removed: {removed}"
    )

    return df

# ---------------------------------------------------------
# Save Dataset
# ---------------------------------------------------------

def save_dataset(df):

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    logging.info(
        f"Cleaned dataset saved to:\n{OUTPUT_FILE}"
    )

# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

def print_summary(df):

    print("\n" + "=" * 55)
    print("STUDENT PERFORMANCE DATA CLEANING COMPLETED")
    print("=" * 55)

    print(f"Rows Processed : {len(df)}")
    print(f"Columns        : {len(df.columns)}")

    print(f"\nOutput File:")
    print(OUTPUT_FILE)

    print("=" * 55)

# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    try:

        df = load_dataset()

        validate_columns(df)

        df = clean_text_columns(df)

        df = convert_numeric_columns(df)

        df = recalculate_totals(df)

        df = recalculate_improvement(df)

        df = remove_duplicates(df)

        save_dataset(df)

        print_summary(df)

    except Exception as error:

        logging.error(error)


if __name__ == "__main__":
    main()
