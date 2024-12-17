from __future__ import print_function
import weatherapi
import json
from weatherapi.rest import ApiException
import google.generativeai as genai
import os

genai.configure(api_key='YOUR_API_KEY')
# Configure API key authorization: ApiKeyAuth
configuration = weatherapi.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
sijainti = (input("Anna sijainti: ").capitalize())
# create an instance of the API class
api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))
q = sijainti  # City name
days = 2  # Forecast for 3 days
lang = 'fi'  

try:
    # Forecast API
    api_response = api_instance.forecast_weather(q, days, lang=lang)

    
    location = api_response['location']
    forecast_days = api_response['forecast']['forecastday']
    
    print(f"Sijainti: {location['name']}, {location['region']}\n")
    temp = api_response['current']['temp_c']
    current_condition = api_response['current']['condition']['text']
    print("Sää tänään:")
    print(f"Lämpötila: {temp}")
    print(f"Olosuhteet: {current_condition}\n")
    print("Sääennuste:")
    for day in forecast_days[1:]:
        date = day['date']
        maxtemp = day['day']['maxtemp_c']
        mintemp = day['day']['mintemp_c']
        avgtemp = day['day']['avgtemp_c']
        condition = day['day']['condition']['text']
        
        print(f"Päivämäärä: {date}")
        print(f"  Keskiarvo lämpötila: {avgtemp}°C")
        print(f"  Korkein lämpötila: {maxtemp}°C")
        print(f"  Matalin lämpötila: {mintemp}°C")
        print(f"  Olosuhteet: {condition}\n")

    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Anna lyhyt kuvaus kunnasta {sijainti}.")
    print(response.text) 
        

except ApiException as e:
    print("Exception when calling APIsApi->forecast_weather: %s\n" % e)
except Exception as e:
    print(f"Yleinen virhe: {e}")
