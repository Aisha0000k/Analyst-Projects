"""
SpaceX Launch Data SQL Analysis Module

I perform SQL-based analysis on SpaceX launch data using SQLite.
I connect to a database, load launch records, and execute queries
to answer analytical questions about launches.

Author: Yaseen
"""

import sqlite3
import pandas as pd


DATABASE_NAME = "spacex_launches.db"
SPACEX_CSV_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv"


def create_database_connection(db_name=DATABASE_NAME):
    """
    I create a connection to the SQLite database.

    Args:
        db_name: Name of the database file

    Returns:
        tuple: (connection, cursor)
    """
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    return con, cur


def load_csv_to_database(csv_url, table_name, con):
    """
    I load SpaceX data from a CSV URL into a SQLite table.

    Args:
        csv_url: URL to the CSV file
        table_name: Name for the database table
        con: Database connection

    Returns:
        DataFrame: Loaded data
    """
    df = pd.read_csv(csv_url)
    df.to_sql(table_name, con, if_exists="replace", index=False, method="multi")
    return df


def clean_table(con):
    """
    I remove any rows with null dates and create a clean table.

    Args:
        con: Database connection
    """
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS SPACEXTABLE")
    cur.execute(
        "create table SPACEXTABLE as select * from SPACEXTBL where Date is not null"
    )
    con.commit()


def query_unique_launch_sites(con):
    """
    I find all unique launch sites in the dataset.

    Args:
        con: Database connection

    Returns:
        list: Tuple of launch site names
    """
    query = "SELECT DISTINCT Launch_Site FROM SPACEXTABLE"
    return con.execute(query).fetchall()


def query_launches_by_site_pattern(con, pattern, limit=None):
    """
    I find launches where the site name matches a pattern.

    Args:
        con: Database connection
        pattern: SQL LIKE pattern (e.g., 'CCA%')
        limit: Optional row limit

    Returns:
        list: Matching rows
    """
    query = f"SELECT * FROM SPACEXTABLE WHERE Launch_Site LIKE '{pattern}'"
    if limit:
        query += f" LIMIT {limit}"
    return con.execute(query).fetchall()


def query_total_payload_by_customer(con, customer):
    """
    I calculate the total payload mass for a specific customer.

    Args:
        con: Database connection
        customer: Customer name

    Returns:
        tuple: Total payload mass
    """
    query = f"""
        SELECT SUM(PAYLOAD_MASS__KG_) AS total_payload_mass_kg 
        FROM SPACEXTABLE 
        WHERE Customer = '{customer}'
    """
    return con.execute(query).fetchall()


def query_booster_versions_with_max_payload(con):
    """
    I find all booster versions that carried the maximum payload mass.

    Args:
        con: Database connection

    Returns:
        list: Booster versions with max payload
    """
    query = """
        SELECT DISTINCT Booster_Version 
        FROM SPACEXTABLE 
        WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTABLE)
    """
    return con.execute(query).fetchall()


def query_first_successful_ground_pad_landing(con):
    """
    I find the date of the first successful landing on a ground pad.

    Args:
        con: Database connection

    Returns:
        tuple: Date string
    """
    query = """
        SELECT MIN(Date) AS first_success_ground_pad_date 
        FROM SPACEXTABLE 
        WHERE Landing_Outcome LIKE 'Success (ground pad)%'
    """
    return con.execute(query).fetchall()


def query_drone_ship_success_with_payload_range(con, min_mass, max_mass):
    """
    I find boosters that successfully landed on drone ship
    with payload in a specific range.

    Args:
        con: Database connection
        min_mass: Minimum payload mass
        max_mass: Maximum payload mass

    Returns:
        list: Booster versions
    """
    query = f"""
        SELECT DISTINCT Booster_Version 
        FROM SPACEXTABLE 
        WHERE Landing_Outcome LIKE 'Success (drone ship)%' 
          AND PAYLOAD_MASS__KG_ > {min_mass} 
          AND PAYLOAD_MASS__KG_ < {max_mass}
    """
    return con.execute(query).fetchall()


def query_landing_outcome_counts(con):
    """
    I count occurrences of each landing outcome type.

    Args:
        con: Database connection

    Returns:
        list: Outcome counts
    """
    query = """
        SELECT Landing_Outcome, COUNT(*) AS total 
        FROM SPACEXTABLE 
        GROUP BY Landing_Outcome
    """
    return con.execute(query).fetchall()


def query_failures_in_2015(con):
    """
    I find all drone ship landing failures in the year 2015.

    Args:
        con: Database connection

    Returns:
        list: Failure records
    """
    query = """
        SELECT substr(Date, 6, 2) AS month, 
               Landing_Outcome, 
               Booster_Version, 
               Launch_Site 
        FROM SPACEXTABLE 
        WHERE substr(Date, 0, 5) = '2015' 
          AND Landing_Outcome LIKE 'Failure (drone ship)%'
    """
    return con.execute(query).fetchall()


def query_landing_outcomes_by_date_range(con, start_date, end_date):
    """
    I rank landing outcomes by count within a date range.

    Args:
        con: Database connection
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)

    Returns:
        list: Ranked outcome counts
    """
    query = f"""
        SELECT Landing_Outcome, COUNT(*) AS outcome_count 
        FROM SPACEXTABLE 
        WHERE Date BETWEEN '{start_date}' AND '{end_date}' 
        GROUP BY Landing_Outcome 
        ORDER BY outcome_count DESC
    """
    return con.execute(query).fetchall()


def run_sql_analysis():
    """
    I orchestrate the complete SQL analysis pipeline:
    load data, clean, and run analytical queries.
    """
    con, cur = create_database_connection()

    print("=== Loading CSV Data ===")
    df = load_csv_to_database(SPACEX_CSV_URL, "SPACEXTBL", con)
    print(f"Loaded {len(df)} records")

    print("\n=== Cleaning Table ===")
    clean_table(con)

    print("\n=== Unique Launch Sites ===")
    sites = query_unique_launch_sites(con)
    for site in sites:
        print(f"  - {site[0]}")

    print("\n=== CCA Launch Sites (First 5) ===")
    cca_launches = query_launches_by_site_pattern(con, "CCA%", 5)
    print(f"Found {len(cca_launches)} launches")

    print("\n=== NASA CRS Total Payload ===")
    nasa_payload = query_total_payload_by_customer(con, "NASA (CRS)")
    print(f"Total: {nasa_payload[0][0]} kg")

    print("\n=== First Successful Ground Pad Landing ===")
    first_landing = query_first_successful_ground_pad_landing(con)
    print(f"Date: {first_landing[0][0]}")

    print("\n=== Drone Ship Success (4000-6000 kg payload) ===")
    boosters = query_drone_ship_success_with_payload_range(con, 4000, 6000)
    for booster in boosters:
        print(f"  - {booster[0]}")

    print("\n=== Landing Outcome Counts ===")
    outcomes = query_landing_outcome_counts(con)
    for outcome, count in outcomes:
        print(f"  {outcome}: {count}")

    print("\n=== 2015 Drone Ship Failures ===")
    failures = query_failures_in_2015(con)
    for failure in failures:
        print(f"  Month {failure[0]}: {failure[2]} at {failure[3]}")

    print("\n=== Landing Outcomes (2010-2017) ===")
    ranked = query_landing_outcomes_by_date_range(con, "2010-06-04", "2017-03-20")
    for outcome, count in ranked:
        print(f"  {outcome}: {count}")

    con.close()
    print("\n=== Analysis Complete ===")


if __name__ == "__main__":
    run_sql_analysis()
