def start():
    # Define speed and delay values
    drive_straight_speed = [60, 60, 60, 60]  # Speed for short straight movement
    small_turn_clockwise_speed = [60, -60, 60, -60]  # Speed for a small angle turn
    green = (0, 255, 0)
    red = (255, 0, 0)
    yellow = (255, 255, 0)
    time_delay_drive = 0.5  # Short time to drive straight
    time_delay_turn = 0.3  # Short time to make a small turn (about 30 degrees)
    random_stop_interval = 5  

     # Set gimbal to follow chassis
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)

    while True:
        for _ in range(36):  # Adjust the number of repetitions for a full circle
            # Set LEDs to green while driving straight
            led_ctrl.set_top_led(rm_define.armor_top_all, green[0], green[1], green[2], rm_define.effect_flash)
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all, green[0], green[1], green[2], rm_define.effect_flash)

            # Drive straight for a short distance
            chassis_ctrl.set_wheel_speed(drive_straight_speed[0], drive_straight_speed[1], 
                                         drive_straight_speed[2], drive_straight_speed[3])
            time.sleep(time_delay_drive)
            
            # Rotate the gimbal from side to side
            gimbal_ctrl.rotate_with_degree(rm_define.gimbal_left, 90)
            time.sleep(0.5)
            gimbal_ctrl.rotate_with_degree(rm_define.gimbal_right, 90)
            time.sleep(0.5)

            chassis_ctrl.set_wheel_speed(small_turn_clockwise_speed[0], small_turn_clockwise_speed[1], 
                                         small_turn_clockwise_speed[2], small_turn_clockwise_speed[3])
            time.sleep(time_delay_turn)
            
            # Randomly stop and change LED to red
            if random.random() < 0.1:  # 10% chance to stop
                led_ctrl.set_top_led(rm_define.armor_top_all, red[0], red[1], red[2], rm_define.effect_breath)
                led_ctrl.set_bottom_led(rm_define.armor_bottom_all, red[0], red[1], red[2], rm_define.effect_breath)
                chassis_ctrl.stop()
                
                # Perform a 360-degree gimbal rotation
                gimbal_ctrl.rotate_with_degree(rm_define.gimbal_left, 180)
                time.sleep(1)
                gimbal_ctrl.rotate_with_degree(rm_define.gimbal_right, 180)
                time.sleep(1)
                
                # Check for seekers using vision detection
                vision_ctrl.enable_detection(rm_define.vision_detection_marker)
                time.sleep(1)
                markers = vision_ctrl.get_marker_detection_info()
                if markers:
                    led_ctrl.set_top_led(rm_define.armor_top_all, yellow[0], yellow[1], yellow[2], rm_define.effect_breath)
                    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, yellow[0], yellow[1], yellow[2], rm_define.effect_breath)
                    time.sleep(2)  # Pause to indicate seeker found
                
                time.sleep(random_stop_interval)
                break