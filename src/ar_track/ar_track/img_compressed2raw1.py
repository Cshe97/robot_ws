import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
import cv2
import numpy as np

class ImageCovertor(Node):

    def __init__(self):
        super().__init__('img_convert')
        qos_profile = QoSProfile(depth=10)

        self.subscription = self.create_subscription(CompressedImage, 
                'camera/image/compressed', 
                self.get_compressed, 
                10)

        self.pub_img = self.create_publisher(Image, 'image_raw', qos_profile)
        self.bridge = CvBridge()
        self.cv_img = cv2.imread("empty.png",cv2.IMREAD_UNCHANGED)

    def get_compressed(self, msg):
        self.cv_img = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
        
        #self.img_msg = self.bridge.cv2_to_imgmsg(self.cv_img)#, "bgr8")
        #self.pub_img.publish(self.img_msg)

def main(args=None):
    rclpy.init(args=args)
    node = ImageCovertor()
    try:
        while rclpy.ok():
            print("start publish image_raw...") 
            rclpy.spin_once(node, timeout_sec = 0.1)
            image = node.cv_img
            if image is not None and image.size[0] > 0 and image.size[1] > 0:
                cv2.imshow('Image', image)

     
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt(SIGINT)')
        print("finish publish image_raw...") 


if __name__ == '__main__':
    main()
