#! /usr/bin/python3
__author__ = 'Jeff Schreiner'

from random import SystemRandom
import sys

# Global Variables
r1 = SystemRandom()  # Our random number generator
board = []  # Holds the game board
ship_coord = []  # Ships' coordinates
num_ships = 0  # Number of ships set by user
board_size = 0  # Width and height of board, multiple of 5 * num_ships
num_turns = 0  # Number of turns, set by player to adjust difficulty
test_mode = False  # Flag for turning on automated game play for difficulty testing
debug_mode = False  # Flag for enabling the debug mode that shows ship locations
wins = 0  # Number of wins recorded for testing
losses = 0  # Number of losses recorded for testing
winning_turns = []  # An array of the last turn counter in a winning game for testing
test_num_ships = 4  # Default number of ships for testing
test_num_turns = 41  # Default number of turns for testing
test_num_rounds = 300  # Default number of games to play for testing


# Reset all variables after every game
# @param is_testing is False by default, if True will reset more global variables
def reset_vars(is_testing=False):
    global board, ship_coord, wins, losses, winning_turns, test_mode

    board = []
    ship_coord = []

    # Also reset win records if T is passed for test mode
    if is_testing:
        wins = 0
        losses = 0
        winning_turns = []
        test_mode = False


# Ask the user for the number of ships and turns
def ask_game_options():
    global num_ships, num_turns, board_size

    if test_mode:  # DEBUG suppresses asking while in test mode, we already have our variables set
        return

    print("Type Q to quit or H for help.")

    # Ask the user for the number of ships, more ships make a bigger board and generally longer game.
    is_input_valid = False
    while not is_input_valid:
        try:
            get_input = input("\nHow many ships do you want to play with? (4)") or 4
            num_ships = int(get_input)
            # Our valid inputs are between 1 and 7 ships
            if 1 <= num_ships <= 7:
                is_input_valid = True
            else:
                print("\nPlease enter a number between 1 and 7.")
        except ValueError:
            # The user can enable the automated test mode
            if get_input == "t3st":
                set_test_params()
                global test_mode
                test_mode = True
                return
            # The user can toggle debug mode
            elif get_input == "d3bug":
                set_debug_mode()
            # The user can quit by typing Q or Quit, case-insensitive
            elif get_input[:1] == "q" or get_input[:1] == "Q":
                quit_game()
            # The help screen
            elif get_input[:1] == "h" or get_input[:1] == "H":
                print_help()
            else:
                print("\nPlease enter a number.")

    # The default number of turns is equal to one-tenth the area of the board ( medium )
    default_turns = int(((num_ships * 5) ** 2) / 10) + 1
    # The max number of turns is equal to half area of the board ( easy ). Board size is 5 times the number of ships
    turns_limit = int(((num_ships * 5) ** 2) / 2) + 1

    # Ask the user how many turns they want, this sets difficulty, the default is medium
    is_input_valid = False
    while not is_input_valid:
        try:
            get_input = input(
                "\nHow many turns do you want? (%d) is medium." % default_turns) or default_turns
            num_turns = int(get_input)
            # Valid number of turns is between 1 and the upper limit, which is based on the number of ships
            if 1 <= num_turns <= turns_limit:
                is_input_valid = True
            else:
                print("\nPlease enter a number between 1 and %d." % turns_limit)
        except ValueError:
            # The user can toggle testing mid-game
            if get_input == "t3st":
                set_test_params()
                global test_mode
                test_mode = True
                return
            # The user can toggle debug mode mid-game
            elif get_input == "d3bug":
                set_debug_mode()
            # The user can quit or get help at this prompt also
            elif get_input[:1] == "q" or get_input[:1] == "Q":
                quit_game()
            elif get_input[:1] == "h" or get_input[:1] == "H":
                print_help()
            else:
                print("\nPlease enter a number.")


# Sets the ships randomly on the board, but only save them to an array
def make_board():
    global ship_coord, board_size

    # The board size is 5 times the number of ships
    board_size = num_ships * 5

    # Build an empty board of ocean waves in an array
    for y in range(board_size):
        board.append(["~"] * board_size)

    # For every ship that we need to create
    for z in range(num_ships):
        # Get a random coordinate to start
        ship_row = SystemRandom.randint(r1, 1, board_size)
        ship_col = SystemRandom.randint(r1, 1, board_size)

        # For every new ship, roll to see if it is longer than one coordinate, this determines ship length
        ship_length = SystemRandom.randint(r1, 0, 4)

        # If it is longer than one, then we roll to see what direction it will grow ( 1 through 4 )
        if ship_length:
            ship_orientation = SystemRandom.randint(r1, 1, 4)

            # These are ships that can be 2-5 coordinates long and stem in one of the four directions.
            # We also don't worry if they leave the board, it just makes a shorter ship.
            # We save each coordinate of the ship into the ship_coord array

            # Ship grows right
            if ship_orientation == 1:
                ship_coord.append([ship_row, ship_col])
                for i in range(1, ship_length):
                    ship_row += 1
                    ship_coord.append([ship_row, ship_col])

            # Ship grows down
            elif ship_orientation == 2:
                ship_coord.append([ship_row, ship_col])
                for i in range(1, ship_length):
                    ship_col += 1
                    ship_coord.append([ship_row, ship_col])

            # Ship grows left
            elif ship_orientation == 3:
                ship_coord.append([ship_row, ship_col])
                for i in range(1, ship_length):
                    ship_row -= 1
                    ship_coord.append([ship_row, ship_col])

            # Ship grows up
            elif ship_orientation == 4:
                ship_coord.append([ship_row, ship_col])
                for i in range(1, ship_length):
                    ship_col -= 1
                    ship_coord.append([ship_row, ship_col])

        # This is a single coordinate ship
        else:
            ship_coord.append([ship_row, ship_col])


