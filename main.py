import streamlit as st
from streamlit.components.v1 import html

# JavaScript to fetch the user's location
GEOLOCATION_SCRIPT = """
<script>
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        document.getElementById("data").innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    document.getElementById("data").innerHTML = lat + "," + lon;
}

function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            document.getElementById("data").innerHTML = "User denied the request for Geolocation.";
            break;
        case error.POSITION_UNAVAILABLE:
            document.getElementById("data").innerHTML = "Location information is unavailable.";
            break;
        case error.TIMEOUT:
            document.getElementById("data").innerHTML = "The request to get user location timed out.";
            break;
        case error.UNKNOWN_ERROR:
            document.getElementById("data").innerHTML = "An unknown error occurred.";
            break;
    }
}
getLocation();
</script>
<div id="data">Fetching location...</div>
"""

st.title("Location-based Attendance System")

# Render the geolocation script
result = html(GEOLOCATION_SCRIPT, height=300)

# Extract the location data
if "latitude" not in st.session_state:
    st.session_state.latitude = None
    st.session_state.longitude = None

if "Fetching location..." not in result and "," in result:
    try:
        latitude, longitude = map(float, result.split(","))
        st.session_state.latitude = latitude
        st.session_state.longitude = longitude
    except ValueError:
        st.error("Failed to parse GPS coordinates.")

# Display the coordinates
latitude = st.session_state.latitude
longitude = st.session_state.longitude

if latitude and longitude:
    st.success(f"Your location is: Latitude = {latitude}, Longitude = {longitude}")
else:
    st.warning("Please allow GPS access to fetch your location.")

if st.button("Mark Attendance"):
    # Preset location
    preset_lat = 11.172543682434414
    preset_lon = 78.95127871338087

    # Compare the fetched location with the preset location
    tolerance = 0.0005
    if latitude and longitude:
        if abs(latitude - preset_lat) < tolerance and abs(longitude - preset_lon) < tolerance:
            st.success("Attendance marked successfully!")
        else:
            st.error(f"You are not in the correct location. Your location: {latitude}, {longitude}")
    else:
        st.error("Unable to fetch your location. Please try again.")
