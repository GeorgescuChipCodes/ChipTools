from maya import cmds


class gear_object(object): # initiate gear object class

#Initiate the code block 

	def __init__(self):
		self.transform = None
		self.extrude = None
		self.constructor = None
	
#crete gear method	
	def create_gear(self, teeth = 15, length = 0.3):
		spans = teeth * 2
		self.transform, self.constructor = cmds.polyPipe(subdivisionsAxis = spans)
		sideFaces = range(spans * 2, spans * 3, 2)

		cmds.select (clear = True)

		for face in sideFaces :
			cmds.select("%s.f[%s]" % (self.transform, face), add = True)

		self.extrude = cmds.polyExtrudeFacet(localTranslateZ = length)[0]
    
# change teeth method		
	def change_teeth(self, teeth = 10, length = 0.3) :
		spans = teeth *2
        
		cmds.polyPipe(self.constructor, edit=True, subdivisionsAxis=spans)
        

        
        

		sideFaces = range(spans * 2, spans * 3, 2)
          
        
		faceNames = []

		for face in sideFaces:
			faceName = 'f[%s]' % (face)
			faceNames.append(faceName)

		cmds.setAttr ('%s.inputComponents' % (self.extrude), len(faceNames), *faceNames, type = "componentList")

		cmds.polyExtrudeFacet(self.extrude, edit = True, ltz = length)
    
    
class gear_window(object) : # initiate the UI class
    
    #Initiate the code block
    def __init__(self):
        self.window_name = "gearCreator"
        self.gear = gear_object()


    # Method to show the window  
    def show(self):
        
        if cmds.window(self.window_name, query = True, exists = True):
            cmds.deleteUI(self.window_name)


        cmds.window(self.window_name, sizeable = True)
        

        self.build_ui()


        cmds.showWindow()
        cmds.window(self.window_name, edit=True, widthHeight=(600, 100))

    # Method to build the UI
    def build_ui(self):
        slider_value = 15

        def create_button(name, value = 10):
            cmds.button(label = name, command = lambda *args: self.gear.create_gear(value), width = 198)

        column = cmds.columnLayout(adjustableColumn=True)
        cmds.text(label="Use the slider to set the amount of teeth in the gear")


        row = cmds.rowLayout(numberOfColumns = 3)

        
        
        cmds.button(label = "create", command = lambda *args: self.gear.create_gear(int(cmds.floatSlider(self.slider, q=True, value=True))), width = 130)
        self.teeth_field = cmds.textFieldButtonGrp( label='teeth: ', text="", buttonLabel='Change Teeth', buttonCommand= self.apply_teeth_from_field )

        cmds.setParent(column)

        self.divider_text = cmds.text("----------------------------------------------")
        self.slider = cmds.floatSlider(width = 398, min = 1, max = 30, value = 15, step = 1, changeCommand = self.update_teeth_from_slider)
        self.slider_label = cmds.text("slider value is %s" % slider_value)

       
    # catch all warning method
    def warning_msg(self, *args):
         if self.gear.transform is None: # check if gear exists
            cmds.warning("create the gear first")
            return True
         return False
         
    # method to update teeth from slider
    def update_teeth_from_slider(self, *args):
        if self.warning_msg() : return
        
        teeth_value = cmds.floatSlider(self.slider, query = True, value = True)
        teeth_value = int(teeth_value) 

        cmds.text(self.slider_label, edit = True, label = "slider value is %s" % teeth_value)
        self.gear.change_teeth(teeth_value)

    # method to apply teeth from text field
    def apply_teeth_from_field(self, *args):
         

         if self.warning_msg() : return # check for warning


         text_value = cmds.textFieldButtonGrp(self.teeth_field, query = True, text = True)


         try: # try to convert to integer
              teeth_value = int(text_value)
         except:   
              cmds.warning("please enter an integer value")
              return
         

         teeth_value = max(1, min(30, teeth_value)) # clamp value between 1 and 30 and store it in a local variable

         cmds.floatSlider(self.slider, edit = True, value = teeth_value) # update slider to match text field

         cmds.text(self.slider_label, edit = True, label = "slider value is %s" % teeth_value) # update label to match text field

         self.gear.change_teeth(teeth_value) # call change teeth method from gear object class
    



    # method to reset the slider
    def reset(self, *args):
        cmds.floatSlider(self.slider, edit = True, value = 10)

    # method to close the window   
    def close(self, *args):
        cmds.deleteUI(self.window_name)


        
gear_window().show()