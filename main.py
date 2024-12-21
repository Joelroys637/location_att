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

# JavaScript to fetch geolocation
st.markdown("""
    <script>
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            document.getElementById("latitude").value = latitude;
            document.getElementById("longitude").value = longitude;
            document.getElementById("location-form").dispatchEvent(new Event("submit", { cancelable: true, bubbles: true }));
        },
        (error) => {
            const errorMessage = `Error: ${error.message}`;
            document.getElementById("error").value = errorMessage;
            document.getElementById("error-form").dispatchEvent(new Event("submit", { cancelable: true, bubbles: true }));
        }
    );
    </script>
    <form id="location-form" method="post">
        <input id="latitude" name="latitude" type="hidden" />
        <input id="longitude" name="longitude" type="hidden" />
    </form>
    <form id="error-form" method="post">
        <input id="error" name="error" type="hidden" />
    </form>
""", unsafe_allow_html=True)

# Get location or error from query params
latitude = st.query_params.get("latitude", [None])[0]
longitude = st.query_params.get("longitude", [None])[0]
error = st.query_params.get("error", [None])[0]

if error:
    st.error(error)
elif latitude and longitude:
    # Convert string to float
    latitude = float(latitude)
    longitude = float(longitude)

    # Display coordinates
    st.success(f"Latitude: {latitude}")
    st.success(f"Longitude: {longitude}")

    # Get and display address
    address = get_address_from_coordinates(latitude, longitude)
    st.write(f"**Address:** {address}")
else:
    st.info("Allow location access in your browser for this app to fetch your current location automatically.")
