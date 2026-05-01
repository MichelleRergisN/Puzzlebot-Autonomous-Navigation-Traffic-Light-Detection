#!/usr/bin/env python3
import rclpy, time, math
from rclpy import qos
from rclpy.node import Node
from turtlesim.msg import Pose
from std_msgs.msg import Float32

class TurtleOdometry(Node):
	def __init__(self):
		super().__init__("odometry_node")
		self.get_logger().info("Robot pose estimated by odometry")
		self.r = 0.052
		self.L = 0.18
		self.v = 0.0
		self.w = 0.0
		self.wR = 0.0
		self.wL = 0.0
		self.rate = 100.0
		self.x, self.y, self.theta = 0.0, 0.0, 0.0
		self.pub = self.create_publisher(Pose, "/odom", 1)
		self.timer = self.create_timer(1.0/self.rate, self.callback_odometry)
		self.create_subscription(Float32, "/VelocityEncR", self.callback_wR, qos.qos_profile_sensor_data)
		self.create_subscription(Float32, "/VelocityEncL", self.callback_wL, qos.qos_profile_sensor_data)
		self.t0 = time.time()

	def callback_odometry(self):
		elapsed_time = time.time() - self.t0
		self.t0 = time.time()
		self.v = self.r * (self.wR + self.wL) / 2
		self.w = self.r * (self.wR - self.wL) / self.L
		self.x += elapsed_time * self.v * math.cos(self.theta)
		self.y += elapsed_time * self.v * math.sin(self.theta)
		self.theta += elapsed_time * self.w
		self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))
		msg = Pose()
		msg.x = self.x
		msg.y = self.y
		msg.theta = self.theta
		self.pub.publish(msg)

	def callback_wR(self, msg):
		self.wR = msg.data

	def callback_wL(self, msg):
		self.wL = msg.data

def main(args=None):
	rclpy.init(args=args)
	nodeh = TurtleOdometry()
	try:
		rclpy.spin(nodeh)
	except KeyboardInterrupt:
		print("Terminado por el usuario!!")
	finally:
		nodeh.destroy_node()
		if rclpy.ok():
			rclpy.shutdown()

if __name__ == "__main__":
	main()
