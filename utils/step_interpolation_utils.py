import env
import pandas as pd
from database_connection import get_db_connection
from list_generator_utils import randomListGenerator, zeroListGenerator


def stepInterpolation(store_id, date, time_stamps , activity_status, input, output):
   df = pd.DataFrame({'timestamp': pd.to_datetime(time_stamps , format="%H:%M"), 'activity_status': activity_status})
   df.set_index('timestamp', inplace=True)
   df_interpolated = df.resample(str(env.STEP_INTERPOLATION_VALUE)+'T').interpolate(method='pad').bfill()
   df_interpolated.reset_index(inplace=True)
   db_connection = get_db_connection()
   
   list_size = 1440/env.STEP_INTERPOLATION_VALUE
   previous = randomListGenerator(list_size)
   current = [0]
   for index, row in df_interpolated.iterrows():

      #creating a input and output dataset for training purpose of machine learning model
      input1 = current + zeroListGenerator(list_size-len(current))
      input2 = [previous[index]]
      input.append(input1 + input2)
      output.append([row['timestamp'].strftime('%H:%M')])
      current.append(row['timestamp'].strftime('%H:%M'))

      # inserting the data into dataset table      
      db_connection.execute_query("INSERT OR REPLACE INTO dataSet (store_id, date, time, status) VALUES (?, ?, ?, ?)", (store_id,date, row['timestamp'].strftime('%H:%M'),row['activity_status'],))
   db_connection.commit()
   db_connection.close()
