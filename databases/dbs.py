import mysql.connector as mysql
from config import config
# from pandas import DataFrame
# import pandas as pd


def connect_to_mysql():
    # print(f"Connecting to Host: {config.MYSQL_HOST}, \nuser: {config.MYSQL_USER}, \npassword: {config.MYSQL_PASSWORD}, \ndatabase: {config.MYSQL_DB} ")
    my_db = mysql.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DB
    )
    print(f"Connection to: {my_db.server_host} is: {my_db.is_connected()}")
    return my_db


def query_mysql(q):
    try:
        my_sql = connect_to_mysql()
        cursor = my_sql.cursor(dictionary=True)  # mysql.connector
        cursor.execute(q)
        results = cursor.fetchall()
        my_sql.commit()
        cursor.close()
        my_sql.close()
        return results, 200
    except Exception as e:
        print(f"Error: {e} was returned while executing the following sql query: {q}")
        return f"{e}", 400
