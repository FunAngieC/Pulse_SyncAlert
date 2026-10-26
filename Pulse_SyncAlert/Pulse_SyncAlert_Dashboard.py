import streamlit
import sqlite3
import pandas
import statistics
import plotly.graph_objects as go


def get_data(database, x):
    #accesses database.db
    con = sqlite3.connect(database)
    cur = con.cursor()
    #if time, bpm, then there would be a list that has tuples of BPM and time
    res = cur.execute(f'SELECT {x} FROM "heartrate" LIMIT 500')
    #fetchall returns a list containting all the values in this column. (returns tuples of length 1)
    output = res.fetchall()
    con.close()
    return output


#makes the graph
def make_graph():
    #Line Graph
    bpm = get_data("synthetic_database.db", "rolling_avg")
    time = get_data("synthetic_database.db", "time")

    list_bpms = []
    list_times = []

    #Makes the whole data time and bpms for the chart
    for i in range(len(time)):
        if bpm[i][0] is not None:
            list_times.append(pandas.to_datetime(time[i][0], unit="s"))
            list_bpms.append(bpm[i][0])

    #makes just the anomaly time and bpm (time2 & bpm2) for the red dots on the graph
    con = sqlite3.connect("synthetic_database.db")
    cur = con.cursor()
    res = cur.execute("SELECT bpm, time FROM heartrate WHERE anomaly_detected = -1 AND rowid <= 500")
    anomalies = res.fetchall()
    con.close()
    bpm2 = []
    time2 = []
    for i in range(len(anomalies)):
        row = anomalies[i]
        #bpmx is just another name for bpm
        bpmx = row[0]
        timex = row[1]
        bpm2.append(bpmx)
        time2.append(pandas.to_datetime(timex, unit="s"))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list_times,
            y=list_bpms,
            name="Heart Rate"
        )
    )
    #makes the second line
    fig.add_trace(
        go.Scatter(
            x=time2,
            #grab all the timestampes and grab all the anomaly heartrates
            y=bpm2,
            mode="markers",
            marker={"color":"red"},
            name="⚠️ Anomaly"

        )
    )

    streamlit.plotly_chart(fig, config = {'scrollZoom': False})



#Download Button
def download_button():
    con = sqlite3.connect("synthetic_database.db")
    df = pandas.read_sql_query("SELECT * FROM heartrate", con)
    df = df.to_csv().encode("utf-8")

    streamlit.download_button(
        label="**📋 Download & Save Full Report for Cardiologist**",
        data= df,
        file_name="data.csv",
        mime="text/csv",
    )


#Average BPM
def average_bpm():
    bpm = get_data("synthetic_database.db", "rolling_avg")
    clean_bpm = []
    for point in bpm:
        if point[0] is not None:
            clean_bpm.append(point[0])

    avg_bpm = statistics.median(clean_bpm)
    return avg_bpm


def baseline():
    avg_bpm = average_bpm()
    with streamlit.container(border=True):
        streamlit.subheader("Average Beats Per Minute (BPM): ")
        streamlit.write(f"{round(avg_bpm, 1)}")


def anomaly():
    con = sqlite3.connect("synthetic_database.db")
    cur = con.cursor()
    res = cur.execute("SELECT bpm, time FROM heartrate WHERE anomaly_detected = -1 AND rowid <= 500")
    anomalies = res.fetchall()
    con.close()
    with streamlit.container(border=True):
        streamlit.subheader("Anomalies Detected:")
        streamlit.write(f" Total: {len(anomalies)}")
        streamlit.write(f"Percentage: {round((int(len(anomalies))/500)*100, 1)}% ")

def latest_bpm():
    #this is not anomalies, but is in this box anyway.
    con = sqlite3.connect("synthetic_database.db")
    cur = con.cursor()
    res1 = cur.execute("SELECT bpm FROM heartrate LIMIT 1 OFFSET 1999")
    latest_bpm = res1.fetchone()[0]
    with streamlit.container(border=True):
        streamlit.subheader("Latest BPM:")
        streamlit.write(f"{round(float(latest_bpm), 1)}")

    con.close()

def total_readings():
    with streamlit.container(border=True):
        streamlit.subheader("Total Readings:")
        streamlit.write("500")

def main():
    streamlit.set_page_config(page_title="Pulse SyncAlert", page_icon="❤️")
    streamlit.title("Pulse SyncAlert 🫀")
    streamlit.subheader("Real-time cardiac anomaly detection")
    make_graph()
    download_button()
    baseline()
    anomaly()
    latest_bpm()
    total_readings()
if __name__ == "__main__":
    main()