# Print the Help Screen
def print_help():
    clear_screen()
    print("\nHelp:")
    print("\nGame Objects: ~ water; X miss; M ship")
    print("\nFor a quick game, the default values are in parenthesis. Just press enter to select defaults.")
    print("You can quit at anytime by typing Q or QUIT (not case-sensitive).")
    print("You can get to this help screen by typing H or HELP (not case-sensitive).")
    print("\nFor testing, you can automate thousands rounds of play by typing \"t3st\" at the prompt.")
    print("Also, you can print a map with ship locations by typing \"d3bug\" at the prompt.")


# Clear the screen and print the title
def clear_screen():
    if test_mode:  # DEBUG suppresses console output in test mode
        return
    for i in range(100):
        print("\n")
    print("Let's play Battleship!\n")


# Show board to user
# @param msg sets a message to display below the board
def print_board(msg=""):
    if test_mode:  # DEBUG suppresses console output in test mode
        return
    clear_screen()
    for row in board:
        print(" ".join(row))
    print()
    # There seems to be a bug when putting these on the same line, we get a leading space.
    print(msg, "\n")


# Print statistics after the game.
def print_stats():
    print("Wins: ", wins, "Losses: ", losses)

    avg = 0
    for w in winning_turns:
        avg += w
    if len(winning_turns) > 0:  # Suppress if there weren't any wins, prevents !DIV/0
        avg //= len(winning_turns)
        print("Average Winning Turn: ", avg)
    print()


# Quit the game
def quit_game():
    print("\nHave a nice day!")
    sys.exit(0)


# Plays one full game of Battleship
def play_one_round():
    global board, num_ships

    # Setup the game by asking the user some questions and printing the blank board
    clear_screen()
    ask_game_options()
    make_board()
    print_board()
    # Start with the total number of turns that the user chose
    turns_left = num_turns

    # Playing the game as long we have turns (shots) left.
    while turns_left > 0:
        if not test_mode:  # DEBUG suppresses console output in test mode
            if turns_left == 1:
                print("Turn ", num_turns - turns_left + 1, ", last turn!")
            else:
                print("Turn ", num_turns - turns_left + 1, " / ", num_turns)

            if debug_mode:  # DEBUG displays debugging info and cheat board in debug mode
                print_debug_info()

        if test_mode:  # DEBUG fake user input in testing mode.
            guess_row = SystemRandom.randint(r1, 1, board_size)
            guess_col = SystemRandom.randint(r1, 1, board_size)

        else:  # The user is playing the game
            # Get user's guess coordinates
            is_input_valid = False
            while not is_input_valid:
                try:
                    row_input = ""
                    col_input = ""

                    row_input = input("\nGuess Row: ")
                    # Make sure the user's guess is an integer
                    guess_row = int(row_input)

                    col_input = input("Guess Col: ")
                    # Make sure the user's guess is an integer
                    guess_col = int(col_input)

                    # User's guess is two integers, we can continue
                    is_input_valid = True

                # The user's input was not an integer, they may be trying to tell us something else
                except ValueError:
                    # The user can quit mid-game, by typing Q or Quit, case-insensitive
                    if row_input[:1] == "q" or row_input[:1] == "Q" or col_input[:1] == "q" or col_input[:1] == "Q":
                        quit_game()
                    # The user can toggle debug mode for the next turn.
                    elif row_input == "d3bug":
                        set_debug_mode()
                    else:
                        print("\nPlease enter a number.")

        # msg gets passed to the print_board function to tell the user what happened during the round.
        msg = ""

        # Check to see if the shot is within the board limits
        if (1 <= guess_row <= board_size) and (1 <= guess_col <= board_size):

            # Check the guess coordinates for a ship in the ship location array.
            for x in ship_coord:
                if x == [guess_row, guess_col]:
                    # A match was found, the user scored a direct hit, draw damaged boat
                    board[guess_row - 1][guess_col - 1] = "M"
                    msg = "Congratulations! You sunk my battleship!\n"
                    global winning_turns
                    # Add a win to the stats, and record what turn it was
                    winning_turns.append(num_turns - turns_left + 1)  # DEBUG
                    print_board(msg)
                    global wins
                    wins += 1
                    # Exit play_one_round and return to the main menu
                    return True

                # Check against previous misses by looking for X's on the board
                elif board[guess_row - 1][guess_col - 1] == "X":
                    msg = "You guessed that one already."
                    # Send them back to guess again
                    break

                # The shot missed and wasn't previously guessed
                msg = "You missed my battleship!"

            # Add an X to the board at the guess location to keep track of previous guesses
            board[guess_row - 1][guess_col - 1] = "X"

        # The shot wasn't inside the board limits
        else:
            msg = "Oops, that's not even in the ocean!"

        # Subtract a turn
        turns_left -= 1

        # Print the board and tell the user what happened with msg
        print_board(msg)

    # The user ran ouf of turns. Add a loss to stats and return to the main menu
    else:
        print_board("Game Over")
        global losses
        losses += 1
        return False


