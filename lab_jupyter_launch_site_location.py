"""
Converted from lab_jupyter_launch_site_location.ipynb.html.
I run this notebook as a regular Python script outside Jupyter.
"""

# I note: **Hands-on Lab: Interactive Visual Analytics with Folium**

# I note that the launch success rate may depend on many factors such as payload mass, orbit type, and so on. It may also depend on the location and proximities of a launch site, i.e., the initial position of rocket trajectories. Finding an optimal location for building a launch site certainly involves many factors and hopefully we could discover some of the factors by analyzing the existing launch site locations.

# I note: In the previous exploratory data analysis labs, you have visualized the SpaceX launch dataset using matplotlib and seaborn and discovered some preliminary correlations between the launch site and success rates. In this lab, you will be performing more interactive visual analytics using Folium.

# I note that this lab contains the following tasks:
# I note: **TASK 1:** Mark all launch sites on a map
# I note: **TASK 2:** Mark the success/failed launches for each site on the map
# I note: **TASK 3:** Calculate the distances between a launch site to its proximities
# I note: After completed the above tasks, you should be able to find some geographical patterns about launch sites.

# I used piplite in the notebook environment, but I do not need it in a regular Python script.
# I skipped piplite.install(['folium'])
# I skipped piplite.install(['pandas'])

import folium
import pandas as pd

# Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
# Import folium MousePosition plugin
from folium.plugins import MousePosition
# Import folium DivIcon plugin
from folium.features import DivIcon

# I note: If you need to refresh your memory about folium, you may download and refer to this previous folium lab:

# I note: Generating Maps with Python

## Task 1: Mark all launch sites on a map

# I note: First, let's try to add each site's location on a map using site's latitude and longitude coordinates

# I note that the following dataset with the name spacex_launch_geo.csv is an augmented dataset with latitude and longitude added for each site.

# Download and read the `spacex_launch_geo.csv`
import requests
# I load the CSV with requests in the script version.

URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
resp = requests.get(URL, timeout=30)
resp.raise_for_status()
from io import StringIO
spacex_csv_file = StringIO(resp.text)
spacex_df=pd.read_csv(spacex_csv_file)

# I note: Now, you can take a look at what are the coordinates for each site.

# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
launch_sites_df

# I note: Above coordinates are just plain numbers that can not give you any intuitive insights about where are those launch sites. If you are very good at geography, you can interpret those numbers directly in your mind. If not, that's fine too. Let's visualize those locations by pinning them on a map.

# I note: We first need to create a folium Map object, with an initial center location to be NASA Johnson Space Center at Houston, Texas.

# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

# I note: We could use folium.Circle to add a highlighted circle area with a text label on a specific coordinate. For example,

# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,
    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)

# I note: and you should find a small yellow circle near the city of Houston and you can zoom-in to see a larger circle.

# I note: Now, let's add a circle for each launch site in data frame launch_sites

# I note: *TODO:*  Create and add folium.Circle and folium.Marker for each launch site on the site map

# I note that an example of folium.Circle:

# I note: folium.Circle(coordinate, radius=1000, color='#000000', fill=True).add_child(folium.Popup(...))

# I note that an example of folium.Marker:

# I note: folium.map.Marker(coordinate, icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0), html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'label', ))

# Initial the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)
# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label

# I note that the generated map with marked launch sites should look similar to the following:

# I note: Now, you can explore the map by zoom-in/out the marked areas
# I note: , and try to answer the following questions:
# I note: Are all launch sites in proximity to the Equator line?
# I note: Are all launch sites in very close proximity to the coast?
# I note: Also please try to explain your findings.

# Task 2: Mark the success/failed launches for each site on the map
# Initial the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)

# Add a circle + text label for each launch site
for _, row in launch_sites_df.iterrows():
    coordinate = [row['Lat'], row['Long']]
    launch_site_name = row['Launch Site']
    
    # Circle with popup
    folium.Circle(
        coordinate,
        radius=1000,
        color='#000000',
        fill=True
    ).add_child(folium.Popup(launch_site_name)).add_to(site_map)
    
    # Text label marker
    folium.map.Marker(
        coordinate,
        icon=DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 12; color:#d35400;"><b>{launch_site_name}</b></div>'
        )
    ).add_to(site_map)

site_map

# I note: Next, let's try to enhance the map by adding the launch outcomes for each site, and see which sites have high success rates.
# I note: Recall that data frame spacex_df has detailed launch records, and the class column indicates if this launch was successful or not

