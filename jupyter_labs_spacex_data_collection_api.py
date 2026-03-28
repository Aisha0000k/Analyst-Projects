"""
Converted from jupyter-labs-spacex-data-collection-api.ipynb.html.
I run this notebook as a regular Python script outside Jupyter.
"""

# I note: **SpaceX  Falcon 9 first stage Landing Prediction**

# I note: In this capstone, we will predict if the Falcon 9 first stage will land successfully. SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is because SpaceX can reuse the first stage. Therefore if we can determine if the first stage will land, we can determine the cost of a launch. This information can be used if an alternate company wants to bid against SpaceX for a rocket launch. In this lab, you will collect and make sure the data is in the correct format from an API. The following is an example of a successful and launch.

# I note: Several examples of an unsuccessful landing are shown here:

# I note: Most unsuccessful landings are planned. Space X performs a controlled landing in the oceans.

# I note: Request to the SpaceX API
# I note: Clean the requested data

# I note: Import Libraries and Define Auxiliary Functions

# I note: We will import the following libraries into the lab

# Requests allows us to make HTTP requests which we will use to get data from an API
import requests
# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Datetime is a library that allows us to represent dates
import datetime

# Setting this option will print all collumns of a dataframe
pd.set_option('display.max_columns', None)
# Setting this option will print all of the data in a feature
pd.set_option('display.max_colwidth', None)

# I note: Below we will define a series of helper functions that will help us use the API to extract information using identification numbers in the launch data.
# I note: From the <code>rocket</code> column we would like to learn the booster name.

# Takes the dataset and uses the rocket column to call the API and append the data to the list
def getBoosterVersion(data):
    for x in data['rocket']:
        if x:
            response = requests.get("https://api.spacexdata.com/v4/rockets/"+
                                    str(x)).json()
            BoosterVersion.append(response['name'])

# I note: From the <code>launchpad</code> we would like to know the name of the launch site being used, the logitude, and the latitude.

# Takes the dataset and uses the launchpad column to call the API and append the data to the list
def getLaunchSite(data):
    for x in data['launchpad']:
        if x:
            response = requests.get("https://api.spacexdata.com/v4/launchpads/"+
                                    str(x)).json()
            Longitude.append(response['longitude'])
            Latitude.append(response['latitude'])
            LaunchSite.append(response['name'])

# I note: From the <code>payload</code> we would like to learn the mass of the payload and the orbit that it is going to.

# Takes the dataset and uses the payloads column to call the API and append the data to the lists
def getPayloadData(data):
    for load in data['payloads']:
        if load:
            response = requests.get("https://api.spacexdata.com/v4/payloads/"+
                                    load).json()
            PayloadMass.append(response['mass_kg'])
            Orbit.append(response['orbit'])

# I note: From <code>cores</code> we would like to learn the outcome of the landing, the type of the landing, number of flights with that core, whether gridfins were used, wheter the core is reused, wheter legs were used, the landing pad used, the block of the core which is a number used to seperate version of cores, the number of times this specific core has been reused, and the serial of the core.

# Takes the dataset and uses the cores column to call the API and append the data to the lists
def getCoreData(data):
    for core in data['cores']:
        if core['core'] is not None:
            response = requests.get("https://api.spacexdata.com/v4/cores/"+core
                                    ['core']).json()
            Block.append(response['block'])
            ReusedCount.append(response['reuse_count'])
            Serial.append(response['serial'])
        else:
            Block.append(None)
            ReusedCount.append(None)
            Serial.append(None)
        Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
        Flights.append(core['flight'])
        GridFins.append(core['gridfins'])
        Reused.append(core['reused'])
        Legs.append(core['legs'])
        LandingPad.append(core['landpad'])

# I note: Now let's start requesting rocket launch data from SpaceX API with the following URL:

spacex_url = "https://api.spacexdata.com/v4/launches/past"

response = requests.get(spacex_url)

# I note: Check the content of the response

print(response.content)

# I note: You should see the response contains massive information about SpaceX launches. Next, let's try to discover some more relevant information for this project.

# I note: To make the requested JSON results more consistent, we will use the following static response object for this project:

static_json_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'

# I note: We should see that the request was successfull with the 200 status response code

response = requests.get(static_json_url)

response.status_code

# I note: Now we decode the response content as a Json using <code>.json()</code> and turn it into a Pandas dataframe using <code>.json_normalize()</code>

# Use json_normalize meethod to convert the json result into a dataframe
# Build the final dataframe (common DS0321 structure)
data = pd.json_normalize(response.json())

