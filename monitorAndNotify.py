from utilities.database import Database
from utilities.pushbullet import PushBullet
from time import sleep, time
from datetime import datetime
from sense_hat import SenseHat
import json 

class MonitorAndNotifier():
    SENSOR_DATA_COLLECT_PERIOD = 60 # seconds
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
            sensor_data = self.get_sensor_data()
            print(sensor_data)
            self.database.add_sensor_data_record(*sensor_data.values())
            if (self.is_outside_comfortable_range(sensor_data) and 
                not self.is_notified_today()):
                    notification_id = self.notify(sensor_data)
                    self.database.add_notification_record(notification_id)
            sleep(self.SENSOR_DATA_COLLECT_PERIOD)        

    def get_sensor_data(self):
        return {'humidity': round(self.sense.get_humidity()), 
                'temperature': round(self.sense.get_temperature())}

    def is_outside_comfortable_range(self, sensor_data):
        if (not self.is_comfortable(sensor_data['temperature'])):
            return True
        if (not self.is_comfortable(sensor_data['humidity'])):
            return True
        return False

    def is_comfortable(self, value):
        return value in range(self.config['comfortable_min'], 
                              self.config['comfortable_max'] + 1)

    def is_notified_today(self):
        notification = self.database.fetch_latest_notification_record()
        if (notification == None): 
            return False
        today = datetime.today().date()
        last_notify_date = datetime.fromtimestamp(notification['time']).date()
        return ((today - last_notify_date).days == 0)          

    def notify(self, sensor_data):
        uncomfortable_level = self.calculate_uncomfortable_level(sensor_data)
        title = self.construct_notify_title(uncomfortable_level)
        body = self.construct_notify_body(sensor_data)
        pushbullet = PushBullet()
        pushbullet_result = pushbullet.push_notification(title, body)
        return pushbullet_result['iden']

    def calculate_uncomfortable_level(self, sensor_data):
        level = 0
        if (not self.is_comfortable(sensor_data['temperature'])):
            level += 1
        if (not self.is_comfortable(sensor_data['humidity'])):
            level += 2
        return level

    def construct_notify_title(self, level):
        title = '''[Warning] The {} is outside comfortable range!'''
        if (level == 1):
            return title.format("temperature")
        elif (level == 2):
            return title.format("humidity")
        else:
            return title.format("temperature and humidity")        

    def construct_notify_body(self, sensor_data):
        body =  'Current temperature: {}.\nCurrent humidity: {}.'
        return body.format(sensor_data['temperature'],
                           sensor_data['humidity'])

if __name__ == '__main__':
    man = MonitorAndNotifier()
    man.run()