def main():
    # Entry point, this loops the game until user exits.
    while True:
        # Automated testing mode is enabled
        if test_mode:
            test_play()
            print_stats()
            reset_vars(True)

        # User is playing the game
        else:
            play_one_round()
            reset_vars(False)

            # This prevents the stats from printing when we begin test mode,
            # Because when testing mode is enabled, the round ends prematurely and finishes this if statement.
            # It will then loop from the while True to the testing mode branch of this if statement.
            if not test_mode:
                print_stats()

        # After each round of play or batch of testing, ask the user if they would like to play again or quit.
        if not test_mode:
            play_again = input("Play again? (Q to Quit or any key to Continue)") or "Y"
            if play_again[:1] == "q" or play_again[:1] == "Q":
                quit_game()


# region DEBUG Functions ////////////////////////////////////////////////////////////////////////////////////////////

# Toggles debug mode on and off from a prompt
def set_debug_mode():
    global debug_mode
    debug_mode = not debug_mode
    if debug_mode:
        print("\nDebug mode enabled. No cheating! Be respectful of the computer's feelings.")
    else:
        print("\nDebug mode disabled.")


# DEBUG Prints the ship locations
def print_debug_board():
    debug_board = []
    for j in range(board_size):
        debug_board.append(["*"] * board_size)
    for k in ship_coord:
        debug_row = k[0]
        debug_col = k[1]
        if 1 <= debug_row <= board_size and 1 <= debug_col <= board_size:
            debug_board[debug_row - 1][debug_col - 1] = "M"
    print()
    for row in debug_board:
        print(" ".join(row))
    print()


# DEBUG This shows where the ships are for testing
def print_debug_info():
    print("\nDEBUG INFO: ")
    for x in ship_coord:
        print(x)
    print("board_size: " + str(board_size))
    print("Cheat Board -----------------")
    print_debug_board()
    print("/Cheat Board -----------------")


# DEBUG Play the game 300 times automatically for testing
def test_play():
    global board, ship_coord
    for w in range(test_num_rounds):
        reset_vars(False)
        play_one_round()


# DEBUG This prompts the user for the parameters to test with.
def set_test_params():
    global test_num_ships, test_num_turns, test_num_rounds, num_ships, num_turns

    is_input_valid = False
    while not is_input_valid:
        try:
            get_input = input("\nHow many ships for testing? (4)") or 4
            test_num_ships = int(get_input)
            if 1 <= test_num_ships <= 7:
                is_input_valid = True
            else:
                print("\nPlease enter a number between 1 and 7.")
        except ValueError:
            if get_input[:1] == "q" or get_input[:1] == "Q":
                quit_game()
            else:
                print("\nPlease enter a number.")

    test_def_turns = int(((test_num_ships * 5) ** 2) / 10) + 1
    is_input_valid = False
    while not is_input_valid:
        try:
            get_input = input(
                "\nHow many shots do you want? (%d) is medium." % test_def_turns) or test_def_turns
            test_num_turns = int(get_input)
            test_turns_limit = int(((test_num_ships * 5) ** 2) / 2) + 1
            if 1 <= test_num_turns <= test_turns_limit:
                is_input_valid = True
            else:
                print("\nPlease enter a number between 1 and %d." % test_turns_limit)
        except ValueError:
            if get_input[:1] == "q" or get_input[:1] == "Q":
                quit_game()
            else:
                print("\nPlease enter a number.")

    is_input_valid = False
    while not is_input_valid:
        try:
            get_input = input(
                "\nHow many rounds to play the game? (300)") or 300
            test_num_rounds = int(get_input)
            if 1 <= test_num_rounds:
                is_input_valid = True
        except ValueError:
            if get_input[:1] == "q" or get_input[:1] == "Q":
                quit_game()
            else:
                print("\nPlease enter a number.")
    print()
    num_turns = test_num_turns
    num_ships = test_num_ships

# endRegion DEBUG Functions /////////////////////////////////////////////////////////////////////////////////////////

main()