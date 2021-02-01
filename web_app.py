
from flask import Flask

from Module.db_connector import connect
from Module.db_connector import disconnect

app = Flask(__name__)

@app.route("/get_user_name/<user_id>")
def get_user_name(user_id):
    # connect to DB
    conn, cursor = connect()

    user_name = cursor.execute("SELECT user_name FROM 42Oh3xFfiH.users_dateTime WHERE user_id = %s", args=user_id)
    if user_name != 0:
        for row in cursor:
            disconnect(conn, cursor)
            return "<h1 id='user'>" + row[0] + "</h1>"
    else:
        return "<h1 id='error'>" + 'no such user: ' + user_id + "</h1>"


app.run(host='127.0.0.1', debug=True, port=5001)
