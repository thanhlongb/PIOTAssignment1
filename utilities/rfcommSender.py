import sys
import bluetooth
from sense_hat import SenseHat
import json

class RFCOMMSender:
    UUID = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848"
    def __init__(self):
        self.sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        self.min_temperature = None
        self.max_temperature = None
        self.min_humidity = None
        self.max_humidity = None
        self.temperature_value = None
        self.humidity_value = None
        self.sense = SenseHat()

    def read_config(self):
        with open('config_min_max.json') as file:
            data = json.load(file)
            self.min_temperature = data['min_temperature']
            self.max_temperature = data['max_temperature']
            self.min_humidity = data['min_humidity']
            self.max_humidity = data['max_humidity']

    def find_and_connect_service(self):
        while True:
            service_matches = bluetooth.find_service( uuid = self.UUID )
            if len(service_matches) != 0:
                first_match = service_matches[0]
                port = first_match["port"]
                name = first_match["name"]
                host = first_match["host"]
                print("connecting to \"%s\" on %s" % (name, host))
                self.sock.connect((host, port))

    def read_sensor_data(self):
        self.temperature_value = self.sense.get_temperature()
        self.humidity_value = self.sense.get_humidity()

    def data_within_range(self):
        return (((self.temperature_value >= self.min_temperature) & (self.temperature_value <= self.max_temperature))
                & ((self.humidity_value >= self.min_humidity) & (self.humidity_value <= self.max_humidity)))

    def send_data(self):
        data = str(self.temperature_value) + ',' + str(self.humidity_value)
        self.sock.send(data)

    def disconnect(self):
        self.sock.close()

    def execute(self):
        self.read_sensor_data()
        self.read_config()
        if self.data_within_range():
            self.find_and_connect_service()
            self.send_data()
            self.disconnect()
            


