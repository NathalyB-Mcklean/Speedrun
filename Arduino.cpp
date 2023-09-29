#include <ESP8266WiFi.h>
#include <DHT.h>

const char* ssid = "NOMBRE_DE_TU_RED";
const char* password = "CONTRASEÑA_DE_TU_RED";

const char* server = "IP_DEL_SERVIDOR"; // Por ejemplo: "192.168.1.10"

WiFiClient client;

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }
  Serial.println("Conectado a WiFi");
}

void loop() {
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  
  if (client.connect(server, 80)) {
    String url = "/recibir_datos?temperatura=";
    url += String(temp);
    url += "&humedad=";
    url += String(hum);
    
    client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                 "Host: " + server + "\r\n" +
                 "Connection: close\r\n\r\n");
    delay(10);
  }
  client.stop();
  delay(5000);  // Envía datos cada 5 segundos.
}
