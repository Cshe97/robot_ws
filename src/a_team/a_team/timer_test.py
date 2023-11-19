import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist
import cv2
import numpy as np
from std_msgs.msg import String


finding = 0
TB_LIN_SPD = 0.1
TB_ANG_SPD = 1





#=======================================================================================
tw = Twist()

def go():
    tw.angular.z = 0.0
    tw.linear.x = 0.03
    
def stop():
    tw.angular.z = 0.0
    tw.linear.x = 0.0

def turn_left():
    tw.angular.z = 0.8
    tw.linear.x = 0.0

def turn_right():
    tw.angular.z = -0.8
    tw.linear.x = 0.0





class Servo_Control(Node):

    def __init__(self):
        super().__init__('servo_control')
        self.pub_pt = self.create_publisher(String, 'pt_msg', 10)
        self.pt_msg = String()
        self.up()
        
    def up(self):
        msg = String()
        msg.data = 'up'
        self.pub_pt.publish(msg)
        
    def down(self):
        msg = String()
        msg.data = 'down'
        self.pub_pt.publish(msg)
        
#=======================================================================================



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


#=======================================================================================
class Timer(Node):
    def __init__(self):
        super().__init__('Timer')
        #self.publisher_ = self.create_publisher(String, 'publisher', 10)
        timer_period = 1  # seconds
        self.timer    = self.create_timer(1.0, self.count_sec)
        self.cnt_sec = 0

    
    def count_sec(self):
        print("self.cnt_sec", self.cnt_sec)
        self.cnt_sec += 1
        duration = self.cnt_sec + 5
        self.get_logger().info(f'Elapsed seconds: {self.cnt_sec}')
        if self.cnt_sec <= duration:
            print("cnt_sec(go) : ", self.cnt_sec)
            print("go !")
            go()
        else:
            print("cnt_sec(stop) : ", self.cnt_sec)
            print("stop !")
            #stop()
            
    
#=======================================================================================


def main(args=None):
    rclpy.init(args=args)
    node = LineDetector()
    timer = Timer()
    servo = Servo_Control()
    #tw = Twist()
    pub = node.create_publisher(Twist, '/cmd_vel', 10)
    servo.up()
    
    try:   
        while rclpy.ok():
            print("while문 시작")
            rclpy.spin_once(node, timeout_sec=0.1)
            servo.up()
                        
            #duration = timer.cnt_sec  + 5
            #3초 카운트
            duration = timer.cnt_sec + 5
            print("현재 timer.cnt_sec : ", timer.cnt_sec)
            print("현재 timer.duration : ", duration)
            while timer.cnt_sec < duration: 
                rclpy.spin_once(timer, timeout_sec = 1.0)
                print("wait ...........  : ", duration - timer.cnt_sec + 1)
                pub.publish(tw)
                
            stop()
            print("end")
            pub.publish(tw) 
            servo.down()
            print("=================================")
            print("=================================")
            print("=================================")
            print("=================================")
            print("=================================")
                 
                        
                  
            if cv2.waitKey(1) == ord('q'):
                stop()
                pub.publish(tw)
                break
    
            cv2.destroyAllWindows()
            
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt(SIGINT)')
        stop()
        pub.publish(tw)
        
    finally:
        node.destroy_node()
        rclpy.shutdown()
            
if __name__ == '__main__':
    main()
    
    # cv2.rectangle(mask, (cx-3, cy-3), (cx+3,cv+3), (255,255,255), 1, lineType=None, shift=None)
