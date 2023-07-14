import sqlite3
from datetime import datetime
import time
import schedule
from app.dao.hourly_report_dao import hourly_task
from app.dao.daily_report_dao import daily_task
from app.dao.weekly_report_dao import weekly_task
from database_initialization.database_connection import DatabaseConnection
from utils.calender_utils import Calender
from utils.file_editing_utils import create_csv_file, merge_csv


calender = Calender(datetime.now())

def schedule_jobs():
    # Schedule the hourly task to run every hour
    schedule.every().hour.do(lambda: hourly_task(calender.last_hr_start , calender.last_hr_end , calender.date))
    
    # Schedule the daily task to run at 9:00 AM every day
    schedule.every().day.at("23:59").do(lambda: daily_task(calender.last_date))

    # Schedule the weekly task to run on Mondays at 10:00 AM
    schedule.every().sunday.at("23:59").do(lambda: weekly_task(calender.last_week_start_date , calender.last_week_end_date))
    while True:
     schedule.run_pending()
     time.sleep(1)


# Define a function to check the status of the schedulers
def check_scheduler_status(report_id):
    # Perform action if any scheduler is not running
    while'hourly_scheduler' in schedule.jobs or 'daily_scheduler' in schedule.jobs or 'weekly_scheduler' in schedule.jobs:
        pass

    create_csv_file('hourlyReport', ['store_id','uptime_last_hrs','downtime_last_hrs'])
    create_csv_file('dailyReport', ['store_id','uptime_last_day','downtime_last_day'])
    create_csv_file('weeklyReport', ['store_id','uptime_last_week','downtime_last_week'])
    location = merge_csv(report_id)
    db_connection = DatabaseConnection()

    update_report_data = '''
      UPDATE report set location = ? and status = ? where report_id = ?
    '''

    db_connection.execute_query(update_report_data, (location, "Completed", report_id))
    db_connection.commit()
    db_connection.close()



scheduler = schedule


