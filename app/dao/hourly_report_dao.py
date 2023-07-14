
import sys
sys.path.append('../../database_initialization')

from database_connection import DatabaseConnection

def create_hourly_report_table():
    db_connection = DatabaseConnection()
    create_hourly_report_table_query = '''
    CREATE TABLE IF NOT EXISTS hourlyReport (
        store_id BIGINT PRIMARY KEY,
        uptime_last_hrs INTEGER,
        downtime_last_hrs INTEGER
    )
    '''
    db_connection.execute_query(create_hourly_report_table_query)
    db_connection.commit()
    db_connection.close()

def hourly_task(last_hr_start , last_hr_end , date):
    print(1)
    db_connection = DatabaseConnection()
    get_data = '''
    SELECT dataSet.store_id,
        SUM(CASE WHEN time >= ? AND time <= ? AND date = ? THEN Cast(status as int) ELSE 0 END) AS uptime_last_hr,
        SUM(CASE WHEN time >= ? AND time <= ? AND date = ? AND Cast(status as int) == 0 THEN 1 ELSE 0 END) AS downtime_last_hr
    FROM dataSet group by store_id;
    '''
    rows = db_connection.execute_query(get_data, (last_hr_start, last_hr_end , date , last_hr_start, last_hr_end , date))
    for row in rows:
        print(rows)
        db_connection.execute_query("INSERT OR REPLACE INTO hourlyReport (store_id, uptime_last_hrs, downtime_last_hrs) VALUES (?, ?, ?)", row)
    db_connection.commit()
    db_connection.close()
