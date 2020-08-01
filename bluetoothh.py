import sys
import bluetooth
from utilities.rfcommReceiver import RFCOMMReceiver
from utilities.rfcommSender import RFCOMMSender


class Bluetooth():
    """
    Main class to run the data sending application via bluetooth.
    """
    def __init__(self):
        """
        Initialize the class.

        Properties:
            -   device: to determine if this application
                is a data receiver (uses RFCOMMReceiver class)
                or a data sender (uses RFCOMMSender class) by
                reading the 1st command line argument.
        """
        self.device = None
        if str(sys.argv[1]) == 'Sender':
            try:
                self.device = RFCOMMSender()
            except bluetooth.BluetoothError as err:
                print(err)
                sys.exit(0)
        else:
            try:
                self.device = RFCOMMReceiver()
            except bluetooth.BluetoothError as err:
                print(err)
                sys.exit(0)

    def run(self):
        """
        Call the main flow program of RFCOMMReceiver or RFCOMMSender
        """
        self.device.execute()


if __name__ == "__main__":
    BLUETOOTH = Bluetooth()
    BLUETOOTH.run()
