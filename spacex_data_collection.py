"""
SpaceX Falcon 9 Launch Data Collection Module

This module handles collecting SpaceX launch data from the SpaceX API v4.
It fetches rocket, launchpad, payload, and core information to build
a comprehensive launch dataset.

Author: Yaseen
"""

import requests
import pandas as pd
import numpy as np
import datetime


pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)


SPACE_X_API_BASE = "https://api.spacexdata.com/v4"
STATIC_JSON_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json"


def get_booster_version(data):
    """
    I fetch the booster/rocket name for each launch from the SpaceX API.

    Args:
        data: DataFrame containing 'rocket' column with rocket IDs

    Returns:
        list: Booster names corresponding to each launch
    """
    booster_versions = []
    for x in data["rocket"]:
        if x:
            response = requests.get(f"{SPACE_X_API_BASE}/rockets/{str(x)}").json()
            booster_versions.append(response["name"])
    return booster_versions


def get_launch_site(data):
    """
    I extract launch site details including name, longitude, and latitude
    from the SpaceX API for each launch.

    Args:
        data: DataFrame containing 'launchpad' column with launchpad IDs

    Returns:
        tuple: Lists of (longitudes, latitudes, launch_site_names)
    """
    longitudes, latitudes, launch_sites = [], [], []
    for x in data["launchpad"]:
        if x:
            response = requests.get(f"{SPACE_X_API_BASE}/launchpads/{str(x)}").json()
            longitudes.append(response["longitude"])
            latitudes.append(response["latitude"])
            launch_sites.append(response["name"])
    return longitudes, latitudes, launch_sites


def get_payload_data(data):
    """
    I retrieve payload mass (kg) and orbit type for each launch
    from the SpaceX API.

    Args:
        data: DataFrame containing 'payloads' column with payload IDs

    Returns:
        tuple: Lists of (payload_masses, orbits)
    """
    payload_masses, orbits = [], []
    for load in data["payloads"]:
        if load:
            response = requests.get(f"{SPACE_X_API_BASE}/payloads/{load}").json()
            payload_masses.append(response["mass_kg"])
            orbits.append(response["orbit"])
    return payload_masses, orbits


def get_core_data(data):
    """
    I gather detailed core information including landing outcomes,
    flight counts, gridfin status, reuse status, legs, landing pad,
    block number, reuse count, and serial number from the API.

    Args:
        data: DataFrame containing 'cores' column with core information

    Returns:
        tuple: Lists of all core-related attributes
    """
    blocks, reused_counts, serials = [], [], []
    outcomes, flights, gridfins, reused, legs, landing_pads = [], [], [], [], [], []

    for core in data["cores"]:
        if core["core"] is not None:
            response = requests.get(f"{SPACE_X_API_BASE}/cores/{core['core']}").json()
            blocks.append(response["block"])
            reused_counts.append(response["reuse_count"])
            serials.append(response["serial"])
        else:
            blocks.append(None)
            reused_counts.append(None)
            serials.append(None)

        outcomes.append(str(core["landing_success"]) + " " + str(core["landing_type"]))
        flights.append(core["flight"])
        gridfins.append(core["gridfins"])
        reused.append(core["reused"])
        legs.append(core["legs"])
        landing_pads.append(core["landpad"])

    return (
        blocks,
        reused_counts,
        serials,
        outcomes,
        flights,
        gridfins,
        reused,
        legs,
        landing_pads,
    )


def fetch_launch_data():
    """
    I fetch all past SpaceX launches from the API and return a normalized DataFrame.

    Returns:
        DataFrame: Normalized launch data with all relevant columns
    """
    response = requests.get(STATIC_JSON_URL)
    data = pd.json_normalize(response.json())

    data = data[
        ["flight_number", "date_utc", "rocket", "payloads", "launchpad", "cores"]
    ].copy()
    data["payloads"] = data["payloads"].apply(
        lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None
    )
    data["cores"] = data["cores"].apply(
        lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None
    )

    return data


def build_launch_dataframe(data):
    """
    I construct a clean DataFrame by calling helper functions to enrich
    the launch data with detailed rocket, site, payload, and core information.

    Args:
        data: DataFrame with basic launch information

    Returns:
        DataFrame: Enriched launch data with all features
    """
    booster_versions = get_booster_version(data)
    longitudes, latitudes, launch_sites = get_launch_site(data)
    payload_masses, orbits = get_payload_data(data)
    (
        blocks,
        reused_counts,
        serials,
        outcomes,
        flights,
        gridfins,
        reused,
        legs,
        landing_pads,
    ) = get_core_data(data)

    launch_df = pd.DataFrame(
        {
            "FlightNumber": data["flight_number"],
            "Date": pd.to_datetime(data["date_utc"]).dt.date,
            "BoosterVersion": booster_versions,
            "PayloadMass": payload_masses,
            "Orbit": orbits,
            "LaunchSite": launch_sites,
            "Longitude": longitudes,
            "Latitude": latitudes,
            "Outcome": outcomes,
            "Flights": flights,
            "GridFins": gridfins,
            "Reused": reused,
            "Legs": legs,
            "LandingPad": landing_pads,
            "Block": blocks,
            "ReusedCount": reused_counts,
            "Serial": serials,
        }
    )

    return launch_df


def filter_falcon9_launches(launch_df):
    """
    I filter the DataFrame to include only Falcon 9 launches,
    excluding Falcon 1 and Falcon Heavy missions.

    Args:
        launch_df: DataFrame with all launches

    Returns:
        DataFrame: Filtered DataFrame with only Falcon 9 launches
    """
    return launch_df[launch_df["BoosterVersion"] != "Falcon 1"].copy()


def run_data_collection():
    """
    I orchestrate the complete data collection pipeline:
    fetch data, build DataFrame, and filter for Falcon 9.

    Returns:
        DataFrame: Cleaned Falcon 9 launch data ready for analysis
    """
    raw_data = fetch_launch_data()
    launch_df = build_launch_dataframe(raw_data)
    falcon9_df = filter_falcon9_launches(launch_df)

    return falcon9_df


if __name__ == "__main__":
    df = run_data_collection()
    print(f"Collected {len(df)} Falcon 9 launches")
    print(df.head())
