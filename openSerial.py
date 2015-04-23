#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
import serial
import serial.tools.list_ports
import argparse
import sys


serialPort = None

webSocketHandlers = []

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
        # while True:
        #     read = serialPort.readline()
        #     print u"Read %s" % read
        #     self.write_message(read)
        #     gen.sleep(1)

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print "WebSocket closed"
        clients.remove(self)

application = tornado.web.Application([
    (r"/", SerialWebSocket),
])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--webPort", type=int, default=8888, help="Websocket port number")
    parser.add_argument("--serialPort", help="Serial device name")

    args = parser.parse_args()

    if args.serialPort == None:
        # List serial ports and exit 
        print "Serial devices:"
        for (port, description, id) in serial.tools.list_ports.comports():
            print "%s - %s - %s" % (port, description, id)
        sys.exit(0)

    # Connect to serial port
    print "Connecting to serial port %s" % args.serialPort
    global serialPort
    serialPort = serial.Serial(args.serialPort)
    serialPort.write("l")
    read = serialPort.readline()
    print "Read %s" % read
    broadcast(read)

    print "Listening on websocket port %d" % args.webPort
    application.listen(args.webPort)
    tornado.ioloop.IOLoop.instance().start()
