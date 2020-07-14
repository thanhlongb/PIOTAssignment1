from library.diceLibrary import DiceLibrary
from time import sleep
from sense_hat import SenseHat

class electronicDie():
    SCROLL_SPEED = 0.05
    TEXT_COLOUR = [100,100,100]
    SHAKING_THRESHOLD_DETECTION = 1.8

    def __init__(self):
        self.sense = SenseHat()
        self.dice_library = DiceLibrary()

    def show_message(self, message):
        self.sense.show_message(message, scroll_speed=self.SCROLL_SPEED, text_colour=self.TEXT_COLOUR)

    def roll_die(self):
        while True:
            if self.detect_rolling_motion():
                self.dice_library.display_dice_rolling_animation(self.sense)
                break
        return self.dice_library.display_random(self.sense, 1.5)

    def detect_rolling_motion(self):
        x, y, z = self.sense.get_accelerometer_raw().values()
        x = abs(x)
        y = abs(y)
        z = abs(z)

        if x > self.SHAKING_THRESHOLD_DETECTION or y > self.SHAKING_THRESHOLD_DETECTION or z > self.SHAKING_THRESHOLD_DETECTION:
            return True
        else: 
            return False

    def run(self):
        while True:
            self.show_message("Please roll your dice")
            die_num_rolled = self.roll_die()
            self.show_message("The die number is %d " %(die_num_rolled))
        pass

if __name__ == "__main__":
    electronic_die = electronicDie()
    electronic_die.run()

