# Game logic for detecting a randomly selected vision marker within a set time range
# Borrowed logic from 'app_vision_marker.py'

vmarker_af = ['AUDIO1', 'AUDIO2', 'AUDIO3']
vmarker = [2,3,5]

# Dictionary makes command calls easier
vmarker_dict = {2:rm_define.cond_recognized_marker_number_two, 3: rm_define.cond_recognized_marker_number_three, 5:rm_define.cond_recognized_marker_number_five}
        
def shoot_one_lazer():
    led_ctrl.gun_led_on()
    ir_blaster_ctrl.fire_once()
    led_ctrl.gun_led_off()
    media_ctrl.play_sound(rm_define.media_sound_shoot)

def detect_vmarker(vmarker, simon_says:bool, round_time):
    # Set camera exposure to low for better detection
    media_ctrl.exposure_value_update(rm_define.exposure_value_small)

    # Get robomaster call from dict
    vmarker_cmd = vmarker_dict.get(vmarker)

    # timer
    tools.timer_ctrl(rm_define.timer_start)

    while tools.timer_current() < round_time:

        # If vmarker is detected
        if vision_ctrl.check_condition(vmarker_cmd):

            # If Simon didn't say, player loses
            if simon_says:
                # led light changes to green
                led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 0, 255, 0, rm_define.effect_always_on)
                media_ctrl.play_sound(rm_define.media_sound_recognize_success, wait_for_complete=True)
                # robot moves forward by 1 meter
            
            else:
                led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_always_on)
                shoot_one_lazer()
    

        # Timer ended, no vmarker detected
        # Simon didn't say... (win)
        if tools.timer_current() > 10 & (not simon_says):
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 0, 255, 0, rm_define.effect_always_on)

        # Simon did say... (lose)
        elif tools.timer_current() > 10:
            
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_always_on)
            # TODO - What occurs when vmarker not detected and simon didn't say
            shoot_one_lazer()
    
    tools.timer_ctrl(rm_define.timer_reset)

def start():
    #TODO find optimal camera settings for identification in regards to game area

    # vision detection enabled
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    # max distance 
    vision_ctrl.set_marker_detection_distance(1)