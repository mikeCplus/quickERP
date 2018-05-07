from __future__ import print_function
from pylsl import StreamInlet, resolve_stream
import sys
import subprocess
import datetime

programline = ['muse-io', '--no-dsp', '--preset', 'AD', '--lsl-eeg', 'eegdata'];

def start_study():
    
    print('Participant Id: ', end='')
    subjectid = raw_input()
    acqfname = study_prefix + subjectid + acquisition_suffix
    acqfid = open(acqfname, 'w')

   

def start_acquisition(fileh, starttime, in_channel, msg_channel):
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    print("recording!")
    msg_channel.put((True, 'recording'))
    flush_count = 128
    count = 0
    while True:
        # Check if we've been signalled to end, if there is any message break
        # the loop, this allows us to cleanup the file handles and close the
        # muse program
        if not in_channel.empty() and in_channel.get() == 'close':
            break

        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, _ = inlet.pull_sample()

        # We convert all elements in sample to a string then we join them with
        # by putting , between each element
        datetimenow = datetime.datetime.now()
        elapsedtime = datetimenow - starttime

        print(datetimenow.isoformat(), elapsedtime.total_seconds(), 
              *sample, sep=',', file=fileh)
        count = (count + 1) % flush_count
        if count == 0:
            fileh.flush()

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
        
    
