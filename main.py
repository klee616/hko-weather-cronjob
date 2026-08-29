import sys
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

# Import database Data Access Object (DAO) functions
from weather_dao import (
    get_lastest_weather_snapshot,
    insert_humidity,
    insert_lightning,
    insert_rainfall,
    insert_temperature,
    insert_uvindex,
    insert_weather_snapshot,
)


def corn_job() -> None:
  """Fetch the latest weather data from the Hong Kong Observatory API

  and write it to PostgreSQL tables if new updates are available.
  """
  # Endpoint and request parameters for the Hong Kong Observatory API
  url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"
  params = {"dataType": "rhrread", "lang": "en"}

  # Send HTTP GET request to fetch weather data
  try:
    resp = requests.get(url=url, params=params, timeout=10)
    resp.raise_for_status()  # Raise exception for HTTP 4xx/5xx status codes
    data = resp.json()
  except Exception as e:
    print(f"[Error] API fetch failed: {e}")
    return

  # Extract the primary update timestamp from the API payload
  api_update_time = data.get("updateTime")
  if not api_update_time:
    print("[Warning] API response missing 'updateTime'")
    return

  # Safely retrieve the latest updateTime recorded in the database (handles None gracefully)
  lastest_weather = get_lastest_weather_snapshot() or {}
  last_data = lastest_weather.get("data") or {}
  last_update_time = last_data.get("updateTime")

  print(f"Latest DB updateTime: {last_update_time}")
  print(f"API updateTime: {api_update_time}")

  # Skip execution if the database payload is already up-to-date
  if last_update_time == api_update_time:
    print("Data is up to date. Skipping execution.")
    return

  print("New data found! Processing insertion...")

  # Generate a unique batch ID (UUID) to link child records with the master snapshot
  batch_id = str(uuid.uuid4())

  # 1. Prepare master record (weather_snapshots)
  icon_list = data.get("icon") or []
  icon_val = (
      icon_list[0] if icon_list else None
  )  # Safely handle potential empty list

  master_record = {
      "weather_snapshots": batch_id,
      "update_time": api_update_time,
      "icon": icon_val,
      "icon_update_time": data.get("iconUpdateTime"),
      "warning_message": data.get("warningMessage"),
      "mintemp_from00_to09": data.get("mintempFrom00To09"),
      "rainfall_from00_to12": data.get("rainfallFrom00To12"),
      "rainfall_last_month": data.get("rainfallLastMonth"),
      "rainfall_january_to_last_month": data.get(
          "rainfallJanuaryToLastMonth"
      ),
      "tcmessage": data.get("tcmessage"),
      "json": data,
  }
  insert_weather_snapshot(master_record)

  # 2. Extract and insert Lightning data
  lightning_obj = data.get("lightning") or {}
  lightning_start_time = lightning_obj.get("startTime")
  lightning_end_time = lightning_obj.get("endTime")
  lightning_items = lightning_obj.get("data") or []

  lightning_data = [
      {
          "batch_id": batch_id,
          "place": item.get("place"),
          "occur": str(item.get("occur")).lower() == "true",
          "start_time": lightning_start_time,
          "end_time": lightning_end_time,
      }
      for item in lightning_items
  ]
  if lightning_data:
    insert_lightning(lightning_data)

  # 3. Extract and insert Rainfall data
  rainfall_obj = data.get("rainfall") or {}
  rainfall_start_time = rainfall_obj.get("startTime")
  rainfall_end_time = rainfall_obj.get("endTime")
  rainfall_items = rainfall_obj.get("data") or []

  rainfall_data = [
      {
          "batch_id": batch_id,
          "unit": item.get("unit"),
          "place": item.get("place"),
          "max": item.get("max"),
          "min": item.get("min"),
          "main": item.get("main"),
          "start_time": rainfall_start_time,
          "end_time": rainfall_end_time,
      }
      for item in rainfall_items
  ]
  if rainfall_data:
    insert_rainfall(rainfall_data)

  # 4. Extract and insert Temperature data
  temperature_obj = data.get("temperature") or {}
  temperature_record_time = temperature_obj.get("recordTime")
  temperature_items = temperature_obj.get("data") or []

  temperature_data = [
      {
          "batch_id": batch_id,
          "place": item.get("place"),
          "value": item.get("value"),
          "unit": item.get("unit"),
          "record_time": temperature_record_time,
      }
      for item in temperature_items
  ]
  if temperature_data:
    insert_temperature(temperature_data)

  # 5. Extract and insert Humidity data
  humidity_obj = data.get("humidity") or {}
  humidity_record_time = humidity_obj.get("recordTime")
  humidity_items = humidity_obj.get("data") or []

  humidity_data = [
      {
          "batch_id": batch_id,
          "unit": item.get("unit"),
          "value": item.get("value"),
          "place": item.get("place"),
          "record_time": humidity_record_time,
      }
      for item in humidity_items
  ]
  if humidity_data:
    insert_humidity(humidity_data)

  # 6. Extract and insert UV Index data
  uvindex_obj = data.get("uvindex") or {}
  uvindex_record_desc = uvindex_obj.get("recordDesc")
  uvindex_items = uvindex_obj.get("data") or []

  uvindex_data = [
      {
          "batch_id": batch_id,
          "place": item.get("place"),
          "value": item.get("value"),
          "desc": item.get("desc"),
          "record_desc": uvindex_record_desc,
      }
      for item in uvindex_items
  ]
  if uvindex_data:
    insert_uvindex(uvindex_data)

  print("All data inserted successfully.")


# Entry point for standalone script execution
if __name__ == "__main__":
  corn_job()