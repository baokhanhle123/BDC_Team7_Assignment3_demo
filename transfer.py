import sqlite3
import pandas as pd

df = pd.read_csv("data.csv")
df = df.drop(df.columns[0], axis=1)
print(df.columns)

conn = sqlite3.connect("data/data.db")

create_sql = "CREATE TABLE IF NOT EXISTS \
        users (id INTEGER,\
        delay INTEGER, \
        ip_address TEXT,\
        hit_status TEXT,\
        content_name TEXT,\
        file_size INTEGER,\
        latitude REAL,\
        longitude REAL,\
        ISP TEXT,\
        region TEXT,\
        country TEXT,\
        file_type TEXT,\
        req_date DATE,\
        req_time TIME)"

cursor = conn.cursor()
cursor.execute(create_sql)
