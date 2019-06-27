
const int button1Pin = 52;
const int button2Pin = 50;
const int button3Pin = 48;
const int led1Pin = 42;
const int led2Pin = 44;
const int led3Pin = 46;
int buttonOn = -1;

void setup() {
  Serial.begin(115200);
  pinMode(button1Pin, INPUT_PULLUP);
  pinMode(button2Pin, INPUT_PULLUP);
  pinMode(button3Pin, INPUT_PULLUP);
  pinMode(led1Pin, OUTPUT);
  pinMode(led2Pin, OUTPUT);
  pinMode(led3Pin, OUTPUT);
}

void loop() {
  if (digitalRead(button1Pin) == LOW) {
    buttonPressed(1);
    delay(200);
  } else if (digitalRead(button2Pin) == LOW) {
    buttonPressed(2);
    delay(200);
  } else if (digitalRead(button3Pin) == LOW) {
    buttonPressed(3);
    delay(200);
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
  if (buttonId == 1) {
    digitalWrite(led1Pin, HIGH);  
  } else if (buttonId == 2) {
    digitalWrite(led2Pin, HIGH);
  } else if (buttonId == 3) {
    digitalWrite(led3Pin, HIGH);
  }
}

void turnOffLed(int buttonId) {
  if (buttonId == 1) {
    digitalWrite(led1Pin, LOW);  
  } else if (buttonId == 2) {
    digitalWrite(led2Pin, LOW);
  } else if (buttonId == 3) {
    digitalWrite(led3Pin, LOW);
  }
}

void stopCurrentTask() {
  if (buttonOn != -1) {
    turnOffLed(buttonOn);
    Serial.print(buttonOn);
    Serial.print("f\n");
    buttonOn = -1;
  }
 }
