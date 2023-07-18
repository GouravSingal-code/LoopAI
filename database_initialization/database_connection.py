import sqlite3

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = None
        return cls._instance

    def get_connection(self):
        self.conn = sqlite3.connect('C:\\Users\\GOURAV\\Desktop\\loopAI\\database.db')
        return self.conn

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
        if self.conn:
            self.conn.close()
            self.conn = None