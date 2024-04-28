import math
from lx16a import *
import time

# Use COM6 port
LX16A.initialize("/dev/ttyUSB0", 0.1)


##### SETUP #####
servos = []
positions = [0, 0, 0, 0, 0, 0, 0, 0]
angles_recorded = {new_servo_id: [] for new_servo_id in range(1, 9)}  # Dictionary to store angle history
servo_limits = [(0, 185), (0, 190), (30, 230), (0, 180), (10, 215), (25, 225), (5, 220), (20, 225)]
straight_positions = [95, 105, 129, 85, 113, 73, 119, 126]


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
        positions[i] = servos[i].get_physical_angle()
        angles_recorded[i+1].append(positions[i])
    return positions

def move_servo(servo_id, desired_angle, positions, move_time):
    try:
        start_angle = positions[servo_id-1]
        angle_range = (desired_angle - start_angle)
        t = 0
        while t < move_time:
            # Create a sinusoidal wave between the start and end angles with period of move_time
            sinusoidal_angle = start_angle + (angle_range / 2) * (1 - math.cos(math.pi * t / move_time))
            servos[servo_id-1].move(sinusoidal_angle)
            time.sleep(0.05)
            t += 0.1
            update_positions(servos, positions)
        print(f"Moved servo {servo_id} to {desired_angle} degrees in {move_time} seconds")
    except ServoTimeoutError as e:
        print(f"Servo {e.id_} is not responding. Exiting...")

def move_2_servos(servo_id_1, servo_id_2, desired_angle_1, desired_angle_2, positions, move_time):
    try:
        start_angle_1 = positions[servo_id_1-1]
        start_angle_2 = positions[servo_id_2-1]
        angle_range_1 = (desired_angle_1 - start_angle_1)
        angle_range_2 = (desired_angle_2 - start_angle_2)
        t = 0
        while t < move_time:
            # Create a sinusoidal wave between the start and end angles with period of move_time
            sinusoidal_angle_1 = start_angle_1 + (angle_range_1 / 2) * (1 - math.cos(math.pi * t / move_time))
            sinusoidal_angle_2 = start_angle_2 + (angle_range_2 / 2) * (1 - math.cos(math.pi * t / move_time))
            servos[servo_id_1-1].move(sinusoidal_angle_1)
            servos[servo_id_2-1].move(sinusoidal_angle_2)
            time.sleep(0.05)
            t += 0.1
            update_positions(servos, positions)
        print(f"Moved servos {servo_id_1} and {servo_id_2} to {desired_angle_1} and {desired_angle_2} degrees in {move_time} seconds")
    except ServoTimeoutError as e:
        print(f"Servo {e.id_} is not responding. Exiting...")

def move_servo_with_offset(servo_id, desired_angle, straight_positions, positions, move_time):
    offset = straight_positions[servo_id-1]
    move_servo(servo_id, desired_angle+offset, positions, move_time)

def move_2_servos_with_offsets(servo_id_1, servo_id_2, desired_angle_1, desired_angle_2, straight_positions, positions, move_time):
    offset_1 = straight_positions[servo_id_1-1]
    offset_2 = straight_positions[servo_id_2-1]
    move_2_servos(servo_id_1, servo_id_2, desired_angle_1+offset_1, desired_angle_2+offset_2, positions, move_time)

def home_position():
    move_2_servos_with_offsets(1, 2, -50, 40, straight_positions, positions, 1)
    move_2_servos_with_offsets(4, 3, 50, -40, straight_positions, positions, 1)
    move_2_servos_with_offsets(5, 6, -40, 30, straight_positions, positions, 1)
    move_2_servos_with_offsets(7, 8, 40, -30, straight_positions, positions, 1)
    print("Moved to home position")

def leg_1_gait():
    move_2_servos_with_offsets(1, 2, 50.4, -49.2, straight_positions, positions, 1.5)
    move_2_servos_with_offsets(1, 2, 38, 85, straight_positions, positions, 1.5)
    move_2_servos_with_offsets(1, 2, -80, 85, straight_positions, positions, 1)
    move_2_servos_with_offsets(1, 2, -50, 40, straight_positions, positions, 1)

def leg_2_gait():
    move_2_servos_with_offsets(4, 3, -50.4, 49.2, straight_positions, positions, 1.5)
    move_2_servos_with_offsets(4, 3, -38, -85, straight_positions, positions, 1.5)
    move_2_servos_with_offsets(4, 3, 80, -85, straight_positions, positions,  1)
    move_2_servos_with_offsets(4, 3, 50, -40, straight_positions, positions, 1)

def leg_3_forward():
    move_2_servos_with_offsets(5, 6, 47, -43, straight_positions, positions, 1)

def leg_3_backward():
    move_2_servos_with_offsets(5, 6, -40, 30, straight_positions, positions, 1)

def leg_4_forward():
    move_2_servos_with_offsets(7, 8, -47, 43, straight_positions, positions, 1)

def leg_4_backward():
    move_2_servos_with_offsets(7, 8, 40, -30, straight_positions, positions, 1)


##### MAIN METHOD #####

# Initialize servos
for i in range(8):
    servos.append(initialize_servo(i+1, *servo_limits[i]))
    positions[i] = servos[i].get_physical_angle()
    print(f"Servo {i+1}: {positions[i]} degrees")
print("Initialized 8 servos")

# Move to home positions
home_position()

# Walking Cycle!!!
for i in range(1, 100):
    leg_4_forward()
    leg_1_gait()
    leg_4_backward()
    leg_3_forward()
    leg_2_gait()
    leg_3_backward()