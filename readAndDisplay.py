from utilities.database import Database
from time import sleep, time
from sense_hat import SenseHat
from utilities.cron import CronJob
import json

class ReadAndDisplayer():
    """
    An ReadAndDisplayer which constantly reading the sensor data
    from the database after a period of time and displaying the 
    temperture on sense hat LED display.

    Constants:
        -   TEXT_SCROLL_SPEED: Speed of the text being displayed
            on the LED matrix.
        -   TEMPERATURE_DISPLAY_TIME: The duration the temperature displays
            on the sensehat LED matrix.
        -   TEMPERATURE_CONFIG_FILE_PATH: Path to the temperature 
            configuration file.

    Variables:
        -   config: system configurations read from the config.json file.
    """

    RGB_HEX_RED = (255, 0, 0)
    RGB_HEX_GREEN = (0, 255, 0)
    RGB_HEX_BLUE = (0, 0, 255)
    RGB_HEX_BLACK = (0, 0, 0)
    
    TEXT_SCROLL_SPEED = 0.1
    TEMPERATURE_DISPLAY_TIME = 60 # 1 minute
    TEMPERATURE_CONFIG_FILE_PATH = 'config.json'

    def __init__(self):
        """
        Initialize the ReadAndDisplayer.

        Properties:
            -   sense: sense_hat object.
            -   database: Database object.
        """        
        self.database = Database()
        self.sense = SenseHat()
        self.load_config()

    def load_config(self):
        """
        Load the humidity and temperature configurations.
        """     
        with open(self.TEMPERATURE_CONFIG_FILE_PATH, 'r') as file:
            self.config = json.load(file)

    def run(self):
        """
        Main flow of the class
        """
        self.set_cron_job()
        while True:
            sensor_data = self.database.fetch_latest_sensor_data_record()
            self.display_temperature(sensor_data['temperature'])

    def display_temperature(self, temperature):
        """
        Display the temperature on the sensehat in a duration of time.
        """             
        text_color = self.get_text_color_based_on_temperature(temperature)
        start_time = time()
        while time() - start_time < self.TEMPERATURE_DISPLAY_TIME:
            self.sense.show_message(str(temperature), 
                                    text_colour = text_color,
                                    back_colour = self.RGB_HEX_BLACK,
                                    scroll_speed = self.TEXT_SCROLL_SPEED)            

    def get_text_color_based_on_temperature(self, temperature):
        """
        Get the text color based on the current temperature.
        """             
        if (self.is_cold(temperature)):
            return self.RGB_HEX_BLUE
        elif (self.is_hot(temperature)):
            return self.RGB_HEX_RED
        else:
            return self.RGB_HEX_GREEN

    def is_cold(self, temperature):
        """
        Return true if the temperature is cold.
        """             
        return (temperature <= self.config['temperature']['comfortable_min'])
    
    def is_hot(self, temperature):  
        """
        Return true if the temperature is hot.
        """             
        return (temperature >= self.config['temperature']['comfortable_max'])

    def set_cron_job(self):
        """
        Set the cron job if the job does not
        exist in the crontab.
        """
        command = ' && @reboot python3 readAndDisplay.py'
        cron = CronJob(command)
        cron.set_job(comment='taskB')


if __name__ == '__main__':
    rad = ReadAndDisplayer()
    rad.run()