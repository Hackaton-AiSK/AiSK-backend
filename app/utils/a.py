import sqlite3
import json

con = sqlite3.connect('/root/AiSK-backend/restaurant_info.db')

# get all the restaurants
cur = con.cursor()
cur.execute('SELECT * FROM restaurants')
rows = cur.fetchall()
print(len(rows))
for row in rows:
    print(row)
cur.execute('SELECT * FROM MenuItems')
rows = cur.fetchall()
print(len(rows))
for row in rows:
    print(row)


with open('/root/관내 음식점 텍스트 데이터셋.json') as f:
    data = json.load(f)

