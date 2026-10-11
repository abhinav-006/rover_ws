import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class ObstacleAvoider(Node):

    def __init__(self):
        super().__init__('obstacle_avoider')

        # Settings, with default values
        self.declare_parameter('stop_distance', 0.5)   # meters
        self.declare_parameter('forward_speed', 0.15)  # meters per second
        self.declare_parameter('turn_speed', 0.8)      # radians per second

        # Output: speed commands. Input: lidar scans.
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.create_subscription(
            LaserScan, 'scan', self.scan_callback, qos_profile_sensor_data)

        self.get_logger().info('obstacle_avoider started')

    def closest_in_sector(self, msg, start_angle, end_angle):
        """Nearest valid distance among beams between two angles (radians)."""
        closest = float('inf')
        for i, distance in enumerate(msg.ranges):
            angle = msg.angle_min + i * msg.angle_increment
            if start_angle <= angle <= end_angle:
                if msg.range_min < distance < msg.range_max:
                    closest = min(closest, distance)
        return closest

    def scan_callback(self, msg):
        stop_distance = self.get_parameter('stop_distance').value
        forward_speed = self.get_parameter('forward_speed').value
        turn_speed = self.get_parameter('turn_speed').value

        # Angle 0 = straight ahead, positive = left, negative = right
        front = self.closest_in_sector(msg, -0.5, 0.5)
        left = self.closest_in_sector(msg, 0.5, 1.57)
        right = self.closest_in_sector(msg, -1.57, -0.5)

        cmd = Twist()
        if front < stop_distance:
            # Blocked ahead: turn toward the more open side
            cmd.angular.z = turn_speed if left > right else -turn_speed
        else:
            cmd.linear.x = forward_speed
        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoider()
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