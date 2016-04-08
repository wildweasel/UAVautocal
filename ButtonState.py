# Matt Kaplan 
# CISC 849 -  Spring '16

from enum import Enum

# Simple encapsulation of button state for UAV stepping
class ButtonState():

	class State(Enum):
		INIT = 0
		LOADED = 1
		RUNNING = 2
		PAUSED = 3
	
	def __init__(self, button1, button2):
		self.button1 = button1
		self.button2 = button2		
		self.setState(ButtonState.State.INIT)
			
	def setState(self, newState):
		self.state = newState
		if newState == ButtonState.State.INIT:
			self.button1.config(text='Load', state="normal")
			self.button2.config(text='Run', state="disabled")
		if newState == ButtonState.State.LOADED:
			self.button1.config(text='Load', state="normal")
			self.button2.config(text='Run', state="normal")
		if newState == ButtonState.State.RUNNING:
			self.button1.config(text='Pause', state="normal")
			self.button2.config(text='Run', state="disabled")	
		if newState == ButtonState.State.PAUSED:
			self.button1.config(text='Reset', state="normal")
			self.button2.config(text='Run', state="normal")	
		
	def getState(self):
		return self.state
