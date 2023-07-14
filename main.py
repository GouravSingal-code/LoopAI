import csv
import datetime
from app.models.dataset import Dataset
from app.models.store_business_hrs import StoreBusinessHrs
from app.models.store_status import StoreStatus
from app.models.store_time_zone import StoreTimeZone
from app.dao.daily_report_dao import daily_task
from database_initialization.database_connection import DatabaseConnection
from app.dao.dataset_dao import insert_dataset
from app.dao.hourly_report_dao import hourly_task
from ml.data_preparation.data_loading import dataCreation
from app.dao.store_business_hrs_dao import insert_business_hrs_details
from app.dao.store_status_dao import insert_store_status_details
from app.dao.store_time_zone_dao import insert_timezone_details
from utils.calender_utils import Calender
from app.dao.weekly_report_dao import weekly_task


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


def insert_store_id():
    
    store_id_query = '''
    SELECT distinct storeStatus.store_id
    FROM storeStatus
    '''

    rows = db_connection.execute_query(store_id_query)
    for row in rows:
        db_connection.execute_query("INSERT OR IGNORE INTO store (store_id) VALUES (?)", row)


    store_id_query = '''
    SELECT distinct storeBusinessHrs.store_id
    FROM storeBusinessHrs
    '''

    rows = db_connection.execute_query(store_id_query)
    for row in rows:
        db_connection.execute_query("INSERT OR IGNORE INTO store (store_id) VALUES (?)", row)


    store_id_query = '''
    SELECT distinct storeTimeZone.store_id
    FROM storeTimeZone
    '''

    rows = db_connection.execute_query(store_id_query)
    for row in rows:
        db_connection.execute_query("INSERT OR IGNORE INTO store (store_id) VALUES (?)", row)


def insert_dataset_details(dataset):
   for id in dataset:
      storeData = dataset[id]
      for date in storeData:
         data = storeData[date]
         for row in enumerate(data):
            dataset = Dataset(row[1][0],row[1][1],row[1][2],row[1][3])
            insert_dataset(dataset)


insert_business_hrs('./data_source/business_hours.csv')
print("done")
insert_timezone('./data_source/timezone.csv')
print("done")
insert_store_status('./data_source/store_status.csv')
print("done")
insert_store_id()
insert_dataset_details(dataCreation())
# calender = Calender(datetime.datetime.now())
# print(calender)
# hourly_task(calender.last_hr_start , calender.last_hr_end , calender.date)
# print("done")
# daily_task(calender.last_date)
# weekly_task(calender.last_week_start_date , calender.last_week_end_date)
db_connection.commit()
db_connection.close()    

