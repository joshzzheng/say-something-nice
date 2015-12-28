#include <Wire.h>
#include "rgb_lcd.h"

rgb_lcd lcd;

const int colorR = 255;
const int colorG = 0;
const int colorB = 0;

String data;

void setup() 
{
    // set up the LCD's number of columns and rows:
    lcd.begin(16, 2);
    lcd.setRGB(colorR, colorG, colorB);
    
    // opens serial port, sets data rate to 9600 bps
    Serial.begin(9600);

    // set pins for output
    pinMode(12, OUTPUT);
    pinMode(13, OUTPUT);
}

void loop()
{
    // when characters arrive over the serial port...
    if (Serial.available()) 
    {
        // wait a bit for the entire message to arrive
        delay(100);
        // clear the screen
        lcd.clear();
        // read all the available characters
        while (Serial.available() > 0) 
        {
            data = Serial.readString();
            // display each character to the LCD
            if (data == "p") {
              lcd.print("YES");
              lcd.print(" ");
              lcd.print(data);
              digitalWrite(12, HIGH);   // Turn on the LED
              delay(3000);              // Wait for one second
              digitalWrite(12, LOW);    // Turn off the LED
              delay(3000);
            } else {
              lcd.print("NO");
              lcd.print(" ");
              lcd.print(data);
              digitalWrite(13, HIGH);   // Turn on the LED
              delay(3000);              // Wait for one second
              digitalWrite(13, LOW);    // Turn off the LED
              delay(3000);
            }
        }
    }
}

