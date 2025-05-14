from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Color, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# --- Setup Motors & Sensors ---
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.B)
colour_sensor = ColorSensor(Port.C)
distance_sensor = UltrasonicSensor(Port.D)

# NEW: Gripper motor (assuming it's on Port E)
gripper_motor = Motor(Port.E)

robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=112)

# --- Settings ---
DRIVE_SPEED = 200       # Normal speed (mm/s)
TURN_SPEED = 90         # Turning speed (deg/s)
GRIPPER_SPEED = 500     # Gripper motor speed (deg/s)
GRIPPER_ANGLE = 90      # How much the gripper opens/closes (degrees)

BLOCK_DISTANCE = 80     # How close to get before grabbing (mm)
AVOID_DISTANCE = 200    # When to avoid something (mm)

# Colours we want (red and yellow)
RED = (90, 20, 20)      # Mostly red
YELLOW = (80, 80, 10)   # Red + green (makes yellow)

# Colours to avoid (blue and green)
BAD_COLOURS = [Color.BLUE, Color.GREEN]

# Tracks which blocks we've collected
got_red = False
got_yellow = False

# --- NEW: Gripper Functions ---
def open_gripper():
    gripper_motor.run_angle(GRIPPER_SPEED, -GRIPPER_ANGLE)  # Opens gripper
    wait(200)

def close_gripper():
    gripper_motor.run_angle(GRIPPER_SPEED, GRIPPER_ANGLE)   # Closes gripper
    wait(200)

# --- Movement Functions ---
def avoid_block():
    print("Avoiding bad block!")
    robot.stop()
    robot.straight(-50)  # Reverse a bit
    robot.turn(45)       # Turn right
    robot.straight(150)  # Go around
    robot.turn(-45)      # Turn back straight

def grab_block():
    print("Grabbing block!")
    open_gripper()              # Open gripper
    robot.straight(30)          # Move a tiny bit closer
    close_gripper()             # Close gripper on block
    wait(500)                   # Wait to make sure it's gripped

def return_home():
    print("Returning to start zone!")
    robot.turn(180)             # Turn around
    robot.straight(500)         # Drive back to start (adjust distance)
    open_gripper()              # Drop the block
    robot.straight(-500)        # Go back to searching
    close_gripper()             # Close gripper for next block

# --- Main Program ---
while not (got_red and got_yellow):
    robot.drive(DRIVE_SPEED, 0)  # Drive forward
    
    # If something is close
    if distance_sensor.distance() < AVOID_DISTANCE:
        current_colour = colour_sensor.color()
        
        # Check if it's red or yellow
        if not got_red and (current_colour.r() > RED[0] and current_colour.g() < RED[1]):
            print("Found RED block!")
            grab_block()
            return_home()
            got_red = True
        elif not got_yellow and (current_colour.r() > YELLOW[0] and current_colour.g() > YELLOW[1]):
            print("Found YELLOW block!")
            grab_block()
            return_home()
            got_yellow = True
        elif current_colour in BAD_COLOURS:
            avoid_block()  # Dodge blue/green blocks
        else:
            avoid_block()  # Avoid unknown stuff
    
    wait(10)

print("Mission complete! Both blocks delivered!")
