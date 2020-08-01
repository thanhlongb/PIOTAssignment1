from library.diceLibrary import DiceLibrary
from sense_hat import SenseHat


class ElectronicDie():
    """
    An electronic die which displays the die rolling animation
    on the sense hat LED matrix triggered by the sense hat being
    shaken.

    Constants:
        -   SCROLL_SPEED: Speed of the text being displayed
            on the LED matrix.
        -   TEXT_COLOUR: Color the text being displayed
            on the LED matrix.
        -   THRESHOLD: threshold value to detect shaking motion.
    """
    SCROLL_SPEED = 0.05
    TEXT_COLOUR = [100, 100, 100]
    THRESHOLD = 1.8

    def __init__(self):
        """
        Initialize the electronic die.

        Properties:
            -   sense: sense_hat object.
            -   dice_library: DiceLibrary object.
        """
        self.sense = SenseHat()
        self.dice_library = DiceLibrary()

    def show_message(self, message):
        """
        Display message on the pi's sense hat.

        Inputs:
            -   message: a message string to display.
        """
        self.sense.show_message(
            message,
            scroll_speed=self.SCROLL_SPEED,
            text_colour=self.TEXT_COLOUR
        )

    def roll_die(self):
        """
        Simulate the die rolling animation triggered by the
        sense hat being shaken.

        Returns:
            -   The last number being displayed on the sense hat
                LED matrix at the end of the animation, which
                is also the resulting die number being rolled.
        """
        while True:
            if self.detect_rolling_motion():
                self.dice_library.display_dice_rolling_animation(self.sense)
                break
        return self.dice_library.display_random(self.sense, 1.5)

    def detect_rolling_motion(self):
        """
        Detect the shaking motion by reading the values
        from accelerometer sensors and check them against
        the predefined threshold.

        Returns:
            - true:   If the x, y, z absolute values of accelerometer
                      sensors are larger than predefined threshold.
            - false:  Otherwise.
        """
        x_axis, y_axis, z_axis = self.sense.get_accelerometer_raw().values()
        x_abs = abs(x_axis)
        y_abs = abs(y_axis)
        z_abs = abs(z_axis)
        return x_abs > self.THRESHOLD \
            or y_abs > self.THRESHOLD \
            or z_abs > self.THRESHOLD

    def run(self):
        """
        Main flow program.
        """
        while True:
            self.show_message("Please roll your dice")
            die_num_rolled = self.roll_die()
            self.show_message("The die number is %d " % (die_num_rolled))


if __name__ == "__main__":
    ELECTRONIC_DIE = ElectronicDie()
    ELECTRONIC_DIE.run()
