import sys
sys.path.append('../../database_initialization')

from database_connection import DatabaseConnection

def create_weekly_report_table():
    db_connection = DatabaseConnection()

    create_weekly_report_table_query = '''
    CREATE TABLE IF NOT EXISTS weeklyReport (
        store_id BIGINT PRIMARY KEY,
        uptime_last_week INTEGER,
        downtime_last_week INTEGER
    )
    '''
    db_connection.execute_query(create_weekly_report_table_query)  
    db_connection.commit()
    db_connection.close()


def weekly_task(last_week_start_date , last_week_end_date):
    db_connection = DatabaseConnection()

    get_data = '''
    SELECT dataSet.store_id,
        SUM(CASE WHEN date >= ? AND date <= ? THEN Cast(status as int) ELSE 0 END) AS uptime_last_week,
        SUM(CASE WHEN date >= ? AND date <= ? AND Cast(status as int) == 0 THEN 1 ELSE 0 END) AS downtime_last_week
    FROM dataSet group by store_id;
    '''

    rows = db_connection.execute_query(get_data, (last_week_start_date, last_week_end_date, last_week_start_date, last_week_end_date))
    for row in rows:
        db_connection.execute_query("INSERT OR REPLACE INTO weeklyReport (store_id, uptime_last_week, downtime_last_week) VALUES (?, ?, ?)", row)
    db_connection.commit()
    db_connection.close()
