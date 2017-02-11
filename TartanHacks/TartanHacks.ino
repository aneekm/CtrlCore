#include <stdlib.h>
#include <Adafruit_NeoPixel.h>

#define LED 97    
#define PIN 6

//constants for the serial input processing and LED strip
String input;
int red = 0;
int green = 0;
int blue = 0;
uint32_t color = 0;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(100, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);
  strip.begin();
  strip.setBrightness(200);
  strip.show();
  input.reserve(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  //Code that reads in from Serial port and sets the necessary variables to their components
  while (Serial.available() == 0) {}
  while (Serial.available() > 0) {
    input = Serial.readStringUntil('\n');
    Serial.println(input);
    red = input.substring(0, 3).toInt();
    green = input.substring(3, 6).toInt();
    blue = input.substring(6).toInt();
  }   
  
  //Code that sets the color for each pixel in the strip
  color = strip.Color(red, green, blue);
  for(int i=0;i<LED;i++) {
    strip.setPixelColor(i, color);
  }

  //pushes the colors to the strip
  strip.show();
}
