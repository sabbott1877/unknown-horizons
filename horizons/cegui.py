import PyCEGUI

import horizons.globals
from horizons.util.startgameoptions import StartGameOptions


class MainMenu(object):

	def __init__(self):
		self.gui = PyCEGUI.WindowManager.getSingleton().loadWindowLayout("Mainmenu.layout")
		self.gui.hide()

		self.gui.getChild("single_button").subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'start_game')
		self.gui.getChild("single_label").subscribeEvent(PyCEGUI.Window.EventMouseClick, self, 'start_game')

	def start_game(self, args):
		options = StartGameOptions.create_start_scenario("content/scenarios/tutorial_en.yaml")
		horizons.main.start_singleplayer(options)

	def show(self):
		self.gui.show()

	def hide(self):
		self.gui.hide()


class Gui(object):

	def __init__(self):
		self.root = PyCEGUI.WindowManager.getSingleton().createWindow("DefaultWindow")
		horizons.globals.fife.root.addChildWindow(self.root)

		self.background = PyCEGUI.WindowManager.getSingleton().createWindow("TaharezLook/StaticImage")
		self.background.setProperty("FrameEnabled", "False")
		self.background.setProperty("Image", "set:content/gui/images/background/mainmenu/bg_1.png image:full_image")
		self.root.addChildWindow(self.background)

		self.main = MainMenu()
		self.root.addChildWindow(self.main.gui)

	def show_main(self):
		self.main.show()

	def show_loading_screen(self):
		pass

	def close_all(self):
		self.root.hide()

	def subscribe(self):
		pass

	def unsubscribe(self):
		pass
