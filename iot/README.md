# IoT sensor: ESP32, MQTT, Supabase and Grafana Cloud

This folder contains the full sample IoT path. Its two data-product subfolders are:

- [`database/`](database/): PostgreSQL schema, sample readings, and local-only database roles.
- [`grafana-cloud/`](grafana-cloud/): dashboard JSON to import into Grafana Cloud.

The other files provide the ESP32 sketch, local MQTT simulator, and MQTT-to-PostgreSQL bridge:

```text
ESP32 ──MQTT/TLS──► MQTT broker ──► mqtt_bridge.py ──SQL──► Supabase PostgreSQL
                                                               ▲
                                                               │ query
                                                         Grafana Cloud
```

MQTT does not write to PostgreSQL by itself. `mqtt_bridge.py` subscribes to messages and inserts them into the database. The local simulator and database let you try the flow without cloud credentials.

## Create cloud accounts

- [Sign up for Grafana Cloud](https://grafana.com/auth/sign-up/create-user) to host and view the IoT dashboard.
- [Sign up for Supabase](https://supabase.com/dashboard/sign-up) to create the hosted PostgreSQL database.

## 1. Try the local simulation

From the repository root:

```bash
docker compose --profile iot --profile iot-simulator up -d --build
```

The containers seed the local PostgreSQL database, start the MQTT broker and publish simulated readings every five seconds. Check bridge logs:

```bash
docker compose logs -f iot-bridge
```

Query the latest readings:

```bash
docker compose exec postgres psql -U postgres -d iot_demo -c \
  "SELECT sensor_id, recorded_at, voltage_v FROM voltage_readings ORDER BY recorded_at DESC LIMIT 10;"
```

Local database connection: host `localhost`, port `5432`, database `iot_demo`, user `postgres`, password `local_iot_demo_password`. The local MQTT broker listens on `localhost:1883` and allows anonymous connections on loopback only.

Stop the demo and retain the data volume:

```bash
docker compose --profile iot --profile iot-simulator down
```

Delete the volume to reset the sample data:

```bash
docker compose --profile iot --profile iot-simulator down --volumes
```

## 2. Connect an ESP32 to MQTT

The sketch is [`arduino/voltage_sensor.ino`](arduino/voltage_sensor.ino).

1. In Arduino IDE, install the **PubSubClient** library and select an ESP32 board.
2. Fill in `WIFI_SSID`, `WIFI_PASSWORD`, `MQTT_HOST`, `MQTT_PORT`, `MQTT_USERNAME`, and `MQTT_PASSWORD`.
3. Paste your MQTT broker's root CA certificate into `MQTT_ROOT_CA`. The sketch validates the broker's TLS certificate; do not disable verification.
4. Configure `VOLTAGE_PIN` and `VOLTAGE_SCALE` for your sensor or voltage-divider circuit. GPIO 34 is the default for a classic ESP32 DevKit. Keep the input within the board's electrical limits.
5. Upload the sketch and open Serial Monitor at 115200 baud.

The ESP32 publishes every five seconds to `sensors/sensor-01/voltage` with this JSON format:

```json
{
  "sensor_id": "sensor-01",
  "voltage_v": 3.295,
  "recorded_at": "2026-11-13T10:00:00Z"
}
```

The bridge subscribes to `sensors/+/voltage`. Use the MQTT provider's host, port, username, and password in the sketch; when using TLS, use port 8883 and the provider's root CA.

## 3. Send MQTT readings to Supabase

1. In Supabase SQL Editor, run [`database/schema.sql`](database/schema.sql).
2. Create an insert-only database user for the bridge and a read-only user for Grafana Cloud. Example grants are in the [full IoT guide](../docs/iot-sensor-demo.md). Do **not** run [`database/local-roles.sql`](database/local-roles.sql) in Supabase; it contains local training passwords.
3. Copy the repository-root `.env.example` to `.env`. Set:

   ```dotenv
   IOT_DATABASE_URL=postgresql://iot_writer:YOUR_PASSWORD@YOUR_SUPABASE_HOST:5432/postgres?sslmode=require
   IOT_MQTT_URL=mqtts://YOUR_MQTT_USER:YOUR_MQTT_PASSWORD@YOUR_MQTT_HOST:8883
   ```

   Replace the placeholders with your provider values and URL-encode special characters in credentials. `.env` is ignored by Git; never commit real credentials.
4. Start the bridge from the repository root without the simulator profile:

   ```bash
   docker compose --profile iot up -d --build iot-bridge
   docker compose logs -f iot-bridge
   ```

The bridge connects to the configured MQTT broker and Supabase PostgreSQL URL. Ensure the broker is reachable from the Docker host. The Compose stack may also start local PostgreSQL and Mosquitto as dependencies, but the bridge uses the remote URLs in `.env`.

## 4. Connect Grafana Cloud

1. In Grafana Cloud, add a PostgreSQL data source using the Supabase host, database, read-only user, and SSL settings required by Supabase. Use **Save & test** to check the connection.
2. Import [`grafana-cloud/iot-voltage-dashboard.json`](grafana-cloud/iot-voltage-dashboard.json).
3. Select the Supabase PostgreSQL data source when Grafana prompts for it.

The dashboard plots 5-minute average voltage by sensor. Grafana Cloud queries Supabase; it does not subscribe to MQTT. Grafana Cloud must be able to reach the database and cannot connect to your computer's `localhost`. Use the panel's **Inspect → Data** menu to export CSV.

For detailed Supabase SQL and cloud setup, see the [IoT demo guide](../docs/iot-sensor-demo.md).
