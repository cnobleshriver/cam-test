#include <Servo.h>

#define PANSERVO 14
#define TILTSERVO 11
#define RELOADSERVO 16

#define loadAngle 0
#define restAngle 50

Servo panServo;
Servo tiltServo;
Servo reloadServo;

int panPos = 90;
int tiltPos = 90;
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
  if (Serial.available() >= 2) {
    byte x_byte = Serial.read();
    byte y_byte = Serial.read();

    if (x_byte == 255 && y_byte == 255) { // Unique signal for fire command
      fire();
    } else {
      panPos = x_byte;
      tiltPos = y_byte;

      panPos = constrain(panPos, 0, 180);
      tiltPos = constrain(tiltPos, 80, 110);

      panServo.write(panPos);
      tiltServo.write(tiltPos);
    }
  }

  if (isFiring) {
    fire(); // Check if firing is complete
  }
}
