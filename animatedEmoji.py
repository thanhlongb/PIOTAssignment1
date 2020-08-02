from library.emojiLibrary import EmojiLibrary
from sense_hat import SenseHat


if __name__ == '__main__':
    """
    This script loop through all the emojis one by one and display them
    on sensehat LED matrix with a 3 seconds period each. 
    """
    sense = SenseHat()
    emoji_library = EmojiLibrary()
    emoji_library.display_all(sense)