# 2) Keep the core columns used in this lab
data = data[['flight_number', 'date_utc', 'rocket', 'payloads', 'launchpad', 'cores']].copy()

# 3) Use only the first payload/core per launch (as in the DS0321 lab)
data['payloads'] = data['payloads'].apply(lambda x: x[0] if isinstance(x, list)
                                          and len(x) > 0 else None)
data['cores'] = data['cores'].apply(lambda x: x[0] if isinstance(x, list)
                                    and len(x) > 0 else None)

# 4) Create the lists that helper functions will fill
BoosterVersion, LaunchSite, Longitude, Latitude = [], [], [], []
PayloadMass, Orbit = [], []
Outcome, Flights, GridFins, Reused, Legs, LandingPad = [], [], [], [], [], []
Block, ReusedCount, Serial = [], [], []

# 5) Call the provided helper functions to populate the lists
getBoosterVersion(data)
getLaunchSite(data)
getPayloadData(data)
getCoreData(data)

# 6) Build the final dataframe (common DS0321 structure)
launch_df = pd.DataFrame({
    'FlightNumber': data['flight_number'],
    'Date': pd.to_datetime(data['date_utc']).dt.date,
    'BoosterVersion': BoosterVersion,
    'PayloadMass': PayloadMass,
    'Orbit': Orbit,
    'LaunchSite': LaunchSite,
    'Longitude': Longitude,
    'Latitude': Latitude,
    'Outcome': Outcome,
    'Flights': Flights,
    'GridFins': GridFins,
    'Reused': Reused,
    'Legs': Legs,
    'LandingPad': LandingPad,
    'Block': Block,
    'ReusedCount': ReusedCount,
    'Serial': Serial
})

# I note: Using the dataframe <code>data</code> print the first 5 rows

# Get the head of the dataframe
launch_df.head()

# I note: You will notice that a lot of the data are IDs. For example the rocket column has no information about the rocket just an identification number.
# I note: We will now use the API again to get information about the launches using the IDs given for each launch. Specifically we will be using columns <code>rocket</code>, <code>payloads</code>, <code>launchpad</code>, and <code>cores</code>.

# Lets take a subset of our dataframe keeping only the features we want
# and the flight number, and date_utc.
data = data[['rocket',
             'payloads',
             'launchpad',
             'cores',
             'flight_number',
             'date_utc']]

# We will remove rows with multiple cores
# because those are falcon rockets with 2 extra rocket boosters 
# and rows that have multiple payloads in a single rocket.
data = data[data['cores'].map(len) == 1]
data = data[data['payloads'].map(len) == 1]

# Since payloads and cores are lists of size 1 
# we will also extract the single value in the list and replace the feature.
data['cores'] = data['cores'].map(lambda x: x[0])
data['payloads'] = data['payloads'].map(lambda x: x[0])

# We also want to convert the date_utc to a datetime datatype
# then extracting the date leaving the time
data['date'] = pd.to_datetime(data['date_utc']).dt.date

# Using the date we will restrict the dates of the launches
data = data[data['date'] <= datetime.date(2020, 11, 13)]

# I note: From the <code>rocket</code> we would like to learn the booster name
# I note: From the <code>payload</code> we would like to learn the mass of the payload and the orbit that it is going to
# I note: From the <code>launchpad</code> we would like to know the name of the launch site being used, the longitude, and the latitude.
# I note: **From <code>cores</code> we would like to learn the outcome of the landing, the type of the landing, number of flights with that core, whether gridfins were used, whether the core is reused, whether legs were used, the landing pad used, the block of the core which is a number used to seperate version of cores, the number of times this specific core has been reused, and the serial of the core.**
# I note that the data from these requests will be stored in lists and will be used to create a new dataframe.

# #Global variables
# BoosterVersion = []
# PayloadMass = []
# Orbit = []
# LaunchSite = []
# Outcome = []
# Flights = []
# GridFins = []
# Reused = []
# Legs = []
# LandingPad = []
# Block = []
# ReusedCount = []
# Serial = []
# Longitude = []
# Latitude = []

BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []


getBoosterVersion(data)
getLaunchSite(data)
getPayloadData(data)
getCoreData(data)

# I note that these functions will apply the outputs globally to the above variables. Let's take a looks at <code>BoosterVersion</code> variable. Before we apply  <code>getBoosterVersion</code> the list is empty:

print(BoosterVersion)

