# -*- coding: utf-8 -*-
#########################################################################
##  Muse_EEG (May 15, 2017)                                            ##                   
##  by Mike Cichonski @ Brock Univerity Cognitive and Affective        ##
##  Neuroscience Lab (BUCANL)                                          ## 
##  © 2017 BUCANL / Under supervision of Dr. Sidney Segalowitz         ##
##  Code Written by Mike Cichonski                                     ##
##  Not for distribution or publication without permission of          ##
##  the director of BUCANL.                                            ##
##                                                                     ##
#########################################################################

### DEFINE: Result ###
class Result:
    '''A single "result" - includes stimulus, result, and reaction time'''

    def __init__(self, trial, stim, res, RTime, errType = "NONE"):
        "creates a new instance of a Result"
        '''
        trial is the trial number
        stim is the first stimulus (e.g. S1,S2,S3,S4,S5,S6)
        res is the result type (e.g. S12,S13,S14,S15)
        RTime is the reaction time (SXX - stop)
        errType is the error type:
            "NONE" = no error
            "INIT" = response before initial stimulus
            "EARLY" = response before stop
            "DUPL" = duplicate result
            "MISS" = missed response
            "tOUT" = timed out response (response after first stim)
            "OVRD" = response at the same time as stop'''
        self.trial = trial
        self.stim = stim
        self.res = res
        self.RTime = RTime
        self.errType = errType

### END: Result ###

### DEFINE: Result2 ###
class Result2(Result):
    '''A single "result" - includes two stimuli, result, and reaction time'''

    def __init__(self, trial, stim, stim2, res, RTime, errType = "NONE"):
        "creates a new instance of a Result"
        '''
        trial is the trial number
        stim is the first stimulus (e.g. S1,S2,S3,S4,S5)
        stim2 is the second stimulus (e.g. S6,S7,S8,S9,S10)
        res is the result type (e.g. S12,S13,S14,S15)
        RTime is the reaction time (SXX - stop)
        errType is the error type:
            "NONE" = no error
            "INIT" = response before initial sentence is played
            "EARLY" = response before stop
            "DUPL" = duplicate result
            "MISS" = missed response
            "tOUT" = timed out response (response after first stim)
            "OVRD" = response at the same time as stop'''
        self.trial = trial
        self.stim = stim
        self.stim2 = stim2
        self.res = res
        self.RTime = RTime
        self.errType = errType

### END: Result2 ###

### DEFINE: Participant ###
class Participant:
    '''a participant in the study.'''

    def __init__(self, name, results = [], errors = []):
        "creates a new instance of a participant"
        '''
        name is the participant name (defaulted as the filename)
        result is a list of Result and Result2 objects
        extra is a list of the error results'''

        self.name = name
        self.results = results
        self.errors = errors

    def addResult(self, theResult):
        self.results.append(theResult)

    def addError(self, theResult):
        self.errors.append(theResult)

    def clearResults(self):
        "clears the result and error lists"
        self.results=[]
        self.errors=[]

### END: Participant ###

### DEFINE: Experiment ###
class Experiment:
    '''A list of all participants in the experiment'''

    def __init__(self, participants = []):
        "creates a new instance of Experiment (list of Participants)"
        
        self.participants = participants

    def addParticipant(self, theParticipant):
        "adds a participant to the list"
        #as long as participant isn't already in the participants list...
        if not self.__containsPart(theParticipant.name):
            self.participants.append(theParticipant) #add participant
        else: #otherwise, overwrite the participant with new data
            self.participants[self.__partWithName(theParticipant.name)] = theParticipant

    def __containsPart(self, partName):
        "checks if participant with partName is in the list"
        for p in self.participants:
            if p.name == partName:
                return True
        return False

    def __partWithName(self, partName):
        "returns index number of participant with partName as name" 
        for index, p in enumerate(self.participants):
            if p.name == partName:
                return index
        return False

### END: Experiment ###
