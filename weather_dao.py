# weather_dao.py
from psycopg2.extras import Json
from db import get_db_connection


def get_latest_weather_snapshot() -> dict:
  """Retrieve the most recent weather snapshot record."""
  sql = """
        SELECT UPDATE_TIME, JSON 
        FROM weather_snapshots 
        ORDER BY UPDATE_TIME DESC 
        LIMIT 1;
    """

  try:
    with get_db_connection() as conn:
      with conn.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()
        if row:
          update_time, json_data = row
          return {
              "update_time": update_time,
              "data": json_data,
          }
        return {}

  except Exception as error:
    print(f"[Error] Failed to fetch latest weather snapshot: {error}")
    return None


def insert_weather_snapshot(record: dict) -> bool:
  """Insert a single weather_snapshot record into PostgreSQL."""
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
  prepared_data["icon"] = (
      Json(record["icon"]) if record.get("icon") is not None else None
  )
  prepared_data["warning_message"] = (
      Json(record["warning_message"])
      if record.get("warning_message") is not None
      else None
  )
  prepared_data["tcmessage"] = (
      Json(record["tcmessage"]) if record.get("tcmessage") is not None else None
  )
  prepared_data["json"] = (
      Json(record["json"]) if record.get("json") is not None else None
  )

  try:
    with get_db_connection() as conn:
      with conn.cursor() as cursor:
        cursor.execute(sql, prepared_data)
        conn.commit()
        print(
            f"[Success] Inserted weather_snapshot ID:"
            f" {record.get('weather_snapshots')}"
        )
        return True
  except Exception as error:
    print(f"[Error] Weather snapshot insertion failed: {error}")
    return False


def insert_lightning(lightning_list: list) -> bool:
  """Batch insert lightning records into PostgreSQL."""
  if not lightning_list:
    return True

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
        print(
            f"[Success] Batch inserted {len(lightning_list)} lightning records."
        )
        return True
  except Exception as error:
    print(f"[Error] Batch lightning insertion failed: {error}")
    return False


def insert_rainfall(rainfall_list: list) -> bool:
  """Batch insert rainfall records into PostgreSQL."""
  if not rainfall_list:
    return True

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
        print(
            f"[Success] Batch inserted {len(rainfall_list)} rainfall records."
        )
        return True
  except Exception as error:
    print(f"[Error] Batch rainfall insertion failed: {error}")
    return False


def insert_temperature(temperature_list: list) -> bool:
  """Batch insert temperature records into PostgreSQL."""
  if not temperature_list:
    return True

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
        print(
            "[Success] Batch inserted"
            f" {len(temperature_list)} temperature records."
        )
        return True
  except Exception as error:
    print(f"[Error] Batch temperature insertion failed: {error}")
    return False


def insert_humidity(humidity_list: list) -> bool:
  """Batch insert humidity records into PostgreSQL."""
  if not humidity_list:
    return True

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
        print(
            f"[Success] Batch inserted {len(humidity_list)} humidity records."
        )
        return True
  except Exception as error:
    print(f"[Error] Batch humidity insertion failed: {error}")
    return False


def insert_uvindex(uvindex_list: list) -> bool:
  """Batch insert UV index records into PostgreSQL."""
  if not uvindex_list:
    return True

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
        print(
            f"[Success] Batch inserted {len(uvindex_list)} uvindex records."
        )
        return True
  except Exception as error:
    print(f"[Error] Batch uvindex insertion failed: {error}")
    return False