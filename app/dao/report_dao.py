from database_connection import DatabaseConnection

def create_report_table():
    db_connection = DatabaseConnection()
    create_report_table_query = '''
    CREATE TABLE IF NOT EXISTS report (
        report_id TEXT PRIMARY KEY,
        time_stamp DATETIME,
        status TEXT,
        location TEXT
    )
    '''
    db_connection.execute_query(create_report_table_query)
    db_connection.commit()
    db_connection.close()


def get_report_status_location(report_id):
    db_connection = DatabaseConnection()
    print(report_id)
    rows = db_connection.execute_query("SELECT report.status,report.location FROM report WHERE report_id=?", (report_id,))
    return rows


def get_last_report(timeStamp):
    db_connection = DatabaseConnection()
    get_last_report_id_details = '''
      SELECT * from report where status == ? AND strftime('%H', report.time_stamp) = strftime('%H', ?)
      AND date(report.time_stamp) = date(?) ORDER BY time_stamp DESC LIMIT 1 
   '''
    row = db_connection.execute_query(get_last_report_id_details , ("Completed" , timeStamp, timeStamp))
    return row

def insert_report(report):
    db_connection = DatabaseConnection()
    insert_report_query = '''
    INSERT OR REPLACE INTO report (report_id, time_stamp, status, location)
    VALUES (?, ?, ?, ?);
    '''
    db_connection.execute_query(insert_report_query, (report.report_id, report.time_stamp, report.status, report.location))
    db_connection.commit()
    db_connection.close()



def update_report(location, report_id, timestamp):
    db_connection = DatabaseConnection()
    insert_report_query = '''
    INSERT OR REPLACE INTO report (report_id, time_stamp, status, location)
    VALUES (?, ?, ?, ?);
    '''
    db_connection.execute_query(insert_report_query, (report_id, timestamp, "Completed", location))
    db_connection.commit()
    db_connection.close()  