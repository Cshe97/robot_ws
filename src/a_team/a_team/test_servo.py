import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from arduino.getchar import Getchar

class PubPT_MSG(Node):

    def __init__(self):
        super().__init__('pub_led_msg')
        self.pub_pt = self.create_publisher(String, 'pt_msg', 10)
        self.pt_msg = String()
        
    def up(self):
        msg = String()
        msg.data = 'up'
        self.pub_pt.publish(msg)
        
    def down(self):
        msg = String()
        msg.data = 'down'
        self.pub_pt.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    node = PubPT_MSG()

    #rclpy.spin(node)
    try:
        kb = Getchar()
        key =''
        while rclpy.ok():
            key = kb.getch()
            if key == '1':
                node.down()
            elif key == '2':
                node.up()
            else:
                pass
    except KeyboardInterrupt:
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    
            node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()
