from pygame import joystick
from pygame import JOYAXISMOTION, JOYBUTTONDOWN, JOYBUTTONUP

class XboxControllers:

	def __init__(self):
		joystick.init()
		self.count = joystick.get_count()
		self.joysticks = []
		for i in xrange(self.count):
			controller = XboxController(i)
			self.joysticks.append(controller)

class XboxController:

	# Controller button/axis indexes
	# Specific to the Xbox One!

	# Right Joystick
	horiz_axis_right = 2
	vert_axis_right = 3
	right_button = 6

	# Left Joystick
	horiz_axis_left = 0
	vert_axis_left = 1
	left_button = 7

	# ABXY buttons
	a_button = 11
	b_button = 12
	x_button = 13
	y_button = 14

	# D pad buttons
	d_up = 0
	d_down = 1
	d_left = 2
	d_right = 4

	# initialize the ith joystick
	def __init__(self, idx=0):
		if (idx < joystick.get_count()):
			self.controller = joystick.Joystick(idx)
			self.controller.init()
			self.id = idx

    # AXIS VALUE INTERFACE
	def getdX_right(self):
		return self.getAxisVal(2)

	def getdY_right(self):
		return self.getAxisVal(3)

	def getdX_left(self):
		return self.getAxisVal(0)

	def getdY_left(self):
		return self.getAxisVal(1)

	# BUTTON VALUE INTERFACE
	def getAButton(self):
		return self.getButtonVal(11)

	def getBButton(self):
		return self.getButtonVal(12)

	def getXButton(self):
		return self.getButtonVal(13)

	def getYButton(self):
		return self.getButtonVal(14)

	def getDDown(self):
		return self.getButtonVal(1)

	def getDUp(self):
		return self.getButtonVal(0)

	# GENERAL Up/Down MOVEMENT
	# includes d-pad, and either joystick
	def isUp(self):
		dpad = self.getDUp();
		joystick_left = (self.getdY_left() < -0.5)
		joystick_right = (self.getdY_right() < -0.5)
		return (dpad or joystick_left or joystick_right)

	def isDown(self):
		dpad = self.getDDown();
		joystick_left = (self.getdY_left() > 0.5)
		joystick_right = (self.getdY_right() > 0.5)
		return dpad or joystick_left or joystick_right

    # returns the not currently snap-corrected axis value
	def getAxisVal(self, idx):
		return self.stick_center_snap(self.controller.get_axis(idx))

	# returns the snap-corrected button's value
	def getButtonVal(self, idx):
                print self.controller.get_button(idx)
		return self.controller.get_button(idx)

	def stick_center_snap(self, value, snap=0.2):
		# Feeble attempt to compensate for calibration and loose stick.
		if value >= snap or value <= -snap:
			return value
		else:
			return 0.0
