import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
import cv2
import numpy as np

class LineDetector(Node):

    def __init__(self):
        super().__init__('img_convert')
        qos_profile = QoSProfile(depth=10)

        self.subscription = self.create_subscription(CompressedImage, 
                'camera/image/compressed', 
                self.get_compressed, 
                10)
        self.bridge = CvBridge()
        self.cv_img = cv2.imread("empty.png",cv2.IMREAD_UNCHANGED)

    def get_compressed(self, msg):
        self.cv_img = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")

def main(args=None):
    rclpy.init(args=args)
    node = LineDetector()
    try:   
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.1)
            img = node.cv_img
            frame = img
            frame = cv2.resize(img, (160,120))
            frame = cv2.flip(frame,-1)
            cv2.imshow( 'normal' , frame)
            crop_img =frame[60:120, 0:160]
            gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5,5) , 0)
            ret,thresh1 = cv2.threshold(blur, 123, 255, cv2.THRESH_BINARY_INV)
            mask = cv2.erode(thresh1, None, iterations=2)  
            mask = cv2.dilate(mask, None, iterations=2)
            cv2.imshow('mask',mask)
            contours,hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
            if len(contours) > 0:
                c = max(contours, key=cv2.contourArea)
                M = cv2.moments(c)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                
                cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
                cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
                cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
                print(cx) 
                
                if cx >= 95 and cx <= 125:              
                    print("Turn Left!")
                    
                elif cx >= 39 and cx <= 65:
                    print("Turn Right")
                else:
                    print("go")
                
            if cv2.waitKey(1) == ord('q'):
                break
    
        cv2.destroyAllWindows()
            
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt(SIGINT)')
        
    finally:
        node.destroy_node()
        rclpy.shutdown()
            
if __name__ == '__main__':
    main()
