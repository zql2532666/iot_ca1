from flask import Flask, render_template, request, jsonify, abort, redirect, url_for, flash
from gevent.pywsgi import WSGIServer
from gpiozero import LED
import database_utils
import mysql.connector as mysql
import Adafruit_DHT
from time import sleep
from gpiozero import MCP3008
from datetime import datetime
from time import sleep
import threading
from threading import Lock


app = Flask(__name__,
            static_folder='static',
            template_folder='templates')


RECORD_INTERVAL = 10
PIN = 24   

adc = MCP3008(channel=0)
lock = Lock()

LED_PIN = 13
led = LED(LED_PIN)
HOST = "localhost"
USER = "root"
PASSWORD = "root"
DATABASE = "iot_ca1"


def ldr_main():
      mysql_connection, mysql_cursor = database_utils.get_mysql_connection(HOST, USER, PASSWORD, DATABASE)
      while True:
            try:
                  light_value = adc.value

                  if light_value:
                        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        rows_affected = database_utils.insert_ldr_data(mysql_connection, mysql_cursor, light_value, current_datetime)
                        print("Light sensor reading: {}".format(light_value))
                        print("{} rows updated in the database...\n".format(rows_affected))

                  sleep(RECORD_INTERVAL)

            except Exception as err:
                  print(err)


def dht11_main():
      mysql_connection, mysql_cursor = database_utils.get_mysql_connection(HOST, USER, PASSWORD, DATABASE)
      while True:
            try:
                  humidity, temperature = Adafruit_DHT.read_retry(11, PIN)
                  print("Temp: {0} degree".format(temperature))
                  print("Humidity: {0} %".format(humidity))

                  if temperature and humidity:
                        # store the current temperature and humidity reading to database
                        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        rows_affected = database_utils.insert_dht11_data(mysql_connection, mysql_cursor, temperature, humidity, current_datetime)
                        print("{} rows updated in the database...\n".format(rows_affected))

                  sleep(RECORD_INTERVAL)

            except Exception as err:
                  print(err)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api/led-status', methods=['GET'])
def get_led_status():
    if led.is_lit:
        led_status = True
    else:
        led_status = False
 
    return jsonify({'led_status': led_status}), 201


@app.route('/api/led-on', methods=['GET'])
def turn_on_led():
    led.on()
    return jsonify({'completed': True}), 201


@app.route('/api/led-off', methods=['GET'])
def turn_off_led():
    led.off()
    return jsonify({'completed': True}), 201


@app.route('/api/latest-dht11-reading', methods=['GET'])
def retrieve_latest_dht11_reading():
    # create the connection and cursor object for database access
    mysql_connection, mysql_cursor = database_utils.get_mysql_connection(HOST, USER, PASSWORD, DATABASE)

    # retrieve the latest dht11 data from database
    latest_dht11_data = database_utils.retrieve_latest_dht11_data(mysql_connection, mysql_cursor)

    if latest_dht11_data:
        return jsonify(latest_dht11_data), 201
    else:
        abort(400)


@app.route('/api/latest-ldr-reading', methods=['GET'])
def retrieve_latest_ldr_reading():
    mysql_connection, mysql_cursor = database_utils.get_mysql_connection(HOST, USER, PASSWORD, DATABASE)  
    latest_ldr_data = database_utils.retrieve_latest_ldr_data(mysql_connection, mysql_cursor)

    if latest_ldr_data:
        return jsonify(latest_ldr_data), 201
    else:
        abort(400)


@app.route('/api/dht11-data', methods = ['GET'])
def retrieve_dht11_data():
    mysql_connection, mysql_cursor = database_utils.get_mysql_connection(HOST, USER, PASSWORD, DATABASE) 
    dht11_data = database_utils.retrieve_dht11_data(mysql_connection, mysql_cursor)

    if dht11_data:
        return jsonify(dht11_data), 201
    else:
        abort(400)

    

@app.route('/api/ldr-data', methods = ['GET'])
def retrieve_ldr_data():
    mysql_connection, mysql_cursor = database_utils.get_mysql_connection(HOST, USER, PASSWORD, DATABASE) 
    ldr_data = database_utils.retrieve_ldr_data(mysql_connection, mysql_cursor)

    if ldr_data:
        return jsonify(ldr_data), 201
    else:
        abort(400)

    


if __name__ == "__main__":

    try:
        t1 = threading.Thread(target=dht11_main, args=())
        t2 = threading.Thread(target=ldr_main, args=())
        t1.start()
        t2.start()

        http_server = WSGIServer(('0.0.0.0', 5000), app)
        # app.debug = True
        print('Waiting for requests.. ')
        http_server.serve_forever()

    except Exception as err:
        print(err)
