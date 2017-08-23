# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

from pybpodapi.event_occurrence import EventOccurrence
from pybpodapi.softcode_occurrence import SoftCodeOccurrence


class RawData(object):
	"""
	Stores states and events while trial is running.
	
	:ivar list(int) states: a list of states occurrences indexes
	:ivar list(int) states_timestamps: list of states occurrences timestamps (tuple with start and end)
	:ivar float trial_start_timestamp: trial start timestamp (only updated on trial end)
	:ivar list(EventOccurrence) events_occurrences: list of events occurrences
	"""

	def __init__(self):
		self.states = [0]
		self.state_timestamps = [0]
		self.event_timestamps = []  # see also BpodBase.__update_timestamps
		self.trial_start_timestamp = None  # type: float
		self.events_occurrences = []  # type: list(EventOccurrence)
		self.softcode_occurrences = []  # type: list(SoftCodeOccurrence)

	def add_event_occurrence(self, event_index, event_name, timestamp=None):
		"""
		Event has happened, save occurrence. Creates a new EventOccurrence object and stores it in the events list.

		:param int event_index: index of the event
		:param str event_name: name of the event
		:param float timestamp: optional for now because bpod doesn't send it

		:rtype: EventOccurrence
		"""
		event = EventOccurrence(event_name, event_index, timestamp)

		self.events_occurrences.append(event)

		return event

	def add_softcode_occurrence(self, softcode_number, timestamp=None):
		"""
		SoftCode detected by Bpod's.

		:param int softcode_number: id of the softcode
		:param float timestamp: optional for now because bpod doesn't send it

		:rtype: SoftCodeOccurrence
		"""
		softcode = SoftCodeOccurrence(softcode_number, timestamp)

		self.softcode_occurrences.append(softcode)

		return softcode

	def export(self):
		return {'Trial start timestamp': self.trial_start_timestamp,
		        'States': self.states,
		        'States timestamps': self.state_timestamps,
		        'Events timestamps': [str(event) for event in self.events_occurrences]}

	def __str__(self):
		return str(self.export())