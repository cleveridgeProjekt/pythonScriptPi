import time
import adafruit_dht
import board
import requests

api_url = 'https://cleveridge.onrender.com/api/sensor'
dht_device = adafruit_dht.DHT22(board.D4)
while True:
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        if temperature is not None and humidity is not None:
            payload = {
                "status":"online",
                "temperature":round(temperature, 2),
                "humidity":round(humidity, 2)
            }
                
            response = requests.post(api_url, json=payload)
            print(f"Sent data: {payload}, Response: {response.status_code}")
        else:
            print("Sensor read failed. Trying again ...")
    except Exception as error:
        print("Error:", error)
    time.sleep(10) #send every 10 seconds
