import sys
from lib import parse as parse
from lib import test as Test
import random 
import string 
import argparse

# The required arguments for authentication
parser = argparse.ArgumentParser(description='Stinkbug')
parser.add_argument('pdml', type=str,
                   help='The PDML file to parse')
parser.add_argument('--sulley', action="store_true",
                   help='Output a sulley configuration file.')
parser.add_argument('--mbytes', action="store_true",
                   help='Outputs the location of missing bytes, this is common. *** DOES NOT WORK IF PDML DOES NOT INCLUDE HEX STREAM ***')
parser.add_argument('--pbytes', action="store_true",
                   help='Outputs a hex stream for the data if possible ***BUGGY DUE TO BROKEN DISSECTORS***') 

args = parser.parse_args()

pdml = args.pdml
# generate random string with file
fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(20))
print "|+| Using /tmp/stinkbug_"+fname+".txt as a temporary file"

parse.run(fname,pdml)

if args.sulley:
    Test.output_sulley("/tmp/stinkbug_"+fname+".txt")
if args.pbytes:
    Test.print_buffer("/tmp/stinkbug_"+fname+".txt","00")
if args.mbytes:
    parse.print_buffer("/tmp/stinkbug_"+fname+".txt","00")
