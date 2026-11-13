#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <time.h>

const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

const char* MQTT_HOST = "YOUR_MQTT_HOST";
const uint16_t MQTT_PORT = 8883;
const char* MQTT_USERNAME = "YOUR_MQTT_USERNAME";
const char* MQTT_PASSWORD = "YOUR_MQTT_PASSWORD";
const char* MQTT_ROOT_CA = R"EOF(
-----BEGIN CERTIFICATE-----
PASTE_YOUR_MQTT_BROKER_ROOT_CA_CERTIFICATE_HERE
-----END CERTIFICATE-----
)EOF";

const char* SENSOR_ID = "sensor-01";
const int VOLTAGE_PIN = 34;
const float VOLTAGE_SCALE = 1.0;
const unsigned long PUBLISH_INTERVAL_MS = 5000;

WiFiClientSecure secureClient;
PubSubClient mqttClient(secureClient);
unsigned long lastPublishMs = 0;

void connectWifi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Wi-Fi connected: ");
  Serial.println(WiFi.localIP());
}

void connectMqtt() {
  while (!mqttClient.connected()) {
    const String clientId = String("voltage-") + SENSOR_ID;
    Serial.print("Connecting to MQTT...");

    bool connected;
    if (MQTT_USERNAME[0] == '\0') {
      connected = mqttClient.connect(clientId.c_str());
    } else {
      connected = mqttClient.connect(
          clientId.c_str(), MQTT_USERNAME, MQTT_PASSWORD);
    }

    if (connected) {
      Serial.println("connected");
    } else {
      Serial.print("failed, state=");
      Serial.println(mqttClient.state());
      delay(3000);
    }
  }
}

void publishVoltage() {
  struct tm timeInfo;
  if (!getLocalTime(&timeInfo, 1000)) {
    Serial.println("Time is not available yet; skipping reading");
    return;
  }

  char recordedAt[25];
  strftime(recordedAt, sizeof(recordedAt), "%Y-%m-%dT%H:%M:%SZ", &timeInfo);

  const float voltageV = analogReadMilliVolts(VOLTAGE_PIN) / 1000.0 * VOLTAGE_SCALE;
  char payload[160];
  snprintf(
      payload,
      sizeof(payload),
      "{\"sensor_id\":\"%s\",\"voltage_v\":%.3f,\"recorded_at\":\"%s\"}",
      SENSOR_ID,
      voltageV,
      recordedAt);

  const String topic = String("sensors/") + SENSOR_ID + "/voltage";
  if (mqttClient.publish(topic.c_str(), payload)) {
    Serial.print("Published ");
    Serial.println(payload);
  } else {
    Serial.println("MQTT publish failed");
  }
}

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);

  connectWifi();
  configTime(0, 0, "pool.ntp.org", "time.google.com");

  secureClient.setCACert(MQTT_ROOT_CA);
  mqttClient.setServer(MQTT_HOST, MQTT_PORT);
  mqttClient.setBufferSize(256);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWifi();
  }
  if (!mqttClient.connected()) {
    connectMqtt();
  }
  mqttClient.loop();

  const unsigned long now = millis();
  if (now - lastPublishMs >= PUBLISH_INTERVAL_MS) {
    lastPublishMs = now;
    publishVoltage();
  }
}
