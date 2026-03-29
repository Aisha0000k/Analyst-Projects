"""
SpaceX Falcon 9 Web Scraping Module

I scrape Falcon 9 and Falcon Heavy launch records from Wikipedia.
This module extracts launch data from HTML tables on the Wikipedia
page and converts it into a structured pandas DataFrame.

Author: Yaseen
"""

import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd


WIKIPEDIA_URL = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36"
}


def date_time(table_cells):
    """
    I extract date and time from an HTML table cell.

    Args:
        table_cells: BeautifulSoup element containing table cell data

    Returns:
        list: [date_string, time_string]
    """
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]


def booster_version(table_cells):
    """
    I extract the booster version from an HTML table cell.
    I filter out reference markers and unwanted characters.

    Args:
        table_cells: BeautifulSoup element containing booster info

    Returns:
        str: Clean booster version string
    """
    out = "".join(
        [
            booster_version
            for i, booster_version in enumerate(table_cells.strings)
            if i % 2 == 0
        ][0:-1]
    )
    return out


def landing_status(table_cells):
    """
    I extract the landing status/outcome from an HTML table cell.

    Args:
        table_cells: BeautifulSoup element containing landing status

    Returns:
        str: Landing status string
    """
    out = [i for i in table_cells.strings][0]
    return out


def get_mass(table_cells):
    """
    I extract the payload mass from an HTML table cell,
    cleaning up Unicode characters and formatting.

    Args:
        table_cells: BeautifulSoup element containing mass info

    Returns:
        str: Mass string with units (e.g., "500 kg")
    """
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass = mass[0 : mass.find("kg") + 2]
    else:
        new_mass = "0"
    return new_mass


def extract_column_from_header(row):
    """
    I extract column names from HTML table headers,
    cleaning up HTML tags and special characters.

    Args:
        row: BeautifulSoup element containing header row

    Returns:
        str or None: Clean column name if valid
    """
    if row.br:
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()

    column_name = " ".join(row.contents)

    if not (column_name.strip().isdigit()):
        column_name = column_name.strip()
        return column_name
    return None


def fetch_wikipedia_page():
    """
    I fetch the Wikipedia page and create a BeautifulSoup parser.

    Returns:
        BeautifulSoup: Parsed HTML content
    """
    response = requests.get(WIKIPEDIA_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def get_launch_table(soup):
    """
    I find and return the main launch records table from the parsed HTML.
    The third table on the page contains the actual launch data.

    Args:
        soup: BeautifulSoup object of the Wikipedia page

    Returns:
        BeautifulSoup element: The launch records table
    """
    html_tables = soup.find_all("table")
    return html_tables[2]


def extract_column_names(table):
    """
    I iterate through table headers to extract all valid column names.

    Args:
        table: BeautifulSoup table element

    Returns:
        list: Column names extracted from headers
    """
    column_names = []
    for th in table.find_all("th"):
        name = extract_column_from_header(th)
        if name is not None and len(name) > 0:
            column_names.append(name)
    return column_names


def initialize_launch_dictionary(column_names):
    """
    I create a dictionary structure to store parsed launch records,
    initializing lists for each column.

    Args:
        column_names: List of column names for the dictionary

    Returns:
        dict: Empty dictionary with list values for each column
    """
    launch_dict = dict.fromkeys(column_names)
    del launch_dict["Date and time ( )"]

    launch_dict["Flight No."] = []
    launch_dict["Launch site"] = []
    launch_dict["Payload"] = []
    launch_dict["Payload mass"] = []
    launch_dict["Orbit"] = []
    launch_dict["Customer"] = []
    launch_dict["Launch outcome"] = []
    launch_dict["Version Booster"] = []
    launch_dict["Booster landing"] = []
    launch_dict["Date"] = []
    launch_dict["Time"] = []

    return launch_dict


def parse_launch_records(soup, launch_dict):
    """
    I parse all launch records from the HTML tables and populate
    the launch dictionary with extracted data.

    Args:
        soup: BeautifulSoup object of the Wikipedia page
        launch_dict: Dictionary to populate with parsed data

    Returns:
        dict: Populated launch dictionary
    """
    extracted_row = 0

    for table_number, table in enumerate(
        soup.find_all("table", "wikitable plainrowheaders collapsible")
    ):
        for rows in table.find_all("tr"):
            if rows.th:
                if rows.th.string:
                    flight_number = rows.th.string.strip()
                    flag = flight_number.isdigit()
            else:
                flag = False

            row = rows.find_all("td")

            if flag:
                extracted_row += 1
                launch_dict["Flight No."].append(flight_number)

                datatimelist = date_time(row[0])
                date = datatimelist[0].strip(",")
                launch_dict["Date"].append(date)

                time = datatimelist[1]
                launch_dict["Time"].append(time)

                bv = booster_version(row[1])
                if not bv:
                    bv = row[1].a.string
                launch_dict["Version Booster"].append(bv)

                launch_dict["Launch site"].append(row[2].a.string)
                launch_dict["Payload"].append(row[3].a.string)
                launch_dict["Payload mass"].append(get_mass(row[4]))
                launch_dict["Orbit"].append(row[5].a.string)

                if row[6].a:
                    launch_dict["Customer"].append(row[6].a.string)
                else:
                    launch_dict["Customer"].append(row[6].strings)

                launch_dict["Launch outcome"].append(list(row[7].strings)[0])
                launch_dict["Booster landing"].append(landing_status(row[8]))

    return launch_dict


def create_dataframe(launch_dict):
    """
    I convert the parsed launch dictionary into a pandas DataFrame.

    Args:
        launch_dict: Dictionary containing parsed launch data

    Returns:
        DataFrame: Structured launch data
    """
    return pd.DataFrame(launch_dict)


def run_scraping():
    """
    I orchestrate the complete web scraping pipeline:
    fetch page, parse tables, extract records, and return DataFrame.

    Returns:
        DataFrame: Parsed SpaceX launch records from Wikipedia
    """
    soup = fetch_wikipedia_page()
    table = get_launch_table(soup)
    column_names = extract_column_names(table)
    launch_dict = initialize_launch_dictionary(column_names)
    launch_dict = parse_launch_records(soup, launch_dict)
    df = create_dataframe(launch_dict)

    return df


if __name__ == "__main__":
    df = run_scraping()
    print(f"Scraped {len(df)} launch records")
    print(df.head())
