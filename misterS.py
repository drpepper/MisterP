#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
import serial
import serial.tools.list_ports
import argparse
import sys
import threading


serialPort = None
shouldStop = False

webSocketHandlers = []


def read_from_serial_port():
    while not shouldStop:
        dataRead = serialPort.readline()
        broadcast(dataRead)

def broadcast(msg):
    for handler in webSocketHandlers:
        handler.write_message(msg)


class SerialWebSocket(tornado.websocket.WebSocketHandler):
    instances = set()

    # Allow any origin
    def check_origin(self, origin):
        return True

    def open(self):
        print "WebSocket opened"
        webSocketHandlers.append(self)

    def on_message(self, message):
        asciiMessage = message.encode("ascii", "ignore")
        print "Writing to serial: %s" % asciiMessage
        serialPort.write(asciiMessage)

    def on_close(self):
        print "WebSocket closed"
        webSocketHandlers.remove(self)

application = tornado.web.Application([
    (r"/", SerialWebSocket),
])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--webPort", type=int, default=53141, help="Websocket port number")
    parser.add_argument("--serialPort", help="Serial device name")
    parser.add_argument("--list", action='store_true', help="List serial devices")

    args = parser.parse_args()

    if args.list or args.serialPort == None:
        # List serial ports and exit 
        print "Serial devices:"
        for (port, description, id) in serial.tools.list_ports.comports():
            print "%s: %s (ID: %s)" % (port, description, id)
        sys.exit(0)

    # Connect to serial port
    print "Connecting to serial port %s" % args.serialPort
    serialPort = serial.Serial(args.serialPort)
    
    # Read from it in the background
    thread = threading.Thread(target=read_from_serial_port)
    thread.daemon = True # Kill thread when main thread quits
    thread.start()

    try:
        print "Listening on websocket port %d" % args.webPort
        application.listen(args.webPort)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print "\nInterrupted by user, shutting down"
        shouldStop = True
        sys.exit()
