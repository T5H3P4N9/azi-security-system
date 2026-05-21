# AZI Security System

Advanced AI-powered surveillance and IoT monitoring system built with Python, Flask, OpenAI, and ESP32 hardware integration.

AZI Security System combines artificial intelligence, embedded systems, robotics, and real-time sensor monitoring into a smart security platform capable of voice interaction, radar visualization, and automated threat detection.

---

# Overview

AZI Security System is a real-time AI surveillance and monitoring project designed to simulate an intelligent security operating system.

The system integrates:

- AI voice interaction
- ESP32 sensor communication
- Ultrasonic distance tracking
- Real-time radar visualization
- Threat level detection
- Smart voice alerts
- Servo motor tracking systems
- Browser-based monitoring dashboard

The project demonstrates the integration of software engineering, IoT systems, robotics concepts, and AI-powered automation into a single platform.

---

# Features

## AI Voice Assistant
- OpenAI-powered conversational assistant
- Voice input using browser speech recognition
- AI voice responses using speech synthesis
- Security-focused system behavior

## Real-Time Radar System
- Live radar visualization using HTML5 Canvas
- Animated scanning radar sweep
- Real-time target plotting
- Coordinate-based object tracking

## ESP32 Hardware Integration
- ESP32 WiFi communication
- Ultrasonic sensor monitoring
- Servo motor radar scanning
- Laser tracking support
- LED and buzzer alert system

## Threat Detection System
- Multi-level threat detection
- CLEAR
- INTRUDER
- WARNING
- FINAL_WARNING

## Smart Event System
- Anti-spam alert cooldown system
- Real-time voice notifications
- Browser dashboard updates
- Intelligent event handling

## Robotics Features
- Servo interpolation smoothing
- Automated target tracking
- Dynamic radar sweep logic
- Embedded systems communication

---

# System Architecture

```text
ESP32 Sensors
     │
     ▼
Flask Backend Server
     │
     ▼
AI Processing + Threat Logic
     │
     ▼
Web Dashboard + Voice Interface
```

---

# Tech Stack

## Backend
- Python
- Flask

## AI
- OpenAI API
- GPT-4o-mini

## Frontend
- HTML
- CSS
- JavaScript

## Embedded Systems
- ESP32
- Ultrasonic sensor
- Servo motors
- LED indicators
- Buzzer alarm system

## Communication
- HTTP Requests
- WiFi Networking
- REST-style API communication

---

# Project Structure

```bash
azi-security-system/
│
├── server.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── esp32/
│   └── azi_security_system.ino
│
├── screenshots/
│   ├── dashboard.png
│   ├── radar-system.png
│   ├── threat-detection.png
│   └── esp32-hardware.jpg
│
└── docs/
    └── architecture.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/azi-security-system.git
cd azi-security-system
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

# Running the Server

```bash
python server.py
```

Server runs on:

```text
http://localhost:8000
```

---

# ESP32 Setup

1. Open `azi_security_system.ino`
2. Configure:
   - WiFi SSID
   - WiFi Password
   - Flask server IP address
3. Upload code to ESP32
4. Connect:
   - Ultrasonic sensor
   - Servo motors
   - LED
   - Buzzer

---

# Hardware Components

- ESP32 Development Board
- HC-SR04 Ultrasonic Sensor
- Servo Motors
- Active Buzzer
- LEDs
- Jumper Wires
- Breadboard
- Optional laser module

---

# Security Event Levels

| Level | Description |
|---|---|
| CLEAR | No object detected |
| INTRUDER | Object detected within range |
| WARNING | Target approaching |
| FINAL_WARNING | Immediate threat detected |

---

# Current Capabilities

- Real-time sensor monitoring
- AI-assisted interaction
- Browser-based radar dashboard
- Voice communication
- Threat alert system
- Servo-based scanning system
- ESP32 remote communication
- Live coordinate tracking

---

# Planned Features

- Facial recognition
- Live camera feeds
- SQLite event logging
- WebSocket real-time updates
- Mobile dashboard
- Voice authentication
- Smart home integration
- Autonomous security routines
- Cloud deployment

---

# Screenshots

## Dashboard
Add dashboard screenshot here.

## Radar System
Add radar visualization screenshot here.

## ESP32 Hardware
Add hardware setup image here.

## Threat Detection
Add detection alert screenshot here.

---

# Educational Purpose

This project was built for learning and experimentation in:
- Artificial Intelligence
- Embedded Systems
- Robotics
- IoT Engineering
- Full-Stack Development
- Real-Time Systems
- Sensor Integration
- Smart Automation

---

# Author

Tshepang Oliver

Junior Backend & Robotics Developer

Focused on:
- AI systems
- Robotics
- IoT development
- Embedded programming
- Full-stack backend engineering

---

# License

This project is open-source and available under the MIT License.