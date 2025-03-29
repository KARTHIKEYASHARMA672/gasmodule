import streamlit as st
import requests
import pandas as pd

# ThingSpeak API Details
THINGSPEAK_CHANNEL_ID = "2841812"  # Replace with your ThingSpeak Channel ID
THINGSPEAK_API_KEY = "6WCGKOYH3N875K6P"   # Replace with your ThingSpeak Read API Key
THINGSPEAK_URL = "https://api.thingspeak.com/channels/2897716/feeds.json?api_key=5U8VB0UD2P19JNA5&results=2"

# Streamlit Web App
st.set_page_config(page_title="IoT Dashboard", layout="wide")

st.title("📡 IoT Monitoring Dashboard")
st.write("Live data from Gas, Temperature, and Humidity sensors!")

# Fetch Data from ThingSpeak
response = requests.get(THINGSPEAK_URL)
if response.status_code == 200:
    data = response.json()
    feeds = data["feeds"]
    
    if feeds:
        # Convert Data to DataFrame
        df = pd.DataFrame(feeds)
        df["created_at"] = pd.to_datetime(df["created_at"])
        df = df.rename(columns={
            "field1": "Temperature (°C)",
            "field2": "Humidity (%)",
            "field3": "Gas Level"
        })
        df = df[["created_at", "Temperature (°C)", "Humidity (%)", "Gas Level"]]
        
        # Show Data
        st.dataframe(df, use_container_width=True)

        # Display Latest Readings
        latest = df.iloc[-1]
        col1, col2, col3 = st.columns(3)
        col1.metric("🌡 Temperature", f"{latest['Temperature (°C)']} °C")
        col2.metric("💧 Humidity", f"{latest['Humidity (%)']} %")
        col3.metric("🔥 Gas Level", f"{latest['Gas Level']}")

        # Line Charts
        st.subheader("📊 Sensor Readings Over Time")
        st.line_chart(df.set_index("created_at"))

    else:
        st.warning("No data available yet!")
else:
    st.error("Failed to fetch data from ThingSpeak!")

