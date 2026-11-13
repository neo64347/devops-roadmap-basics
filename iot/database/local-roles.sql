CREATE ROLE grafana_reader LOGIN PASSWORD 'grafana_demo_password';
GRANT CONNECT ON DATABASE iot_demo TO grafana_reader;
GRANT USAGE ON SCHEMA public TO grafana_reader;
GRANT SELECT ON sensors, voltage_readings TO grafana_reader;

CREATE ROLE iot_writer LOGIN PASSWORD 'local_iot_writer_password';
GRANT CONNECT ON DATABASE iot_demo TO iot_writer;
GRANT USAGE ON SCHEMA public TO iot_writer;
GRANT INSERT ON voltage_readings TO iot_writer;
GRANT USAGE, SELECT ON SEQUENCE voltage_readings_id_seq TO iot_writer;
