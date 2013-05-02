# ###################################################
# Copyright (C) 2008-2013 The Unknown Horizons Team
# team@unknown-horizons.org
# This file is part of Unknown Horizons.
#
# Unknown Horizons is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ###################################################

from horizons.component import Component


class InventoryOverlayComponent(Component):
	"""Display different additional graphics ("animation overlays" in FIFE terminology)
	depending on inventory status of a building or unit.
	"""
	NAME = "inventoryoverlay"
	DEPENDENCIES = ['StorageComponent']

	def __init__(self, overlays=None, properties=None):
		"""
		"""
		super(InventoryOverlayComponent, self).__init__()
		self.overlays = overlays or {}
		self.properties = properties

	@property
	def fife_instance(self):
		return self.instance._instance

	def initialize(self):
		super(InventoryOverlayComponent, self).initialize()

		print self.fife_instance, self.overlays
		print self.instance, self.instance._action

		aset = self.overlays.keys()[0]
		for (res, overlay_order) in self.overlays[aset].iteritems():
			for (amount, overlay_set) in sorted(overlay_order):
				print res, amount, overlay_set

		# 'idle_as_lumberjack_barrack0'
		identifier = str(self.instance._action) + '_' + str(aset)
		print identifier

		return

		# True: also convert color overlays attached to base frame(s) into animation
		self.fife_instance.convertToOverlays(identifier, True)

		for rotation in range(45, 360, 90):
			pass
			#ov_file = overlay_set[rotation].keys()[0]
			#ov_img = horizons.globals.fife.imagemanager.load(ov_file)
			#ov_anim = Actionsets[overlay_action]

	def load(self, db, worldid):
		super(InventoryOverlayComponent, self).load(db, worldid)
		self.initialize()

	def remove(self):
		#TODO
		# Convert animation overlay on drawing order 0
		# back to plain "action set" in UH terminology
		super(InventoryOverlayComponent, self).remove()
