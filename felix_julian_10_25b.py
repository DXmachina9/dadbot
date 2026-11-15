from pybricks.hubs import PrimeHub # Or your hub type
from pybricks.robotics import DriveBase
from pybricks.pupdevices import Motor
from pybricks.iodevices import XboxController
from pybricks.parameters import Button, Direction, Port
from pybricks.tools import wait

# Initialize the robot
hub = PrimeHub()
left_front_drive_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
left_back_drive_motor = Motor(Port.E, Direction.COUNTERCLOCKWISE)
right_front_drive_motor = Motor(Port.B)
right_back_drive_motor = Motor(Port.F)
task_motor_1 = Motor(Port.C)
task_motor_2 = Motor(Port.D)

# Initialize the Xbox controller
controller = XboxController()

# Define deadzone and speed scale factor
DEADZONE_THRESHOLD = 16
SPEED_SCALE_FACTOR = 10.0

# Main control loop
while True:
    # Get joystick input (values between -100 and 100)
    drive_speed = controller.joystick_left()[1] 
    sideways_speed = controller.joystick_left()[0]
    turn_speed = controller.joystick_right()[0]
    triggers = controller.triggers()
    task_speed = triggers[1]-triggers[0]
    task_speed_2 = controller.joystick_right()[1]


    # Apply deadzone to prevent drift
    if abs(drive_speed) < DEADZONE_THRESHOLD:
        drive_speed = 0
    if abs(sideways_speed) < DEADZONE_THRESHOLD:
        sideways_speed = 0
    if abs(turn_speed) < DEADZONE_THRESHOLD:
        turn_speed = 0
    if abs(task_speed) < DEADZONE_THRESHOLD:
        task_speed = 0
    if abs(task_speed_2) < DEADZONE_THRESHOLD:
        task_speed_2 = 0

    # Scale the speeds
    scaled_drive_speed = drive_speed * SPEED_SCALE_FACTOR
    scaled_turn_speed = turn_speed * 5.0
    scaled_sideways_speed = sideways_speed * SPEED_SCALE_FACTOR
    scaled_task_speed = task_speed * 5.0
    scaled_task_speed_2 = task_speed_2 * 5.0

    # Control the robot
    left_front_drive_motor.run(scaled_drive_speed+scaled_turn_speed+scaled_sideways_speed)
    left_back_drive_motor.run(scaled_drive_speed+scaled_turn_speed-scaled_sideways_speed)
    right_front_drive_motor.run(scaled_drive_speed-scaled_turn_speed-scaled_sideways_speed)
    right_back_drive_motor.run(scaled_drive_speed-scaled_turn_speed+scaled_sideways_speed)
    task_motor_1.run(scaled_task_speed)
    task_motor_2.run(scaled_task_speed_2)

    # Add a small wait to keep the loop from running too fast
    wait(10)