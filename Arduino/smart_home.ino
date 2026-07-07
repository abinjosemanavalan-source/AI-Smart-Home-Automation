/*
==========================================================
 AI Powered Smart Home Automation
 Author : Abin Jose
 Platform : Arduino Uno
==========================================================

Components Used:
----------------
1. TMP36 Temperature Sensor -> A0
2. LDR + 10kΩ Resistor      -> A1
3. PIR Motion Sensor        -> D2
4. Room Light LED           -> D8
5. Fan LED                  -> D9
6. Piezo Buzzer             -> D10

Function:
---------
• Turns ON room light when it is dark.
• Turns ON fan when temperature is high.
• Sounds buzzer when motion is detected.
• Sends sensor data over Serial for Python.

Serial Output:
--------------
Temperature,Light,Motion

Example:
28.5,640,0
31.2,320,1
*/

const int TEMP_PIN = A0;
const int LDR_PIN = A1;
const int PIR_PIN = 2;

const int LIGHT_LED = 8;
const int FAN_LED = 9;
const int BUZZER = 10;

// Threshold values
const float TEMP_THRESHOLD = 30.0;
const int LIGHT_THRESHOLD = 500;

void setup() {

  Serial.begin(9600);

  pinMode(PIR_PIN, INPUT);

  pinMode(LIGHT_LED, OUTPUT);
  pinMode(FAN_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  digitalWrite(LIGHT_LED, LOW);
  digitalWrite(FAN_LED, LOW);
}

void loop() {

  // -----------------------------
  // Read Temperature Sensor
  // -----------------------------
  int tempRaw = analogRead(TEMP_PIN);

  float voltage = tempRaw * (5.0 / 1023.0);

  float temperature = (voltage - 0.5) * 100.0;

  // -----------------------------
  // Read LDR
  // -----------------------------
  int lightValue = analogRead(LDR_PIN);

  // -----------------------------
  // Read PIR Motion Sensor
  // -----------------------------
  int motion = digitalRead(PIR_PIN);

  // -----------------------------
  // Automatic Light Control
  // -----------------------------
  if (lightValue < LIGHT_THRESHOLD) {
    digitalWrite(LIGHT_LED, HIGH);
  } else {
    digitalWrite(LIGHT_LED, LOW);
  }

  // -----------------------------
  // Automatic Fan Control
  // -----------------------------
  if (temperature > TEMP_THRESHOLD) {
    digitalWrite(FAN_LED, HIGH);
  } else {
    digitalWrite(FAN_LED, LOW);
  }

  // -----------------------------
  // Motion Alarm
  // -----------------------------
  if (motion == HIGH) {

    tone(BUZZER, 1000);

  } else {

    noTone(BUZZER);

  }

  // -----------------------------
  // Send Data to Python
  // Format:
  // Temperature,Light,Motion
  // -----------------------------
  Serial.print(temperature);
  Serial.print(",");
  Serial.print(lightValue);
  Serial.print(",");
  Serial.println(motion);

  delay(500);
}