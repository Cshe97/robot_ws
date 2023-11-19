import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry



class SubOdom(Node):

    def __init__(self):
        super().__init__('odometry_subscriber')
        self.sub = self.create_subscription(Odometry, '/odom', self.get_odom, 10)
        self.odom = Odometry()
        #self.subscription  # prevent unused variable warning

    def get_odom(self, msg):
        self.odom = msg
        print("position.x", self.odom.pose.pose.position.x)


def main(args=None):
    rclpy.init(args=args)

    node = SubOdom()

    rclpy.spin(node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
