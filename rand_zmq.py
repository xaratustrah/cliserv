#!/usr/bin/env python
"""
A client/server code written in Python

Xaratustrah
2016

"""

import datetime, time
import random
import argparse
import zmq

__version_info__ = (0, 0, 1)
__version__ = '.'.join('%d' % d for d in __version_info__)


def start_server(host, port):
    context = zmq.Context()
    sock = context.socket(zmq.PUB)
    sock.bind("tcp://{}:{}".format(host, port))

    print('Server started. ctrl-c to abort.\n')
    try:
        while True:
            topic = '10001'  # just a number for identification
            current_time = datetime.datetime.now().strftime('%Y-%m-%d@%H:%M:%S.%f')
            number = round(random.random() * 10, 3)
            messagedata = current_time + ' ' + str(number)
            print("{} {}".format(topic, messagedata))
            sock.send_string("{} {}".format(topic, messagedata))
            time.sleep(0.5)

    except(EOFError, KeyboardInterrupt):
        print('\nUser input cancelled. Aborting...')


def start_client(host, port):
    context = zmq.Context()
    print('Client started. ctrl-c to abort.\n')
    try:
        sock = context.socket(zmq.SUB)
        sock.connect("tcp://{}:{}".format(host, port))
        topic_filter = '10001'
        sock.setsockopt_string(zmq.SUBSCRIBE, topic_filter)

        for update_nbr in range(5):
            string = sock.recv().decode("utf-8")
            topic, time, value = string.split()
            print(time, float(value))

    except(ConnectionRefusedError):
        print('Server not running. Aborting...')

    except(EOFError, KeyboardInterrupt):
        print('\nUser input cancelled. Aborting...')


def main():
    parser = argparse.ArgumentParser(prog='daqserv')
    parser.add_argument('--host', nargs=1, type=str, help='Host address', default='localhost')
    parser.add_argument('--port', nargs=1, type=int, help='Port number', default=1234)
    parser.add_argument('--version', action='version', version=__version__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--client', action='store_true', help='Start client')
    group.add_argument('--server', action='store_true', help='Start server')
    parser.set_defaults(server=False)
    parser.set_defaults(client=False)

    args = parser.parse_args()
    # check the first switches

    if isinstance(args.host, list):
        host = args.host[0]
    else:
        host = args.host

    if isinstance(args.port, list):
        port = args.port[0]
    else:
        port = args.port

    if args.server:
        start_server(host, port)

    elif args.host:
        start_client(host, port)

    else:
        parser.print_help()


# ----------------------------

if __name__ == '__main__':
    main()
