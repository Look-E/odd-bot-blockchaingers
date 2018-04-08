
from bge import logic

from socket import *

import sys
def printf(format, *args):
    sys.stdout.write(format % args)
    
#Port we are listening to

port = 10000

logic.Sock = socket(AF_INET,SOCK_DGRAM)
logic.Sock.setblocking(0)

logic.Sock.bind(("",port))

printf ("binded to port = %d\n", port)



