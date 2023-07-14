import sys
sys.path.append('../app')
sys.path.append('../ml')
sys.path.append('../utils')

import csv
import datetime
from models.store import Store
from dao.store_dao import insert_store_id
from models.dataset import Dataset
from models.store_business_hrs import StoreBusinessHrs
from models.store_status import StoreStatus
from models.store_time_zone import StoreTimeZone
from database_connection import DatabaseConnection
from dao.dataset_dao import insert_dataset
from data_preparation.data_loading import dataCreation
from dao.store_business_hrs_dao import get_unique_store_business_hrs_ids, insert_business_hrs_details
from dao.store_status_dao import get_unique_store_status_ids, insert_store_status_details
from dao.store_time_zone_dao import get_unique_store_timezone_ids, insert_timezone_details

db_connection = DatabaseConnection()


def insert_business_hrs(path):
    with open(path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row if present
        for row in csv_reader:
            store_business_hr = StoreBusinessHrs(row[0],row[1],row[2],row[3])
            insert_business_hrs_details(store_business_hr)


def insert_store_status(path):
    weekdays = {'Monday':0 , 'Tuesday':1, 'Wednesday':2, 'Thursday':3, 'Friday':4, 'Saturday':6, 'Sunday':6}
    with open(path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row if present
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
            store_status = StoreStatus(row[0],row[1],row[2],row[3],row[4],row[5])
            insert_store_status_details(store_status)

def insert_timezone(path):
    with open(path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row if present
        for row in csv_reader:
            store_timezone = StoreTimeZone(row[0],row[1])
            insert_timezone_details(store_timezone)

def insert_store_ids():
    rows = get_unique_store_status_ids()
    for row in rows:
        store = Store(row[0])
        insert_store_id(store)

    rows = get_unique_store_business_hrs_ids()
    for row in rows:
        store = Store(row[0])
        insert_store_id(store)

    rows = get_unique_store_timezone_ids()
    for row in rows:
        store = Store(row[0])
        insert_store_id(store)


def insert_dataset_details():
   for id in dataset:
      storeData = dataset[id]
      for date in storeData:
         data = storeData[date]
         for row in enumerate(data):
            dataset = Dataset(row[0],row[1],row[2],row[3])
            insert_dataset(dataset)


# insert_business_hrs('../data_source/business_hours.csv')
# print("1")
# insert_timezone('../data_source/timezone.csv')
# print("2")
insert_store_status('../data_source/store_status.csv')
print("3")
insert_store_ids()
print("4")
insert_dataset_details(dataCreation())
print("5")

db_connection.commit()
db_connection.close()    

