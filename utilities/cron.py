import os
from crontab import CronTab


class CronJob():
    """
    A class which set the cron job if not 
    exist in the crontab

    Constants:
        -   ABSOLUTE_PATH_TO_DIR: absolute path to the current directory
        -   CHANGE_DIR_COMMAND: command to change directory to ABSOLUTE_PATH_TO_DIR
    """
    ABSOLUTE_PATH_TO_DIR = os.path.dirname(os.path.realpath(__file__))
    CHANGE_DIR_COMMAND = 'cd ' + ABSOLUTE_PATH_TO_DIR

    def __init__(self, command):
        """
        Initialization.

        Properties:
            -   command: command that will be set in the cron job
        """
        self.command = self.CHANGE_DIR_COMMAND + command
    
    def set_job(self):
        """
        Set the command in the crontab if it does not exist.
        """
        cron = CronTab(user='pi')
        cron_command_found = cron.find_command(self.command)
        if len(list(cron_command_found)) == 0:
            job = cron.new(command=self.command)
            job.minute.every(1)
            cron.write()
