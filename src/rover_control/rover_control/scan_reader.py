import math
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan


class ScanReader(Node):

    def __init__(self):
        super().__init__('scan_reader')
        self.subscription = self.create_subscription(
            LaserScan, 'scan', self.scan_callback, qos_profile_sensor_data)
        self.get_logger().info('scan_reader started')

    def scan_callback(self, msg):
        # Find the beam pointing straight ahead (angle = 0)
        index = round((0.0 - msg.angle_min) / msg.angle_increment)
        distance = msg.ranges[index]

        if math.isinf(distance) or math.isnan(distance):
            self.get_logger().info(
                'Front: nothing in range', throttle_duration_sec=1.0)
        else:
            self.get_logger().info(
                f'Front: {distance:.2f} m', throttle_duration_sec=1.0)


def main(args=None):
    rclpy.init(args=args)
    node = ScanReader()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()