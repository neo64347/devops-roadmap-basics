import json
import logging
import math
import os
import time
from datetime import datetime
from urllib.parse import unquote, urlparse

import paho.mqtt.client as mqtt
import psycopg

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TLS = os.getenv("MQTT_TLS", "false").lower() == "true"
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "sensors/+/voltage")
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
MQTT_URL = os.getenv("MQTT_URL")
if MQTT_URL:
    mqtt_url = urlparse(MQTT_URL)
    if mqtt_url.scheme not in ("mqtt", "mqtts") or not mqtt_url.hostname:
        raise ValueError("MQTT_URL must use mqtt:// or mqtts:// and include a host")
    MQTT_HOST = mqtt_url.hostname
    MQTT_PORT = mqtt_url.port or (8883 if mqtt_url.scheme == "mqtts" else 1883)
    MQTT_TLS = mqtt_url.scheme == "mqtts"
    if mqtt_url.username:
        MQTT_USERNAME = unquote(mqtt_url.username)
        MQTT_PASSWORD = unquote(mqtt_url.password or "")

DATABASE_URL = os.getenv("DATABASE_URL")
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "iot_demo"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "local_iot_demo_password"),
    "sslmode": os.getenv("DB_SSLMODE", "disable"),
}


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        logging.error("MQTT connection failed: %s", reason_code)
        return
    logging.info("Connected to MQTT broker; subscribing to %s", MQTT_TOPIC)
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        logging.error("Ignoring invalid message on %s: %s", message.topic, error)
        return

    if not isinstance(payload, dict):
        logging.error("Ignoring non-object message on %s", message.topic)
        return

    sensor_id = payload.get("sensor_id")
    raw_voltage = payload.get("voltage_v")
    raw_recorded_at = payload.get("recorded_at")
    if not isinstance(sensor_id, str) or not sensor_id:
        logging.error("Ignoring message with invalid sensor_id on %s", message.topic)
        return
    if not isinstance(raw_recorded_at, str):
        logging.error("Ignoring message with invalid recorded_at on %s", message.topic)
        return

    try:
        voltage_v = float(raw_voltage)
        recorded_at = datetime.fromisoformat(raw_recorded_at.replace("Z", "+00:00"))
    except (TypeError, ValueError) as error:
        logging.error("Ignoring invalid reading on %s: %s", message.topic, error)
        return

    if not math.isfinite(voltage_v) or voltage_v < 0:
        logging.error("Ignoring message with invalid voltage_v on %s", message.topic)
        return
    if recorded_at.tzinfo is None:
        logging.error("Ignoring timezone-naive recorded_at on %s", message.topic)
        return

    try:
        connection = (
            psycopg.connect(DATABASE_URL)
            if DATABASE_URL
            else psycopg.connect(**DB_CONFIG)
        )
        with connection:
            connection.execute(
                """
                INSERT INTO voltage_readings (sensor_id, recorded_at, voltage_v)
                VALUES (%s, %s, %s)
                """,
                (sensor_id, recorded_at, voltage_v),
            )
    except psycopg.Error:
        logging.exception("Could not save reading from %s", message.topic)
        return

    logging.info("Saved %.3f V from %s", voltage_v, sensor_id)


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    if MQTT_USERNAME:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    if MQTT_TLS:
        client.tls_set()

    while True:
        try:
            logging.info("Connecting to MQTT broker at %s:%s", MQTT_HOST, MQTT_PORT)
            client.connect(MQTT_HOST, MQTT_PORT, 60)
            client.loop_forever()
        except (OSError, mqtt.MqttError):
            logging.exception("MQTT connection failed; retrying in 5 seconds")
            time.sleep(5)


if __name__ == "__main__":
    main()
