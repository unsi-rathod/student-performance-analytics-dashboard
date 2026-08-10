"""
=========================================================
Student Performance Analytics Project
Phase 3 - Feature Engineering

Author  : Unsi Rathod
Purpose : Generate analytical features from the cleaned
          student performance dataset.

This script:
1. Reads the cleaned dataset
2. Creates engineered analytical features
3. Saves a new feature engineered dataset
=========================================================
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd


# =========================================================
# Logging Configuration
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)


# =========================================================
# Paths
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FOLDER = PROJECT_ROOT / "Data" / "Cleaned_Data"
OUTPUT_FOLDER = PROJECT_ROOT / "Data" / "Cleaned_Data"


# =========================================================
# Helper Functions
# =========================================================

def get_latest_cleaned_file(folder):
    """
    Returns the most recently modified cleaned dataset.
    """

    files = list(folder.glob("*.csv"))

    if not files:
        raise FileNotFoundError(
            "No cleaned CSV dataset found."
        )

    latest = max(files, key=lambda x: x.stat().st_mtime)

    logging.info(f"Reading file: {latest.name}")

    return latest


def validate_columns(df):
    """
    Validate required columns.
    """

    required_columns = [

        "HY",
        "Y",

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

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )


def calculate_percentages(df):
    """
    Creates Half-Yearly and Annual percentages.
    """

    TOTAL_MARKS = 80

    df["HY_Percentage"] = (
        (df["HY"] / TOTAL_MARKS) * 100
    ).round(2)

    df["Annual_Percentage"] = (
        (df["Y"] / TOTAL_MARKS) * 100
    ).round(2)

    df["Improvement_Percentage"] = (
        df["Annual_Percentage"]
        - df["HY_Percentage"]
    ).round(2)

    return df


# =========================================================
# Improvement Status
# =========================================================

def improvement_status(value):

    if value > 5:
        return "Improved"

    if value < -5:
        return "Declined"

    return "Stable"


# =========================================================
# Performance Band
# =========================================================

def performance_band(value):

    if value >= 90:
        return "Excellent"

    if value >= 75:
        return "Good"

    if value >= 60:
        return "Average"

    if value >= 40:
        return "Needs Improvement"

    return "At Risk"


# =========================================================
# Risk Level
# =========================================================

def risk_level(value):

    if value >= 75:
        return "Low"

    if value >= 50:
        return "Medium"

    return "High"


# =========================================================
# Growth Category
# =========================================================

def growth_category(value):

    if value > 10:
        return "Significant Growth"

    if value > 5:
        return "Moderate Growth"

    if value >= -5:
        return "Stable"

    if value >= -10:
        return "Slight Decline"

    return "Major Decline"


# =========================================================
# Consistency Score
# =========================================================

def consistency_score(row):

    difference = abs(
        row["Annual_Percentage"]
        - row["HY_Percentage"]
    )

    if difference <= 5:
        return "High"

    if difference <= 10:
        return "Moderate"

    return "Low"


# =========================================================
# Strongest / Weakest Section
# =========================================================

SECTION_NAMES = {

    "Y_Q1": "MCQ",

    "Y_Q2": "2-Mark Questions",

    "Y_Q3": "3-Mark Questions",

    "Y_Q4": "Long Answer",

    "Y_Q5": "Case Based"

}


def strongest_section(row):

    scores = {

        "Y_Q1": row["Y_Q1"],
        "Y_Q2": row["Y_Q2"],
        "Y_Q3": row["Y_Q3"],
        "Y_Q4": row["Y_Q4"],
        "Y_Q5": row["Y_Q5"]

    }

    highest = max(
        scores,
        key=scores.get
    )

    return SECTION_NAMES[highest]


def weakest_section(row):

    scores = {

        "Y_Q1": row["Y_Q1"],
        "Y_Q2": row["Y_Q2"],
        "Y_Q3": row["Y_Q3"],
        "Y_Q4": row["Y_Q4"],
        "Y_Q5": row["Y_Q5"]

    }

    lowest = min(
        scores,
        key=scores.get
    )

    return SECTION_NAMES[lowest]

# =========================================================
# Feature Engineering
# =========================================================

def engineer_features(df):
    """
    Create all engineered analytical features.
    """

    logging.info("Creating analytical features...")

    # Percentages
    df = calculate_percentages(df)

    # Improvement Status
    df["Improvement_Status"] = (
        df["Improvement_Percentage"]
        .apply(improvement_status)
    )

    # Performance Band
    df["Performance_Band"] = (
        df["Annual_Percentage"]
        .apply(performance_band)
    )

    # Risk Level
    df["Risk_Level"] = (
        df["Annual_Percentage"]
        .apply(risk_level)
    )

    # Needs Intervention
    df["Needs_Intervention"] = np.where(
        df["Risk_Level"] == "High",
        "Yes",
        "No"
    )

    # Consistency Score
    df["Consistency_Score"] = (
        df.apply(
            consistency_score,
            axis=1
        )
    )

    # Strongest Section
    df["Strongest_Section"] = (
        df.apply(
            strongest_section,
            axis=1
        )
    )

    # Weakest Section
    df["Weakest_Section"] = (
        df.apply(
            weakest_section,
            axis=1
        )
    )

    # Growth Category
    df["Growth_Category"] = (
        df["Improvement_Percentage"]
        .apply(growth_category)
    )

    logging.info("Feature engineering completed.")

    return df


# =========================================================
# Save Dataset
# =========================================================

def save_dataset(df):
    """
    Save feature engineered dataset.
    """

    output_file = (
        OUTPUT_FOLDER /
        "student_performance_feature_engineered.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    logging.info(
        "Feature engineered dataset saved successfully."
    )

    logging.info(
        f"Location: {output_file}"
    )


# =========================================================
# Main Function
# =========================================================

def main():
    """
    Main execution function.
    """

    try:

        logging.info(
            "Starting Feature Engineering..."
        )

        input_file = get_latest_cleaned_file(
            INPUT_FOLDER
        )

        df = pd.read_csv(input_file)

        logging.info(
            "Dataset loaded successfully."
        )

        validate_columns(df)

        logging.info(
            "Required columns validated."
        )

        df = engineer_features(df)

        save_dataset(df)

        logging.info(
            "Feature Engineering completed successfully."
        )

    except FileNotFoundError as error:

        logging.error(error)

    except ValueError as error:

        logging.error(error)

    except Exception as error:

        logging.error(
            f"Unexpected Error: {error}"
        )


# =========================================================
# Program Entry
# =========================================================

if __name__ == "__main__":
    main()
