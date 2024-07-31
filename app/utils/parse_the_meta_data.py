import sqlite3

# Connect to the database
con = sqlite3.connect('/root/AiSK-backend/restaurant_info.db')
cur = con.cursor()

# Function to format the restaurant information
def format_restaurant_info(restaurant, menu_items):
    info = f"""
    식당 이름: {restaurant['NAME']}
    식당 주소: {restaurant['ADDRESS']}
        전화 번호: {restaurant['PHONE']}
        영업 시간: {restaurant['OPEN_HR_INFO']}
        종류: {restaurant['TYPE']}
        판매 품종: {', '.join(set([item['ITEM_NM'] for item in menu_items]))}
        경도: {restaurant['LNG']}
        위도: {restaurant['LAT']}
        메뉴: 
"""
    for item in menu_items:
        info += f"            {item['ITEM_NM']}: {item['ITEM_PRICE']}원\n"
    return info

# Query to get all restaurants
cur.execute("SELECT * FROM restaurants")
restaurants = cur.fetchall()

# Process each restaurant
for restaurant in restaurants:
    restaurant_dict = {
        'ID': restaurant[0],
        'NAME': restaurant[1],
        'ADDRESS': restaurant[2],
        'LAT': restaurant[3],
        'LNG': restaurant[4],
        'PHONE': restaurant[5],
        'TYPE': restaurant[6],
        'URL': restaurant[7],
        'INFO': restaurant[8],
        'MENU_ID': restaurant[9],
        'OPEN_HR_INFO': restaurant[10]
    }

    # Query to get menu items for the current restaurant
    cur.execute("SELECT ITEM_NM, ITEM_PRICE FROM MenuItems WHERE MENU_ID = ?", (restaurant_dict['MENU_ID'],))
    menu_items = cur.fetchall()

    # Convert menu items to a list of dictionaries
    menu_items_list = [{'ITEM_NM': item[0], 'ITEM_PRICE': item[1]} for item in menu_items]

    # Format and print the restaurant information
    formatted_info = format_restaurant_info(restaurant_dict, menu_items_list)
    print(formatted_info)

# Close the connection
con.close()
