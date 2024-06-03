#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidance(Node):

    def __init__(self):
        super().__init__('obstacle_avoidance')
        self.publisher_ = self.create_publisher(Twist, '/robot_base_controller/cmd_vel_unstamped', 10)
        self.subscription = self.create_subscription(LaserScan, 'scan', self.laser_callback, 10)
        self.cmd_msg = Twist()

    def laser_callback(self, msg):
        # Assuming the YDLidar sensor provides LaserScan messages
        ranges = msg.ranges
        min_distance = min(ranges)

        if min_distance < 0.8:  # Adjust this threshold based on your robot's specifications
            # Obstacle detected, perform raycasting to determine safe direction
            min_index = ranges.index(min_distance)
            if min_index < len(ranges) // 2:
                # Obstacle on the left, turn right
                self.cmd_msg.angular.z = -0.5
            else:
                # Obstacle on the right, turn left
                self.cmd_msg.angular.z = 0.5
        else:
            # No obstacle, move forward
            self.cmd_msg.linear.x = 0.5

        self.publisher_.publish(self.cmd_msg)
    
    def move_forward(self):
        self.cmd.linear.x = 0.5
        self.cmd.angular.z = 0.0
        self.publisher.publish(self.cmd)

def main(args=None):
    rclpy.init(args=args)
    obstacle_avoidance = ObstacleAvoidance()
    rclpy.spin(obstacle_avoidance)
    obstacle_avoidance.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()