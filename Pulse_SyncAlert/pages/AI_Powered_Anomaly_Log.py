import streamlit
import sqlite3
import pandas
import statistics


streamlit.set_page_config(page_title="Pulse SyncAlert", page_icon="❤️")
streamlit.title("🚨 Anomaly Log")
streamlit.markdown("Flagged anomalous readings from the baseline")

def get_data(database, x):
    #accesses database.db
    con = sqlite3.connect(database)
    cur = con.cursor()
    #if time, bpm, then there would be a list that has tuples of BPM and time
    res = cur.execute(f'SELECT {x} FROM "heartrate"')
    #fetchall returns a list containting all the values in this column. (returns tuples of length 1)
    output = res.fetchall()
    con.close()
    return output

def get_bpm(database):
    #accesses database.db
    con = sqlite3.connect(database)
    cur = con.cursor()
    #if time, bpm, then there would be a list that has tuples of BPM and time
    res = cur.execute('SELECT bpm FROM "heartrate"')
    #fetchall returns a list containting all the values in this column. (returns tuples of length 1)
    output = res.fetchall()
    print(output)
    con.close()
    return output

chart = []
con = sqlite3.connect("synthetic_database.db")
cur = con.cursor()
res = cur.execute("SELECT bpm, time FROM heartrate WHERE anomaly_detected = -1 AND rowid <= 500")
anomalies = res.fetchall()
con.close()


abpm = get_bpm("synthetic_database.db")
def average_bpm():
    clean_bpm = []
    for point in abpm:
        if point[0] is not None:
            clean_bpm.append(point[0])

    avg_bpm = statistics.median(clean_bpm)
    return avg_bpm

avg_bpm = average_bpm()
for i in range(len(anomalies)):
    row = anomalies[i]
    bpm = row[0]
    time = row[1]

    difference = bpm - avg_bpm
    chart.append((pandas.to_datetime(time, unit="s"), bpm, difference))


table = pandas.DataFrame(chart, columns=["Time", "BPM", "Difference"])


# def update_database(data):
#     #accesses database.db
#     con = sqlite3.connect("alerts.db")
#     cur = con.cursor()
#     #creates heartrate table with time, IR, BPM, and avg bpm if it does not already exist
#     cur.execute("CREATE TABLE IF NOT EXISTS heartrate(time, BPM, change, severity, note)")
#     #adds the data into the table
#     cur.executemany("INSERT INTO heartrate VALUES(?, ?, ?, ?)", data)
#     con.commit()

# update_database()

with streamlit.container(border=True):
    streamlit.subheader("Total Anomalies Detected:  ")
    streamlit.subheader(f"{len(anomalies)}")

streamlit.dataframe(table, use_container_width=True)
