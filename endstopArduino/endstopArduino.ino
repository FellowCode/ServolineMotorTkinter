#define endstop_pin 14
#define resetbtn_pin 12

#define relay_pin 16

#define TIME_HOLD_ENDSTOP 10
#define TIME_HOLD_RESET 1000

#define CHECK_CONN_DELAY 1000

bool relayIsOn = true;
unsigned long int timer_btn_endstop = 0, timer_btn_reset = 0;
int timer = 0;

unsigned long int timer_conn_check = 0;

void setup() {
  Serial.begin(115200);
  pinMode(endstop_pin, INPUT);
  pinMode(resetbtn_pin, INPUT);
  pinMode(relay_pin, OUTPUT);

  digitalWrite(relay_pin, HIGH);
}

void loop() {
    CheckEndstop();
    CheckResetBtn();
    CheckConnection();
}

void CheckEndstop() {
  if (digitalRead(endstop_pin) == HIGH && relayIsOn){
      if (timer_btn_endstop == 0)
        timer_btn_endstop = millis();
      if (millis() - timer_btn_endstop > TIME_HOLD_ENDSTOP){
        relayIsOn = false;
        Serial.println("stop");
        while (Serial.available() < 1 && timer < 50){
          timer += 1;
          delay(1);
        }
        if (Serial.available() > 0) {
          String ans = Serial.readString();
          if (ans != "motor stop"){
            relayIsOn = false;
            digitalWrite(relay_pin, LOW);
          }
        }
        else  {
          relayIsOn = false;
          digitalWrite(relay_pin, LOW);
        }
      }
    }
    else
      timer_btn_endstop = 0;
}
void CheckResetBtn(){
  if (digitalRead(resetbtn_pin) == HIGH && !relayIsOn){
      if (timer_btn_reset == 0)
        timer_btn_reset = millis();
      if (millis() - timer_btn_reset > TIME_HOLD_RESET){
        relayIsOn = true;
        digitalWrite(relay_pin, HIGH);
      }
    }
    else
      timer_btn_reset = 0;
}

void CheckConnection(){
  if (millis() - timer_conn_check > CHECK_CONN_DELAY) {
    timer_conn_check = millis();
    Serial.println("endstop OK");
  }
}
