#include <Arduino.h>
#include <LiquidCrystal.h>
#include <DHT.h>

LiquidCrystal lcd(12, 11, 2, 3, 4,5);
DHT dht(8, DHT11);

void setup() {
    Serial.begin(9600);
    pinMode(13, OUTPUT);
    lcd.begin(16, 2);
    dht.begin();
    lcd.clear();
    // lcd.print("Hello World");

}
bool flag = false;
void loop() {
    if (Serial.available()) {
        char c = Serial.read();
        switch (c) {
            case 'n': digitalWrite(13, HIGH); break;
            case 'f': digitalWrite(13, LOW); break;
            case 'b': flag = !flag; break;
        }
    }
    static uint32_t tmr2;
    if (flag && millis() - tmr2 >= 1000) {
        tmr2 = millis();
        digitalWrite(13, !digitalRead(13));
    }
    static uint32_t tmr;
    static float h;
    static float t;
    if (millis() - tmr >= 50) {
        tmr = millis();
        h = dht.readHumidity();
        t = dht.readTemperature();
        // Serial protocol
        Serial.print(t);
        Serial.print('\t');
        Serial.println(h);
        // end of serial protocol
    }
    static uint32_t tmr1;
    if (millis() - tmr1 >= 1000) {
        tmr1 = millis();
        lcd.clear();
        lcd.home();
        String temp = "Temp: " + String(t) + "C";
        lcd.print(temp);
        lcd.setCursor(0, 1);
        String hum = "Hum: " + String(h) + "%";
        lcd.print(hum);
    }


}