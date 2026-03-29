"""
Converted from jupyter-labs-webscraping.ipynb.html.
I run this notebook as a regular Python script outside Jupyter.
"""

# I note: **Space X  Falcon 9 First Stage Landing Prediction**

# I note: Web scraping Falcon 9 and Falcon Heavy Launches Records from Wikipedia

# I note: https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches

# I note: Falcon 9 first stage will land successfully

# I note: Several examples of an unsuccessful landing are shown here:

# I note: More specifically, the launch records are stored in a HTML table shown below:

# I note: Web scrap Falcon 9 launch records with BeautifulSoup:
# I note: Extract a Falcon 9 launch records HTML table from Wikipedia
# I note: Parse the table and convert it into a Pandas data frame

# I note: First let's import required packages for this lab

# I ran this notebook shell command interactively: !pip3 install beautifulsoup4
# I ran this notebook shell command interactively: !pip3 install requests

import sys

import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd

# I note: and we will provide some helper functions for you to process web scraped HTML table

def date_time(table_cells):
    """
    This function returns the data and time from the HTML  table cell
    Input: the  element of a table data cell extracts extra row
    """
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

def booster_version(table_cells):
    """
    This function returns the booster version from the HTML  table cell 
    Input: the  element of a table data cell extracts extra row
    """
    out = ''.join([booster_version for i, booster_version in enumerate(table_cells.strings) if i%2==0][0:-1])
    return out

def landing_status(table_cells):
    """
    This function returns the landing status from the HTML table cell 
    Input: the  element of a table data cell extracts extra row
    """
    out = [i for i in table_cells.strings][0]
    return out


def get_mass(table_cells):
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass = mass[0:mass.find("kg")+2]
    else:
        new_mass = 0
    return new_mass


def extract_column_from_header(row):
    """
    This function returns the landing status from the HTML table cell 
    Input: the  element of a table data cell extracts extra row
    """
    if (row.br):
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()

    colunm_name = ' '.join(row.contents)

    # Filter the digit and empty names
    if not (colunm_name.strip().isdigit()):
        colunm_name = colunm_name.strip()
        return colunm_name

# I note: To keep the lab tasks consistent, you will be asked to scrape the data from a snapshot of the  List of Falcon 9 and Falcon Heavy launches Wikipage updated on
# I note: 9th June 2021

static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}

# I note: Next, request the HTML page from the above URL and get a response object

# I note: First, let's perform an HTTP GET method to request the Falcon9 Launch HTML page, as an HTTP response.

# use requests.get() method with the provided static_url and headers
# assign the response to a object
response = requests.get(static_url, headers=headers)

# I note: Create a BeautifulSoup object from the HTML response

# Use BeautifulSoup() to create a BeautifulSoup object from a response text content
soup = BeautifulSoup(response.text, "html.parser")

# I note: Print the page title to verify if the BeautifulSoup object was created properly

# Use soup.title attribute
print(soup.title)

# I note: Next, we want to collect all relevant column names from the HTML table header

# Use the find_all function in the BeautifulSoup object, with element type `table`
# Assign the result to a list called `html_tables`
html_tables = soup.find_all("table")

# I note: Starting from the third table is our target table contains the actual launch records.

# Let's print the third table and check its content
first_launch_table = html_tables[2]
print(first_launch_table)

# I note: You should able to see the columns names embedded in the table header elements <th> as follows:

# I note: ```
# I note: Flight No.
# I note: Date and time ( UTC )
# I note: Version, Booster [b]
# I note: Launch site
# I note: Payload [c]
# I note: Payload mass
# I note: Orbit
# I note: Customer
# I note: Launch outcome
# I note: Booster landing
# I note: ```

# I note: Next, we just need to iterate through the <th> elements and apply the provided extract_column_from_header() to extract column name one by one

column_names = []

# Apply find_all() function with `th` element on first_launch_table
# Iterate each th element and apply the provided extract_column_from_header() to get a column name
# Append the Non-empty column name (`if name is not None and len(name) > 0`) into a list called column_names
for th in first_launch_table.find_all("th"):
    name = extract_column_from_header(th)
    if name is not None and len(name) > 0:
        column_names.append(name)

column_names

# I note: Check the extracted column names

print(column_names)

# I note: We will create an empty dictionary with keys from the extracted column names in the previous task. Later, this dictionary will be converted into a Pandas dataframe

launch_dict= dict.fromkeys(column_names)

# Remove an irrelvant column
del launch_dict['Date and time ( )']

