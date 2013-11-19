import sys
from lib import parse as parse
import random 
import string 

if len(sys.argv) < 2:
    print "\t|!| Please include pdml file"
    sys.exit()

# generate random string with file
fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(20))
print "|+| Using /tmp/stinkbug_"+fname+".txt as a temporary file"

parse.run(fname)

parse.print_buffer("/tmp/stinkbug_"+fname+".txt","00")
