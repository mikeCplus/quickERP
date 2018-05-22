from future import print_function
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
##  file: objects.py                                                   ##
##  This file contains all the objects used in the experiment.         ##
##  This contains Event, Block, Participant, Montage, and Experiment   ##
##                                                                     ##
#########################################################################

import json

ROOT_PROJECT_PATH = '../../'

### DEFINE: Event ###
class Event:
    '''A single "event" - includes two stimuli, result, and reaction time'''

    def __init__(self,name,latency):
        "creates a new instance of an Event"
        '''
        name is the event name
        latency is the event latency in ms since the start of the recording'''
        self.name = name
        self.latency = float(latency)

    def jsonify(self):
        return {'name':self.name,'latency',self.latency}

### END: Event ###


### DEFINE: Block ###
class Block:
    '''A block (or 'pattern') of Events'''
       
    def __init__(self,name,events=[]):
        "creates a new instance of a block of events'
        self.name = name
        self.events = events

    def __init__(self,name='',events=[]):
        "creates a new instance of a block of events'
        self.name = self.next_name()
        self.events = events

    def addEvent(self,event):
        '''add a single event to the block
        indices will adjust accordingly based on latency'''
        if self.events==[]: self.events.append(event)
        for i,e in enumerate(self.events):
            if event.latency>=e.latency:
                self.events.insert(i,event)
                break
    
    
    def nextName(self,digits=3)
        ''' digits represents how many different possible 
        participant numbers you can have'''
        if not hasattr(nextName,'nextName') and '
        if not hasattr(nextName,'num'):
            self.num = 0
            self.nextName = '000'
        num_len = len(str(self.num))
        self.nextName = '0'*(digits-num_len)+str(self.num)
        return self.nextName
        

    def jsonify(self):
        j_events = [e.jsonify() for e in self.events]
        return {'events',j_events}


### END: Block ###

### DEFINE: Participant ###
class Participant:
    '''a participant in the study.'''

    def __init__(self, name, sex, age, block_order):
        "creates a new instance of a participant"
        self.name = name
        self.sex = sex
        self.age = age
        self.block_order = block_order # index of orders of presented blocks

    def jsonify(self):
        return {'name':self.name,'sex':self.sex,'age':self.age,'block_order':block_order}

### END: Participant ###

### DEFINE: Montage ###
class Montage:
    '''An dictionary object defining a scalp montage'''

    def __init__(self,m_filename):
        "initializes a montage based on the file type given"
        self.electrodes = {}
        if os.path.splitext(m_filename)[1]=='sfp':
            __init_sfp(m_filename)
        else if os.path.splitext(m_filename)[1]=='elc':
            __init_elc(m_filename)

    def __init_sfp(self,montage):
        fid = open(montage,'r')
        lines=fid.readlines()
        fid.close()
        electrodes = {}
        for line in lines:
            [ch,x,y,z] = line.split(' ')
            self.electrodes[ch] = [float(x),float(y),float(z)]
        
    def __init_elc(self,montage):
        fid = open(montage,'r')
        lines=fid.readlines()
        fid.close()
        electrodes = {}
        rec_pos = False # set to true when recording positions
        rec_lab = False # set to true when recording labels
        pos = []
        lab = []
        
        for line in lines:
            if line=='Positions':
                rec_pos = True
                continue
            if rec_pos:
                pos.append([float(item) in line.spilt(' ')])
            if line=='Labels':
                rec_pos = False
                rec_lab = True
                continue
            if rec_lab:
                line = line.strip(' ')
                if line!='':
                    loc.append(line)
        
        if len(pos!=len(lab)):
            print('ERROR: cannot import'+ montage + '\n' +
                  'Make sure number of Positions matches number of Labels.')
            os.exit(0)
        
        self.electrodes = {}
        for i,l in enumerate(lab)
            self.electrodes[l] = pos[i]

        def jsonify(self):
            return self.electrodes

### END: Montage ###

### DEFINE: Experiment ###
class Experiment:
    '''contains a name, all participants, events, and montage(s) in an experiment'''

    def __init__(self,name,participants,blocks,montage):
        "loads an instance of Experiment"
        self.name = name # name of the experiment
        self.participants = participants
        self.blocks = blocks # will be a list of Block objects
        self.montage = montage # will be a list of one or more Montage objects
        # if one montage present, the same montage is assumed for all participants

    def __init__(self,name,participants=[],events=[],montage=[]):
        "creates a new empty instance of Experiment"
        self.name = name # name of the experiment        
        self.participants = participants
        self.blocks = blocks # will be a list of Block objects
        self.montage = montage # will be a list of one or more Montage objects
        # if one montage present, the same montage is assumed for all participants

    def __init__(self,name='exp'participants=[],events=[],montage=[]):
        "creates a new empty instance of Experiment named 'exp' by default"
        self.name = name
        self.participants = participants
        self.blocks = blocks # will be a list of block objects
        self.montage = montage # will be a list of one or more Montage objects
        # if one montage present, the same montage is assumed for all participants

    #---Participant---#
    def addParticipant(self, participant):
        "adds a participant to the list"
        #as long as participant isn't already in the participants list...
        if not self.__containsPart(participant.name):
            self.participants.append(participant) #add participant
        else: #otherwise, overwrite the participant with new data
            self.participants[self.__partWithName(participant.name)] = participant
        return self # to enabe cascading

    def __containsPart(self, name):
        "checks if participant with name is in the list"
        for p in self.participants:
            if p.name == name:
                return True
        return False

    def __partWithName(self, name):
        "returns index number of participant with name equal to self.name" 
        for index, p in enumerate(self.participants):
            if p.name == name:
                return index
        return False

    #---Event---#
    def addEvent(self,name,latency):
        "adds an event to the list at the specified latency; indices will adjust accordingly"
        ev = Event(name,latency)
        if self.events == []: self.events.append(ev)        
        for i,e in enumerate(self.events):
            if ev.latency>=self.events[i].latency:
                self.events.insert(i,ev)
        return self        

    #---Montage---#
    def addMontage(self,montage):
    '''adds a montage to the experiment
     montage is a string representing the name of the file''' 
        m = Montage(montage)
        self.montage.append(m)
        return self

    #---Save the current Experiment---#
    def jsonify(self):
        ''' saves the entire experiment as a json file'''
        
        data = {{'name':self.name}}
        for p in self.participants:
            data['participants'] = jsonify(p);
        for b in self.blocks:
            data['blocks'] = jsonify(b);
        for m in self.montage:
            data['montage'] = jsonify(m);
        with open(ROOT_PROJECT_PATH+self.name+'.exp','w',encoding='utf-8') as out:
            return json.dump(data,out)

### END: Experiment ###
