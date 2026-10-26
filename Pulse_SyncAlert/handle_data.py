#Assuming there is a time stamp and a #. 
import sqlite3
import time
import serial

data = [
        ("19:50:49.607", 111615, 60.01, 99),
        ("19:55:49.607", 111615, 65.09, 99), 
        ("20:00:49.380", 111184, 80.45, 99), 
        ("20:05:49.380", 111184, 75.31, 99), 
        ("20:10:49.380", 111184, 73.70, 99), 
        ("20:15:49.380", 111184, 75.09, 99), 
        ("20:20:49.380", 111184, 71.00, 99), 
        ("20:25:49.380", 111184, 65.00, 99), 
        ("20:30:49.380", 111184, 70.00, 99), 
        ("20:35:49.380", 111184, 78.00, 99), 
        ("20:40:49.380", 111184, 73.00, 99), 
        ("20:45:49.380", 111184, 68.00, 99), 
        ("20:50:49.380", 111184, 64.00, 99), 
        ("20:55:49.380", 111184, 59.00, 99), 
        ]
def update_database(data):
    #accesses database.db
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    #creates heartrate table with time, IR, BPM, and avg bpm if it does not already exist
    cur.execute("CREATE TABLE IF NOT EXISTS heartrate(time, IR, BPM, avg_bpm)")
    #adds the data into the table
    cur.executemany("INSERT INTO heartrate VALUES(?, ?, ?, ?)", data)
    con.commit()
    #!!!!What does this do?
    res = cur.execute('SELECT * FROM "heartrate"')
    output = res.fetchone()
    print(output)
    con.close()

update_database(data)

