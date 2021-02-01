
from flask import Flask, request
from datetime import datetime

from Module.db_connector import connect
from Module.db_connector import disconnect

app = Flask(__name__)


@app.route("/users/<user_id>", methods=['GET', 'POST', 'DELETE', 'PUT'])
def users_actions(USER_ID):
    if request.method == 'GET':
        try:
            # Connect to DB
            conn, cursor = connect()

            cursor.execute("SELECT * FROM 42Oh3xFfiH.users_dateTime WHERE user_id = %s", args=USER_ID)
            for row in cursor:
                name = row[1]


            disconnect(conn, cursor)

            return {"status": "ok", "user_name": name}, 200

        except Exception as err:
            return {"status": "error", "reason": "no such id"}, 500

    elif request.method == 'POST':  # Check if the method given os POST
        try:
            # Prepared
            sql = "INSERT INTO 42Oh3xFfiH.users_dateTime (user_id, user_name, creation_date) VALUES (%s, %s, %s)"

            # Connect to DB
            conn, cursor = connect()

            data = request.json  # Get data from json payload
            date = datetime.now()  # Get current date and time for creation date field in users table
            cursor.execute(sql, args=(
                USER_ID, data.get("user_name"), date.strftime("%Y-%m-%d %H:%M:%S")))  # Execute the query

            # Disconnect from DB
            disconnect(conn, cursor)

            # If user generation succeeded
            return {"status": "ok", "user_added": data.get("user_name")}, 200

        except Exception as err:
            return {"status": "error", "reason": "id already exist"}, 500

    elif request.method == 'PUT':
        try:
            # Connect to DB
            conn, cursor = connect()

            data = request.json
            cursor.execute("UPDATE 42Oh3xFfiH.users_dateTime SET user_name = %s WHERE user_id = %s",
                           args=(data.get("user_name"), USER_ID))


            disconnect(conn, cursor)

            # Return json of success
            return {"status": "ok", "user_updated": data.get("user_name")}, 200

        except Exception as err:  # If error occurred
            return {"status": "error", "reason": "no such id"}, 500

    elif request.method == 'DELETE':
        try:
            # Connect to DB
            conn, cursor = connect()

            cursor.execute("DELETE from 42Oh3xFfiH.users_dateTime WHERE user_id = %s", args=(USER_ID))

            # Disconnect from DB
            disconnect(conn, cursor)

            # Return json of success
            return {"status": "ok", "user_deleted": USER_ID}, 200

        except Exception as err:  # If error occurred
            return {"status": "error", "reason": "no such id"}, 500


app.run(host='127.0.0.1', debug=True, port=5000)
