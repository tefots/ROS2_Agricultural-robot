#!/usr/bin/python3

import math
from geographiclib.geodesic import Geodesic


def gps_to_cartesian(goal_lat, goal_long):
    """
    Finds the cartesian cordinate of the gps location with respect to the gps
    reference origin which is the same as Gazebo world origin.

    Args:
      goal_lat : Goal latitude
      goal_long : Goal longitude

    Returns:
      x : x cordinate in the sensor frame in meters
      y : y cordinate in the sensor frame in meters
    """
    
    # Origin coordinates
    origin_lat = 49.90000010022057
    origin_long = 8.900000304717647
    
    geod = Geodesic.WGS84  # define the WGS84 ellipsoid
    g = geod.Inverse(origin_lat, origin_long, goal_lat, goal_long)

    # Compute several geodesic calculations between two GPS points
    distance = g["s12"]  # Access distance
    azimuth = g["azi1"]  # Access azimuth

    # Convert polar (distance and azimuth) to x,y translation in metres
    # (needed for ROS) by finding side lengths of a right-angle triangle.
    # x, y and distance are adjacent,opposite and hypotenuse sides of a
    # right-angle triangle respectively

    # Convert azimuth to radians
    azimuth = math.radians(azimuth)
    x = math.cos(azimuth) * distance
    y = math.sin(azimuth) * distance

    y = -y

    return x, y
