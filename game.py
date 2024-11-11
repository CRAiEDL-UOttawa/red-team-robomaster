import random
import time

# mapping vision markers to numbers 
vmarker = {
    1:rm_define.marker_number_one,
    2:rm_define.marker_number_two,
    3:rm_define.marker_number_three,
    4:rm_define.marker_number_four,
    5:rm_define.marker_number_five
}

condmapper = {
    1:rm_define.cond_recognized_marker_number_one,
    2:rm_define.cond_recognized_marker_number_two,
    3:rm_define.cond_recognized_marker_number_three,
    4:rm_define.cond_recognized_marker_number_four,
    5:rm_define.cond_recognized_marker_number_five
}

def user_defined_Detect(r):
    random_marker = vmarker.get(r)
    print(random_marker)
    print(condmapper.get(r))
    print(r)
    vision_ctrl. enable_detection(rm_define.vision_detection_marker)
    vision_ctrl.set_marker_detection_distance(1)
    time.sleep(2)
    if vision_ctrl.check_condition(condmapper.get(r)):
        # change led to flash red
        led_ctrl.set_top_led(rm_define.armor_top_all, 255, 0, 0, rm_define.effect_flash)
        vision_ctrl.detect_marker_and_aim(random_marker) 
        gun_ctrl.fire_once()
        # remove marker from list if detected
        vmarker.pop(r)
        return True
    return False
        
def move():
    r = random.randint(1,5)
    found = False
    
    chassis_ctrl.move_with_distance(90,2)
    gimbal_ctrl.yaw_ctrl(-90)
    chassis_ctrl.move_with_distance(0,1)
    if not found:
        found = user_defined_Detect(r)
    chassis_ctrl.move_with_distance(0,1.5)
    if not found:
        found = user_defined_Detect(r)
    gimbal_ctrl.yaw_ctrl(-180)
    chassis_ctrl.move_with_distance(-90,1)
    if not found:
        found = user_defined_Detect(r)
    chassis_ctrl.move_with_distance(-90,1)
    if not found:
        found = user_defined_Detect(r)
    gimbal_ctrl.yaw_ctrl(90)
    chassis_ctrl.move_with_distance(-180,1)
    if not found:
        found = user_defined_Detect(r)
    chassis_ctrl.move_with_distance(-180,1.5)
    if not found:
        found = user_defined_Detect(r)
    gimbal_ctrl.recenter()
        
def start():
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    if len(vmarker) > 1:
        for count in range(5):   # 5 rounds for every game 
            # at start of each round, robot will count down a from a random number between 1-5
            rand = random.randint(1,5)
            for i in range(rand,0,-1):
                media_ctrl.play_sound(rm_define.media_sound_count_down)
                time.sleep(1)
            time.sleep(1)
            media_ctrl.play_sound(rm_define.media_sound_solmization_2D)
            move()
    else:
        conclusion()
    

def conclusion():
    # flashing lights
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 0, 127, 70, rm_define.effect_flash)
    media_ctrl.play_sound(rm_define.media_sound_count_down)
    time.sleep(2)
    

# NOTES:
    
        
