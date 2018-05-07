from __future__ import print_function
import os, sys
from plugins.pylsl import StreamInlet, resolve_byprop
import subprocess
import datetime
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

programline = ['muse-io', '--no-dsp', '--preset', 'AB', '--lsl-eeg', 'eegdata'];

def start_acquisition(fileh, logfile, sub_path, starttime, in_channel, msg_channel):
    # first resolve an EEG stream on the lab network
        
    print("looking for an EEG stream...")
    streams = resolve_byprop('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0],max_chunklen=16)

    print("recording!")
    msg_channel.put((True, 'recording'))    

    ## initialize all acquisition loop variables
    #######################################################################################################

    CONSTANT = 0.9999 # CHANGE THIS to adjust time corrected timestamp to as close to UNIX time as possible

    count = 0 # resets every time it reaches flush_count value    
    flush_count = 128 # print to file every X number of loops (default: X=128)
    ms_count = 0.000 # assumed increase in time (sec) between each sample without correction 
    firstLoop = True # set to true for first loop only
    
    init_time = None # this will initialize to an actual value after recording of first sample
    start_offset = None # this will initialize to an actual value after recording of first sample
    elapsedtime = None # this will initialize to an actual value after recording any sample
    prevelapsed = None # this will initialize to an actual value after recording any sample
    prev_stamp = None # this will initialize to an actual value after recording any sample

    loopcount = 0 # counter for number of loops (should correspond with number of samples)
    packet_size = 0 # counter for current number of packets    
    timestamp = 0 # this will initialize to an actual value after recording any sample
    time_corr = 0 # initialize time correction to 0 until after the first sample pull
    delayshift = 0 # shift between each packet
    first_in_packet = 0 # this will initialize to an actual value after each new packet is identified
    total_pulltime = 0 # to account for time spent waiting for pull
    corr_time = 0 # current corrected timestamp

    ## store all the different times in variables to graph
    #######################################################################################################

    UNIX_times = [] # list of UNIX elapsed times since starttime
    UNIX_diffs = [] # differences between UNIX sample times
    inlet_times = [] # list of inlet elapsed times since starttime
    inlet_diffs = [] # differences between inlet sample times
    corr_times = [] # list of corrected times since starttime
    corr_diffs = [] # differences between corrected sample times
    packet_sizes = [] # list of packet sizes


    print ("timestamp,init_time,start_offset,time_corr,ms_count,delayshift,inlet_diff,CONSTANT,TOTAL",file=logfile)

    while True:

        # Check if we've been signalled to end, if there is any message break the loop,
        # this allows us to cleanup the file handles and close the muse program
        if not in_channel.empty() and in_channel.get() == 'close':
            break
    
        loopcount += 1
        packet_size += 1 # resets to 0 each time new packet is found
        datetimeref = datetime.datetime.now() # record UNIX time as close to before inlet timestamp
        prev_stamp = timestamp # record previous timestamp before we update it        
        sample, timestamp = inlet.pull_sample() # record inlet sample and timestamp before correction
        datetimenow = datetime.datetime.now() # record UNIX time as close to after inlet timestamp
        approx_pulltime = (datetimenow-datetimeref) # calculate approximate UNIX time of sample pull
        datetimenow = datetimenow - (approx_pulltime)/2 # approximate UNIX timing of pull_sample call
        approx_pulltime = approx_pulltime.total_seconds() # convert to seconds
        prevelapsed = elapsedtime # record previous elapsed UNIX time
        elapsedtime = (datetimenow - starttime).total_seconds() # elapsed UNIX time since starttime
        total_pulltime += approx_pulltime

        if firstLoop:
            first_in_packet = timestamp # record first raw inlet timestamp in first packet
            init_time = timestamp # record first raw inlet timestamp before time correction   
            prev_stamp = init_time # make previous timestamp same as initial timestamp
            prevelapsed = elapsedtime # record previous elapsed time as current elapsed time 
            start_offset = elapsedtime # record initial approximate time since UNIX starttime
            packet_size = 0 # only reset for first loop to adjust the count of the first packet            
            firstLoop = False

        inlet_diff = timestamp-prev_stamp # delay between current sample and previous

        # update between-packet delay if current sample is more than 8ms from previous sample
        if timestamp - first_in_packet > 0.008:
            inlet_diff = np.mean(inlet_diffs) # if between packets, use mean of previous inlet timestamp diffs
            packet_sizes.append(packet_size)
            print ('|-----------> packet_diff =',timestamp-first_in_packet,'size =',packet_size,sep=' ',file=logfile)
            # update by adding time between beginning of current timestamp and first of previous packet,
            # plus time taken to send packet
            delayshift = delayshift + timestamp - first_in_packet
            first_in_packet = timestamp
            packet_size = 0 # reset packet count

        # update inlet time correction (should be in the microsecond range)
        #if time_corr != inlet.time_correction(): # only whenever it changes
        time_corr = time_corr + inlet.time_correction()
        
        # *** ADJUST TIMING OF INLET TIMESTAMP *** #
        # 0. [inlet_time] timestamp adjusted to initial timestamp plus start_offset
        #    a) [timestamp] current raw timestamp
        #    b) [- init_time] adjust to the initial inlet timestamp
        #    c) [+ start_offset] add difference between first elapsedtime and starttime
        # 1. [+ ms_count] add 2ms      
        # 2. [+ time_corr] add time correction (approx. microsecond difference from 2ms)
        # 3. [- delayshift] subtract combined shift in delay between each packet
        # 4. [- inlet_diff] subtract delay between receiving current sample and last
        # 5. [* CONSTANT] adjust to get as close as possible to actual UNIX time
        ##XXXX [- approx_pulltime] subtract time spent waiting for pull_sample call ## apparently already accounted for
        inlet_time = float(timestamp) - init_time + start_offset
        prev_corr = corr_time # record previous corrected timestamp        
        corr_time = (inlet_time + ms_count + time_corr - delayshift - inlet_diff)*CONSTANT
        print (str(loopcount)+': (',timestamp,'-',init_time,'+',start_offset,'+',ms_count,'+',
               time_corr,'-',delayshift,'-',inlet_diff,' ) *',CONSTANT,'=',corr_time,sep=' ',file=logfile)

        # convert all elements in sample to a string, and join them with a comma
        print(datetimenow.isoformat(),elapsedtime,inlet_time,corr_time,*sample, sep=',', file=fileh)       

        # add to data for graphs
        UNIX_times.append(elapsedtime)
        UNIX_diffs.append(elapsedtime-prevelapsed)
        inlet_times.append(inlet_time)
        inlet_diffs.append(timestamp-prev_stamp)
        corr_times.append(corr_time)
        corr_diffs.append(corr_time-prev_corr)

        ms_count = ms_count + 0.002 # add 2ms to each loop

        # flush to file every [flush_count] number of loops
        count = (count + 1) % flush_count
        if count == 0:
            fileh.flush()
            logfile.flush()

    ######### PLOT FIGURES #########

    graph_dir = sub_path + '/figures/'
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)

    ### plot first 5 seconds of samples vs UNIX timestamp
    sys.stdout.write('\nplotting first 5 seconds of samples vs UNIX timestamp...'); sys.stdout.flush()
    figA = plt.figure()
    axA = figA.add_subplot(111)    
    axA.scatter(range(len(UNIX_times[:2500])),UNIX_times[:2500],s=0.5,marker='.',c='r')
    axA.set_xlabel('sample'); axA.set_ylabel('UNIX_time (sec)')
    patches = []    
    patches.append(mpatches.Patch(color='r',label='samples VS UNIX_time'))
    axA.legend(handles=patches,loc=1,\
               bbox_to_anchor=[float(-0.17),float(-0.15)],fontsize=7.5)    
    plt.savefig(graph_dir+'samples_vs_unix_5_sec.eps',format='eps',dpi=1000)
    sys.stdout.write('done.'); sys.stdout.flush()

    ### plot first 5 seconds of samples vs inlet timestamp
    sys.stdout.write('\nplotting first 5 seconds of samples vs inlet timestamp...'); sys.stdout.flush()
    figB = plt.figure()    
    axB = figB.add_subplot(111)    
    axB.scatter(range(len(inlet_times[:2500])),inlet_times[:2500],s=0.5,marker='.',c='g')
    axB.set_xlabel('samples'); axB.set_ylabel('inlet_time (sec)')
    patches = []    
    patches.append(mpatches.Patch(color='g',label='samples vs inlet_time'))
    axB.legend(handles=patches,loc=1,\
              bbox_to_anchor=[float(-0.17),float(-0.15)],fontsize=7.5)    
    plt.savefig(graph_dir+'samples_vs_inlet_5_sec.eps',format='eps',dpi=1000)    
    sys.stdout.write('done.'); sys.stdout.flush()    

    ### plot first 5 seconds of samples vs corrected timestamp
    sys.stdout.write('\nplotting first 5 seconds of samples vs corrected timestamp...'); sys.stdout.flush()
    figC = plt.figure()
    axC = figC.add_subplot(111)
    axC.scatter(range(len(corr_times[:2500])),corr_times[:2500],s=0.5,marker='.',c='b')
    axC.set_xlabel('sample'); axC.set_ylabel('corr_time (sec)')
    patches = []    
    patches.append(mpatches.Patch(color='b',label='samples vs corr_time'))
    axC.legend(handles=patches,loc=1,\
              bbox_to_anchor=[float(-0.17),float(-0.15)],fontsize=7.5)    
    plt.savefig(graph_dir+'samples_vs_corr_5_sec.eps',format='eps',dpi=1000)
    sys.stdout.write('done.'); sys.stdout.flush()

    ### plot first 5 second time comparison between all 3 times
    sys.stdout.write('\nplotting first 5 second time comparison between all 3 times...'); sys.stdout.flush()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(range(len(UNIX_times[:2500])),UNIX_times[:2500],s=0.5,marker='.',c='r')
    ax.scatter(range(len(inlet_times[:2500])),inlet_times[:2500],s=0.5,marker='.',c='g')
    ax.scatter(range(len(corr_times[:2500])),corr_times[:2500],s=0.5,marker='.',c='b')
    ax.set_xlabel('sample'); ax.set_ylabel('time (sec)')
    patches = []
    patches.append(mpatches.Patch(color='r',label='UNIX_time'))
    patches.append(mpatches.Patch(color='g',label='inlet_time'))
    patches.append(mpatches.Patch(color='b',label='corr_time'))    
    plt.legend(handles=patches,loc=3,\
               bbox_to_anchor=[float(-0.17),float(-0.15)],fontsize=7.5)
    plt.savefig(graph_dir+'time_comparison_5_sec.eps',format='eps',dpi=1000)
    sys.stdout.write('done.'); sys.stdout.flush()

    ### plot one second time comparison between all 3 times
    sys.stdout.write('\nplotting one second time comparison between all 3 times...'); sys.stdout.flush()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(range(2000,2500),UNIX_times[2000:2500],s=0.5,marker='.',c='r')
    ax.scatter(range(2000,2500),inlet_times[2000:2500],s=0.5,marker='.',c='g')
    ax.scatter(range(2000,2500),corr_times[2000:2500],s=0.5,marker='.',c='b')
    ax.set_xlabel('sample'); ax.set_ylabel('time (sec)')
    patches = []
    patches.append(mpatches.Patch(color='r',label='UNIX_time'))
    patches.append(mpatches.Patch(color='g',label='inlet_time'))
    patches.append(mpatches.Patch(color='b',label='corr_time'))    
    plt.legend(handles=patches,loc=3,\
               bbox_to_anchor=[float(-0.17),float(-0.15)],fontsize=7.5)
    plt.savefig(graph_dir+'time_comparison_1_sec.eps',format='eps',dpi=1000)
    sys.stdout.write('done.'); sys.stdout.flush()

    ### plot full time comparison between all 3 times
    sys.stdout.write('\nplotting full time comparison between all 3 times...'); sys.stdout.flush()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(range(len(UNIX_times)),UNIX_times,s=0.5,marker='.',c='r')
    ax.scatter(range(len(inlet_times)),inlet_times,s=0.5,marker='.',c='g')
    ax.scatter(range(len(corr_times)),corr_times,s=0.5,marker='.',c='b')
    ax.set_xlabel('sample'); ax.set_ylabel('time (sec)')
    patches = []
    patches.append(mpatches.Patch(color='r',label='UNIX_time'))
    patches.append(mpatches.Patch(color='g',label='inlet_time'))
    patches.append(mpatches.Patch(color='b',label='corr_time'))    
    plt.legend(handles=patches,loc=3,\
               bbox_to_anchor=[float(-0.17),float(-0.15)],fontsize=7.5)
    plt.savefig(graph_dir+'time_comparison_full.eps',format='eps',dpi=1000)
    sys.stdout.write('done.'); sys.stdout.flush()

    ### plot UNIX timestamp differences
    sys.stdout.write('\nplotting UNIX timestamp differences...'); sys.stdout.flush()
    UNIX_diffs = UNIX_diffs[2:] # ignore first 2 differences since first is meaningless and second is huge
    fig = plt.figure()
    ax = fig.add_subplot(111)
    bar_width = 0.1
    rects = ax.bar(range(len(UNIX_diffs)),UNIX_diffs,bar_width,color='b',label='UNIX_diffs')
    mean = np.mean(UNIX_diffs)
    ax.axhline(mean,color='r',linewidth=1)
    ax.text(len(packet_sizes)/3,mean+(mean*0.1),'Mean = '+str(mean),color='r')   
    ax.set_title('Differences Between UNIX Timestamps')    
    ax.set_xlabel('sample #')    
    ax.set_ylabel('time between samples (sec)')
    plt.savefig(graph_dir+'UNIX_diffs.eps',format='eps',dpi=1000)
    sys.stdout.write('done.'); sys.stdout.flush()

    ### plot inlet time differences
    sys.stdout.write('\nplotting inlet timestamp differences...'); sys.stdout.flush()
    inlet_diffs = inlet_diffs[1:] # ignore first difference since it is meaningless
    fig = plt.figure()
    ax = fig.add_subplot(111)
    bar_width = 0.1
    rects = ax.bar(range(len(inlet_diffs)),inlet_diffs,bar_width,color='b',label='inlet_diffs')
    mean = np.mean(inlet_diffs)
    ax.axhline(mean,color='r',linewidth=1)
    ax.text(len(packet_sizes)/3,mean+(mean*0.1),'Mean = '+str(mean),color='r')
    ax.set_title('Differences Between Inlet Timestamps')    
    ax.set_xlabel('sample #')    
    ax.set_ylabel('time between samples (sec)')
    plt.savefig(graph_dir+'inlet_diffs.eps',format='eps',dpi=1000)
    sys.stdout.write('done.'); sys.stdout.flush()

    ### plot inlet time differences
    sys.stdout.write('\nplotting corrected timestamp differences...'); sys.stdout.flush()
    corr_diffs = corr_diffs[1:] # ignore first difference since it is meaningless
    fig = plt.figure()
    ax = fig.add_subplot(111)
    bar_width = 0.1
    rects = ax.bar(range(len(corr_diffs)),corr_diffs,bar_width,color='b',label='corr_diffs')
    mean = np.mean(corr_diffs)
    ax.axhline(mean,color='r',linewidth=1)
    ax.text(len(packet_sizes)/3,mean+(mean*0.1),'Mean = '+str(mean),color='r')   
    ax.set_title('Differences Between Corrected Timestamps')
    ax.set_xlabel('sample #')    
    ax.set_ylabel('time between samples (sec)')
    plt.savefig(graph_dir+'corr_diffs.eps',format='eps',dpi=1000)
    sys.stdout.write('done.'); sys.stdout.flush()

    ### plot packet sizes
    sys.stdout.write('\nplotting packet sizes...'); sys.stdout.flush()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    bar_width = 0.1
    rects = ax.bar(range(len(packet_sizes)),packet_sizes,bar_width,color='b',label='packet_sizes')
    mean = np.mean(packet_sizes)
    ax.axhline(mean,color='r',linewidth=1)
    ax.text(len(packet_sizes)/3,mean+(mean*0.1),'Mean = '+str(mean),color='r')
    ax.set_title('Packet Sizes')    
    ax.set_xlabel('packet #')    
    ax.set_ylabel('packet_size')    
    plt.savefig(graph_dir+'packet_sizes.eps',format='eps',dpi=1000)
    sys.stdout.write('done.'); sys.stdout.flush()

# Start a process and return a Popen object that tracks the process
def start_muse():
    return subprocess.Popen(programline, stdin=subprocess.PIPE)

# Closs the muse process that is given    
def close_muse(process):
    process.kill()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('We need a filename for output in csv')
        exit(1)
        
    outputfile = sys.argv[1]
#    museprog = start_muse()
    with open(outputfile, 'w') as fhandle:
        try:
            start_acquisition(fhandle)
        finally:
            pass
#        close_muse(museprog)
        
    
