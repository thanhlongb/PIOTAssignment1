import os
from time import sleep
from .pattern import Pattern
from sense_hat import SenseHat

class EmojiLibrary:
    EMOJI_LIBRARY_PATH = 'library/emoji'
    EMOJI_FILE_EXTENSION = '.emo'

    SENSE_HAT_LED_BLINK_PERIOD = 3 # seconds
    
    emoji_library = list()  

    def __init__(self):
        self.scan()
        
    def scan(self):
        for file in os.listdir(self.EMOJI_LIBRARY_PATH):
            if file.endswith(self.EMOJI_FILE_EXTENSION):
                self.add(os.path.join(self.EMOJI_LIBRARY_PATH, file))

    def add(self, file):
        self.emoji_library.append(Pattern(file))

    def display_all(self, sense, period = SENSE_HAT_LED_BLINK_PERIOD):
        for emoji in self.emoji_library:
            self.display(sense, emoji)
            sleep(period)
        self.display_all(sense) # for infiite loop

    def display(self, sense, emoji):
        sense.set_pixels(emoji.pixels)
