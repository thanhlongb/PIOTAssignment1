import requests

class APITestKit:
    SERVER_URL = 'http://127.0.0.1:5000/'
    MANUAL_TEXT = '''Available options:
    1. Get newest temp, humidity, timestamp
    2. Upload a record to database
    3. Update newest record
    4. Exit'''

    def __init__(self):
        pass

    def run(self):
        while True:
            print(self.MANUAL_TEXT)
            option = input("Your option: ")
            if (option == '1'):
                self.send_get_request()
            elif (option == '2'):
                self.send_post_request()
            elif (option == '3'):
                self.send_put_request()
            elif (option == '4'):
                break
            else:
                print(">> Invalid option.")
        print(">> Goodbye.")
            
    def send_get_request(self):
        try:
            response = requests.get(self.SERVER_URL)
        except:
            print(">> Can't connect.")
            return
        print(response.json())

    def send_post_request(self):
        sensor_data = self.prompt_sensor_data()
        try:
            response = requests.post(self.SERVER_URL,
                                    data = sensor_data).json()
        except:
            print(">> Can't connect.")
            return
        if (response['success']):
            print(">> Success.")
        else:
            print(">> Failed.")

    def send_put_request(self):
        sensor_data = self.prompt_sensor_data()
        try:
            response = requests.put(self.SERVER_URL,
                                    data = sensor_data).json()
        except:
            print(">> Can't connect.")
            return
        if (response['success']):
            print(">> Success.")
        else:
            print(">> Failed.")
    
    def prompt_sensor_data(self):
        temperature = input("Temperature: ")
        humidity = input("Humidity: ")
        return  {"temperature": temperature, 
                 "humidity": humidity}

if __name__ == '__main__':
    atk = APITestKit()
    atk.run()
