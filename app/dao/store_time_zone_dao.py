from database_connection import get_db_connection

def create_store_timezone_table():
    db_connection = get_db_connection()
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
    db_connection = get_db_connection()

    get_timeZone = '''
      SELECT * from storeTimeZone
      WHERE store_id = ?
    '''
    return db_connection.execute_query(get_timeZone, (store_id,))


def insert_timezone_details(store_timezone):
    db_connection = get_db_connection()
    db_connection.execute_query("INSERT OR REPLACE  INTO storeTimeZone (store_id, timezone) VALUES (?, ?)", (store_timezone.store_id, store_timezone.timezone))
    db_connection.commit()
    db_connection.close()
   

def get_unique_store_timezone_ids():
    db_connection = get_db_connection()
    return db_connection.execute_query("SELECT distinct storeTimeZone.store_id FROM storeTimeZone")

