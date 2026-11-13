import json
import logging
import math
import os
import random
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
SENSORS = {
    "sensor-01": 3.3,
    "sensor-02": 3.28,
    "sensor-03": 5.0,
}


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    while True:
        try:
            logging.info("Connecting to MQTT broker at %s", MQTT_HOST)
            client.connect(MQTT_HOST, MQTT_PORT, 60)
            break
        except (OSError, mqtt.MqttError):
            logging.exception("MQTT connection failed; retrying in 5 seconds")
            time.sleep(5)

    client.loop_start()
    try:
        sample = 0
        while True:
            for sensor_id, base_voltage in SENSORS.items():
                voltage_v = (
                    base_voltage
                    - sample * 0.00002
                    + 0.015 * math.sin(sample / 3)
                    + random.uniform(-0.005, 0.005)
                )
                payload = {
                    "sensor_id": sensor_id,
                    "voltage_v": round(voltage_v, 3),
                    "recorded_at": datetime.now(timezone.utc).isoformat(),
                }
                result = client.publish(
                    f"sensors/{sensor_id}/voltage",
                    json.dumps(payload),
                    qos=1,
                )
                if result.rc != mqtt.MQTT_ERR_SUCCESS:
                    logging.error("Could not publish reading for %s", sensor_id)
                else:
                    logging.info("Published %.3f V from %s", voltage_v, sensor_id)
            sample += 1
            time.sleep(5)
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
