import os
from time import sleep
from .pattern import Pattern


class EmojiLibrary:
    """
    A Emoji class with the following operations:
        -   Find the absolute path to each .emo file in folder emoji
            which contains the 8x8 configuration for the emojis.
        -   Read the color configurations from .emo file and store.
        -   Display emoji on the LED matrix.

        Constants:
            -   EMOJI_LIBRARY_PATH: relative path extension to folder emoji.
            -   EMOJI_FILE_EXTENSION: type of emoji config file extension
                is .emo.
            -   SENSE_HAT_LED_BLINK_PERIOD: The period of time program stopped
                between 2 consecutive emoji being shown
                on the LED matrix.
    """

    EMOJI_LIBRARY_PATH = 'library/emoji'
    EMOJI_FILE_EXTENSION = '.emo'

    SENSE_HAT_LED_BLINK_PERIOD = 3  # seconds

    emoji_library = list()

    def __init__(self):
        self.scan()

    def scan(self):
        """
        Find the absolute path with ending relative path to emoji
        config files and read those configurations to the list emoji_library.
        """
        for file in os.listdir(self.EMOJI_LIBRARY_PATH):
            if file.endswith(self.EMOJI_FILE_EXTENSION):
                self.add(os.path.join(self.EMOJI_LIBRARY_PATH, file))

    def add(self, file):
        """
        Add the emoji configs to emoji_library list.

        Inputs:
            -   file: path to the .emo file
        """
        self.emoji_library.append(Pattern(file))

    def display_all(self, sense, period=SENSE_HAT_LED_BLINK_PERIOD):
        """
        Display emoji from the emoji_library on the LED matrix
        of the sense hat one by one.

        Inputs:
            -   sense: the Sense Hat object
            -   period: time between each emoji display
        """
        for emoji in self.emoji_library:
            self.display(sense, emoji)
            sleep(period)
        self.display_all(sense)  # for infiite loop

    def display(self, sense, emoji):
        """
        Display a emoji on the LED matrix of the raspberry pi sense hat.

        Inputs:
            -   sense: the Sense Hat object
            -   emoji: list containing 8x8 LED matrix color config
        """
        sense.set_pixels(emoji.pixels)
