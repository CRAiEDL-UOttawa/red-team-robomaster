import robomaster
from robomaster import robot
import time 

# Initialize the robot
ep_robot = robot.Robot()
ep_robot.initialize(conn_type="sta")

# Define the callback function for motion detection
def on_motion_detected(event):
    print("Motion detected!")
    
def move_to_path(robot):
    path = [(0, 0), (1, 1), (1, 0), (0, 1)]  # Example coordinates
    for coord in path:
        x, y = coord
        robot.move_to(x, y)  # Pseudo function to move to coordinates
        time.sleep(2)  # Pause for 2 seconds at each coordinate


# Enable the vision module
ep_vision = ep_robot.vision
ep_vision.sub_detect_info(name="motion", callback=on_motion_detected)

# Start motion detection
ep_vision.motion_detection(enable=True)

# Keep the script running to detect motion
try:
    while True:
        pass
except KeyboardInterrupt:
    # Stop motion detection and close the robot connection
    ep_vision.motion_detection(enable=False)
    ep_robot.close()