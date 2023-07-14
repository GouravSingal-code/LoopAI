import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('database.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

create_table_query = '''
DROP TABLE hourlyReport
'''

cursor.execute(create_table_query)