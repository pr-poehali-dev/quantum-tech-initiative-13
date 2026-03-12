import json
import os
import psycopg2
from datetime import datetime

SCHEMA = "t_p29589758_quantum_tech_initiat"

def get_conn():
    return psycopg2.connect(os.environ["DATABASE_URL"])

def handler(event: dict, context) -> dict:
    """Получение и запись показаний CO2. GET — список замеров, POST — добавить замер."""
    cors = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 200, "headers": cors, "body": ""}

    method = event.get("httpMethod", "GET")

    if method == "GET":
        params = event.get("queryStringParameters") or {}
        limit = int(params.get("limit", 100))
        sensor_id = params.get("sensor_id")

        conn = get_conn()
        cur = conn.cursor()

        if sensor_id:
            cur.execute(
                f"SELECT id, value, unit, location, sensor_id, measured_at FROM {SCHEMA}.co2_measurements WHERE sensor_id = %s ORDER BY measured_at DESC LIMIT %s",
                (sensor_id, limit)
            )
        else:
            cur.execute(
                f"SELECT id, value, unit, location, sensor_id, measured_at FROM {SCHEMA}.co2_measurements ORDER BY measured_at DESC LIMIT %s",
                (limit,)
            )

        rows = cur.fetchall()
        cur.close()
        conn.close()

        data = [
            {
                "id": r[0],
                "value": float(r[1]),
                "unit": r[2],
                "location": r[3],
                "sensor_id": r[4],
                "measured_at": r[5].isoformat() if r[5] else None,
            }
            for r in rows
        ]
        return {"statusCode": 200, "headers": cors, "body": json.dumps({"measurements": data, "count": len(data)})}

    if method == "POST":
        body = json.loads(event.get("body") or "{}")
        value = body.get("value")
        unit = body.get("unit", "ppm")
        location = body.get("location")
        sensor_id = body.get("sensor_id")
        measured_at = body.get("measured_at")

        if value is None:
            return {"statusCode": 400, "headers": cors, "body": json.dumps({"error": "value is required"})}

        conn = get_conn()
        cur = conn.cursor()

        if measured_at:
            cur.execute(
                f"INSERT INTO {SCHEMA}.co2_measurements (value, unit, location, sensor_id, measured_at) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (value, unit, location, sensor_id, measured_at)
            )
        else:
            cur.execute(
                f"INSERT INTO {SCHEMA}.co2_measurements (value, unit, location, sensor_id) VALUES (%s, %s, %s, %s) RETURNING id",
                (value, unit, location, sensor_id)
            )

        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return {"statusCode": 201, "headers": cors, "body": json.dumps({"id": new_id, "status": "created"})}

    return {"statusCode": 405, "headers": cors, "body": json.dumps({"error": "Method not allowed"})}
