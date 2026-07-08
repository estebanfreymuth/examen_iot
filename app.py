from flask import Flask, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# 1. Configuración de tus credenciales de Supabase
SUPABASE_URL = "https://byobujonqxckavzvmorc.supabase.co"
SUPABASE_KEY = "sb_publishable_yF0idrHP0Lt_oxwaiBiiNA_gqQI0Sr8"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Variables globales para guardar el estado en tiempo real
nivel_gas_actual = 0.0
estado_actual = "NORMAL"

@app.route('/')
def home():
    # Configuración dinámica avanzada de colores y efectos según el estado
    if estado_actual == "ADVERTENCIA":
        color_alerta = "#ffbb00"  # Ámbar neón
        color_rgb = "255, 187, 0"
        animacion = ""
    elif estado_actual == "CRITICO":
        color_alerta = "#ff3333"  # Rojo vibrante
        color_rgb = "255, 51, 51"
        animacion = "animation: pulso 1.5s infinite alternate;"  # Parpadeo de alerta
    else:
        color_alerta = "#00ff88"  # Verde neón
        color_rgb = "0, 255, 136"
        animacion = ""

    # Calcular el porcentaje de la barra de progreso (Máximo estimado: 1000 PPM)
    porcentaje_barra = min(100, max(0, (nivel_gas_actual / 1000.0) * 100))

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="2">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Monitoreo de Gas IoT</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                background: radial-gradient(circle at center, #111625 0%, #07080c 100%);
                color: #e2e8f0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }}
            @keyframes pulso {{
                0% {{ box-shadow: 0 0 20px rgba({color_rgb}, 0.4); }}
                100% {{ box-shadow: 0 0 40px rgba({color_rgb}, 0.8); border-top-color: #ff6666; }}
            }}
            #contenedor {{
                background: rgba(31, 40, 51, 0.65);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                padding: 45px 35px;
                border-radius: 24px;
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), 0 0 25px rgba({color_rgb}, 0.2);
                text-align: center;
                max-width: 420px;
                width: 90%;
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-top: 6px solid {color_alerta};
                transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
                {animacion}
            }}
            #titulo {{
                font-size: 13px;
                text-transform: uppercase;
                letter-spacing: 3px;
                color: #66fcf1;
                margin-bottom: 30px;
                opacity: 0.9;
            }}
            #dato {{
                font-size: 64px;
                font-weight: 900;
                color: #ffffff;
                margin-bottom: 15px;
                letter-spacing: -1px;
            }}
            #unidad {{
                font-size: 22px; 
                font-weight: 500; 
                color: #66fcf1;
                margin-left: 5px;
            }}
            /* Estilos de la barra de progreso */
            #barra-contenedor {{
                background: rgba(255, 255, 255, 0.06);
                border-radius: 10px;
                height: 6px;
                width: 100%;
                margin: 0 auto 30px auto;
                overflow: hidden;
                border: 1px solid rgba(255, 255, 255, 0.02);
            }}
            #barra-llenado {{
                background: {color_alerta};
                height: 100%;
                width: {porcentaje_barra}%;
                box-shadow: 0 0 12px {color_alerta};
                border-radius: 10px;
                transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            #semaforo {{
                display: inline-block;
                padding: 12px 30px;
                border-radius: 50px;
                font-size: 14px;
                font-weight: 700;
                letter-spacing: 1.5px;
                background-color: rgba({color_rgb}, 0.12);
                color: {color_alerta};
                border: 1px solid rgba({color_rgb}, 0.35);
                text-shadow: 0 0 10px rgba({color_rgb}, 0.3);
                transition: all 0.5s ease;
            }}
            #footer-cloud {{
                margin-top: 25px;
                font-size: 11px;
                color: #45f3ff;
                opacity: 0.5;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 6px;
            }}
            #dot {{
                width: 7px;
                height: 7px;
                background-color: #00ff88;
                border-radius: 50%;
                display: inline-block;
                box-shadow: 0 0 8px #00ff88;
            }}
        </style>
    </head>
    <body>
        <div id="contenedor">
            <h1 id="titulo">Estación Central de Gas</h1>
            <div id="dato">{nivel_gas_actual}<span id="unidad">PPM</span></div>
            
            <div id="barra-contenedor">
                <div id="barra-llenado"></div>
            </div>

            <div id="semaforo">ESTADO: {estado_actual}</div>
            <div id="footer-cloud"><span id="dot"></span> Supabase Cloud Connected</div>
        </div>
    </body>
    </html>
    """

# RUTA POST: Aquí la ESP32 N°1 (Sensor) enviará los datos
@app.route('/actualizar_gas', methods=['POST'])
def actualizar_gas():
    global nivel_gas_actual, estado_actual
    data = request.get_json()
    
    if not data or 'nivel_gas' not in data:
        return jsonify({"error": "Datos inválidos"}), 400
        
    nivel_gas_actual = float(data['nivel_gas'])
    
    if nivel_gas_actual > 700:
        estado_actual = "CRITICO"
    elif nivel_gas_actual > 350:
        estado_actual = "ADVERTENCIA"
    else:
        estado_actual = "NORMAL"
        
    # 2. Guardar automáticamente el registro en Supabase forzando la conversión a entero (int)
    try:
        registro = {
            "nivel_gas": int(nivel_gas_actual),
            "estado": estado_actual
        }
        supabase.table("registros_gas").insert(registro).execute()
        print(f"[Supabase] ¡Registro respaldado con éxito! Nivel: {int(nivel_gas_actual)} PPM")
    except Exception as e:
        print(f"[Error Supabase] No se pudo guardar en la nube: {e}")
    
    return jsonify({"status": "ok", "estado_alertado": estado_actual}), 200

# RUTA GET: Aquí la ESP32 N°2 (Alarma) preguntará qué hacer
@app.route('/obtener_estado', methods=['GET'])
def obtener_estado():
    global estado_actual
    return jsonify({"estado": estado_actual}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
