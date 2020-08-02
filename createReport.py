import os
import json
from utilities.database import Database


class ReportCreator():
    """
    A ReportCreator class will generate a .csv format report of daily
    temperature fetched from the database.

        Constants:
            -   TEMPERATURE_CONFIG_FILE_PATH: Path to the temperature
                configuration file.
            -   REPORT_FILE_PATH: Default path to the report file.
    """
    TEMPERATURE_CONFIG_FILE_PATH = 'config.json'
    REPORT_FILE_PATH = 'report.csv'

    config = dict()

    def __init__(self):
        """
        Initialize the report creator.

        Properties:
            -   database: Database object.
        """
        self.database = Database()
        self.load_config()

    def load_config(self):
        """
        Load the humidity and temperature configurations.
        """
        with open(self.TEMPERATURE_CONFIG_FILE_PATH, 'r') as file:
            self.config = json.load(file)

    def run(self):
        """
        Main flow of the class.
        """
        report_file = self.get_report_file_name()
        self.export_records_to_file(report_file)
        print("Report file ({}) generated.".format(report_file))

    def get_report_file_name(self):
        """
        Get the .csv report file name.
        """
        if os.path.isfile(self.REPORT_FILE_PATH):
            print("'{}' is already exist!".format(self.REPORT_FILE_PATH))
            report_file = self.prompt_report_file_name()
        else:
            report_file = self.REPORT_FILE_PATH
        return report_file

    def prompt_report_file_name(self):
        """
        Promt the report file name until it's not duplicate with an
        exist file name.
        """
        while True:
            report_file = input("Enter name for your report file: ")
            if os.path.isfile(report_file):
                print("'{}' is already exist!".format(report_file))
            else:
                break
        return report_file

    def export_records_to_file(self, report_file):
        """
        Export the report to report file.

        Input:
            -   report_file: path to report file.
        """
        self.write_to_file(report_file, self.construct_report_columns())
        for record in self.database.fetch_sensor_data_grouped_by_date():
            date_report = self.construct_date_report(record)
            print("{},{}".format(*date_report))
            self.database.add_report_record(*date_report)
            self.write_to_file(report_file, "{},{}".format(*date_report))

    def construct_report_columns(self):
        """
        Return .csv report file header.
        """
        return "Date,Status"

    def write_to_file(self, file, content):
        """
        Write content to file.

        Inputs:
            -   file: path to file to be written to.
            -   content: content to be written to file.
        """
        with open(file, 'a') as report_file:
            report_file.write('{}\n'.format(content))

    def construct_date_report(self, record):
        """
        Construct the date report from the sensor data.

        Input:
            -   record: sensor data.
        """
        status = 'BAD: {} the comfort temperature'
        diffs = list()
        if record['min_temp'] < self.config['temperature']['comfortable_min']:
            diff = self.config['temperature']['comfortable_min'] - record['min_temp']
            diffs.append('{}*C below'.format(diff))
        if record['max_temp'] > self.config['temperature']['comfortable_max']:
            diff = record['max_temp'] - self.config['temperature']['comfortable_max']
            diffs.append('{}*C above'.format(diff))
        if len(diffs) == 0:
            status = 'OK'
        else:
            status = status.format(' and '.join(diffs))
        return (record['ftime'], status)


if __name__ == '__main__':
    RC = ReportCreator()
    RC.run()
