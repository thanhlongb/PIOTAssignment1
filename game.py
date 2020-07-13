from library.diceLibrary import DiceLibrary
from time import sleep
from sense_hat import SenseHat

class DieRollingGame():
    SCROLL_SPEED = 0.05
    TEXT_COLOUR = [100,100,100]

    def __init__(self):
        self.players_score = [0,0]
        self.dice_library = DiceLibrary()
        self.player_turn = 0
        self.sense = SenseHat()

    def show_message(self, message):
        self.sense.show_message(message, scroll_speed=self.SCROLL_SPEED, text_colour=self.TEXT_COLOUR)

    def show_instruction(self):
        self.show_message("Welcome to Electronic Die Game")
        self.show_message("Each player takes turn to roll the dice. First one to reach above 30 points wins the game.")
        
    def show_player_turn(self):
        if self.player_turn == 0:
            self.show_message("Player 1 turn!")
        else :
            self.show_message("Player 2 turn!")

    def detect_rolling_motion(self):
        x, y, z = self.sense.get_accelerometer_raw().values()
        x = abs(x)
        y = abs(y)
        z = abs(z)

        if x > 1.6 or y > 1.6 or z > 1.6:
            return True
        else: 
            return False

    def calculate_and_show_score(self, delta_score):
        self.players_score[self.player_turn] += delta_score
        self.show_message("Player %d score is %d" %(self.player_turn + 1, self.players_score[self.player_turn]))

    def check_winner(self):
        if self.players_score[self.player_turn] > 30:
            return self.player_turn
        else:
            return -1

    def change_player_turn(self):
        if self.player_turn == 0:
            self.player_turn = 1
        else:
            self.player_turn = 0

    def declare_winner(self):
        self.show_message("Congratulations! Player %d is the winner !" %(self.player_turn + 1))
        self.show_message("Game over!")

    def print_report(self):
        
        pass

    def run(self):
        self.show_instruction()
        while self.player_turn != -1:
            self.show_player_turn()
            while True:
                if self.detect_rolling_motion():
                    self.dice_library.display_dice_rolling_animation(self.sense)
                    break
            die_rolled = self.dice_library.display_random(self.sense, 0.8)
            self.calculate_and_show_score(die_rolled)
            if self.check_winner() != -1:
                self.declare_winner()
                # self.print_report()
                self.player_turn = -1
            else:
                self.change_player_turn()
                
if __name__ == "__main__":
    die_game = DieRollingGame()
    die_game.run()
