import subprocess
import sys
import os
import pandas as pd
import requests 
from translate import Translator
import unidecode
from credenciales import api_key, twilio_account_sid, twilio_auth_token, f_phone_number, t_phone_number
from twilio.rest import Client
from datetime import datetime
import pandas as pd
import requests
import json 

# obtener la fecha de hoy
fecha_actual = datetime.today().strftime("%d de %B del %Y")

#cargar datos de json
with open('consulta.json') as f:
    data = json.load(f)
    
#acceder a las coordenadas del municipio o ciudad
locacion = data ['locacion'][0]
lat = locacion ['lat']
lon = locacion ['lon']

# Definir función para consultar el pronóstico del clima
def obtener_pronostico(lat, lon):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={lat},{lon}&days=1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Realizar la consulta con las coordenadas
pronostico = obtener_pronostico(lat,lon )

# Crear lista para almacenar los pronósticos
pronosticos = []

# Verificar si se obtuvo el pronóstico
if pronostico and pronostico['location']['country'] == 'Mexico':
    for forecast_day in pronostico['forecast']['forecastday']:
        forecast = forecast_day['day']
        pronosticos.append({
            'municipio': pronostico['location']['name'],
            'forecast_date': forecast_day['date'],
            'maxtemp_c': forecast['maxtemp_c'],
            'mintemp_c': forecast['mintemp_c'],
            'condition_text': forecast['condition']['text'],
            'wind_kph': forecast.get('maxwind_kph')
        })
else:
    # Si no se obtuvo pronóstico válido, añade entradas vacías
    for i in range(3):
        pronosticos.append({
            'municipio': "Desconocido",
            'forecast_date': None,
            'maxtemp_c': None,
            'mintemp_c': None,
            'condition_text': None,
            'wind_kph': None
        })

# Convertir la lista de pronósticos en un DataFrame
df_pronosticos = pd.DataFrame(pronosticos)

# cambiar los nombres de las columnas a español
df_pronosticos.columns = ['municipio', 'fecha_pronostico', 'temp_max_c', 'temp_min_c', 'condicion', 'velocidad_viento']

# crear un traductor del inglés al español
translator = Translator(to_lang="es")

# función para traducir texto
def traducir(texto):
    try:
        if texto is not None:
            return translator.translate(texto)
        else:
            return texto
    except Exception as e:
        return texto

# aplicar la traducción a la columna condition_text
df_pronosticos['condicion'] = df_pronosticos['condicion'].apply(traducir)

# quitar acentos en la columna condicion
df_pronosticos['condicion'] = df_pronosticos['condicion'].apply(lambda x: unidecode.unidecode(x))

# poner los nombres de los municipios con la primera letra en mayúscula
df_pronosticos['municipio'] = df_pronosticos['municipio'].apply(lambda x: x.title())

mensaje = f"Clima para hoy {fecha_actual} en {pronostico['location']['name']}:\n"
for index, row in df_pronosticos.iterrows():
    mensaje += f"+ Max: {row['temp_max_c']}°C,- Min: {row['temp_min_c']}°C, Condición: {row['condicion']}, Viento: {row['velocidad_viento']} kph\n"

# enviar mensaje usando Twilio
client = Client(twilio_account_sid, twilio_auth_token)
message = client.messages.create(
    body=mensaje,
    from_=f_phone_number,
    to=t_phone_number
)
