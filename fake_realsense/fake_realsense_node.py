#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from sensor_msgs.msg import  CameraInfo
from foundation_pose_interfaces.srv import Registration

from cv_bridge import CvBridge
import cv2
import os
import glob

import numpy as np

import matplotlib.pyplot as plt

from pynput import keyboard  # For handling key presses


class FakeRealsenseNode(Node):
  def __init__(self,):
    super().__init__('FakeRealsense')
    self.get_logger().info('FakeRealsense is Up! ')
    self.frame_rate = 60 # FPS
    self.downscale = 1


    # timer callbacks
    self._timer = self.create_timer(1.0 / self.frame_rate, self.timer_callback)

    # publishers
    self.rgb_pub =  self.create_publisher(Image, '/camera/camera/color/image_raw', 10)
    self.depth_pub =  self.create_publisher(Image, '/camera/camera/aligned_depth_to_color/image_raw', 10)
    self.camera_info_pub =  self.create_publisher(CameraInfo, '/camera/camera/depth/camera_info', 10)

    # images
    self.bridge = CvBridge()
    code_dir = os.path.dirname(os.path.realpath(__file__))
    self.test_scene_dir = f'{code_dir}/demo_data/mustard0'

    self.rgb_counter = 0

    self.id_strs = []
    self.rgbs = sorted(glob.glob(f"{self.test_scene_dir}/rgb/*.png"))
    self.depths = sorted(glob.glob(f"{self.test_scene_dir}/depth/*.png"))

    for color_file in self.rgbs:
      id_str = os.path.basename(color_file).replace('.png','')
      self.id_strs.append(id_str)


    print(f"self.rgbs[0]::{self.rgbs[0]}")
    print(f"self.id_strs[0]::{self.id_strs[0]}")

    self.rgb_count = len(self.rgbs)-1


    # Start listening for key presses
    self.listener = keyboard.Listener(on_press=self.on_key_press)
    self.listener.start()

  def on_key_press(self, key):
      try:
          if key == keyboard.Key.right:
              self.rgb_counter = (self.rgb_counter + 1) % len(self.rgbs)
              self.get_logger().info(f"Right arrow pressed. rgb_counter: {self.rgb_counter}")
          elif key == keyboard.Key.left:
              self.rgb_counter = (self.rgb_counter - 1) % len(self.rgbs)
              self.get_logger().info(f"Left arrow pressed. rgb_counter: {self.rgb_counter}")
      except Exception as e:
          self.get_logger().error(f"Error handling key press: {e}")

  # timer callbacks
  def timer_callback(self):
    self.depth_pub.publish(self.get_depth())
    self.rgb_pub.publish(self.get_color())
    self.camera_info_pub.publish(self.get_camera_info())

  # uitility
  def get_color(self):
    color = cv2.imread(self.rgbs[self.rgb_counter], cv2.IMREAD_COLOR)

    self.H,self.W = color.shape[:2]
    self.H = int(self.H*self.downscale)
    self.W = int(self.W*self.downscale)
    color = cv2.resize(color, (self.W,self.H), interpolation=cv2.INTER_NEAREST)

    msg =  self.bridge.cv2_to_imgmsg(color, encoding="bgr8")
    msg.header.frame_id = self.id_strs[self.rgb_counter]

    return msg

  def get_depth(self):
    # depth = None
    # if self.depths[self.rgb_counter] == 0:
    #   depth = cv2.imread(self.depths[self.rgb_counter], -1)/1e3
    #   depth[(depth<0.001) | (depth>=np.inf)] = 0
    # else:
    depth = cv2.imread(self.depths[self.rgb_counter], -1)
    msg =  self.bridge.cv2_to_imgmsg(depth, encoding="passthrough")

    msg.header.frame_id = self.id_strs[self.rgb_counter]
    return msg

  def get_camera_info(self):
    msg = CameraInfo()

    msg.k = [ 3.195820007324218750e+02, 0.000000000000000000e+00, 3.202149847676955687e+02,
              0.000000000000000000e+00, 4.171186828613281250e+02, 2.443486680871046701e+02,
              0.000000000000000000e+00, 0.000000000000000000e+00, 1.000000000000000000e+00
    ]

    return msg

def main(args=None):
    rclpy.init(args=args)

    node = FakeRealsenseNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Node stopped by user.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
  main()