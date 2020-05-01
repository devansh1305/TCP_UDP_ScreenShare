from socket import *
import threading
import sys
import numpy
import cv2
import pickle
import zlib
import mss

LIST = 0
THREAD = 1

import tkinter as tk

class TCPServer():

    def __init__(self, port, process_type, width = 720, height = 480, compression_level = 6):
        self.clients = []
        self.type = process_type
        self.screen_width = width
        self.screen_height = height
        self.compression_level = compression_level
        self.monitor = {"top": 0, "left": 0, "width": self.screen_width, "height": self.screen_height}

        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server_socket.bind(('', port))
        self.server_socket.listen()

    def send_frames_list(self):
        try:
            while True:
                screenshot = mss.mss().grab(self.monitor)
                pixel_array = numpy.array(screenshot)
                serialized_parray = pickle.dumps(pixel_array)
                compressed_sparray = zlib.compress(serialized_parray, self.compression_level)
                size = len(compressed_sparray)
                for client in self.clients:
                    try:
                        # send the frame size to client
                        client.sendall((str(size) + "\n").encode())
                        # send the serialized frame to client
                        client.sendall(compressed_sparray)
                    except:
                        self.clients.remove(client)
                        print("removed a client from list of clients")
        finally:
            for client in self.clients:
                client.close()
            return

    def send_frames_threading(self, connection_socket):
        try:
            while True:
                screenshot = mss.mss().grab(self.monitor)
                pixel_array = numpy.array(screenshot)
                serialized_parray = pickle.dumps(pixel_array)
                compressed_sparray = zlib.compress(serialized_parray, self.compression_level)
                size = len(compressed_sparray)
                connection_socket.sendall((str(size) + "\n").encode())
                connection_socket.sendall(compressed_sparray)
        finally:
            connection_socket.close()
            print("Thread: a client has disconnected")
            return

    def get_full_screen(self):
        root = tk.Tk()
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.montior = {"top": 0, "left": 0, "width": self.screen_width, "height": self.screen_height}
        return (self.screen_width, self.screen_height)

    def run(self):
        print("Server has started...")
        # self.get_full_screen()
        if self.type == LIST:
            t = threading.Thread(target = self.send_frames_list, args = ()).start()
            try:
                while True:
                    connection_socket, addr = self.server_socket.accept()
                    self.clients.append(connection_socket)
                    print("List: adding client to list of clients")
            finally:
                self.server_socket.close()
                return
        else:
            try:
                while True:
                    connection_socket, addr = self.server_socket.accept()
                    threading.Thread(target = self.send_frames_threading, args = (connection_socket,)).start()
                    print("Thread: a client has connected")
            finally:
                self.server_socket.close()
                return
            
if __name__ == '__main__':
    if len(sys.argv) < 2:
        tcp_server = TCPServer(12345, THREAD)
        tcp_server.run()
    elif len(sys.argv) == 2:
        tcp_server = TCPServer(int(sys.argv[1]), THREAD)
        tcp_server.run()
    elif len(sys.argv) == 3 and sys.argv[1] == "TEST":
        tcp_server = TCPServer(12345, LIST, 720, 480, int(sys.argv[2]))
        tcp_server.run()
    elif len(sys.argv) == 3:
        process_type = LIST if (sys.argv[2] == "LIST") else THREAD
        tcp_server = TCPServer(int(sys.argv[1]), process_type)
        tcp_server.run()
    elif len(sys.argv) == 4:
        process_type = LIST if (sys.argv[2] == "LIST") else THREAD
        tcp_server = TCPServer(int(sys.argv[1]), process_type, 720, 480, int(sys.argv[3]))
        tcp_server.run()
    else:
        print("Invalid Arguments")
        sys.exit(1)
