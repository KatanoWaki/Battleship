#! /usr/bin/python3

from random import SystemRandom
import sys

# Global Variables
r1 = SystemRandom()  # Our random number generator, SystemRandom gives very good results
board = []  # Holds the game board
ship_coord = []  # where the ships are located
num_ships = 0  # This is set by user
board_size = 0  # width and height of board, multiple of 5 * num_ships
num_turns = 0  # Change this manually for difficulty
test_mode = False  # This gets enabled for automated game play to trial difficulty
debug_mode = False  # This shows the ships locations and other information
wins = 0  # Number of wins recorded for testing
losses = 0  # Number of losses recorded for testing
winning_turns = []  # An array of the last turn counter in a winning game for testing
test_num_ships = 4  # Default number of ships for testing
test_num_turns = 41  # Default number of turns for testing
test_num_rounds = 300  # Default number of games to play for testing


# Reset all variables after every game
# Reset win records if T is passed for test mode
def reset_vars(arg):
    global board, ship_coord, wins, losses, winning_turns, test_mode

    board = []
    ship_coord = []
    # We reset data after a test run
    if arg == "T":
        wins = 0
        losses = 0
        winning_turns = []
        test_mode = False


# Ask for the number of ships and turns
def ask_game_options():
    global num_ships, num_turns, board_size

    if test_mode:  # DEBUG suppresses asking while in test mode, we already have our vars set
        return

    print("Type Q to quit or H for help.")

    # Ask for then number of ships, this also create a bigger board and generally longer game.
    is_input_valid = False
    while not is_input_valid:
        try:
            get_input = input("\nHow many ships do you want to play with? (4)") or 4
            num_ships = int(get_input)
            if 1 <= num_ships <= 7:
                is_input_valid = True
            else:
                print("\nPlease enter a number between 1 and 7.")
        except ValueError:
            # Check for testing mode enabled, this enables automated game play for difficulty testing
            if get_input == "t3st":
                set_test_params()
                global test_mode
                test_mode = True
                return
            # Toggle debug mode, this shows a map of all ship locations for every turn for testing
            elif get_input == "d3bug":
                set_debug_mode()
            # The ability to Quit mid-game, by typing Q or Quit, case-insensitive
            elif get_input[:1] == "q" or get_input[:1] == "Q":
                quit_game()
            # The help screen
            elif get_input[:1] == "h" or get_input[:1] == "H":
                print_help()
            else:
                print("\nPlease enter a number.")

    # Math to determine the medium (default_turns) and easiest (turns_limit) difficulty
    default_turns = int(((num_ships * 5) ** 2) / 10) + 1
    turns_limit = int(((num_ships * 5) ** 2) / 2) + 1

    # Ask for how many turns we want, this sets difficulty, the default is medium
    is_input_valid = False
    while not is_input_valid:
        try:
            get_input = input(
                "\nHow many turns do you want? (%d) is medium." % default_turns) or default_turns
            num_turns = int(get_input)
            if 1 <= num_turns <= turns_limit:
                is_input_valid = True
            else:
                print("\nPlease enter a number between 1 and %d." % turns_limit)
        except ValueError:
            # Check for testing mode enabled, this enables automated game play for difficulty testing
            if get_input == "t3st":
                set_test_params()
                global test_mode
                test_mode = True
                return
            elif get_input == "d3bug":
                set_debug_mode()
            elif get_input[:1] == "q" or get_input[:1] == "Q":
                quit_game()
            elif get_input[:1] == "h" or get_input[:1] == "H":
                print_help()
            else:
                print("\nPlease enter a number.")


# Set the ships randomly on the board
def make_board():
    global ship_coord, board_size

    # The board size is 5 times the number of ships
    board_size = num_ships * 5
    # Build an empty board of ocean waves
    for y in range(board_size):
        board.append(["~"] * board_size)

    for z in range(num_ships):
        ship_row = SystemRandom.randint(r1, 1, board_size)
        ship_col = SystemRandom.randint(r1, 1, board_size)
        # For every ship we roll to see if it is longer than one coordinate
        ship_length = SystemRandom.randint(r1, 0, 4)
        # If it is, then we roll to see what direction it stems out from.
        if ship_length:
            ship_orientation = SystemRandom.randint(r1, 1, 4)
            # These are ships that can be 2-5 coordinates long and stem in one of the 4 directions.
            # We also don't worry if they leave the board, it just makes a shorter ship.
            if ship_orientation == 1:
                ship_coord.append([ship_row, ship_col])
                for i in range(1, ship_length):
                    ship_row += 1
                    ship_coord.append([ship_row, ship_col])
            elif ship_orientation == 2:
                ship_coord.append([ship_row, ship_col])
                for i in range(1, ship_length):
                    ship_col += 1
                    ship_coord.append([ship_row, ship_col])
            elif ship_orientation == 3:
                ship_coord.append([ship_row, ship_col])
                for i in range(1, ship_length):
                    ship_row -= 1
                    ship_coord.append([ship_row, ship_col])
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
    print("\nGame Objects: ~ water, X miss, M ship")
    print("\nAt the setup prompts, the default values are in parenthesis. Press enter to select defaults.")
    print("You can quit at anytime by typing Q or QUIT (case-insensitve).")
    print("For testing, you can automate thousands rounds of play by typing \"t3st\" at the prompt.")
    print("Also, you can print a cheat map with ship locations by typing \"d3bug\" at the prompt.")


