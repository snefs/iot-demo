# IoT Machine Monitoring Architecture

PowerPoint-ready landscape version: [architecture.svg](D:/Projects/Src/iot-demo/architecture.svg)

```mermaid
flowchart LR
    subgraph N[Node-RED]
        G[MachineDataGenerator<br/>10 machines<br/>orders 1-5<br/>dynamic measurements]
        S[MachineDataStorage]
        O[OrderAPI<br/>callback + Dashboard 2.0]
    end

    M[ Mosquitto MQTT<br/>machine-sensors ]
    I[(InfluxDB<br/>iot-data bucket)]
    F[FastAPI OrderCalculator<br/>POST /calculate]
    D[Grafana<br/>technical telemetry + order table]
    U[Users / Browser]

    G -->|JSON sensor messages| M
    M -->|machine-sensors| S
    S -->|machine_measurements<br/>temperature, vibration, pressure<br/>machine_id + order_id tags| I
    I -->|sensor queries| D
    D --> U

    U -->|Trigger calculation| F
    F -->|Query recent sensors| I
    F -->|Orders 1-5<br/>quality + delivery dates| O
    O -->|order_results<br/>fixed order control records| I
    O -->|Order results| U

    classDef stream fill:#071b2b,stroke:#00d4ff,color:#fff;
    classDef storage fill:#26133d,stroke:#c084fc,color:#fff;
    classDef app fill:#123522,stroke:#4ade80,color:#fff;
    class G,M,S,F,O app;
    class I storage;
    class D,U stream;
```

## Data behavior

- Sensor measurements are continuously generated for 10 machines and assigned to orders 1–5.
- Sensor data is published to MQTT topic `machine-sensors`.
- InfluxDB stores technical fields: temperature, vibration, and pressure.
- Grafana visualizes telemetry grouped by `order_id`.
- `POST /calculate` triggers `OrderCalculator`.
- `OrderCalculator` reads sensor data, calculates quality and delivery dates, and calls Node-RED `/orderapi`.
- Node-RED stores fixed order-control records in the `order_results` measurement and displays them in Dashboard 2.0.
