import datetime
from database_connection import get_db_connection

def create_store_business_hrs_table():
    db_connection = get_db_connection()
    create_storeBusinessHrs_table_query = '''
    CREATE TABLE IF NOT EXISTS storeBusinessHrs (
        store_id BIGINT,
        day INTEGER,
        start_time DATETIME,
        end_time DATETIME,
        PRIMARY KEY (store_id, day)
    )
    '''
    db_connection.execute_query(create_storeBusinessHrs_table_query)
    db_connection.commit()
    db_connection.close()


def getBusinessHrs(store_id , day):
    db_connection = get_db_connection()

    get_business_hrs = '''
      SELECT * from storeBusinessHrs
      WHERE store_id = ?
      AND day = ?
    '''
    return db_connection.execute_query(get_business_hrs, (store_id, day))


def getNonBusinessHrsDetails(start_time , end_time):
   time = datetime.datetime.strptime(start_time, "%H:%M")
   increment = datetime.timedelta(minutes=1)
   time_stamps = []
   activity_status = []

   while True:
      time_stamps.append(time.strftime("%H:%M")) # time
      activity_status.append(0)
      if time.strftime("%H:%M") == end_time[0:5]:
         break    
      time += increment
   return time_stamps, activity_status


def insert_business_hrs_details(store_business_hr):
    db_connection = get_db_connection()
    db_connection.execute_query("INSERT OR REPLACE  INTO storeBusinessHrs (store_id, day, start_time , end_time) VALUES (?, ?, ?, ?)", (store_business_hr.store_id, store_business_hr.day, store_business_hr.start_time, store_business_hr.end_time))
    db_connection.commit()
    db_connection.close()
   


def get_unique_store_business_hrs_ids():
    db_connection = get_db_connection()
    return db_connection.execute_query("SELECT distinct storeBusinessHrs.store_id FROM storeBusinessHrs")

