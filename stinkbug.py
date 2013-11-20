import sys
from lib import parse as parse
from lib import test as Test
import random 
import string 
import argparse
from lxml import etree

# The required arguments for authentication
parser = argparse.ArgumentParser(description='Stinkbug')
parser.add_argument('pdml', type=str,
                   help='The PDML file to parse')
parser.add_argument('--sulley', action="store_true",
                   help='SECURITY_TEST: Output a sulley configuration file.')
parser.add_argument('--mbytes', action="store_true",
                   help='Outputs the location of missing bytes, this is common. *** DOES NOT WORK IF PDML DOES NOT INCLUDE HEX STREAM ***')
parser.add_argument('--pbytes', action="store_true",
                   help='Outputs a hex stream for the data if possible ***BUGGY DUE TO BROKEN DISSECTORS***') 
parser.add_argument('--outfile', type=str,
                   help='Output a test to a file; NOTE: only works on SECURITY_TESTS')

args = parser.parse_args()

pdml = args.pdml

# check if multiple packets
tree = etree.parse(pdml)
frames = [e for e in tree.xpath('/pdml/packet')]
n_frames = len(frames)

# garbage collect this - TODO:check this actually works
tree = None

print "|+| "+str(n_frames)+" packets in input"
ofname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(20))

n = 1
for frame in frames:

    fname = ofname+"_"+str(n)
    print "|+| Using /tmp/stinkbug_"+fname+".txt as a temporary file"
    parse.run(fname,pdml,frame.getchildren())

    if args.sulley and args.outfile:
        print "|+| Writing output to "+str(args.outfile)
        Test.output_sulley_file("/tmp/stinkbug_"+fname+".txt","./templates/sulley_fuzz.py",args.outfile)        
    else: 
        if args.sulley:
            Test.output_sulley("/tmp/stinkbug_"+fname+".txt","./templates/sulley_fuzz.py")
    if args.pbytes:
        parse.print_buffer("/tmp/stinkbug_"+fname+".txt","00")
    if args.mbytes:
        parse.missing_bytes("/tmp/stinkbug_"+fname+".txt")
    n = n + 1
