# LoopAI

#steps to run projects
1) cd database_initialization/
2) python migration.py
  ( create all required tables at one go )
4) python initialized_data.py
---- this will take some time  -----
( push the data present in data source in the subsequent table and in the required table )
( creating the machine learning data set { input , output } )
( training of model using  LSTM  with step interpolation )
5) cd ..
6) python run.py
   ( start the 4 scheduler)
      1) pooling data from restaurant in every hour
         # pooling data request for a restaurant
              SUCCESS ->  put the status of restaurant in dataset
              FAILED -> predict the status of restaurant and then put it in dataset
      3) updating the hourly_report_table in every hour from the data we get from pooling
      4) updating the daily_report_table in every day from the data we get from pooling
      5) updating the weekly_report_table in every week from the data we get from pooling
  


2 routes  
1)
     REQUEST ->  /trigger_report , METHOD -> POST
     RESPONSE -> report_id

     # push the report details inside with report_table with following report_id  , {status -> Running} , timestamp , {location -> none}
     # check for latest report entry in report_table whose status is completed  and is of same day and same hour
        -> if present 
              update the location of report to latest_report_location
              make the status completed
        -> if not
              create hourly , daily and weekly csv file from respective table
              merge all 3 files and get the location
              update the status(completed) and location (merge file location)
          
     
2)
     REQUEST -> /get_report?report_id = {report_id from trigger_report }   ,METHOD -> GET
     RESPONSE -> csv file 
                # format of csv file
                  store_id, uptime_last_hr , downtime_last_hr , uptime_last_day , downtime_last_day , uptime_last_week , downtime_last_week


     #  report status is running  ,then return running
     #  report status is completed , then return csv file from the location of report      

                  
