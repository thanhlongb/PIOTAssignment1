from library.emojiLibrary import EmojiLibrary
from sense_hat import SenseHat


if __name__ == '__main__':    
    sense = SenseHat()
    emoji_library = EmojiLibrary()
    emoji_library.display_all(sense)
