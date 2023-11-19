import rclpy 
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import sys
import cv2
import math
import cv2 as cv
import numpy as np
 
class ImageConvertor(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.subscription = self.create_subscription(
      Image, 
      '/image_raw', 
      self.get_img_cb, 
      10)
        self.img_pub = self.create_publisher(Image, 'image_gray', 10)
        self.subscription # prevent unused variable warning
      
    # Used to convert between ROS and OpenCV images
        self.bridge = CvBridge()
   
    def get_img_cb(self, msg):
    #self.get_logger().info('---')
 
        cv_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        cap = cv2.VideoCapture(0)

        while (True):
            ret, src = cap.read()
            #src = cv2.resize(src, (640, 480))
            dst = cv.Canny(src, 250, 254, None, 3)
            cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
            cdstP = np.copy(cdst)
            
            lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
            if lines is not None:
                for i in range(0, len(lines)):
                    rho = lines[i][0][0]
                    theta = lines[i][0][1]
                    a = math.cos(theta)
                    b = math.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
                    pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
                    cv.line(cdst, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)

            linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)

            if linesP is not None:
                for i in range(0, len(linesP)):
                    l = linesP[i][0]
                    cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv.LINE_AA)

            result = cv2.addWeighted(src, 1, cdstP, 0.8, 0)
            
            cv.imshow("Source", src)
            cv.imshow("Standard Hough Line Transform", cdst)
            cv.imshow("Probabilistic Line Transform", cdstP)
            cv.imshow("Result", result)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        img_msg = self.bridge.cv2_to_imgmsg(img_gray)
        self.img_pub.publish(img_msg)
def main(args=None):
  
  # Initialize the rclpy library
    rclpy.init(args=args)
  
  # Create the node
    node = ImageConvertor()
  
  # Spin the node so the callback function is called.
    rclpy.spin(node)
  
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
    image_subscriber.destroy_node()
  
  # Shutdown the ROS client library for Python
    rclpy.shutdown()
  
if __name__ == '__main__':
    main()