# Clear Screen
def clear_screen():
    if test_mode:  # DEBUG suppresses console output in test mode
        return
    for i in range(100):
        print("\n")
    print("Let's play Battleship!\n")


# Show board to user
def print_board(msg=""):
    if test_mode:  # DEBUG suppresses console output in test mode
        return
    clear_screen()
    for row in board:
        print(" ".join(row))
    print()  # There seems to be a bug when putting these
    print(msg, "\n")  # on the same line, we get a leading space.


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


# DEBUG Functions ///////////////////////////////////////////////////////////////////////////////////////////////////
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
        reset_vars("P")
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


# END DEBUG Functions ///////////////////////////////////////////////////////////////////////////////////////////////


# Main body of the game
def play_one_round():
    global board, num_ships

    # Setup the game
    clear_screen()
    ask_game_options()
    make_board()
    print_board()
    turns_left = num_turns

    # Playing the game
    while turns_left > 0:
        if not test_mode:  # DEBUG suppresses console output in test mode
            if turns_left == 1:
                print("Turn ", num_turns - turns_left + 1, ", last turn!")
            else:
                print("Turn ", num_turns - turns_left + 1, " / ", num_turns)

            if debug_mode:  # DEBUG displays debugging info and cheat board in debug mode
                print_debug_info()

        # Get user's guess
        is_input_valid = False
        if test_mode:  # DEBUG fake user input
            guess_row = SystemRandom.randint(r1, 1, board_size)
            guess_col = SystemRandom.randint(r1, 1, board_size)
        else:
            while not is_input_valid:
                try:
                    row_input = ""
                    col_input = ""
                    row_input = input("\nGuess Row: ")
                    guess_row = int(row_input)
                    col_input = input("Guess Col: ")
                    guess_col = int(col_input)
                    is_input_valid = True
                except ValueError:
                    # The ability to Quit mid-game, by typing Q or Quit, case-insensitive
                    if row_input[:1] == "q" or row_input[:1] == "Q" or col_input[:1] == "q" or col_input[:1] == "Q":
                        quit_game()
                    elif row_input == "d3bug":
                        set_debug_mode()
                    else:
                        print("\nPlease enter a number.")

        msg = ""

        # Check the guess coordinates for a ship
        if (1 <= guess_row <= board_size) and (1 <= guess_col <= board_size):
            for x in ship_coord:
                if x == [guess_row, guess_col]:
                    board[guess_row - 1][guess_col - 1] = "M"
                    msg = "Congratulations! You sunk my battleship!\n"
                    global winning_turns
                    winning_turns.append(num_turns - turns_left + 1)  # DEBUG
                    print_board(msg)
                    global wins  # DEBUG
                    wins += 1  # DEBUG
                    return True
                # This checks against previous misses by looking for X's on the board
                elif board[guess_row - 1][guess_col - 1] == "X":
                    msg = "You guessed that one already."
                    break
                msg = "You missed my battleship!"
            board[guess_row - 1][guess_col - 1] = "X"
        else:
            msg = "Oops, that's not even in the ocean!"

        turns_left -= 1

        print_board(msg)

    else:
        print_board("Game Over")
        global losses  # DEBUG
        losses += 1  # DEBUG
        return False

# Start here, this is the wrapper that loops the game until user exits.
while True:
    if test_mode:
        test_play()
        print_stats()
        reset_vars("T")
    else:
        play_one_round()
        reset_vars("P")
        if not test_mode:
            print_stats()

    if not test_mode:
        play_again = input("Play again? (Q to Quit or any key to Continue)") or "Y"
        if play_again[:1] == "q" or play_again[:1] == "Q":
            quit_game()