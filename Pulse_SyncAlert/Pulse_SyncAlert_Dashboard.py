import streamlit
import sqlite3
import pandas
import statistics
import plotly.graph_objects as go
import os
import random
import time as time_module
from sklearn.ensemble import IsolationForest

# Use absolute path so SQLite always finds the file regardless of working directory
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "synthetic_database.db")
TRAINING_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "training_data.db")


def db_needs_setup():
    """Return True if the heartrate table is missing or empty."""
    try:
        con = sqlite3.connect(DB)
        cur = con.cursor()
        count = cur.execute('SELECT COUNT(*) FROM heartrate').fetchone()[0]
        con.close()
        return count == 0
    except sqlite3.OperationalError:
        return True


def generate_data():
    """Generate 2000 synthetic SVT heart rate readings and write to DB."""
    average, anomaly_average = 85, 170
    anomaly_percentage, anomaly_number, deviation, data_amount = 0.00005, 3, 6, 2000

    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS heartrate"
        "(time REAL, bpm REAL, ir REAL, rolling_avg REAL, anomaly_detected INTEGER)"
    )
    con.commit()

    anomaly_counts = 0
    rows = []
    for i in range(data_amount):
        rnd = random.random()
        if rnd > anomaly_percentage and anomaly_counts % anomaly_number == 0 and anomaly_counts != 0:
            bpm = random.gauss(average, deviation)
            bpm = max(average - deviation * 3, min(average + deviation * 3, bpm))
        else:
            bpm = random.gauss(anomaly_average, deviation)
            bpm = max(anomaly_average - deviation * 3, min(anomaly_average + deviation * 3, bpm))
            anomaly_counts += 1
        ir = random.gauss(92500, 10000)
        ir = max(50000, min(135000, ir))
        ts = time_module.time() + i
        rows.append((ts, bpm, ir, None, None))

    cur.executemany("INSERT INTO heartrate VALUES(?, ?, ?, ?, ?)", rows)
    con.commit()
    con.close()


def run_analysis():
    """Compute rolling average and anomaly detection, write results to DB."""
    import pandas as pd

    con = sqlite3.connect(DB)
    rows = con.execute('SELECT bpm FROM heartrate ORDER BY rowid').fetchall()
    con.close()

    df = pd.DataFrame(rows, columns=["bpm"])
    df["rolling_avg"] = df["bpm"].rolling(window=3).mean()

    con = sqlite3.connect(DB)
    cur = con.cursor()
    for i, avg in enumerate(df["rolling_avg"], start=1):
        cur.execute("UPDATE heartrate SET rolling_avg = ? WHERE rowid = ?", (avg, i))
    con.commit()
    con.close()

    data = [(r[0],) for r in rows]
    try:
        tcon = sqlite3.connect(TRAINING_DB)
        training_data = tcon.execute('SELECT BPM FROM heartrate').fetchall()
        tcon.close()
        if not training_data:
            training_data = data
    except Exception:
        training_data = data

    forest = IsolationForest()
    forest.fit(training_data)
    labels = forest.predict(data)

    con = sqlite3.connect(DB)
    cur = con.cursor()
    for i, label in enumerate(labels, start=1):
        cur.execute("UPDATE heartrate SET anomaly_detected = ? WHERE rowid = ?",
                    (int(label), i))
    con.commit()
    con.close()


def ensure_data():
    if db_needs_setup():
        with streamlit.spinner("Setting up data for first run — about 10 seconds…"):
            generate_data()
            run_analysis()


# ── page functions ─────────────────────────────────────────────────────────────

def get_data(x):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    res = cur.execute(f'SELECT {x} FROM "heartrate" LIMIT 500')
    output = res.fetchall()
    con.close()
    return output


def make_graph():
    bpm = get_data("rolling_avg")
    time = get_data("time")

    list_bpms, list_times = [], []
    for i in range(len(time)):
        if bpm[i][0] is not None:
            list_times.append(pandas.to_datetime(time[i][0], unit="s"))
            list_bpms.append(bpm[i][0])

    con = sqlite3.connect(DB)
    cur = con.cursor()
    anomalies = cur.execute(
        "SELECT bpm, time FROM heartrate WHERE anomaly_detected = -1 AND rowid <= 500"
    ).fetchall()
    con.close()

    bpm2, time2 = [], []
    for row in anomalies:
        bpm2.append(row[0])
        time2.append(pandas.to_datetime(row[1], unit="s"))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list_times, y=list_bpms, name="Heart Rate"))
    fig.add_trace(go.Scatter(
        x=time2, y=bpm2,
        mode="markers",
        marker={"color": "red"},
        name="⚠️ Anomaly"
    ))
    streamlit.plotly_chart(fig, config={'scrollZoom': False})


def download_button():
    con = sqlite3.connect(DB)
    df = pandas.read_sql_query("SELECT * FROM heartrate", con)
    con.close()
    csv = df.to_csv().encode("utf-8")
    streamlit.download_button(
        label="**📋 Download & Save Full Report for Cardiologist**",
        data=csv,
        file_name="data.csv",
        mime="text/csv",
    )


def average_bpm():
    bpm = get_data("rolling_avg")
    clean = [p[0] for p in bpm if p[0] is not None]
    return statistics.median(clean)


def baseline():
    with streamlit.container(border=True):
        streamlit.subheader("Average Beats Per Minute (BPM): ")
        streamlit.write(f"{round(average_bpm(), 1)}")


def anomaly():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    anomalies = cur.execute(
        "SELECT bpm, time FROM heartrate WHERE anomaly_detected = -1 AND rowid <= 500"
    ).fetchall()
    con.close()
    with streamlit.container(border=True):
        streamlit.subheader("Anomalies Detected:")
        streamlit.write(f" Total: {len(anomalies)}")
        streamlit.write(f"Percentage: {round((len(anomalies) / 500) * 100, 1)}%")


def latest_bpm():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    row = cur.execute("SELECT bpm FROM heartrate LIMIT 1 OFFSET 1999").fetchone()
    con.close()
    with streamlit.container(border=True):
        streamlit.subheader("Latest BPM:")
        streamlit.write(f"{round(float(row[0]), 1)}")


def total_readings():
    with streamlit.container(border=True):
        streamlit.subheader("Total Readings:")
        streamlit.write("500")


def main():
    streamlit.set_page_config(page_title="Pulse SyncAlert", page_icon="❤️")
    streamlit.title("Pulse SyncAlert 🫀")
    streamlit.subheader("Real-time cardiac anomaly detection")

    ensure_data()  # reads from db if populated; generates fresh if empty/missing

    make_graph()
    download_button()
    baseline()
    anomaly()
    latest_bpm()
    total_readings()


if __name__ == "__main__":
    main()
