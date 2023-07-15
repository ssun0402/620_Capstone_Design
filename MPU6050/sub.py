import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile

from std_msgs.msg import Float32

class Sub(Node):
    
    def __init__(self):
        super().__init__('sub')
        qos_profile = QoSProfile(depth=10)
        self.subscriber_ = self.create_subscription(
            Float32,
            'topic',
            self.listener_callback,
            qos_profile
        )
        
    def listener_callback(self, msg):
        self.get_logger().info('Received Gx: "%f"' % msg.data)
        self.get_logger().info('Received Gy: "%f"' % msg.data)
        self.get_logger().info('Received Gz: "%f"' % msg.data)
        self.get_logger().info('Received Ax: "%f"' % msg.data)
        self.get_logger().info('Received Ay: "%f"' % msg.data)
        self.get_logger().info('Received Az: "%f"' % msg.data)
        
def main(args=None):
    rclpy.init(args=args)
    node = Sub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()
        
if __name__ == '__main__' :
    main()