spacex_df.tail(10)

# I note: Next, let's create markers for all launch records.
# I note: If a launch was successful (class=1), then we use a green marker and if a launch was failed, we use a red marker (class=0)

# I note: Note that a launch only happens in one of the four launch sites, which means many launch records will have the exact same coordinate. Marker clusters can be a good way to simplify a map containing many markers having the same coordinate.

marker_cluster = MarkerCluster()

# I note: *TODO:* Create a new column in spacex_df dataframe called marker_color to store the marker colors based on the class value


# Apply a function to check the value of `class` column
# If class=1, marker_color value will be green
# If class=0, marker_color value will be red
spacex_df['marker_color'] = spacex_df['class'].apply(lambda x: 'green' if x == 1 else 'red')

# I note: *TODO:* For each launch result in spacex_df data frame, add a folium.Marker to marker_cluster

# # Add marker_cluster to current site_map
# site_map.add_child(marker_cluster)

# # for each row in spacex_df data frame
# # create a Marker object with its coordinate
# # and customize the Marker's icon property to indicate if this launch was successed or failed, 
# # e.g., icon=folium.Icon(color='white', icon_color=row['marker_color']
# for index, record in spacex_df.iterrows():
#     # TODO: Create and add a Marker cluster to the site map
#     # marker = folium.Marker(...)
#     marker_cluster.add_child(marker)

# site_map

# Add marker_cluster to current site_map
site_map.add_child(marker_cluster)

for _, record in spacex_df.iterrows():
    marker = folium.Marker(
        location=[record['Lat'], record['Long']],
        popup=record['Launch Site'],
        icon=folium.Icon(color='white', icon_color=record['marker_color'])
    )
    marker_cluster.add_child(marker)

site_map

# I note: Your updated map may look like the following screenshots:

# I note: From the color-labeled markers in marker clusters, you should be able to easily identify which launch sites have relatively high success rates.

# TASK 3: Calculate the distances between a launch site to its proximities
import math

# Haversine distance (km)
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlmb/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Pick a launch site (commonly used in the lab)
launch_site = 'CCAFS LC-40'
site_lat = launch_sites_df.loc[launch_sites_df['Launch Site'] == launch_site, 'Lat'].values[0]
site_lon = launch_sites_df.loc[launch_sites_df['Launch Site'] == launch_site, 'Long'].values[0]
launch_coord = [site_lat, site_lon]

# TODO: replace these with the coordinates you identify on the map
coastline_coord = [0, 0]
highway_coord   = [0, 0]
railway_coord   = [0, 0]
city_coord      = [0, 0]

# Add distance markers + lines
for name, coord in [
    ('Coastline', coastline_coord),
    ('Highway', highway_coord),
    ('Railway', railway_coord),
    ('City', city_coord),
]:
    dist_km = calculate_distance(launch_coord[0], launch_coord[1], coord[0], coord[1])

    folium.Marker(
        coord,
        icon=DivIcon(
            icon_size=(250, 20),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 12px; color:#000000;"><b>{name}: {dist_km:.2f} km</b></div>'
        )
    ).add_to(site_map)

    folium.PolyLine([launch_coord, coord], color='blue', weight=2).add_to(site_map)

site_map

# I note: Next, we need to explore and analyze the proximities of launch sites.

# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)

site_map.add_child(mouse_position)
site_map

# I note: Now zoom in to a launch site and explore its proximity to see if you can easily find any railway, highway, coastline, etc. Move your mouse to these points and mark down their coordinates (shown on the top-left) in order to the distance to the launch site.

# I note: Now zoom in to a launch site and explore its proximity to see if you can easily find any railway, highway, coastline, etc. Move your mouse to these points and mark down their coordinates (shown on the top-left) in order to the distance to the launch site.

from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# I note: *TODO:* Mark down a point on the closest coastline using MousePosition and calculate the distance between the coastline point and the launch site.

# find coordinate of the closet coastline
# e.g.,: Lat: 28.56367  Lon: -80.57163
# distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)
# 1) Pick a launch site (example: CCAFS LC-40). Change if you’re using a different site.
launch_site = 'CCAFS LC-40'
launch_site_lat = launch_sites_df.loc[launch_sites_df['Launch Site'] == launch_site, 'Lat'].values[0]
launch_site_lon = launch_sites_df.loc[launch_sites_df['Launch Site'] == launch_site, 'Long'].values[0]

