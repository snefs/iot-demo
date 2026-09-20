import os
from datetime import datetime, timedelta, timezone
from typing import Any
import requests
from fastapi import FastAPI, HTTPException
from influxdb_client import InfluxDBClient

app = FastAPI(title="OrderCalculator", version="1.0.0")
INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "")
INFLUX_ORG = os.getenv("INFLUX_ORG", "my-iot-org")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "iot-data")
ORDER_API_URL = os.getenv("ORDER_API_URL", "http://nodered:1880/orderapi")

def retrieve_sensor_data() -> list[dict[str, Any]]:
    if not INFLUX_TOKEN:
        return []
    query = f'''from(bucket: "{INFLUX_BUCKET}") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "machine_measurements")'''
    with InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG) as client:
        return [{"machine_id": r.values.get("machine_id"), "order_id": r.values.get("order_id"), "field": r.get_field(), "value": r.get_value(), "extreme_value": r.values.get("extreme_value")} for t in client.query_api().query(query, org=INFLUX_ORG) for r in t.records]

def calculate_orders(sensor_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for order_id in range(1, 6):
        affected = any(str(i.get("order_id")) == str(order_id) and (i.get("extreme_value") == "True" or (i.get("field") == "temperature_c" and float(i.get("value", 0)) > 100) or (i.get("field") == "vibration_mm_s" and float(i.get("value", 0)) > 10)) for i in sensor_data)
        simulated_delay = order_id == 3
        quality = 65 if simulated_delay else 100
        delivery_days = order_id + (2 if simulated_delay else 0)
        result.append({"order_id": order_id, "start_date": datetime.now(timezone.utc).date().isoformat(), "planned_delivery": (datetime.now(timezone.utc) + timedelta(days=delivery_days)).date().isoformat(), "quality": quality, "comment": "quality issue detected; delivery shifted by 2 days" if simulated_delay else ("no remarks" if affected else "quality OK")})
    return result

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/calculate")
def calculate() -> dict[str, Any]:
    orders = calculate_orders(retrieve_sensor_data())
    try:
        response = requests.post(ORDER_API_URL, json={"orders": orders}, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"OrderAPI unavailable: {exc}") from exc
    return {"orders": orders, "sent_to": ORDER_API_URL}
