from maya import cmds


class gear_object(object):

	def __init__(self):
		self.transform = None
		self.extrude = None
		self.constructor = None
	
	
	def create_gear(self, teeth = 10, length = 0.3):
		spans = teeth * 2
		self.transform, self.constructor = cmds.polyPipe(subdivisionsAxis = spans)
		sideFaces = range(spans * 2, spans * 3, 2)

		cmds.select (clear = True)

		for face in sideFaces :
			cmds.select("%s.f[%s]" % (self.transform, face), add = True)

		self.extrude = cmds.polyExtrudeFacet(localTranslateZ = length)[0]
    
		
	def change_teeth(self, teeth = 10, length = 0.3) :
		spans = teeth *2

		cmds.polyPipe(self.constructor, edit = True, subdivisionsAxis = spans)

		sideFaces = range(spans * 2, spans * 3, 2)
		faceNames = []

		for face in sideFaces:
			faceName = 'f[%s]' % (face)
			faceNames.append(faceName)

		cmds.setAttr ('%s.inputComponents' % (self.extrude), len(faceNames), *faceNames, type = "componentList")

		cmds.polyExtrudeFacet(self.extrude, edit = True, ltz = length)

class gear_window(object) :
    
    def __init__(self):
        self.window_name = "gearCreator"
        self.gear = gear_object()


        
    def show(self):
        
        if cmds.window(self.window_name, query = True, exists = True):
            cmds.deleteUI(self.window_name)


        cmds.window(self.window_name, sizeable = True)
        

        self.build_ui()


        cmds.showWindow()
        cmds.window(self.window_name, edit=True, widthHeight=(600, 100))


    def build_ui(self):
        slider_value = 15

        def create_button(name, value = 10):
            cmds.button(label = name, command = lambda *args: self.gear.create_gear(value), width = 198)

        column = cmds.columnLayout(adjustableColumn=True)
        cmds.text(label="Use the slider to set the amount of teeth in the gear")

        self.slider_label = cmds.text("slider value is %s" % slider_value)

        row = cmds.rowLayout(numberOfColumns = 3)

        cmds.button(label = "<", command = self.decrement_slider)
        
        self.slider = cmds.floatSlider(width = 398, min = 1, max = 30, value = 15, step = 1, changeCommand = self.update_teeth_from_slider)
        cmds.button(label = ">", command = self.incriment_slider)
        
        
        cmds.setParent(column)
        creator_button = create_button("create", 10)
        cmds.button(label = "Close", command = self.close)

    def warning_msg(self, *args):
         if self.gear.transform is None:
            cmds.warning("create the gear first")
            return True
         return False
         

    def update_teeth_from_slider(self, *args):
        if self.warning_msg() : return
        
        teeth_value = cmds.floatSlider(self.slider, query = True, value = True)
        teeth_value = int(teeth_value) 

        cmds.text(self.slider_label, edit = True, label = "slider value is %s" % teeth_value)
        self.gear.change_teeth(teeth_value)


    def decrement_slider(self, *args):
        if self.warning_msg() : return
        current = int(cmds.floatSlider(self.slider, query = True, value = True))
        new_value = max(1, current - 1)
        cmds.floatSlider(self.slider, edit = True, value = new_value)
        self.update_teeth_from_slider()

    def incriment_slider(self, *args):
        if self.warning_msg(): return
        current = int(cmds.floatSlider(self.slider, query = True, value = True))
        new_value = min(30, current + 1)
        cmds.floatSlider(self.slider, edit = True, value = new_value)
        self.update_teeth_from_slider()

    def reset(self, *args):
        cmds.floatSlider(self.slider, edit = True, value = 10)

        
    def close(self, *args):
        cmds.deleteUI(self.window_name)
        
gear_window().show()