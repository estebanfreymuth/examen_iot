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

Como primer paso, hacemos una carpeta que dejamos en el escritorio, para luego abrirla y abrir el codigo del servidor flask que dejamos dentro de la carpeta,
al abrir el programa se puede ver como funciona con exito, mostrandonos que hay conexion y el valor que entrega el esp32 emisor.

A continuacion vamos a ver en el navegador la interfaz web (frontend) que nuestro servidor Flask esta sirviendo desde el backend.
El backend (corriendo en tu terminal) procesa la logica, se conecta a Supabase y le entrega al navegador ese diseño visual con los datos en tiempo real.

<img width="736" height="560" alt="WhatsApp Image 2026-07-09 at 12 17 53" src="https://github.com/user-attachments/assets/d60faa1f-2a5d-44ac-8e04-dd72b57779d6" />

<img width="769" height="599" alt="WhatsApp Image 2026-07-09 at 12 18 36" src="https://github.com/user-attachments/assets/52426070-582e-4e33-9f34-4a0e594d64d7" />








