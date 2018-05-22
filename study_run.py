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
##  file: study_run.py                                                 ##
##  Runs the study once the participant, paradigm, and equipment are   ##
##  set up. More documentation on this to come. This is the main file. ##
#########################################################################

from __future__ import print_function
import os, sys
import datetime

# Local files
from scripts import objects as obj
from scripts import task_skeleton
from scripts import acquire
from scripts import gui

# Python packages
from multiprocessing import Queue, Process

# relative paths
pattern_path = 'task/patterns'
out_path     = 'output'

# prefixes
sub_pref = 'sub-'     # study prefix
pat_pref = 'pat_'     # pattern prefix

# suffixes
acq_suff = '_acq.csv' # acquisition suffix
tsk_suff = '_tsk.csv' # task suffix
log_suff = '_log.log' # log suffix

# Wraps the acquire subprogram so we can use it as a subprocess without
# giving up our ability to catch exceptions
def acq_wrap(acqfname, logfname, sub_path, starttime, in_channel, msg_channel, start_muse=False):

    acqfid = open(acqfname, 'w')
    logfid = open(logfname, 'w')
    if start_muse:
        prog = acquire.start_muse()
    try:
        acquire.start_acquisition(acqfid, logfid, sub_path, starttime, in_channel, msg_channel)
    except Exception as e:
        print(e)
        print('acq_wrap exit')
        if start_muse:
            acquire.close_muse(prog)
    acqfid.close()
    logfid.close()

def start_study():

    obj = Experiment(
    gui.display()
    
    print('Participant Id: ', end='')
    sub_id = raw_input()

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    sub_path = out_path+'/'+sub_pref+sub_id+'_'+str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    if not os.path.exists(sub_path):
        os.makedirs(sub_path)

    acqfname = sub_path +'/'+str(sub_pref)+str(sub_id)+str(acq_suff)
    logfname = sub_path +'/'+str(sub_pref)+str(sub_id)+str(log_suff)

    print('Pattern number[0-4]: ', end='')
    patternfname = raw_input()

    patf = open ('/'.join([pattern_path,pat_pref+str(patternfname)+'.txt']), 'r')
    pattern = patf.readlines()
    patf.close() 
  
    # Channels to use for communication across subprocess 
    in_channel = Queue()
    msg_channel = Queue()
    
    start_muse = True
    # For environments where we cannot start muse from Python
    # If you want to start muse from python comment the line below
    start_muse = False
    
    starttime = datetime.datetime.now()
    acqp = Process(target=acq_wrap, args=(acqfname, logfname, sub_path,
                   starttime,in_channel, msg_channel, start_muse))
    acqp.start()

    # Blocks until msg_channel has a message
    msg = msg_channel.get()

    # msg will be (True/False, <msg>)
    # msg[0] will be True iff we are ready to record
    if not msg[0]:
        print('Error starting acq subprocess', msg[1], sep=',')
        exit(1)

    with open(sub_pref + sub_id + tsk_suff, 'w') as task_fid:
        task_skeleton.run(task_fid, acqfname, starttime, pattern, 
                          in_channel, msg_channel)

    # Request subprocess exit
    in_channel.put('close')

    acqp.join()
    print('done')

if __name__ == '__main__':
    start_study()
