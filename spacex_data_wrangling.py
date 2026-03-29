"""
SpaceX Falcon 9 Data Wrangling Module

I perform data cleaning and transformation on SpaceX launch data.
I identify patterns in landing outcomes and create classification
labels for machine learning (landing success/failure).

Author: Yaseen
"""

import pandas as pd
import numpy as np


DATASET_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv"


def load_spacex_data(url=DATASET_URL):
    """
    I load the SpaceX dataset from a CSV URL.

    Args:
        url: URL to the CSV file

    Returns:
        DataFrame: Raw SpaceX launch data
    """
    df = pd.read_csv(url)
    return df


def calculate_missing_values_percentage(df):
    """
    I calculate the percentage of missing values in each column.

    Args:
        df: DataFrame to analyze

    Returns:
        Series: Percentage of null values per column
    """
    return df.isnull().sum() / len(df) * 100


def identify_column_types(df):
    """
    I identify and return the data types of all columns.

    Args:
        df: DataFrame to analyze

    Returns:
        Series: Data types for each column
    """
    return df.dtypes


def count_launches_by_site(df):
    """
    I count the number of launches at each launch site.

    Args:
        df: DataFrame with LaunchSite column

    Returns:
        Series: Launch counts per site
    """
    return df["LaunchSite"].value_counts()


def count_launches_by_orbit(df):
    """
    I count the number of launches for each orbit type.

    Args:
        df: DataFrame with Orbit column

    Returns:
        Series: Launch counts per orbit
    """
    return df["Orbit"].value_counts()


def get_landing_outcomes(df):
    """
    I get the count of each unique landing outcome in the dataset.

    Args:
        df: DataFrame with Outcome column

    Returns:
        Series: Counts of each landing outcome
    """
    return df["Outcome"].value_counts()


def identify_failed_landings():
    """
    I define which landing outcomes represent failures.
    These are outcomes where the first stage did not land successfully.

    Returns:
        set: Set of failure outcome strings
    """
    failed_outcomes = {
        "False ASDS",
        "False Ocean",
        "False RTLS",
        "None ASDS",
        "None None",
    }
    return failed_outcomes


def create_landing_class(df):
    """
    I create a binary classification label based on landing outcome.
    1 = successful landing, 0 = failed landing.

    Args:
        df: DataFrame with Outcome column

    Returns:
        list: Binary classification labels
    """
    bad_outcomes = identify_failed_landings()
    landing_class = [0 if outcome in bad_outcomes else 1 for outcome in df["Outcome"]]
    return landing_class


def add_class_column(df):
    """
    I add the Class column to the DataFrame based on landing outcomes.

    Args:
        df: DataFrame with Outcome column

    Returns:
        DataFrame: DataFrame with new Class column
    """
    df["Class"] = create_landing_class(df)
    return df


def calculate_success_rate(df):
    """
    I calculate the overall landing success rate.

    Args:
        df: DataFrame with Class column

    Returns:
        float: Proportion of successful landings
    """
    return df["Class"].mean()


def save_processed_data(df, filepath="dataset_part_2.csv"):
    """
    I save the processed DataFrame to a CSV file.

    Args:
        df: Processed DataFrame
        filepath: Output file path
    """
    df.to_csv(filepath, index=False)


def run_wrangling():
    """
    I orchestrate the complete data wrangling pipeline:
    load data, analyze it, create labels, and save results.

    Returns:
        DataFrame: Fully processed SpaceX data with class labels
    """
    df = load_spacex_data()

    print("=== Missing Values Analysis ===")
    print(calculate_missing_values_percentage(df))

    print("\n=== Column Types ===")
    print(identify_column_types(df))

    print("\n=== Launches by Site ===")
    print(count_launches_by_site(df))

    print("\n=== Launches by Orbit ===")
    print(count_launches_by_orbit(df))

    print("\n=== Landing Outcomes ===")
    print(get_landing_outcomes(df))

    df = add_class_column(df)

    print(f"\n=== Success Rate ===")
    print(f"Landing Success Rate: {calculate_success_rate(df):.2%}")

    save_processed_data(df)

    return df


if __name__ == "__main__":
    df = run_wrangling()
    print(f"\nProcessed {len(df)} launches")
    print(df.head())
