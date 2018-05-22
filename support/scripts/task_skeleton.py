from __future__ import print_function
# -*- coding: utf-8 -*-
#########################################################################
##  QuickERP (May 22, 2017)                                            ## ##                                                                     ##
##  by Mike Cichonski @ Brock Univerity Cognitive and Affective        ##
##  Neuroscience Lab (BUCANL)                                          ## 
##  © 2017 BUCANL / Under supervision of Dr. Sidney Segalowitz         ##
##  Code Written by Mike Cichonski                                     ##
##  Not for distribution or publication without permission of          ##
##  the director of BUCANL.                                            ##
##                                                                     ##
##  file: task_skeleton.py                                             ##
##  This file defines the actual task and order of stimuli. It can     ##
##  define a number of sub-tasks as functions and then call them       ##
##  in a desired order and number of repeats.                          ##
#########################################################################

from psychopy import core, visual, event, gui, monitors
import random
import datetime
import sys

# Instruct sting to be displayed before actual task starts
instructions = """
This task will involve responding to letters. 
Press 'A' when presented with an 'H'. 
Press 'L' when presented with an 'S'.
A period of 30 seconds will preface the task.
Press spacebar to begin.
"""

sync_instructions = """
Connect the photo diode to the monitor and press spacebar to continue, do not
detatch until the next instructions are presented
"""

sync_pattern = [3, .2, .3, .2, .3, .2, .3, .2, .3, .2, .3, .2, .3, .2, .3, .2, .3, \
               .2, .3, .2, .3, .2, .3, .2, .3, .2, .3, .2, .3, .2, .3, .2, .3, .2, \
               .3, .2, .3, .2, .3, .2, .3, .2, .3, .2, .3, .2, .3, .2, .3, .2, .3, \
               .2, .3, .2, .3, .2, .3, .2, .3, .2, .3, .2, .3, .2, .3, .2, .3] # B W B . . .
# In ms of (min,max) resting time between stimulous presentation
resting_interval = (1000, 3000)
presentation_interval = (800, 1200)
# Config option for scaling the fixation cross size
fixation_line_len = 10
# Waiting period in seconds after accepting the instructions
wait_period = 5

# Psychopy config options
monName = 'defMon'
mon = monitors.Monitor(monName)

# Key mapping for correct answers
correct_dict = {"1" : "a", "0" : "l"}
stim_dict = {0 : 'S', 1 : 'H'}
valid_keys = ['a','l']

# Function that takes a random value between resting interval to wait for
def rest_wait():
    val = random.randrange(resting_interval[0], resting_interval[1])
    return float(val)/1000.0

# Function that will display the fixation cross and then clear the screen once done
# To change how long the cross is on screen, change the fixation_duration variable.
def draw_fixation(win, fixH, fixV, blank_stim, wait_duration):
    fixH.draw()
    fixV.draw()
    win.flip()
    core.wait(wait_duration)
    blank_stim.draw()
    win.flip()

# Function that will present stimulus and record data as needed
def present_stim(win, letter, stim_pair, blank_stim, out_file, starttime):
    blank_stim.draw()
    try:
        choice = stim_dict.values().index(letter.strip())
    except ValueError as e:
        raise ValueError('File had invalid character, {}, expected one of {}'\
            .format(letter, stim_dict.values()))

    stim_pair[choice].draw()
    win.flip()

    pre_time, pre_time_datetime = _string_datetime()
    # Block until we receive input, wait for 1s and let it override
    timedelay = random.randrange(*presentation_interval)
    k = event.waitKeys(maxWait=timedelay/1000.0) 

    post_time, post_time_datetime = _string_datetime()

    # Clear the screen upon response
    blank_stim.draw()
    win.flip()
    pret_elapsed = str((pre_time_datetime - starttime).total_seconds())
    postt_elapsed = str((post_time_datetime - starttime).total_seconds())
    # Process input
    if k is not None and 'escape' in k:
        return False
    elif k is not None: # Just in case...
        out_build = [stim_dict[choice], pre_time, pret_elapsed, 
                     post_time, postt_elapsed, k[0]]
        if correct_dict[str(choice)] in k: # Correct response
            out_build.append('right')
        elif k[0] in valid_keys: # Incorrect
            out_build.append('wrong')
        else: # Invalid response
            out_build.append('inval')

        out_file.write(','.join(out_build))
        out_file.write('\n')
    return True

