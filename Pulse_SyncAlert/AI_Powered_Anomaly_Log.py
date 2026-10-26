import streamlit
import sqlite3
import pandas
import statistics
import os

# Absolute path — same folder as this file
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "synthetic_database.db")

streamlit.set_page_config(page_title="Pulse SyncAlert", page_icon="❤️")
streamlit.title("🚨 Anomaly Log")
streamlit.markdown("Flagged anomalous readings from the baseline")


def db_ready():
    try:
        con = sqlite3.connect(DB)
        count = con.execute('SELECT COUNT(*) FROM heartrate').fetchone()[0]
        con.close()
        return count > 0
    except sqlite3.OperationalError:
        return False


if not db_ready():
    streamlit.warning(
        "Data is still being set up. Please open the **Pulse SyncAlert Dashboard** "
        "page first, then return here."
    )
    streamlit.stop()


def get_bpm():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    output = cur.execute('SELECT bpm FROM "heartrate"').fetchall()
    con.close()
    return output


chart = []
con = sqlite3.connect(DB)
cur = con.cursor()
anomalies = cur.execute(
    "SELECT bpm, time FROM heartrate WHERE anomaly_detected = -1 AND rowid <= 500"
).fetchall()
con.close()

abpm = get_bpm()


def average_bpm():
    clean_bpm = [p[0] for p in abpm if p[0] is not None]
    return statistics.median(clean_bpm)


avg_bpm = average_bpm()
for row in anomalies:
    bpm = row[0]
    t = row[1]
    difference = bpm - avg_bpm
    chart.append((pandas.to_datetime(t, unit="s"), bpm, difference))

table = pandas.DataFrame(chart, columns=["Time", "BPM", "Difference"])

with streamlit.container(border=True):
    streamlit.subheader("Total Anomalies Detected:  ")
    streamlit.subheader(f"{len(anomalies)}")

streamlit.dataframe(table, use_container_width=True)
