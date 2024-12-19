import folium
import requests
import geocoder #type: ignore

lat = 0
lon = 0
g = geocoder.ip('me')
if g.ok:
    lat = g.latlng[0]
    lon = g.latlng[1]
else:
    print("Unable to get location")
    exit(0)

# Step 2: Query Overpass API for Nearby Locations
def get_nearby_places(lat, lon, radius=5000):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node["amenity"="police"](around:{radius},{lat},{lon});
      node["amenity"="hospital"](around:{radius},{lat},{lon});
      node["amenity"="fire_station"](around:{radius},{lat},{lon});
    );
    out body;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    return response.json()

# Step 3: Create the Map and Add Markers
def create_map(lat, lon, places):
    map = folium.Map(location=[lat, lon], zoom_start=14)

    # Mark the current location
    folium.Marker([lat, lon], popup="Your Location", icon=folium.Icon(color="blue")).add_to(map)

    # Initialize counters
    police_count = 0
    hospital_count = 0
    fire_station_count = 0

    # Add markers for each place found
    for place in places['elements']:
        name = place.get('tags', {}).get('name', 'Unnamed')
        place_type = place.get('tags', {}).get('amenity', 'Unknown')
        place_lat = place['lat']
        place_lon = place['lon']
        
        # Increment counters based on place type
        if place_type == "police":
            police_count += 1
            color = "red"
        elif place_type == "hospital":
            hospital_count += 1
            color = "green"
        elif place_type == "fire_station":
            fire_station_count += 1
            color = "orange"
        else:
            color = "blue"

        # Add a marker for the place
        folium.Marker(
            [place_lat, place_lon],
            popup=f"{name} ({place_type})",
            icon=folium.Icon(color=color)
        ).add_to(map)

    # Add text on the map for location counts with improved positioning and styling
    folium.Marker(
        location=[lat, lon],
        popup=f"Police Stations: {police_count} Hospitals: {hospital_count} Fire Stations: {fire_station_count}",
        icon=folium.DivIcon(
            html=f"""
            <div style="font-size: 14pt; font-weight: bold; color: black; background-color: white; padding: 5px; border-radius: 5px;">
                Police: {police_count} | Hospital: {hospital_count} | Fire Stations: {fire_station_count}
            </div>
            """,
            icon_size=(150, 50),  # Size of the text box
            icon_anchor=(0, 0)     # Adjust positioning
        )
    ).add_to(map)

    return map

# Main Execution
def main():
    # Directly set the latitude and longitude here
    # lat, lon = 28.7041, 77.1025  # Example: New Delhi, India (Latitude: 28.7041, Longitude: 77.1025)
    # lat, lon = get_current_location()[0], get_current_location()[1]
    
    print(f"Current Location: Latitude {lat}, Longitude {lon}")
        
    places = get_nearby_places(lat, lon, radius=5000)
    map = create_map(lat, lon, places)

    # Save the map to an HTML file
    map.save("map/location_map.html")
    print("Map has been saved to 'location_map.html'. Open it in a browser to view.")

# Run the main function
if __name__ == "__main__":
    main()