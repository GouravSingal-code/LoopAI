
from calender_utils import get_utc_to_local_timezone
from database_connection import DatabaseConnection



def create_store_status_table():
    db_connection = DatabaseConnection()
    create_storeStatus_table_query = '''
    CREATE TABLE IF NOT EXISTS storeStatus (
        store_id BIGINT,
        status TEXT,
        timeStamp_utc DATETIME,
        date TEXT,
        time TEXT,
        day INTEGER,
        PRIMARY KEY (store_id, date, time)
    )
    '''
    db_connection.execute_query(create_storeStatus_table_query)
    db_connection.commit()
    db_connection.close()

def getDate(type):
    db_connection = DatabaseConnection()
    get_date = '''
     Select Min(date) from storeStatus
     ''' if type == "min" else '''
     Select Max(date) from storeStatus
     '''
    rows = db_connection.execute_query(get_date)
    return rows[0][0] 


def getAvailableStatus(store_id , date , start_time , end_time, time_zone):
    db_connection = DatabaseConnection()
    get_available_status = '''
      SELECT * from storeStatus
      WHERE store_id = ?
      AND date = ? order by time
    '''
    availableStatus = db_connection.execute_query(get_available_status, (store_id, date))
    time_stamps = []
    activity_status = []
    for row in availableStatus:
      standard_time = get_utc_to_local_timezone(row[4] , time_zone)
      if start_time < standard_time < end_time:
         time_stamps.append(standard_time)
         activity_status.append(1 if row[1] =='active' else 0) # status
    return time_stamps , activity_status


def insert_store_status_details(store_status):
    db_connection = DatabaseConnection()
    db_connection.execute_query("INSERT OR REPLACE  INTO storeStatus (store_id, status, timeStamp_utc, date, time, day) VALUES (?, ?, ?, ?, ?, ?)", (store_status.store_id, store_status.status, store_status.timeStamp_utc, store_status.date, store_status.time, store_status.day))
    db_connection.commit()
    db_connection.close()



def get_unique_store_status_ids():
    db_connection = DatabaseConnection()
    return db_connection.execute_query("SELECT distinct storeStatus.store_id FROM storeStatus")

