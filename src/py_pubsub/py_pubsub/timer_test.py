import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'publisher', 10)
        timer_period = 1  # seconds
        self.timer    = self.create_timer(1.0, self.count_sec)
        self.cnt_sec = 0

    
    def count_sec(self):
        self.cnt_sec += 1


def main(args=None):
    rclpy.init(args=args)

    node = MinimalPublisher()
    count = 0
    while rclpy.ok():
        rclpy.spin_once(node, timeout_sec = 0.1)
        duration = 10
        
        while node.cnt_sec < duration: 
            rclpy.spin_once(node, timeout_sec = 1.0)
            print("duration - node.cnt_sec : ", duration - node.cnt_sec)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()  
