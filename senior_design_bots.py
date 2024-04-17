from math import sin, cos
from pylx16a.lx16a import *
import time
import numpy as np

# Use COM6 port
LX16A.initialize("COM6", 0.1)


##### SETUP #####
servos = np.zeros(2)
positions = np.zeros(2)
servo_limits = [(5, 185), (0, 190)]


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
for i in range(2):
    servos[i+1] = initialize_servo(i+1, *servo_limits[i])
    positions[i+1] = servos[i+1].get_physical_angle()
    print(f"Servo {i+1}: {positions[i+1]} degrees")
print("Initialized 2 servos")

# Move to home positions