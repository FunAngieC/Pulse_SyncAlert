import streamlit
import sqlite3
import pandas
import statistics
import plotly.graph_objects as go

streamlit.set_page_config(page_title="Pulse SyncAlert", page_icon="❤️")
streamlit.title("Understanding Supraventricular tachycardia SVT")
streamlit.markdown("***Supraventricular Tachycardia — What it is, what to watch for, and when to get help***")
streamlit.markdown("Source: American Heart Association  ·  heart.org")
streamlit.markdown("")
streamlit.markdown("")
streamlit.subheader("What is SVT?")
streamlit.markdown("**Supraventricular tachycardia (SVT)** is a fast heart rate — more than 100 beats per minute — that starts in the **atria,** the heart's upper chambers. Episodes can come and go suddenly. SVT is also called **atrial tachycardia.**")
streamlit.markdown("")
streamlit.subheader("Symptoms to watch for")
streamlit.markdown("""
An SVT episode may cause any of the following:

- Palpitations — a fluttering or pounding feeling in your chest
- A strong pulse felt in your neck
- A strong pulse felt in your neck
- Shortness of breath
- Chest discomfort or tightness
- Dizziness or lightheadedness
- Fatigue or weakness
- Sweating
- Nausea
- Fainting or near-fainting
 
""")

streamlit.markdown("")
streamlit.markdown("")

with streamlit.container(border=True):
    streamlit.subheader("⚠  IMPORTANT — SEE A DOCTOR")
    streamlit.markdown("If you experience any of the symptoms above,  especially fainting, severe chest pain, or a heart rate that will not slow down — seek medical attention right away.")
    streamlit.markdown("Do NOT try to diagnose or treat yourself based on an app or wearable device alone. Pulse SyncAlert is a monitoring tool only. It cannot diagnose SVT or any other condition.")
    streamlit.markdown("Always share your app data with your doctor, who can order the right tests and provide proper care.")


streamlit.markdown("")
streamlit.markdown("")

streamlit.subheader("Call 911 or go to the ER if you have:")
streamlit.markdown("⚠ Fainting or loss of consciousness")
streamlit.markdown("⚠ Severe chest pain lasting more than a few minutes")
streamlit.markdown("⚠ Difficulty breathing at rest")
streamlit.markdown("⚠ A heart rate that stays above 150 bpm and will not slow down")
streamlit.markdown("⚠ Sudden weakness or numbness on one side of your body")

streamlit.markdown("")
streamlit.markdown("")

streamlit.subheader("What to do next")
streamlit.markdown("""
1. **See a cardiologist.** Even if your symptoms are mild, a cardiology appointment will confirm whether you have SVT and determine the right plan for you.
2. **Keep a symptom log.** Note when episodes happen, how long they last, and any possible triggers. Bring this log — and any data from Pulse SyncAlert — to your appointment.
3. **Do not ignore recurring episodes.** If episodes are becoming more frequent or severe, contact your doctor sooner.
""")

streamlit.markdown("")
streamlit.markdown("")

with streamlit.container(border=True):
    streamlit.markdown("*Pulse SyncAlert is not a medical device. It is a data collection and personal awareness tool. Its outputs are for awareness only, not medical diagnosis. Users should consult a doctor for any health concerns. Pulse SyncAlert is designed to help patients bring better data to their doctor, not replace that conversation. It is not a substitute for evaluation by a qualified healthcare professional. Information sourced from the American Heart Association (heart.org).*")
    


