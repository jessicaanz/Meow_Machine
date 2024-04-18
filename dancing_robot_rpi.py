import math #no
from lx16a import *
import time
import numpy as np
import matplotlib.pyplot as plt

# Use COM6 port
LX16A.initialize("/dev/ttyUSB0", 0.1)


##### SETUP #####
servos = []
positions = np.zeros(8)
angles_recorded = {new_servo_id: [] for new_servo_id in range(1, 9)}  # Dictionary to store angle history
servo_limits = [(0, 185), (0, 190), (30, 230), (0, 180), (10, 215), (25, 225), (5, 220), (20, 225)]
straight_positions = [90, 45, 125, 85, 109, 82, 122, 127]


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

def move_servo_sin(servo_id, amplitude, frequency, phase_shift, vertical_shift, positions, move_time):
    try:
        t = 0
        while t < move_time:
            # Create a sinusoidal wave between the start and end angles with period of move_time
            sinusoidal_angle = amplitude * np.sin((frequency*t) + phase_shift) + vertical_shift
            servos[servo_id-1].move(sinusoidal_angle)
            time.sleep(0.05)
            t += 0.1
            update_positions(servos, positions)
        print(f"Moved servo {servo_id} degrees in {move_time} seconds")
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

def plot_motor_angles(angles_recorded):
    plt.figure(figsize=(10, 8))
    for servo_id, angles in angles_recorded.items():
        plt.plot(angles, label=f'Servo {servo_id}')
    plt.xlabel('Time Step')
    plt.ylabel('Servo Angle')
    plt.title('Motor Angles Over Time')
    plt.legend()
    plt.show()

def home_position():
    move_2_servos_with_offsets(1, 2, -50, 40, straight_positions, positions, 1)
    move_2_servos_with_offsets(4, 3, 50, -40, straight_positions, positions, 1)
    move_2_servos_with_offsets(5, 6, -40, 30, straight_positions, positions, 1)
    move_2_servos_with_offsets(7, 8, 40, -30, straight_positions, positions, 1)
    print("Moved to home position")

def swaying():
    move_2_servos_with_offsets(1, 4, -70, 70, straight_positions, positions, 1)
    move_2_servos_with_offsets(1, 4, -50, 50, straight_positions, positions, 1)
    move_2_servos_with_offsets(5, 7, -20, 20, straight_positions, positions, 1)
    move_2_servos_with_offsets(5, 7, -40, 40, straight_positions, positions, 1)


def leg_lifts():
    # move_2_servos_with_offsets(1, 2, -55, -10, straight_positions, positions, 1)
    # move_2_servos_with_offsets(1, 2, -50, 40, straight_positions, positions, 1)
    move_2_servos_with_offsets(4, 3, 60, -3, straight_positions, positions, 1)
    move_2_servos_with_offsets(4, 3, 50, -40, straight_positions, positions, 1)

def twerk():
    move_2_servos_with_offsets(1, 4, -70, 70, straight_positions, positions, 1)
    move_2_servos_with_offsets(5, 7, -10, 10, straight_positions, positions, 0.5)
    move_2_servos_with_offsets(5, 7, -40, 40, straight_positions, positions, 0.5)
    move_2_servos_with_offsets(5, 7, -10, 10, straight_positions, positions, 0.5)
    move_2_servos_with_offsets(5, 7, -40, 40, straight_positions, positions, 0.5)


##### MAIN METHOD #####

# Initialize servos
for i in range(8):
    servos.append(initialize_servo(i+1, *servo_limits[i]))
    positions[i] = servos[i].get_physical_angle()
    print(f"Servo {i+1}: {positions[i]} degrees")
print("Initialized 8 servos")

# Move to home positions
home_position()

# Dancing Cycle!!!
for i in range(1, 20):
    swaying()
    leg_lifts()
    twerk()

# Plot Angles over time
#plot_motor_angles(angles_recorded)