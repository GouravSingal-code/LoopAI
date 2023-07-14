import pandas as pd

def stepInterpolation(store_id, date, time_stamps , activity_status):
   df = pd.DataFrame({'timestamp': pd.to_datetime(time_stamps , format="%H:%M"), 'activity_status': activity_status})
   df.set_index('timestamp', inplace=True)
   df_interpolated = df.resample('1T').interpolate(method='pad').bfill()
   df_interpolated.reset_index(inplace=True)
   data = []
   for _, row in df_interpolated.iterrows():
      datarow = []
      datarow.append(store_id)
      datarow.append(date)
      datarow.append(row['timestamp'].strftime('%H:%M'))
      datarow.append(row['activity_status'])
      data.append(datarow)
   return data
