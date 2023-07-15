import sys
sys.path.append('c:\\Users\\GOURAV\\Desktop\\loopAI')
sys.path.append('c:\\Users\\GOURAV\\Desktop\\loopAI\\app')
sys.path.append('c:\\Users\\GOURAV\\Desktop\\loopAI\\data_source')
sys.path.append('c:\\Users\\GOURAV\\Desktop\\loopAI\\database_initialization')
sys.path.append('c:\\Users\\GOURAV\\Desktop\\loopAI\\ml')
sys.path.append('c:\\Users\\GOURAV\\Desktop\\loopAI\\utils')

import csv,os
import datetime
from check_utils import check
from dao.store_dao import insert_store_id
from dao.dataset_dao import insert_dataset
from data_preparation.data_preprocessing import data_set_creation
from dao.store_business_hrs_dao import get_unique_store_business_hrs_ids, insert_business_hrs_details
from dao.store_status_dao import get_unique_store_status_ids, insert_store_status_details
from dao.store_time_zone_dao import get_unique_store_timezone_ids, insert_timezone_details
from concurrent.futures import ThreadPoolExecutor


from database_connection import DatabaseConnection
db_connection = DatabaseConnection()

def insert_business_hrs(path):
    with open(os.path.abspath(path), 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            if check(row[0]) and check(row[1]) and check(row[2]) and check(row[3]):
                db_connection.execute_query("INSERT OR REPLACE  INTO storeBusinessHrs (store_id, day, start_time , end_time) VALUES (?, ?, ?, ?)", (row[0],row[1],row[2],row[3],))

def insert_store_status(path):
    weekdays = {'Monday':0 , 'Tuesday':1, 'Wednesday':2, 'Thursday':3, 'Friday':4, 'Saturday':6, 'Sunday':6}
    with open(os.path.abspath(path), 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        with ThreadPoolExecutor(max_workers=5) as executor:
            for row in csv_reader:
                timestamp_str = row[2]
                timestamp_str = timestamp_str.replace(" UTC", "")
                timestamp_str = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
                timestamp_str = timestamp_str.strftime('%Y-%m-%d %H:%M:%S.%f')
                timestamp = datetime.datetime.fromisoformat(timestamp_str)
                nearest_minute = timestamp.replace(second=0, microsecond=0)
                row[2] = nearest_minute.isoformat()
                date = nearest_minute.strftime('%Y-%m-%d')
                time = nearest_minute.strftime('%H:%M')
                day  = weekdays[nearest_minute.strftime('%A')]
                row.append(date)
                row.append(time)
                row.append(day)
                # converting timestamp into date  , time and day
                if check(row[0]) and check(row[1]) and check(row[2]) and check(row[3]) and check(row[4]) and check(row[5]):
                    db_connection.execute_query("INSERT OR REPLACE  INTO storeStatus (store_id, status, timeStamp_utc, date, time, day) VALUES (?, ?, ?, ?, ?, ?)", (row[0],row[1],row[2],row[3],row[4],row[5],))

def insert_timezone(path):
    with open(os.path.abspath(path), 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            if check(row[0]) and check(row[1]):
                db_connection.execute_query("INSERT OR REPLACE  INTO storeTimeZone (store_id, timezone) VALUES (?, ?)", (row[0],row[1],))

def insert_store_ids():
    # get the unique store_ids from each table and insert into store table
    rows = get_unique_store_status_ids()
    for row in rows:
        db_connection.execute_query("INSERT OR REPLACE  INTO store (store_id) VALUES (?)", (row[0],))

    rows = get_unique_store_business_hrs_ids()
    for row in rows:
        db_connection.execute_query("INSERT OR REPLACE  INTO store (store_id) VALUES (?)", (row[0],))

    rows = get_unique_store_timezone_ids()
    for row in rows:
        db_connection.execute_query("INSERT OR REPLACE  INTO store (store_id) VALUES (?)", (row[0],))


print("start --- filling store_business_hrs table")
insert_business_hrs('data_source/business_hours.csv')
print("complete --- filling business_hrs table")

print("start --- filling store_timezone table")
insert_timezone('data_source/timezone.csv')
print("complete --- filling timezone table")

print("start --- filling store_status table")
insert_store_status('data_source/store_status.csv')
print("complete --- filling store_status table")

print("start --- filling store_ids table")
insert_store_ids()
print("complete --- filling store_ids table")

print("start --- filling dataset table")
data_set_creation()
print("complete --- filling dataset table")

db_connection.commit()
db_connection.close()