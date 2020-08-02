
# Assignment 1 IoT



RMIT University Vietnam Course: COSC2790 Programming Internet of Things 

Semester: 2020B 

Assessment: Assignment1 

Team name: Group 14

Team members: Ngo Quang Trung (3742774), Bui Thanh Long (3748575)


## Introduction

This is a set of Python applications according to the specifications of COSC2790 - Programming IoT assignment 1: Python & Sense HAT programming.

## Main files and Features

1. Task A
    * **animatedEmoji.py** : A Python program which displays 3 faces (configured by the user) on the Sense Hat LED matrix with an interval of 3 seconds each. 
    
2. Task B
    * **config.json**: JSON file which allows the user to configure the following information for this task:
        * minimum comfortable temperature, humidity
        * maximum confortable temperature, humidity
    
    * **monitorAndNotify.py**: A Python application which will create and save a record including current time, temperature and humidity to the database (SQLite). If the temperature and humidity values are out of comfortable range (defined in the **config.json** file), a notification will be sent to other devices using **Pushbullet** with the maximum of 1 notification per day. After running for the first time, a job will be created and saved in the user's crontab so that this script will always be executed on boot.
    * **readAndDisplay.py**: A Python scripts which get the latest temperature record in the database and display it on the Sense Hat LED matrix with the following rule
        *   If the temperature is **cold** (< minimum comfortable temperature): display with **blue** color.
        *   If the temperature is **comfortable** (within the comfortable range): display with **green** color.
        *   If the temperature is **hot** (> maximum comfortable temperature): display the temperature with **red** color.
    * **createReport.py**: Create a file named 'report.csv' which shows all the records residing in the database. For each record, if the temperature is outside the comfortable temperature range then it will be labeled as **BAD** with an appropriate message stating the errors; otherwise,  it is labeled as **OK**. 
    * **apiRESTful.py**: Utilize Flask and Flask-RESTful to build RESTful APIs allowing user to interact with the database through different types of request including: GET, POST and PUT.
        *   **GET**: Get the latest temperature and humidity record with timestamp in JSON format.   
        *   **POST**: Upload a record to database with current timestamp.
        *   **PUT**: update the newest record in the database. 
    * **apiTestKit.pt**: provide tests to make sure those RESTful APIs built above are fully functional.

3. Task C
    * **config.json**: JSON file which allows the user to configure the following information for this task:
        * minimum temperature, humidity
        * maximum temperature, humidity
    * **bluetoothh.py**: Using Bluetooth to detect other Raspberry Pis. If the current temperature and humidity values got from the Sense Hat sensors are within the configured min/max range in **config.json**, the rPi will send appropriate messages to other Bluetooth-connected rPis stating the current temperature/humidity values. The other rPis receive the values and display them on their own Sense Hat LED matrix.
    
4. Task D
    * **electronicDie.py**: An electronic die which simualtes the die rolling animation using the Sense Hat LED matrix. When the user shakes the rPi, the accelerometer sensor's values will change accordingly which will then be captured and trigger the die rolling animation.
    * **game.py**: Uses **electronicDie.py** to make a game between 2 players. Each takes turn to roll the die, and the number being rolled will be count towards the total points of the according player. The first one to reach above 30 points will be the winner. A file named 'winner.csv' will be generated to record every won game including time and final points of the winner. 

## Installation

* Clone the project using terminal.

* Change current working directory to the project's directory.

* Use **```pip3 install -r requirements.txt```** command to install this project's dependencies.


### Compile and Run
    Run the according commands in the terminal for each specific task.
1. Task A
    * **```python3 animatedEmoji.py```**

2. Task B
    * Configure **config.json** file to set min/max comfortable temperature/humidity values. 
    * **```python3 monitorAndNotify.py```**
    * Create new terminal window, then **```python3 readAndDisplay.py```**
    * Create new terminal window, then **```python3 apiRESTful.py```**
    * Create new terminal window, then **```python3 apiTestKit.py```**
3. Task C
    * Requires 2 Raspberry Pis.
    * **```sudo hciconfig hci0 piscan && python3 bluetoothh.py Receiver```** on 1st rpi.
    * Configure **config.json** file to set min/max temperature/humidity values (on the 2nd pi). 
    * **```sudo hciconfig hci0 piscan && python3 bluetoothh.py Sender```** on 2nd rpi.

4. Task D
    * **```python3 electronicDie.py```** for **electronicDie.py**
    * **```python3 game.py```** for **game.py**
## Known bugs

All exceptions have been handled.

## Acknowledgement

* COSC2790 learning' materials

* https://pybluez.readthedocs.io/en/latest/?fbclid=IwAR0hQ40IOikDz8xjjoYhd8u4nn5j0uzf-RmfvMfZGm07GyHdFfDwEGzJJZk
