from sklearn.ensemble import IsolationForest
import sqlite3
import pandas as pd
#use isolation forest


def get_column(database):
    #accesses database.db
    con = sqlite3.connect(database)
    cur = con.cursor()
    #if time, bpm, then there would be a list that has tuples of BPM and time
    res = cur.execute('SELECT BPM FROM "heartrate"')
    #fetchall returns a list containting all the values in this column. (returns tuples of length 1)
    output = res.fetchall()
    print(output)
    con.close()
    return output


def rolling_average(data):
    df = pd.DataFrame(data, columns=["bpm"])
    df["rolling_avg"] = df["bpm"].rolling(window=3).mean()
    conn = sqlite3.connect("synthetic_database.db")
    cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE heartrate ADD COLUMN rolling_avg REAL;")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    for i, avg in enumerate(df["rolling_avg"], start=1):
        cur.execute("UPDATE heartrate SET rolling_avg = ? WHERE rowid = ?", (avg, i))
    conn.commit()
    conn.close()
    return df["rolling_avg"]


def process_data(data):
    training_data = get_column("training_data.db")
    #cannot make this more accurate unless there is a contamination rate, which we cannot have b/c of how we decide %
    forest = IsolationForest()
    forest.fit(training_data)

    conn = sqlite3.connect("synthetic_database.db")
    cur = conn.cursor()

    try:
        cur.execute("ALTER TABLE heartrate ADD COLUMN anomaly_detected INTEGER;")
        conn.commit()
    except sqlite3.OperationalError:
        pass

    output = forest.predict(data)


    for i, analysis in enumerate(output, start=1):
        cur.execute("UPDATE heartrate SET anomaly_detected = ? WHERE rowid = ?",
                    [int(analysis), i])

    conn.commit()
    conn.close()

    return output


def smooth_data(labels):
    for i in range(len(labels) - 2):
        previous_number = labels[i]
        if previous_number == labels[i+1]:
            pass
        elif previous_number != labels[i+1]:
            if previous_number ==labels[i+2]:
                labels[i+1] = previous_number
            else:
                pass
    return labels


if __name__ == "__main__":
    data = get_column("synthetic_database.db")
    rolling_average(data)
    labels = process_data(data)

    con = sqlite3.connect("synthetic_database.db")
    cur = con.cursor()
    res = cur.execute("SELECT bpm, time FROM heartrate WHERE anomaly_detected = -1 AND rowid <= 500")
    anomalies = res.fetchall()
    con.close()

    number_of_anomalies = len(anomalies)

    data1 = smooth_data(labels)
    for p1, p2 in zip(data, data1):
        print(p1, p2)
