/*
 * Basic Candy Machine controller - runs the motor for 1 second any time data is recieved on the serial port
 * By Nathan Friedly <nfriedly@us.ibm.com>
 */
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Select which 'port' M1, M2, M3 or M4. In this case, M1
Adafruit_DCMotor *motor1 = AFMS.getMotor(1);
// You can also make another motor on port M2
Adafruit_DCMotor *motor2 = AFMS.getMotor(2);

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("Welcome To The Polite Candy Machine!");

  AFMS.begin();  // create with the default frequency 1.6KHz
  
  // Set the speed to start, from 0 (off) to 255 (max speed)
  motor1->setSpeed(255);
  motor1->run(FORWARD);
  motor1->run(RELEASE);

  // Set the speed to start, from 0 (off) to 255 (max speed)
  motor2->setSpeed(255);
  motor2->run(FORWARD);
  motor2->run(RELEASE);
}

void loop() {
  String data;
  if (Serial.available()) {
    // read all the available characters
    while (Serial.available() > 0) {
      data = Serial.readString();
      data = data[0];
      // display each character to the LCD
      if (data == "p") {
        Serial.println(data);
        motor1->run(FORWARD);
        delay(500);
        motor1->run(RELEASE);
      } else {
        Serial.println(data);
        motor2->run(FORWARD);
        delay(500);
        motor2->run(RELEASE);
      }
    }
  }
}
