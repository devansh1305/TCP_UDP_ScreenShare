import cv2
import pickle
from socket import *

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(("127.0.0.1", 12345))
cv2.namedWindow("screen", cv2.WINDOW_NORMAL)
cv2.resizeWindow("screen", 1440, 900)
while True:
    num = ""
    data = client_socket.recv(1).decode()
    dump = b''
    while data != "\n":
        num += data
        data = client_socket.recv(1).decode()
    num = int(num)
    while num > 0:
        dump += client_socket.recv(min(100000, num))
        num -= min(100000, num)
    frame = pickle.loads(dump)

    cv2.imshow("screen", frame)
    if cv2.waitKey(1) == 27:
        break
client_socket.close()