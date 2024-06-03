#!/usr/bin/env python3
"""
Script to autonomously navigate Robot
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time


class AutonomousRobot(Node):
    def __init__(self):
        super().__init__("autonomous_robot")
        self.publisher = self.create_publisher(
            Twist, "/robot_base_controller/cmd_vel_unstamped", 10
        )
        self.subscriber = self.create_subscription(
            LaserScan, "/scan", self.lidar_callback, 10
        )
        self.cmd = Twist()
        self.safe_distance = 0.5  # Distance to avoid obstacles in meters
        self.is_obstacle_ahead = False

    def lidar_callback(self, msg):
        # Check for obstacles in front of the robot
        front_distances = msg.ranges[len(msg.ranges)//3:2*len(msg.ranges)//3]
        if min(front_distances) < self.safe_distance:
            self.is_obstacle_ahead = True
        else:
            self.is_obstacle_ahead = False

    def run(self):
        while rclpy.ok():
            if self.is_obstacle_ahead:
                self.avoid_obstacle()
            else:
                self.move_forward()
            rclpy.spin_once(self)

    def move_forward(self):
        self.cmd.linear.x = 0.5
        self.cmd.angular.z = 0.0
        self.publisher.publish(self.cmd)

    def avoid_obstacle(self):
        self.cmd.linear.x = 0.0
        self.cmd.angular.z = 0.5  # Turn in place
        self.publisher.publish(self.cmd)


def main(args=None):
    rclpy.init(args=args)
    autonomous_robot = AutonomousRobot()
    try:
        autonomous_robot.run()
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()


if __name__ == "__main__":
    main()
