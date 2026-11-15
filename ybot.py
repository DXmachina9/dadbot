from pybricks.hubs import PrimeHub # Or your hub type
from pybricks.robotics import DriveBase
from pybricks.pupdevices import Motor
from pybricks.iodevices import XboxController
from pybricks.parameters import Button, Direction, Port
from pybricks.tools import wait

# Initialize the robot
hub = PrimeHub()
left_front_drive_motor = Motor(Port.F, Direction.COUNTERCLOCKWISE)
right_front_drive_motor = Motor(Port.E)
left_back_drive_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_back_drive_motor = Motor(Port.A)
claw_motor = Motor(Port.C)
grab_motor = Motor(Port.D)
grab_motor.reset_angle(0)

# Initialize the Xbox controller
controller = XboxController()

# Define deadzone and speed scale factor
DEADZONE_THRESHOLD = 1
SPEED_SCALE_FACTOR = 5.0

controller.rumble()

# Main control loop
while True:
    # Get joystick input (values between -100 and 100)
    drive_speed = controller.joystick_left()[1] 
    strafe_speed = controller.joystick_left()[0]

    triggers = controller.triggers()
    turn_speed = triggers[1]-triggers[0]

    pressed = controller.buttons.pressed()
    if Button.A in pressed:
        claw_motor.run(100)
    elif Button.B in pressed:
        claw_motor.run(-100)
    else:
        claw_motor.run(0)

    if Button.X in pressed:
        grab_motor.run_target(500,0)
    elif Button.Y in pressed:
        grab_motor.run_target(500,-90)

    # Apply deadzone to prevent drift
    if abs(drive_speed) < DEADZONE_THRESHOLD:
        drive_speed = 0
    if abs(turn_speed) < DEADZONE_THRESHOLD:
        turn_speed = 0
    if abs(strafe_speed) < DEADZONE_THRESHOLD:
        strafe_speed = 0

    # Scale the speeds
    scaled_drive_speed = drive_speed * SPEED_SCALE_FACTOR
    scaled_strafe_speed = strafe_speed * SPEED_SCALE_FACTOR
    scaled_turn_speed = turn_speed * 10.0

    # Control the robot
    left_front_drive_motor.run(scaled_drive_speed+scaled_turn_speed+scaled_strafe_speed)
    left_back_drive_motor.run(scaled_drive_speed+scaled_turn_speed-scaled_strafe_speed)
    right_front_drive_motor.run(scaled_drive_speed-scaled_turn_speed-scaled_strafe_speed)
    right_back_drive_motor.run(scaled_drive_speed-scaled_turn_speed+scaled_strafe_speed)

    # Add a small wait to keep the loop from running too fast
    wait(10)