# I note: Now, let's apply <code> getBoosterVersion</code> function method to get the booster version

# Call getBoosterVersion
getBoosterVersion(data)

# I note that the list has now been update

BoosterVersion[0:5]

# I note: we can apply the rest of the  functions here:

# Call getLaunchSite
getLaunchSite(data)

# Call getPayloadData
getPayloadData(data)

# Call getCoreData
getCoreData(data)

# I note: Finally lets construct our dataset using the data we have obtained. We we combine the columns into a dictionary.

launch_dict = {
                'BoosterVersion': BoosterVersion, 'PayloadMass': PayloadMass,
                'Orbit': Orbit,
                'LaunchSite': LaunchSite,
                'Outcome': Outcome,
                'Flights': Flights,
                'GridFins': GridFins,
                'Reused': Reused,
                'Legs': Legs,
                'LandingPad': LandingPad,
                'Block': Block,
                'ReusedCount': ReusedCount,
                'Serial': Serial,
                'Longitude': Longitude,
                'Latitude': Latitude
              }


launch_df = pd.DataFrame(launch_dict)

data_falcon9 = launch_df[launch_df['BoosterVersion'] != 'Falcon 1'].copy()
data_falcon9.shape, data_falcon9['BoosterVersion'].value_counts().head()


# I note: Then, we need to create a Pandas data frame from the dictionary launch_dict.

# Create a data from launch_dict
launch_df = pd.DataFrame(launch_dict)

# I note: Show the summary of the dataframe

# Show the head of the dataframe
launch_df.head(5)

# I note: Finally we will remove the Falcon 1 launches keeping only the Falcon 9 launches. Filter the data dataframe using the <code>BoosterVersion</code> column to only keep the Falcon 9 launches. Save the filtered data to a new dataframe called <code>data_falcon9</code>.

# Hint data['BoosterVersion']!='Falcon 1'
data_falcon9 = launch_df[launch_df['BoosterVersion'] != 'Falcon 1'].copy()
data_falcon9.head()

# I note: Now that we have removed some values we should reset the FlgihtNumber column

data_falcon9.loc[:, 'FlightNumber'] = list(range(1, data_falcon9.shape[0]+1))
data_falcon9

# I note: Data Wrangling

# I note: We can see below that some of the rows are missing values in our dataset.

data_falcon9.isnull().sum()

# I note: Before we can continue we must deal with these missing values. The <code>LandingPad</code> column will retain None values to represent when landing pads were not used.

# I note: Calculate below the mean for the <code>PayloadMass</code> using the <code>.mean()</code>. Then use the mean and the <code>.replace()</code> function to replace np.nan values in the data with the mean you calculated.

# # Calculate the mean value of PayloadMass column
# payloadMass_mean = data_falcon9.PayloadMass.mean()


# # Replace the np.nan values with its mean value
# data_falcon9.PayloadMass.fillna(payloadMass_mean)

# Calculate the mean payload mass (ignoring NaNs by default)
payload_mean = data_falcon9['PayloadMass'].mean()

# Replace NaN payload masses with the mean
data_falcon9['PayloadMass'] = data_falcon9['PayloadMass'].replace(np.nan, payload_mean)

# Quick check
data_falcon9['PayloadMass'].isnull().sum(), payload_mean

# I note: You should see the number of missing values of the <code>PayLoadMass</code> change to zero.

# I note: Now we should have no missing values in our dataset except for in <code>LandingPad</code>.

# I note: We can now export it to a <b>CSV</b> for the next section,but to make the answers consistent, in the next lab we will provide data in a pre-selected date range.

# I note: data_falcon9.to_csv('dataset_part_1.csv', index=False)

data_falcon9.to_csv('dataset_part_1.csv', index=False)

# I note: Authors

# I note: Joseph Santarcangelo has a PhD in Electrical Engineering, his research focused on using machine learning, signal processing, and computer vision to determine how videos impact human cognition. Joseph has been working for IBM since he completed his PhD.

# I note: <!--## Change Log
# I note: -->

# I note: <!--
# I note: |Date (YYYY-MM-DD)|Version|Changed By|Change Description|
# I note: |-|-|-|-|
# I note: |2020-09-20|1.1|Joseph|get result each time you run|
# I note: |2020-09-20|1.1|Azim |Created Part 1 Lab using SpaceX API|
# I note: |2020-09-20|1.0|Joseph |Modified Multiple Areas|
# I note: -->

# I note: Copyright ©IBM Corporation. All rights reserved.
