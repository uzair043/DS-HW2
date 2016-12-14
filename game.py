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

board = []
game_board('u',board)