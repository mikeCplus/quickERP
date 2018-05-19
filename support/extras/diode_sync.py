from sys import argv

script, f_name, = argv

if __name__=="__main__":
    
    in_file = open(f_name,'r')
    lines = in_file.readlines()
    in_file.close()
	
    times = [] # list to store total time for each packet
    count = [] # list to store total count for each packet

    # set value of col1 (s) of first line/row:
    curr_s = float(lines[0].split(',')[1])
    # set current count:
    curr_count = 0 

    for line in lines: # loop through each line/row
        s = float(line.split(',')[2]) # s of current line/row
        if s==curr_s:     # if s is the same as previous
            curr_count+=1 # increase current count
        else: # if s is not the same as previous
            times.append(s - curr_s) # add total time for current packet
            count.append(curr_count) # add total count for current packet
            curr_s = s     # update new current s
            curr_count = 1 # reset counter 

    values = [] # list to store final values

    # iterate through every time & count
    for i in range(0,len(times)):
        # add current time/count to values list
        values.append(times[i]/count[i])

    for value in values:
        # print value # print all the values! :D		
	
	packet_suffix = '_pack.csv'
	packetfname = f_name + packet_suffix
	packetfid = open(packetfname, 'w').write(str(values))
	
	
	
	
	
	
	