import datetime
from modeling.train import train_model
from dao.store_business_hrs_dao import getBusinessHrs, getNonBusinessHrsDetails
from dao.store_dao import get_store_ids
from dao.store_status_dao import getAvailableStatus, getDate
from dao.store_time_zone_dao import getTimeZone
from step_interpolation_utils import stepInterpolation
import env


def data_set_creation():
   start_date = datetime.datetime.strptime(getDate("min"), "%Y-%m-%d")
   end_date = datetime.datetime.strptime(getDate('max'), "%Y-%m-%d")
   time_zone = env.DEFAULT_TIME_ZONE
   start_time = env.DEFAULT_START_TIME
   end_time = env.DEFAULT_END_TIME

   stores = get_store_ids()
   input_array = []
   output_array = []
   #loop over the every unique store ids
   for store in stores:
      store_id = store[0]
      # get the timezone of particular store_id , if not use default
      timezone = getTimeZone(store_id)
      if len(timezone) > 0:
         time_zone = timezone[0][1]

      current_date = start_date
      # loop over the every date from start date to end date
      while current_date <= end_date:
         date = current_date.strftime("%Y-%m-%d")
         day = current_date.strftime("%A")
         business_hrs = getBusinessHrs(store_id, day)
         if len(business_hrs) > 0:
            start_time = business_hrs[0][2]
            end_time = business_hrs[0][3]

         # for a particular store_id and date , get the available status within business hours and non business hours
         time_stamps1 , activity_status1  = getNonBusinessHrsDetails("00:00" , start_time)
         time_stamps2 , activity_status2 = getAvailableStatus(store_id, date, start_time , end_time, time_zone)
         time_stamps3 , activity_status3 = getNonBusinessHrsDetails(end_time, "23:59")
         time_stamps = time_stamps1 + time_stamps2 + time_stamps3
         activity_status = activity_status1 + activity_status2 + activity_status3

         # interpolate the intervals using step interpolation
         stepInterpolation(store_id, date, time_stamps , activity_status, input_array, output_array)
         current_date += datetime.timedelta(days=1)

   print("calling machine learning model")      
   train_model(input_array, output_array)   
