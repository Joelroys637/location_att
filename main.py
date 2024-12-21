import streamlit as st
import geocoder
from geopy.geocoders import Nominatim

def get_current_location():
    try:
        # Get current latitude and longitude
        location = geocoder.ip('me')
        latitude = location.latlng[0]
        longitude = location.latlng[1]
        
        # Reverse geocode the location to get the address
        geolocator = Nominatim(user_agent="location_finder")
        address = geolocator.reverse((latitude, longitude), language='en')
        
        return {
            "latitude": latitude,
            "longitude": longitude,
            "address": address.address if address else "Address not found"
        }
    except Exception as e:
        return {"error": str(e)}

# Streamlit App
st.title("Find My Current Location")

# Button to fetch location
if st.button("Get Current Location"):
    with st.spinner("Fetching location..."):
        location_details = get_current_location()
        if "error" in location_details:
            st.error(f"Error: {location_details['error']}")
        else:
            st.success("Location fetched successfully!")
            st.write(f"**Latitude:** {location_details['latitude']}")
            st.write(f"**Longitude:** {location_details['longitude']}")
            st.write(f"**Address:** {location_details['address']}")
