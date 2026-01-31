#include <Arduino.h>
#include <IRremoteESP8266.h>
#include <IRrecv.h>
#include <IRutils.h>

const uint16_t kRecvPin = 15;  // VS1838B接続ピン
IRrecv irrecv(kRecvPin);
decode_results results;

void setup() {
  Serial.begin(115200);
  irrecv.enableIRIn();  // 受信開始
  Serial.println("赤外線受信待機中...");
}

void loop() {
  if (irrecv.decode(&results)) {
    // 受信したデータを表示
    serialPrintUint64(results.value, HEX);
    Serial.println("");
    Serial.print("Protocol: ");
    Serial.println(results.decode_type);
    
    // 送信用のコード生成
    Serial.println(resultToSourceCode(&results));
    Serial.println("----");
    
    irrecv.resume();  // 次の受信待機
  }
  delay(100);
}