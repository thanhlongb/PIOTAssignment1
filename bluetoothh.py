import sys
import bluetooth
from utilities.rfcommReceiver import RFCOMMReceiver
from utilities.rfcommSender import RFCOMMSender
from utilities.cron import CronJob


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
            -   device_name: 'Sender' if self.device is
                RFCOMMSender's instance, 'Receiver' if
                self.device is RFCOMMReceiver's instance.
        """
        self.device = None
        self.device_name = None
        if str(sys.argv[1]) == 'Sender':
            try:
                self.device = RFCOMMSender()
                self.device_name = 'Sender'
            except bluetooth.BluetoothError as err:
                print(err)
                sys.exit(0)
        else:
            try:
                self.device = RFCOMMReceiver()
                self.device_name = 'Receiver'
            except bluetooth.BluetoothError as err:
                print(err)
                sys.exit(0)

    def set_cron_job(self):
        """
        Set the cron job if the job does not
        exist in the crontab.
        """
        bluetooth_on_command = ' && sudo hciconfig hci0 piscan'
        run_command = ' && python3 bluetoothh.py ' + self.device_name
        command = bluetooth_on_command + run_command
        cron = CronJob(command)
        cron.set_job('taskC')

    def run(self):
        """
        Call the main flow program of RFCOMMReceiver or RFCOMMSender
        """
        self.set_cron_job()
        self.device.execute()


if __name__ == "__main__":
    BLUETOOTH = Bluetooth()
    BLUETOOTH.run()
