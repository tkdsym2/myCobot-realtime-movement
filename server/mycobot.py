from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle, Coord

class MyCobotCon:
    def __init__(self, port, client, realtime_client):
        self.port = port
        self.client = client
        self.Rclient = realtime_client
        self.arm = None

    # util functions
    def connect(self):
        self.arm = MyCobot(self.port)
        self.arm.power_on()
        return self.arm.is_power_on()

    def disconnect(self):
        self.arm.power_off()
        return self.arm.is_power_on()
    
    def get_arm_status(self):
        _angles = self.arm.get_angles()
        _coords = self.arm.get_coords()
        _radians = self.arm.get_radians()
        d = {
            'angles': _angles,
            'coords': _coords,
            'radians': _radians
        }
        return d
    
    def release_all_servo(self):
        self.arm.release_all_servos()
    
    def set_free_mode(self):
        self.arm.set_free_mode()
    
    def initialize_position(self):
        self.arm.send_angles([0,0,0, 0,0,0], 50)

    def move_test(self):
        self.arm.send_coords([100,0,0, 0,0,0], 10, 1)
    
    # arm motion - angle
    def command_angle(self, _angles, _speed):
        self.arm.send_angles(_angles, _speed)

    def sync_angle(self, _angles, _speed):
        self.arm.sync_send_angles(_angles, _speed)

    # arm hand - settings
    def set_led_color(self, _r, _g, _b):
        self.arm.set_color(_r, _g, _b)