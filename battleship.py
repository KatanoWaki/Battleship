#! /usr/bin/python3
__author__ = 'Jeff Schreiner @ jeff.s.schreiner@gmail.com'

""" This is a text based game of battleship.
    This version has difficulty and length options,
    as well as a text based graphic of the game board.
"""

from random import SystemRandom
import sys

# Global Variables
random = SystemRandom()  # Our random number generator
board = []  # Holds the game board
debug_board = []  # Holds the debug version of the game board
ship_coord = []  # Ships' coordinates
num_ships = 0  # Number of ships set by user
board_size = 0  # Width and height of board, multiple of 5 * num_ships
num_turns = 0  # Number of turns, set by player to adjust difficulty
test_mode_enabled = False  # Flag for turning on automated game play for difficulty testing
debug_mode_enabled = False  # Flag for enabling the debug mode that shows ship locations
wins_counter = 0  # Number of wins recorded for testing
losses_counter = 0  # Number of losses recorded for testing
winning_turns = []  # An array of the last turn counter in a winning game for testing
test_num_games = 3000  # Default number of games to play during testing


# Reset board variables after every game
def reset_board():
    global board, ship_coord, debug_board
    board = []
    ship_coord = []
    debug_board = []


# Reset everything else, called after testing complete
def reset_test_vars():
    global wins_counter, losses_counter, winning_turns, num_ships, num_turns, test_num_games
    wins_counter = 0
    losses_counter = 0
    winning_turns = []
    test_num_games = 3000
    num_ships = 0
    num_turns = 0


# Toggles debug mode on and off, this is called from the prompt with "d3bug"
def toggle_debug_mode():
    global debug_mode_enabled
    debug_mode_enabled = not debug_mode_enabled
    if debug_mode_enabled:
        print("\nDebug mode enabled. No cheating! Be respectful of the computer's feelings.")
    else:
        print("\nDebug mode disabled.")


def toggle_test_mode(on_off):
    global test_mode_enabled
    test_mode_enabled = on_off


# Ask the user for the number of ships and turns
def ask_game_options():
    global num_ships, num_turns

    if test_mode_enabled:  # DEBUG suppresses asking while in test mode, we already have our variables set
        return

    print("Type Q to quit or H for help.")

    # Ask the user for the number of ships, more ships make a bigger board and generally longer game.
    is_input_valid = False
    get_input = ""
    while not is_input_valid:
        try:
            get_input = input("\nHow many ships do you want to play with? 1-7(4) ") or 4
            num_ships = int(get_input)
            # Our valid inputs are between 1 and 7 ships
            if 1 <= num_ships <= 7:
                is_input_valid = True
            else:
                print("\nPlease enter a number between 1 and 7.")
        except ValueError:
            if ui_input(get_input, "game_options"):
                return

    # The default number of turns
    default_turns = num_ships * 6

    # The max number of turns
    turns_limit = num_ships * 12

    # Ask the user how many turns they want, this sets difficulty, the default is medium
    is_input_valid = False
    while not is_input_valid:
        try:
            get_input = input(
                "\nHow many shots/turns do you want? (%d) is medium. " % default_turns) or default_turns
            num_turns = int(get_input)

            # Valid number of turns is between 1 and the upper limit, which is based on the number of ships
            if 1 <= num_turns <= turns_limit:
                is_input_valid = True
            else:
                print("\nPlease enter a number between 1 and %d." % turns_limit)
        except ValueError:
            if ui_input(get_input, "game_options"):
                return


# This prompts the user for the number of ships to begin testing with.
def ask_test_options():
    global num_ships, num_turns, test_num_games

    print("\nTest Mode Enabled, press \"Q\" to quit")

    is_input_valid = False
    get_input = ""
    while not is_input_valid:
        try:
            get_input = input("\nHow many ships for testing? 1-7(4) ") or 4
            num_ships = int(get_input)
            if 1 <= num_ships <= 7:
                is_input_valid = True
            else:
                print("\nPlease enter a number between 1 and 7.")
        except ValueError:
            ui_input(get_input)

    # The default number of turns
    default_turns = num_ships * 6

    # The max number of turns
    turns_limit = num_ships * 12

    # This prompts the user for the number of shots they want to test with
    is_input_valid = False
    while not is_input_valid:
        try:
            get_input = input(
                "\nHow many shots/turns do you want for testing? (%d) is medium." % default_turns) or default_turns
            num_turns = int(get_input)
            if 1 <= num_turns <= turns_limit:
                is_input_valid = True
            else:
                print("\nPlease enter a number between 1 and %d." % turns_limit)
        except ValueError:
            ui_input(get_input)

    # This prompts the user for how many full games they would like the testing to cycle through
    is_input_valid = False
    while not is_input_valid:
        try:
            get_input = input(
                "\nHow many rounds to play the game? (%d) " % test_num_games) or test_num_games
            num_games = int(get_input)
            if 1 <= num_games:
                is_input_valid = True
        except ValueError:
            ui_input(get_input)

    print()


