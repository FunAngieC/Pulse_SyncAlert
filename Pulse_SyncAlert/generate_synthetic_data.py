import random
import sqlite3
import time



def update_database(data):
    #accesses database.db
    con = sqlite3.connect("synthetic_database.db")
    cur = con.cursor()
    #creates heartrate table with time, IR, BPM, and avg bpm if it does not already exist

    cur.execute("CREATE TABLE IF NOT EXISTS heartrate(time REAL, bpm REAL, ir REAL)")
    #adds the data into the table
    cur.executemany("INSERT INTO heartrate VALUES(?, ?, ?)", data)
    con.commit()
    #This takes all the lines from the db
    res = cur.execute('SELECT * FROM "heartrate"')
    #this prints the first line
    output = res.fetchone()
    print(output)
    con.close()

#66% = 68-72, ~97% spread*3
#Makes 50 pieces of AVERAGE DATA
#add the spread to the variables. Remember to change both the spread and the + and - (also change it on the anomaly average)
#make up imaginary people
#Make a parameter for the number of data points you want.
def make_heartrate(average, anomaly_average,  anomaly_percentage, anomaly_number, deviation, data_amount,):
    anomaly_counts = 0
    #pick number between 0 and one and see if it is below anomaly. If so, generate anomaly
    for i in range(data_amount):
        random_number = random.random()
        if random_number > anomaly_percentage and anomaly_counts%anomaly_number == 0 and anomaly_counts!=0:
            bpm = random.gauss(average, deviation)
            bpm = max(average-(deviation*3), min(average+(deviation*3), bpm))


        else:
            bpm = random.gauss(anomaly_average, deviation)
            bpm = max(anomaly_average-(deviation*3), min(anomaly_average+(deviation*3), bpm))
            anomaly_counts += 1

        ir = random.gauss(92500, 10000)
        ir = max(50000, min(135000, ir))
        time_stamp = time.time() + i
        data = [(time_stamp, bpm, ir)]
        update_database(data)
        print(data)

if __name__ == "__main__":
    svt = make_heartrate(85, 170, 0.00005, 3, 6, 500)
    #hyperthyroid = make_heartrate(100, 160, 500)
