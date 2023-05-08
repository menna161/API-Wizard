import sys
import time
import random
import asyncio
import asyncio.streams


@asyncio.coroutine
def _handle_client(self, client_reader, client_writer):
    '\n        This method actually does the work to handle the requests for\n        a specific client.  The protocol is line oriented, so there is\n        a main loop that reads a line with a request and then sends\n        out one or more lines back to the client with the result.\n        '
    while True:
        data = (yield from client_reader.readline()).decode('utf-8')
        if (not data):
            break
        (cmd, *args) = data.rstrip().split(' ')
        if (cmd == 'add'):
            arg1 = float(args[0])
            arg2 = float(args[1])
            retval = (arg1 + arg2)
            client_writer.write('{!r}\n'.format(retval).encode('utf-8'))
        elif (cmd == 'repeat'):
            times = int(args[0])
            msg = args[1]
            client_writer.write('begin\n'.encode('utf-8'))
            for idx in range(times):
                client_writer.write('{}. {}\n'.format((idx + 1), (msg + ('x' * random.randint(10, 50)))).encode('utf-8'))
            client_writer.write('end\n'.encode('utf-8'))
        else:
            print('Bad command {!r}'.format(data), file=sys.stderr)
        (yield from client_writer.drain())
