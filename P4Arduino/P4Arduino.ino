
int motorPin = 3; // Set the digital output pin for the motor
int motorPin2 = 5;
int startBtnPin = 6;
int feedbackBtnPin = 7;
int promptBtnPin = 8;
int answerBtnPin = 9;

char programState = 's';

int lastFeedbackBtnState = HIGH;
int lastStartBtnState = HIGH;
int lastAnswerBtnState = HIGH;
int lastPromptBtnState = HIGH;

int promptState = 0;
bool answerState = false;
int feedbackState = 0;

String response = "";

unsigned long buzzLastMillis = 0;
int buzzMotorState = LOW;

void setup() {
  Serial.begin(9600);
  pinMode(motorPin, OUTPUT); // Set the motorPin as an output
  pinMode(motorPin2, OUTPUT);
  pinMode(startBtnPin, INPUT_PULLUP);
  pinMode(feedbackBtnPin, INPUT_PULLUP);
  pinMode(promptBtnPin, INPUT_PULLUP);
  pinMode(answerBtnPin, INPUT_PULLUP);
  programState = 's';
  promptState = 0;
  answerState = false;
}

void loop() {
  int startBtnVal = digitalRead(startBtnPin);
  int promptBtnVal = digitalRead(promptBtnPin);
  int answerBtnVal = digitalRead(answerBtnPin);
  int feedbackBtnVal = digitalRead(feedbackBtnPin);
  bool startBtnWasUpdated = checkBtnState(startBtnVal, lastStartBtnState);
  bool promptBtnWasUpdated = checkBtnState(promptBtnVal, lastPromptBtnState);
  bool answerBtnWasUpdated = checkBtnState(answerBtnVal, lastAnswerBtnState);
  bool feedbackBtnWasUpdated = checkBtnState(feedbackBtnVal, lastFeedbackBtnState);
  if(Serial.available()>0){
    response = Serial.readStringUntil('\n');
  }else{
    response = "";
  }
  if(answerBtnVal == LOW && promptBtnVal == LOW){
    programState = 's';
  }
  if(programState == 's'){
      if(startBtnVal == LOW){
        String data = "Start,";
        switch(promptState){
          case 0:
            data += "Buzz,";
            break;
          case 1:
            data += "Talk,";
            break;
          case 2:
            data += "Light,";
            break;
        }
        if(answerState){
          data += "answer,";
        }else{
          data += "button,";
        }
        switch(feedbackState){
          case 0:
            data += "None";
            break;
          case 1:
            data += "Buzz";
            break;
          case 2:
            data += "Light";
            break; 
        }
        programState = 'w';
        Serial.println(data);
      }else if(promptBtnVal == LOW && promptBtnWasUpdated){
        promptState = updateIntState(promptState);
      }else if(answerBtnVal == LOW  && answerBtnWasUpdated){
        answerState = updateAnswerState(answerState);
      }else if(feedbackBtnVal == LOW && feedbackBtnWasUpdated){
        feedbackState = updateIntState(feedbackState);

      }
  }else if(programState == 'w'){
    if(response == "Start Prompting"){
      programState = 'p';
    }else if(response == "Start Again"){
      programState = 's';
    }
  }else if(programState == 'p'){
      if(answerState){
        switch(promptState){
          case 0:
            if(response == "Stop Prompting"){
              stopBuzzing();
              startTheChat();
            }else if(buzzLastMillis + 300 <= millis()){
              updateMotorState(motorPin, motorPin2);
              buzzLastMillis = millis();
            }
            break;
          case 1:
            if(response == "Stop Prompting"){
              startTheChat();
            }
            break;
          case 2:
            if(response == "Stop Prompting"){
              startTheChat();
            }
            break;
        }
      }else{
        switch(promptState){
          case 0:
            if(startBtnVal == LOW && startBtnWasUpdated){
             stopBuzzing();
             startTheChat();
            }else if(buzzLastMillis + 300 <= millis()){
              updateMotorState(motorPin, motorPin2);
              buzzLastMillis = millis();
            }
            break;
          case 1:
            if(startBtnVal == LOW && startBtnWasUpdated){
             startTheChat();
            }
            break;
          case 2:
            if(startBtnVal == LOW && startBtnWasUpdated){
              startTheChat();
            }            
            break;
        }
        
      }
  }else if(programState = 'f'){
    if(response == "Start Feedback"){
      switch(feedbackState){
        case 0:
          break;
        case 1:
          digitalWrite(motorPin, HIGH);
          digitalWrite(motorPin2, HIGH);
          break;
        case 2:
          break;
      }
    }else if(response == "Stop Feedback"){
      switch(feedbackState){
        case 0:
          break;
        case 1:
          stopBuzzing();
          break;
        case 2:
          break;
      }
    }
  }
}
int updateIntState(int currentState){
  if(currentState == 2){
    return 0;
  }else{
    return currentState + 1; 
  }
}
bool updateAnswerState(bool currentState){
  return !currentState;
} 
void updateMotorState(int motorPin1, int motorPin2){
  if(buzzMotorState == LOW){
    buzzMotorState = HIGH;    
  }else{
    buzzMotorState = LOW;
  }
  digitalWrite(motorPin1, buzzMotorState);
  digitalWrite(motorPin2, buzzMotorState);
}
bool checkBtnState(int currentState, int &lastBtnState){
  if(currentState == lastBtnState){
    return false;
  }else {
    lastBtnState = currentState;
    return true;
  }
}
void stopBuzzing(){
  buzzMotorState = HIGH;
  updateMotorState(motorPin,motorPin2);
}
void startTheChat(){
  programState = 'f'; 
  Serial.println("Talk");
}
