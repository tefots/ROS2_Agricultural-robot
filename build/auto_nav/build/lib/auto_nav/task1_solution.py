import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance')
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.twist = Twist()

    def scan_callback(self, msg):
        # Process the scan data
        min_distance = min(msg.ranges)
        if min_distance < 1.0:  # Obstacle within 1 meter
            self.avoid_obstacle()
        else:
            self.move_forward()

    def avoid_obstacle(self):
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.5  # Turn in place
        self.cmd_pub.publish(self.twist)

    def move_forward(self):
        self.twist.linear.x = 0.2  # Move forward
        self.twist.angular.z = 0.0
        self.cmd_pub.publish(self.twist)

def main(args=None):
    rclpy.init(args=args)
    obstacle_avoidance = ObstacleAvoidance()
    rclpy.spin(obstacle_avoidance)
    obstacle_avoidance.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
