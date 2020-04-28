import cv2
import pickle
import zlib
from socket import *

# create client socket
client_socket = socket(AF_INET, SOCK_STREAM)
# connect client socket to localhost with specified port
client_socket.connect(("127.0.0.1", 12345))
# name a window and adjust it's size
cv2.namedWindow("screen", cv2.WINDOW_NORMAL)
cv2.resizeWindow("screen", 1440, 900)
try:
    # continuous loop that gets frames from the server
    while True:
        try:
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
            # checks if ESC is pressed. If so, then the screen sharing window will close
            if cv2.waitKey(1) == 27:
                break
        except:
            continue
except KeyboardInterrupt:
    pass
# close connection
client_socket.close()