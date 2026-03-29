
"""Run the SpaceX SQLite notebook as a regular Python script.

This file was converted from the uploaded notebook HTML.
It loads the SpaceX CSV into a local SQLite database and runs the
same SQL queries that appeared in the notebook.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


DATABASE_PATH = Path("my_data1.db")
DATASET_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv"
)


def print_section(title: str) -> None:
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


def run_query(con: sqlite3.Connection, title: str, query: str) -> pd.DataFrame:
    print_section(title)
    print(query.strip())
    result = pd.read_sql_query(query, con)
    if result.empty:
        print("No rows returned.")
    else:
        print(result.to_string(index=False))
    return result


def main() -> None:
    # I build a small local SQLite database so I can run the notebook queries as a script.
    con = sqlite3.connect(DATABASE_PATH)

    # I load the SpaceX launch dataset directly from the source CSV.
    df = pd.read_csv(DATASET_URL)
    df.to_sql("SPACEXTBL", con, if_exists="replace", index=False, method="multi")

    # I remove blank rows from the final table by rebuilding it from rows with a valid date.
    con.execute("DROP TABLE IF EXISTS SPACEXTABLE;")
    con.execute(
        "CREATE TABLE SPACEXTABLE AS "
        "SELECT * FROM SPACEXTBL WHERE Date IS NOT NULL"
    )
    con.commit()

    # I keep a short overview here so the converted file still has context.
    # I am working with SpaceX launch records so I can inspect launch sites,
    # payload mass, booster versions, customers, dates, and landing outcomes.

    # I list the distinct launch sites.
    run_query(
        con,
        "Query 1: I list the distinct launch sites.",
        """
        SELECT DISTINCT Launch_Site
        FROM SPACEXTABLE;
        """,
    )

    # I show five records where the launch site starts with 'CCA'.
    run_query(
        con,
        "Query 2: I show five records where the launch site starts with 'CCA'.",
        """
        SELECT *
        FROM SPACEXTABLE
        WHERE Launch_Site LIKE 'CCA%'
        LIMIT 5;
        """,
    )

    # I calculate the total payload mass carried for NASA (CRS) missions.
    run_query(
        con,
        "Query 3: I calculate the total payload mass carried for NASA (CRS) missions.",
        """
        SELECT SUM(PAYLOAD_MASS__KG_) AS total_payload_mass_kg
        FROM SPACEXTABLE
        WHERE Customer = 'NASA (CRS)';
        """,
    )

    # I list customers whose names start with NASA.
    run_query(
        con,
        "Query 4: I list customers whose names start with NASA.",
        """
        SELECT DISTINCT Customer
        FROM SPACEXTABLE
        WHERE Customer LIKE 'NASA%';
        """,
    )

    # I find the first successful ground-pad landing date.
    run_query(
        con,
        "Query 5: I find the first successful ground-pad landing date.",
        """
        SELECT MIN(Date) AS first_success_ground_pad_date
        FROM SPACEXTABLE
        WHERE Landing_Outcome LIKE 'Success (ground pad)%';
        """,
    )

    # I list booster versions with successful drone-ship landings and payload mass between 4000 and 6000 kg.
    run_query(
        con,
        "Query 6: I list booster versions with successful drone-ship landings and payload mass between 4000 and 6000 kg.",
        """
        SELECT DISTINCT Booster_Version
        FROM SPACEXTABLE
        WHERE Landing_Outcome LIKE 'Success (drone ship)%'
          AND PAYLOAD_MASS__KG_ > 4000
          AND PAYLOAD_MASS__KG_ < 6000;
        """,
    )

    # I count each landing outcome.
    run_query(
        con,
        "Query 7: I count each landing outcome.",
        """
        SELECT Landing_Outcome, COUNT(*) AS total
        FROM SPACEXTABLE
        GROUP BY Landing_Outcome;
        """,
    )

    # I list booster versions that carried the maximum payload mass.
    run_query(
        con,
        "Query 8: I list booster versions that carried the maximum payload mass.",
        """
        SELECT DISTINCT Booster_Version
        FROM SPACEXTABLE
        WHERE PAYLOAD_MASS__KG_ = (
            SELECT MAX(PAYLOAD_MASS__KG_)
            FROM SPACEXTABLE
        );
        """,
    )

    # I show 2015 drone-ship landing failures with month, booster version, and launch site.
    run_query(
        con,
        "Query 9: I show 2015 drone-ship landing failures with month, booster version, and launch site.",
        """
        SELECT substr(Date, 6, 2) AS month,
               Landing_Outcome,
               Booster_Version,
               Launch_Site
        FROM SPACEXTABLE
        WHERE substr(Date, 0, 5) = '2015'
          AND Landing_Outcome LIKE 'Failure (drone ship)%';
        """,
    )

    # I rank landing outcomes by count between 2010-06-04 and 2017-03-20.
    run_query(
        con,
        "Query 10: I rank landing outcomes by count between 2010-06-04 and 2017-03-20.",
        """
        SELECT Landing_Outcome, COUNT(*) AS outcome_count
        FROM SPACEXTABLE
        WHERE Date BETWEEN '2010-06-04' AND '2017-03-20'
        GROUP BY Landing_Outcome
        ORDER BY outcome_count DESC;
        """,
    )

    con.close()


if __name__ == "__main__":
    main()
