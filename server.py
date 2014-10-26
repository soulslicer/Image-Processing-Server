from ImageProcessingServer import ImageServer
import cv2
import time

def process_image1(img):
    #print img
    return "DONE1"

def process_image2(img):
    #print img
    return "DONE2"

# Sample code
if __name__ == '__main__':

    # Create instance of image server and attach processes to them
    image_server = ImageServer()
    image_server.launch_process(port=8000, func=process_image2)

    # Sample code to control processes
    while(1):
        time.sleep(20)
        image_server.end_process(8000)
        #time.sleep(5)
        #image_server.launch_process(port=8000, func=process_image1)
