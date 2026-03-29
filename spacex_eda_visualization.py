"""
SpaceX Falcon 9 Exploratory Data Analysis Module

I perform exploratory data analysis and feature engineering on SpaceX
launch data. I create visualizations to understand relationships
between features and landing success, then prepare features for
machine learning models.

Author: Yaseen
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


DATASET_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"


def load_data(url=DATASET_URL):
    """
    I load the SpaceX dataset for analysis.

    Args:
        url: URL to the CSV file

    Returns:
        DataFrame: SpaceX launch data
    """
    df = pd.read_csv(url)
    return df


def plot_flight_number_vs_payload(df):
    """
    I create a scatter plot showing Flight Number vs Payload Mass,
    colored by landing outcome to visualize patterns.

    Args:
        df: DataFrame with FlightNumber, PayloadMass, and Class columns
    """
    sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect=5)
    plt.xlabel("Flight Number", fontsize=20)
    plt.ylabel("Payload Mass (kg)", fontsize=20)
    plt.title("Flight Number vs Payload Mass by Landing Success")
    plt.show()


def plot_flight_number_vs_launch_site(df):
    """
    I visualize the relationship between flight number and launch site,
    showing how success rates vary across sites over time.

    Args:
        df: DataFrame with FlightNumber, LaunchSite, and Class columns
    """
    sns.catplot(x="FlightNumber", y="LaunchSite", hue="Class", data=df, aspect=5)
    plt.xlabel("Flight Number", fontsize=20)
    plt.ylabel("Launch Site", fontsize=20)
    plt.title("Flight Number vs Launch Site by Landing Success")
    plt.show()


def plot_payload_vs_launch_site(df):
    """
    I visualize how payload mass relates to launch sites
    and landing success.

    Args:
        df: DataFrame with PayloadMass, LaunchSite, and Class columns
    """
    sns.catplot(x="PayloadMass", y="LaunchSite", hue="Class", data=df, aspect=5)
    plt.xlabel("Payload Mass (kg)", fontsize=20)
    plt.ylabel("Launch Site", fontsize=20)
    plt.title("Payload Mass vs Launch Site by Landing Success")
    plt.show()


def calculate_orbit_success_rates(df):
    """
    I calculate the success rate for each orbit type.

    Args:
        df: DataFrame with Orbit and Class columns

    Returns:
        DataFrame: Orbit success rates
    """
    orbit_success = df.groupby("Orbit")["Class"].mean().reset_index()
    return orbit_success


def plot_orbit_success_rates(df):
    """
    I create a bar chart showing success rates by orbit type.

    Args:
        df: DataFrame with Orbit and Class columns
    """
    orbit_success = calculate_orbit_success_rates(df)

    plt.figure(figsize=(12, 6))
    sns.barplot(x="Orbit", y="Class", data=orbit_success)
    plt.xlabel("Orbit", fontsize=12)
    plt.ylabel("Success Rate", fontsize=12)
    plt.title("Landing Success Rate by Orbit Type")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_flight_number_vs_orbit(df):
    """
    I visualize the relationship between flight number and orbit type,
    revealing how success patterns vary across different orbits over time.

    Args:
        df: DataFrame with FlightNumber, Orbit, and Class columns
    """
    sns.catplot(x="FlightNumber", y="Orbit", hue="Class", data=df, aspect=5)
    plt.xlabel("Flight Number", fontsize=20)
    plt.ylabel("Orbit", fontsize=20)
    plt.title("Flight Number vs Orbit by Landing Success")
    plt.show()


def plot_payload_vs_orbit(df):
    """
    I visualize the relationship between payload mass and orbit type,
    showing how heavy payloads perform in different orbits.

    Args:
        df: DataFrame with PayloadMass, Orbit, and Class columns
    """
    sns.catplot(x="PayloadMass", y="Orbit", hue="Class", data=df, aspect=5)
    plt.xlabel("Payload Mass (kg)", fontsize=20)
    plt.ylabel("Orbit", fontsize=20)
    plt.title("Payload Mass vs Orbit by Landing Success")
    plt.show()


def extract_year_from_date(df):
    """
    I extract the year from the Date column for temporal analysis.

    Args:
        df: DataFrame with Date column

    Returns:
        DataFrame: DataFrame with Date converted to year
    """
    df["Date"] = pd.to_datetime(df["Date"]).dt.year
    return df


def calculate_yearly_success_trend(df):
    """
    I calculate the average success rate for each year.

    Args:
        df: DataFrame with Date (year) and Class columns

    Returns:
        DataFrame: Yearly success rates
    """
    df = extract_year_from_date(df)
    yearly_success = df.groupby("Date")["Class"].mean().reset_index()
    return yearly_success


def plot_yearly_success_trend(df):
    """
    I create a line chart showing how landing success rate
    evolved over the years.

    Args:
        df: DataFrame with Date (year) and Class columns
    """
    yearly_success = calculate_yearly_success_trend(df)

    plt.figure(figsize=(10, 5))
    plt.plot(yearly_success["Date"], yearly_success["Class"])
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Average Success Rate", fontsize=12)
    plt.title("Yearly Launch Success Trend")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def select_features(df):
    """
    I select the relevant features for machine learning.

    Args:
        df: DataFrame with all columns

    Returns:
        DataFrame: Feature matrix
    """
    features = df[
        [
            "FlightNumber",
            "PayloadMass",
            "Orbit",
            "LaunchSite",
            "Flights",
            "GridFins",
            "Reused",
            "Legs",
            "LandingPad",
            "Block",
            "ReusedCount",
            "Serial",
        ]
    ]
    return features


def one_hot_encode_features(features):
    """
    I apply one-hot encoding to categorical columns.

    Args:
        features: DataFrame with categorical columns

    Returns:
        DataFrame: One-hot encoded feature matrix
    """
    features_one_hot = pd.get_dummies(
        features, columns=["Orbit", "LaunchSite", "LandingPad", "Serial"]
    )
    return features_one_hot


def cast_to_float64(df):
    """
    I cast all columns to float64 for machine learning compatibility.

    Args:
        df: DataFrame to convert

    Returns:
        DataFrame: All columns as float64
    """
    return df.astype("float64")


def save_features(features, filepath="dataset_part_3.csv"):
    """
    I save the engineered features to a CSV file.

    Args:
        features: Feature DataFrame
        filepath: Output file path
    """
    features.to_csv(filepath, index=False)


def run_eda():
    """
    I orchestrate the complete EDA pipeline:
    load data, create visualizations, and prepare features.

    Returns:
        DataFrame: Engineered features ready for ML
    """
    df = load_data()

    print("=== Sample Data ===")
    print(df.head())

    print("\n=== Plotting Flight Number vs Payload Mass ===")
    plot_flight_number_vs_payload(df)

    print("\n=== Plotting Flight Number vs Launch Site ===")
    plot_flight_number_vs_launch_site(df)

    print("\n=== Plotting Payload vs Launch Site ===")
    plot_payload_vs_launch_site(df)

    print("\n=== Plotting Orbit Success Rates ===")
    plot_orbit_success_rates(df)

    print("\n=== Plotting Flight Number vs Orbit ===")
    plot_flight_number_vs_orbit(df)

    print("\n=== Plotting Payload vs Orbit ===")
    plot_payload_vs_orbit(df)

    print("\n=== Plotting Yearly Success Trend ===")
    plot_yearly_success_trend(df)

    features = select_features(df)
    features_one_hot = one_hot_encode_features(features)
    features_one_hot = cast_to_float64(features_one_hot)

    print("\n=== Engineered Features Shape ===")
    print(f"Features: {features_one_hot.shape}")

    save_features(features_one_hot)

    return features_one_hot


if __name__ == "__main__":
    features = run_eda()
    print(f"\nSaved {len(features)} feature rows")
