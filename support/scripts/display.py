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
##  file: display.py                                                   ##
##  Displays the main window of the application.                       ##
##  This file contains the GUI and the user interface which gives the  ##
##  user easy access and control of the other functions.               ##
#########################################################################

from Tkinter import *
import subprocess
    
### DEFINE: display() ###
def display(experiment):
    
    ### CREATE: WINDOW ###
    root = Tk() #create main GUI window
    root.title("Muse_EEG") #add title
    root.resizable(0, 0)  #make size unchangeable

    curFile = [None] # keeps track of the currently displayed file (for saving purposes)
    manual = [0] #boolean for manual or automatic settings (automatic is default)

    ### DEFINE: runMain() ###
    def runMain(event = None):
        "Main running function: 'Extract Data' button"
        part = data.participant.Participant(name.get()) #create participant
        part.clearResults() #clear result list in case there was a previous participant
        inList = experiment.containsPart(part.name) #check if experiment already contains participant with that name: assign to variable
        nStims = data.importData(part, "%s.vmrk" % name.get(),manual[0]) #import .VMRK results from given filename
        if nStims!=0: #as long as file exists
            experiment.addParticipant(part) # add part to experiment
        data.exportData(part, nStims, "%s.res" % name.get(), "%s.err" % name.get()) #export .res and .err with same filename as .VMRK
        if not inList and nStims>0: #as long as experiment didn't already contain this participant and participant file exists
            listBox.insert(END, name.get()) #populate listBox with participant
        listBox.select_clear(0, listBox.size()-1) #clear all previous selections in listBox
        listBox.selection_set(experiment.partWithName(name.get())) #select current participant in listbox
        name.delete(0, END) #clear name entry box
        #now that all files exist, enable buttons for viewing them
        viewVMRK['state'] = NORMAL
        viewRes['state'] = NORMAL
        viewErr['state'] = NORMAL
        openVMRK['state'] = NORMAL
        openRes['state'] = NORMAL
        openErr['state'] = NORMAL
    ### END: runMain() ###

    ### DEFINE: displayVMRK() ###
    def displayVMRK(curFile=curFile):
        "display contents of VMRK file in textbox"
        try:
            dataFile = open("vmrk/%s.VMRK" % listBox.get(listBox.curselection()), 'r')
            curFile[0] = "%s.VMRK" % listBox.get(listBox.curselection()) # sets the current file for saving purposes
            lines = dataFile.readlines()
            textBox.delete(1.0, END)
            for line in lines:
                textBox.insert(INSERT, line)
            textBox.config(state=DISABLED) #disable text so it is read-only
            dataFile.close()
        except TclError:
            print "No participant selected!"
    ### END: displayVMRK() ###
            
    ### DEFINE: displayRes() ###
    def displayRes(curFile=curFile):
        "display contents of result file in text box"
        try:
            dataFile = open("res/%s.res" % listBox.get(listBox.curselection()), 'r')
            curFile[0] = "%s.res" % listBox.get(listBox.curselection()) # sets the current file for saving purposes
            lines = dataFile.readlines()
            textBox.delete(1.0, END) #clear previous contents of text box
            for line in lines:
                textBox.insert(INSERT, line)
            textBox.config(state=NORMAL) #make sure text is editable
            dataFile.close() 
        except TclError:
            print "No participant selected!"
    ### END: displayRes() ###

    ### DEFINE: displayErr() ###
    def displayErr(curFile=curFile):
        "display contents of error file in text box"
        try:
            dataFile = open("res/%s.err" % listBox.get(listBox.curselection()), 'r')
            curFile[0] = "%s.err" % listBox.get(listBox.curselection()) # sets the current file for saving purposes
            lines = dataFile.readlines()
            textBox.delete(1.0, END)
            for line in lines:
                textBox.insert(INSERT, line)
            textBox.config(state=NORMAL) #make sure text is editable
            dataFile.close()
        except TclError:
            print "No participant selected!"
    ### END: displayErr() ###

    ### DEFINE: OPEN ###
    def openVMRK():
        try:
            subprocess.Popen('vmrk\%s.VMRK' % listBox.get(listBox.curselection()), shell=True)
        except TclError:
            print "No participant selected!"
    def openRes():
        try:
            subprocess.Popen('res\%s.res' % listBox.get(listBox.curselection()), shell=True)
        except TclError:
            print "No participant selected!"
    def openErr():
        try:
            subprocess.Popen('res\%s.err' % listBox.get(listBox.curselection()), shell=True)
        except TclError:
            print "No participant selected!"
    ### END: OPEN ###

    ### DEFINE: saveFile() ###
    def saveFile():
        '''saves the changes made in the textBox to the appropriate file.
        called when "Save Changes" menu option is selected'''
        dataFile = open(curFile[0], 'w')
        for line in textBox.get('1.0', 'end-1c').splitlines():
            dataFile.write(line + "\n")
        dataFile.close()
        filemenu.entryconfig(0,state=DISABLED)
    ### END: saveFile() ###

    ### DEFINE: enableSave() ###
    def enableSave(event):
        if ".vmrk" not in curFile[0] and ".VMRK" not in curFile[0]: # as long as it's not the .vmrk file
            filemenu.entryconfig(0,state=NORMAL)
    ### END: enableSave() ###

    ### DEFINE: enableManual() ###
    def enableManual(manual=manual):
        if(auto.get()):
            editmenu.entryconfig(1,state=DISABLED)
            manual[0] = 0
        else:
            editmenu.entryconfig(1,state=NORMAL)
            manual[0] = 1
    ### END: enableManual() ###
            
    ###################
    ### CREATE: GUI ###
    ###################

    #-----MENUBAR-----#
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0) #create 'File' menu
    filemenu.add_command(label="Save Changes", state=DISABLED, command=saveFile)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)

    editmenu = Menu(menubar, tearoff=0) #create 'Edit' menu
    auto = BooleanVar()
    editmenu.add_checkbutton(label="Auto-Detect Settings", onvalue=1, offvalue=0, variable=auto, command=enableManual)
    auto.set(1)
    editmenu.add_command(label="Settings...", state=DISABLED, command=lambda: settings.runSettings(root))

    helpmenu = Menu(menubar, tearoff=0) #create 'Help' menu
    helpmenu.add_command(label="About", command=lambda: about(root))
    
    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_cascade(label="Edit", menu=editmenu)
    menubar.add_cascade(label="Help", menu=helpmenu)

    #-----FRAME A-----#
    newFrameA = Frame(root)
    labelA = Label(newFrameA, height=2, width=15, text="Input Filename:")
    name = Entry(newFrameA, width=15, bd =5)
    extract = Button(newFrameA, width=8, text="Extract Data", command = runMain)
    #-----FRAME B-----#
    newFrameB = Frame(root)
    labelB = Label(newFrameB, height=5, width=15, text="Select Participant:\n", anchor=N)
    scrollBarA = Scrollbar(newFrameB)
    listBox = Listbox(newFrameB, height=4, width=23, bd=5, selectmode=SINGLE, yscrollcommand = scrollBarA.set)
    #-----FRAME C-----#
    newFrameC = Frame(root)
        #-----FRAME C1----#
    newFrameC1 = LabelFrame(newFrameC, text="VMRK", labelanchor=N)
    viewVMRK = Button(newFrameC1, text="View", width=11, state = DISABLED, command = displayVMRK)
    openVMRK = Button(newFrameC1, text="Open", width=11, state = DISABLED, command = openVMRK)
        #-----FRAME C2----#
    newFrameC2 = LabelFrame(newFrameC, text="Results", labelanchor=N)
    viewRes = Button(newFrameC2, text="View", width=11, state = DISABLED, command = displayRes)
    openRes = Button(newFrameC2, text="Open", width=11, state = DISABLED, command = openRes)
        #-----FRAME C3----#
    newFrameC3 = LabelFrame(newFrameC, text="Errors", labelanchor=N)
    viewErr = Button(newFrameC3, text="View", width=11, state = DISABLED, command = displayErr)
    openErr = Button(newFrameC3, text="Open", width=11, state = DISABLED, command = openErr)
    #-----FRAME D-----#
    newFrameD = Frame(root)
    scrollBarB = Scrollbar(newFrameD)
    textBox = Text(newFrameD, height=10, width=33, bd=5, yscrollcommand = scrollBarB.set)

    ### BIND: ENTER KEY ###
    name.bind('<Return>', runMain) #bind name input box to 'enter' key (same as clicking extract button: calls exportData)
    textBox.bind("<Key>", enableSave) #if change is made in textBox, enable "Save Changes" option in File menu

    ### PLACE: WIDGETS ###
    #-----FRAME A-----#
    newFrameA.grid(column=0, row=0, columnspan=3)
    labelA.pack(side=LEFT)
    name.pack(side=LEFT)
    extract.pack(side=LEFT)
    #-----FRAME B-----#
    newFrameB.grid(column=0, row=1, columnspan=3)
    labelB.pack(side=LEFT)
    scrollBarA.pack(side=RIGHT, fill=Y)
    listBox.pack()
    #-----FRAME C-----#
    newFrameC.grid(column=0, row=2, columnspan=3)
    newFrameC1.pack(side=LEFT)
    viewVMRK.pack()
    openVMRK.pack()
    newFrameC2.pack(side=LEFT)
    viewRes.pack()
    openRes.pack()
    newFrameC3.pack(side=LEFT)
    viewErr.pack()
    openErr.pack()
    #-----FRAME D-----#
    newFrameD.grid(column=0, row=3, columnspan=3)
    scrollBarB.pack(side=RIGHT, fill=Y)
    textBox.pack(side=LEFT)
    
    #------OTHER------#
    scrollBarA.config(command=listBox.yview) #link scrollBarA position to listBox
    scrollBarB.config(command=textBox.yview) #link scrollBarB position to textBox
    name.focus() #set focus to name input box
    settings.center(root) #center window

    root.config(menu=menubar)
    root.mainloop()

### END: display() ###


### DEFINE: about() ###
def about(win):

    def displayReadme():
        "display contents of readme.txt file in textbox"
        dataFile = open("readme.txt", 'r')
        lines = dataFile.readlines()
        textBox.delete(1.0, END)
        for line in lines:
            textBox.insert(INSERT, line)
        textBox.config(state=DISABLED) #disable text so it is read-only

    about = Toplevel(win)
    about.title("About")
    about.resizable(0,0)
    about.bind('<Visibility>', settings.putOnTop)
    about.transient(win)

    frameX = LabelFrame(about, text="Readme.txt") # frame for entire window

    scrollBar = Scrollbar(frameX)
    textBox = Text(frameX, height=15, width=42, bd=5, yscrollcommand = scrollBar.set)

    frameX.pack()
    scrollBar.pack(side=RIGHT, fill=Y)
    textBox.pack(side=LEFT)
    
    scrollBar.config(command=textBox.yview) #link scrollBar position to textBox
    settings.center(about) #center window
    displayReadme()

### END: about() ###
