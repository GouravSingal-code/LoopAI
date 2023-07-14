import sys
sys.path.append('../../database_initialization')

from database_connection import DatabaseConnection

def create_daily_report_table():
    db_connection = DatabaseConnection()
    create_daily_report_table_query = '''
    CREATE TABLE IF NOT EXISTS dailyReport (
        store_id BIGINT PRIMARY KEY,
        uptime_last_day INTEGER,
        downtime_last_day INTEGER
    )
    '''
    db_connection.execute_query(create_daily_report_table_query)
    db_connection.commit()
    db_connection.close()

def daily_task(last_date):
    db_connection = DatabaseConnection()

    get_data = '''
    SELECT dataSet.store_id,
        SUM(CASE WHEN  date = ? THEN Cast(status as int) ELSE 0 END) AS uptime_last_day,
        SUM(CASE WHEN  date = ? AND Cast(status as int) == 0 THEN 1 ELSE 0 END) AS downtime_last_day
    FROM dataSet group by store_id;
    '''

    rows = db_connection.execute_query(get_data, (last_date,last_date))
    for row in rows:
        db_connection.execute_query("INSERT OR REPLACE INTO dailyReport (store_id, uptime_last_day, downtime_last_day) VALUES (?, ?, ?)", row)
    db_connection.commit()
    db_connection.close()