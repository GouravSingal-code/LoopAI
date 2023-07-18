from database_connection import get_db_connection

def create_store_table():
    db_connection = get_db_connection()
    create_store_query = '''
    CREATE TABLE IF NOT EXISTS store (
        store_id BIGINT PRIMARY KEY
    )
    '''
    db_connection.execute_query(create_store_query)
    db_connection.commit()
    db_connection.close()

def get_store_ids():
    db_connection = get_db_connection()
    get_store_id = '''
     SELECT * from store
    '''
    return db_connection.execute_query(get_store_id)


def insert_store_id(store):
    db_connection = get_db_connection()       
    db_connection.execute_query("INSERT OR REPLACE  INTO Store (store_id) VALUES (?)", (store.store_id,))
    db_connection.commit()
    db_connection.close()
