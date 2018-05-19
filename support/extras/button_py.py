from __future__ import print_function
import serial
import time
from datetime import datetime


# This should be replaced with the device name
device = '/dev/ttyACM0'
baudrate = 9600

# Smoothing factor in seconds
resettime = 0.5

def string_datetime():
    return datetime.now().isoformat()

def main_loop(fileh):
    '''
    This approach uses the concept of "last time" to avoid connection stutter
    in the output, so instead we record only the previous change if the previous
    change was made more than <resettime> seconds ago. We also keep track of
    that time in order to prevent an offset.

    0 indicates an open circuit
    1 indicates a closed circuit
    '''
    ser = serial.Serial(device, baudrate)
    # Set up some reasonable defaults
    prevdatetime = string_datetime()
    prevstate = '0'
    prevtime = time.time()
    print('time', 'open/closed', sep='\t', file=fileh)
    # Loop until we exit
    while True:
        # True if we get a ascii 1, false if we get an ascii 0
        # Strip removes whitespace 
        valopen = ser.readline().strip() == b'1'

        # Time of this serial message sent
        thistime = time.time()

        # Get the current time formatted in a string
        thisdatetime = string_datetime()

        # We reset if true
        # If the previous time plus the reset time is less than this time, that
        # means our last interaction was more than resettime seconds ago
        if prevtime + resettime < thistime:
            # Print the previous interaction timestamp
            print(prevdatetime, prevstate, sep='\t', file=fileh)

            # Store the previous state, or the last state polled from the device
            prevstate = '0' if valopen else '1'

            # Store the previous seconds since the epoch (start of compute time)
            prevtime = thistime

            # Store the current datetime
            prevdatetime = thisdatetime

def naive_loop():
    '''
    This approach just prints all interactions out to the console in tsv
    it however, will contain stuttering when the pads connect due to incomplete
    connections, this may be more appropriate if you are concerned the above
    code is not going to record properly
    '''
    ser = serial.Serial(device, baudrate)
    while True:
            valopen = ser.readline().strip() == b'1'
            prevstate = '0' if valopen else '1'
            print(string_datetime(), prevstate, sep='\t')

if __name__ == '__main__':
#    naive_loop()
    main_loop()



