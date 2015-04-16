#! /usr/bin/python3

from random import SystemRandom
import sys

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


# Ask for the number of ships, we get the board size from this, returns false in test mode
def ask_ships():
    global board, board_size, num_ships
    if test_mode:  # DEBUG
        return

    print("Type Q to quit or H for help.")

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
            # Check for debug mode enabled, this shows a map of all ship locations for every turn for testing
            elif get_input == "d3bug":
                print("\nDebug mode enabled. No cheating! Be respectful of the computer's feelings.")
                global debug_mode
                debug_mode = True
            # The ability to Quit mid-game, by typing Q or Quit, case-insensitive
            elif get_input[:1] == "q" or get_input[:1] == "Q":
                print("\nHave a nice day!")
                sys.exit(0)
            # The help screen
            elif get_input[:1] == "h" or get_input[:1] == "H":
                print_help()
            else:
                print("\nPlease enter a number.")


# Ask for how many turns we want, this sets difficulty, the default is medium, returns false in test mode.
def ask_turns():
    global num_turns
    if test_mode:  # DEBUG
        return

    default_turns = int(((num_ships * 5) ** 2) / 10) + 1

    is_input_valid = False
    while not is_input_valid:
        try:
            get_input = input(
                "\nHow many turns do you want? (%d) is medium." % default_turns) or default_turns
            num_turns = int(get_input)
            turns_limit = int(((num_ships * 5) ** 2) / 2) + 1
            if 1 <= num_turns <= turns_limit:
                is_input_valid = True
            else:
                print("\nPlease enter a number between 1 and %d." % turns_limit)
        except ValueError:
            if get_input[:1] == "q" or get_input[:1] == "Q":
                print("\nHave a nice day!")
                sys.exit(0)
            else:
                print("\nPlease enter a number.")
    return


# Query the user and build the game board
def setup_board():
    global board_size

    clear_screen()
    ask_ships()
    clear_screen()
    ask_turns()

    # The board size is 5 times the number of ships
    board_size = num_ships * 5
    # Build an empty board of ocean waves
    for y in range(board_size):
        board.append(["~"] * board_size)
    place_ships()
    print_board()


# Set the ships randomly in the ocean
def place_ships():
    global ship_coord
    for z in range(num_ships):
        ship_row = SystemRandom.randint(r1, 1, board_size)
        ship_col = SystemRandom.randint(r1, 1, board_size)
        # For every ship we roll to see if it is longer than one coordinate
        ship_length = SystemRandom.randint(r1, 0, 4)
        # If it is, then we roll to see what direction it stems out from.
        if ship_length:
            ship_orientation = SystemRandom.randint(r1, 1, 4)
            # These are ships that can be 2-5 coord long and stem in one of the 4 directions.
            # We also don't worry if they leave the board, this is caught later and we can't fire off the board
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

        # This saves the coordinates to be referenced for hits later
        # This is a single coordinate ship
        else:
            ship_coord.append([ship_row, ship_col])


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
    if test_mode:  # DEBUG
        return
    for i in range(100):
        print("\n")
    print("Let's play Battleship!\n")


# Show board to user
def print_board(msg=""):
    if test_mode:  # DEBUG
        return
    clear_screen()
    for row in board:
        print(" ".join(row))
    print()  # There seems to be a bug when putting these
    print(msg, "\n")  # on the same line, we get a leading space.


# DEBUG Methods ///////////////////////////////////////////////////////////////////////////////////////////////////
# DEBUG Prints the ship locations
def print_cheat_board():
    cheat_board = []
    for j in range(board_size):
        cheat_board.append(["*"] * board_size)
    for k in ship_coord:
        cheat_row = k[0]
        cheat_col = k[1]
        if 1 <= cheat_row <= board_size and 1 <= cheat_col <= board_size:
            cheat_board[cheat_row - 1][cheat_col - 1] = "M"
    print()
    for row in cheat_board:
        print(" ".join(row))
    print()


# DEBUG This shows where the ships are for testing
def print_debug_info():
    print("\nDEBUG INFO: ")
    for x in ship_coord:
        print(x)
    print("board_size: " + str(board_size))
    print("Cheat Board -----------------")
    print_cheat_board()
    print("/Cheat Board -----------------")


# DEBUG Play the game 300 times automatically for testing
def test_play():
    global board, ship_coord, num_ships, num_turns, board_size
    if test_mode:
        for w in range(test_num_rounds):
            # Clean up and start over
            board = []  # Holds the game board
            ship_coord = []  # where the ships are located

            main_func()

        print("\nWins: ", wins, "Losses: ", losses)

        avg = 0
        for w in winning_turns:
            avg += w

        avg //= len(winning_turns)
        print("Average Winning Turn: ", avg)


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
                print("\nHave a nice day!")
                sys.exit(0)
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
                print("\nHave a nice day!")
                sys.exit(0)
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
                print("\nHave a nice day!")
                sys.exit(0)
            else:
                print("\nPlease enter a number.")

    num_turns = test_num_turns
    num_ships = test_num_ships


# END DEBUG /////////////////////////////////////////////////////////////////////////////////////////////////////////


# Main body
def main_func():
    global board
    global board_size
    global num_ships
    setup_board()
    turns_left = num_turns
    # Playing the game
    while turns_left > 0:
        if not test_mode:  # DEBUG
            if turns_left == 1:
                print("Turn ", num_turns - turns_left + 1, ", last turn!")
            else:
                print("Turn ", num_turns - turns_left + 1, " / ", num_turns)

            if debug_mode:
                print_debug_info()

        # Get user's guess
        is_input_valid = False
        if test_mode:  # DEBUG
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
                        print("\nHave a nice day!")
                        sys.exit(0)
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

        if not test_mode:
            print_board(msg)
    else:
        print("Game Over")
        global losses  # DEBUG
        losses += 1  # DEBUG
        return False

# Start Main Body
main_func()

# To Test
if test_mode:
    test_play()
