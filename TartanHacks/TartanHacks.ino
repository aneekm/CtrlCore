#include <Adafruit_NeoPixel.h>

#define num 100    //has to be even (idk why)
#define PIN 6

//constants for the serial input processing and LED strip
String input;
int brightness = 0;
int red = 0;
int green = 0;
int blue = 0;
uint32_t color = 0;
int arr[num] = { 0 };
Adafruit_NeoPixel(num, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  strip.begin();
  strip.show();
  input.reserve(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  //Code that reads in from Serial port and sets the necessary variables to their components
  while (Serial.available > 0) {
    input = Serial.readStringUntil('\n');
    if(input.startsWith("L")) {
      brightness = input.substring(1);
    } else if (input.startsWith("R")) {
      red = input.substring(1);
    } else if (input.startsWith("G")) {
      green = input.substring(1);
    } else if (input.substring("B")) {
      blue = input.substring(1);  
    }
  }

  
}
