#!/usr/bin/env python
"""
A client/server code written in Python

Xaratustrah
2016

"""

import socket
import datetime
import random
import argparse

__version_info__ = (0, 0, 1)
__version__ = '.'.join('%d' % d for d in __version_info__)


def start_server(host, port):
    print('Server listening to host %s port %s' % (host, port))
    # create a socket object
    serversocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    # host = socket.gethostname()
    # port = 1234

    # bind to the port
    serversocket.bind((host, port))

    # queue up to 5 requests
    serversocket.listen(5)
    print('Server started. ctrl-c to abort.\n')
    try:
        while True:
            # establish a connection
            clientsocket, addr = serversocket.accept()
            print("Got a connection from %s" % str(addr))

            currentTime = datetime.datetime.now().strftime('%Y-%m-%d@%H:%M')

            number = round(random.random() * 10, 3)
            strout = currentTime + ' ' + str(number)
            clientsocket.send(strout.encode('ascii'))
            clientsocket.close()

    except(EOFError, KeyboardInterrupt):
        print('\nUser input cancelled. Aborting...')


def start_client(host, port):
    print('Client connecting to host %s port %s' % (host, port))
    # create a socket object
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # get local machine name
        # host = socket.gethostname()
        # port = 1234

        # connection to hostname on the port.
        s.connect((host, port))

        # Receive no more than 1024 bytes
        tm = s.recv(1024)
        s.close()
        print("%s" % tm.decode('ascii'))

    except(ConnectionRefusedError):
        print('Server not running. Aborting...')


def main():
    parser = argparse.ArgumentParser(prog='daqserv')
    parser.add_argument('--host', nargs=1, type=str, help='Host address', default='localhost')
    parser.add_argument('--port', nargs=1, type=int, help='Port number', default=1234)
    parser.add_argument('--server', action='store_true', help='Start server')
    parser.add_argument('--client', action='store_true', help='Start client')
    parser.add_argument('--version', action='version', version=__version__)
    parser.set_defaults(server=False)
    parser.set_defaults(client=False)

    args = parser.parse_args()
    # check the first switches

    if args.server and args.client:
        parser.print_help()
        exit()

    host = args.host[0]
    port = args.port[0]
    if args.server:
        start_server(host, port)

    elif args.host:
        start_client(host, port)

    else:
        parser.print_help()


# ----------------------------

if __name__ == '__main__':
    main()
