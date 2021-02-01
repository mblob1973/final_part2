
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests

from Module.db_connector import connect
from Module.db_connector import disconnect

# Backend check
try:
    # Connect to DB
    conn, cursor = connect()

    # Get all data
    cursor.execute("SELECT * FROM 42Oh3xFfiH.config")
    last_line = list(cursor)[cursor.arraysize]

    user_id = input("Insert requested id for entry creation: ")
    http_link = last_line[1]
    user_name = last_line[2]
    browser = last_line[3]

    # request a post action to store data inside the DB
    requests.post("%s/%s" % (http_link, user_id), json={"user_name": user_name})
    # Check if user created successfully
    data = requests.get("%s/%s" % (http_link, user_id))
    if data.status_code == 200 and data.json()["user_name"] == user_name:
        print("Status code is \'%i\', Data retrieved from REST API is the same as posted" % data.status_code)

        # Check if user requested to create by user is stored under the requested id
        cursor.execute("SELECT * from 42Oh3xFfiH.users_dateTime WHERE user_id = %s", args=user_id)
        cursor.execute("SELECT * from 42Oh3xFfiH.users_dateTime WHERE user_id = %s", args=user_id)
        for row in cursor:
            print("User\'s ID and Name are \'%s\' and \'%s\' and the values the user asked for are ID \'%s\' and Name "
                  "\'%s\'." % (row[0], row[1], user_id, user_name))


        disconnect(conn, cursor)

        # Frontend check
        if browser == "chrome" or browser == "Chrome":
            chrome = webdriver.Chrome(".\\chromedriver.exe")
            chrome.get("http://127.0.0.1:5001/get_user_name/%s" % user_id)
            WebDriverWait(chrome, 15).until(EC.presence_of_element_located((By.ID, "user")))
            print("User name fetched from server:", chrome.find_element_by_id("user").text + ",", "Same as user requested at POST: %s" % user_name)

            chrome.close()

    else:
        print("Status code is \'%i\', Data retrieved from REST API is not the same as the data posted." % data.status_code)
        raise Exception("Test Failed")


except Exception as err:
    print(err)
