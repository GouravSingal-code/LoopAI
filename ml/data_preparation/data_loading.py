import sys
sys.path.append('../../app')
sys.path.append('../../utils')
from datetime import datetime, timedelta
from dao.store_business_hrs_dao import getBusinessHrs, getNonBusinessHrsDetails
from dao.store_dao import get_store_ids
from dao.store_status_dao import getAvailableStatus, getDate
from dao.store_time_zone_dao import getTimeZone
from step_interpolation_utils import stepInterpolation



def dataCreation():
   start_date = datetime.strptime(getDate("min"), "%Y-%m-%d")
   end_date = datetime.strptime('2023-01-25', "%Y-%m-%d")
   timeZone = 'America/Chicago'
   start_time = '00:00'
   end_time = '23:59'

   stores = get_store_ids()

   idWiseData = {}
   for store in stores:
      store_id = store[0]
      time_zone = getTimeZone(store_id)
      if len(time_zone) > 0:
         time_zone = time_zone[0][1]
      current_date = start_date
      dateWiseData = {}
      while current_date <= end_date:
         date = current_date.strftime("%Y-%m-%d")
         day = current_date.strftime("%A")
         business_hrs = getBusinessHrs(store_id, day)
         if len(business_hrs) > 0:
            start_time = business_hrs[0][2]
            end_time = business_hrs[0][3]
         time_stamps1 , activity_status1  = getNonBusinessHrsDetails("00:00" , start_time)

         # here try to insert the timestamp which are included in business hrs ( so there try to take care of the timezone)
         time_stamps2 , activity_status2 = getAvailableStatus(store_id, date, start_time , end_time, time_zone)
         time_stamps3 , activity_status3 = getNonBusinessHrsDetails(end_time, "23:59")
         time_stamps = time_stamps1 + time_stamps2 + time_stamps3
         activity_status = activity_status1 + activity_status2 + activity_status3
         dateWiseData[current_date] = stepInterpolation(store_id, date, time_stamps , activity_status)
         current_date += timedelta(days=1)
      idWiseData[store_id] = dateWiseData
      break    
   return idWiseData
