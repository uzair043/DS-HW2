#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

Created on Mon Dec 13 22:04:34 2016
@author: Muhammad Uzair

"""


#Imports----------------------------------------------------------

import copy
import random

#End Imports------------------------------------------------------

# Constants -------------------------------------------------------------------
___NAME = 'Battleship Game'
___VER = '0.1.0.0'
___DESC = 'Battleship Game'
___BUILT = '2016-12-13'
# Private methods -------------------------------------------------------------
def __info():
    return '%s version %s (%s)' % (___NAME, ___VER, ___BUILT)



#Function to create game board
#This function will create a 10x10 board
def game_board(s, board):

    BOARD_SIZE = 10
    player = "Server"
    if s == "c":
        player = "client"

    print "The " + player + " game board is as follows: "

    # printing the column numbers
    print " ",
    for i in range(BOARD_SIZE):
        print "  " + str(i + 1) + "  ",
    print "\n"

    for i in range(BOARD_SIZE):

        # printing the row numbers
        if i != BOARD_SIZE-1:
            print str(i + 1) + "  ",
        else:
            print str(i + 1) + " ",

        # printing the actual board
        for j in range(BOARD_SIZE):
            if board[i][j] == -1:
                print ' ',
            elif s == "u":
                print board[i][j],
            elif s == "c":
                if board[i][j] == "*" or board[i][j] == "$":
                    print board[i][j],
                else:
                    print " ",

            if j != BOARD_SIZE-1:
                print " | ",
        print

        # print the horizontal line when the cells have been drawn for a single row
        if i != BOARD_SIZE:
            print "   ----------------------------------------------------------"
        else:
            print

#Function ends here-----------------------------------------------------------------------------

#function to place ships at the given coordinates by the user
#if the coordinates are validated, the ship will be placed
#if the coordinates are not validated, the message will be delivered to the user
#and the board with the previous values will be returned to the user
def ship_placement_client(board, ships):
    for ship in ships.keys():

        #getting the coordinates from user and validating if they can be placed on the game board
        is_valid = False
        while (not is_valid):
            game_board("u", board)
            print "Placing a/an " + ship
            x_cord, y_cord = get_coordinates()
            orientation = vertical_or_horizontal()
            is_valid = validate_coordinates(board, ships[ship], x_cord, y_cord, orientation)
            if not is_valid:
                print "The entered coordinates are not correct. Please try again."
                raw_input("Press any key to continue...")

        # if the coordinates are valid, then place the ship on the given coordinates
        board = place_ship(board, ships[ship], ship[0], orientation, x_cord, y_cord)
        game_board("u", board)

    print "All the ships are placed at the given coordinates."
    raw_input("Press any key to continue...")
    return board

#Function End Here------------------------------------------------------------------------------


#function to place the ships by the server at coordinates choosen randomly between 1-10
#the coordinates will be validated
#the board will be returned with the ships from server
def random_ship_placement_server(board, ships):
    for ship in ships.keys():

        # random x and y coordinates and get the orientation
        is_valid = False
        while (not is_valid):

            x_cord = random.randint(1, 10) - 1
            y_cord = random.randint(1, 10) - 1
            get_ori = random.randint(0, 1)
            if get_ori == 0:
                orientation = "v"
            else:
                orientation = "h"
            is_valid = validate_coordinates(board, ships[ship], x_cord, y_cord, orientation)

        # server placing the ship
        print "Ship placed by server:  " + ship
        board = place_ship(board, ships[ship], ship[0], get_ori, x_cord, y_cord)

    return board

#Function End Here------------------------------------------------------------------------------


#Function to place the ship on the board
#the ship can be from user or from server
def place_ship(board,ship, s_type, orientation, x_cord, y_cord):

	if orientation == "v":
		for i in range(ship):
			board[x_cord+i][y_cord] = s_type
	elif orientation == "h":
		for i in range(ship):
			board[x_cord][y_cord+i] = s_type

	return board

#Function ends here----------------------------------------------------------------------------


#Function to validate the input coordinates from the user and random coordinates from the server
#the output will be true if the ship can be place on the given coordinates, false otherwise
def validate_coordinates(board, ship, x_cord, y_cord, orientation):

    BOARD_SIZE = 10
    if orientation == "v" and x_cord + ship > BOARD_SIZE:
        return False
    elif orientation == "h" and y_cord + ship > BOARD_SIZE:
        return False
    else:
        if orientation == "v":
            for i in range(ship):
                if board[x_cord + i][y_cord] != -1:
                    return False
        elif orientation == "h":
            for i in range(ship):
                if board[x_cord][y_cord + i] != -1:
                    return False

    return True

#Function ends here----------------------------------------------------------------------------

#Function to choose orientation
def vertical_or_horizontal():

	#get orientation from user until user enters correct orientation
	while(True):
		choice = raw_input("Enter v for vertical and h for horizontal: ")
		if choice == "v" or choice == "h":
			return choice
		else:
			print "Please only enter letters v or h."

#Function ends here----------------------------------------------------------------------------


#Function to get coordinates from the user
def get_coordinates():
    while (True):
        #get coordinates from the user
        #These coordinates can be used for placing ship or guessing the ship when it is user's move to guess the ship
        input_coor = raw_input("Enter coordinates to place/guess ship(r,c): ")
        try:
            #check if two values were entered by user
            #values should be separated by comma
            coordinates = input_coor.split(",")
            if len(coordinates) != 2:
                raise Exception("Too many/few coordinates.");

            coordinates[0] = int(coordinates[0]) - 1
            coordinates[1] = int(coordinates[1]) - 1

            # check that values of coordinates should be between 1 to 10
            if coordinates[0] > 9 or coordinates[0] < 0 or coordinates[1] > 9 or coordinates[1] < 0:
                raise Exception("Please enter values between 1 to 10.")

            # return input coordinates if they are in correct format
            return coordinates

        #Throw an error message if the value is not a numeric value.
        except ValueError:
            print "Please enter only numeric values."
        except Exception as e:
            print e


# Function ends here----------------------------------------------------------------------------


#Making a board move
def make_move(board, x_cord, y_cord):
    # make a move on the board and return the result, hit, miss or try again for repeat hit
    if board[x_cord][y_cord] == -1:
        return "miss"
    elif board[x_cord][y_cord] == '*' or board[x_cord][y_cord] == '$':
        return "try again"
    else:
        return "hit"

#Function ends here----------------------------------------------------------------------------


#function to get the coordinates from the client to make a move
#if the move is a hit, check for sinking of ship and also for Win
#If it is not hit, return miss
#If already hit, return try again
def client_move(board):
    # get coordinates from the client to make a move
    # if move is a hit, check for sinking of whole ship
    #also check for Win condition
    while (True):
        x_cord, y_cord = get_coordinates()
        res = make_move(board, x_cord, y_cord)
        if res == "hit":
            print "Hit at " + str(x_cord + 1) + "," + str(y_cord + 1)
            check_sink_ship(board, x_cord, y_cord)
            board[x_cord][y_cord] = '$'
            if check_win(board):
                return "WIN"
        elif res == "miss":
            print "Sorry, " + str(x_cord + 1) + "," + str(y_cord + 1) + " is a miss."
            board[x_cord][y_cord] = "*"
        elif res == "try again":
            print "Sorry, that coordinate was already hit. Please try again"

        if res != "try again":
            return board

#Function ends here----------------------------------------------------------------------------


#Function to make move for server at randomly selected coordinates
#if the move is a hit, check for sinking of ship and also for Win
#If it is not hit, return miss
def server_move(board):
    # generate user coordinates from the user and try to make move
    # if move is a hit, check ship sunk and win condition
    while (True):
        x_cord = random.randint(1, 10) - 1
        y_cord = random.randint(1, 10) - 1
        res = make_move(board, x_cord, y_cord)
        if res == "hit":
            print "Hit at " + str(x_cord + 1) + "," + str(y_cord + 1)
            check_sink_ship(board, x_cord, y_cord)
            board[x_cord][y_cord] = '$'
            if check_win(board):
                return "WIN"
        elif res == "miss":
            print "Sorry, " + str(x_cord + 1) + "," + str(y_cord + 1) + " is a miss."
            board[x_cord][y_cord] = "*"

        if res != "try again":
            return board


#Function ends here----------------------------------------------------------------------------


#Function to check which ship is sunk
#The alphabet value will be get from the coordinates and then assign that to a variable
#Then return the value of that ship
def check_sink_ship(board, x_cord, y_cord):
    # figure out what ship was hit
    if board[x_cord][y_cord] == "A":
        sunken_ship = "Aircraft Carrier"
    elif board[x_cord][y_cord] == "B":
        sunken_ship = "Battleship"
    elif board[x_cord][y_cord] == "S":
        sunken_ship = "Submarine"
    elif board[x_cord][y_cord] == "D":
        sunken_ship = "Destroyer"
    elif board[x_cord][y_cord] == "P":
        sunken_ship = "Patrol Boat"

    # mark cell as hit and check if sunk
    board[-1][sunken_ship] -= 1
    if board[-1][sunken_ship] == 0:
        print sunken_ship + " is Sunken."

#Function ends here----------------------------------------------------------------------------


#Function to check which board
#It will check all the cell values and return true if all the cell values contains a hit and false otherwise
def check_win(board):
    BOARD_SIZE = 10
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != -1 and board[i][j] != '*' and board[i][j] != '$':
                return False
    return True


#Function ends here----------------------------------------------------------------------------