# Let's initial the launch_dict with each value to be an empty list
launch_dict['Flight No.'] = []
launch_dict['Launch site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []
# Added some new columns
launch_dict['Version Booster']=[]
launch_dict['Booster landing']=[]
launch_dict['Date']=[]
launch_dict['Time']=[]

# I note: Next, we just need to fill up the launch_dict with launch records extracted from table rows.

# I note: Usually, HTML tables in Wiki pages are likely to contain unexpected annotations and other types of noises, such as reference links B0004.1[8], missing values N/A [e], inconsistent formatting, etc.

# I note: To simplify the parsing process, we have provided an incomplete code snippet below to help you to fill up the launch_dict. Please complete the following code snippet with TODOs or you can choose to write your own logic to parse all launch tables:

extracted_row = 0
#Extract each table

for table_number, table in enumerate(soup.find_all('table', "wikitable plainrowheaders collapsible")):
   # get table row 
    for rows in table.find_all("tr"):
        #check to see if first table heading is as number corresponding to launch a number 
        if rows.th:
            if rows.th.string:
                flight_number = rows.th.string.strip()
                flag = flight_number.isdigit()
        else:
            flag = False
        #get table element 
        row = rows.find_all('td')
        #if it is number save cells in a dictonary 
        if flag:
            extracted_row += 1
            # Flight Number value
            launch_dict['Flight No.'].append(flight_number)
            # TODO: Append the flight_number into launch_dict with key `Flight No.`
            #print(flight_number)
            datatimelist=date_time(row[0])
            
            # Date value
            # TODO: Append the date into launch_dict with key `Date`
            date = datatimelist[0].strip(',')
            launch_dict['Date'].append(date)
            #print(date)
            
            # Time value
            # TODO: Append the time into launch_dict with key `Time`
            time = datatimelist[1]
            launch_dict['Time'].append(time)
            #print(time)
              
            # Booster version
            # TODO: Append the bv into launch_dict with key `Version Booster`
            bv=booster_version(row[1])
            if not(bv):
                bv=row[1].a.string
            launch_dict['Version Booster'].append(bv)
            print(bv)
            
            # Launch Site
            # TODO: Append the bv into launch_dict with key `Launch Site`
            launch_site = row[2].a.string
            launch_dict['Launch site'].append(launch_site)
            #print(launch_site)
            
            
            # Payload
            # TODO: Append the payload into launch_dict with key `Payload`
            payload = row[3].a.string
            launch_dict['Payload'].append(payload)
            #print(payload)
            
            
            # Payload Mass
            # TODO: Append the payload_mass into launch_dict with key `Payload mass`
            payload_mass = get_mass(row[4])
            launch_dict['Payload mass'].append(payload_mass)
            #print(payload)
            
            
            # Orbit
            # TODO: Append the orbit into launch_dict with key `Orbit`
            orbit = row[5].a.string
            launch_dict['Orbit'].append(orbit)
            #print(orbit)
            
            
            # Customer
            # TODO: Append the customer into launch_dict with key `Customer`
            customer = row[6].a.string
            launch_dict['Customer'].append(customer)
            #print(customer)
            
            
            # Launch outcome
            # TODO: Append the launch_outcome into launch_dict with key `Launch outcome`
            launch_outcome = list(row[7].strings)[0]
            launch_dict['Launch outcome'].append(launch_outcome)
            #print(launch_outcome)
            
            
            # Booster landing
            # TODO: Append the launch_outcome into launch_dict with key `Booster landing`
            booster_landing = landing_status(row[8])
            launch_dict['Booster landing'].append(booster_landing)
            #print(booster_landing)

# I note: After you have fill in the parsed launch record values into launch_dict, you can create a dataframe from it.

df= pd.DataFrame({ key:pd.Series(value) for key, value in launch_dict.items() })

# I note: We can now export it to a <b>CSV</b> for the next section, but to make the answers consistent and in case you have difficulties finishing this lab.
# I note: Following labs will be using a provided dataset to make each lab independent.

# I note: df.to_csv('spacex_web_scraped.csv', index=False)

# I note: Authors

# I note: Yan Luo

# I note: Nayef Abou Tayoun

# I note: <!--
# I note: Change Log
# I note: -->

# I note: <!--
# I note: | Date (YYYY-MM-DD) | Version | Changed By | Change Description      |
# I note: | ----------------- | ------- | ---------- | ----------------------- |
# I note: | 2021-06-09        | 1.0     | Yan Luo    | Tasks updates           |
# I note: | 2020-11-10        | 1.0     | Nayef      | Created the initial version |
# I note: -->

# I note: Copyright © 2021 IBM Corporation. All rights reserved.
