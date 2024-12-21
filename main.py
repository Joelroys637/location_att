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

# JavaScript to fetch the geolocation
st.markdown("""
    <script>
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            document.getElementById("latitude").value = latitude;
            document.getElementById("longitude").value = longitude;
            document.getElementById("form").dispatchEvent(new Event("submit", { cancelable: true, bubbles: true }));
        }
    );
    </script>
    <form id="form" method="post">
        <input id="latitude" name="latitude" type="text" />
        <input id="longitude" name="longitude" type="text" />
    </form>
""", unsafe_allow_html=True)

# Fetch latitude and longitude from the form
latitude = st.experimental_get_query_params().get("latitude", [None])[0]
longitude = st.experimental_get_query_params().get("longitude", [None])[0]

if latitude and longitude:
    # Display coordinates
    st.success(f"Latitude: {latitude}")
    st.success(f"Longitude: {longitude}")

    # Get and display address
    address = get_address_from_coordinates(latitude, longitude)
    st.write(f"**Address:** {address}")
else:
    st.write("Click the button in the popup to allow location access.")
