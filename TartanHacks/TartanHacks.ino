#include <stdlib.h>
#include <Adafruit_NeoPixel.h>

#define LED 97    
#define PIN 6

//constants for the serial input processing and LED strip
String input;
int brightness = 255;
int red = 0;
int green = 0;
int blue = 0;
uint32_t color = 0;
int arr[LED] = { 0 };
Adafruit_NeoPixel strip = Adafruit_NeoPixel(100, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);
  strip.begin();
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
    if (input.startsWith("B")) {
      brightness = input.substring(1).toInt();
    } else if (input.startsWith("C")) {
      red = input.substring(1, 4).toInt();
      green = input.substring(4, 7).toInt();
      blue = input.substring(7).toInt();
    }
  }   

  //Code to adjust the rgb values by brightness
  red = brightness*red/100;
  green = brightness*green/100;
  blue - brightness*blue/100;  

  //Code that pushes the color to the led strip
  color = strip.Color(red, green, blue);
  for(int i=0;i<LED;i++) {
    strip.setPixelColor(i, color);
  }

  strip.show();
  
}
