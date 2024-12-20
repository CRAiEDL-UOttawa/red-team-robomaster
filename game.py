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

picked = [1, 2, 3, 4, 5] # list of picked markers

# Dictionary of RGB colors
RGB = {
    "red": [255,0,0],
    "yellow": [255,255,0],
    "blue": [0,0,255],
    "green": [0,255,0],
    "pink": [255,0,150],
    "magenta": [224,0,255],
    "purple": [100,0,100],
    "blue": [36,103,255],
    "cyan": [69,215,255],
    "lime": [161,255,69],
    "yellow": [255,193,0],
    "orange": [255,50,0],
    "white": [255,255,255]
}

LED_Effects = {
    'pulsing': 2,
    'scanning': 4,
    'flashing': 3,
    'solid': 0,
    'off': 1
}


def set_led_color(top_color, bottom_color, effect): # from blue team (thanks guys)
    # get RGB values for colors
    top_rgb = RGB.get(top_color)
    bottom_rgb = RGB.get(bottom_color)
    
    effect_color = LED_Effects.get(effect)
    # check if both colors exist in dictionary
    if top_rgb is None:
        raise ValueError(f"Top color '{top_color}' not found.")
    if bottom_rgb is None:
        raise ValueError(f"Bottom color '{bottom_color}' not found.")
    
    if effect=="scanning":
        led_ctrl.set_top_led(rm_define.armor_top_all, top_rgb[0], top_rgb[1], top_rgb[2], effect_color)
    else:
        # set the top and bottom LEDs 
        led_ctrl.set_top_led(rm_define.armor_top_all, top_rgb[0], top_rgb[1], top_rgb[2], effect_color)
        led_ctrl.set_bottom_led(rm_define.armor_bottom_all, bottom_rgb[0], bottom_rgb[1], bottom_rgb[2], effect_color)

   

def intro():
    # robot comes in 
    # robot says hi
    # robot says the rules
    # robot says the game is about to start
    media_ctrl.play_sound(rm_define.media_custom_audio_6,wait_for_complete_flag = True) # intro audio
    media_ctrl.play_sound(rm_define.media_custom_audio_1,wait_for_complete_flag = True)

def user_defined_Detect(r):
    media_ctrl.exposure_value_update(rm_define.exposure_value_medium)
    random_marker = vmarker.get(r) 
    print(random_marker)
    print(condmapper.get(r))
    print(r)
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    vision_ctrl.set_marker_detection_distance(1.5)
    media_ctrl.play_sound(rm_define.media_sound_scanning, wait_for_complete=True)
    time.sleep(2)
    if vision_ctrl.check_condition(condmapper.get(r)):
        # change led to flash red
        set_led_color("red", "red", "flashing")
        vision_ctrl.detect_marker_and_aim(random_marker) 
        #media_ctrl.play_sound(rm_define.media_custom_audio_2,wait_for_complete_flag = True) # not human #TODO: idk why it takes so long 
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
        set_led_color("green", "green", "flashing")
        media_ctrl.play_sound(rm_define.media_sound_solmization_1C)
        media_ctrl.play_sound(rm_define.media_custom_audio_0,wait_for_complete_flag = True) # safe audio
    return False 
        
def move(direction):
    r = random.choice(picked)
    found = False
    gimbal_ctrl.pitch_ctrl(35)
    if direction == "anticlockwise":
        chassis_ctrl.move_with_distance(90,2.9)
        gimbal_ctrl.yaw_ctrl(-90)
        chassis_ctrl.move_with_distance(0,1.9)
        if not found:
            found = user_defined_Detect(r)
        chassis_ctrl.move_with_distance(0,1.9)
        gimbal_ctrl.yaw_ctrl(-180)
        chassis_ctrl.move_with_distance(-90,1.45)
        if not found:
            found = user_defined_Detect(r)
        chassis_ctrl.move_with_distance(-90,1.45)
        # increasing gimbal rotation speed 
        gimbal_ctrl.set_rotate_speed(250)
        gimbal_ctrl.yaw_ctrl(90) # at this point, the gimbal moves all around 
        chassis_ctrl.move_with_distance(-180,1.9)
        if not found:
            found = user_defined_Detect(r)
        chassis_ctrl.move_with_distance(-180,1.9)
    
    else:
        gimbal_ctrl.yaw_ctrl(90)
        chassis_ctrl.move_with_distance(0,1.9)
        if not found:
            found = user_defined_Detect(r)
        chassis_ctrl.move_with_distance(0,1.9)
        gimbal_ctrl.yaw_ctrl(180)
        chassis_ctrl.move_with_distance(90,1.45)
        if not found:
            found = user_defined_Detect(r)
        chassis_ctrl.move_with_distance(90,1.45)
        
        gimbal_ctrl.set_rotate_speed(250)
        gimbal_ctrl.yaw_ctrl(-90)
        chassis_ctrl.move_with_distance(180,1.9)
        if not found:
            found = user_defined_Detect(r)
        chassis_ctrl.move_with_distance(180,1.9)

        chassis_ctrl.move_with_distance(-90,2.9)
    gimbal_ctrl.recenter()
        
