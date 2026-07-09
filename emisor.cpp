#include <WiFi.h>
#include <HTTPClient.h>

// configuracion wifi
const char* ssid = "nombre_internet";        
const char* password = "contraseña_internet"; 

// servidor flask con ip
const char* serverUrl = "http://ip_local_del_servidor/actualizar_gas";

// mq2
const int mq2Pin = 34;     

void setup() {
  Serial.begin(115200);

  // wifi
  WiFi.begin(ssid, password);
  Serial.print("Conectando a Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n[Wi-Fi] ¡Conectado con éxito!");
  Serial.print("[Wi-Fi] IP asignada al ESP32: ");
  Serial.println(WiFi.localIP());
  Serial.println("----------------------------------------");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    // leer el valor analogico de mq2
    int mq2Value = analogRead(mq2Pin);
    Serial.print("[SENSOR] Lectura MQ-2: ");
    Serial.println(mq2Value);

    // peticion http
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // cadena json estructurada
    String jsonPayload = "{\"nivel_gas\":" + String(mq2Value) + "}";

    // enviar datos
    int httpResponseCode = http.POST(jsonPayload);

    // respuesta de servidor
    if (httpResponseCode > 0) {
      Serial.print("[HTTP] Código de respuesta: ");
      Serial.println(httpResponseCode); 
      
      String responseBody = http.getString();
      Serial.print("[SERVIDOR] Respuesta: ");
      Serial.println(responseBody);
    } else {
      Serial.print("[ERROR] Fallo al enviar POST. Código HTTP: ");
      Serial.println(httpResponseCode);
    }

    http.end(); 
  } else {
    Serial.println("[ALERTA] Conexión Wi-Fi perdida. Reintentando...");
  }

  Serial.println("----------------------------------------"); 
  delay(2000); 
}
