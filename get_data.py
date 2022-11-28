import mysql.connector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


conn = mysql.connector.connect(user='root', password='@Kingpin12', host='localhost', database='OwenSwims')

cur = conn.cursor()


d = pd.read_sql_query("SELECT * FROM Back200Y", conn)
df = pd.DataFrame(d, columns = ['times', 'meets', 'dates', 'year', 'sec'])
'''month = df['dates'].str.split(pat = ' ', n = 1, expand = True)
year = month[1].str.split(pat = ' ', expand = True)
df.insert(loc = 3, column = 'year', value = year[1])
df['year'] = pd.to_numeric(df['year'])'''
#df["times"] = df['times'].dt.time
t2 = []
for t1 in df['sec']:
    print(t1)
    t2.append(str(timedelta(seconds=t1)))

df['times1'] = t2
df = df.sort_values(by=['sec'])

print(df)

plt.scatter(df["year"],df['times1'],color="b")
plt.yticks([str(timedelta((df.iloc[-1,-2] - (df.iloc[-1, -2] * 0.05)))), str(timedelta((df.iloc[len(df['sec']) / 2, -2]))), str(timedelta((df.iloc[0, -2] + (df.iloc[0,-2] * 0.05))))])
plt.show()
conn.commit()