def start():
    time.sleep(3)
    intro()
    time.sleep(3)
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    for count in range(8):   # 5 rounds for every game, 3 free rounds for possible errors 
        # at start of each round, robot will count down a from a random number between 1-5
        if(len(vmarker) > 1):
            media_ctrl.play_sound(rm_define.media_custom_audio_3,wait_for_complete_flag = True) # shuffle cards audio
            print("ROUND "+ str(count+1) + " START")
            
            if count+1 == 3:
                media_ctrl.play_sound(rm_define.media_custom_audio_8,wait_for_complete_flag = True) # space out audio 
            rand = random.randint(1,5)
            
            # have LED be a random color for each round, except for green and red, these are reserved for the game
            color = random.choice(list(RGB.keys()))
            while color == "red" or color == "green":
                color = random.choice(list(RGB.keys()))
            set_led_color(color, color, "pulsing")
            for i in range(rand,0,-1):
                media_ctrl.play_sound(rm_define.media_sound_count_down)
                time.sleep(1)
            time.sleep(1)
            # media_ctrl.play_sound(rm_define.media_sound_solmization_2D)
            
            #determining direction 
            randomd = random.randint(1,1000)
            direction = "clockwise" if randomd % 2 == 0 else "anticlockwise"
            print("Direction: "+direction)
            move(direction)
            print("Vmarker size: "+str(len(vmarker)))
            time.sleep(10)
        else:
            conclusion()
            break
    

# last person standing
# play congratulations audio - record that
# victory dance
# ask person to follow them, turn arund and move a bit
# mid move, turn and shoot last perosn standing, and play a gamne over sound
def conclusion():
    gimbal_ctrl.pitch_ctrl(35)
    media_ctrl.play_sound(rm_define.media_custom_audio_7,wait_for_complete_flag = True) # please step forward 
    media_ctrl.play_sound(rm_define.media_custom_audio_5,wait_for_complete_flag = True)
    time.sleep(5)
    # detect the last marker
    user_defined_Detect(picked[0])
    # keep shooting and set leds to random 
    for i in range(5):
        set_led_color(random.choice(list(RGB.keys())), random.choice(list(RGB.keys())), "flashing") #TODO: add like a dance
        gun_ctrl.fire_once()
        time.sleep(1)
    # play game over audio 
    dance()
    gimbal_ctrl.recenter()
    
    media_ctrl.play_sound(rm_define.media_custom_audio_4,wait_for_complete=True) # hahaha
    
def dance(): 
    gun_ctrl.fire_once()
    chassis_ctrl.set_trans_speed(1.5)
    chassis_ctrl.set_rotate_speed(180)
    # chassis_ctrl.move_with_time(0,0.5)
    chassis_ctrl.move_with_distance(0,1)
    chassis_ctrl.move_and_rotate(45,rm_define.anticlockwise)
    time.sleep(1)
    
# NOTES:
# 1. I can make a set list to store values from 1 to 5, pick a random value and remove it after picked. DONE LOL
# 2. more work to be done on conclusion NOT DONE
# 3. spin? at corner man f 
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
# 8. remove picked vs using vmarker
#

        
# POST PRES
# 1. fix the movement issue 
# 2. Maybe a function to center itself at some point or its know position 
# 3. Is it possible to flip the follow mode on the fly? and then find the center 
# 4. More features
# 6. more robust edge cases and all 
# 7. PID controller 
# 8. test w people 
# 9. Add more marquis LEDs, like loading LED when scanning


# talk about: errors, how we fixed, including the 