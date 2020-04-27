import numpy as np
import cv2
import PIL
import pyscreenshot as ImageGrab
import pickle
from socket import *

# create server socket
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', 12345))

# initiate server's ability to listen
server_socket.listen()

# function used to continuously send frames
def send_frames(connection_socket):
    try:
        while True:
            # take a screenshot of current screen
            img = ImageGrab.grab() # note the screenshot is stored as a PIL image
            # converts screenshot into a byte array
            img_np = np.array(img)
            # PIL images are color as BGR, converting the color to RGB
            frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            # serialize the frame
            data = pickle.dumps(frame)
            # send the frame size to client
            connection_socket.sendall((str(len(data)) + "\n").encode())
            # send the serialized frame to client
            connection_socket.sendall(data)
    except:
        return "ok"

# loop to continousoly accept connections
while True:
    # accept connection
    connection_socket, addr = server_socket.accept()
    # call outer func to send frames
    ret = send_frames(connection_socket)
        
# close server
server_socket.close()
