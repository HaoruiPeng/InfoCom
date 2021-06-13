import requests
import time
import random

SERVER_URL = "http://127.0.0.1:5000/clock"
SerialNumber = '111111'
params = {'SerialNumber': SerialNumber}

with requests.Session() as session:
    while True:
        current_location = {'x': round(random.random()*100,9),
                            'y': round(random.random()*100,9)}
        print(current_location)
        resp = session.post(SERVER_URL, json=current_location, params=params)
        print(resp.text)
        time.sleep(2)
