from database_connection import DatabaseConnection

def create_store_timezone_table():
    db_connection = DatabaseConnection()
    create_storeTimeZone_table_query = '''
    CREATE TABLE IF NOT EXISTS storeTimeZone (
        store_id BIGINT PRIMARY_KEY,
        timezone TEXT
    )
    '''
    db_connection.execute_query(create_storeTimeZone_table_query)
    db_connection.commit()
    db_connection.close()


def getTimeZone(store_id):
    db_connection = DatabaseConnection()

    get_timeZone = '''
      SELECT * from storeTimeZone
      WHERE store_id = ?
    '''
    return db_connection.execute_query(get_timeZone, (store_id,))


def insert_timezone_details(store_timezone):
    db_connection = DatabaseConnection()
    db_connection.execute_query("INSERT OR REPLACE  INTO storeTimeZone (store_id, timezone) VALUES (?, ?)", (store_timezone.store_id, store_timezone.timezone))
    db_connection.commit()
    db_connection.close()
   

def get_unique_store_timezone_ids():
    db_connection = DatabaseConnection()
    return db_connection.execute_query("SELECT distinct storeTimeZone.store_id FROM storeTimeZone")

