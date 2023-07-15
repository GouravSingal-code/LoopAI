import sys
sys.path.append('c:\\Users\\GOURAV\\Desktop\\loopAI')
sys.path.append('c:\\Users\\GOURAV\\Desktop\\loopAI\\app')
sys.path.append('c:\\Users\\GOURAV\\Desktop\\loopAI\\data_source')
sys.path.append('c:\\Users\\GOURAV\\Desktop\\loopAI\\database_initialization')
sys.path.append('c:\\Users\\GOURAV\\Desktop\\loopAI\\ml')
sys.path.append('c:\\Users\\GOURAV\\Desktop\\loopAI\\utils')

from dao.daily_report_dao import create_daily_report_table
from dao.dataset_dao import create_dataset_table
from dao.hourly_report_dao import create_hourly_report_table
from dao.report_dao import create_report_table
from dao.store_business_hrs_dao import create_store_business_hrs_table
from dao.store_dao import create_store_table
from dao.store_status_dao import create_store_status_table
from dao.store_time_zone_dao import create_store_timezone_table
from dao.weekly_report_dao import create_weekly_report_table

create_daily_report_table()
create_dataset_table()
create_hourly_report_table()
create_report_table()
create_store_business_hrs_table()
create_store_table()
create_store_status_table()
create_store_timezone_table()
create_weekly_report_table()
