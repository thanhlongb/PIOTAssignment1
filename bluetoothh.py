import bluetooth
import sys
from utilities.rfcommReceiver import RFCOMMReceiver
from utilities.rfcommSender import RFCOMMSender

class Bluetooth():
    def __init__(self):
        self.object = None
        if str(sys.argv[1]) == 'Sender':
            try:
                self.object = RFCOMMSender()
            except bluetooth.BluetoothError as err:
                print(err)
                sys.exit(0)
        else:
            try:
                self.object = RFCOMMReceiver()
            except bluetooth.BluetoothError as err:
                print(err)
                sys.exit(0)

    def run(self):
        self.object.execute()

if __name__ == "__main__":
    bluetooth = Bluetooth()
    bluetooth.run()