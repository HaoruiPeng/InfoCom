from flask import Flask, redirect, render_template, jsonify, request, url_for, Response, session
import json
from geopy.geocoders import Nominatim
import time
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
socket = SocketIO(app, cors_allowed_origins="*")

class DataStore():
    SN = None
    rasp_time = None

rasp_data = DataStore()

def translate(coords):
    x_origins_lim = (13.143390664, 13.257501336)
    y_origins_lim = (55.678138854000004, 55.734680845999996)

    x_translated_lim = (212.155699, 968.644301)
    y_translated_lim = (103.68, 768.96)

    x_origin = coords[0]
    y_origin = coords[1]

    x_ratio = (x_translated_lim[1] - x_translated_lim[0]) / (x_origins_lim[1] - x_origins_lim[0])
    y_ratio = (y_translated_lim[1] - y_translated_lim[0]) / (y_origins_lim[1] - y_origins_lim[0])
    x_translated = x_ratio * (x_origin - x_origins_lim[0]) + x_translated_lim[0]
    y_translated = y_ratio * (y_origins_lim[1] - y_origin) + y_translated_lim[0]

    return x_translated, y_translated

@app.route('/')
def do_GET():
    return redirect(url_for('login'))

@app.route('/clock', methods=['POST'])
def get_clock():
    SN = request.args.get('SerialNumber')
    current_time = request.get_json()
    rasp_data.SN = SN
    rasp_data.rasp_time = str(current_time['time'])
    print("SN {}: {}".format(SN, current_time['time']))
    return 'Get data'

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        r = request.form.get('SerialNumber')
        return redirect(url_for('map', SerialNumber=r))
    else:
        return render_template('login.html')

@app.route('/map', methods=['POST', 'GET'])
def map():
    if request.method == 'GET':
        SerialNumber = request.args['SerialNumber']
        print(SerialNumber)
        return render_template('index.html', SerialNumber=SerialNumber)

@socket.on('get_time')
def get_time():
    while True:
        current_time = rasp_data.rasp_time
        print(current_time)
        emit('get_time', current_time)
        time.sleep(2)

@app.route('/submit',  methods=['POST'])
def do_submit():
    geolocator = Nominatim(user_agent="my_request")
    region = ", Lund, Skåne, Sweden"
    r = json.loads(request.data.decode())
    if r['dst_addr'] == "" or r['src_addr'] == "":
        return "Input your address"
    src_addr = r['src_addr'] + region
    dst_addr = r['dst_addr'] + region

    src_location = geolocator.geocode(src_addr)
    dst_location = geolocator.geocode(dst_addr)

    if src_location is None and dst_location is None:
        return "Couldn't find source and destinations addresses, try another input"
    elif src_location is None:
        return "Couldn't find source address, try another input"
    elif dst_location is None:
        return "Couldn't find destinations address, try another input"

    src_x, src_y = translate((src_location.longitude, src_location.latitude))
    dst_x, dst_y = translate((dst_location.longitude, dst_location.latitude))

    data = { 'src_x': src_x,
             'src_y': src_y,
             'dst_x': dst_x,
             'dst_y': dst_y
            }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
