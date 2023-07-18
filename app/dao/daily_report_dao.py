from database_connection import get_db_connection
import env


def create_daily_report_table():
    db_connection = get_db_connection()
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
    db_connection = get_db_connection()
    get_data = '''
    SELECT dataSet.store_id,
        SUM(CASE WHEN  date = ? THEN Cast(status as int)*? ELSE 0 END) AS uptime_last_day,
        SUM(CASE WHEN  date = ? AND Cast(status as int) == 0 THEN 1*? ELSE 0 END) AS downtime_last_day
    FROM dataSet group by store_id;
    '''
    rows = db_connection.execute_query(get_data, (last_date, env.STEP_INTERPOLATION_VALUE, last_date, env.STEP_INTERPOLATION_VALUE))
    for row in rows:
        db_connection.execute_query("INSERT OR REPLACE INTO dailyReport (store_id, uptime_last_day, downtime_last_day) VALUES (?, ?, ?)", row)
    db_connection.commit()
    db_connection.close()