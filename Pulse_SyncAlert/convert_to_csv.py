import streamlit
import sqlite3
import pandas
import statistics
import plotly.graph_objects as go


con = sqlite3.connect("synthetic_database2.db")
df = pandas.read_sql_query("SELECT * FROM heartrate", con)
df.to_csv("heart_rate_report.csv", index=False)
