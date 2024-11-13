import time

def move_square():

    # Define the movements
    movements = [
        (1.7, 0, 0),  # Move right 1.7m
        (0, 0, 90),   # Turn 90 degrees clockwise
        (2.5, 0, 0),  # Move down 2.5m
        (0, 0, 90),   # Turn 90 degrees clockwise
        (1.7, 0, 0),  # Move left 1.7m
        (0, 0, 90),   # Turn 90 degrees clockwise
        (2.5, 0, 0),  # Move up 2.5m
        (0, 0, 90)    # Turn 90 degrees clockwise to original orientation
    ]

    # Move in a square path
    for x, y, z in movements:
        chassis_ctrl.move(x=x, y=y, z=z, xy_speed=0.5).wait_for_completed()
        time.sleep(1)

    # Keep the gimbal faced inwards
    gimbal_ctrl.recenter(pitch=0, yaw=0).wait_for_completed()
