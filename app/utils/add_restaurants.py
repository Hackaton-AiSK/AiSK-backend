import sqlite3
import json

# Connect to the database
con = sqlite3.connect('/root/AiSK-backend/restaurant_info.db')
cur = con.cursor()

# Create table for restaurants (ID, NAME, ADDRESS, LAT, LNG, PHONE, TYPE, URL, INFO, MENU_ID, OPEN_HR_INFO)
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
                MENU_ID INTEGER,
                OPEN_HR_INFO TEXT,
                IMAGE_URL TEXT
                )''')

# Create table for menu items
cur.execute("""
CREATE TABLE IF NOT EXISTS MenuItems (
    ITEM_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    MENU_ID INTEGER,
    ITEM_NM TEXT,
    ITEM_PRICE INTEGER,
    ITEM_INFO TEXT
);
""")

# Open the JSON file and parse it
with open('/root/관내 음식점 텍스트 데이터셋.json') as f:
    data = json.load(f)
    for d in data:
        # If any critical data is missing or empty, skip the entry
        if not d['REST_NM'] or not d['ADDR'] or not d['LAT'] or not d['LOT'] or not d['TELNO'] or not d['TOB_INFO'] or not d['SD_URL'] or not d['MENU_ID'] or not d['MENU_KORN_NM'] or not d['MENU_AMT'] or (len(d['MENU_KORN_NM'].lstrip("[").rstrip("]").split(",")) != len(d['MENU_AMT'].lstrip("[").rstrip("]").split(","))):
            continue
        
        # Insert restaurant data including OPEN_HR_INFO
        cur.execute('''INSERT INTO restaurants (NAME, ADDRESS, LAT, LNG, PHONE, TYPE, URL, INFO, MENU_ID, OPEN_HR_INFO, IMAGE_URL)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (d['REST_NM'], d['ADDR'], d['LAT'], d['LOT'], d['TELNO'], d['TOB_INFO'], d['SD_URL'], "", d['MENU_ID'], d['OPEN_HR_INFO'], ""))
        
        # Insert menu items data
        menu_items = d['MENU_KORN_NM'].lstrip("[").rstrip("]").split(",")
        menu_prices = d['MENU_AMT'].lstrip("[").rstrip("]").split(",")
        for i in range(len(menu_items)):
            cur.execute('''INSERT INTO MenuItems (MENU_ID, ITEM_NM, ITEM_PRICE, ITEM_INFO)
                            VALUES (?,?,?,?)''', (d['MENU_ID'], menu_items[i], menu_prices[i], ""))
                            
# Commit changes and close the connection
con.commit()
con.close()
