import re
import os
import mysql.connector

from configs.db_config import *


def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def connect_database():
    try:
        connection = mysql.connector.connect(**db_config)
    except Exception as e:
        print(e)
        print("Cannot connect to database")
        connection = None
    return connection


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def check_username(email):
    return True
    # return re.fullmatch(regex, email)

