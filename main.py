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
st.title("Automatically Fetch Current Location")

# JavaScript to fetch geolocation and send it back to Streamlit
st.markdown("""
    <script>
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            document.getElementById("latitude").value = latitude;
            document.getElementById("longitude").value = longitude;
            document.getElementById("location-form").submit();
        },
        (error) => {
            document.getElementById("error-message").innerText = `Error: ${error.message}`;
        }
    );
    </script>
    <form id="location-form" method="GET">
        <input id="latitude" name="latitude" type="hidden" />
        <input id="longitude" name="longitude" type="hidden" />
    </form>
    <p id="error-message" style="color: red;"></p>
""", unsafe_allow_html=True)

# Retrieve latitude and longitude from URL parameters
latitude = st.experimental_get_query_params().get("latitude", [None])[0]
longitude = st.experimental_get_query_params().get("longitude", [None])[0]

if latitude and longitude:
    # Convert coordinates from strings to float
    latitude = float(latitude)
    longitude = float(longitude)

    # Display coordinates
    st.success(f"Latitude: {latitude}")
    st.success(f"Longitude: {longitude}")

    # Reverse geocode to get the address
    address = get_address_from_coordinates(latitude, longitude)
    st.write(f"**Address:** {address}")
else:
    st.info("Allow location access in your browser for the app to automatically fetch your current location.")