# 2) After you mouse-hover the closest coastline point, paste its coordinates here:
coastline_lat = 28.56367
coastline_lon = -80.57163

# 3) Compute distance (km)
distance_coastline = calculate_distance(
    launch_site_lat, launch_site_lon,
    coastline_lat, coastline_lon
)

distance_coastline

# Create and add a folium.Marker on your selected closest coastline point on the map
# Display the distance between coastline point and launch site using the icon property 
# for example
# distance_marker = folium.Marker(
#    coordinate,
#    icon=DivIcon(
#        icon_size=(20,20),
#        icon_anchor=(0,0),
#        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance),
#        )
#    )
# Coordinate of the closest coastline point (replace with your MousePosition values)
coastline_coordinate = [coastline_lat, coastline_lon]

# Distance (km) already computed as distance_coastline
distance_marker = folium.Marker(
    coastline_coordinate,
    icon=DivIcon(
        icon_size=(200, 20),
        icon_anchor=(0, 0),
        html='<div style="font-size: 12px; color:#d35400;"><b>%s</b></div>' 
             # I skipped this notebook magic command: % "{:10.2f} KM".format(distance_coastline),
    )
)

site_map.add_child(distance_marker)
site_map

# I note: *TODO:* Draw a PolyLine between a launch site to the selected coastline point

# Create a `folium.PolyLine` object using the coastline coordinates and launch site coordinate
# lines=folium.PolyLine(locations=coordinates, weight=1)
coordinates = [
    [launch_site_lat, launch_site_lon],
    [coastline_lat, coastline_lon]
]

lines = folium.PolyLine(locations=coordinates, weight=1)

site_map.add_child(lines)
site_map

# I note: Your updated map with distance line should look like the following screenshot:

# I note: *TODO:* Similarly, you can draw a line betwee a launch site to its closest city, railway, highway, etc. You need to use MousePosition to find the their coordinates on the map first

# I note that a railway map symbol may look like this:

# I note that a highway map symbol may look like this:

# I note that a city map symbol may look like this:

# Create a marker with distance to a closest city, railway, highway, etc.
# Draw a line between the marker to the launch site
# ---- 1) Paste the coordinates you read from MousePosition here ----
city_lat, city_lon       = 28.4, -80.6
railway_lat, railway_lon = 28.6, -80.6
highway_lat, highway_lon = 28.6, -80.6

# ---- 2) Helper to add a distance label marker + line to the launch site ----
def add_distance_marker_and_line(name, lat, lon, color='blue'):
    dist = calculate_distance(launch_site_lat, launch_site_lon, lat, lon)

    # distance label marker
    folium.Marker(
        [lat, lon],
        icon=DivIcon(
            icon_size=(250, 20),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 12px; color:#d35400;"><b>{name}: {dist:10.2f} KM</b></div>'
        )
    ).add_to(site_map)

    # line from launch site -> point
    folium.PolyLine(
        locations=[[launch_site_lat, launch_site_lon], [lat, lon]],
        weight=1,
        color=color
    ).add_to(site_map)

# ---- 3) Add city / railway / highway (once you fill in coordinates) ----
add_distance_marker_and_line("Closest city", city_lat, city_lon)
add_distance_marker_and_line("Closest railway", railway_lat, railway_lon)
add_distance_marker_and_line("Closest highway", highway_lat, highway_lon)

site_map

# I note: After you plot distance lines to the proximities, you can answer the following questions easily:
# I note: Are launch sites in close proximity to railways?
# I note: Are launch sites in close proximity to highways?
# I note: Are launch sites in close proximity to coastline?
# I note: Do launch sites keep certain distance away from cities?
# I note: Also please try to explain your findings.

# I note: Next Steps:
# I note: Now you have discovered many interesting insights related to the launch sites' location using folium, in a very interactive way. Next, you will need to build a dashboard using Ploty Dash on detailed launch records.

# I note: Authors

# I note: Pratiksha Verma

# I note: <!--## Change Log--!>

# I note: <!--| Date (YYYY-MM-DD) | Version | Changed By      | Change Description      |
# I note: | ----------------- | ------- | -------------   | ----------------------- |
# I note: | 2022-11-09        | 1.0     | Pratiksha Verma | Converted initial version to Jupyterlite|--!>

# I note: <h3 align="center"> IBM Corporation 2022. All rights reserved. <h3/>
