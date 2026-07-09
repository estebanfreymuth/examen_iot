#include <WiFi.h>
#include <HTTPClient.h> 
#include <UrlEncode.h>  

// configuracion wifi (Celular)
const char* ssid = "nombre_internet";        
const char* password = "contraseña_internet"; 

// servidor flask con ip
const char* serverUrl = "http://ip_local_del_servidor/obtener_estado";

// actuadores
const int pinBaliza = 12;  // Pin para el relé/transistor de la baliza 12V

// configuracion WhatsApp (CallMeBot)
String phoneNumber = "numero_celular"; 
String apiKey = "llave_whatsapp_bot";           

// control para que la baliza y el WhatsApp se activen solo 1 vez por evento critico
bool balizaActivada = false;

void setup() {
  Serial.begin(115200);

  // pines como salida
  pinMode(pinBaliza, OUTPUT);
  
  // comienzan apagados
  digitalWrite(pinBaliza, LOW);

  // conexion wifi
  WiFi.begin(ssid, password);
  Serial.print("Conectando Alarma a Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n[Wi-Fi] ¡Alarma conectada con éxito!");
  Serial.println("----------------------------------------");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    // inicializar peticion http
    http.begin(serverUrl);
    int httpResponseCode = http.GET();

    // procesar respuesta servidos
    if (httpResponseCode > 0) {
      String payload = http.getString();
      Serial.print("[SERVIDOR] Estado recibido: ");
      Serial.println(payload);

      // logica de activacion segun estado
      if (payload.indexOf("CRITICO") != -1) {

        if (!balizaActivada) {
          Serial.println("[ALERTA] ¡CRÍTICO! Activando baliza por 1 segundo...");
          digitalWrite(pinBaliza, HIGH); // prende baliza
          delay(1000);                   // 1 segundo
          digitalWrite(pinBaliza, LOW);  // apaga baliza
          
          // integracion whatsapp
          Serial.println("[WhatsApp] Enviando notificación de emergencia...");
          enviarAlertaWhatsApp(" ¡ALERTA CRÍTICA! Se ha detectado un nivel de GAS CRÍTICO en la estación de monitoreo.");

          balizaActivada = true;  // bloquea para que no repita el sonido ni el mensaje continuamente
        }
      } 
      else if (payload.indexOf("ADVERTENCIA") != -1) {
        digitalWrite(pinBaliza, LOW);
        balizaActivada = false; 
        Serial.println("[PRECAUCIÓN] Nivel de gas moderado.");
      } 
      else {
        digitalWrite(pinBaliza, LOW);
        balizaActivada = false; 
        Serial.println("[OK] Todo bajo control.");
      }
    } else {
      Serial.print("[ERROR] Error al consultar. Código HTTP: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("[ALERTA] Wi-Fi desconectado.");
  }

  Serial.println("----------------------------------------");
  delay(2000); // consulta cada 2 seg
}

// funcion para enviar mensaje
void enviarAlertaWhatsApp(String mensaje) {
  if (WiFi.status() == WL_CONNECTED) { 
    HTTPClient http;                  
    String url = "https://api.callmebot.com/whatsapp.php?phone=" + phoneNumber +
                 "&text=" + urlEncode(mensaje) +
                 "&apikey=" + apiKey;  
    http.begin(url);                  
    int httpResponseCode = http.GET(); 
    Serial.print("[WhatsApp] Código de respuesta API: "); 
    Serial.println(httpResponseCode);
    http.end();                        
  } else {
    Serial.println("[WhatsApp] WiFi no conectado, no se envió el mensaje."); 
  }
}
