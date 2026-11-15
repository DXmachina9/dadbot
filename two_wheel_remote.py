from pybricks.hubs import PrimeHub # Or your hub type
from pybricks.robotics import DriveBase
from pybricks.pupdevices import Motor
from pybricks.iodevices import XboxController
from pybricks.parameters import Button, Direction, Port
from pybricks.tools import wait

# Initialize the robot
hub = PrimeHub()
left_drive_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_drive_motor = Motor(Port.F)
drive_base = DriveBase(left_drive_motor, right_drive_motor, wheel_diameter=87, axle_track=142.5)

# Initialize the Xbox controller
controller = XboxController()

# Define deadzone and speed scale factor
DEADZONE_THRESHOLD = 64
SPEED_SCALE_FACTOR = 5.0

# Main control loop
while True:
    # Get joystick input (values between -100 and 100)
    drive_speed = controller.joystick_left()[1] 
    turn_speed = controller.joystick_left()[0]

    # Apply deadzone to prevent drift
    if abs(drive_speed) < DEADZONE_THRESHOLD:
        drive_speed = 0
    if abs(turn_speed) < DEADZONE_THRESHOLD:
        turn_speed = 0

    # Scale the speeds
    scaled_drive_speed = drive_speed * SPEED_SCALE_FACTOR
    scaled_turn_speed = turn_speed * 1.0

    # Control the robot
    drive_base.drive(scaled_drive_speed, scaled_turn_speed)

    # Add a small wait to keep the loop from running too fast
    wait(10)
