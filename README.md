Este proyecto implementa un ecosistema de internet (IoT) con una arquitectura cliente servidor en tiempo real.
Utiliza un ESP32 y un ESP32S3 para la adquisición y visualización de datos, junto a un backend local desarrollado en Flask y una base de datos relacional en la nube mediante Supabase.
Sistema monitoreo de nivel de gas

Componentes: Esp32 (emisor)
Esp32S3 (alarma y mensaje)
Sensor mq2
Baliza 12V
Resistencias
Transistores
Diodo

Funciones: 
Esp32: Realiza la lectura analógica de los niveles de PPM desde el sensor de gas,
empaqueta el valor y genera peticiones HTTP POST hacia la ruta  /actualizar_gas del servidor local de manera periódica.

Servidor backend (Flask): cerebro del sistema, recibe las lecturas del emisor y castea los datos a enteros (int) para evitar errores de sintaxis en la base de datos,
determina el umbral de alerta (Normal o Advertencia) e inserta los registros de manera inmediata en la nube.
Mediante POST /actualizar_gas recibe el nivel de gas y actualiza el estado y mediante GET /obtener_estado sirve el ultimo registro en formato JSON.

Base de datos (Supabase): visualiza los datos con una estructura en la tabla especifica
id (int8): llave primaria autoincrementable
created_at (timestamptz): timestamp automático de la medición.
nivel_gas (int8): nivel entero de PPM registrado.
estado (text): string con la etiqueta del estado actual.

Esp32S3: monitor visual que realiza consultas HTTP GET a la ruta /obtener_estado,
procesa la respuesta JSON y renderiza dinámicamente una barra de progreso en su pantalla TFT/LCD cambiando el esquema de colores dependiendo del riesgo detectado,
(Verde para niveles estables, Amarillo/Rojo para advertencias)


<img width="811" height="517" alt="WhatsApp Image 2026-07-09 at 12 17 41" src="https://github.com/user-attachments/assets/c16e99cd-209b-49f4-a5a0-3aaba4646cc7" />


