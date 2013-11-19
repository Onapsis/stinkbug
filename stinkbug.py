import sys
from lib import parse as parse
import random 
import string 
import argparse

# The required arguments for authentication
parser = argparse.ArgumentParser(description='Stinkbug')
parser.add_argument('pdml', type=str,
                   help='The PDML file to parse')
parser.add_argument('--sulley', action="store_true",
                   help='Output a sulley configuration file.')
parser.add_argument('--missing-bytes', action="store_true",
                   help='Outputs the location of missing bytes.')
parser.add_argument('--pbytes', action="store_true",
                   help='Outputs a hex stream for the data if possible ***BUGGY DO TO BROKEN DISSECTORS***')                  

args = parser.parse_args()

pdml = args.pdml
# generate random string with file
fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(20))
print "|+| Using /tmp/stinkbug_"+fname+".txt as a temporary file"

parse.run(fname,pdml)

if args.sulley:
    parse.output_sulley("/tmp/stinkbug_"+fname+".txt")
if args.pbytes:
    parse.print_buffer("/tmp/stinkbug_"+fname+".txt","00")
