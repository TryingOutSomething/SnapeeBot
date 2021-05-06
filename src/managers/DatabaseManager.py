from src.managers import LoggerManager, IOassetsManager

import mysql.connector
from mysql.connector import Error


def init_db_connection():
    HOST, PORT, USERNAME, PASSWORD = IOassetsManager.get_db_conn_details()

    return mysql.connector.connect(host=HOST,
                                   port=PORT,
                                   user=USERNAME,
                                   password=PASSWORD)


def query_database_with_conditions(query_statement, values):
    try:
        conn = init_db_connection()

        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(query_statement, values)
            result = cursor.fetchall()

            cursor.close()
            conn.close()

            return result

        else:
            LoggerManager.general_logs(
                'Connection to SQL DB cannot be established.')
            conn.close()

    except Error as e:
        LoggerManager.exception_logs(e)


def query_database_no_conditions(query_statement):
    try:
        conn = init_db_connection()

        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(query_statement)
            result = cursor.fetchall()

            cursor.close()
            conn.close()

            return result

        else:
            LoggerManager.general_logs(
                'Connection to SQL DB cannot be established.')
            conn.close()

    except Error as e:
        LoggerManager.exception_logs(e)


def update_database_table(update_statement, values):
    try:
        conn = init_db_connection()

        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(update_statement, values)
            conn.commit()

            cursor.close()
            conn.close()

            return True

        else:
            LoggerManager.general_logs(
                'Connection to SQL DB cannot be established.')
            conn.close()

    except Error as e:
        LoggerManager.exception_logs(e)
