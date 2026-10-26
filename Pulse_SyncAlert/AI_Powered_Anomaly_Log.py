import streamlit
import sqlite3
import pandas
import statistics
import os
import time

# pages/ is one level below the main app folder — go up one to find the db
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "synthetic_database.db")

streamlit.set_page_config(page_title="Pulse SyncAlert", page_icon="❤️")
streamlit.title("🚨 Anomaly Log")
streamlit.markdown("Flagged anomalous readings from the baseline")


def db_ready():
    """Check that the table exists, has rows, AND has anomaly_detected populated."""
    try:
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cols = [row[1] for row in cur.execute('PRAGMA table_info(heartrate)').fetchall()]
        if 'anomaly_detected' not in cols:
            con.close()
            return False
        filled = cur.execute(
            'SELECT COUNT(*) FROM heartrate WHERE anomaly_detected IS NOT NULL'
        ).fetchone()[0]
        con.close()
        return filled > 0
    except sqlite3.OperationalError:
        return False


# Wait up to 30 seconds for the dashboard to finish setting up the data
if not db_ready():
    with streamlit.spinner("Waiting for data to finish loading — please wait…"):
        for _ in range(15):  # try every 2 seconds for up to 30 seconds
            time.sleep(2)
            if db_ready():
                streamlit.rerun()
        # If still not ready after 30 seconds, show message
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
