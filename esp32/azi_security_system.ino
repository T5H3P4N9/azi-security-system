#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>
#include <HTTPClient.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASSWORD";

WebServer server(80);

// ================= PINS =================
#define TRIG_PIN 5
#define ECHO_PIN 18
#define LED_PIN 4
#define BUZZER 19

#define SCANNER_SERVO_PIN 13   // sweeping radar servo
#define LASER_SERVO_PIN 15     // fixed laser pointer servo

// ================= SERVOS =================
Servo scannerServo;
Servo laserServo;

// ================= STATE =================
String command = "";
String lastState = "";

int scanAngle = 90;
int direction = 1;

int targetAngle = 90;   // 🔥 angle from sensor lock
int currentLaserAngle = 90;

unsigned long lastMove = 0;

// ================= DISTANCE =================
int getDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG_PIN, LOW);

  long t = pulseIn(ECHO_PIN, HIGH, 30000);
  return t * 0.034 / 2;
}

// ================= BUZZER =================
void beep(int freq, int duration) {
  ledcAttach(BUZZER, freq, 8);
  ledcWrite(BUZZER, 128);
  delay(duration);
  ledcWrite(BUZZER, 0);
}

void alarmFast() {
  for (int i = 0; i < 3; i++) {
    beep(2500, 80);
    delay(50);
  }
}

// ================= SEND SENSOR =================
void sendSensor(int dist, String state, int angle) {

  String url =
    "http://YOUR_PC_IP:8000/sensor?dist=" +
    String(dist) +
    "&state=" +
    state +
    "&angle=" +
    String(angle);

  WiFiClient client;
  HTTPClient http;

  http.begin(client, url);
  http.GET();
  http.end();

  Serial.println("📡 SENT: " + state);
}

// ================= SETUP =================
void setup() {

  Serial.begin(115200);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  scannerServo.attach(SCANNER_SERVO_PIN);
  laserServo.attach(LASER_SERVO_PIN);

  scannerServo.write(90);
  laserServo.write(90);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ WIFI CONNECTED");
  Serial.println(WiFi.localIP());

  server.on("/cmd", []() {
    command = server.arg("cmd");
    Serial.println("CMD: " + command);
    server.send(200, "text/plain", "OK");
  });

  server.begin();
}

// ================= LOOP =================
void loop() {

  server.handleClient();

  int dist = getDistance();

  String state = "CLEAR";

  // ================= THREAT LEVELS =================
  if (dist > 0 && dist < 50) state = "INTRUDER";
  if (dist > 0 && dist < 35) state = "WARNING";
  if (dist > 0 && dist < 20) state = "FINAL_WARNING";

  // ================= SCANNER SERVO (RADAR SWEEP) =================
  if (state == "CLEAR") {

    digitalWrite(LED_PIN, LOW);

    if (millis() - lastMove > 20) {
      lastMove = millis();

      scanAngle += direction;

      if (scanAngle >= 180) {
        scanAngle = 180;
        direction = -1;
      }

      if (scanAngle <= 0) {
        scanAngle = 0;
        direction = 1;
      }

      scannerServo.write(scanAngle);
    }
  }

  // ================= TARGET LOCK =================
  else {

    digitalWrite(LED_PIN, HIGH);

    // 🔥 IMPORTANT FIX:
    // map raw scan position into stable laser tracking
    targetAngle = scanAngle;

    // smooth movement (prevents shaking)
    currentLaserAngle = currentLaserAngle + (targetAngle - currentLaserAngle) * 0.3;

    laserServo.write(currentLaserAngle);

    if (state == "FINAL_WARNING") {
      alarmFast();
    }
  }

  // ================= SEND ONLY ON CHANGE =================
  if (state != lastState) {

    lastState = state;

    sendSensor(dist, state, scanAngle);
  }

  // ================= COMMANDS =================
  if (command == "ARM") {
    beep(2000, 150);
    command = "";
  }

  else if (command == "ALERT") {
    alarmFast();
    command = "";
  }

  else if (command == "WARNING") {
    beep(1800, 200);
    command = "";
  }

  else if (command == "FINAL_WARNING") {
    alarmFast();
    alarmFast();
    command = "";
  }

  else if (command == "STOP") {
    digitalWrite(LED_PIN, LOW);
    scannerServo.write(90);
    laserServo.write(90);
    command = "";
  }

  delay(100);
}