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

		extrude = cmds.polyExtrudeFacet(localTranslateZ = length)[0]
    
		
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
