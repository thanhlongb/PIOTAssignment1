from sense_hat import SenseHat
import bluetooth


class RFCOMMReceiver:
    """
    A RFCOMM protocol bluetooth server which broadcasts its
    services for the clients to connect. The server receives
    the data sent from the clients then display it on the
    sense hat LED matrix.

    Constants:
        -   UUID: uuid hex number to define the unique service
            used between servers and client.
        -   PORT: default port for the device to listen.
        -   SCROLL_SPEED: Speed of the text being displayed
            on the LED matrix.
        -   TEXT_COLOUR: Color the text being displayed
            on the LED matrix.
    """
    UUID = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848"
    PORT = 1
    SCROLL_SPEED = 0.05
    TEXT_COLOUR = [100, 100, 100]

    def __init__(self):
        """
        Initialize server

        Properties:
            -   client_sock: rfcomm client socket object
            -   server_sock: rfcomm server socket object
            -   sense: sense_hat object
        """
        self.client_sock = None
        self.server_sock = None
        self.sense = SenseHat()

    def advertise_and_connect(self):
        """
        Server ddvertises the service to nearby devices with
        specific uuid. If the client got the same uuid, they
        will automatically connect.
        """
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", self.PORT))
        self.server_sock.listen(1)
        bluetooth.advertise_service(
            self.server_sock,
            "Sensor Service",
            self.UUID
        )
        self.client_sock, client_address = self.server_sock.accept()

    def show_message(self, message):
        """
        Display message on the pi's sense hat.

        Inputs:
            -   message: a message string to display.
        """
        self.sense.show_message(
            message,
            scroll_speed=self.SCROLL_SPEED,
            text_colour=self.TEXT_COLOUR
        )

    def display_data(self):
        """
        Display temperature and humidity on the sense hat.
        """
        data = self.client_sock.recv(1024)
        data_string = data.decode('utf-8')
        data_split = data_string.split(",")
        temperature = int(data_split[0])
        humidity = int(data_split[1])
        self.show_message("The temperature is %d" % (temperature))
        self.show_message("The humidity is %d" % (humidity))

    def disconnect(self):
        """
        Close both the client and server sockets after
        finishing data transfer.
        """
        self.server_sock.close()
        self.client_sock.close()

    def execute(self):
        """
        Main flow of the program.
        """
        self.advertise_and_connect()
        self.display_data()
        self.disconnect()