# Check user input for options
def ui_input(user_in, ui_type="", turns_left=0):
    # If the user is in the normal options menu, we can select these options
    if ui_type == "game_options":
        if user_in == "t3st":
            ask_test_options()
            toggle_test_mode(True)
            # If this returns true we will break out of the main game and start testing
            return True
        elif user_in == "d3bug":
            toggle_debug_mode()
            return False

    # If the user is in the middle of a game, we can select these options
    elif ui_type == "in_game":
        if user_in[:1] == "e" or user_in[:1] == "E":
            print_board(turns_left)
            return False
        # The user can toggle debug mode for the next turn.
        elif user_in == "d3bug":
            toggle_debug_mode()
            if debug_mode_enabled:
                msg = "Debug Mode enabled"
            else:
                msg = "Debug Mode disabled"
            print_board(turns_left, msg)
            return False

    # All UI types have these options
    if user_in[:1] == "q" or user_in[:1] == "Q":
        quit_game()
    elif user_in[:1] == "h" or user_in[:1] == "H":
        print_help()
        if ui_type == "in_game":
            print("\nE to exit Help.")
    else:
        print("\nPlease enter a number.")

    # If this function returns false, we can just continue.
    return False


# Sets the ships randomly and save them to an array
def make_board():
    global ship_coord, board_size, debug_board, board

    # The board size is 5 times the number of ships
    board_size = num_ships * 5

    # For every ship that we need to create
    for z in range(num_ships):
        # Get a random coordinate to start
        ship_row = SystemRandom.randint(random, 1, board_size)
        ship_col = SystemRandom.randint(random, 1, board_size)

        # For every new ship, roll to see how long it is
        ship_length = SystemRandom.randint(random, 2, 6)

        # For every new ship, roll to see which direction it is facing
        ship_orientation = SystemRandom.randint(random, 1, 4)

        # These are ships that can be 2-6 coordinates long and stem in one of the four directions.
        # We also don't worry if they leave the board, it just makes a shorter ship.
        # We save each coordinate of the ship into the ship_coord array
        # When we check for a win, we test to see if the shot was on the board before
        # checking against the ship_coord array.

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

    # Build an array of empty ocean waves to represent the game board
    for y in range(board_size):
        board.append(["~"] * board_size)
        debug_board.append(["~"] * board_size)

    # Add all the ships to the debug_board
    for k in ship_coord:
        if 1 <= k[0] <= board_size and 1 <= k[1] <= board_size:
            debug_board[k[0] - 1][k[1] - 1] = "M"


# Show board to user
# @param msg sets a message to display below the board
def print_board(turns_left, msg=" "):
    if test_mode_enabled:  # DEBUG suppresses console output in test mode
        return

    clear_screen()

    # Print the debug board if in debug mode
    if debug_mode_enabled:
        display_board = debug_board
        # Print the ship locations as coordinates also.
        print("Ship Locations:", ship_coord, "\n")
    else:
        # Otherwise print the normal board
        display_board = board

    # Print the selected board with a message at the bottom
    for row in display_board:
        print(" ".join(row))
    print("\n" + msg + "\n")

    # If a zero is passed or we are out of turns, print the stats
    if turns_left == 0:
        print(get_stats())
    # Special statement for last turn
    elif turns_left == 1:
        print("Turn ", num_turns - turns_left + 1, ", last turn!")
    # Print the number of turns
    else:
        print("Turn ", num_turns - turns_left + 1, " / ", num_turns)


# Print the Help Screen
def print_help():
    clear_screen()
    print("\nHelp:")
    print("\nGame Objects:\n   ~~ = Water\n    X = Miss\n    M = Ship")
    print("\nWhen you see a value in parenthesis (4), just press ENTER to select defaults.\n")
    print("\"Q\" or \"QUIT\" (not case-sensitive). - Quits at any prompt")
    print("\"H\" or \"HELP\" (not case-sensitive) - Prints this help screen.")
    print("\n\"t3st\" at the game setup prompt - Setup and run thousands of automated rounds of game play.")
    print("\"d3bug\" at the setup or in-game prompt - Toggles Debug mode, shows the ship locations on the board.")


