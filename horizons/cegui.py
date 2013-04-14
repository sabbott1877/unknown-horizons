import PyCEGUI

import horizons.globals

class Gui(object):
	def show_main(self):
		newWindow = PyCEGUI.WindowManager.getSingleton().loadWindowLayout("MyConsole.layout","second_")
		horizons.globals.fife.root.addChildWindow(newWindow)

	def show_loading_screen(self):
		pass

	def close_all(self):
		pass
