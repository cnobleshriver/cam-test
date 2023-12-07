#include <Servo.h>

#define PANSERVO 14
#define TILTSERVO 11
#define RELOADSERVO 16

#define loadAngle 0
#define restAngle 50

Servo panServo;  // Create servo object for pan
Servo tiltServo; // Create servo object for tilt
Servo reloadServo;

int panPos = 90; // Initial pan position
int tiltPos = 90; // Initial tilt position
unsigned long lastFireTime = 0;
bool isFiring = false;

void setup() {
  panServo.attach(PANSERVO);
  tiltServo.attach(TILTSERVO);
  reloadServo.attach(RELOADSERVO);
  
  panServo.write(panPos);
  tiltServo.write(tiltPos);
  reloadServo.write(restAngle);
  

  Serial.begin(115200);
}

//void fire() {
//  reloadServo.write(loadAngle);
//  delay(500);
//  reloadServo.write(restAngle);
//  delay(500);
//}


void fire() {
  if (!isFiring) {
    reloadServo.write(loadAngle);
    lastFireTime = millis();
    isFiring = true;
  } else if (millis() - lastFireTime > 500) {
    reloadServo.write(restAngle);
    isFiring = false;
  }
}
void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('>');
    if (input.startsWith("fire")) {
      fire();
    } else {
      
      int commaIndex = input.indexOf(',');

      if (commaIndex != -1) {
        int errorX = input.substring(1, commaIndex).toInt();
        int errorY = input.substring(commaIndex + 1).toInt();

        // Add a fraction of the error to the servo position
        panPos += errorX * 0.02;
        tiltPos += errorY * 0.02;

        panPos = constrain(panPos, 0, 180);
        tiltPos = constrain(tiltPos, 80, 100);

        panServo.write(panPos);
        tiltServo.write(tiltPos);
      }
    }
  }
    if (isFiring) {
    fire(); // Check if firing is complete
  }
}
