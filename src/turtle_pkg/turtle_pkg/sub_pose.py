import rclpy, sys
from math import degrees
from rclpy.node import Node

from turtlesim.msg import Pose



class SubPose(Node):
    def __init__(self):
        super().__init__('sub_turlte_pose')
        self.pose = Pose()
        sub = self.create_subscription(Pose, '/turtle1/pose', self.print_pose, 10)
        
       
    def get_pose(self, msg):
        self.pose = msg
        #print('1x = "%s", y="%s", theta="%s"' %(msg.x, msg.y, msg.theta))
        #self.print_pose()
     
    def print_pose(self, msg):
        print('1x = "%s", y="%s", theta="%s"' %(self.pose.x, self.pose.y, self.pose.theta))
     


def main(args=None):
    rclpy.init(args=args)
    node= SubPose()
    
    while rclpy.ok():
        node.print_pose()
    
    rclpy.spin(node)
    
    node.destroy_node()
    rclpy.shutdown()
        
if __name__ == '__main__':
    main()
