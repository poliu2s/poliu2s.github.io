/* Use a variable called byteRead to temporarily store
   the data coming from the computer */
#include <Servo.h>

Servo myservo;
int pos = 0;
byte byteRead;
int led = 13;
int count = 0;


void setup()
{
  Serial.begin(9600);
  Serial.println("Hello world!");
  pinMode(led, OUTPUT); 
  myservo.attach(9);
}



void loop()
{
  if (Serial.available()) {
    byteRead = Serial.read();
    count += 1;
    if (byteRead == 49 && count > 10) {
       digitalWrite(led, HIGH);
       turnCW();
    } else if (byteRead == 50 && count > 10) {
      digitalWrite(led, LOW);
      turnCCW();
    }
    

    Serial.println(byteRead);
    // Serial.flush();
  }
}


void turnCW() {
  if (pos < 360) {
    delay(5);
    pos += 1;
    myservo.write(pos);
  }
  count = 0;
}

void turnCCW() {
  if (pos > 1) {
    delay(5);
    pos -= 1;
    myservo.write(pos);
  }
  count = 0;
}
