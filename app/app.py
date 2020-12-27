from flask import Flask, render_template, request, jsonify, abort, redirect, url_for, flash
from gevent.pywsgi import WSGIServer
from gpiozero import LED
import database_utils
import mysql.connector as mysql


app = Flask(__name__,
            static_folder='static',
            template_folder='templates')


LED_PIN = 13
led = LED(LED_PIN)
HOST = "localhost"
USER = "root"
PASSWORD = "root"
DATABASE = "iot_ca1"


@app.route('/')
def index():
    return render_template("index.html")


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
        http_server = WSGIServer(('0.0.0.0', 5000), app)
        app.debug = True
        print('Waiting for requests.. ')
        http_server.serve_forever()
    except Exception as err:
        print(err)