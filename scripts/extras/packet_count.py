from sys import argv
import os 
 
if __name__=="__main__":
     
    script, filename = argv 
     
    in_file = open(filename,'r')
    lines = in_file.readlines()
    in_file.close()
     
    out_name = os.path.splitext(filename)[0]+'_pkt.csv'
    out_file = open(out_name,'w')
 
    times = [] # list to store total time for each packet
    count = [] # list to store total count for each packet
 
    # set value of col1 (s) of first line/row:
    curr_s = float(lines[0].split(',')[1])
    # set current count:
    curr_count = 0
 
    packet_start = [lines[0].split(',')[1]] # add first packet start time
    for line in lines: # loop through each line/row
        s = float(line.split(',')[1]) # s of current line/row
        if s==curr_s:     # if s is the same as previous
            curr_count+=1 # increase current count --> why is there a += what is it doing
        else: # if s is not the same as previous
            times.append(s - curr_s) # add total time for current packet
            count.append(curr_count) # add total count for current packet
            packet_start.append(str(s)) # add packet start time
            curr_s = s     # update new current s
            curr_count = 1 # reset counter
 
    values = [] # list to store final values
     
    # iterate through every time & count
    for i in range(0,len(times)):
        print (count[i])
        # add current time/count to values list
        values.append(times[i]/count[i])
 
    out_file.write('packet_start,sample_rate,sample_count\n')
    for i, value in enumerate(values):
        out_file.write(packet_start[i]+','+str(value)+','+str(count[i])+'\n') # print all the values! :D
         
