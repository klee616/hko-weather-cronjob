# DB Connection: postgresql://postgres:rENiFXjjqHtlqZL3@db.clsojwhxubumoipbcwyb.supabase.co:5432/postgres
#host=db.clsojwhxubumoipbcwyb.supabase.co
#port=5432
#database=postgres
#user=postgres
#password=rENiFXjjqHtlqZL3

# Get Json from api
# Hong Kong Weather API = https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en

from datetime import datetime
from zoneinfo import ZoneInfo

import requests
import uuid
import sys
from psycopg2.extras import Json
# main.py
from weather_dao import get_lastest_weather_snapshot, insert_weather_snapshot, insert_lightning, insert_rainfall, insert_temperature, insert_humidity, insert_uvindex



def corn_job() -> dict:

    url='https://data.weather.gov.hk/weatherAPI/opendata/weather.php'

    params = dict(
        dataType='rhrread',
        lang='en'
    )

    resp = requests.get(url=url, params=params)

    data = resp.json()

    print(data)

    batch_id = str(uuid.uuid4())
    inserted_at_hk = datetime.now(ZoneInfo('Asia/Hong_Kong')).strftime(
        '%Y-%m-%d %H:%M:%S'
    )

    # Get last recor
    lastest_weather = get_lastest_weather_snapshot() 
    print(f"lastest_weather: {lastest_weather.get('data').get('updateTime')}")
    print(f"JSON updateTime: {data.get('updateTime')}")
    print(lastest_weather.get('data').get('updateTime') ==data.get('updateTime'))
    if lastest_weather.get('data').get('updateTime') ==data.get('updateTime') :
        sys.exit()

    print('run')

    # Parpare master record (weather_snapshots)
    master_record = {
        'weather_snapshots': batch_id,
        'update_time': data.get('updateTime'),
        'icon':data.get('icon')[0],
        'icon_update_time':data.get('iconUpdateTime'),
        'warning_message':data.get('warningMessage'),
        'mintemp_from00_to09':data.get('mintempFrom00To09'),
        'rainfall_from00_to12':data.get('rainfallFrom00To12'),
        'rainfall_last_month':data.get('rainfallLastMonth'),
        'rainfall_january_to_last_month':data.get('rainfallJanuaryToLastMonth'),
        'tcmessage':data.get('tcmessage'),
        'json': data,
    }
    success = insert_weather_snapshot(master_record)

    #lightning
    lightning_obj = data.get('lightning') or {}
    lightning_start_time = lightning_obj.get('startTime')
    lightning_end_time = lightning_obj.get('endTime')
    lightning_items = lightning_obj.get('data') or []

    lightning_data = []
    for item in lightning_items:
        lightning_data.append({
            'batch_id': batch_id,
            'place': item.get('place'),
            'occur': True if str(item.get('occur')).lower() == 'true' else False, 
            'start_time': lightning_start_time,  
            'end_time': lightning_end_time      
        })


    success = insert_lightning(lightning_data)

    #rainfall
    rainfall_obj = data.get('rainfall') or {}
    rainfall_start_time = rainfall_obj.get('startTime')
    rainfall_end_time = rainfall_obj.get('endTime')
    rainfall_items = rainfall_obj.get('data') or []

    rainfall_data = []
    for item in rainfall_items:
        rainfall_data.append({
            'batch_id': batch_id,
            'unit': item.get('unit'),
            'place': item.get('place'),
            'max': item.get('max'),
            'min': item.get('min'),
            'main': item.get('main'),
            'start_time': rainfall_start_time,  
            'end_time': rainfall_end_time      
        })


    success = insert_rainfall(rainfall_data)

    #temperature
    temperature_obj = data.get('temperature') or {}
    temperature_record_time = temperature_obj.get('recordTime')
    temperature_items = temperature_obj.get('data') or []

    temperature_data = []
    for item in temperature_items:
        temperature_data.append({
            'batch_id': batch_id,
            'place': item.get('place'),
            'value': item.get('value'),
            'unit': item.get('unit'),
            'record_time': temperature_record_time      
        })


    success = insert_temperature(temperature_data)


    #humidity
    humidity_obj = data.get('humidity') or {}
    humidity_record_time = humidity_obj.get('recordTime')
    humidity_items = humidity_obj.get('data') or []

    humidity_data = []
    for item in humidity_items:
        humidity_data.append({
            'batch_id': batch_id,
            'unit': item.get('unit'),
            'value': item.get('value'),
            'place': item.get('place'),
            'record_time': humidity_record_time      
        })


    success = insert_humidity(humidity_data)


    #uvindex
    uvindex_obj = data.get('uvindex') or {}
    uvindex_record_desc = uvindex_obj.get('recordDesc')
    uvindex_items = uvindex_obj.get('data') or []

    uvindex_data = []
    for item in uvindex_items:
        uvindex_data.append({
            'batch_id': batch_id,
            'place': item.get('place'),
            'value': item.get('value'),
            'desc': item.get('desc'),
            'record_desc': uvindex_record_desc      
        })


    success = insert_uvindex(uvindex_data)


corn_job()