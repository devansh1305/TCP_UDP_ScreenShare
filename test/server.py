import socket
from threading import Thread
import sys
import numpy
import pickle
import zlib
import mss
import numpy as np
import cv2 as cv
import tkinter as tk

addr = ("127.0.0.1", 65534)
buf = 512
#cap = cv.VideoCapture(0)
root = tk.Tk()
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
monitor = {"top": 0, "left": 0, "width": WIDTH, "height": HEIGHT}

#print(cap)

#cap.set(3, width)
#cap.set(4, height)
#code = ('start' + (buf - len(code)) * 'a').encode('utf-8')


# if __name__ == '__main__':
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     while(True):
#         #ret, frame = cap.read()
#         frame = numpy.array(mss.mss().grab(monitor))
#         if True:
#             s.sendto(code, addr)
#             data = pickle.dumps(frame)
#             print(len(data))
#             for i in range(0, len(data), buf):
#                 s.sendto(data[i:i+buf], addr)
#             #cv.imshow('send', frame)
#             # if cv.waitKey(1) & 0xFF == ord('q'):
#                 # break
#         else:
#             break
    # s.close()
    # cap.release()
    # cv.destroyAllWindows()

# code = ''

# for x in range(10000):
#     code += chr(65 + (x % 26))

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    frame = numpy.array(mss.mss().grab(monitor))
    sframe = pickle.dumps(frame)
    csframe = zlib.compress(sframe)

    print(len(csframe))

    buf = 512
    t = str((len(csframe)))
    print(t.encode())
    s.sendto(t.encode(), addr)

    while(True):
        for x in range(0, len(csframe), buf):
            s.sendto(csframe[x: x+buf], addr)
            