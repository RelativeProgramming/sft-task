#!python-env/bin/python

import mariadb
import os
import sys
import time
from statistics import mean

#host = "127.0.0.1"
#port = 3306

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
TABLE_NAME = "writer"
TOTAL_MEASUREMENTS = 10

print(f"Host: {DB_HOST} Port: {DB_PORT}")

def connect():
    try:
        return mariadb.connect(user="root", password="test", host=DB_HOST, port=DB_PORT, database="test", autocommit=True)
    except mariadb.Error as err:
        print(f"Error connecting to MariaDB: {err}")

connection = connect()
if not connection:
    sys.exit(1)

try:
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS " + TABLE_NAME)
    cursor.execute("CREATE TABLE "+ TABLE_NAME +"(entry_id INT NOT NULL AUTO_INCREMENT, entry_value INT NOT NULL, PRIMARY KEY (entry_id))")
except mariadb.Error as err:
    print(f"Error dropping/recreating table: {err}")
    sys.exit(1)

seqNum = 0
cur_writes = 0
measurements = []

start = time.time()
while True:
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO `"+ TABLE_NAME +"` (entry_value) VALUES (?)", (seqNum,))
            seqNum += 1
            cur_writes += 1
        except mariadb.Error as err:
            print(f"Error writing to database: {err}")
            connection = None
    else: 
        connection = connect()
        continue

    delta = time.time() - start
    if delta > 1:
        measurements.append(cur_writes)
        cur_writes = 0
        start = time.time()
        if len(measurements) >= TOTAL_MEASUREMENTS:
            break

cursor.execute("DROP TABLE " + TABLE_NAME)
connection.close()

print("Average Insertions per second: "+ str(round(mean(measurements), 1)))
print("All measurements:")
print(*measurements)