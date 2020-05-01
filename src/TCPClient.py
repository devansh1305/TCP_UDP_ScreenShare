from socket import  *

import sys
import cv2
import pickle
import zlib
import time
import tkinter as tk

'''

TODO STATS:

fps
latency
compression levels
udp implementation
tcp implementation
Implementations:
    - thread per client
    - list of clients
Libraries/Modules used
    - OpenCV
    - Pickle
    - zlib
    - mss
    - tkinter (screensize only)
    - numpy

'''

if len(sys.argv) < 2:
    hostname = "DESKTOP-QHVEDFE"
    port = 12345
else:
    hostname = "localhost"
    port = sys.argv[1]
    
root = tk.Tk()
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()

# create client socket
client_socket = socket(AF_INET, SOCK_STREAM)
# connect client socket to localhost with specified port
host = gethostbyname(hostname)
client_socket.connect((host, port))
# name a window and adjust it's size
cv2.namedWindow("screen", cv2.WINDOW_NORMAL)
cv2.resizeWindow("screen", int(WIDTH * 0.75), int(HEIGHT * 0.75))
try:
    # continuous loop that gets frames from the server
    while True:
        try:
            last_time = time.time()
            num = "" # used to get the number of frame bytes to read from the server
            data = client_socket.recv(1).decode()
            dump = b''
            while data != "\n": # continue reading the frame size until new line
                num += data
                data = client_socket.recv(1).decode()
            # convert frame size num into an int
            num = int(num)
            # begin reading the frame from the server
            while num > 0: 
                dump += client_socket.recv(min(100000, num))
                num -= min(100000, num)
            # deserialize the frame
            frame = pickle.loads(zlib.decompress(dump))
            # display the frame
            cv2.imshow("screen", frame)
            print("fps: {}".format(1 / (time.time() - last_time)))
            # checks if ESC is pressed. If so, then the screen sharing window will close
            if cv2.waitKey(1) == 27:
                break
        except:
            continue
except KeyboardInterrupt:
    pass
# close connection
client_socket.close()