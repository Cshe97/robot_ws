import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist
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
        self.cv_img = cv2.imread("empty1.png", cv2.IMREAD_COLOR)
        #self.cv_img = np.zeros([120,160])
        print("type(cv_img)", type(self.cv_img))

    def get_compressed(self, msg):
        self.cv_img = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")

def main(args=None):
    rclpy.init(args=args)
    node = LineDetector()
    tw = Twist()
    pub = node.create_publisher(Twist, '/cmd_vel', 10)
    
    try:   
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.5)
            
            
            img = node.cv_img
            
            dist = np.array([k1, k2, p1, p2, k3])
            mtx = np.array([[fx, 0, cx],
                  [0, fy, cy],
                  [0, 0, 1]])
            
            h, w = img.shape[:2]
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
            dst = cv2.undistort(image, mtx, dist, None, newcameramtx)
            x, y, w, h = roi
            dst = dst[y:y+h, x:x+w]
            cv2.imshow('result', dst)
            cv2.imshow('src', img)
            #cv2.imshow('test', img)
            if img is not None and not img.size == 0:
            #if img is not None and not np.all( img == 0):
                cv2.imshow('show', img)
                
                
                    
                if cv2.waitKey(1) == ord('q'):
                    break
    
        cv2.destroyAllWindows()
            
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt(SIGINT)')
        tw.linear.x = 0.0
        tw.angular.z = 0.0
        pub.publish(tw)
        
    finally:
        node.destroy_node()
        rclpy.shutdown()
            
if __name__ == '__main__':
    main()
    
    # cv2.rectangle(mask, (cx-3, cy-3), (cx+3,cv+3), (255,255,255), 1, lineType=None, shift=None)
