import streamlit as st
from streamlit.components.v1 import html

# JavaScript for fetching the user's location and sending it to Streamlit
GEOLOCATION_SCRIPT = """
<script>
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                // Send latitude and longitude to Streamlit using query params
                window.parent.postMessage({ latitude: lat, longitude: lon }, "*");
            },
            (error) => {
                window.parent.postMessage({ error: error.message }, "*");
            }
        );
    } else {
        window.parent.postMessage({ error: "Geolocation is not supported by this browser." }, "*");
    }
}

getLocation();
</script>
<div>Fetching location...</div>
"""

st.title("Location-based Attendance System")

# Set up a placeholder for displaying location
placeholder = st.empty()

# Create a placeholder for latitude and longitude in session state
if "latitude" not in st.session_state:
    st.session_state["latitude"] = None
if "longitude" not in st.session_state:
    st.session_state["longitude"] = None

# Display the JavaScript component
html(GEOLOCATION_SCRIPT, height=300)

# Check for user location
if st.session_state["latitude"] and st.session_state["longitude"]:
    st.success(
        f"Your location is: Latitude = {st.session_state['latitude']}, Longitude = {st.session_state['longitude']}"
    )
else:
    st.warning("Waiting for your location...")

# Attendance button logic
if st.button("Mark Attendance"):
    preset_lat = 11.172543682434414
    preset_lon = 78.95127871338087
    tolerance = 0.0005  # Define tolerance for location matching

    lat = st.session_state.get("latitude")
    lon = st.session_state.get("longitude")

    if lat is not None and lon is not None:
        if abs(lat - preset_lat) < tolerance and abs(lon - preset_lon) < tolerance:
            st.success("Attendance marked successfully!")
        else:
            st.error(f"Your location does not match. Latitude: {lat}, Longitude: {lon}")
    else:
        st.error("Unable to fetch your location. Please try again.")

# JavaScript communication to update Streamlit session state
st.write(
    """
    <script>
    window.addEventListener("message", (event) => {
        const data = event.data;
        if (data.latitude && data.longitude) {
            // Update Streamlit session state with latitude and longitude
            const streamlit = window.parent.streamlit;
            streamlit.setComponentValue(JSON.stringify({ latitude: data.latitude, longitude: data.longitude }));
        } else if (data.error) {
            console.error(data.error);
        }
    });
    </script>
    """,
    unsafe_allow_html=True,
)
