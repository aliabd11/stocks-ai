import sys

from stocks_csp import *
#from propagators import *
from orderings import *

#data_set =

if __name__ == "__main__":
    print "This is the name of the script: ", sys.argv[0]
    print "Number of arguments: ", len(sys.argv)
    print "The arguments are: " , str(sys.argv)

    #argv1: beliefs (be: everything, ba: no alcohol, bw: no weapons, bg: no gambling)
    #argv2: region (rc: canada, ru: united states, re: everything)
    #argv3: sector (st: tech, sh: health)
    #argv4: flavour (fs: stocks, fbo: bonds, fbf: balanced funds)
    #argv5: desired style (as per style box, l/m/s+v/b/g
        #(large/mid/small+value/blend/growth)) ex. lg for large and growth
    #argv4: y/n to high management fees (y: okay with high fees, n: not okay)

    args = 'be ba bw bg rc ru re st sh fs fbo fbf lv lb lg mv mb mg sv sb sg y n'.split()
    # try:
    #     opts, args = getopt.getopt(argv, args)
    # except getopt.GetoptError as err:
    #     print str(err)
    #     sys.exit(2)