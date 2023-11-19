import rclpy, sys
from rclpy.node import Node
from rclpy.qos import QoSProfile

from geometry_msgs.msg import Twist
from turtle_pkg.getchar import Getchar

msg = """
------------------------------------

            forward
              +---+
              | w |
          +---+---+---+
turn left | a | s | d | turn right
          +---+---+---+
           backward
           
### space for stop\n

------------------------------------
"""

MAX_LIN_SPD = 0.22
MAX_ANG_SPD = 2.84

MIN_LIN_SPD = -0.22
MIN_ANG_SPD = -2.84

LIN_SPD_STEP = 0.01
ANG_SPD_STEP = 0.1

class RemoteTB3(Node):

    def __init__(self):
        self.cnt_sec = 0
        super().__init__('remote_tb3')
        qos_profile = QoSProfile(depth=10)
        #self.pub = self.create_publisher(Twist, '/cmd_vel', qos_profile)
        self.timer    = self.create_timer(1, self.count_sec)
        #self.subscription  # prevent unused variable warning

    def get_pose(self, msg):
        self.pose = msg
        #self.get_logger().info('x = "%s", y="%s", theta="%s"' %(self.pose.x, self.pose.y, self.pose.theta))

    def count_sec(self):
        self.cnt_sec = self.cnt_sec + 1
        #print(self.cnt_sec)


def main(args=None):
    rclpy.init(args=args)
    node= RemoteTB3()
    pub = node.create_publisher(Twist, '/cmd_vel', 10)
    tw = Twist()
    kb = Getchar()
    key = ' '
    count = 0
    
    lin_spd = 0.0
    ang_spd = 0.0
    print(msg)
    try:
            
            while rclpy.ok():
                key = kb.getch()
                if key == 'w':
                    if MAX_LIN_SPD >= lin_spd + LIN_SPD_STEP:
                        tw.linear.x = lin_spd + LIN_SPD_STEP
                        lin_spd += LIN_SPD_STEP
                    else:
                        tw.linear.x = MAX_LIN_SPD
                elif key == 'x':
                    if MIN_LIN_SPD <= lin_spd - LIN_SPD_STEP:
                        tw.linear.x = lin_spd - LIN_SPD_STEP
                        lin_spd -= LIN_SPD_STEP
                    else:
                        tw.linear.x = MIN_LIN_SPD
                elif key == 'a':
                    if MAX_ANG_SPD >= ang_spd + ANG_SPD_STEP:
                        tw.angular.z = ang_spd + ANG_SPD_STEP
                        ang_spd += ANG_SPD_STEP
                    else:
                        tw.angular.z = MAX_ANG_SPD
                elif key == 'd':
                    if MIN_ANG_SPD <= ang_spd - ANG_SPD_STEP:
                        tw.angular.z = ang_spd - ANG_SPD_STEP
                        ang_spd -= ANG_SPD_STEP
                    else:
                        tw.angular.z = MIN_ANG_SPD
                elif key == 's' or key == ' ':
                    tw.linear.x = tw.angular.z = 0.0
                    lin_spd = ang_spd = 0.0
                    
                
                pub.publish(tw)
                print('linear speed = "%s"\nangular speed = "%s"' % (tw.linear.x, tw.angular.z))
                
                count = count % 15
                if count == 0:
                    print(msg)
                #rclpy.spin_once(node, timeout_sec=0.1)
            sys.exit(1)
            rclpy.spin(node)
    except KeyboardInterrupt:
        tw.linear.x = tw.angular.z = 0.0
        pub.publish(tw)
        node.get_logger().info('Keyboard Interrupt(SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()
        
if __name__ == '__main__':
    main()
