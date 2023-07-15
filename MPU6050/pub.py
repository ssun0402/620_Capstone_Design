import smbus
from time import sleep
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile

from std_msgs.msg import Float32

bus = smbus.SMBus(1)
Device_Address = 0x68

PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45

class Pub(Node):
    def MPU_Init(self):
        bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
        bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
        bus.write_byte_data(Device_Address, CONFIG, 0)
        bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
        bus.write_byte_data(Device_Address, INT_ENABLE, 1)

    def read_raw_data(self, addr):
        high = bus.read_word_data(Device_Address, addr)
        value = ((high & 0xFF00) >> 8) | ((high & 0x00FF) << 8)
        if value > 32768:
            value = value - 65536
        return value
    
    def __init__(self):
        super().__init__('pub')
        qos_profile = QoSProfile(depth=10)
        self.publisher_=self.create_publisher(Float32, 'topic', qos_profile)
        timer_period = 0.5 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.MPU_Init()
        
    def timer_callback(self):
        acc_x = self.read_raw_data(ACCEL_XOUT_H)
        acc_y = self.read_raw_data(ACCEL_YOUT_H)
        acc_z = self.read_raw_data(ACCEL_ZOUT_H)
        gyro_x = self.read_raw_data(GYRO_XOUT_H)
        gyro_y = self.read_raw_data(GYRO_YOUT_H)
        gyro_z = self.read_raw_data(GYRO_ZOUT_H)
        Ax = acc_x / 16384.0
        Ay = acc_y / 16384.0
        Az = acc_z / 16384.0
        Gx = gyro_x / 131.0
        Gy = gyro_y / 131.0
        Gz = gyro_z / 131.0

        msg = Float32()
        msg.data = Gx
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing Gx: %f' % msg.data)

        msg.data = Gy
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing Gy: %f' % msg.data)

        msg.data = Gz
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing Gz: %f' % msg.data)

        msg.data = Ax
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing Ax: %f' % msg.data)

        msg.data = Ay
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing Ay: %f' % msg.data)

        msg.data = Az
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing Az: %f' % msg.data)
        
def main(args=None):
    rclpy.init(args=args)
    node = Pub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()
        
if __name__ == '__main__':
    main()