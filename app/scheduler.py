import sys,time,schedule,env
from datetime import datetime
from app.dao.hourly_report_dao import hourly_task
from app.dao.daily_report_dao import daily_task
from app.dao.weekly_report_dao import weekly_task
from utils.calender_utils import Calender
from utils.file_editing_utils import create_csv_file, merge_csv
from app.dao.report_dao import update_report
from app.dao.dataset_dao import update_the_dataset


# creating a schedule task in the interval of 1 hr  , 1 day and 1 week , which will update the hourly , daily and weekly report_table
# and also update the dataset table based on the data received from restaurants ( this is also called in every hr  , and to each restaurant)
def schedule_jobs():
    schedule.every().hour.do(lambda: update_the_dataset())
    schedule.every().hour.do(lambda: hourly_task(calender.last_hr_start , calender.last_hr_end , calender.date))
    schedule.every().day.at("23:59").do(lambda: daily_task(calender.last_date))
    schedule.every().sunday.at("23:59").do(lambda: weekly_task(calender.last_week_start_date , calender.last_week_end_date))
    while True:
     schedule.run_pending()
     time.sleep(1)



# create csv file for each task when no schedule is running 
def check_scheduler_status(report_id,time_stamp):
    while'hourly_scheduler' in schedule.jobs or 'daily_scheduler' in schedule.jobs or 'weekly_scheduler' in schedule.jobs:
        pass
    create_csv_file(env.HOURLY_TASK_CSV, ['store_id','uptime_last_hrs','downtime_last_hrs'])
    create_csv_file(env.DAILY_TASK_CSV, ['store_id','uptime_last_day','downtime_last_day'])
    create_csv_file(env.WEEKLY_TASK_CSV, ['store_id','uptime_last_week','downtime_last_week'])
    location = merge_csv(report_id)
    update_report(location, report_id, time_stamp)


