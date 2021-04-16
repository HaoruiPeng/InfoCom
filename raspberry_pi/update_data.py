import requests
import time

SERVER_URL = "http://127.0.0.1:5000/clock"
SerialNumber = '0000000'
params = {'SerialNumber': SerialNumber}

with requests.Session() as session:
    while True:
        current_time = {'time': time.time()}
        resp = session.post(SERVER_URL, json=current_time, params=params)
        print(resp.text)
        time.sleep(2)
