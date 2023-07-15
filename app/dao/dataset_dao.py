from database_connection import DatabaseConnection
from dao.hourly_report_dao import pool_restaurant_status

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



# def update_the_dataset():
#     db_connection = DatabaseConnection()
#     responses = pool_restaurant_status()    
#     for response in responses:
#         if response.success == True:
#             db_connection.execute_query("INSERT OR REPLACE INTO dataSet (store_id, date, time, status) VALUES (?, ?, ?, ?)", (response.response.store_id,response.date, response.time,response.response.status,))
#         else:
#             #predict 
#             # to predict we need =  what happend on previous day and what happend till now on the given day
#             db_connection.execute_query("INSERT OR REPLACE INTO dataSet (store_id, date, time, status) VALUES (?, ?, ?, ?)", (response.response.store_id,response.date, response.time,prediction))
#     db_connection.commit()
#     db_connection.close()

