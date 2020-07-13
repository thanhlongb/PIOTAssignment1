import os
import random
from time import sleep
from pattern import Pattern
from sense_hat import SenseHat

class DiceLibrary:
    DICE_LIBRARY_PATH = 'library/dice'
    DICE_FILE_EXTENSION = '.die'
    ANIMATION_PERIOD = 0.6
    PERIOD_GROWTH_FACTOR = 1.1

    dice_library = list()  

    def __init__(self):
        self.scan()
        
    def scan(self):
        for file in os.listdir(self.DICE_LIBRARY_PATH):
            if file.endswith(self.DICE_FILE_EXTENSION):
                self.add(os.path.join(self.DICE_LIBRARY_PATH, file))

    def add(self, file):
        self.dice_library.append(Pattern(file))

    def display(self, sense, die):
        sense.set_pixels(die.pixels)

    def display_random(self, sense):
        dieNum = random.randint(0,5)
        self.display(sense, self.dice_library[dieNum]) 
        return dieNum + 1      

    def display_dice_rolling_animation(self, sense, period = ANIMATION_PERIOD, period_growth = PERIOD_GROWTH_FACTOR):
        while period < 1:
            self.display_random(sense)
            sleep(period)
            period *= period_growth

 
