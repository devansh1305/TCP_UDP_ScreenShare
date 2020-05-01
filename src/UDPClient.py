import socket
import struct
import sys
import time
import mss
import mss.tools
import zlib
import pickle
import numpy
import cv2

# import tkinter as tk
# root = tk.Tk()
# WIDTH = root.winfo_screenwidth()
# HEIGHT = root.winfo_screenheight()

# monitor = {"top": 0, "left": 0, "width": WIDTH, "height": HEIGHT}

# frame = mss.mss().grab(monitor)

# cframe = zlib.compress(pickle.dumps(frame))


# data = numpy.array(frame)
# print(len(zlib.compress(pickle.dumps(data), 9)))

# data = cv2.resize(data, (int(WIDTH * 0.75), int(HEIGHT * 0.75)))
# print(len(zlib.compress(pickle.dumps(data), 9)))

# cv2.imshow('image', data)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


message = b''
for x in range(8192):
    message += b'a'
multicast_group = ('224.3.29.71', 10000)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
sock.settimeout(0.2)

# Set the time-to-live for messages to 1 so they do not
# go past the local network segment.
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

count = 0
ack = b'ok'
try:
    # Look for responses from all recipients
    sent = sock.sendto()
    while True:
        
        data = []
        count = 0
        temp = b''
        for x in range(len(message)):
            if count == 500:
                data.append(temp)
                temp = message[x]
                continue
            temp += message[x]
        try:

            while True:
                for d in data:
                    d.
                
        except:
            continue

        # Send data to the multicast group
        print('sending {!r} - {}'.format("message", count))
        sent = sock.sendto(str(len(message)).encode(), multicast_group)
        sent = sock.sendto(message, multicast_group)
        count += 1
        print('waiting to receive')
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            print('timed out, no more responses')
            break
        else:
            print('received {!r} from {}'.format(
                data, server))
        time.sleep(0.5)

finally:
    print('closing socket')
    sock.close()