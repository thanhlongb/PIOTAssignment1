import sqlite3
from time import time

class Database:
    """
    A Database class with the following operations:
        -   Create necesarry tables for the system.
        -   Add records to the database
        -   Fetch records from the database
        -   Update records in the database

        Constants:
            -   DATABASE_FILE_PATH: path to the system's SQLite database.

        Variables:
            -   connection: connection to the system's database
            -   cursor: cursor of the connection of the system's database
    """    
    DATBASE_FILE_PATH = 'database.db'

    connection = None
    cursor = None

    def __init__(self):
        self.setup()
        self.create_necessary_tables()

    def __del__(self):
        self.cleanup()

    def setup(self):
        '''
        Establish connection with the database
        '''
        self.connection = sqlite3.connect(self.DATBASE_FILE_PATH)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
    
    def cleanup(self):
        '''
        Close database connection when this object is destroyed
        '''
        self.connection.close()

    def create_necessary_tables(self):
        '''
        Create necessary table for the system
        '''
        self.create_sensor_data_table()
        self.create_notification_table()
        self.create_report_table()

    def create_sensor_data_table(self):
        '''
        Create SensorData table for the system
        '''
        query = '''CREATE TABLE IF NOT EXISTS SensorData(
                    time TIMESTAMP, 
                    humidity INT, 
                    temperature INT
                )''' 
        self.cursor.execute(query)
        self.connection.commit()        

    def create_notification_table(self):
        '''
        Create Notification table for the system
        '''
        query = '''CREATE TABLE IF NOT EXISTS Notification(
                    time TIMESTAMP, 
                    pushbullet_id VARCHAR(255)
                )''' 
        self.cursor.execute(query)
        self.connection.commit()        

    def create_report_table(self):
        '''
        Create Report table for the system
        '''
        query = '''CREATE TABLE IF NOT EXISTS Report(
                    time TIMESTAMP,
                    date VAR_CHAR(10), 
                    status VARCHAR(255)
                )''' 
        self.cursor.execute(query)
        self.connection.commit()        

    def add_sensor_data_record(self, humidity, temperature):
        '''
        Add sensor data record to the SensorData table
        '''
        query = '''INSERT INTO SensorData VALUES (?,?,?)'''
        try:
            self.cursor.execute(query, (round(time()), humidity, temperature))
            self.connection.commit()
            return True
        except:
            return False

    def add_notification_record(self, pushbullet_id):
        '''
        Add notification record to the Notification table
        '''
        query = '''INSERT INTO Notification VALUES (?,?)'''
        try:    
            self.cursor.execute(query, (round(time()), pushbullet_id))
            self.connection.commit()
            return True
        except:
            return False

    def add_report_record(self, date, status):
        '''
        Add report record to the Report table
        '''
        query = '''INSERT INTO Report VALUES (?,?,?)'''
        try:
            self.cursor.execute(query, (round(time()),date, status))
            self.connection.commit()
            return True
        except:
            return False

    def fetch_latest_sensor_data_record(self):
        '''
        Fetch the newest sensor data record from the SensorData table
        '''
        query = '''SELECT * 
                    FROM SensorData 
                    ORDER BY time DESC LIMIT 1'''
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def fetch_sensor_data_grouped_by_date(self):
        '''
        Fetch sensor data record grouped by date from the SensorData table
        '''
        query = '''SELECT strftime('%m/%d/%Y',
                                    time,
                                    'unixepoch',
                                    'localtime') AS ftime, 
                          MAX(temperature) AS max_temp,
                          MIN(temperature) AS min_temp
                    FROM SensorData 
                    GROUP BY ftime
                    ORDER BY time ASC'''                          
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_latest_notification_record(self):
        '''
        Fetch newest notification record from the Notification table
        '''
        query = '''SELECT * 
                   FROM Notification 
                   ORDER BY time DESC LIMIT 1'''
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def fetch_all_report_records(self):
        '''
        Fetch all report record from the Report table
        '''
        query = '''SELECT * 
                   FROM Report 
                   ORDER BY date ASC'''
        self.cursor.execute(query)
        return self.cursor.fetchall()
            
    def update_sensor_data_status(self, time, humidity, temperature):
        '''
        Update sensor data record in the SensorData table
        '''
        query = '''UPDATE SensorData
                   SET humidity = ?, 
                       temperature = ?
                   WHERE time = ?'''
        self.cursor.execute(query, (humidity, temperature, time))
        self.connection.commit()
        return self.cursor.rowcount > 0
