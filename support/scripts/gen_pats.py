''' gen_pats.py

Written by Mike Cichonski for the Brock University Cogintive
and Affective Neuroscience Lab
purpose:
   generates a desired number of patterns for a task into a list in files
arguments:
   --name OR   -n    # name of the block (default='default')
   --pats OR   -p    # number of patters to generate (default=5)
   --stim OR   -s    # list of unique stims (strings) (default=['A','B'])
optional arguments:
   --count OR  -c    # total number of stims per block (default=100)
   --weight OR -w    # list of numbers of the max number of times each stim 
                     # is allowed to appear in a row (default=[50,50])
                     # must correspond with length of stims and stim_count
examples:
  1. Generate 8 pattern files, each with a randomized sequence of 50 'A's and 50 'B's
>> python gen_pats --pats=8 --stim=['A','B']

  2. Generate 5 pattern files, each with a randomized sequence of 60 'H's and 20 'S's
>> python gen_pats -p=5 -s=['H','S'] -c=80 -w=[60 20]

  3. Generate 20 pattern files, each with a randomized sequence of 100 '1's and 100 '2's  
>> python gen_pats -p=20 -s=['1','2'] -c=200

  4. Generate 3 pattern files, each with a randomized sequence of 20 'X's and 20 'Y's,
     added to the paradigm block set named 'set_001'  
>> python gen_pats -n='set_001' -p=3 -s=['1','2'] -c=200

'''

from __future__ import print_function
import os,sys
from itertools import permutations
import random

if __name__=='__main__':
    
    ROOT_PROJECT_PATH = '../../'

    if len(sys.argv)>6:
        print ('ERROR: Too many imput aruments!')
        sys.exit()
    args = {'name'  : 'default',
            'pats'  : 5,
            'stim'  : ['A','B'],
            'count' : 100,
            'weight': [50,50] }

    for pair in sys.argv[1:]:
        pair = str(pair).lstrip('-').split('=')
        key = pair[0]
        if key=='pats' or key=='count':
            val = int(pair[1])
        elif key=='stim':
            val = list(pair[1])
        elif key='weight':
            val = list([int(w) for w in pair[1]])
        args[key] = val

    if args['count']<sum(args['weight'])-1 or args['count']>sum(args['weight'])+1:
        print ('ERROR: count must be equal to the sum of the weights.')
        sys.exit()

    if len(args['count'])!=len(args['weight']):
        print('ERROR: number of stims must equal to number of weights.')
        sys.exit()

    all_stims = []
    for i,stim in enumerate(args['stims']):
        all_stims.extend(args['stim']*args['weight'][i])
    for i in range(args['pats']):
        random.shuffle(all_stims)
        savedir = ROOT_PROJECT_PATH + 'task/paradigms/' + args['name']
        if not os.path.exists(savedir):
                os.makedirs(savedir)
        f = open(savedir + '/block_' + '0'*(len(str(n_pats))-len(str(i))) + str(i) + '.pat','w')
        [f.write(str(x)+'\n') for x in all_stims]
        f.close()
    print('Done.')

exit(0)
