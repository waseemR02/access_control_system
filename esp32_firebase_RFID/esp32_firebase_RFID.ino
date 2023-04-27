#include <Arduino.h>
#if defined(ESP32)
  #include <WiFi.h>
#elif defined(ESP8266)
  #include <ESP8266WiFi.h>
#endif
#include <Firebase_ESP_Client.h>

// For RFID Checker
#include "SPI.h"
#include "MFRC522.h"

//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

// Insert your network credentials
#define WIFI_SSID "beep.boop"
#define WIFI_PASSWORD "rootroot"

// Insert Firebase project API Key
#define API_KEY "AIzaSyC0YiMnai56d0zS_56hERdTRE1g8hDBTTk"

// Insert RTDB URLefine the RTDB URL */
#define DATABASE_URL "https://cc-project--2023-default-rtdb.asia-southeast1.firebasedatabase.app/" 

// For ESP32 WROOM DA
#define RST_PIN 27
#define SS_PIN 5

//Define Firebase Data object
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

// Creating MFRC522 instance
MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;

unsigned long sendDataPrevMillis = 0;
int count = 0;
bool signupOK = false;

String dump_byte_array(byte *buffer, byte bufferSize) {
    String str = "";
    for (byte i = 0; i < bufferSize; i++) {
        str += buffer[i];
        str += " ";
    }
    return str;
}

void setup(){
  Serial.begin(9600);
  SPI.begin();
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  mfrc522.PCD_Init();
  
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  mfrc522.PCD_DumpVersionToSerial();
  /* Assign the api key (required) */
  config.api_key = API_KEY;

  /* Assign the RTDB URL (required) */
  config.database_url = DATABASE_URL;

  /* Sign up */
  if (Firebase.signUp(&config, &auth, "", "")){
    Serial.println("ok");
    signupOK = true;
  }
  else{
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }

  /* Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h
  
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
}

void loop(){
  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
  if ( ! mfrc522.PICC_IsNewCardPresent())
    return;

    // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial())
    return;
        
  if (Firebase.ready() && signupOK){

    // Write an Float number on the database path test/float
    if (Firebase.RTDB.setFloat(&fbdo, "active", 0.01 + random(0,100))){
      Serial.println("PASSED");
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println("TYPE: " + fbdo.dataType());
    }
    else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fbdo.errorReason());
    }
    
    // Write an Int number on the database path test/int
    String str = dump_byte_array(mfrc522.uid.uidByte, mfrc522.uid.size);
    if (Firebase.RTDB.setString(&fbdo, "User/", str)){
      Serial.println("PASSED");
      Serial.println("CARD_ID: " + str);
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println("TYPE: " + fbdo.dataType());
    }
    else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fbdo.errorReason());
    }
  }
  mfrc522.PICC_HaltA();
}
