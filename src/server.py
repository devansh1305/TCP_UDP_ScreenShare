from socket import *
from threading import Thread

import numpy
import cv2
import pickle
import zlib
import mss
# import tkinter as tk

# root = tk.Tk()
WIDTH = 1000
HEIGHT = 500

clients = []

# create server socket
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', 12345))

# initiate server's ability to listen
server_socket.listen()
monitor = {"top": 0, "left": 0, "width": 900, "height": 600}
# function used to continuously send frames
def send_frames():
    try:
        # loop to continousoly accept connections
        while True:
            # take a screenshot of current screen
            frame = numpy.array(mss.mss().grab(monitor))
            # serialize the frame
            data = zlib.compress(pickle.dumps(frame), 2)
            for client in clients:
                try:
                    # send the frame size to client
                    client.sendall((str(len(data)) + "\n").encode())
                    # send the serialized frame to client
                    client.sendall(data)
                except:
                    clients.remove(client)
                    print("removed a client from list of clients")
    except:
        return
try:
    # loop to continousoly accept connections
    Thread(target=send_frames, args=()).start()
    while True:
        # accept connection
        connection_socket, addr = server_socket.accept()
        # call outer func to send frames
        clients.append(connection_socket)
        print("adding client to list of clients")
            
    # close server
except KeyboardInterrupt:
    pass
server_socket.close()
