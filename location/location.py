import geocoder #type: ignore

def get_current_location():
    # Getting current location using geocoder
    g = geocoder.ip('me')  # This will fetch location based on your IP address
    if g.ok:
        return f"Latitude: {g.latlng[0]}, Longitude: {g.latlng[1]}"
    else:
        return "Unable to get location."

# Call the function and print the location
location = get_current_location()
print(f"Your current location is: {location}")

