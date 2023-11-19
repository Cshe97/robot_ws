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
        self.cv_img = cv2.imread("/home/cshe97/robot_ws/src/ar_track/ar_trackempty.png")

    def get_compressed(self, msg):
        #self.cv_img = cv2.imread("empty.png")
        self.cv_img = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")

def main(args=None):
    rclpy.init(args=args)
    node = LineDetector()
    try:   
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.1)
            img = node.cv_img

            frame = cv2.resize(img, dsize=(160,120), interpolation=cv2.INTER_AREA)
            
            frame = cv2.flip(frame,-1)
            crop_img =frame[60:120, 0:160]
            gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY) #이미지를 회색으로 변경
            
            
            cv2.imshow('src', frame)
            
            blur = cv2.GaussianBlur(gray, (5,5) , 0) #가우시간 블러로 블러처리를 한다.

            
            ret,thresh1 = cv2.threshold(blur, 123, 255, cv2.THRESH_BINARY_INV) #임계점 처리
            if ret == False:
                print("No Threshold")
                break    
              

            #이미지를 압축해서 노이즈를 없앤다.
            mask = cv2.erode(thresh1, None, iterations=2)  
            mask = cv2.dilate(mask, None, iterations=2)
            
            cv2.imshow('mask', mask)
            
            #이미지의 윤곽선을 검출
            contours,hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
            
            #윤곽선이 있다면, max(가장큰값)을 반환, 모멘트를 계산한다.
            if len(contours) > 0:
                c = max(contours, key=cv2.contourArea)
                M = cv2.moments(c)
                 
                #X축과 Y축의 무게중심을 구한다.
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                
               #X축의 무게중심을 출력한다.
                cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
                cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
            
                cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
                
                print("-----------")

                if cx >= 95 and cx <= 125:              
                    print("Turn Left!")
                    print(cx) #출력값을 print 한다.
                elif cx >= 39 and cx <= 65:
                    print("Turn Right")
                    print(cx) #출력값을 print 한다.
                else:
                    print("go")
                    print(cx) #출력값을 print 한다.
                    
                print("-----------")
                
                if cv2.waitKey(1) == ord('q'): #q값을 누르면 종료
                    break
        
            cv2.destroyAllWindows()
            
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt(SIGINT)')


if __name__ == '__main__':
    main()
