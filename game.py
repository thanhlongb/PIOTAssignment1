import csv
import os
from datetime import datetime
from electronicDie import ElectronicDie
from sense_hat import SenseHat


class DieRollingGame():
    """
    Die rolling game simulation class.

    Constants:
        -   SCROLL_SPEED: Speed of the text being displayed
            on the LED matrix.
        -   TEXT_COLOUR: Color the text being displayed
            on the LED matrix.
    """
    SCROLL_SPEED = 0.05
    TEXT_COLOUR = [100, 100, 100]

    def __init__(self):
        """
        Initialization.

        Properties:
            -   players_score: a list containing the scores of 2 players.
            -   player_turn: turn of player 1 or 2.
            -   sense: sense_hat object.
            -   electronic_die: ElectronicDie object.
        """
        self.players_score = [0, 0]
        self.player_turn = 0
        self.sense = SenseHat()
        self.electronic_die = ElectronicDie()

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

    def show_instruction(self):
        """
        Show the instructions at the start of the game
        on the sense hat LED matrix.
        """
        self.show_message("Welcome to Electronic Die Game")
        self.show_message("First one to reach above 30 points wins the game.")

    def show_player_turn(self):
        """
        Show message on sense hat LED matrix indicating
        the current player turn.
        """
        if self.player_turn == 0:
            self.show_message("Player 1 turn!")
        else:
            self.show_message("Player 2 turn!")

    def calculate_and_show_score(self, delta_score):
        """
        Show the points gained by the current player rolling the
        die. Add those points to that player's total points.
        """
        self.players_score[self.player_turn] += delta_score
        self.show_message(
            "Player %d score is %d"
            % (self.player_turn + 1, self.players_score[self.player_turn])
        )

    def check_winner(self):
        """
        Check if the current player is the winner
        (total points >= 30).

        Returns:
            -   self.player_turn: if the total points
                of self.player_turn >= 30.
            -   -1: otherwise.
        """
        if self.players_score[self.player_turn] >= 30:
            return self.player_turn
        return -1

    def change_player_turn(self):
        """
        Change the turn to the next player.
        """
        if self.player_turn == 0:
            self.player_turn = 1
        else:
            self.player_turn = 0

    def declare_winner(self):
        """
        Declare the winner by displaying message on
        the sense hat LED matrix.
        """
        self.show_message(
            "Congratulations! Player %d is the winner !"
            % (self.player_turn + 1)
        )
        self.show_message("Game over!")

    def print_report(self):
        """
        Print the record (including time and winner score)
        to the winner.csv file.
        """
        now = datetime.now()
        filename = "winner.csv"
        flag = True
        if os.path.isfile('./' + filename):
            flag = False

        with open(filename, 'a') as filedata:
            writer = csv.writer(filedata, delimiter=',')
            if flag:
                writer.writerow(['time', 'winner_score'])
            writer.writerow([now, self.players_score[self.player_turn]])

    def run(self):
        """
        Main flow program.
        """
        self.show_instruction()
        while self.player_turn != -1:
            self.show_player_turn()
            die_num_rolled = self.electronic_die.roll_die()
            self.calculate_and_show_score(die_num_rolled)
            if self.check_winner() != -1:
                self.declare_winner()
                self.print_report()
                self.player_turn = -1
            else:
                self.change_player_turn()


if __name__ == "__main__":
    DIE_ROLLING_GAME = DieRollingGame()
    DIE_ROLLING_GAME.run()
