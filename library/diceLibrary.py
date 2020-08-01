import os
import random
from time import sleep
from .pattern import Pattern


class DiceLibrary:
    """
    A Die class with the following operations:
        -   Find the absolute path to each .die file in folder dice
            which contains the 8x8 configuration for the color of die
            numbers from 1 - 6.
        -   Read the color configurations from .die file and store.
        -   Display a die number on the LED matrix.
        -   Display a random die number on the LED matrix.
        -   Display die rolling animation.

        Constants:
            -   DICE_LIBRARY_PATH: relative path extension to folder dice.
            -   DICE_FILE_EXTENSION: type of die color config file extension
                is .die.
            -   ANIMATION_PERIOD: The period of time program stopped
                between 2 consecutive die numbers being shown
                on the LED matrix for dice rolling animation.
            -   PERIOD_GROWTH_FACTOR: The decaying factor of the
                ANIMATION_PERIOD.
    """
    DICE_LIBRARY_PATH = 'library/dice'
    DICE_FILE_EXTENSION = '.die'
    ANIMATION_PERIOD = 0.2
    PERIOD_GROWTH_FACTOR = 1.2

    dice_library = list()

    def __init__(self):
        self.scan()

    def scan(self):
        """
        Find the absolute path with ending relative path to 6 .die color
        config files and read those configurations to the list dice_library.
        """
        file_list = os.listdir(self.DICE_LIBRARY_PATH)
        for i in range(1, 7):
            for file in file_list:
                if file.endswith(str(i) + self.DICE_FILE_EXTENSION):
                    self.add(os.path.join(self.DICE_LIBRARY_PATH, file))

    def add(self, file):
        """
        Add the 6 die color configs to dice_library list.

        Inputs:
            -   file: path to the .die file
        """
        self.dice_library.append(Pattern(file))

    def display(self, sense, die):
        """
        Display a die number on the LED matrix of the raspberry pi sense hat.

        Inputs:
            -   sense: the Sense Hat object
            -   die: list containing 8x8 LED matrix color config
        """
        sense.set_pixels(die.pixels)

    def display_random(self, sense, period):
        """
        Display a random die number on the LED matrix of
        the raspberry pi sense hat.

        Inputs:
            -   sense: sense_hat object
            -   period: period of time to halt between 2 die numbers
                being displayed.

        Returns:
            -   The die number that we have randomly chosen.
        """
        die_num = random.randint(0, 5)
        self.display(sense, self.dice_library[die_num])
        sleep(period)
        return die_num + 1

    def display_dice_rolling_animation(self, sense,
                                       period=ANIMATION_PERIOD,
                                       period_growth=PERIOD_GROWTH_FACTOR):
        """
        Display die rolling animation on the LED matrix
        by displaying randomly die numbers with decreasing
        speed. The last die number shown will be the score.

        Inputs:
            -   sense: sense_hat object
            -   period: The period of time program stopped
                between 2 consecutive die numbers being shown
                on the LED matrix. This time period will be fast
                at the beginning and slowly decays to make
                the animation looks real.
            -   period_growth: The decaying factor of period.
        """
        while period < 1:
            self.display_random(sense, period)
            period *= period_growth
