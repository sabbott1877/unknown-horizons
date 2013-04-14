import PyCEGUI

import horizons.globals
from horizons.util.startgameoptions import StartGameOptions


class MainMenu(object):

	def __init__(self):
		self.gui = PyCEGUI.WindowManager.getSingleton().loadWindowLayout("Mainmenu.layout")
		self.gui.hide()

		PyCEGUI.ImagesetManager.getSingleton().createFromImageFile("mm_background", "bg_1.png")
		self.gui.getChild("background").setProperty("Image", "set:mm_background image:full_image")
		self.gui.getChild("startSingleplayer").subscribeEvent(PyCEGUI.PushButton.EventClicked, self, 'start_game')

		horizons.globals.fife.root.addChildWindow(self.gui)

	def start_game(self, args):
		options = StartGameOptions.create_start_scenario("content/scenarios/tutorial_en.yaml")
		horizons.main.start_singleplayer(options)

	def show(self):
		self.gui.show()

	def hide(self):
		self.gui.hide()


class Gui(object):

	def __init__(self):
		self.main = MainMenu()

	def show_main(self):
		self.main.show()

	def show_loading_screen(self):
		pass

	def close_all(self):
		self.main.hide()

	def subscribe(self):
		pass

	def unsubscribe(self):
		pass
