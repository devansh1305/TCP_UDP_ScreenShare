from socket import socket
from socket import SOL_SOCKET
from socket import SO_REUSEADDR
from threading import Thread
from zlib import compress

from mss import mss


WIDTH = 1900
HEIGHT = 1000


def retreive_screenshot(conn):
    with mss() as sct:
        # The region to capture
        rect = {'top': 0, 'left': 0, 'width': WIDTH/2, 'height': HEIGHT/2}

        while 'recording':
            # Capture the screen
            img = sct.grab(rect)
            # Tweak the compression level here (0-9)
            pixels = compress(img.rgb, 6)

            # Send the size of the pixels length
            size = len(pixels)
            size_len = (size.bit_length() + 7) // 8
            conn.send(bytes([size_len]))

            # Send the actual pixels length
            size_bytes = size.to_bytes(size_len, 'big')
            conn.send(size_bytes)

            # Send pixels
            conn.sendall(pixels)


def screen_share_tcp():
    port = 12345
    sock = socket()
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(('',port))
    try:
        sock.listen(5)
        print('Server started.')

        while 'connected':
            conn, addr = sock.accept()
            print('Client connected IP:', addr)
            thread = Thread(target=retreive_screenshot, args=(conn,))
            thread.start()
    finally:
        sock.close()

def screen_share_udp():
    return

if __name__ == '__main__':
    if sys.argv[1] == "tcp":
        screen_share_tcp()
    elif sys.argv[1] == "udp":
        screen_share_udp()
    else:
        screen_share_tcp()
    