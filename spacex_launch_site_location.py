"""
SpaceX Launch Site Location Analysis Module

I create interactive maps showing SpaceX launch sites and analyze
their proximities to geographical features like coastlines, railways,
and highways using Folium for visualization.

Author: Yaseen
"""

import folium
import pandas as pd
from folium.plugins import MarkerCluster, MousePosition
from folium.features import DivIcon
import math


LAUNCH_GEO_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv"

NASA_JSC_COORDINATE = [29.559684888503615, -95.0830971930759]


def load_launch_geo_data(url=LAUNCH_GEO_URL):
    """
    I load the SpaceX launch data with geographic coordinates.

    Args:
        url: URL to the CSV file

    Returns:
        DataFrame: Launch data with latitude and longitude
    """
    df = pd.read_csv(url)
    return df


def prepare_launch_sites(df):
    """
    I extract unique launch sites with their coordinates.

    Args:
        df: DataFrame with Launch Site, Lat, Long columns

    Returns:
        DataFrame: Unique launch sites
    """
    df = df[["Launch Site", "Lat", "Long", "class"]]
    launch_sites = df.groupby(["Launch Site"], as_index=False).first()
    launch_sites = launch_sites[["Launch Site", "Lat", "Long"]]
    return launch_sites


def create_base_map(center=NASA_JSC_COORDINATE, zoom=10):
    """
    I create a Folium map centered on a given location.

    Args:
        center: [latitude, longitude] for map center
        zoom: Initial zoom level

    Returns:
        Map: Folium map object
    """
    return folium.Map(location=center, zoom_start=zoom)


def add_launch_site_markers(site_map, launch_sites):
    """
    I add circle markers and labels for each launch site.

    Args:
        site_map: Folium map object
        launch_sites: DataFrame with Launch Site, Lat, Long
    """
    for _, row in launch_sites.iterrows():
        coordinate = [row["Lat"], row["Long"]]
        launch_site_name = row["Launch Site"]

        folium.Circle(coordinate, radius=1000, color="#000000", fill=True).add_child(
            folium.Popup(launch_site_name)
        ).add_to(site_map)

        folium.map.Marker(
            coordinate,
            icon=DivIcon(
                icon_size=(20, 20),
                icon_anchor=(0, 0),
                html=f'<div style="font-size: 12; color:#d35400;"><b>{launch_site_name}</b></div>',
            ),
        ).add_to(site_map)


def add_outcome_markers(site_map, df):
    """
    I add colored markers for each launch showing success (green)
    or failure (red) outcomes.

    Args:
        site_map: Folium map object
        df: DataFrame with Lat, Long, and class columns
    """
    df["marker_color"] = df["class"].apply(lambda x: "green" if x == 1 else "red")

    marker_cluster = MarkerCluster()

    for _, record in df.iterrows():
        marker = folium.Marker(
            location=[record["Lat"], record["Long"]],
            popup=record["Launch Site"],
            icon=folium.Icon(color="white", icon_color=record["marker_color"]),
        )
        marker_cluster.add_child(marker)

    site_map.add_child(marker_cluster)


def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """
    I calculate the great-circle distance between two points on Earth
    using the Haversine formula.

    Args:
        lat1, lon1: Coordinates of first point
        lat2, lon2: Coordinates of second point

    Returns:
        float: Distance in kilometers
    """
    R = 6371.0

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlmb / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def add_proximity_markers(
    site_map, launch_site_name, launch_sites, proximity_coords, proximity_names
):
    """
    I add distance markers and lines from a launch site to nearby
    geographical features.

    Args:
        site_map: Folium map object
        launch_site_name: Name of the launch site
        launch_sites: DataFrame with launch site coordinates
        proximity_coords: List of [lat, lon] for nearby features
        proximity_names: List of names for nearby features
    """
    site_data = launch_sites[launch_sites["Launch Site"] == launch_site_name]
    launch_lat = site_data["Lat"].values[0]
    launch_lon = site_data["Long"].values[0]
    launch_coord = [launch_lat, launch_lon]

    for name, coord in zip(proximity_names, proximity_coords):
        dist_km = calculate_haversine_distance(
            launch_coord[0], launch_coord[1], coord[0], coord[1]
        )

        folium.Marker(
            coord,
            icon=DivIcon(
                icon_size=(250, 20),
                icon_anchor=(0, 0),
                html=f'<div style="font-size: 12px; color:#d35400;"><b>{name}: {dist_km:.2f} km</b></div>',
            ),
        ).add_to(site_map)

        folium.PolyLine([launch_coord, coord], color="blue", weight=2).add_to(site_map)


def add_mouse_position(site_map):
    """
    I add a mouse position widget to the map for coordinate discovery.

    Args:
        site_map: Folium map object
    """
    formatter = "function(num) {return L.Util.formatNum(num, 5);};"
    mouse_position = MousePosition(
        position="topright",
        separator=" Long: ",
        empty_string="NaN",
        lng_first=False,
        num_digits=20,
        prefix="Lat:",
        lat_formatter=formatter,
        lng_formatter=formatter,
    )
    site_map.add_child(mouse_position)


def run_launch_site_analysis():
    """
    I orchestrate the complete launch site analysis:
    load data, create maps with markers and proximities.

    Returns:
        tuple: (site_map, launch_sites DataFrame)
    """
    df = load_launch_geo_data()
    launch_sites = prepare_launch_sites(df)

    print("=== Launch Sites ===")
    print(launch_sites)

    site_map = create_base_map()
    add_launch_site_markers(site_map, launch_sites)
    add_outcome_markers(site_map, df)

    print("\n=== Calculating Proximity Distances ===")
    launch_site = "CCAFS LC-40"
    site_lat = launch_sites.loc[
        launch_sites["Launch Site"] == launch_site, "Lat"
    ].values[0]
    site_lon = launch_sites.loc[
        launch_sites["Launch Site"] == launch_site, "Long"
    ].values[0]

    coastline_coord = [28.56367, -80.57163]
    city_coord = [28.4, -80.6]
    railway_coord = [28.6, -80.6]
    highway_coord = [28.6, -80.6]

    proximity_coords = [coastline_coord, city_coord, railway_coord, highway_coord]
    proximity_names = ["Coastline", "City", "Railway", "Highway"]

    add_proximity_markers(
        site_map, launch_site, launch_sites, proximity_coords, proximity_names
    )

    add_mouse_position(site_map)

    return site_map, launch_sites


if __name__ == "__main__":
    site_map, launch_sites = run_launch_site_analysis()
    site_map.save("launch_sites_map.html")
    print("\nMap saved to launch_sites_map.html")
