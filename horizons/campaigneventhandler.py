# ###################################################
# Copyright (C) 2009 The Unknown Horizons Team
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

import os.path
import yaml

from horizons.constants import RES

from horizons.scheduler import Scheduler

class InvalidScenarioFileFormat(Exception):
	def __init__(self, msg=None):
		if msg is None:
			msg = "Invalid campaign file."
		super(InvalidScenarioFileFormat, self).__init__(msg)


class CampaignEventHandler(object):
	"""Handles event, that make up a campaign. See wiki."""

	def __init__(self, session, campaignfile = None):
		"""
		@param session: Session instance
		@param campaignfile: yaml file that describes the campaign
		@throws Exception on yaml parse error
		"""
		self.session = session
		self._events = []
		if campaignfile:
			self._data = self._parse_yaml_file(campaignfile)
			for event_dict in self._data['events']:
				self._events.append( _Event(self.session, event_dict) )
		# Add the check_events methode to the scheduler to be checked evrey two seconds
		Scheduler().add_new_object(self.check_events, self, runin = Scheduler().get_ticks(2), loops = -1)

	def schedule_check(self):
		"""Schedules a check on the next tick. Prefer this over check_events, so that no lags appear."""
		Scheduler().add_new_object(self.check_events, self)

	def check_events(self):
		"""Checks whether an event happened"""
		events_to_remove = []
		for event in self._events:
			event_executed = event.check()
			if event_executed:
				events_to_remove.append(event)
		for event in events_to_remove:
			self._events.remove(event)

	def get_map_file(self):
		return self._data['mapfile']

	@classmethod
	def get_description_from_file(cls, filename):
		"""Returns the description from a yaml file"""
		return cls._parse_yaml_file(filename)['description']

	@staticmethod
	def _parse_yaml_file(filename):
		try:
			return yaml.load( open(filename, 'r') )
		except: # catch anything yaml might throw
			raise InvalidScenarioFileFormat()


###
# Campaign Actions

def show_message(session, message_id):
	"""Shows a message on the ingame message widget"""
	session.ingame_gui.message_widget.add(None, None, message_id)

def do_win(session):
	"""Called when player won"""
	show_message(session, 'YOU_HAVE_WON')

def do_lose(session):
	"""Called when player lost"""
	#session.gui.show_popup("You lost!", "You have lost. Please give us money so we can create a better 'you have lost'-message")
	pass

###
# Campaign Conditions

def settlements_num_greater(session, limit):
	"""Returns whether the number of settlements owned by the human player is greater than limit."""
	player_settlements = filter(lambda x: x.owner == session.world.player, session.world.settlements)
	return len(player_settlements) > limit

def settler_level_greater(session, limit):
	"""Returns wheter the max level of settlers is greater than limit"""
	return (session.world.player.settler_level > limit)

def player_gold_greater(session, limit):
	"""Returns whether the player has more gold then limit"""
	return (session.world.player.inventory[RES.GOLD_ID] > limit)

def player_gold_less(session, limit):
	"""Returns whether the player has less gold then limit"""
	return (session.world.player.inventory[RES.GOLD_ID] < limit)

###
# Simple utility classes

class _Event(object):
	"""Internal data structure representing an event."""
	def __init__(self, session, event_dict):
		self.session = session
		self.actions = []
		self.conditions = []
		for action_dict in event_dict['actions']:
			self.actions.append( _Action(action_dict) )
		for cond_dict in event_dict['conditions']:
			self.conditions.append( _Condition(session, cond_dict) )

	def check(self):
		for cond in self.conditions:
			if not cond():
				return False
		for action in self.actions:
			action(self.session)
		return True


class _Action(object):
	"""Internal data structure representing an ingame campaign action"""
	action_types = {
	  'message': show_message,
	  'win' : do_win,
	  'lose' : do_lose
	  }

	def __init__(self, action_dict):
		self.callback = self.action_types[ action_dict['type'] ]
		self.arguments = action_dict['arguments'] if 'arguments' in action_dict else []

	def __call__(self, session):
		self.callback(session, *self.arguments)


class _Condition(object):
	"""Internal data structure representing a condition"""
	condition_types = {
	  'settlements_num_greater' : settlements_num_greater,
	  'settler_level_greater' : settler_level_greater,
	  'player_gold_greater': player_gold_greater,
	  'player_gold_less': player_gold_less
	}
	def __init__(self, session, cond_dict):
		self.session = session
		self.callback = self.condition_types[ cond_dict['type'] ]
		self.arguments = cond_dict['arguments'] if 'arguments' in cond_dict else []

	def __call__(self):
		return self.callback(self.session, *self.arguments)

