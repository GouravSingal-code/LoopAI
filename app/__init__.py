import sys, datetime,os 
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import env
sys.path.append(env.PATH_DIR  + '\\app')
sys.path.append(env.PATH_DIR  + '\\data_source')
sys.path.append(env.PATH_DIR  + '\\database_initialization')
sys.path.append(env.PATH_DIR  + '\\ml')
sys.path.append(env.PATH_DIR  + '\\utils')

from flask import Flask
from app.scheduler import schedule_jobs
from utils.calender_utils import Calender
from app.dao.hourly_report_dao import hourly_task
from app.dao.daily_report_dao import daily_task
from app.dao.weekly_report_dao import weekly_task
from .controllers.trigger_report import trigger_report_route
from .controllers.get_report import get_report_route

app = Flask(__name__)

app.register_blueprint(trigger_report_route)
app.register_blueprint(get_report_route)


# initialized the hourly , daily and weekly report table
calender = Calender(datetime.datetime.now())
hourly_task(calender.last_hr_start , calender.last_hr_end , calender.date)
daily_task(calender.last_date)
weekly_task(calender.last_week_start_date , calender.last_week_end_date)

# schedule jobs
if __name__ == "__main__":
    schedule_jobs()
