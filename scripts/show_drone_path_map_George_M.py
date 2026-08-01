import folium
import random
import math
import time
from folium.elements import Element

def generate_new_point(initial_lat, initial_lon, distance_km, bearing_deg):
    """
    Generates a new latitude and longitude given a starting point, 
    distance, and bearing.

    :param initial_lat: Starting latitude in degrees.
    :param initial_lon: Starting longitude in degrees.
    :param distance_km: Distance to travel in kilometers.
    :param bearing_deg: Bearing (direction) in degrees, clockwise from North.
    :return: A tuple (new_lat, new_lon) in degrees.
    """
    # Earth's radius in kilometers
    R = 6378.1 #

    # Convert degrees to radians
    lat1 = math.radians(initial_lat)
    lon1 = math.radians(initial_lon)
    bearing_rad = math.radians(bearing_deg)
    
    # Angular distance
    angular_distance = distance_km / R

    # Calculate new latitude
    lat2 = math.asin(math.sin(lat1) * math.cos(angular_distance) +
                    math.cos(lat1) * math.sin(angular_distance) * math.cos(bearing_rad))
    
    # Calculate new longitude
    lon2 = lon1 + math.atan2(math.sin(bearing_rad) * math.sin(angular_distance) * math.cos(lat1),
                             math.cos(angular_distance) - math.sin(lat1) * math.sin(lat2))
    
    # Convert radians back to degrees
    new_lat = math.degrees(lat2)
    new_lon = math.degrees(lon2)
    
    return (new_lat, new_lon)

line1_coordinates = [
]

inv_coordinates = [
]

#Hardcoded invasives detected list.
invasive_species_list = [
    "Chinese Privet",
    "Chinese Privet",
    "Chinese Privet",
    "Chinese Privet",
    "Chinese Privet",
    "Chinese Privet",


    "Chinese Tallow",
    "Chinese Tallow",
    "Chinese Tallow",
    "Chinese Tallow",
    "Chinese Tallow",
    "Chinese Tallow",
    "Chinese Tallow",
    "Chinese Tallow",



    "Japanese Climbing Fern",
    "Japanese Climbing Fern",
    "Japanese Climbing Fern",
    "Japanese Climbing Fern",
    "Japanese Climbing Fern",
    "Japanese Climbing Fern"
]

detected_species = {"Chinese Tallow":3, "Chinese Privet":3, "Japanese Climbing Fern":3, "Japanese Honeysuckle":2, "Kudzu":3}

#30.17277, -95.54574

start_lat = 30.17277
start_lon = -95.54574

distance = 0.0015       # Distance in km

latitude = start_lat
longitude = start_lon
bearing = 0

invasive_count = 0 

for a in range(1,100):    
    if a % 25 == 0:
        bearing += 90

    new_coordinates = generate_new_point(latitude, longitude, distance, bearing)
    latitude = new_coordinates[0]
    longitude = new_coordinates[1]
    line1_coordinates.append([latitude, longitude])
           
    if a <= len(invasive_species_list):
        new_coordinates = generate_new_point(start_lat, start_lon, random.uniform(distance*2,distance*20), random.randint(0, 90))
        invasive_count += 1
        inv_coordinates.append(new_coordinates)        

    # Create a map centered at a specific location
    m1 = folium.Map(location=[start_lat, start_lon], zoom_start=19)
    m2 = folium.Map(location=[start_lat, start_lon], zoom_start=19)

    # Add start and end markers
    folium.Marker(
        location=line1_coordinates[0],
        popup='Start',
        icon=folium.Icon(color='green', icon='play', prefix='fa')
    ).add_to(m1)

    folium.Marker(
        location=line1_coordinates[-1],
        popup='End',
        icon=folium.Icon(color='red', icon='stop', prefix='fa')
    ).add_to(m1)

    folium.Marker(
        location=line1_coordinates[0],
        popup='Start',
        icon=folium.Icon(color='green', icon='play', prefix='fa')
    ).add_to(m2)

    folium.Marker(
        location=line1_coordinates[-1],
        popup='End',
        icon=folium.Icon(color='red', icon='stop', prefix='fa')
    ).add_to(m2)

    risk_score = 0
    for x in range(len(inv_coordinates)):
        if detected_species[invasive_species_list[x]] == 3:
            inv_m = folium.Marker(icon=folium.Icon(color='red', icon='3', prefix='fa'), location=inv_coordinates[x],tooltip=invasive_species_list[x]).add_to(m1)
        elif detected_species[invasive_species_list[x]] == 2:
            inv_m = folium.Marker(icon=folium.Icon(color='orange', icon='2', prefix='fa'), location=inv_coordinates[x],tooltip=invasive_species_list[x]).add_to(m1)

        risk_score += detected_species[invasive_species_list[x]]
    line1 = None
    # Add a marker to the map
    if risk_score >= 40:
        line1 = folium.PolyLine(locations=line1_coordinates, color='red', weight=5, opacity=0.8)
    elif 25 <= risk_score < 40:
        line1 = folium.PolyLine(locations=line1_coordinates, color='orange', weight=5, opacity=0.8)
    else:
        line1 = folium.PolyLine(locations=line1_coordinates, color='darkgreen', weight=5, opacity=0.8)
    line1.add_to(m1)

    for x in range(len(inv_coordinates)):
        inv_m = folium.Marker(location=inv_coordinates[x],tooltip=invasive_species_list[x]).add_to(m2)
    line1 = None
    line1 = folium.PolyLine(locations=line1_coordinates, color='blue', weight=5, opacity=0.8)
    line1.add_to(m2)

    # Display the map
    m1.save("C:\\Venky\\invasive_species_detection\\drone_path\\drone_path_George_M.html")
    m2.save("C:\\Venky\\invasive_species_detection\\drone_path\\drone_path_George_M_orig.html")