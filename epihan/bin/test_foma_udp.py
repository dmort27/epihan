#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import socket

import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 6062)
message = u'你'

try:

    # Send data
    print >>sys.stderr, u'sending "%s"'.encode('utf-8') % message
    sent = sock.sendto(message.encode('utf-8'), server_address)

    # Receive response
    print >>sys.stderr, u'waiting to receive'.encode('utf-8')
    data, server = sock.recvfrom(6062)
    print >>sys.stderr, u'received "%s"'.encode('utf-8') % data

finally:
    print >>sys.stderr, u'closing socket'.encode('utf-8')
    sock.close()
