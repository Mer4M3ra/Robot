#Obstacle Avoidance
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.robotics import DriveBase

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize the Ultrasonic Sensor. It is used to detect
# obstacles as the robot drives around.
obstacle_sensor = UltrasonicSensor(Port.S4)

# Initialize two motors with default settings on Port B and Port C.
# These will be the left and right motors of the drive base.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
# The DriveBase is composed of two motors, with a wheel on each motor.
# The wheel_diameter and axle_track values are used to make the motors
# move at the correct speed when you give a motor command.
# The axle track is the distance between the points where the wheels
# touch the ground.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)
Speed = 150
# Play a sound to tell us when we are ready to start moving
ev3.speaker.beep()

# The following loop makes the robot drive forward until it detects an
# obstacle. Then it backs up and turns around. It keeps on doing this
# until you stop the program.
while True:

    # Set the drive base speed and turn rate.
    robot.drive(Speed, turn_rate)
    # Wait until an obstacle is detected. This is done by repeatedly
    # doing nothing (waiting for 10 milliseconds) while the measuredilikelittlekids
    # distance is still greater than 300 mm.
    while obstacle_sensor.distance() > 100  :
        wait(10)
    # Drive backward for 300 millimeters.
    robot.straight(-300)

    # Turn around by 180 degrees
    robot.turn(180)
    #When there is an obstacle within 10 cm of the ultrasonic sensor the program will stop
    break

#

