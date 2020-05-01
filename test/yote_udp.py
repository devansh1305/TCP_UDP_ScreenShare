from __future__ import division
import cv2
import numpy as np
import socket
import struct
import sys

IMG_DATA_SIZE_MAX = 65536

def get_buffer(my_client):
    # Receiving all pizels
    while True:
        segment, addr = my_client.recvfrom(IMG_DATA_SIZE_MAX)
        print(segment[0])
        if struct.unpack("B", segment[0:1])[0] == 1:
            print("finish emptying buffer")
            break

if __name__ == "__main__":
    
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
    else:
        host = "127.0.0.1"
        port = 12345

    # Set up socket
    my_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_client.bind((host, port))
    data = b''
    get_buffer(my_client)

    while True:
        segment, addr = my_client.recvfrom(IMG_DATA_SIZE_MAX)
        if struct.unpack("B", segment[0:1])[0] > 1:
            data += segment[1:]
        else:
            data += segment[1:]
            img = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), 1)
            # img = np.frombuffer(data, dtype=np.uint8)
            cv2.imshow('frame', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            data = b''

    cv2.destroyAllWindows()
    my_client.close()
