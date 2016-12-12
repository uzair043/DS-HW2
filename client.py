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
    except socket.error as e:
        LOG.error('Can\'t connect to %s:%d, error: %s' % (server + (e,)))
        exit(1)
    LOG.info('Client connected to %s:%d' % server)
    connected = [True]

    # -------------------------------------------------------------------------