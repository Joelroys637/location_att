import streamlit as st

# JavaScript for fetching user's location and sending it to Streamlit
GEOLOCATION_SCRIPT = """
<script>
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                // Send latitude and longitude to Streamlit
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
<div id="data">Fetching location...</div>
"""

st.title("Location-based Attendance System")

# JavaScript communication placeholder
coordinates_placeholder = st.empty()

# Initialize session state for latitude and longitude
if "latitude" not in st.session_state:
    st.session_state["latitude"] = None
if "longitude" not in st.session_state:
    st.session_state["longitude"] = None

# Display JavaScript to fetch location
st.components.v1.html(GEOLOCATION_SCRIPT, height=300)

# Display location details dynamically
if st.session_state["latitude"] is not None and st.session_state["longitude"] is not None:
    coordinates_placeholder.success(
        f"Your location is: Latitude = {st.session_state['latitude']}, Longitude = {st.session_state['longitude']}"
    )
else:
    coordinates_placeholder.warning("Waiting for your location...")

# Attendance button logic
if st.button("Mark Attendance"):
    preset_lat = 11.172543682434414
    preset_lon = 78.95127871338087
    tolerance = 0.0005

    lat = st.session_state.get("latitude")
    lon = st.session_state.get("longitude")

    if lat is not None and lon is not None:
        if abs(lat - preset_lat) < tolerance and abs(lon - preset_lon) < tolerance:
            st.success("Attendance marked successfully!")
        else:
            st.error(f"Your location does not match. Latitude: {lat}, Longitude: {lon}")
    else:
        st.error("Unable to fetch your location. Please try again.")

# JavaScript to Streamlit message listener
st.write(
    """
    <script>
    window.addEventListener("message", (event) => {
        const data = event.data;
        if (data.latitude && data.longitude) {
            const streamlit = window.parent.streamlit;
            streamlit.setComponentValue(JSON.stringify({ latitude: data.latitude, longitude: data.longitude }));
        }
    });
    </script>
    """,
    unsafe_allow_html=True,
)
