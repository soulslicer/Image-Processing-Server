Image-Processing-Server
=======================

Created this for socket based image processing. Easily create multi process image processing servers and pass a processing function in

1. Client

  ````python
  from ImageProcessingServer import ImageClient
  import cv2
  
  # Get an iamge
  school_img = cv2.imread('school.jpg')

  # Open connection to server
  image_client = ImageClient('localhost',8000)
  image_client.start()

  # Stream content and get response
  response = image_client.transmit(school_img)
  print response

  # Close connection to server
  image_client.stop()
  ````
2. Server

  ````python
  from ImageProcessingServer import ImageServer
  import cv2
  
  def process_image1(flags, img):
    print flags
    return "DONE1"

  def process_image2(flag, img):
    print flags
    return "DONE2"

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
  ````

