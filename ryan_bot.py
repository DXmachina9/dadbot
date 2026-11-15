from pybricks.hubs import TechnicHub # Or your hub type
from pybricks.robotics import DriveBase
from pybricks.pupdevices import Motor, DCMotor
from pybricks.iodevices import XboxController
from pybricks.parameters import Button, Direction, Port, Stop
from pybricks.tools import wait
from SPServo import SPServo_init, getPosition, setPosition, dev_id


# Initialize the robot
hub = TechnicHub()
left_motor = DCMotor(Port.B)
right_motor = DCMotor(Port.A, Direction.COUNTERCLOCKWISE)

# Initialize the Xbox controller
controller = XboxController()

SPServo_init('C')
setPosition(1,64)

    

# Define deadzone and speed scale factor
DEADZONE_THRESHOLD = 10
SPEED_SCALE_FACTOR = 3.0

past_drive_speed = 0

# Main control loop
while True:
    # Get joystick input (values between -100 and 100)
    drive_speed = controller.joystick_left()[1] 
    turn_speed = controller.joystick_left()[0]
    lift_speed = controller.joystick_right()[1] 
    
    pressed = controller.buttons.pressed()
    if Button.LB in pressed:
        setPosition(1,64)
        print('left bumper')
    elif Button.RB in pressed:
        setPosition(1,50)
        print('right bumper')

    # Apply deadzone to prevent drift
    if abs(drive_speed) < DEADZONE_THRESHOLD:
        drive_speed = 0
    if abs(turn_speed) < DEADZONE_THRESHOLD:
        turn_speed = 0
    if abs(lift_speed) < DEADZONE_THRESHOLD:
        lift_speed = 0


    if Button.UP in pressed:
        drive_speed = 200
    elif Button.DOWN in pressed:
        drive_speed = -200

    if Button.LEFT in pressed:
        turn_speed = -200
    elif Button.RIGHT in pressed:
        turn_speed = 200

    drive_speed = max(min(drive_speed,past_drive_speed+20),past_drive_speed-20)

    past_drive_speed = drive_speed

    # Calculate raw motor power using differential mixing    
    left_power  = (drive_speed + turn_speed)/2.0
    right_power = (drive_speed - turn_speed)/2.0


    # Constrain values to the valid LEGO duty cycle range (-100 to 100)
    left_power = max(-100, min(100, left_power))
    right_power = max(-100, min(100, right_power))
    
    # Apply power to the DC motors
    left_motor.dc(left_power)
    right_motor.dc(right_power)

    # Add a small wait to keep the loop from running too fast
    wait(10)
