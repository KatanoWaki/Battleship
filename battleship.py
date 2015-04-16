#! /usr/bin/python3

from random import SystemRandom
import time  # DEBUG

board = []  # Holds the game board
ship_coord = []  # where the ships are located
num_ships = 0  # This is set by user
board_size = 0  # width and height of board, multiple of 5 * num_ships
num_turns = 0  # Change this manually for difficulty
test_mode = False  # This gets enabled for automated game play to trial difficulty
wins = 0
losses = 0
winning_turns = []
r1 = SystemRandom()

# TODO: make better, cleanup and add doc comments, make manual from comments, test for difficulty


# Query the user and build the game board
def setup_board():
    global board_size

    clear_screen()
    print("Let's play Battleship!")

    ask_ships()

    clear_screen()
    print("Let's play Battleship!")

    ask_turns()

    # The board size is 5 times the number of ships
    board_size = num_ships * 5
    # Build an empty board of ocean waves
    for y in range(board_size):
        board.append(["~"] * board_size)
    set_ships()
    print_board()


# Clear Screen
def clear_screen():
    for i in range(100):
        print("\n")


# Ask for the number of ships, we get the board size from this, returns false in test mode
def ask_ships():
    global board
    global board_size
    global num_ships
    global test_mode
    is_input_valid = False
    if test_mode:  # DEBUG
        num_ships = 4
        return False
    while not is_input_valid:
        get_input = ""
        try:
            get_input = input("\nHow many ships do you want to play with? (2)") or 2
            num_ships = int(get_input)
            if 1 <= num_ships <= 7:
                is_input_valid = True
            else:
                print("\nPlease enter a number between 1 and 7.")
        except ValueError:
            # Check for testing mode enabled, this triggers automated gameplay for difficulty testing purposes
            if get_input == "t3st":
                test_mode = True
                print("\nTesting Enabled, num_ships 4 and num_turns 134")
                num_ships = 4
                return False
            else:
                print("\nPlease enter a number.")
    return True


# Ask for how many turns we want, this sets difficulty, the default is medium, returns false in test mode.
def ask_turns():
    global num_turns
    is_input_valid = False
    default_turns = int(((num_ships * 5) ** 2) / 9) + 1
    if test_mode:  # DEBUG
        num_turns = default_turns
        return False
    while not is_input_valid:
        try:
            num_turns = int(input("\nHow many turns do you want? (%d) is medium, lower is harder." % default_turns)
                            or default_turns)
            turns_limit = int(((num_ships * 5) ** 2) / 2) + 1
            if 1 <= num_turns <= turns_limit:
                is_input_valid = True
            else:
                print("\nPlease enter a number between 1 and %d." % turns_limit)
        except ValueError:
            print("\nPlease enter a number.")
    return True


# Set the ships randomly in the ocean
def set_ships():
    global ship_coord
    for z in range(num_ships):
        ship_row = SystemRandom.randint(r1, 1, board_size)
        ship_col = SystemRandom.randint(r1, 1, board_size)
        # For every ship we roll to see if it is longer than one coordinate
        ship_length = r1.randint(0, 4)
        # If it is, then we roll to see what direction it stems out from.
        if ship_length:
            ship_orientation = r1.randint(1, 4)
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


# Show board to user
def print_board(msg=""):
    if test_mode:  # DEBUG
        return
    clear_screen()
    print(msg, "\n")
    for row in board:
        print(" ".join(row))
    print("\n")


'''
# For debugging only/////////////////////////////////////////////////////////////////////////////////////
def print_cheat_board():

    cheat_board = []
    for j in range(board_size):
        cheat_board.append(["+"] * board_size)
    for k in ship_coord:
        cheat_row = k[0]
        cheat_col = k[1]
        if 1 <= cheat_row <= board_size and 1 <= cheat_col <= board_size:
            cheat_board[cheat_row - 1][cheat_col - 1] = "%"
    print()
    for row in cheat_board:
        print(" ".join(row))
    print()
# /////////////////////////////////////////////////////////////////////////////////////////////////////////
'''


# Main body
def main_func():
    global board
    global board_size
    global num_ships
    setup_board()
    turns_left = num_turns
    # Playing the game
    while turns_left > 0:
        # time.sleep(1)  # DEBUG
        if turns_left == 1:
            print("Turn ", num_turns - turns_left + 1, " , last turn.")
        else:
            print("Turn ", num_turns - turns_left + 1, " / ", num_turns)
        '''
        # DEBUG Remove for final, this shows where the ships are for testing/////////////////////////////
        print("\nDEBUG INFO: ")
        for x in ship_coord:
            print(x)
        print("board_size: " + str(board_size))
        print("Cheat Board -----------------")
        print_cheat_board()
        print("/Cheat Board -----------------")
        # END DEBUG//////////////////////////////////////////////////////////////////////////////////////
        '''

        # Get user's guess
        is_input_valid = False
        if test_mode:  # DEBUG
            guess_row = r1.randint(1, board_size)
            guess_col = r1.randint(1, board_size)
        else:
            while not is_input_valid:
                try:
                    row_input = input("\nGuess Row: ")
                    guess_row = int(row_input)
                    guess_col = int(input("Guess Col: "))
                    is_input_valid = True
                except ValueError:
                    # The ability to Quit mid-game, by typing Q or Quit, case-insensitive
                    if row_input[:1] == "q" or row_input[:1] == "Q":
                        print("\nHave a nice day!")
                        return False

                print("\nPlease enter a number.")

        turns_left -= 1
        msg = ""
        # Check the guess coordinates for a ship
        if (1 <= guess_row <= board_size) and (1 <= guess_col <= board_size):
            for x in ship_coord:
                if x == [guess_row, guess_col]:
                    board[guess_row - 1][guess_col - 1] = "%"
                    msg = "Congratulations! You sunk my battleship!\n"
                    winning_turns.append(num_turns - turns_left + 1)
                    print_board(msg)
                    global wins
                    wins += 1
                    return True
                # This checks against previous misses
                elif board[guess_row - 1][guess_col - 1] == "X":
                    msg = "You guessed that one already."
                    break
            msg = "You missed my battleship!"
            board[guess_row - 1][guess_col - 1] = "X"
        else:
            msg = "Oops, that's not even in the ocean!"

        if not test_mode:
            print_board(msg)
    else:
        print("Game Over")
        global losses
        losses += 1
        return False

# Start Main Body
main_func()

# Play the game 300 times automatically for testing
if test_mode:
    for w in range(300):
        # Clean up and start over
        board = []  # Holds the game board
        ship_coord = []  # where the ships are located
        num_ships = 0  # This is set by user
        board_size = 0  # width and height of board, multiple of 5 * num_ships
        num_turns = 0  # Change this manually for difficulty

        main_func()

    print("\nWins: ", wins, "Losses: ", losses)

    avg = 0
    for w in winning_turns:
        avg += w

    avg /= len(winning_turns)
    print(avg)