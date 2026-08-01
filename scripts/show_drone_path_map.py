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

bearing_list = [10, 20, 30, 40, 50, 60, 80, 90, 100, 110, 120, 150, 180, 190, 200, 210, 220, 230, 240, 250, 270, 290, 300, 320, 330, 360]

# Select a single random element
bearing = random.choice(bearing_list)

# cattail 30.1943126,-95.5294824
# tupelo 30.1481819,-95.5325817
start_lat = 30.1474586
start_lon = 95.5313913

distance = 0.005       # Distance in km
bearing = random.choice(bearing_list)

latitude = start_lat
longitude = start_lon

for a in range(1,100):
    bearing = random.choice(bearing_list)
    new_coordinates = generate_new_point(latitude, longitude, distance, bearing)
    latitude = new_coordinates[0]
    longitude = new_coordinates[1]
    line1_coordinates.append([latitude, longitude])

    # Create a map centered at a specific location
    m = folium.Map(location=[start_lat, start_lon], zoom_start=19)

    # Inject the meta refresh tag: refresh every 30 seconds
    refresh_interval_seconds = 3
    meta_refresh_tag = f'<meta http-equiv="refresh" content="{refresh_interval_seconds}">'
    m.get_root().header.add_child(Element(meta_refresh_tag))

    # Add a marker to the map
    line1 = folium.PolyLine(locations=line1_coordinates, color='blue', weight=5, opacity=0.8)
    line1.add_to(m)
    # Display the map
    m.save("C:\\Venky\\Invasive_Species\\invasive_species_detection\\drone_path\\drone_path.html")
    time.sleep(2)
