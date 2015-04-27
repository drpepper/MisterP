# Mister S.

A program to connect web applications to serial devices via web sockets.


## Installation

1. Install Python 2.7
2. Install pip: `sudo easy_install pip`
3. Install tornado: `sudo pip install tornado`
4. Install pyserial: `sudo pip install pyserial`


## Running

Run `misterS.py --list` to list serial devices. Then copy the name serial port and run the program again using the `--serialPort` argument.

Here is an example session.

```
$ ./misterS.py --list
Serial devices:
/dev/cu.Bluetooth-Incoming-Port: n/a (ID: n/a)
/dev/cu.Bluetooth-Modem: n/a (ID: n/a)
/dev/cu.usbmodem1421: USB IO Board (ID: USB VID:PID=1b4f:9204 SNR=None)

$ ./misterS.py --serialPort /dev/cu.usbmodem1421
Connecting to serial port /dev/cu.usbmodem1421
Listening on websocket port 53141
```

By default, Mister S. serves web sockets on port 53141. To change the port, use the `--webPort` argument.
