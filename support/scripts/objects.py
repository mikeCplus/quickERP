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

import os
import json
from random import shuffle

ROOT_PROJECT_PATH = '../../'

### DEFINE: Event ###
class Event:
    '''A single 'Event' - includes a name and a latency'''

    def __init__(self,name,latency):
        '''creates a new instance of an Event
        name:    the event name
        latency: the event latency in ms since the start of the recording'''
        self.name = str(name)        
        self.latency = float(latency)
        self.index = -1 # will be given a positive value once added to block

    def jsonify(self,save=True):
        event = {self.name:self.latency} 
        if save:
            savedir = ROOT_PROJECT_PATH+'task/paradigms/events/'
            if not os.path.exists(savedir):
                os.makedirs(savedir)
            with open(savedir + self.name+ '.json','w',encoding='utf-8') as out:
            success = json.dump(event,out)
            print(success)
        return event

### END: Event ###


### DEFINE: Block ###
class Block:
    '''A block (or 'pattern') of Events'''

    def __init__(self,name=self.___next_name(),bname='default',events=[]):
        '''creates a new instance of a block of events
        name:   the name of the block (e.g. 'pattern_013')
        bname:  the name of the Blocks object (e.g. 'set_02')
        events: the list of Events
        size:   the number of Events in this block'''
        self.name = self.next_name() # creates a default block name
        self.bname = bname # creates a default bname called 'default'
        self.events = events # sequential list of events
        self.count = len(self.events)

    def addEvent(self,new):
        '''add a single event to the block
        indices will adjust accordingly based on latency
        returns the index of the newly added event'''
        # if this is the first event...
        if self.events==[]:
            self.events.append(event);
            self.events[0].index = 0
            self.count = 1
            return 0
        # if this event has a latency earlier than the first event...
        if new.latency<self.events[0].latency:
                self.events.insert(0,event)
                self.events[0].index = 0
                for e in self.events[1:]:
                    e.index += 1
                self.count += 1
                return 0
        # every other case...
        for i,old in enumerate(self.events):
            if new.latency>=self.events[0].latency:
                if new.latency>=old.latency:
                    self.events.insert(i+1,event)
                    self.events[i+1].index = i+1
                    for e in self.events[i+2:]:
                        e.ind'ex += 1
                    self.count += 1
                    return i+1

    def __nextName(self,digits=3)
        ''' digits represents how many different possible 
        participant numbers you can have'''
        if not hasattr(self.nextName,'nextName'):
            self.nextName = 'pattern_000'
        num_len = len(str(self.count-1))
        self.nextName = 'pattern_' + '0'*(digits-num_len) + str(self.num)
        return self.nextName
 
    def jsonify(self,save=True):
        '''puts the Block object into json form
           can also be saved as a .json (default: self.name)
           save: either True or False, depending on if we want to save the files'''
        events = {}
        for i,e in enumerate(self.events):
            events.update({i:e.jsonify()})
        events = {'events':events}
        
        # if we save a single block, we'll just put it in a 'default' folder
        if save:
            savedir = ROOT_PROJECT_PATH+'task/paradigms/default/'
            if not os.path.exists(savedir):
                os.makedirs(savedir)
            with open(ROOT_PROJECT_PATH+'task/paradigms/default/' + \
              self.name+ '.json','w',encoding='utf-8') as out:
            success = json.dump(events,out)
            print(success)
        return events

### END: Block ###

### DEFINE: Blocks ###
class Blocks:

    def __init__(self,name,blocks=[]):
        '''creates a new instance of a set of Blocks
        name:   name of the Block set
        blocks: a list of Block objects'''
        self.name = name
        self.blocks = blocks
        self.count = len(blocks)

    def addBlock(self,block,ind=-1):
        '''appends a new Block object to the list of Blocks
        block: a Block object
        ind:   an integer representing the index of where to
               insert the block (default is end of list)
        returns the current Blocks object'''
        if ind<0: self.blocks.append(block)
        else: self.blocks.insert(ind,block)
        self.count += 1
        return self

    def randomize(self):
        self.blocks = shuffle(self.blocks)

    def jsonify(self,save=True):
        '''puts the Blocks object into json form
           can also be saved as a .json (default: block.name)
           save: either True or False, depending on if we want to save the files'''
        blocks = {}
        for i,b in enumerate(self.blocks):
            blocks.update({i:b.jsonify()})
        blocks = {'blocks':blocks}

        if save:
            for block in self.blocks:
                with open(ROOT_PROJECT_PATH+'task/paradigms/'+ self.name + \
                  '/' + block.name+ '.json','w',encoding='utf-8') as out:
                    success = json.dump(blocks,out)
        return blocks

### END: Blocks ###

### DEFINE: Participant ###
class Participant:
    '''a participant in the study.'''

    def __init__(self, pid, name, sex, age, blocks):
        '''creates a new instance of a participant
        pid:     ID given to the participant
        name:   name given to the participant
        sex:    a string that can be 'M' or 'Male', 'F' or 'Female', or 'N/A'
        age:    an integer (or float) value representing participant age
        blocks: a Blocks structure representing order of Blocks'''
        self.id = pid
        self.name = name
        self.sex = sex
        self.age = age
        self.blocks = blocks

    def jsonify(self,save=True):
        part = {'id':self.id,'name':self.name,'sex':self.sex,'age':self.age,'blocks':blocks}
        if save:
            
            with open(ROOT_PROJECT_PATH+'task/participants/sub-'+ \ 
               '0'*(3-(len(self.id))) + '/' + self.name+ '.json', \
               'w',encoding='utf-8') as out:
                success = json.dump(part,out)
        return part
    

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

### END: Experiment ###name of the Block
