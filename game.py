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

responses = {
    
    
}

condmapper = {
    1:rm_define.cond_recognized_marker_number_one,
    2:rm_define.cond_recognized_marker_number_two,
    3:rm_define.cond_recognized_marker_number_three,
    4:rm_define.cond_recognized_marker_number_four,
    5:rm_define.cond_recognized_marker_number_five
}

picked = [1, 2, 3, 4, 5] # list of picked markers

def user_defined_Detect(r):
    random_marker = vmarker.get(r) #3
    print(random_marker)
    print(condmapper.get(r))
    print(r)
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    vision_ctrl.set_marker_detection_distance(1.5)
    time.sleep(2)
    if vision_ctrl.check_condition(condmapper.get(r)):
        # change led to flash red
        led_ctrl.set_top_led(rm_define.armor_top_all, 255, 0, 0, rm_define.effect_flash)
        vision_ctrl.detect_marker_and_aim(random_marker) 
        gun_ctrl.fire_once()
        gun_ctrl.fire_once()
        gun_ctrl.fire_once()
        # remove marker from list if detected
        vmarker.pop(r)
        # remove r from picked
        picked.remove(r)
        time.sleep(2)
        return True
    else:
        led_ctrl.set_top_led(rm_define.armor_top_all, 0, 255, 0, rm_define.effect_flash)
        media_ctrl.play_sound(rm_define.media_sound_solmization_1C)
    return False
        
def move(direction):
    r = random.choice(picked)
    found = False
    if direction == "anti":
        chassis_ctrl.move_with_distance(90,2.7)
        gimbal_ctrl.yaw_ctrl(-90)
        chassis_ctrl.move_with_distance(0,1.9)
        if not found:
            found = user_defined_Detect(r)
        chassis_ctrl.move_with_distance(0,1.9)
        if not found:
            found = user_defined_Detect(r)
        gimbal_ctrl.yaw_ctrl(-180)
        chassis_ctrl.move_with_distance(-90,1.35)
        if not found:
            found = user_defined_Detect(r)
        chassis_ctrl.move_with_distance(-90,1.35)
        if not found:
            found = user_defined_Detect(r)
        # increasing gimbal rotation speed 
        gimbal_ctrl.set_rotate_speed(250)
        gimbal_ctrl.yaw_ctrl(90) # at this point, the gimbal moves all around 
        chassis_ctrl.move_with_distance(-180,1.9)
        if not found:
            found = user_defined_Detect(r)
        chassis_ctrl.move_with_distance(-180,1.9)
        if not found:
            found = user_defined_Detect(r)
        gimbal_ctrl.recenter()
    
    else:
        #chassis_ctrl.move_with_distance(-90,2)
        gimbal_ctrl.yaw_ctrl(90)
        chassis_ctrl.move_with_distance(0,1.9)
        if not found:
            found = user_defined_Detect(r)
        chassis_ctrl.move_with_distance(0,1.9)
        if not found:
            found = user_defined_Detect(r)
        gimbal_ctrl.yaw_ctrl(180)
        chassis_ctrl.move_with_distance(90,1.35)
        if not found:
            found = user_defined_Detect(r)
        chassis_ctrl.move_with_distance(90,1.35)
        if not found:
            found = user_defined_Detect(r)
        gimbal_ctrl.set_rotate_speed(250)
        gimbal_ctrl.yaw_ctrl(-90)
        chassis_ctrl.move_with_distance(180,1.9)
        if not found:
            found = user_defined_Detect(r)
        chassis_ctrl.move_with_distance(180,1.9)
        if not found:
            found = user_defined_Detect(r)
        chassis_ctrl.move_with_distance(-90,2.7)
        gimbal_ctrl.recenter()
        
def start():
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    for count in range(5):   # 5 rounds for every game 
        # at start of each round, robot will count down a from a random number between 1-5
        if len(vmarker) > 1:
            print("ROUND "+ str(count+1) + " START")
            rand = random.randint(1,5)
            for i in range(rand,0,-1):
                media_ctrl.play_sound(rm_define.media_sound_count_down)
                time.sleep(1)
            time.sleep(1)
            media_ctrl.play_sound(rm_define.media_sound_solmization_2D)
            
            #determining direction 
            randomd = random.randint(1,1000)
            direction = "clockwise" if randomd % 2 == 0 else "anti"
            print("Direction: "+direction)
            move(direction)
            print("Vmarker size: "+str(len(vmarker)))
            time.sleep(10)
        else:
            conclusion()
    

def conclusion():
    # flashing lights and loud sounds for 5s
    led_ctrl.set_top_led(rm_define.armor_top_all, 255, 0, 0, rm_define.effect_flash)
    media_ctrl.play_sound(rm_define.media_sound_recognize_success)
    time.sleep(5)
    

# NOTES:
# 1. I can make a set list to store values from 1 to 5, pick a random value and remove it after picked.
# 2. more work to be done on conclusion
# 3. spin? at corner
# 4. for the scare factors, maybe adding more sounds and more menacing lights in each round 
# 5. intro for sure 
# 6. in blocks, add current chassis position
# 7. line detection(?)
# 8. 


# TODO
# 1. Gimbal locked at 250 > 0 > -250
# 2. add responses for each marker recognized, so like one to kill and the rest get maybe a ding or a positive response for everything else 
# 3. more gamey aspects, for example let number 5 get killed first and then randomize (SLASH)
# 4. more workshop problems, have problem x solution documened in time for friday 
# 5. fix the spin at corner thing 
# 6. programming how each individual wheel works and understand and explain 
# 7. different movement parameters for each round probably (IMPORTANT)
#

        
