# Arduino, MQTT, Supabase PostgreSQL and Grafana Cloud

MQTT does not write to PostgreSQL by itself. A subscriber/bridge receives Arduino messages from an MQTT broker and inserts them into Supabase. Grafana Cloud then queries Supabase PostgreSQL for the dashboard:

```text
Arduino ──MQTT──► MQTT broker ──► iot-bridge ──SQL──► Supabase PostgreSQL
                                                           ▲
                                                           │ query
                                                     Grafana Cloud
```

This repository includes a local simulation (Mosquitto + a simulated sensor + PostgreSQL) and a bridge that can instead be configured with your Supabase and MQTT connection strings. The IoT dashboard is for **Grafana Cloud**, not the local Grafana.

## Add your connection strings

Copy [`.env.example`](../.env.example) to `.env` and replace the placeholders:

```dotenv
IOT_DATABASE_URL=postgresql://iot_writer:YOUR_PASSWORD@YOUR_SUPABASE_HOST:5432/postgres?sslmode=require
IOT_MQTT_URL=mqtts://YOUR_MQTT_USER:YOUR_MQTT_PASSWORD@YOUR_MQTT_HOST:8883
```

Use the PostgreSQL host, database name, port, and credentials from your Supabase **Connect** settings. The example uses the common `postgres` database and `sslmode=require`; use the values Supabase provides for your project/network. Create a database user that can insert into `voltage_readings`, but cannot modify the schema. URL-encode special characters in passwords.

The MQTT URL uses `mqtts://` for a TLS-enabled broker. Use credentials and the hostname/port given by your MQTT provider. The local Mosquitto demo uses unauthenticated `mqtt://` only on loopback; do not use that mode on a public broker.

`.env` is ignored by Git. Never commit real connection strings, passwords, or API keys.

## Create the Supabase tables

Run [`iot/database/schema.sql`](../iot/database/schema.sql) in the Supabase SQL Editor. It creates a `sensors` table, a `voltage_readings` table, and a day of sample readings for three sensors. It contains no local demo passwords.

Create separate credentials for the MQTT bridge and Grafana Cloud. For example, after replacing the placeholders with strong passwords, run:

```sql
CREATE ROLE iot_writer LOGIN PASSWORD 'REPLACE_WITH_STRONG_WRITER_PASSWORD';
GRANT CONNECT ON DATABASE postgres TO iot_writer;
GRANT USAGE ON SCHEMA public TO iot_writer;
GRANT INSERT ON voltage_readings TO iot_writer;
GRANT USAGE, SELECT ON SEQUENCE voltage_readings_id_seq TO iot_writer;

CREATE ROLE grafana_reader LOGIN PASSWORD 'REPLACE_WITH_STRONG_READ_ONLY_PASSWORD';
GRANT CONNECT ON DATABASE postgres TO grafana_reader;
GRANT USAGE ON SCHEMA public TO grafana_reader;
GRANT SELECT ON sensors, voltage_readings TO grafana_reader;
```

Use `iot_writer` in `IOT_DATABASE_URL` and `grafana_reader` in Grafana Cloud. Keep the Grafana credential read-only.

## Run the MQTT bridge

The ESP32 sketch is [`iot/arduino/voltage_sensor.ino`](../iot/arduino/voltage_sensor.ino). Install the **PubSubClient** library in Arduino IDE, select an ESP32 board, and fill in Wi-Fi settings. Split `IOT_MQTT_URL` from `.env` into its host, port, username, and password fields in the sketch, then paste the broker's root CA certificate. The voltage input is read from GPIO 34; `VOLTAGE_SCALE` must match your sensor or voltage-divider circuit. Keep the ESP32 input within its electrical limits.

The sketch publishes JSON messages to topic `sensors/<sensor_id>/voltage`:

```json
{
  "sensor_id": "sensor-01",
  "voltage_v": 3.295,
  "recorded_at": "2026-11-13T10:00:00+00:00"
}
```

Start the bridge using the `.env` settings. Do not enable the simulator profile when sending actual readings:

```bash
docker compose --profile iot up -d --build iot-bridge
docker compose logs -f iot-bridge
```

The bridge subscribes to `sensors/+/voltage`, validates each reading, and inserts it into Supabase. The local MQTT broker and PostgreSQL services may also start as Compose dependencies, but the bridge uses the remote endpoints in `.env`.

To try the full pipeline without cloud accounts, leave `.env` absent and run the local simulator:

```bash
docker compose --profile iot --profile iot-simulator up -d --build
docker compose exec postgres psql -U postgres -d iot_demo -c \
  "SELECT sensor_id, recorded_at, voltage_v FROM voltage_readings ORDER BY recorded_at DESC LIMIT 10;"
```

The local database listens on `localhost:5432`; the local MQTT broker listens on `localhost:1883`. The sample credentials are `postgres` / `local_iot_demo_password`. The local bridge uses a separate insert-only account. These credentials and the anonymous local MQTT broker are for loopback training only.

## Set up the Grafana Cloud dashboard

1. In Grafana Cloud, add a **PostgreSQL** data source using the Supabase host and database, user `grafana_reader`, its password, and Supabase's required SSL settings. Grafana Cloud must be able to reach the Supabase database; it cannot connect to a developer computer's `localhost`.
2. Import [`iot/grafana-cloud/iot-voltage-dashboard.json`](../iot/grafana-cloud/iot-voltage-dashboard.json) into Grafana Cloud.
3. During import, select the PostgreSQL data source you just configured.

The dashboard plots 5-minute average voltage by sensor for the selected time range. Grafana Cloud queries the Supabase database; it does not receive MQTT messages directly. You can export panel data as CSV from Grafana.

## Stop and reset the local simulation

Stop the containers while keeping the local database volume:

```bash
docker compose --profile iot --profile iot-simulator down
```

Erase the local database and regenerate its initial sample data:

```bash
docker compose --profile iot --profile iot-simulator down --volumes
docker compose --profile iot --profile iot-simulator up -d --build
```
