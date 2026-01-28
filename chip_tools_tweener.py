from maya import cmds


def tween(percentage, obj = None, Attrs = None, selection = True):
    
    ####################################################

    #if obj is not given and selection is set to false, error early
    if not obj and not selection:
        raise ValueError("No object given to tween")
    
    #if no obj is specified, get from frist selection
    if not obj:
        obj = cmds.ls(selection = True)[0]
    
    if not Attrs:
        attrs = cmds.listAttr(obj, keyable = True)
    ###################################################

    current_time = cmds.currentTime (query = True)

    for attr in attrs:
        
        #initialize values in the scope of this loop

        
        attr_full = "%s.%s" % (obj, attr) #construct the full name of the Attribute with it object
        keyframes = cmds.keyframe(attr_full, query = True) #get keyframes of attr on object
        

        
        if not keyframes: #if attr has no keyframes, ignore it
            continue



        previous_keyframes = [frame for frame in keyframes if frame < current_time]  #stores the previous keyframe in a list
        later_keyframes = [frame for frame in keyframes if frame > current_time] #stores the later keyframe in a list




        previous_frame = max(previous_keyframes) if previous_keyframes else None
        next_frame = min(later_keyframes) if later_keyframes else None

        if not previous_frame or not next_frame:
            continue

        previous_value = cmds.getAttr(attr_full, time = previous_frame)
        next_value = cmds.getAttr(attr_full, time = next_frame)

        difference = next_value - previous_value
        weighted_difference = (difference * percentage) / 100.0
        current_value = previous_value + weighted_difference

        cmds.setKeyframe(attr_full, time = current_time, value = current_value)
