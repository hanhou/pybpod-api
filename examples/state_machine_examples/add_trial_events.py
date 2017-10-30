# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Demonstration of AddTrialEvents used in a simple visual 2AFC session.
AddTrialEvents formats each trial's data in a human-readable struct, and adds to myBpod.data (to save to disk later)
Connect noseports to ports 1-3.

Example adapted from Josh Sanders' original version on Sanworks Bpod repository
"""

import random

from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
from pybpodapi.bpod.hardware.events import EventName
from pybpodapi.bpod.hardware.output_channels import OutputChannel



my_bpod = Bpod()

nTrials = 100
trialTypes = [1, 2]  # 1 (rewarded left) or 2 (rewarded right)

dosomething = True

for i in range(nTrials):  # Main loop
	print('Trial: ', i + 1)

	thisTrialType = random.choice(trialTypes)  # Randomly choose trial type
	if thisTrialType == 1:
		stimulus = OutputChannel.PWM1  # set stimulus channel for trial type 1
		leftAction = 'Reward'
		rightAction = 'Punish'
		rewardValve = 1
	elif thisTrialType == 2:
		stimulus = OutputChannel.PWM3  # set stimulus channel for trial type 1
		leftAction = 'Punish'
		rightAction = 'Reward'
		rewardValve = 3

	sma = StateMachine(my_bpod)

	sma.add_state(
		state_name='WaitForPort2Poke',
		state_timer=1,
		state_change_conditions={EventName.Tup: 'FlashStimulus'},
		output_actions=[(OutputChannel.PWM2, 255)])
	sma.add_state(
		state_name='FlashStimulus',
		state_timer=0.1,
		state_change_conditions={EventName.Tup: 'WaitForResponse'},
		output_actions=[(stimulus, 255)])
	if dosomething:
		sma.add_state(
			state_name='WaitForResponse',
			state_timer=1,
			state_change_conditions={EventName.Tup: leftAction, EventName.Port3In: rightAction},
			output_actions=[])
	else:
		sma.add_state(
			state_name='WaitForResponse',
			state_timer=1,
			state_change_conditions={EventName.Tup: leftAction, EventName.Port3In: rightAction},
			output_actions=[])
	sma.add_state(
		state_name='Reward',
		state_timer=0.1,
		state_change_conditions={EventName.Tup: 'exit'},
		output_actions=[(OutputChannel.Valve, rewardValve)])  # Reward correct choice
	sma.add_state(
		state_name='Punish',
		state_timer=3,
		state_change_conditions={EventName.Tup: 'exit'},
		output_actions=[(OutputChannel.LED, 1), (OutputChannel.LED, 2), (OutputChannel.LED, 3)])  # Signal incorrect choice

	my_bpod.send_state_machine(sma)  # Send state machine description to Bpod device

	print("Waiting for poke. Reward: ", 'left' if thisTrialType == 1 else 'right')

	my_bpod.run_state_machine(sma)  # Run state machine

	print("Current trial info: {0}".format(my_bpod.session.current_trial))


my_bpod.stop()  # Disconnect Bpod
