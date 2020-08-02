from flask import Flask, request
from flask_restful import Resource, Api
from utilities.database import Database
from utilities.cron import CronJob
import json

app = Flask(__name__)
api = Api(app)

class API(Resource):
    """
    A API class with the following operations:
        -   Allow RESTful GET requests to get the latest sensor data.
        -   Allow RESTful POST requests to add new sensor data.
        -   Allow RESTful PUT requests to update latest sensor data.
    """    

    def __init__(self):
        self.database = Database()

    def get(self):
        '''
        Return the latest sensor data in JSON format.
        '''
        sensor_data = self.database.fetch_latest_sensor_data_record()
        response_data = {"timestamp": sensor_data['time'],
                        "humidity": sensor_data['humidity'],
                        "temperature": sensor_data['temperature']}
        return response_data, 200
    
    def post(self):
        '''
        API endpoint for adding a new sensor data record. 
        '''
        temperature = request.form['temperature']
        humidity = request.form['humidity']
        if (self.database.add_sensor_data_record(humidity, temperature)):
            return {"success": True}, 200
        else: 
            return {"success": False}, 500

    def put(self):
        '''
        API endpoint for updating the latest sensor data record. 
        '''
        temperature = request.form['temperature']
        humidity = request.form['humidity']
        sensor_data = self.database.fetch_latest_sensor_data_record()
        if (self.database.update_sensor_data_status(sensor_data['time'], 
                                                    humidity, 
                                                    temperature)):
            return {"success": True}, 200
        else: 
            return {"success": False}, 500

    def set_cron_job(self):
        """
        Set the cron job if the job does not
        exist in the crontab.
        """
        command = ' && python3 apiRESTful.py'
        cron = CronJob(command)
        cron.set_job()

api.add_resource(API, '/')

if __name__ == '__main__':
    api.set_cron_job()
    app.run(debug=True)