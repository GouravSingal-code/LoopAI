from database_connection import DatabaseConnection
from dao.hourly_report_dao import pool_restaurant_status
from modeling.prediction import prediction
from calender_utils import Calender

def create_dataset_table():
    db_connection = DatabaseConnection()
    create_dataset_table_query = '''
    CREATE TABLE IF NOT EXISTS dataSet (
        store_id TEXT,
        date TEXT,
        time TEXT,
        status TEXT,
        PRIMARY KEY (store_id, date, time)
    )
    '''
    db_connection.execute_query(create_dataset_table_query)
    db_connection.commit()
    db_connection.close()

def insert_dataset(dataset):
    db_connection = DatabaseConnection()
    insert_dataset_query = '''
     INSERT OR REPLACE INTO dataSet
     (store_id, date, time, status)
     VALUES (?, ?, ?, ?)
    '''
    db_connection.execute_query(insert_dataset_query, (dataset.store_id, dataset.date, dataset.time, dataset.status))
    db_connection.commit()
    db_connection.close()




# pool the data from restaurant in every hour
# if we get the response then we allocate the complete hour to that response
# else we predict the response from out machine learning model and then allocate the complete hour to that predicted response

def status_till_now(store_id, date , time):
    db_connection = DatabaseConnection()
    get_status_till_now = '''
      Select dataSet.status from dataSet
      where dataSet.store_id = ? and dataSet.date=? and dataSet.time <= ?
    '''
    db_connection.execute_query(get_status_till_now, (store_id, date, time,))

def previous_day_status(store_id, date):
    db_connection = DatabaseConnection()
    get_previous_day_status = '''
      Select dataSet.status from dataSet
      where dataSet.store_id = ? and dataSet.date=?
    '''
    db_connection.execute_query(get_previous_day_status, (store_id, date,))    

def update_the_dataset():
    db_connection = DatabaseConnection()
    responses = pool_restaurant_status()    
    for response in responses:
        calender = Calender(response.timestamp)
        if response.success == True:
            db_connection.execute_query("INSERT OR REPLACE INTO dataSet (store_id, date, time, status) VALUES (?, ?, ?, ?)", (response.response.store_id,calender.date, calender.time,response.response.status,))
        else:
            #predict 
            # to predict we need =  what happend on previous day and what happend till now on the given day
            data = status_till_now(response.response.store_id, calender.date , response.time)
            data.append(previous_day_status(response.response.store_id, calender.last_date))
            predict = prediction(data)
            db_connection.execute_query("INSERT OR REPLACE INTO dataSet (store_id, date, time, status) VALUES (?, ?, ?, ?)", (response.response.store_id,calender.date, calender.time,predict))
    db_connection.commit()
    db_connection.close()

