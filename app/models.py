from . import mysql

def execute_query(query, params=None):
    cursor = mysql.connection.cursor()
    cursor.execute(query, params)
    mysql.connection.commit()
    cursor.close()

def fetch_query(query, params=None):
    cursor = mysql.connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    return result