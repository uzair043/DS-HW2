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


#Function to create game board
#This function will create a 10x10 board
def game_board(s, board):

    BOARD_SIZE = 10
    player = "Server"
    if s == "u":
        player = "User"


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

        # print a horizontal line
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
            is_valid = validate(board, ships[ship], x_cord, y_cord, orientation)
            if not is_valid:
                print "The entered coordinates are not correct. Please try again."
                raw_input("Press any key to continue...")

        # if the coordinates are valid, then place the ship on the given coordinates
        board = place_ship(board, ships[ship], ship[0], orientation, x_cord, y_cord)
        game_board("u", board)

    print "The ship is placed on the given coordinates."
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
            is_valid = validate(board, ships[ship], x_cord, y_cord, orientation)

        # server placing the ship
        print "Ship placed by server:  " + ship
        board = place_ship(board, ships[ship], ship[0], ori, x, y)

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