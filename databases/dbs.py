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
    # print("Connected to:", my_db.get_server_info())
    # print(f"my_db: {my_db}")
    return my_db


def query_mysql(q):
    try:
        my_sql = connect_to_mysql()
        cursor = my_sql.cursor(dictionary=True, buffered=True)
        cursor.execute(q)
        results = cursor.fetchall()
        cursor.close()
        my_sql.close()
        return results
    except Exception as e:
        print(f"Error: {e}, executing the sql query: {q}")
        return 400
