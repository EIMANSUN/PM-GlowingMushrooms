#include <FastLED.h>
#define LED_PIN 9
#define NUM_LEDS 3
unsigned long runTime;

CRGB leds[NUM_LEDS];

void setup() {
  Serial.begin(9600);
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, 500);
  FastLED.clear();
  FastLED.show();

}

void loop() {
    // RED GREEN BLUE

    static float rad;
    static float f1 = (1.0/2);
    static float f2 = (1.0/3);
    static float f3 = (1.0/4);
    int from = 0;
    int to = 255;
    runTime = millis();
    

    int y1 = 127.5 + 127.5 * sin(f1 * 2.0 * PI * (runTime / 1000.0));
    int y2 = 127.5 + 127.5 * sin(f2 * 2.0 * PI * (runTime / 1000.0));
    int y3 = 127.5 + 127.5 * sin(f3 * 2.0 * PI * (runTime / 1000.0));
    Serial.print(y1);
    Serial.print(",");
    Serial.print(y2);
    Serial.print(",");
    Serial.println(y3);
    leds[0] = CRGB(y1, 0, 0);
    leds[1] = CRGB(0, y2, 0);
    leds[2] = CRGB(0, 0, y3);
    FastLED.show();



}
