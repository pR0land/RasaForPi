int motorPin = 3; // Set the digital output pin for the motor
int motorPin2 = 5;

void setup() {
  pinMode(motorPin, OUTPUT); // Set the motorPin as an output
  pinMode(motorPin2, OUTPUT);
}

void loop() {
  // Turn on the motor and wait for 1 second
  digitalWrite(motorPin, HIGH);
  digitalWrite(motorPin2, HIGH);
  delay(500);

  // Turn off the motor and wait for 1 second
  digitalWrite(motorPin, LOW);
  digitalWrite(motorPin2, LOW);
  delay(500);

  // Repeat the on/off cycle 2 more times
  for(int i = 0; i < 2; i++){
    digitalWrite(motorPin, HIGH);
    digitalWrite(motorPin2, HIGH);
    delay(200);
    digitalWrite(motorPin, LOW);
    digitalWrite(motorPin2, LOW);
    delay(200);

  }
}
