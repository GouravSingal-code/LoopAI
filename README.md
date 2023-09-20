# LoopAI

# demo link
  https://www.loom.com/share/b8ad71a7e6954b8f94f0c64666273de3?sid=42e0bc14-4325-4e52-b563-6ffa98d1fcd8

# Doc
https://drive.google.com/file/d/1vHDLU0iiwenJ-9hAExydJdIVV1Ijazqz/view?usp=sharing](https://drive.google.com/file/d/1HC2QOxZuZcmJ1Q0kZr_EUQnJoA4JO6eC/view?usp=sharing

# steps to run projects
0) change the location of PATH_DIR in env file.<br/><br/>
1) cd database_initialization/<br/><br/>
2) python migration.py<br/>
  ( create all required tables at one go )<br/><br/>
4) python initialized_data.py <br/><br/>
   ---- this will take some time-----<br/>
   ( push the data present in data source in the subsequent table and in the required table )<br/>
   ( creating the machine learning data set { input , output } )<br/>
   ( training of model using  LSTM  with step interpolation ) <br/><br/>
6) cd .. <br/><br/>
7) python run.py  <br/><br/>
   ( start the 4 scheduler) <br/>
      1) pooling data from restaurant in every hour <br/>
           ----pooling data request for a restaurant----<br/>
           SUCCESS ->  put the status of restaurant in dataset<br/>
           FAILED -> predict the status of restaurant and then put it in dataset<br/>
      3) updating the hourly_report_table in every hour from the data we get from pooling
      4) updating the daily_report_table in every day from the data we get from pooling
      5) updating the weekly_report_table in every week from the data we get from pooling
  


# 2 routes  
1)
     REQUEST ->  /trigger_report , METHOD -> POST <br/>
     RESPONSE -> report_id <br/><br/>
       &nbsp;&nbsp; &nbsp;&nbsp;  push the report details inside with report_table with following report_id  , {status -> Running} , timestamp , {location -> none}<br/>
        &nbsp;&nbsp; &nbsp;&nbsp; check for latest report entry in report_table whose status is completed  and is of same day and same hour<br/>
         &nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; -> if present <br/>
          &nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;   update the location of report to latest_report_location<br/>
          &nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;   make the status completed<br/>
         &nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; -> if not <br/>
           &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp;   create hourly , daily and weekly csv file from respective table<br/>
           &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp;   merge all 3 files and get the location<br/>
           &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp;   update the status(completed) and location (merge file location)<br/>
          <br/>
     
2)
     REQUEST -> /get_report?report_id = {report_id from trigger_report }   ,METHOD -> GET <br/>
     RESPONSE -> csv file  <br/><br/>
      &nbsp;&nbsp; &nbsp;&nbsp;            format of csv file <br/>
      &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp;             {store_id, uptime_last_hr , downtime_last_hr , uptime_last_day , downtime_last_day , uptime_last_week , downtime_last_week}<br/>
      <br/>
       &nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;      report status is running  ,then return "Running"<br/>
       &nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;        report status is completed , then return csv file from the location of report     <br/> 

                  
