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
        cmds.refresh(force=True)

class tween_window(object) :
    
    def __init__(self):
        self.window_name = "Tweener"
        
    def show(self):
        
        if cmds.window(self.window_name, query = True, exists = True):
            cmds.deleteUI(self.window_name)


        cmds.window(self.window_name, sizeable = True)
        

        self.build_ui()


        cmds.showWindow()
        cmds.window(self.window_name, edit=True, widthHeight=(600, 100))


    def build_ui(self):
        

        column = cmds.columnLayout(adjustableColumn=True)
        cmds.text(label="Use the slider to set the tween amount")

        row = cmds.rowLayout(numberOfColumns = 2)

        self.slider = cmds.floatSlider(width = 398, min = 0, max = 100, value = 50, step = 1, changeCommand = tween)

        reset_button = cmds.button(label = "Reset", command = self.reset, width = 198)

        cmds.setParent('..')  # leave rowLayout

        cmds.rowLayout(numberOfColumns=3)

        one_quarter_button = cmds.button(label = "Favor Left", command = lambda *args: tween(25), width = 198)
        half_button = cmds.button(label = "Middle", command = lambda *args: tween(50), width = 198)
        three_quarters_button = cmds.button(label = "Favor Right", command = lambda *args: tween(75), width = 198)

        cmds.setParent(column)

        cmds.button(label = "Close", command = self.close)


        

    def reset(self, *args):
        cmds.floatSlider(self.slider, edit = True, value = 50)

        
    def close(self, *args):
        cmds.deleteUI(self.window_name)

tween_window().show()
