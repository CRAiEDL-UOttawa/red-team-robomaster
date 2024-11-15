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