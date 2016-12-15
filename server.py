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
# Imports ---------------------------------------------------------------------

import socket
from argparse import ArgumentParser
import game
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



# Main method -----------------------------------------------------------------
if __name__ == '__main__':
    # Parsing arguments
    parser = ArgumentParser()
    parser.add_argument('-l','--listenaddr', \
                        help='Bind server socket to INET address, '\
                        'defaults to %s' % DEFAULT_SERVER_INET_ADDR, \
                        default=DEFAULT_SERVER_INET_ADDR)
    parser.add_argument('-p','--listenport', \
                        help='Bind server socket to UDP port, '\
                        'defaults to %d' % DEFAULT_SERVER_PORT, \
                        default=DEFAULT_SERVER_PORT)
    '''parser.add_argument('-d','--directory', \
                        help='Directory where the files will be stored',\
                        required=False)'''
    args = parser.parse_args()

    # # Declaring, binding TCP socket, and puting into listening state
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((args.listenaddr, int(args.listenport)))
    except socket_error:
        print 'You cannot connect.'
        exit()
    s.listen(0)

    # Accepting the client connection
    while True:
        try:
            c, addr = s.accept()
            c.send('Enter your name: ')
            client_name =  c.recv(1024)
        except KeyboardInterrupt as e:
            LOG.debug('Crtrl+C issued ...')
            LOG.info('Terminating server ...')
            break

    # Close server socket
    s.close()
    LOG.debug('Server socket closed')

