import rclpy, sys
from rclpy.node import Node
from rclpy.qos import QoSProfile

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import radians, degrees


class RotateTurtle(Node):

    def __init__(self):
        self.pose = Pose()
        super().__init__('retate_turtle')
        qos_profile = QoSProfile(depth=10)
        self.create_subscription(Pose, '/turtle1/pose', self.get_pose, 10)
        
    def get_pose(self, msg):
        self.pose = msg
        #self.get_logger().info('x = "%s", y="%s", theta="%s"' %(self.pose.x, self.pose.y, self.pose.theta))
        
        def print_pose(self):
            print('1x = "%s", y="%s", theta="%s"' %(self.pose.x, self.pose.y, self.pose.theta))
    

    def count_sec(self):
        self.cnt_sec = self.cnt_sec + 1
        #print(self.cnt_sec)


def main(args=None):
    rclpy.init(args=args)
    node= RotateTurtle()
    pub = node.create_publisher(Twist, '/turtle1/cmd_vel', 10)
    tw = Twist()

    try:
            while rclpy.ok():
                rclpy.spin_once(node, timeout_sec=0.1)
                deg = int(input("input angle to rotate(degree) : "))
                
                if deg < 0:
                    dir = -1
                    print("dir : ", dir)
                else:
                    dir = 1
                    print("dir : ", dir)
                    
                current = node.pose.theta 
                goal = current + radians(deg)
                d_goal = degrees(goal)
                if d_goal > 179:
                    over_value = d_goal - 179
                    d_goal = -180 + over_value
                    print("d_goal : ", d_goal)
                print('current = "%f", goal = "%f" ' %(degrees(current) , d_goal))
                
                #print(deg)
                tw.angular.z = radians(30) * dir
                if dir < 0:
                    while goal < current:
                        rclpy.spin_once(node, timeout_sec=0.1)
                        current = node.pose.theta 
                        print('current : %f' % (degrees(current)))
                        pub.publish(tw)    
                    tw.angular.z = 0.0
                    pub.publish(tw)
                
                else:
                    while goal > current:
                        rclpy.spin_once(node, timeout_sec=0.1)
                        current = node.pose.theta
                        print('current : %f' % (degrees(current)))
                        pub.publish(tw)
                    tw.angular.z = 0.0 
                    pub.publish(tw) 
                
                #rclpy.spin_once(node, timeout_sec=0.1)
            sys.exit(1)
            rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt(SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()
        
if __name__ == '__main__':
    main()
