
import pymysql


def connect():
    conn = pymysql.connect(host='remotemysql.com', port=3306, user='42Oh3xFfiH', passwd='Yqr21iqYpw', db='42Oh3xFfiH')
    conn.autocommit(True)
    cursor = conn.cursor()

    return conn, cursor


def disconnect(conn, cursor):
    cursor.close()
    conn.close()
