import asyncio, aiohttp
from get_urls_utils import get_urls
from database_connection import DatabaseConnection
import env


def create_hourly_report_table():
    db_connection = DatabaseConnection()
    create_hourly_report_table_query = '''
    CREATE TABLE IF NOT EXISTS hourlyReport (
        store_id BIGINT PRIMARY KEY,
        uptime_last_hrs INTEGER,
        downtime_last_hrs INTEGER
    )
    '''
    db_connection.execute_query(create_hourly_report_table_query)
    db_connection.commit()
    db_connection.close()

def hourly_task(last_hr_start , last_hr_end , date):
    db_connection = DatabaseConnection()
    get_data = '''
    SELECT dataSet.store_id,
        SUM(CASE WHEN time >= ? AND time <= ? AND date = ? THEN Cast(status as int)*? ELSE 0 END) AS uptime_last_hr,
        SUM(CASE WHEN time >= ? AND time <= ? AND date = ? AND Cast(status as int) == 0 THEN 1*? ELSE 0 END) AS downtime_last_hr
    FROM dataSet group by store_id;
    '''
    rows = db_connection.execute_query(get_data, (last_hr_start, last_hr_end , date , env.STEP_INTERPOLATION_VALUE, last_hr_start, last_hr_end , date, env.STEP_INTERPOLATION_VALUE))
    for row in rows:
        db_connection.execute_query("INSERT OR REPLACE INTO hourlyReport (store_id, uptime_last_hrs, downtime_last_hrs) VALUES (?, ?, ?)", row)
    db_connection.commit()
    db_connection.close()


def pool_restaurant_status():
    async def fetch(session, url):
        async with session.get(url) as response:
            if response.status >= 200 and response.status < 300:
                # Successful response
                if 'application/json' not in response.headers.get('Content-Type', ''):
                    response_text = await response.text()
                    return {'success':True, 'time':datetime.datetime.now().strftime('%H:%M') , 'date':datetime.datetime.now().strftime('%Y-%m-%d'), response:response_text}
                else:
                    return {'success':True, 'time':datetime.datetime.now().strftime('%H:%M') , 'date':datetime.datetime.now().strftime('%Y-%m-%d'), response:await response.json()}
            else:
                # Unsuccessful response
                return {'success':False, 'time':datetime.datetime.now().strftime('%H:%M') , 'date':datetime.datetime.now().strftime('%Y-%m-%d'),  response:{store_id:url.split('/')[-1]}}

    async def make_api_calls(urls):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                task = asyncio.create_task(fetch(session, url))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
            return responses       

    urls = get_urls()
    return asyncio.run(make_api_calls(urls))

