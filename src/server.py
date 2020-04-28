from socket import *
from threading import Thread

import numpy
import cv2
import pickle
import zlib
import mss
import tkinter as tk

root = tk.Tk()
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()


# create server socket
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', 1234))

# initiate server's ability to listen
server_socket.listen()
monitor = {"top": 0, "left": 0, "width": 600, "height": 600}
# function used to continuously send frames
def send_frames(connection_socket):
    try:
        while True:
            # take a screenshot of current screen
            frame = numpy.array(mss.mss().grab(monitor))
            # serialize the frame
            data = zlib.compress(pickle.dumps(frame), 2)
            # send the frame size to client
            connection_socket.sendall((str(len(data)) + "\n").encode())
            # send the serialized frame to client
            connection_socket.sendall(data)
    except:
        return
try:
    # loop to continousoly accept connections
    while True:
        # accept connection
        connection_socket, addr = server_socket.accept()
        # call outer func to send frames
        Thread(target=send_frames, args=(connection_socket,)).start()
            
    # close server
except KeyboardInterrupt:
    pass
server_socket.close()
