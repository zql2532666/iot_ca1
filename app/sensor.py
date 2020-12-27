import Adafruit_DHT
from time import sleep
from gpiozero import MCP3008
from datetime import datetime
from time import sleep
import threading
from threading import Lock
import database_utils
import mysql.connector as mysql


RECORD_INTERVAL = 5
PIN = 24   # pin number is 24

adc = MCP3008(channel=0)
lock = Lock()

HOST = "localhost"
USER = "root"
PASSWORD = "root"
DATABASE = "iot_ca1"

mysql_connection, mysql_cursor = database_utils.get_mysql_connection(HOST, USER, PASSWORD, DATABASE)


def ldr_main():
      while True:
            try:
                  light_value = adc.value

                  if light_value:
                        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        lock.acquire()
                        rows_affected = database_utils.insert_ldr_data(mysql_connection, mysql_cursor, light_value, current_datetime)
                        lock.release()
                        print("Light sensor reading: {}".format(light_value))
                        print("{} rows updated in the database...\n".format(rows_affected))

                  sleep(5)

            except Exception as err:
                  print(err)


def dht11_main():
      while True:
            try:
                  humidity, temperature = Adafruit_DHT.read_retry(11, PIN)
                  print("Temp: {0} degree".format(temperature))
                  print("Humidity: {0} %".format(humidity))

                  if temperature and humidity:
                        # store the current temperature and humidity reading to database
                        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        lock.acquire()
                        rows_affected = database_utils.insert_dht11_data(mysql_connection, mysql_cursor, temperature, humidity, current_datetime)
                        lock.release()
                        print("{} rows updated in the database...\n".format(rows_affected))

                  sleep(RECORD_INTERVAL)

            except Exception as err:
                  print(err)


if __name__ == "__main__":
      # t1 = threading.Thread(target=dht11_main, args=())
      t2 = threading.Thread(target=ldr_main, args=())
      
      
      # t1.start()
      t2.start()

      # t1.join()
      t2.join()