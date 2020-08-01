import sys
import bluetooth
from utilities.rfcommReceiver import RFCOMMReceiver
from utilities.rfcommSender import RFCOMMSender
from crontab import CronTab


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
        cron = CronTab(user='pi')
        cron_command = 'sudo hciconfig hci0 piscan \
                        && python3 /home/pi/Desktop/PIOTAssignment1/bluetoothh.py ' \
                        + self.device_name
        cron_command_found = cron.find_command(cron_command)
        if len(list(cron_command_found)) == 0:
            job = cron.new(command=cron_command)
            job.minute.every(1)
            cron.write()

    def run(self):
        """
        Call the main flow program of RFCOMMReceiver or RFCOMMSender
        """
        self.set_cron_job()
        self.device.execute()


if __name__ == "main":
    BLUETOOTH = Bluetooth()
    BLUETOOTH.run()
