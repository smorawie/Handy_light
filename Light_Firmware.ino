const int LED_PIN = 9;
int brightness = 0;
const int STEP = 5;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  analogWrite(LED_PIN, brightness);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "ON")      brightness = 255;
    else if (cmd == "OFF") brightness = 0;
    else if (cmd == "BRIGHT_UP") brightness += STEP;
    else if (cmd == "BRIGHT_DOWN") brightness -= STEP;

    brightness = constrain(brightness, 0, 255);
    analogWrite(LED_PIN, brightness);
  }
}
