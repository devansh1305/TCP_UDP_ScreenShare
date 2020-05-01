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

class TCPClient():

    def __init__(self, hostname, port, width = 720, height = 480):
        # create client socket
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        # connect client socket to localhost with specified port
        self.client_socket.connect((gethostbyname(hostname), port))
        self.screen_width = width
        self.screen_height = height
    
    def set_full_screen(self):
        root = tk.Tk()
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

    def resize_window(self):
        cv2.namedWindow("screen", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("screen", self.screen_width, self.screen_height)

    def run(self):
        # self.set_full_screen()
        self.resize_window()

        try:
            # continuous loop that gets frames from the server
            while True:
                try:
                    last_time = time.time()
                    num = "" # used to get the number of frame bytes to read from the server
                    data = self.client_socket.recv(1).decode()
                    dump = b''
                    while data != "\n": # continue reading the frame size until new line
                        num += data
                        data = self.client_socket.recv(1).decode()
                    # convert frame size num into an int
                    num = int(num)
                    # begin reading the frame from the server
                    while num > 0: 
                        dump += self.client_socket.recv(min(100000, num))
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
        finally:
            print("disconnected")
            self.client_socket.close()

if len(sys.argv) == 3:
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    tcp_client = TCPClient(hostname, port)
    tcp_client.run()
else:
    print("invalid arguments")
    sys.exit(1)