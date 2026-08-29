# weather_dao.py
from psycopg2.extras import Json
from db import get_db_connection

def get_lastest_weather_snapshot() -> dict:
  """Get lastest weather record"""
  sql = """
        SELECT UPDATE_TIME, JSON FROM weather_snapshots ORDER BY 1 DESC LIMIT 1
    """

  try:
    # Borrow a connection from the connection pool.
    with get_db_connection() as conn:
      with conn.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()  # 1. 取得單筆查詢結果 (tuple)

        if row:
          update_time, json_data = row
          # 2. 將結果封裝成 dict 回傳
          return {
              "update_time": update_time,
              "data": json_data,  # 若資料庫欄位本身是 JSONB，psycopg2 會自動轉為 dict
          }
        else:
          return {}  # 資料庫為空時回傳空字典

  except Exception as error:
    # 3. 建議修正錯誤訊息（這裡是讀取而非寫入）
    print(f"[Error] Database query failed: {error}")
    return None

def insert_weather_snapshot(record: dict) -> bool:
    """Insert weather_snapshot record into PostgreSQL"""
    sql = """
    INSERT INTO weather_snapshots (
        weather_snapshots, update_time, icon, icon_update_time, 
        warning_message, mintemp_from00_to09, rainfall_from00_to12, 
        rainfall_last_month, rainfall_january_to_last_month, tcmessage, json
    ) VALUES (
        %(weather_snapshots)s, %(update_time)s, %(icon)s, %(icon_update_time)s, 
        %(warning_message)s, %(mintemp_from00_to09)s, %(rainfall_from00_to12)s, 
        %(rainfall_last_month)s, %(rainfall_january_to_last_month)s, %(tcmessage)s, %(json)s
    );
    """

    prepared_data = record.copy()
    prepared_data['icon'] = Json(record['icon']) if record.get('icon') is not None else None
    prepared_data['warning_message'] = Json(record['warning_message']) if record.get('warning_message') is not None else None
    prepared_data['tcmessage'] = Json(record['tcmessage']) if record.get('tcmessage') is not None else None
    prepared_data['json'] = Json(record['json']) if record.get('json') is not None else None

    try:
        # Borrow a connection from the connection pool.
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, prepared_data)
                conn.commit()
                print(f"[Success] Inserted weather_snapshots: {record.get('weather_snapshots')}")
                return True
    except Exception as error:
        print(f"[Error] Database insertion failed: {error}")
        return False
    

def insert_humidity(batch_id: str, humidity_item: dict) -> bool:
    """Insert humidity record into PostgreSQL"""

    sql = """
    INSERT INTO humidity (
        batch_id, unit, value, place, record_time
    ) VALUES (
        %(batch_id)s, %(unit)s, %(value)s, %(place)s, %(record_time)s
    );
    """

    prepared_data = {
        'batch_id': batch_id,
        'unit': humidity_item.get('unit'),
        'value': humidity_item.get('value'),
        'place': humidity_item.get('place'),
        'record_time': humidity_item.get('recordTime')  # 注意：API 回傳 key 為 camelCase
    }
    
    try:
        # Borrow a connection from the connection pool.
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, prepared_data)
                conn.commit()
                print(f"[Success] Inserted humidity: {humidity_item}")
                return True
    except Exception as error:
        print(f"[Error] Database insertion failed: {error}")
        return False
    
def insert_lightning(lightning_list: list) -> bool:
    """Insert lightning record into PostgreSQL"""

    sql = """
    INSERT INTO lightning (
        batch_id, place, occur, start_time, end_time
    ) VALUES (
        %(batch_id)s, %(place)s, %(occur)s, %(start_time)s, %(end_time)s
    );
    """

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(sql, lightning_list)
                conn.commit()
                print(f"[Success] Batch inserted {len(lightning_list)} lightning records.")
                return True
    except Exception as error:
        print(f"[Error] Batch lightning insertion failed: {error}")
        return False

def insert_rainfall(rainfall_list:list) -> bool:
    
    """Insert rainfall record into PostgreSQL"""

    sql = """
    INSERT INTO rainfall (
        batch_id, unit, place, max, min, main, start_time, end_time
    ) VALUES (
        %(batch_id)s, %(unit)s, %(place)s, %(max)s, %(min)s, %(main)s, %(start_time)s, %(end_time)s
    );
    """

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(sql, rainfall_list)
                conn.commit()
                print(f"[Success] Batch inserted {len(rainfall_list)} rainfall records.")
                return True
    except Exception as error:
        print(f"[Error] Batch rainfall insertion failed: {error}")
        return False
    
    
def insert_temperature(temperature_list:list) -> bool:
    
    """Insert temperature record into PostgreSQL"""

    sql = """
    INSERT INTO temperature (
        batch_id, place, value, unit, record_time
    ) VALUES (
        %(batch_id)s, %(place)s, %(value)s, %(unit)s, %(record_time)s
    );
    """

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(sql, temperature_list)
                conn.commit()
                print(f"[Success] Batch inserted {len(temperature_list)} temperature records.")
                return True
    except Exception as error:
        print(f"[Error] Batch temperature insertion failed: {error}")
        return False
    
def insert_humidity(humidity_list:list) -> bool:
    
    """Insert humidity record into PostgreSQL"""

    sql = """
    INSERT INTO humidity (
        batch_id, unit, value, place, record_time
    ) VALUES (
        %(batch_id)s, %(unit)s, %(value)s, %(place)s, %(record_time)s
    );
    """

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(sql, humidity_list)
                conn.commit()
                print(f"[Success] Batch inserted {len(humidity_list)} humidity records.")
                return True
    except Exception as error:
        print(f"[Error] Batch humidity insertion failed: {error}")
        return False
    
def insert_uvindex(uvindex_list:list) -> bool:
    
    """Insert uvindex record into PostgreSQL"""

    sql = """
    INSERT INTO uvindex (
        batch_id, place, value, "desc", record_desc
    ) VALUES (
        %(batch_id)s, %(place)s, %(value)s, %(desc)s, %(record_desc)s
    );
    """

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(sql, uvindex_list)
                conn.commit()
                print(f"[Success] Batch inserted {len(uvindex_list)} uvindex records.")
                return True
    except Exception as error:
        print(f"[Error] Batch uvindex insertion failed: {error}")
        return False
    
