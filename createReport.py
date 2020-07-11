from utilities.database import Database
import os, json

class ReportCreator():
    TEMPERATURE_CONFIG_FILE_PATH = 'config.json'
    REPORT_FILE_PATH = 'report.csv'

    config = dict()

    def __init__(self):
        self.database = Database()
        self.load_config()

    def load_config(self):
        with open(self.TEMPERATURE_CONFIG_FILE_PATH, 'r') as file:
            self.config = json.load(file)

    def run(self):
        if (os.path.isfile(self.REPORT_FILE_PATH)):
            print("'{}' is already exist!".format(self.REPORT_FILE_PATH))
            report_file = self.prompt_report_file_name()
        else:
            report_file = self.REPORT_FILE_PATH
        self.write_to_file(report_file, self.construct_report_columns())
        for record in self.database.fetch_sensor_data_grouped_by_date():
            date_report = self.construct_date_report(record)
            print("{},{}".format(*date_report))
            self.database.add_report_record(*date_report)
            self.write_to_file(report_file, "{},{}".format(*date_report))
        print("Report file ({}) generated.".format(report_file))

    def prompt_report_file_name(self):
        while True:
            file_name = input("Enter name for your report file: ")
            if (os.path.isfile(file_name)):
                print("'{}' is already exist!".format(file_name))
            else:
                break
        return file_name

    def construct_report_columns(self):
        return "Date,Status"

    def write_to_file(self, file, content):
        with open(file, 'a') as report_file:
            report_file.write('{}\n'.format(content))

    def construct_date_report(self, record):
        # status = 'BAD: {} *C {} the comfort temperature'
        # if (record['max_temp'] > self.config['comfortable_max']):
        #     diff = record['max_temp'] - self.config['comfortable_max']
        #     status = status.format(diff, 'above')
        # elif (record['min_temp'] < self.config['comfortable_min']):
        #     diff =  self.config['comfortable_min'] - record['min_temp']
        #     status = status.format(diff, 'below')
        # else:
        #     status = 'OK'
        # return (record['ftime'], status)
        status = 'BAD: {} the comfort temperature'
        diffs = list()
        if (record['min_temp'] < self.config['comfortable_min']):
            diff = self.config['comfortable_min'] - record['min_temp']
            diffs.append('{}*C below'.format(diff))
        if (record['max_temp'] > self.config['comfortable_max']):
            diff = record['max_temp'] - self.config['comfortable_max']
            diffs.append('{}*C above'.format(diff))
        if len(diffs) == 0:
            status = 'OK'
        else:
            status = status.format(' and '.join(diffs))
        return (record['ftime'], status)

if __name__ == '__main__':
    rc = ReportCreator()
    rc.run()


