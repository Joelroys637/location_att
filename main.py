import streamlit as st
from geopy.geocoders import Nominatim

# Function to reverse geocode
def get_address_from_coordinates(latitude, longitude):
    try:
        geolocator = Nominatim(user_agent="location_finder")
        location = geolocator.reverse((latitude, longitude), language='en')
        return location.address if location else "Address not found"
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app
st.title("Get Your Current Location")

# Add a button to capture location
st.write("Click the button below to get your current location.")
location = st.experimental_data_editor({
    "latitude": None,
    "longitude": None,
    "address": "Waiting for input..."
}, editable=False)


# Add JavaScript to get location
st.markdown("""
    <script>
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const latitude = position.coords.lat 

      </code>`
