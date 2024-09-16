import requests
import os
from dotenv import load_dotenv
import time



load_dotenv()
govee_api = os.getenv('GOVEE_API_KEY')
device = os.getenv("DEVICE_KEY")
# print(device)
model = os.getenv("MODEL_KEY")
# print(model)

shutdown_color = (175, 0, 0)


def get_colour(): #sends request to govee api to change colour of lamp
    base_url = "https://developer-api.govee.com/v1/devices/state"
    headers = {
        "Govee-API-Key": govee_api,
        "Content-Type": "application/json"
    }
    params = {
        "device": device,
        "model": model,
    }
    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        for item in data['data']['properties']:
            if "color" in item:
                r = data['data']['properties'][3]['color']['r'] #RED
                g = data['data']['properties'][3]['color']['g'] #RED
                b = data['data']['properties'][3]['color']['b'] #RED
                return r, g, b
            else:
                pass
    else:
        print(" --- FAIL --- ")

def shutdown_computer():
    print(" --- PC SHUTTING DOWN ---")
    os.system('shutdown /s /f /t 3')

def main():
    while True:
        lamp_colour = get_colour()
        if lamp_colour:
            if lamp_colour == shutdown_color:
                shutdown_computer()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()