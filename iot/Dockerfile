FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY mqtt_bridge.py mqtt_simulator.py ./

CMD ["python", "mqtt_bridge.py"]
