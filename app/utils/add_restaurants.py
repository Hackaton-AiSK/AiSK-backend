import sqlite3
import json
import random

# Connect to the database
con = sqlite3.connect('/root/AiSK-backend/demo.db')
cur = con.cursor()




# Open the JSON file and parse it
with open('/root/관내 음식점 텍스트 데이터셋.json') as f:
    data = json.load(f)
    for d in random.sample(data, 30):
        # If any critical data is missing or empty, skip the entry
        if not d['REST_NM'] or not d['ADDR'] or not d['LAT'] or not d['LOT'] or not d['TELNO'] or not d['TOB_INFO'] or not d['SD_URL'] or not d['MENU_ID'] or not d['MENU_KORN_NM'] or not d['MENU_AMT'] or (len(d['MENU_KORN_NM'].lstrip("[").rstrip("]").split(",")) != len(d['MENU_AMT'].lstrip("[").rstrip("]").split(","))):
            continue
        
        # Insert restaurant data including OPEN_HR_INFO
        cur.execute('''INSERT INTO restaurants (NAME, ADDRESS, LAT, LNG, PHONE, TYPE, URL, INFO, MENU_ID, OPEN_HR_INFO, IMAGE_URL)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (d['REST_NM'], d['ADDR'], d['LAT'], d['LOT'], d['TELNO'], d['TOB_INFO'], d['SD_URL'], "", d['MENU_ID'], d['OPEN_HR_INFO'], ""))
    
                            
# Commit changes and close the connection
con.commit()
con.close()
