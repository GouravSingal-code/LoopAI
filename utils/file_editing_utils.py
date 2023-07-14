import os
import sqlite3
import csv
import pandas as pd

from database_initialization.database_connection import DatabaseConnection
# Connect to the SQLite database



def create_csv_file(table_name,column_names):
    db_connection = DatabaseConnection()
    fetch_data = 'SELECT * FROM {}'.format(table_name)
    # Execute a query to fetch the data from the database
    rows = db_connection.execute_query(fetch_data)
    # Fetch all rows of the result
    
    # Specify the path and filename for the CSV file
    csv_filename = table_name + '.csv'

    # Open the CSV file in write mode
    with open(csv_filename, 'w', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write the column names to the CSV file
        csv_writer.writerow(column_names)

        # Write the data rows to the CSV file
        csv_writer.writerows(rows)

    db_connection.commit()    
    db_connection.close()    


def merge_csv(id):
    # Define the filenames of the CSV files
    csv_file1 = 'hourlyReport.csv'
    csv_file2 = 'dailyReport.csv'
    csv_file3 = 'weeklyReport.csv'

    # Read the CSV files into pandas DataFrames
    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)
    df3 = pd.read_csv(csv_file3)

    # Concatenate the DataFrames while excluding duplicate entries from the common column
    merged_df = pd.concat([df1, df2, df3]).drop_duplicates(subset='store_id')

    # Specify the filename for the merged CSV file
    merged_csv_filename = str(id) + '.csv'

    # Write the merged DataFrame to a new CSV file
    merged_df.to_csv(merged_csv_filename, index=False)
    return os.path.abspath(merged_csv_filename)