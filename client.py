#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

Created on Mon Dec 12 10:54:09 2016
@author: Muhammad Uzair

"""

# Setup Python logging ------------------ -------------------------------------
import logging
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
LOG = logging.getLogger()
# Imports----------------------------------------------------------------------

import socket
from argparse import ArgumentParser
from game import *
import copy

# Constants -------------------------------------------------------------------
___NAME = 'Battleship Game'
___VER = '0.1.0.0'
___DESC = 'Battleship Game Client'
___BUILT = '2016-12-12'
# Private methods -------------------------------------------------------------
def __info():
    return '%s version %s (%s)' % (___NAME, ___VER, ___BUILT)

# TCP related constants -------------------------------------------------------
DEFAULT_SERVER_PORT = 7777
DEFAULT_SERVER_INET_ADDR = '127.0.0.1'


#Game main method--------------------------------------------------------------

def game_start():
    BOARD_SIZE = 10
    # There are five types of ships
    # The number next to the ship type describe the number of cells that ship can occupy
    ships = {"Aircraft Carrier": 5,
             "Battleship": 4,
             "Submarine": 3,
             "Destroyer": 3,
             "Patrol Boat": 2}

    # Creating a blank board
    # -1 is added to every cell of the board
    board = []
    for i in range(BOARD_SIZE):
        board_row = []
        for j in range(BOARD_SIZE):
            board_row.append(-1)
        board.append(board_row)

    # client and server boards are being created
    user_board = copy.deepcopy(board)
    comp_board = copy.deepcopy(board)

    # ships are being added to the client and server boards
    user_board.append(copy.deepcopy(ships))
    comp_board.append(copy.deepcopy(ships))

    # Cient ship placement
    user_board = ship_placement_client(user_board, ships)
    # Server Random Ship placement
    comp_board = random_ship_placement_server(comp_board, ships)

    # game main loop
    while (True):

        # client move
        game_board("c", comp_board)
        comp_board = client_move(comp_board)

        # check if client is winner
        if comp_board == "WIN":
            print "Congratulatios! You won."
            quit()

        # display current server board
        game_board("c", comp_board)
        raw_input("Press any key to end yuor turn...")

        # server move
        user_board = server_move(user_board)

        # check if the server is winner
        if user_board == "WIN":
            print "Very sad, the server won the game :("
            quit()

        # display client board
        game_board("u", user_board)
        raw_input("Press any key to end the server turn...")


# Main method ------------------------------------------a----------------------
if __name__ == '__main__':
    # Parsing arguments
    parser = ArgumentParser()
    parser.add_argument('-H', '--host', \
                        help='Server INET address ' \
                             'defaults to %s' % DEFAULT_SERVER_INET_ADDR, \
                        default=DEFAULT_SERVER_INET_ADDR)
    parser.add_argument('-p', '--port', type=int, \
                        help='Server UDP port, ' \
                             'defaults to %d' % DEFAULT_SERVER_PORT, \
                        default=DEFAULT_SERVER_PORT)
    args = parser.parse_args()

    # Server's socket address
    server = (args.host, int(args.port))

    # Connection---------------------------------------------------------------
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((args.host, args.port))
        print s.recv(1024)
        sname = raw_input()
        s.send(sname)
        game_start()

    except socket.error as e:
        LOG.error('Can\'t connect to %s:%d, error: %s' % (server + (e,)))
        exit(1)

    #s.close()
    # -------------------------------------------------------------------------