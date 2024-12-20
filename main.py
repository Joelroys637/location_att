import streamlit as st
import requests


def get_location():
    try:
        # Use a public API to fetch the geolocation
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        
        # Extract latitude and longitude
        location = data["loc"].split(",")
        latitude = float(location[0])
        longitude = float(location[1])
        return latitude, longitude
    except Exception as e:
        print("Error fetching location:", e)
        return None, None


def compare_coordinates(lat1, lon1, lat2, lon2, tolerance=0.0001):
    return abs(lat1 - lat2) < tolerance and abs(lon1 - lon2) < tolerance


latitude, longitude = get_location()

if latitude and longitude:
    print(f"Your location is: Latitude = {latitude}, Longitude = {longitude}")
else:
    print("Unable to fetch GPS location.")


if st.button("Click"):
    # Preset location for comparison
    lat = 11.6538
    lon = 78.1554
    
    # Check if the current location is within the tolerance of the preset location
    if compare_coordinates(lat, lon, latitude, longitude):
        st.success("Present")
    else:
        st.error("You are not in the correct location")
