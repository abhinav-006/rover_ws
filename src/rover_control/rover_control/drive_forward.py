import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class DriveForward(Node):

    def __init__(self):
        super().__init__('drive_forward')

        # Publisher: message type, topic name, queue size
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        # Timer: call timer_callback every 0.1 seconds (10 times a second)
        self.timer = self.create_timer(0.1, self.timer_callback)

        self.start_time = self.get_clock().now()
        self.get_logger().info('drive_forward started')

    def timer_callback(self):
        elapsed = (self.get_clock().now() - self.start_time).nanoseconds / 1e9

        msg = Twist()
        if elapsed < 5.0:
            msg.linear.x = 0.15   # drive forward at 0.15 m/s
        else:
            msg.linear.x = 0.0    # then stop
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = DriveForward()
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