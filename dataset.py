import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import random

from app.models.dataset import Dataset
from app.dao.dataset_dao import insert_dataset

# Connect to the SQLite database
conn = sqlite3.connect('database.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()


def getDate(type):
   get_date = '''
     Select Min(date) from storeStatus
     ''' if type == "min" else '''
     Select Max(date) from storeStatus
     '''
   cursor.execute(get_date)
   rows = cursor.fetchall()
   return rows[0][0] 

def getTimeZone(store_id):
   get_timeZone = '''
      SELECT * from StoreTimeZone
      WHERE store_id = ?
   '''
   cursor.execute(get_timeZone, (store_id,))
   return cursor.fetchall()

def getBusinessHrs(store_id , day):
   get_business_hrs = '''
      SELECT * from StoreBusinessHrs
      WHERE store_id = ?
      AND day = ?
   '''
   cursor.execute(get_business_hrs, (store_id, day))
   return cursor.fetchall()

import pytz
from datetime import datetime

def get_utc_to_timezone(time , time_zone):
   time = datetime.strptime(time, "%H:%M")
   # Define the desired timezone
   timezone = pytz.timezone(time_zone)  # Example: New York timezone

   # Convert UTC time to the desired timezone
   standard_time = time.replace(tzinfo=pytz.utc).astimezone(timezone)

   # Format the standard time as a string
   return standard_time.strftime('%H:%M')


def getAvailableStatus(store_id , date , start_time , end_time, time_zone):
   get_available_status = '''
      SELECT * from StoreStatus
      WHERE store_id = ?
      AND date = ? order by time
   '''
   cursor.execute(get_available_status, (store_id, date))
   availableStatus =  cursor.fetchall()
   time_stamps = []
   activity_status = []
   for row in availableStatus:
      standard_time = get_utc_to_timezone(row[4] , time_zone)
      if start_time < standard_time < end_time:
         time_stamps.append(standard_time)
         activity_status.append(1 if row[1] =='active' else 0) # status
   return time_stamps , activity_status

def getNonBusinessHrsDetails(start_time , end_time):
   time = datetime.strptime(start_time, "%H:%M")
   increment = timedelta(minutes=1)
   time_stamps = []
   activity_status = []

   while True:
      time_stamps.append(time.strftime("%H:%M")) # time
      activity_status.append(0)
      if time.strftime("%H:%M") == end_time[0:5]:
         break    
      time += increment
   return time_stamps, activity_status

def stepInterpolation(store_id, date, time_stamps , activity_status):
   df = pd.DataFrame({'timestamp': pd.to_datetime(time_stamps , format="%H:%M"), 'activity_status': activity_status})
   df.set_index('timestamp', inplace=True)
   df_interpolated = df.resample('60T').interpolate(method='pad').bfill()
   df_interpolated.reset_index(inplace=True)
   data = []
   for _, row in df_interpolated.iterrows():
      print(row['timestamp'])
      datarow = []
      datarow.append(store_id)
      datarow.append(date)
      datarow.append(row['timestamp'].strftime('%H:%M'))
      datarow.append(row['activity_status'])
      data.append(datarow)
   return data

def dataProcessing():
   start_date = datetime.strptime(getDate("min"), "%Y-%m-%d")
   end_date = datetime.strptime('2023-01-25', "%Y-%m-%d")
   timeZone = 'America/Chicago'
   start_time = '00:00'
   end_time = '23:59'
   get_store_id = '''
    SELECT * from store
   '''
   cursor.execute(get_store_id)
   rows = cursor.fetchall()

   idWiseData = {}
   for row in rows:
      store_id = row[0]
      time_zone = getTimeZone(store_id)
      if len(time_zone) > 0:
         time_zone = time_zone[0][1]
      current_date = start_date
      dateWiseData = {}
      while current_date <= end_date:
         date = current_date.strftime("%Y-%m-%d")
         day = current_date.strftime("%A")
         business_hrs = getBusinessHrs(store_id, day)
         if len(business_hrs) > 0:
            start_time = business_hrs[0][2]
            end_time = business_hrs[0][3]
         time_stamps1 , activity_status1  = getNonBusinessHrsDetails("00:00" , start_time)

         # here try to insert the timestamp which are included in business hrs ( so there try to take care of the timezone)
         time_stamps2 , activity_status2 = getAvailableStatus(store_id, date, start_time , end_time, time_zone)
         time_stamps3 , activity_status3 = getNonBusinessHrsDetails(end_time, "23:59")
         time_stamps = time_stamps1 + time_stamps2 + time_stamps3
         activity_status = activity_status1 + activity_status2 + activity_status3
         dateWiseData[current_date] = stepInterpolation(store_id, date, time_stamps , activity_status)
         current_date += timedelta(days=1)
      idWiseData[store_id] = dateWiseData 
      break; 
   return idWiseData

def randomListGenerator(sz):
   return [random.randint(0,1) for _ in range(sz)]

def zeroListGenerator(sz):
   return [0 for _ in range(sz)]

def createSampleSet(dataset):
   input = []
   output = []
   for id in dataset:
      storeData = dataset[id]
      for date in storeData:
         data = storeData[date]
         previous = randomListGenerator(1440)
         current = [0]
         for index , row in enumerate(data):
            input1 = current + zeroListGenerator(1440-len(current))
            input2 = [previous[index]]
            input.append(input1 + input2)
            output.append([row[3]])
            dataset = Dataset(row[0],row[1],row[2],row[3])
            insert_dataset(dataset)
            current.append(row[3])
         current.pop(0)
         previous = current
   return input , output     

print("a")
dataset = dataProcessing()
print("a")
input, output = createSampleSet(dataset)
print("c")

import json

# Open the file in write mode
with open('input.txt', 'w') as file:
    # Write the array to the file using json.dump()
    json.dump(input, file)

# Open the file in write mode
with open('output.txt', 'w') as file:
    # Write the array to the file using json.dump()
    json.dump(output, file)