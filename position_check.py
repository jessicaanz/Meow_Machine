from math import sin, cos
from pylx16a.lx16a import *
import time

# Use COM6 port
LX16A.initialize("COM6", 0.1)

try:
    servo1 = LX16A(1)
    servo2 = LX16A(2)
    servo1.set_angle_limits(0, 240)
    servo2.set_angle_limits(0, 240)

    initial_pos1 = servo1.get_physical_angle()
    initial_pos2 = servo2.get_physical_angle()

    print(f"Servo 1: {initial_pos1} degrees")
    print(f"Servo 2: {initial_pos2} degrees")

except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()