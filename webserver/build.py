from flask import Flask, redirect, render_template, jsonify, request, url_for, Response, session
import json
from geopy.geocoders import Nominatim
import time
from flask_socketio import SocketIO, emit
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_cors import CORS
import redis
from os import environ
from flask_session import Session

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
socket = SocketIO(app, cors_allowed_origins="*")

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'RaspberryPi'

# redis_server = redis.Redis("redis://127.0.0.1:6379")
redis_server = redis.Redis("localhost")
# app.config['SESSION_REDIS'] = redis.from_url('redis://127.0.0.1:6379')

# sess = Session()
# sess.init_app(app)

# Intialize MySQL
mysql = MySQL(app)

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
    print('-------------------------------')
    print(SN)
    coords = request.get_json()
    x_coord = coords['x']
    y_coord = coords['y']
    print('##############################')
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cursor.execute('UPDATE raspberries SET x = %s WHERE serialnumber = %s', (x_coord, SN))
    # print("SN {}: ({}, {})".format(SN, x_coord, y_coord))
    # cursor.execute('SELECT * FROM raspberries WHERE serialnumber = %s', (SN, ))
    # coords = cursor.fetchone()
    redis_server.set(SN, str((x_coord, y_coord)))
    print('Test Socket: {}'.format(redis_server.get(SN)))
    return 'Get data'

def register_user(SerialNumber, email, password):
    print(SerialNumber, email, password)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM raspberries WHERE serialnumber = %s OR email = %s', (SerialNumber, email))
    account = cursor.fetchone()
    if account:
        msg = 'Account already exists!'
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        msg = 'Invalid email address!'
    elif not re.match(r'[A-Za-z0-9]+', SerialNumber):
        msg = 'serialnumber must contain only characters and numbers!'
    elif SerialNumber is None or password is None or email is None:
        msg = 'Please fill out the form!'
    else:
        # Account doesnt exists and the form data is valid, now insert new account into raspberries table
        cursor.execute('INSERT INTO raspberries VALUES (NULL, %s, %s, %s, %s, %s)', (SerialNumber, password, email, 0, 0))
        mysql.connection.commit()
        msg = 'You have successfully registered! Please login.'
        # session[SerialNumber] = (0, 0)
        redis_server.set(SerialNumber, str((0, 0)))

    return msg

def auth_user(SerialNumber, password):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM raspberries WHERE serialnumber = %s AND password = %s', (SerialNumber, password))
        # Fetch one record and return result
    account = cursor.fetchone()
    return account

@app.route('/login', methods=['POST', 'GET'])
def login():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM raspberries')
    accounts = cursor.fetchall()
    for account in accounts:
        if not redis_server.exists(account['serialnumber']):
            redis_server.set(account['serialnumber'], str((0, 0)))
    if request.method == 'POST':
        if request.form.get('login-serialnumber') is None:
            if request.form.get('reg-password') == request.form.get('comfirm-password'):
                reg_serialnumber = request.form.get('reg-serialnumber')
                reg_email = request.form.get("reg-email")
                reg_password = request.form.get('reg-password')
                print(reg_serialnumber, reg_email, reg_password)
                print("=======================================")
                msg = register_user(reg_serialnumber, reg_email, reg_password)
                return render_template('login.html', msg=msg)
            else:
                return render_template('login.html', msg="please check username or password")

        else:
            login_serialnumber = request.form.get('login-serialnumber')
            login_password = request.form.get('login-password')
            if auth_user(login_serialnumber, login_password):
                return redirect(url_for('map', SerialNumber=login_serialnumber))
            else:
                return render_template('login.html', msg="please check username or password")
    else:
        return render_template('login.html')

@app.route('/map', methods=['POST', 'GET'])
def map():
    if request.method == 'GET':
        SerialNumber = request.args['SerialNumber']
        print(SerialNumber)
        return render_template('index.html', SerialNumber=SerialNumber)

@socket.on('get_time')
def get_time(SerialNumber):
    print(SerialNumber)
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    while True:
        coords = redis_server.get(SerialNumber).decode('ascii')
        [x, y] = coords.strip('(').strip(')').split(',')
        x_coord=float(x)
        y_coord=float(y)
        # cursor.execute('SELECT * FROM raspberries WHERE serialnumber = %s', (SerialNumber, ))
        # coords = cursor.fetchone()
        # print('Socket: {}'.format(coords))
        # emit('get_time', (coords['x'], coords['y']))
        print('Socket emit value {}'.format((x_coord, y_coord)))
        emit('get_time', (x_coord, y_coord))
=======
>>>>>>> 3c637b32fb289745221e53cccf170916d2aaed6e
>>>>>>> 10b2cd1d7a2aa123c4e7136f460fa3156627ec41
        time.sleep(1)

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
