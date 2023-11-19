import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from rclpy.action import ActionClient
from action_msgs.msg import GoalStatus
from nav2_msgs.action import FollowWaypoints

class ClientFollowPoints(Node):
    def __init__(self):
        super().__init__('client_follow_points')
        self._client = ActionClient(self, FollowWaypoints, '/FollowWaypoints')

        self.subscription = self.create_subscription(String, '/nav_msg', self.get_nav_msg, 10)
        self.nav_msg = String()

    def send_points(self, goal_msg):
        self._client.wait_for_server()
        self._send_goal_future = self._client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def get_nav_msg(self, msg):
        self.nav_msg = msg
        if self.nav_msg.data == "point1":
            goal_msg = FollowWaypoints.Goal() 
            rgoal1 = PoseStamped()
            rgoal1.header.frame_id = "map"
            rgoal1.header.stamp.sec = 0
            rgoal1.header.stamp.nanosec = 0
            rgoal1.pose.position.z = 0.0
            rgoal1.pose.position.x = 0.5
            rgoal1.pose.position.y = -1.4
            rgoal1.pose.orientation.w = 1.0
            goal_msg.poses = [rgoal1]
            self.send_points(goal_msg)
            
        elif self.nav_msg.data == "point2":
            goal_msg = FollowWaypoints.Goal()  
            rgoal2 = PoseStamped()
            rgoal2.header.frame_id = "map"
            rgoal2.header.stamp.sec = 0
            rgoal2.header.stamp.nanosec = 0
            rgoal2.pose.position.z = 0.0
            rgoal2.pose.position.x = -0.25
            rgoal2.pose.position.y = 1.2
            rgoal2.pose.orientation.w = 1.0
            goal_msg.poses = [rgoal2]
            self.send_points(goal_msg)
            
        elif self.nav_msg.data == "point3":
            goal_msg = FollowWaypoints.Goal()  
            rgoal3 = PoseStamped()
            rgoal3.header.frame_id = "map"
            rgoal3.header.stamp.sec = 0
            rgoal3.header.stamp.nanosec = 0
            rgoal3.pose.position.z = 0.0
            rgoal3.pose.position.x = -4.0
            rgoal3.pose.position.y = -1.8
            rgoal3.pose.orientation.w = 1.0
            goal_msg.poses = [rgoal3]
            self.send_points(goal_msg)
            
        elif self.nav_msg.data == "point4":
            goal_msg = FollowWaypoints.Goal()  
            rgoal4 = PoseStamped()
            rgoal4.header.frame_id = "map"
            rgoal4.header.stamp.sec = 0
            rgoal4.header.stamp.nanosec = 0
            rgoal4.pose.position.z = 0.0
            rgoal4.pose.position.x = -3.8
            rgoal4.pose.position.y = 0.88
            rgoal4.pose.orientation.w = 1.0
            goal_msg.poses = [rgoal4]
            self.send_points(goal_msg)
       

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.missed_waypoints))

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.current_waypoint))

def main(args=None):
    rclpy.init(args=args)
    follow_points_client = ClientFollowPoints()
    print('client inited')
    rclpy.spin(follow_points_client)

if __name__ == 'main':
    main()
