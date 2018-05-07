''' gen_pats.py

Written by Mike Cichonski for the Brock University Cogintive
and Affective Neuroscience Lab
purpose:
   generates a desired number of patterns for a task into a list in files
arguments:
   n_pats = sys.argv[1]       # number of patters to generate 
   stims = sys.argv[2]        # list of unique stims (strings)
optional arguments:
   stim_count = sys.argv[3]   # total number of stims (default 100)
   stim_weights = sys.argv[4] # list of numbers of each stim appearing
                              # must correspond with length of stims and stim_count
examples:
  1. Generate 8 pattern files, each with a randomized sequence of 50 'A's and 50 'B's
>> python gen_pats 8 ['A','B']

  2. Generate 5 pattern files, each with a randomized sequence of 60 'H's and 20 'S's
>> python gen_pats 5 ['H','S'] 80 [60 20]

  3. Generate 20 pattern files, each with a randomized sequence of 100 '1's and 100 '2's  
>> python gen_pats 20 ['1','2'] 200

'''

from __future__ import print_function
import os,sys
from itertools import permutations
import random

if __name__=='__main__':
    
    pat_dir = os.path.dirname(os.path.realpath(__file__))

    if len(sys.argv)<2:
        os.system('man gen_pats.py')
        sys.exit()
    elif len(sys.argv)>5:
        os.system('man gen_pats.py')
        print ('ERROR: Too many imput aruments!')
        sys.exit()

    n_pats = int(sys.argv[1])
    stims  = sys.argv[2].replace('[','').replace(']','').split(',')
    
    if len(sys.argv)<4:
        stim_count = 100
    else:
        stim_count = int(sys.argv[3])

    if len(sys.argv)==5:
        stim_weight = [int(x) for x in sys.argv[4].replace('[','').replace(']','').split(',')]
        if stim_count<sum(stim_weight)-1 or stim_count>sum(stim_weight)+1:
            print ('ERROR: stim_count must add up the sum of stim_weight')
            sys.exit()
    else:
        stim_weight = [round(stim_count/100)]*len(stims);

    if len(stims)!=len(stim_weight):
        print('ERROR: Number of stims must equal to number of stim weights .')
        sys.exit()

    if sum(stim_weight)<stim_count-1 or sum(stim_weight)>stim_count+1:
        print ('ERROR: arg4 "stim_weight" values must add up to stim_count')
        sys.exit()


    all_stims = []
    for i,stim in enumerate(stims):
        all_stims.extend([stim]*stim_weight[i])
    for i in range(n_pats):
        random.shuffle(all_stims)
        f = open('pat_' + '0'*(len(str(n_pats))-len(str(i))) + str(i) + '.txt','w')
        [f.write(str(x)+'\n') for x in all_stims]
        f.close()
    print('Done.')

exit(0)
