import requests
import json
import smtplib
import logging
from email.message import EmailMessage
from datetime import datetime

# Cargar configuración
with open('config.json') as config_file:
    config = json.load(config_file)

API_KEY = config['API_KEY']
URL = 'https://api.vatstack.com/v1/quotes'
SMTP_SERVER = config['SMTP_SERVER']
SMTP_PORT = config['SMTP_PORT']
SMTP_USERNAME = config['SMTP_USERNAME']
SMTP_PASSWORD = config['SMTP_PASSWORD']
CORREO_DESTINATARIO = config['CORREO_DESTINATARIO']

# Configuración inicial de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def obtener_tasas_iva_actuales(api_key, amount=10000):
    tasas_iva_actuales = {}
    try:
        with open('tasas_iva.json', 'r') as archivo:
            paises = json.load(archivo)
    except FileNotFoundError:
        logging.error("Archivo 'tasas_iva.json' no encontrado.")
        return tasas_iva_actuales

    for codigo_pais in paises.keys():
        headers = {'X-API-KEY': api_key}
        payload = {'amount': amount, 'country_code': codigo_pais}
        try:
            response = requests.post(URL, json=payload, headers=headers)
            response.raise_for_status()  # Esto lanzará una excepción para respuestas 4xx y 5xx
            response_data = response.json()
            logging.info(f"Respuesta obtenida de la API para {codigo_pais}: {json.dumps(response_data, indent=4)}")
            tasas_iva_actuales[codigo_pais] = response_data
        except requests.HTTPError as e:
            logging.error(f"Error en la solicitud de la API para {codigo_pais}: {e}")

    return tasas_iva_actuales

def comparar_y_alertar(tasas_iva_nuevas, archivo_almacenamiento='tasas_iva.json'):
    cambios_detectados = False
    mensaje_cambios = ""

    try:
        with open(archivo_almacenamiento, 'r') as archivo:
            tasas_iva_almacenadas = json.load(archivo)
    except FileNotFoundError:
        tasas_iva_almacenadas = {}

    for codigo_pais, tasa_iva_nueva in tasas_iva_nuevas.items():
        tasa_iva_actual = tasa_iva_nueva['vat']['rate']
        tasa_iva_almacenada = tasas_iva_almacenadas.get(codigo_pais, {}).get('rate')

        if tasa_iva_almacenada is None or tasa_iva_almacenada != tasa_iva_actual:
            cambios_detectados = True
            mensaje_cambios += f"Cambio detectado en {codigo_pais}: {tasa_iva_almacenada} -> {tasa_iva_actual}\n"
            tasas_iva_almacenadas[codigo_pais] = {'rate': tasa_iva_actual}

    if cambios_detectados:
        enviar_correo(mensaje_cambios)

    with open(archivo_almacenamiento, 'w') as archivo:
        json.dump(tasas_iva_almacenadas, archivo, indent=4)

def enviar_correo(mensaje):
    subject = "Cambios en tasas de IVA - Informe Diario"
    cuerpo_mensaje = f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nSe han detectado cambios en las tasas de IVA:\n\n{mensaje}"

    msg = EmailMessage()
    msg.set_content(cuerpo_mensaje)
    msg['Subject'] = subject
    msg['From'] = SMTP_USERNAME
    msg['To'] = CORREO_DESTINATARIO

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    logging.info("Iniciando proceso de obtención y comparación de tasas de IVA.")
    tasas_iva_actuales = obtener_tasas_iva_actuales(API_KEY)
    comparar_y_alertar(tasas_iva_actuales)
