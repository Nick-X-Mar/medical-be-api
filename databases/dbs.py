import mysql.connector
from config import config


def connect_to_mysql():
    mydb = mysql.connector.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DB
    )
    print(mydb)
    return mydb
