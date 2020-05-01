from socket import *
import threading
import sys
import numpy
import cv2
import pickle
import zlib
import mss
import tkinter as tk


LIST = 0
THREAD = 1


class TCPServer():

    # constructor
    def __init__(self, port, process_type, width = 720, height = 480, compression_level = 6):
        self.clients = []
        self.type = process_type # process type is used for choosing which implementation (LIST or THREAD)
        self.screen_width = width # width the of screen capture
        self.screen_height = height # height of screen capture
        self.compression_level = compression_level # compression level
        # draw a capture screen
        self.monitor = {"top": 0, "left": 0, "width": self.screen_width, "height": self.screen_height}

        # establish the server socket
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server_socket.bind(('', port))
        self.server_socket.listen()

    # function used to send frames with the LIST implementation
    def send_frames_list(self):
        try:
            while True:
                screenshot = mss.mss().grab(self.monitor) # grab screenshot from screen
                pixel_array = numpy.array(screenshot) # convert screenshot into pixel array
                serialized_parray = pickle.dumps(pixel_array) # serialize pixel array to bytes
                compressed_sparray = zlib.compress(serialized_parray, self.compression_level) # compress data
                size = len(compressed_sparray) # size of compressed data
                # send the compressed data to all the clients
                for client in self.clients:
                    try:
                        # send the frame size to client
                        client.sendall((str(size) + "\n").encode())
                        # send the serialized frame to client
                        client.sendall(compressed_sparray)
                    except:
                        # remove the client when error raises (usually client disconnected)
                        self.clients.remove(client)
                        print("removed a client from list of clients")
        finally:
            # close all clients
            for client in self.clients:
                client.close()
            return

    # function used to send frames with the THREAD implementation
    def send_frames_threading(self, connection_socket):
        try:
            while True:
                screenshot = mss.mss().grab(self.monitor) # grab screenshot from screen 
                pixel_array = numpy.array(screenshot) # convert screenshot into pixel array
                serialized_parray = pickle.dumps(pixel_array) # serialize pixel array to bytes
                compressed_sparray = zlib.compress(serialized_parray, self.compression_level) # compress data
                size = len(compressed_sparray) # size of compress data
                connection_socket.sendall((str(size) + "\n").encode()) # send size to client 
                connection_socket.sendall(compressed_sparray) # send compressed data
        finally:
            connection_socket.close() # close socket
            print("Thread: a client has disconnected")
            return

    def get_full_screen(self):
        # get full screen capture
        root = tk.Tk()
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.montior = {"top": 0, "left": 0, "width": self.screen_width, "height": self.screen_height}
        return (self.screen_width, self.screen_height)

    def run(self):
        print("Server has started...")
        # self.get_full_screen()

        # LIST implementation
        if self.type == LIST:
            # create thread to continously send frames to client in background
            t = threading.Thread(target = self.send_frames_list, args = ()).start()
            try:
                # server continuously accept clients
                while True:
                    connection_socket, addr = self.server_socket.accept()
                    self.clients.append(connection_socket) # add client to server
                    print("List: adding client to list of clients")
            finally:
                self.server_socket.close() # close server
                return
        else:
            try:
                # server continuously accept clients
                while True:
                    connection_socket, addr = self.server_socket.accept()
                    # create and start thread for each client
                    threading.Thread(target = self.send_frames_threading, args = (connection_socket,)).start()
                    print("Thread: a client has connected")
            finally:
                self.server_socket.close() # close server
                return
            
# arguments for specifying implementation, port and compression type
# please refer to the README.md

if __name__ == '__main__':
    tcp_server = ""
    if len(sys.argv) < 2:
        tcp_server = TCPServer(12345, THREAD)
    elif len(sys.argv) == 2:
        tcp_server = TCPServer(int(sys.argv[1]), THREAD)
    elif len(sys.argv) == 3 and sys.argv[1] == "TEST":
        tcp_server = TCPServer(12345, LIST, 720, 480, int(sys.argv[2]))
    elif len(sys.argv) == 3:
        process_type = LIST if (sys.argv[2] == "LIST") else THREAD
        tcp_server = TCPServer(int(sys.argv[1]), process_type)
    elif len(sys.argv) == 4:
        process_type = LIST if (sys.argv[2] == "LIST") else THREAD
        tcp_server = TCPServer(int(sys.argv[1]), process_type, 720, 480, int(sys.argv[3]))
    else:
        print("Invalid Arguments")
        sys.exit(1)
    tcp_server.run()
