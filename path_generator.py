#!/usr/bin/env python3
import rclpy, math
from rclpy.node import Node
from turtlesim.msg import Pose

class PathGenerator(Node):
    def __init__(self):
        super().__init__("path_generator")

        # ── Elige UNA figura descomentando el bloque correspondiente ──

        # CUADRADO
        #self.point_list = [
        #    [2.0, 0.0],
        #    [2.0, 2.0],
        #    [0.0, 2.0],
        #    [0.0, 0.0]
        #]

        # TRIÁNGULO
        #self.point_list = [
        #     [2.0, 0.0],
        #     [1.0, 1.732],
        #     [0.0, 0.0]
        # ]

        # TRAPECIO
        self.point_list = [
             [2.0, 0.0],
             [1.5, 1.0],
             [0.5, 1.0],
             [0.0, 0.0]
         ]

        self.current_goal_idx = 0
        self.threshold = 0.1

        self.pub = self.create_publisher(Pose, "/next_point", 1)
        self.create_subscription(Pose, "/odom", self.odom_callback, 1)
        self.create_timer(0.5, self.publish_goal)

        self.get_logger().info("Generador de trayectoria iniciado.")

    def publish_goal(self):
        if self.current_goal_idx < len(self.point_list):
            msg = Pose()
            msg.x = float(self.point_list[self.current_goal_idx][0])
            msg.y = float(self.point_list[self.current_goal_idx][1])
            self.pub.publish(msg)
        else:
            self.get_logger().info("¡Trayectoria completada con éxito!", throttle_duration_sec=5.0)

    def odom_callback(self, msg):
        if self.current_goal_idx < len(self.point_list):
            target_x = self.point_list[self.current_goal_idx][0]
            target_y = self.point_list[self.current_goal_idx][1]
            distance = math.sqrt((target_x - msg.x)**2 + (target_y - msg.y)**2)
            if distance < self.threshold:
                self.get_logger().info(f"Punto {self.current_goal_idx + 1} alcanzado ({target_x}, {target_y})")
                self.current_goal_idx += 1

def main(args=None):
    rclpy.init(args=args)
    node = PathGenerator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nGenerador detenido por el usuario.")
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == "__main__":
    main()
