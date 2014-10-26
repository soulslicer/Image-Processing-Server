from ImageProcessingServer import ImageClient
import cv2

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

