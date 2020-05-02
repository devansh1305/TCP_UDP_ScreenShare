from __future__ import division
import numpy as np
import sys
import socket
import struct
import math
import mss
import cv2 as cv


# Class to fragment image frame into multiple segments
class FrameSegment(object):
    IMG_DATA_SIZE_MAX = 65472
    def __init__(self, sock, port = 12345, addr="127.0.0.1"):
        self.my_server = sock
        self.port = port
        self.addr = addr

    # Send the fragmented frames
    def udp_frame(self, img):
        # Compress image and Break down into data segments 
        img_compress = cv.imencode('.jpg', img)[1]
        data = img_compress.tostring()
        size_of_img = len(data)
        count = math.ceil(size_of_img/(self.IMG_DATA_SIZE_MAX))
        buf_sent = 0
        while count:
            array_pos_end = min(size_of_img, buf_sent + self.IMG_DATA_SIZE_MAX)
            # Instead of sending data to each client, we will just broadcast for better efficiency
            # This removes the need to implement threads and hence resulting in better performance
            self.my_server.sendto(
                struct.pack("B", count) + data[buf_sent:array_pos_end], 
                ('<broadcast>', self.port)
            )
            buf_sent = array_pos_end
            count -= 1


if __name__ == "__main__":
    width = 720
    height = 480

    # Set up UDP socket
    my_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    my_server.settimeout(0.2)
    
    host = ""
    port = 12345
    
    if len(sys.argv) == 2:          # - [Host]
        host = sys.argv[1]
    elif len(sys.argv) == 3:        # - [Host] [Port]
        host = sys.argv[1]          
        port = int(sys.argv[2])
    elif len(sys.argv) == 4:        # - r [Height] [Width]
        width = int(sys.argv[2])
        height = int(sys.argv[3])
    # elif len(sys.argv) == 4:
    #     host = sys.argv[1]
    #     port = int(sys.argv[2])
    #     if(sys.argv[3])=="TEST": TEST =True
    elif len(sys.argv) == 5:        # - [Host] [Port] [Height] [Width]
        host = sys.argv[1]
        port = int(sys.argv[2])
        width = int(sys.argv[3])
        height = int(sys.argv[4])
    else:
        host = ""
        port = 12345
    
    my_server.bind((host,port))
    
    with mss.mss() as sct:
        fs = FrameSegment(my_server, port, host)
        while True:
            # Get the screen capture
            # bbox specifies specific region (bbox= x,y,width,height *starts top-left)
            monitor = {"top": 0, "left": 0, "width": width, "height": height}
            frame = np.array(sct.grab(monitor))
            fs.udp_frame(frame)
    cv.destroyAllWindows()
    my_server.close()
