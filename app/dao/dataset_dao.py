import sys
sys.path.append('../../database_initialization')

from database_connection import DatabaseConnection


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