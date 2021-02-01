
import requests
from Module.db_connector import connect
from Module.db_connector import disconnect

try:
    # user input
    user_id = input("Insert requested id for entry creation: ")
    user_name = input("Enter a user name for database entry creation: ")

    # store data inside the database
    requests.post("http://127.0.0.1:5000/users/{}".format(user_id), json={"user_name": user_name})

    # Check success
    data = requests.get("http://127.0.0.1:5000/users/{}".format(user_id))
    if data.status_code == 200 and data.json()["user_name"] == user_name:
        print("\nStatus code is \'%i\' and user name is \'%s\' as requested by user.\n" % (data.status_code, user_name))

        # Connect to database
        conn, cursor = connect()

        # Check if user stored
        cursor.execute("SELECT * from 42Oh3xFfiH.users_dateTime WHERE user_id = %s", args=user_id)
        for row in cursor:
            print("User\'s ID and Name are \'%s\' and \'%s\' and the values the user asked for are ID \'%s\' and Name "
                  "\'%s\'." % (row[0], row[1], user_id, user_name))

        disconnect(conn, cursor)

    else:
        print("Status code is \'%i\', the user was not created as requested." % data.status_code)
        raise Exception("Test Failed")


except Exception as err:
    print("Test Failed")