def study_loop(out_file, starttime, pattern):
    # Window setup
    win = visual.Window(monitor=mon, fullscr=True)

    # Fixation cross setup
    fixhor, fixver = _setup_fixation(win)

    # Letters to draw to screen
    hStim = visual.TextStim(win, "H", height=0.5, font='Calibri')
    sStim = visual.TextStim(win, "S", height=0.5, font='Calibri')
	
    instr_stim = visual.TextStim(win, instructions)

        # Blank stim to clear the screen
    blank_stim = visual.Rect(win, units="pix", width=9000, height=9000, 
                            fillColor=[-1,-1,-1])

    # Waiting period
    blank_stim.draw()
    instr_stim.draw()
    win.flip()
    _ = event.waitKeys()

    # Write headers and marker guesses
    out_file.write('stim,presentedTime,presentedTimeElapsed,respondedTime,respondedTimeElapsed,response,correct\n')

    blank_stim.draw()
    draw_fixation(win, fixhor, fixver, blank_stim, wait_period)
    
    for letter in pattern:
        if not present_stim(win, letter, (sStim,hStim), blank_stim, out_file,
                            starttime):
            # Early exit with esc
            break
        core.wait(rest_wait())
    
    win.close()

def synchronize_loop(out_file, starttime):
    """
    This function serves to print a pattern that would help synchronize
    the muse with the output
    """

    # Window setup
    win = visual.Window(monitor=mon, fullscr=True)

    # Blank stim to clear the screen
    white_stim = visual.Rect(win, units="pix", width=9000, height=9000, 
                            fillColor=[1, 1, 1])
    black_stim = visual.Rect(win, units="pix", width=9000, height=9000, 
                            fillColor=[-1, -1, -1])
    black_stim.draw()
    instr_stim = visual.TextStim(win, sync_instructions)
    instr_stim.draw()
    win.flip()
    while not 'space' in event.waitKeys():
        pass
    out_file.write('waitseconds,time,elapsedtime\n')
    # Benchmarking and waiting period
    black = True
    for time in sync_pattern:
        if black:
            black_stim.draw()
        else:
            white_stim.draw()
        black = not black
        win.flip()
        dts, dt = _string_datetime()
        elapsedsec = (dt - starttime).total_seconds()
        out_file.write('{},{},{}\n'.format(time, dts, elapsedsec))
        core.wait(time)

    win.close()

def verify(acqfname):
    """
    This function shows the last 2000 samples in an effort to make it possible
    to validate that the synchronization pulses are present
    """

    # We can import modules into just this function
    import matplotlib
    # Fixes a bug on my system
    #matplotlib.use('Qt4Agg')
    from matplotlib import pyplot
    import numpy as np

    lines = open(acqfname).readlines()
    cols = len(lines[0].split(',')) - 4
    data = np.zeros((len(lines), cols))
    
    for idx, line in enumerate(lines):
        split_lines = line.split(',')
        data[idx,:] = [float(x) for x in split_lines[4:]]

    plotdata = data
    pyplot.plot((plotdata - np.mean(plotdata, axis=0))[:,0], linewidth=0.5)
    pyplot.show()

def _setup_fixation(win):
    fixationHorizontal = visual.Line(win, units="pix", lineColor=[1, 1, 1], 
                                     lineWidth=5)
    fixationHorizontal.start = [-fixation_line_len, 0]
    fixationHorizontal.end = [fixation_line_len, 0]
    fixationVertical = visual.Line(win, units="pix", lineColor=[1, 1, 1],
                                   lineWidth=5)
    fixationVertical.start = [0, -fixation_line_len]
    fixationVertical.end = [0, fixation_line_len]
    return fixationHorizontal, fixationVertical

def _string_datetime():
    t = datetime.datetime.now()
    return t.isoformat(), t

def run(out_file, acqfname, starttime, pattern, in_channel, msg_channel):
    synchronize_loop(out_file, starttime)
    #verify(acqfname)
    study_loop(out_file, starttime, pattern)

