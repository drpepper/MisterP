# Mister P.

A program to connect web applications to parallel port via web sockets.

The parallel port communication only works on Windows.

Based on [Mister S.](https://github.com/CyberCRI/MisterS), the same idea using the serial port.


## Installation

1. Clone or download this repository
2. Install Python 3
3. Using pip, install: 
  - tornado
  - psychopy


## Running

Run `misterP.py` to run. You can set the parallel port address with the `--parallelPort` option.

By default, Mister P. serves web sockets on port 53141. To change the port, use the `--webPort` argument.

The parallel port communication only works on Windows. However, you can test it on any platform by using the `-d` or `--dryRun` option to see what triggers will be sent out.


## Development

The Python code is auto-formatted using [black](https://github.com/psf/black).