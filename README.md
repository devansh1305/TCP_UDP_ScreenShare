# cs422_final_project

A simple Server/Client implementation of a screen sharing application done with Python3. <br/>
The application works on Windows 10 and MacOS Mojave Version 10.14.6

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
`port := any available port` <br/>
`type := LIST | THREAD` <br/>
`compression_level := [1-6]` <br/>
`python3 TCPServer.py [port] [type] [compression_level]` <br/>