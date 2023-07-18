import sqlite3
import threading
import env

class DatabaseConnection:
    def __init__(self):
        self._connection = None

    def get_connection(self):
        if self._connection is None:
            self._connection = sqlite3.connect(env.PATH_DIR + '\\database.db')
        return self._connection

    def execute_query(self, query, params=None):
        connection = self.get_connection()
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

    def commit(self):
        connection = self.get_connection()
        connection.commit()

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None


thread_local = threading.local()

def get_db_connection():
    if not hasattr(thread_local, "db_connection"):
        thread_local.db_connection = DatabaseConnection()
    return thread_local.db_connection