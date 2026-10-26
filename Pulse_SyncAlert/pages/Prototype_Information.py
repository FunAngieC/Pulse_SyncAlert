import streamlit
import sqlite3
import pandas
import statistics
import plotly.graph_objects as go


streamlit.set_page_config(page_title="Pulse SyncAlert", page_icon="❤️")
streamlit.title("About Pulse SyncAlert 💓")


streamlit.subheader("Prototype Information: ")
col1, col2 = streamlit.columns(2)
with col1:
    streamlit.metric("Microcontroller", "Arduino Nano ESP32")
    streamlit.metric("Sensor", "MAX30102")
    streamlit.metric("AI Model", "Isolation Forest")
with col2:
    streamlit.metric("Signal", "BPM")
    streamlit.metric("Database", "SQLite")
    streamlit.metric("Cost", "$34.89")



streamlit.subheader("How Pulse SyncAlert works:")
streamlit.markdown("**1. Sensor** — Arduino Nano ESP32 + MAX30102 optical PPG reads heart rate via fingertip infrared light absorption.")
streamlit.markdown("**2. Database** —  Every reading is stored with a timestamp in SQLite (syncalert.db), labeled by source (synthetic or arduino).")
streamlit.markdown("**3. AI model** —  Isolation Forest (scikit-learn) trains on your personal baseline and flags deviations (contamination = 0.02).")
streamlit.markdown("**4. Dashboard** —  This Streamlit app reads the database and highlights anomalies in real time.")

streamlit.markdown("")
streamlit.markdown("")
streamlit.markdown("")

streamlit.title("Built With:")
streamlit.subheader("Hardware")
streamlit.markdown("""
- MAX30102 pulse oximetry sensor
- Arduino Nano ESP32 microcontroller
- Breadboard + USB-C to Micro-USB cable
""")

streamlit.markdown("")

streamlit.subheader("Language")
streamlit.markdown("- MAX30102 pulse oximetry sensor")

streamlit.markdown("")

streamlit.subheader("Backend")
streamlit.markdown("""
- pyserial — Arduino ↔ laptop serial communication
- sqlite3 — local database storage
- threading — real-time data capture
- Gaussian distribution — synthetic training data generation
""")

streamlit.markdown("")

streamlit.subheader("AI")
streamlit.markdown("""
- scikit-learn — Isolation Forest anomaly detection
""")

streamlit.markdown("")

streamlit.subheader("Dashboard")
streamlit.markdown("""
- Streamlit — 4-tab web app
- pandas — data loading and display
- Plotly — live BPM chart with anomaly markers
""")

streamlit.markdown("")

streamlit.subheader("Development Tools")
streamlit.markdown("""
- Arduino IDE — firmware upload
- VS Code — Python development
""")