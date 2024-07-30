import sqlite3
import json

con = sqlite3.connect('/root/AiSK-backend/restaurant_info.db')
cur = con.cursor()


# create table for restaurants (ID, NAME, ADDRESS, LAT, LNG, PHONE, TYPE, URL, INFO, MENU_ID)
cur.execute('''CREATE TABLE IF NOT EXISTS restaurants
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT,
                ADDRESS TEXT,
                LAT REAL,
                LNG REAL,
                PHONE TEXT,
                TYPE TEXT,
                URL TEXT,
                INFO TEXT,
                MENU_ID INTEGER)''')

# insert menu data
cur.execute("""
CREATE TABLE IF NOT EXISTS MenuItems (
    ITEM_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    MENU_ID INTEGER,
    ITEM_NM TEXT,
    ITEM_PRICE INTEGER,
    ITEM_INFO TEXT
);
""")

# open the json file and parse to db
with open('/root/관내 음식점 텍스트 데이터셋.json') as f:
    data = json.load(f)
    for d in data:
        # if one of the values are missing or empty, skip
        if not d['REST_NM'] or not d['ADDR'] or not d['LAT'] or not d['LOT'] or not d['TELNO'] or not d['TOB_INFO'] or not d['SD_URL'] or not d['MENU_ID'] or not d['MENU_KORN_NM'] or not d['MENU_AMT'] or (len(d['MENU_KORN_NM'].lstrip("[").rstrip("]").split(","))!=len(d['MENU_AMT'].lstrip("[").rstrip("]").split(","))):
            continue

        cur.execute('''INSERT INTO restaurants (NAME, ADDRESS, LAT, LNG, PHONE, TYPE, URL, INFO, MENU_ID)
                        VALUES (?,?,?,?,?,?,?,?,?)''', (d['REST_NM'], d['ADDR'], d['LAT'], d['LOT'], d['TELNO'], d['TOB_INFO'], d['SD_URL'],"",  d['MENU_ID']))
        for i in range(len(d['MENU_KORN_NM'].lstrip("[").rstrip("]").split(","))):
            cur.execute('''INSERT INTO MenuItems (MENU_ID, ITEM_NM, ITEM_PRICE, ITEM_INFO)
                            VALUES (?,?,?,?)''', (d['MENU_ID'], d['MENU_KORN_NM'].lstrip("[").rstrip("]").split(",")[i], d['MENU_AMT'].lstrip("[").rstrip("]").split(",")[i], ""))
# commit and close
con.commit()
con.close()