# Clear the screen and print the title
def clear_screen():
    if test_mode_enabled:  # DEBUG suppresses console output in test mode
        return
    for i in range(100):
        print("\n")
    # This message is at the top of the game most of the time.
    print("Let's play Battleship!\n")


# Print statistics after the game.
def get_stats():
    if test_mode_enabled:  # DEBUG this does not need to run in test mode
        return

    # This finds the average number of turns it took to win the game.
    avg = 0
    average_string = " "
    for w in winning_turns:
        avg += w
    if len(winning_turns) > 0:  # Suppress if there weren't any wins, prevents !DIV/0
        avg //= len(winning_turns)
        average_string = ", Average Winning Turn: " + str(avg)
    return "Wins: " + str(wins_counter) + ", Losses: " + str(losses_counter) + average_string + "\n"


# Quit the game with a goodbye message
def quit_game():
    print("\nHave a nice day!\n\n")
    sys.exit(0)


# Plays one full game of Battleship
def play_one_game():
    global board, debug_board

    # Setup the game by asking the user some questions and printing the blank board
    clear_screen()
    ask_game_options()
    make_board()
    # Start with the total number of turns that the user chose
    turns_left = num_turns
    print_board(turns_left)
    # Playing the game as long we have turns (shots) left.
    # Each loop plays one turn
    while turns_left > 0:

        if test_mode_enabled:  # DEBUG fake user input in testing mode and skip to the win-checking
            guess_row = SystemRandom.randint(random, 1, board_size)
            guess_col = SystemRandom.randint(random, 1, board_size)

        else:
            # The user is playing the game
            # Get user's guess coordinates
            is_input_valid = False
            get_input = ""
            while not is_input_valid:
                try:
                    get_input = input("\nGuess Row: ")

                    # Make sure the user's guess is an integer
                    guess_row = int(get_input)

                    get_input = input("Guess Col: ")

                    # Make sure the user's guess is an integer
                    guess_col = int(get_input)

                    # User's guess is two integers, we can continue
                    is_input_valid = True

                # The user's input was not an integer, they may be trying to tell us something else
                except ValueError:
                    ui_input(get_input, "in_game", turns_left)

        # msg gets passed to the print_board function to tell the user what happened during the round.
        msg = ""

        # Check to see if the shot is within the board limits
        if (1 <= guess_row <= board_size) and (1 <= guess_col <= board_size):

            # CHeck the user input against ship locations
            if [guess_row, guess_col] in ship_coord:
                # A match was found, the user scored a direct hit, draw damaged boat
                board[guess_row - 1][guess_col - 1] = "M"
                msg = "Congratulations! You sunk my battleship!"

                # Add a win to the stats, and record what turn it was
                global winning_turns, wins_counter
                winning_turns.append(num_turns - turns_left + 1)
                wins_counter += 1
                print_board(0, msg)
                reset_board()
                # Exit play_one_game and return to the main menu
                return True

            # Check against previous misses by looking for X's on the board
            elif board[guess_row - 1][guess_col - 1] == "X":
                msg = "You guessed that one already."

            # The shot missed and wasn't previously guessed
            else:
                msg = "You missed my battleship!"

            # Add an X to the board at the guess location to keep track of previous guesses
            board[guess_row - 1][guess_col - 1] = "X"
            debug_board[guess_row - 1][guess_col - 1] = "X"

        # The shot wasn't inside the board limits
        else:
            msg = "Oops, that's not even in the ocean!"

        # Subtract a turn
        turns_left -= 1

        # Print the board and tell the user what happened with msg
        print_board(turns_left, msg)

    # The user ran ouf of turns. Add a loss to stats and return to the main menu
    else:
        global losses_counter
        losses_counter += 1
        print_board(0, "Game Over")
        reset_board()
        return False


# Entry point, this loops the game until user exits.
def main():
    while True:
        # Automated testing mode is enabled
        # Play the game several times in a row automatically for testing
        if test_mode_enabled:
            for w in range(test_num_games):
                play_one_game()
            # Toggle test most off first to print stats
            toggle_test_mode(False)
            print(get_stats())
            # Reset everything back to defaults
            reset_test_vars()

        # User is playing the game
        else:
            play_one_game()

        # After each game or batch of testing, ask the user if they would like to play again or quit.
        if not test_mode_enabled:
            play_again = input("Play again? (Q to Quit or any key to Continue)") or "Y"
            if play_again[:1] == "q" or play_again[:1] == "Q":
                quit_game()

main()