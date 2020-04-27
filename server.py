import numpy as np
import cv2
import PIL
import pyscreenshot as ImageGrab
import pickle
from socket import *

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', 12345))

server_socket.listen()

def send_frames(connection_socket):
    try:
        while True:
            img = ImageGrab.grab()
            img_np = np.array(img)

            frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            data = pickle.dumps(frame)
            connection_socket.sendall((str(len(data)) + "\n").encode())
            connection_socket.sendall(data)
    except:
        return "ok"

while True:
    connection_socket, addr = server_socket.accept()
    ret = send_frames(connection_socket)
        

server_socket.close()
