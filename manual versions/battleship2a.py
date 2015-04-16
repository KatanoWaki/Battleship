#! /usr/bin/python3

from random import randint

board = []
board_size = 0
ship_coord = []
won = False
num_ships = 0


# Build the game board and place the ships
def setup_board():
    is_size_valid = False
    print()
    print()
    print("Let's play Battleship!")
    print()
    global num_ships

    while not is_size_valid:
        num_ships = int(input("How many ships do you want to play with?  "))
        if 1 <= num_ships <= 5:
            is_size_valid = True
        else:
            print()
            print("Please enter a number between 1 and 5.")

    global board_size
    global board

    board_size = num_ships * 5
    for x in range(board_size):
        board.append(["~"] * board_size)

    set_ships(num_ships)
    print_board(board)


# Show board to user
def print_board(board):
    print()
    print()
    for row in board:
        print(" ".join(row))
    print()
    print()


# Random ship placers
def random_row(xboard):
    return randint(0, len(xboard) - 1)


def random_col(xboard):
    return randint(0, len(xboard[0]) - 1)


def set_ships(xnum_ships):
    for x in range(xnum_ships):
        ship_row = random_row(board)
        ship_col = random_col(board)
        coord = [ship_row, ship_col]
        global ship_coord
        ship_coord.append(coord)


# Main body
def main_func():
    setup_board()
    global board_size
    turns_left = 4
    # for turn in range(4):
    while turns_left > 0:
        if 5 - turns_left == 4:
            print("Turn ", 5 - turns_left, " , last turn.")
        else:
            print("Turn ", 5 - turns_left)

        """
        #DEBUG Remove for final
        print
        print "DEBUG INFO: "
        for x in ship_coord:
            print x
        print "board_size: " + str(board_size)
        #ENDEBUG """

        print()
        guess_row = int(input("Guess Row:")) - 1
        guess_col = int(input("Guess Col:")) - 1
        turns_left -= 1
        for x in ship_coord:
            if guess_row == x[0] and guess_col == x[1]:
                board[guess_row][guess_col] = "%"
                print_board(board)
                print("Congratulations! You sunk my battleship!")
                print()
                return True
                break
            else:
                print()
                if (guess_row < 0 or guess_row > board_size - 1) or (guess_col < 0 or guess_col > board_size - 1):
                    print("Oops, that's not even in the ocean.")
                    break
                elif board[guess_row][guess_col] == "X":
                    print("You guessed that one already.")
                    break
                else:
                    print("You missed my battleship!")
                    board[guess_row][guess_col] = "X"
                    break

        print_board(board)
    else:
        print("Game Over")
        return False


main_func()