# 🐧 Penguin Approved Architecture

> Because 31°C Vorlauf is a lifestyle.

## Vision

Penguin Approved is an open-source Home Assistant project that optimizes
underfloor heating and heat pumps using real measurements instead of assumptions.

The goal is not to replace the heating controller.

The goal is to understand the building, provide recommendations and eventually
optimize the system automatically.

---

## Core Principles

- No cloud required
- Data before assumptions
- Explain every decision
- Comfort first
- Open source

---

## System Overview

Weather
        │
        ▼
Home Assistant
        │
        ├──────── Zigbee2MQTT
        │               │
        │               ▼
        │         Room Temperatures
        │
        ├──────── eBUS
        │               │
        │               ▼
        │        Heat Pump Data
        │
        └──────── Future Sensors
                        │
                        ▼

              Penguin Core

        ├── Dashboard
        ├── Statistics
        ├── Recommendations
        └── Automatic Optimization

---

## Long-term Goals

- Automatic hydraulic balancing
- Heating curve optimization
- Cooling optimization
- COP analysis
- Thermal building model
- Energy consumption prediction
