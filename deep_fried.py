from pybricks.hubs import PrimeHub # Or your hub type
from pybricks.robotics import DriveBase
from pybricks.pupdevices import Motor
from pybricks.iodevices import XboxController
from pybricks.parameters import Button, Direction, Port
from pybricks.tools import wait

# Initialize the robot
hub = PrimeHub()
back_left_drive_motor = Motor(Port.F, Direction.COUNTERCLOCKWISE)
front_left_drive_motor = Motor(Port.E, Direction.COUNTERCLOCKWISE)
back_right_drive_motor = Motor(Port.B)
front_right_drive_motor = Motor(Port.A)
brick_collector = Motor(Port.D)

# Initialize the Xbox controller
controller = XboxController()

# Define deadzone and speed scale factor
DEADZONE_THRESHOLD = 20
SPEED_SCALE_FACTOR = 7.0
TURN_SCALE_FACTOR = 5.0
STRAFE_SCALE_FACTOR = 8.0


# Main control loop
while True:
    # Get joystick input (values between -100 and 100)
    drive_speed = controller.joystick_left()[1] 
    turn_speed = controller.joystick_left()[0]
    brick_speed = controller.joystick_right()[0]
    triggers = controller.triggers()
    strafe_speed = triggers[1]-triggers[0]

    # Apply deadzone to prevent drift
    if abs(drive_speed) < DEADZONE_THRESHOLD:
        drive_speed = 0
    if abs(turn_speed) < DEADZONE_THRESHOLD:
        turn_speed = 0
    if abs(brick_speed) < DEADZONE_THRESHOLD:
        brick_speed = 0

    # Scale the speeds
    scaled_drive_speed = drive_speed * SPEED_SCALE_FACTOR
    scaled_turn_speed = turn_speed * TURN_SCALE_FACTOR
    scaled_brick_speed = brick_speed * 5.0
    scaled_strafe_speed = strafe_speed * STRAFE_SCALE_FACTOR

    pressed = controller.buttons.pressed()
    if Button.A in pressed:
        SPEED_SCALE_FACTOR = 18
    elif Button.LB in pressed:
        SPEED_SCALE_FACTOR = 3.5
    else:
        SPEED_SCALE_FACTOR = 7
    
    if Button.B in pressed:
        TURN_SCALE_FACTOR = 10.0
    else:
        TURN_SCALE_FACTOR = 5.0

    if Button.X in pressed:
        STRAFE_SCALE_FACTOR = 14
    elif Button.RB in pressed:
        STRAFE_SCALE_FACTOR = 4
    else:
        STRAFE_SCALE_FACTOR = 8



    # Control the robot
    # drive_base.drive(scaled_drive_speed, scaled_turn_speed)
    front_left_drive_motor.run(scaled_drive_speed+scaled_turn_speed+scaled_strafe_speed)
    front_right_drive_motor.run(scaled_drive_speed-scaled_turn_speed-scaled_strafe_speed)
    back_left_drive_motor.run(scaled_drive_speed+scaled_turn_speed-scaled_strafe_speed)
    back_right_drive_motor.run(scaled_drive_speed-scaled_turn_speed+scaled_strafe_speed)
    brick_collector.run(scaled_brick_speed)

    # Add a small wait to keep the loop from running too fast
    wait(10)

    