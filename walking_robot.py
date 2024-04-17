from math import sin, cos
from pylx16a.lx16a import *
import time
import numpy as np

# Use COM6 port
LX16A.initialize("COM6", 0.1)


##### SETUP #####
servos = np.zeros(8)
positions = np.zeros(8)
servo_limits = [(0, 185), (0, 190), (30, 230), (0, 180), (10, 215), (25, 225), (5, 220), (20, 225)]
straight_positions = [92.16, 93.84, 134.4, 86.16, 115.44, 128.88, 115.2, 126.24]


##### HELPER FUNCTIONS #####
def initialize_servo(servo_id, angle_limit_1, angle_limit_2):
    try:
        servo = LX16A(servo_id)
        servo.set_angle_limits(angle_limit_1, angle_limit_2)
        return servo
    except ServoTimeoutError as e:
        print(f"Servo {e.id_} is not responding. Exiting...")
        quit()

def update_positions(servos, positions):
    for i in range(8):
        positions[i+1] = servos[i+1].get_physical_angle()
        return positions


##### MAIN METHOD #####

# Initialize servos
for i in range(8):
    servos[i+1] = initialize_servo(i+1, *servo_limits[i])
    positions[i+1] = servos[i+1].get_physical_angle()
    print(f"Servo {i+1}: {positions[i+1]} degrees")
print("Initialized 8 servos")

# Move to home positions