#!/usr/bin/env python2

from __future__ import print_function
import psychopy.parallel
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
import argparse
import sys
import time


parallelPort = None
args = None
webSocketHandlers = []


class ParallelWebSocket(tornado.websocket.WebSocketHandler):
    instances = set()

    # Allow any origin
    def check_origin(self, origin):
        return True

    def open(self):
        print("WebSocket opened")
        webSocketHandlers.append(self)

    def on_message(self, message):
        asciiMessage = message.encode("ascii", "ignore")
        trigger = int(asciiMessage)
        print("Sending trigger: %s" % trigger)
        if not args.dryRun:
            parallelPort.setData(trigger)  # Send trigger (START / END)
            time.sleep(args.outputDuration / 1000)  # Wait for trigger to 'catch on'
            parallelPort.setData(0)  # Reset port to 0
            time.sleep(args.outputDuration / 1000)  # Wait for trigger to 'catch on'

    def on_close(self):
        print("WebSocket closed")
        webSocketHandlers.remove(self)


application = tornado.web.Application([(r"/", ParallelWebSocket),])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--webPort", type=int, default=53141, help="Websocket port number"
    )
    parser.add_argument(
        "--parallelPort", type=int, default=0x3FE8, help="Parallel port address"
    )
    parser.add_argument(
        "--outputDuration", type=int, default=10, help="Output duration (in ms)"
    )
    parser.add_argument(
        "-d", "--dryRun", action="store_true", help="Don't actually open the parallel port, just print the triggers"
    )

    args = parser.parse_args()

    if args.dryRun:
        print("WARNING: Dry run. Not opening parallel port")
    else:
        # Connect to serial port
        print("Connecting to parallel port %s" % args.parallelPort)
        parallelPort = psychopy.parallel.ParallelPort(args.parallelPort)
        parallelPort.setData(0)  # Setting initial value to 0
        time.sleep(args.outputDuration / 1000)  # Wait for trigger to 'catch on'

    try:
        print("Listening on websocket port %d" % args.webPort)
        application.listen(args.webPort)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nInterrupted by user, shutting down")
        sys.exit()
