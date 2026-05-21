# System Architecture

## Overview

AZI Security System consists of:

- ESP32 hardware controller
- Flask backend server
- AI assistant system
- Browser dashboard
- Radar visualization engine

---

## Data Flow

ESP32 Sensors
    ↓
Flask API (/sensor)
    ↓
Threat Detection Logic
    ↓
Browser Dashboard Updates
    ↓
Voice Alerts + Radar Visualization

---

## Components

### ESP32
Handles:
- Ultrasonic sensing
- Servo movement
- Threat scanning
- WiFi communication

### Flask Server
Handles:
- API routes
- Sensor data
- AI responses
- Dashboard updates

### Frontend Dashboard
Handles:
- Radar rendering
- Voice interaction
- Real-time monitoring
- Threat display