# TODO
Switch Mosquito to https://hub.docker.com/r/emqx/emqx

# IOT DEMO Environment

Here is a complete, production-ready Docker Compose stack featuring MQTT (Eclipse Mosquitto), Node-RED, InfluxDB, Grafana, and a Python environment.This stack includes persistent data storage, pre-created networks for secure container communication, and automatic container restarts.

- Grafana: Dashboard
- Influx: Timeseries database
- Mqtt: Broker
- Node-Red: Orchestrator

## Flow
----
Sensor (simulated) -> Mqtt 
Mqtt -> Node-Red
Node-Red -> Python -> Influx
Influx -> Grafana Dashboard

# Endpoints
Internal Network hostnamesBecause all services are linked on the iot-network bridge, they can talk to each other securely using their service names instead of IP addresses:

- InfluxDB (UI) http://influxdb:8086 / http://localhost:8086
- Node-RED (UI) http://nodered:1880 / http://localhost:1880
- Grafana (UI) http://localhost:3000
- MQTT Broker (Endpoint / no UI) http://mosquitto:1883 / 

# Accounts
Grafana, admin / admin
InfluxDB admin / ChangeThisSecurePassword123! (org: my-iot-org, bucket: iot-data)
Node-RED: none
Mosquitto: none (allow_anonymous true set in the config)


### Mosquito

Required Configuration Before LaunchingMosquitto 2.0+ requires an explicit configuration file to allow external local traffic. Before running docker compose up, follow these two steps:

1. Create a directory named mosquitto and a subdirectory named config.

2. Inside ./mosquitto/config/, 
    create a file named mosquitto.conf and paste this content:textlistener 1883
    allow_anonymous true

