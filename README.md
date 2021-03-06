# TCP_UDP_ScreenShare

A simple Server/Client implementation of a screen sharing application done with Python3. <br/>
The TCP/UDP application works on Windows 10 and TCP application works on MacOS Mojave Version 10.14.6. <br/>
**Please note that there may still be some bugs with one to many connections as this is still under development** <br/>

## Requirements
- OpenCv
- Mss
- Numpy
- Tkinter
- Pickle
- Zlib

You can install the requirements with the following command: <br/>
`pip3 install -r requirements.txt`

## Execution Arguments

You will need to get the hostname of your computer. You can do this by executing the following command in a Windows/MacOS terminal. <br/>
`hostname`

- TCPServer.py <br/>
    - The default port assigned is `12345`
    - The default type assigned is `THREAD`
    - The default compression_level assigned is `1`
    - The default screen capture resolution is `720 x 480`
    - The default full screen option assigned is `0` (no full screen). <br/>
`port := any available port` <br/>
`type := LIST | THREAD` <br/>
`compression_level := [1-6]` <br/>
`full_screen := 0 | 1` <br/> <br/>
`python3 TCPServer.py` <br/>
`python3 TCPServer.py port type` <br/>
`python3 TCPServer.py port type compression_level` <br/>
`python3 TCPServer.py port type compression_level full_screen` <br/>
- TCPClient.py <br/>
    - There are no default assignments. You need to pass the hostname and port as arguments. <br/> <br/>
`python3 TCPClient.py hostname port`

- UDPServer.py <br/>
    - The default port assigned is `12345`
    - The default screen capture resolution is `720 x 480` <br/>
`port := any available port` <br/>\
Available Commands <br/>
`python3 UDPServer.py` <br/>
`python3 UDPServer.py [port]` <br/>
`python3 UDPServer.py [host] [port]` <br/>
`python3 UDPServer.py r [width] [height]` <br/>
`python3 UDPServer.py [host] [port] [width] [height]` <br/>

- UDPClient.py <br/>
`python3 UDPClient.py` <br/>
`python3 UDPClient.py [host]` <br/>
`python3 UDPClient.py [host] [port]` <br/>
    
