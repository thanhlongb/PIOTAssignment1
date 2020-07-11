from utilities.database import Database
from time import sleep, time
from sense_hat import SenseHat
import json

class ReadAndDisplayer():
    RGB_HEX_RED = (255, 0, 0)
    RGB_HEX_GREEN = (0, 255, 0)
    RGB_HEX_BLUE = (0, 0, 255)
    RGB_HEX_BLACK = (0, 0, 0)
    
    TEXT_SCROLL_SPEED = 0.1
    TEMPERATURE_DISPLAY_TIME = 60 # 1 minute
    TEMPERATURE_CONFIG_FILE_PATH = 'config.json'

    config = dict()

    def __init__(self):
        self.database = Database()
        self.sense = SenseHat()
        self.load_config()

    def load_config(self):
        with open(self.TEMPERATURE_CONFIG_FILE_PATH, 'r') as file:
            self.config = json.load(file)

    def run(self):
        while True:
            sensor_data = self.database.fetch_latest_sensor_data_record()
            print(sensor_data['time'])
            self.display_temperature(sensor_data['temperature'])

    def display_temperature(self, temperature):
        text_color = self.get_text_color_based_on_temperature(temperature)
        start_time = time()
        while time() - start_time < self.TEMPERATURE_DISPLAY_TIME:
            self.sense.show_message(str(temperature), 
                                    text_colour = text_color,
                                    back_colour = self.RGB_HEX_BLACK,
                                    scroll_speed = self.TEXT_SCROLL_SPEED)            

    def get_text_color_based_on_temperature(self, temperature):
        if (self.is_cold(temperature)):
            return self.RGB_HEX_BLUE
        elif (self.is_hot(temperature)):
            return self.RGB_HEX_RED
        else:
            return self.RGB_HEX_GREEN

    def is_cold(self, temperature):
        return (temperature <= self.config['cold_max'])
    
    def is_hot(self, temperature):
        return (temperature >= self.config['hot_min'])

if __name__ == '__main__':
    rad = ReadAndDisplayer()
    rad.run()