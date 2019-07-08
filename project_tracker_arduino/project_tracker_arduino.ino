const int numButtons = 6;
const int buttonPins[] = {10, 9, 8, 14, 12, 11};
const int ledPins[] = {4, 3, 2, 7, 6, 5};
int buttonOn = -1;

void setup() {
  Serial.begin(115200);
  for(int i = 0; i < numButtons; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
    pinMode(ledPins[i], OUTPUT);
  }
}

void loop() {
  for(int i = 0; i < numButtons; i++) {
    if(digitalRead(buttonPins[i]) == LOW) {
      buttonPressed(i+1);
      delay(300);
    }
  }
}

void buttonPressed(int buttonId) {
  if (buttonOn != buttonId) {
    stopCurrentTask();
    buttonOn = buttonId;
    turnOnLed(buttonId);
    Serial.print(buttonId);
    Serial.print("s\n");
  } else {
    stopCurrentTask();
  }
}

void turnOnLed(int buttonId) {
  digitalWrite(ledPins[buttonId-1], HIGH);
}

void turnOffLed(int buttonId) {
  digitalWrite(ledPins[buttonId-1], LOW);
}

void stopCurrentTask() {
  if (buttonOn != -1) {
    turnOffLed(buttonOn);
    Serial.print(buttonOn);
    Serial.print("f\n");
    buttonOn = -1;
  }
}
