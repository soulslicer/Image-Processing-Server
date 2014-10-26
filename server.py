from ImageProcessingServer import ImageServer
import cv2
import time

def process_image1(flags, img):
    print flags
    return "DONE1"

def process_image2(flag, img):
    print flags
    return "DONE2"

# Sample code
if __name__ == '__main__':

    # Create instance of image server and attach processes to them
    image_server = ImageServer()

    # Launch a server instances
    image_server.launch_process(port=8000, func=process_image1)
    image_server.launch_process(port=8001, func=process_image2)

    # Send flags to server instances
    image_server.set_flag(port=8000, flag='test', value=0)
    image_server.set_flag(port=8000, flag='test', value=1)

    # Simulate ending of server
    time.sleep(10)
    # image_server.end_process(8000)
    # image_server.end_process(8001)
    image_server.end_all()