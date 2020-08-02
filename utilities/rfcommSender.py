import json
from sense_hat import SenseHat
import bluetooth
from monitorAndNotify import MonitorAndNotifier


class RFCOMMSender:
    """
    A RFCOMM protocol bluetooth client which finds the service
    being broadcasted by the servers to connect and sends the
    temperature and humidity data.

    Constants:
        -   UUID: uuid hex number to define the unique service
            used between servers and client.
    """
    UUID = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848"

    def __init__(self):
        """
        Initialize client

        Properties:
            -   sock: rfcomm client socket object.
            -   min_temperature: minimum temperature read from config file.
            -   max_temperature: maximum temperature read from config file.
            -   min_humidity: minimum humidity read from config file.
            -   max_humidity: maximum humidity read from config file.
            -   temperature_value: temperature value read from sensor.
            -   humidity_value: humidity value read from sensor.
            -   sense: sense_hat object.
        """
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.min_temperature = None
        self.max_temperature = None
        self.min_humidity = None
        self.max_humidity = None
        self.temperature_value = None
        self.humidity_value = None
        self.sense = SenseHat()

    def read_config(self):
        """
        Read min/max temperature and min/max humidity value
        from config.json file.
        """
        with open('config.json') as file:
            data = json.load(file)
            self.min_temperature = data['temperature']['min']
            self.max_temperature = data['temperature']['max']
            self.min_humidity = data['humidity']['min']
            self.max_humidity = data['humidity']['max']

    def find_and_connect_service(self):
        """
        Find the service being broadcasted by the servers
        to connect and send data.
        """
        while True:
            service_matches = bluetooth.find_service(uuid=self.UUID)
            if len(service_matches) != 0:
                first_match = service_matches[0]
                port = first_match["port"]
                name = first_match["name"]
                host = first_match["host"]
                self.sock.connect((host, port))
                return

    def read_sensor_data(self):
        """
        Read temperature and humidity data from sense hat's sensors
        """
        monitor = MonitorAndNotifier()
        sensor_data = monitor.get_sensor_data()
        self.temperature_value = sensor_data['temperature']
        self.humidity_value = sensor_data['humidity']

    def data_within_range(self):
        """
        Check if the temperature/humidity value read from sensors
        are in the min/max range defined in the config.json file
        before sending.
        """
        return (self.temperature_value >= self.min_temperature) \
            & (self.temperature_value <= self.max_temperature) \
            & (self.humidity_value >= self.min_humidity) \
            & (self.humidity_value <= self.max_humidity)

    def send_data(self):
        """
        Convert temperature/humidity value from float to string,
        combine them into a string seperated by a comma (',')
        and send them to other rpis.
        """
        data = str(self.temperature_value) + ',' + str(self.humidity_value)
        self.sock.send(data)

    def disconnect(self):
        """
        Close the client socket after finishing data transfer.
        """
        self.sock.close()

    def execute(self):
        """
        Main flow of the program.
        """
        self.read_sensor_data()
        self.read_config()
        if self.data_within_range():
            self.find_and_connect_service()
            self.send_data()
            self.disconnect()
