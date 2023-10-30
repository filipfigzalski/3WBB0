#include <Arduino.h>
#include <ArduinoJson.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <TimerInterrupt_Generic.h>

// WiFi Settings
#define AP_SSID        "TILE"               // ssid of wifi
#define AP_PASSPHRASE  "12345678"           // password of wifi

// API Settings
#define PORT        8000                    // port of api
#define HTTPS       false                   // true if using https
#define TILE_ID     1                       // id of tile
#define INTERVAL_MS 10000                   // how often send data 
#define URI         "/tiles/%d/dataframes/" // URI to which POST data

// Connections
#define PIEZO_INPUT_PIN D1                  // pin to which piezo is attached
#define VOLTAGE_INPUT_PIN A0                // pin which senses curent voltage

// Other
#define DEBOUNCE_TIME 100                   // minimum time between steps
#define VOLTAGE_TIMER_INTERVAL_MS 100       // how often to measure voltage


// Variables
uint64_t lastTimeframeTime = 0;             // the last time timeframe was sent

volatile uint16_t steps = 0;                // number of steps since last dataframe
volatile uint64_t lastStepTime = 0;         // time since last step, used for debouncing

volatile uint64_t voltageSum = 0;           // sum of all measurements
volatile uint16_t voltageCount = 0;         // number of measurements

WiFiClient client;                          // handles WiFi connection
ESP8266Timer voltageTimer;                  // timer for voltage measurements

void IRAM_ATTR measureVoltage();            // routine for timer, measures voltage
void IRAM_ATTR stepDetected();              // routine for interrupt, counts steps
void sendDataFrame(const float_t &voltage, const uint16_t &steps);  // sends dataframe

void setup() {
    // setting up serial connection
    Serial.begin(9600);
    Serial.println();

    // setting up interrupt
    pinMode(PIEZO_INPUT_PIN, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(PIEZO_INPUT_PIN), stepDetected, FALLING);
    pinMode(A0, INPUT);

    // setting up timer
    if(voltageTimer.attachInterruptInterval(VOLTAGE_TIMER_INTERVAL_MS * 1000, measureVoltage)) {
        Serial.println("Timer started successfully!");
    } else {
        Serial.println("Cannot set timer correctly. Select another frequency or interval.");
    }

    // setting up access point
    Serial.println("Starting access point");
    Serial.printf("SSID: %s\n", AP_SSID);
    Serial.printf("Password: %s\n", AP_PASSPHRASE);
    WiFi.softAP(AP_SSID, AP_PASSPHRASE);
    Serial.println("Waiting for client to connect...");
    while(WiFi.softAPgetStationNum() == 0) delay(100); // wait for at least one connection
    Serial.println("Client connected!");
}

void loop() {
    uint64_t currentTime = millis();
    if (currentTime >= lastTimeframeTime + INTERVAL_MS) {
        lastTimeframeTime = currentTime;

        // calculating average voltage
        float_t voltage = 0;
        if(voltageCount){
            voltage = ((float)map(voltageSum / voltageCount, 0, 1023, 0, 3300)) / 1000 * 11;
        }

        uint16_t _steps = steps;

        // reseting variables
        steps = voltageSum = voltageCount = 0;

        // sending data
        if (WiFi.softAPgetStationNum() > 0) {
            sendDataFrame(voltage, _steps);
        }
    }
}

void measureVoltage() {
    voltageSum += analogRead(VOLTAGE_INPUT_PIN);
    voltageCount++;
}

void stepDetected() {
    uint64_t currentTime = millis();
    if(currentTime - lastStepTime > DEBOUNCE_TIME) {
        steps++;
    }
    lastStepTime = currentTime;

    voltageSum += analogRead(VOLTAGE_INPUT_PIN);
    voltageCount++;
}

void sendDataFrame(const float_t &voltage, const uint16_t &steps) {
    // initialize connection to the host
    HTTPClient http;
    char buffer[64];
    sprintf(buffer, URI, TILE_ID);
    http.begin(client, "192.168.4.2", PORT, buffer, HTTPS); // TODO

    // add required http headers
    http.addHeader("Content-Type", "application/json");
    http.addHeader("accept", "application/json");

    // create json body
    StaticJsonDocument<64> doc;
    doc["voltage"] = voltage;
    doc["steps"] = steps;
    String data;
    serializeJson(doc, data);

    Serial.println("Sending data:");
    Serial.println(data);

    // send message to api and read response
    http.POST(data);
    Serial.println("Data received:");
    Serial.println(http.getString());
}
