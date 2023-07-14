import datetime

import pytz


class Calender:
    def __init__(self, current_timestamp):
        self.date = current_timestamp.strftime('%Y-%m-%d')
        self.time = current_timestamp.strftime('%H:%M')

        rounded_timestamp = current_timestamp.replace(minute=0, second=0, microsecond=0)
        start_timestamp = rounded_timestamp - datetime.timedelta(hours=1)
        end_timestamp = rounded_timestamp - datetime.timedelta(seconds=1)

        self.last_hr_start = start_timestamp.strftime('%H:%M')
        self.last_hr_end =  end_timestamp.strftime('%H:%M')
        self.last_date = (current_timestamp-datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        self.last_week_start_date = (current_timestamp - datetime.timedelta(days=current_timestamp.weekday() + 7)).strftime('%Y-%m-%d')
        self.last_week_end_date = (current_timestamp - datetime.timedelta(days=current_timestamp.weekday() + 1)).strftime('%Y-%m-%d')

def get_utc_to_timezone(time , time_zone):
    time = datetime.strptime(time, "%H:%M")
        # Define the desired timezone
    timezone = pytz.timezone(time_zone)  # Example: New York timezone

        # Convert UTC time to the desired timezone
    standard_time = time.replace(tzinfo=pytz.utc).astimezone(timezone)

        # Format the standard time as a string
    return standard_time.strftime('%H:%M') 