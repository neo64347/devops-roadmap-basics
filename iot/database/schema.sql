CREATE TABLE sensors (
    sensor_id TEXT PRIMARY KEY,
    location TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE voltage_readings (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sensor_id TEXT NOT NULL REFERENCES sensors(sensor_id),
    recorded_at TIMESTAMPTZ NOT NULL,
    voltage_v NUMERIC(5, 3) NOT NULL CHECK (voltage_v >= 0)
);

CREATE INDEX voltage_readings_sensor_time_idx
    ON voltage_readings (sensor_id, recorded_at DESC);

INSERT INTO sensors (sensor_id, location, description) VALUES
    ('sensor-01', 'Workshop', 'Main device battery'),
    ('sensor-02', 'Greenhouse', 'Remote device battery'),
    ('sensor-03', 'Garage', 'Gateway supply voltage');

INSERT INTO voltage_readings (sensor_id, recorded_at, voltage_v)
SELECT
    sensor.sensor_id,
    NOW() - reading.sample * INTERVAL '1 minute',
    ROUND((
        sensor.base_voltage::double precision
        - reading.sample * sensor.drain_per_sample::double precision
        + 0.025 * SIN(reading.sample / 7.0 + sensor.phase::double precision)
        + 0.010 * COS(reading.sample / 3.0 + sensor.phase::double precision)
    )::numeric, 3)
FROM (
    VALUES
        ('sensor-01', 3.300::numeric, 0.00015::numeric, 0.0::numeric),
        ('sensor-02', 3.280::numeric, 0.00009::numeric, 1.5::numeric),
        ('sensor-03', 5.000::numeric, 0.00004::numeric, 3.0::numeric)
) AS sensor(sensor_id, base_voltage, drain_per_sample, phase)
CROSS JOIN LATERAL generate_series(0, 1439) AS reading(sample);
