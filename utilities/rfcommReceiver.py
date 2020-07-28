import bluetooth
from sense_hat import SenseHat

class RFCOMMReceiver:
    UUID = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848"
    PORT = 1
    SCROLL_SPEED = 0.05
    TEXT_COLOUR = [100,100,100]
    def __init__(self):
        self.client_sock = None
        self.client_address = None
        self.server_sock = None
        self.sense = SenseHat()

    def advertise_and_connect(self):
        self.server_sock = server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        server_sock.bind(("",self.PORT))
        server_sock.listen(1)
        print("listening on port %d" % self.PORT)
        bluetooth.advertise_service( self.server_sock, "Sensor Service", self.UUID )
        self.client_sock, self.address = self.server_sock.accept()
        print("Accepted connection from ",self.address)

    def show_message(self, message):
        self.sense.show_message(message, scroll_speed=self.SCROLL_SPEED, text_colour=self.TEXT_COLOUR)

    def display_data(self):
        data = self.client_sock.recv(1024)
        data_string = data.decode('utf-8')
        data_split = data_string.split(",")
        temperature = float(data_split[0])
        humidity = float(data_split[1])
        self.show_message("The temperature is %.1f" %temperature)
        self.show_message("The humidity is %.1f" %humidity)
        print(data_string)

    def disconnect(self):
        self.server_sock.close()
        self.client_sock.close()

    def execute(self):
        self.advertise_and_connect()
        self.display_data()
        self.disconnect()
        

