from math import sin, cos
from pylx16a.lx16a import *
import time

# Use COM6 port
LX16A.initialize("COM6", 0.1)

################################### CALIBRATION (manually input positions) #########################################################
str8_leg_1 = 92.16
str8_leg_2 = 93.84
str8_leg_3 = 134.4
str8_leg_4 = 86.16
str8_leg_5 = 115.44
str8_leg_6 = 128.88
str8_leg_7 = 115.2
str8_leg_8 = 126.24

#################################### LEG SETUP ########################################################################################
### LEG 1 ###
try:
    servo1 = LX16A(1)
    servo2 = LX16A(2)
    servo1.set_angle_limits(0, 185)
    servo2.set_angle_limits(0, 190)
    position_1 = servo1.get_physical_angle()
    position_2 = servo2.get_physical_angle()

    print(f"Servo 1: {position_1} degrees")
    print(f"Servo 2: {position_2} degrees")

except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()

### LEG 2 ###
try:
    servo3 = LX16A(3)
    servo4 = LX16A(4)
    servo3.set_angle_limits(30, 230)
    servo4.set_angle_limits(0, 180)
    position_3 = servo3.get_physical_angle()
    position_4 = servo4.get_physical_angle()

    print(f"Servo 3: {position_3} degrees")
    print(f"Servo 4: {position_4} degrees")

except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()

### LEG 3 ###
try:
    servo5 = LX16A(5)
    servo6 = LX16A(6)
    servo5.set_angle_limits(10, 215)
    servo6.set_angle_limits(25, 225)
    position_5 = servo5.get_physical_angle()
    position_6 = servo6.get_physical_angle()

    print(f"Servo 5: {position_5} degrees")
    print(f"Servo 6: {position_6} degrees")

except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()

### LEG 4 ###
try:
    servo7 = LX16A(7)
    servo8 = LX16A(8)
    servo7.set_angle_limits(5, 220)
    servo8.set_angle_limits(20, 225)
    position_7 = servo7.get_physical_angle()
    position_8 = servo8.get_physical_angle()

    print(f"Servo 7: {position_7} degrees")
    print(f"Servo 8: {position_8} degrees")

except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()

print("Initialized 8 servos")

#################################################### FUNCTIONS ##########################################################################################
def update_postion(servo1, servo2, servo3, servo4, servo5, servo6, servo7, servo8):
    position_1 = servo1.get_physical_angle()
    position_2 = servo2.get_physical_angle()
    position_3 = servo3.get_physical_angle()
    position_4 = servo4.get_physical_angle()
    position_5 = servo5.get_physical_angle()
    position_6 = servo6.get_physical_angle()
    position_7 = servo7.get_physical_angle()
    position_8 = servo8.get_physical_angle()
    return position_1, position_2, position_3, position_4, position_5, position_6, position_7, position_8

def move_servo(desired_angle, servo, id, current_position, move_time):
    try:
        angle_range = (desired_angle - current_position)
        t = 0
        while t < move_time:
            interpolated_angle = current_position + (angle_range * t / move_time)
            servo.move(interpolated_angle)
            time.sleep(0.05)
            t += 0.1
            update_postion(servo1, servo2, servo3, servo4, servo5, servo6, servo7, servo8)

        print(f"Moved servo {id} to {desired_angle} degrees in {move_time} seconds")
        time.sleep(0.25)

    except ServoTimeoutError as e:
        print(f"Servo {e.id_} is not responding. Exiting...")

def move_2_servos(top_angle, bottom_angle, top_servo, bottom_servo, top_id, bottom_id, top_position, bottom_position, move_time):
    try:
        top_angle_range = (top_angle - top_position)
        bottom_angle_range = (bottom_angle - bottom_position)
        t = 0
        while t < move_time:
            top_interpolated_angle = top_position + (top_angle_range * t / move_time)
            bottom_interpolated_angle = bottom_position + (bottom_angle_range * t / move_time)
            top_servo.move(top_interpolated_angle)
            bottom_servo.move(bottom_interpolated_angle)
            time.sleep(0.05)
            t += 0.1
            update_postion(servo1, servo2, servo3, servo4, servo5, servo6, servo7, servo8)

        print(f"Moved servos {top_id} and {bottom_id} to {top_angle} and {bottom_angle} degrees in {move_time} seconds")
        time.sleep(0.25)

    except ServoTimeoutError as e:
        print(f"Servo {e.id_} is not responding. Exiting...")


#################################################### MOTION ##########################################################################################

### START POSITION ###
move_2_servos(str8_leg_1-50, str8_leg_2+40, servo1, servo2, 1, 2, position_1, position_2, 2)
move_2_servos(str8_leg_4+50, str8_leg_3-40, servo4, servo3, 4, 3, position_4, position_3, 2)
move_2_servos(str8_leg_5-40, str8_leg_6+30, servo5, servo6, 5, 6, position_5, position_6, 2)
move_2_servos(str8_leg_7+40, str8_leg_8-30, servo7, servo8, 7, 8, position_7, position_8, 2)
print("Moved to home position")
time.sleep(2)

### WALKING ###
for i in range(1, 6):
    move_servo(str8_leg_1+35, servo1, 1, position_1, 3)
    move_servo(str8_leg_2+90, servo2, 2, position_2, 0.25)
    move_servo(str8_leg_1-70, servo1, 1, position_1, 0.25)
    move_servo(str8_leg_2+40, servo2, 2, position_2, 0.25)
    move_servo(str8_leg_1-50, servo1, 1, position_1, 0.25)

    move_servo(str8_leg_4-35, servo4, 4, position_4, 3)
    move_servo(str8_leg_3-90, servo3, 3, position_3, 0.25)
    move_servo(str8_leg_4+70, servo4, 4, position_4, 0.25)
    move_servo(str8_leg_3-40, servo3, 3, position_3, 0.25)
    move_servo(str8_leg_4+50, servo4, 4, position_4, 0.25)