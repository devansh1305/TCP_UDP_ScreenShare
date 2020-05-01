from socket import  *

import sys
import cv2
import pickle
import zlib
import time
import tkinter as tk
import numpy



# TEST = False # used for collecting data
# client_count = 0 # used for collecting data
# fps_count = 0 # used for collecting data
# fps = [] # used for collecting data


class TCPClient():

    def __init__(self, hostname, port, full_screen):
        # create client socket
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        # connect client socket to localhost with specified port
        self.client_socket.connect((gethostbyname(hostname), port))
        self.screen_width = 720
        self.screen_height = 480
        self.full_screen = (full_screen == 1)

    def set_full_screen(self):
        # get screen size
        root = tk.Tk()
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

    def resize_window(self):
        # resize the window that will show the screen sharing
        cv2.namedWindow("screen", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("screen", self.screen_width, self.screen_height)

    def run(self):
        # global client_count, fps_count, fps
        if self.full_screen:
            self.set_full_screen()
        self.resize_window()
        # f = ""
        # if TEST:
        #     # f = open("../data/tcp/tcp_client_{}.txt".format(client_count), "w")
        #     client_count += 1
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
                    print("{}".format(1 / (time.time() - last_time)))
                    # if TEST:
                    #     if fps_count == 20:
                    #         f.write(numpy.average(fps))
                    #         fps_count = 0
                    #         fps.clear()
                    #     else:
                    #         fps.append(1 / (time.time() - last_time))
                    #         fps_count += 1

                    # checks if ESC is pressed. If so, then the screen sharing window will close
                    if cv2.waitKey(1) == 27:
                        break
                except:
                    continue
        finally:
            print("disconnected")
            self.client_socket.close()
        # if TEST:
            # f.close()
if len(sys.argv) == 4:
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    full_screen = int(sys.argv[3])
    tcp_client = TCPClient(hostname, port, full_screen)
    tcp_client.run()
elif len(sys.argv) == 2 and sys.argv[1] == "TEST":
    TEST = False
    hostname = ""
    port = 12345
    tcp_client0 = TCPClient(hostname, port).run()
    # tcp_client1 = TCPClient(hostname, port).run()
    # tcp_client2 = TCPClient(hostname, port).run()
    # tcp_client3 = TCPClient(hostname, port).run()
    # tcp_client4 = TCPClient(hostname, port).run()
else:
    print("invalid arguments")
    sys.exit(1)