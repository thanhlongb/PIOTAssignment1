import requests
import json

class PushBullet():
    ACCESS_TOKEN = 'o.q4R1S0YclioxuKil3GHjThCPFET7fzKm'
    API_ENDPOINTS = {
        'pushes': 'https://api.pushbullet.com/v2/pushes'
    }

    def __init__(self):
        pass

    def push_notification(self, title, body):
        payload = {"body": body, "title": title, "type": "note"}
        headers = {'Access-Token': self.ACCESS_TOKEN,
                   'Content-Type': 'application/json'}
        response = requests.post(self.API_ENDPOINTS['pushes'], 
                                 data = json.dumps(payload), 
                                 headers = headers)
        return json.loads(response.content)