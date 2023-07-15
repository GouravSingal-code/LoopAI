import os
import sqlite3
import csv
import pandas as pd
import env
from database_initialization.database_connection import DatabaseConnection



#create a csv file for the given table
def create_csv_file(table_name,column_names):
    db_connection = DatabaseConnection()
    fetch_data = 'SELECT * FROM {}'.format(table_name)
    rows = db_connection.execute_query(fetch_data)
    csv_filename = table_name + '.csv'
    with open(csv_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(column_names)
        csv_writer.writerows(rows)
    db_connection.commit()    
    db_connection.close()    

# merge all 3 csv files
def merge_csv(id):
    csv_file1 = env.HOURLY_TASK_CSV + '.csv'
    csv_file2 = env.DAILY_TASK_CSV + '.csv'
    csv_file3 = env.WEEKLY_TASK_CSV + '.csv'
    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)
    df3 = pd.read_csv(csv_file3)
    merged_df = df1.merge(df2, on='store_id').merge(df3, on='store_id')
    merged_csv_filename = str(id) + '.csv'
    merged_df.to_csv(merged_csv_filename, index=False)
    return os.path.abspath(merged_csv_filename)