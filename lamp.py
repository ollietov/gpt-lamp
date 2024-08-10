import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
import re

def main():
    try:
        load_dotenv()
        client = OpenAI() #auto gets API key from env
        govee_api = os.getenv('GOVEE_API_KEY')
        weather_api = os.getenv('WEATHER_API_KEY')
        device = os.getenv("DEVICE_KEY")
        print(device)
        model = os.getenv("MODEL_KEY")
        print(model)

        def get_weather(city): # get weather in city
            base_url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': weather_api,
                'units': 'metric'
            }
            response = requests.get(base_url, params=params)
            if response.status_code != 200:
                print("Weather failed")
                return None
            
            #Extracts description, temperature, humidity and wind from API call
            weather_json = response.json()
            weather_desc = str(weather_json['weather'][0]['description'])
            weather_temp = str(weather_json['main']['temp']) + "°C"
            weather_humdity = str(weather_json['main']['humidity']) + "%"
            weather_wind = str(weather_json['wind']['speed']) + " meters per second"
            print(weather_desc, weather_temp, weather_humdity, weather_wind)
            return weather_desc, weather_temp, weather_humdity, weather_wind
            
        weather_desc, weather_temp, weather_humdity, weather_wind = get_weather("London")

        def get_colour(weather_desc, weather_temp, weather_humidity, weather_wind): # asks gpt to select a colour depending on weather factors
            completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a smart home assistant and you should determine the colour of my lamp determining on the current weather to match. Return only the RGB values for the colour"},
                {"role": "user", "content": f"The current weather description is {weather_desc}. The current temperature is {weather_temp}. The current humidity is {weather_humidity}. The current wind is {weather_wind}."}
            ]
            )
            return completion.choices[0].message.content
        def extract_rgb(message): #extracts rgb values from gpt response
            message = message[4:-1]
            result = message.split(",")
            r = int(result[0])
            g = int(result[1])
            b = int(result[2])

            return r, g, b

        rgb_text = get_colour(weather_desc, weather_temp, weather_humdity, weather_wind)
        r, g, b = extract_rgb(rgb_text)

        def put_colour(r,g,b): #sends request to govee api to change colour of lamp
            base_url = "https://developer-api.govee.com/v1/devices/control"
            headers = {
                "Govee-API-Key": govee_api,
                "Content-Type": "application/json"
            }
            data = {
                "device": device,
                "model": model,
                "cmd": {
                    "name": "color",
                    "value": {
                        "r": r,
                        "g": g,
                        "b": b
                    }
                }
            }
            response = requests.put(base_url, headers=headers, json=data)
            if response.status_code == 200:
                print(f"Changing colour to {r, g, b}")
            else:
                print("Changing colour failed")
        put_colour(r, g, b)

        
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()