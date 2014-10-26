import numpy as np
import time
import multiprocessing
import requests
import json
import cv2
import socket
import sys


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
                    buf+="MAG"
                    self.client_socket.send(buf)
                
                # Check buffer
                recv_buffer = self.client_socket.recv(1024)
                delim = recv_buffer.strip()[-1:]
                if delim == "-":
                    response = recv_buffer.replace('.','').replace('-','')
                    image_processed = 1
                    recv_buffer = ""
                    return response


    def stop(self):
        self.client_socket.close()


if __name__ == '__main__':

    # Example usage

    # Get an iamge
    school_img = cv2.imread('school.jpg')

    # Open connection to server
    image_client = ImageClient('localhost',8000)
    image_client.start()

    # Stream content and get response
    #while(1):
    response = image_client.transmit(school_img)
    print response

    # Close connection to server
    image_client.stop()

