from flask import Flask, request
from flask_restful import Resource, Api
from utilities.database import Database
import json

app = Flask(__name__)
api = Api(app)

class API(Resource):
    def __init__(self):
        self.database = Database()

    def get(self):
        sensor_data = self.database.fetch_latest_sensor_data_record()
        response_data = {"timestamp": sensor_data['time'],
                        "humidity": sensor_data['humidity'],
                        "temperature": sensor_data['temperature']}
        return response_data, 200
    
    def post(self):
        temperature = request.form['temperature']
        humidity = request.form['humidity']
        if (self.database.add_sensor_data_record(humidity, temperature)):
            return {"success": True}, 200
        else: 
            return {"success": False}, 500

    def put(self):
        temperature = request.form['temperature']
        humidity = request.form['humidity']
        sensor_data = self.database.fetch_latest_sensor_data_record()
        if (self.database.update_sensor_data_status(sensor_data['time'], 
                                                    humidity, 
                                                    temperature)):
            return {"success": True}, 200
        else: 
            return {"success": False}, 500


api.add_resource(API, '/')

if __name__ == '__main__':
    app.run(debug=True)