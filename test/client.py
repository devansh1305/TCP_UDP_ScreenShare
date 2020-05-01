import socket
import numpy as np
import cv2 as cv
import sys
import pickle
import tkinter as tk
import zlib

addr = ("127.0.0.1", 65534)
buf = 512
root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
#width = 640
#height = 480
code = b'start'
num_of_chunks = width * height * 3 / buf
#print(num_of_chunks * buf)

# if __name__ == '__main__':
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.bind(addr)
    
#     while True:
#         try:
#             chunks = []
#             start = False
#             while len(chunks) < num_of_chunks:
#                 temp = s.recvfrom(buf)
#                 #print(temp)
#                 chunk, addr = temp
#                 #chunk, _ = s.recvfrom(buf)
#                 if start:
#                     chunks.append(chunk)
#                 elif chunk.startswith(code):
#                     start = True
#             frame = pickle.loads(b''.join(chunks))
#             # frame = np.frombuffer(
#             #     byte_frame, dtype=np.uint8).reshape(height, width, 3)

#             cv.imshow('recv', frame)
#             if cv.waitKey(1) & 0xFF == ord('q'):
#                 break
#         except:
#             #print(Exception)
#             sys.exit(0)
#             pass
#     s.close()
#     cv.destroyAllWindows()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)

    chunks = []
    size, addr = s.recvfrom(512)
    print(size)
    size = int(size.decode())
    while size > 0:
        chunk, addr = s.recvfrom(buf)
        chunks.append(chunk)
        size -= 512
    frame = b''.join(chunks)
    cv.imshow('recv', pickle.loads(zlib.decompress(frame)))
    if cv.waitKey(1) == 27:
        s.close()
        cv.destroyAllWindows()
    
