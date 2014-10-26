import numpy as np
import time
import multiprocessing
import requests
import json
import cv2
import socket
import sys
import time
from thread import *

# Instance to make connection to server
class ImageClient(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def transmit(self, img):

        recv_buffer = ""
        image_processed = 1

        while(1):
            if img != None:

                # Image has finished processing
                if image_processed == 1:
                    image_processed = 0

                    buf = cv2.imencode( '.jpg', img )[1].tostring()
                    buf+="ACK"
                    self.client_socket.send(buf)
                
                # Check buffer
                recv_buffer = self.client_socket.recv(1024)
                delim = recv_buffer.strip()[-3:]
                if delim == "ACK":
                    response = recv_buffer.replace('ACK','')
                    image_processed = 1
                    recv_buffer = ""
                    return response


    def stop(self):
        self.client_socket.close()

# Instance of image process manages external connections
class ImageProcess(object):

    def __init__(self, host, port, func, ns):
        self.host = host
        self.port = port
        self.func = func
        self.ns = ns
        self.s = None

    # Starts socket server
    def start(self):

        # Attempt to bind the socket to this process
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((self.host, self.port))
        except socket.error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
        self.s.listen(10)
        print 'Listening at port ' + str(self.port)

        # Start thread that checks for flags
        start_new_thread(self.flag_thread ,())

        print "---------------------------------------"
        print "   ++ SERVER CREATED AT PORT " + str(self.port) + " ++"
        print "---------------------------------------"

        # Poll and listen for connections
        while(1):
            try:
                conn, addr = self.s.accept()
                conn.settimeout(5)
                print 'Connected with ' + addr[0] + ':' + str(addr[1])
                start_new_thread(self.thread_process ,(conn,))
            except Exception, e:
                if str(e) == "[Errno 9] Bad file descriptor":
                    print 'Killed at ' + str(self.port)
                    break
                else:
                    print str(e)

    # This thread runs and checks for flags
    def flag_thread(self):
        while(1):
            time.sleep(0.5)
            running = self.ns.flags[self.port]['running']
            if running == 0:
                print 'Stopping at ' + str(self.port)
                self.s.close()
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((self.host, self.port))
                break

    # Launches all new connections to this process and executes function on that image
    def thread_process(self, conn):

        data = ""

        #infinite loop so that function do not terminate and thread do not end.
        while True:
             
            #Receiving from client
            data += conn.recv(1024)
            reply = '.'
            if not data: 
                break
         
            conn.sendall(reply)
            
            if data.strip()[-3:] == "ACK":
                print "RECEIVED FULL"
                data = data.strip()[:-3]
                nparr = np.fromstring(data, np.uint8)
                img = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)

                response = self.func(self.ns.flags[self.port], img)

                data = ""
                conn.sendall(response+"ACK")
         
        #came out of loop
        conn.close()

    # Static method for starting an instance of image server
    @staticmethod
    def process(ns, port, func):
        image_process = ImageProcess('', port, func, ns)
        image_process.start()
        print "---------------------------------------"
        print "   -- SERVER REMOVED AT PORT " + str(port) + " --"
        print "---------------------------------------"

# Instance of image server manages all image processes
class ImageServer(object):

    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.ns = self.manager.Namespace()

        self.ns.flags = {}
        self.processes = {}

        # Launch a command process

    def set_flag(self, port, flag, value):
        clone = self.ns.flags
        if port in clone.keys():
            clone[port][flag] = value
        else:
            clone[port] = {flag:value}
        self.ns.flags = clone

    def port_open(self, port):
        if port in self.ns.flags.keys():
            return 1
        else:
            return 0

    def remove_port_flag(self, port):
        clone = self.ns.flags
        if port in clone.keys():
            del clone[port]
        self.ns.flags = clone

    def launch_process(self, port, func):

        # Check if port exists
        if self.port_open(port) == 1:
            print 'Error: Server at ' + str(port) + ' is already open!'
            return

        # Create new Server with function
        self.set_flag(port,'running',1)
        process = multiprocessing.Process(target=ImageProcess.process, args=(self.ns,port,func,))
        process.start()
        self.processes[port] = process

    def end_process(self, port):

        # Check if port doesn't exist
        if self.port_open(port) == 0:
            print 'Error: Server at ' + str(port) + ' is not open!'
            return

        # Destroy server
        self.set_flag(port,'running',0)
        self.processes[port].join()
        del self.processes[port]
        self.remove_port_flag(port)

    def end_all(self):
        ports = self.ns.flags.keys()
        for port in ports:
            self.end_process(port)