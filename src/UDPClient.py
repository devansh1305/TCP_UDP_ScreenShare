from __future__ import division
import cv2
import numpy as np
import socket
import struct
import sys
import time

IMG_DATA_SIZE_MAX = 65536

def align_buffer(my_client):
    # Receiving all pizels
    while True:
        segment, addr = my_client.recvfrom(IMG_DATA_SIZE_MAX)
        print(segment[0])
        if struct.unpack("B", segment[0:1])[0] == 1:
            print("finish emptying buffer")
            break

if __name__ == "__main__":
    TEST = False
    client_count = 0
    fps_count = 0
    fps = []

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
    align_buffer(my_client)
    f = ""
    if TEST:
        # f = open("../data/tcp/tcp_client_{}.txt".format(client_count), "w")
        client_count += 1
    while True:
        last_time = time.time()
        segment, addr = my_client.recvfrom(IMG_DATA_SIZE_MAX)
        if struct.unpack("B", segment[0:1])[0] > 1:
            data += segment[1:]
        else:
            data += segment[1:]
            img = cv2.imdecode(np.fromstring(data, dtype=np.uint8), 1)
            # img = np.frombuffer(data, dtype=np.uint8)
            cv2.imshow('frame', img)
            print("{}".format(1 / (time.time() - last_time)))
            if TEST:
                if fps_count == 20:
                    f.write(np.average(fps))
                    fps_count = 0
                    fps.clear()
                else:
                    fps.append(1 / (time.time() - last_time))
                    fps_count += 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            data = b''
    # if TEST:
            # f.close()
    cv2.destroyAllWindows()
    my_client.close()
