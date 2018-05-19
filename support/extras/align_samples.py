import os

if __name__=="__main__":

    filenames = []
    subdirs = [x[0] for x in os.walk('.')]
    for subdir in subdirs:
        files = os.walk(subdir).next()[2]
        if len(files) > 0:
            for f in files:
                if os.path.splitext(f)[-1]=='.csv' \
                   and not f.endswith('_new.csv'):
                    filenames.append(os.path.join(subdir+'/'+f))

    for f in filenames:
        
        print 'processing ' + f
        in_file = open(f,'r')
        lines = in_file.readlines()
        in_file.close()

        new_name = os.path.splitext(f)[0]+'_new.csv'
        out_file = open(new_name,'w')

        # set value of col1 (s) of first line/row:
        curr_s = float(lines[0].split(',')[1])
        # set current count:
        curr_count = 0 

        for line in lines: # loop through each line/row
            curr_line = line.split(',') # split line
            s = float(curr_line[1]) # s of current line/row
            if s==curr_s:     # if s is the same as previous
                curr_line[1] = str(s+0.002*curr_count) # increase by 2ms
                curr_count += 1 # increase counter
                out_file.write(','.join(curr_line)) # write line to new file
            else: # if s is not the same as previous
                curr_s = s     # update new current s
                curr_count = 1 # reset counter
                out_file.write(line) # write line to new file

    out_file.close()
