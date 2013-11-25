from lxml import etree
import random 
import string 
from lib import parse as parse
import os

def main(args):    
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

        if args.pbytes:
            parse.print_buffer("/tmp/stinkbug_"+fname+".txt","cc")
        if args.mbytes:
            parse.missing_bytes("/tmp/stinkbug_"+fname+".txt")
        if args.pp:
            #! WARNING. There should be a better way to do this than a system call for cat -_- 
            os.system("cat /tmp/stinkbug_"+fname+".txt")
        n = n + 1

# initialize the module here
def load_(subparser):
    parser = subparser.add_parser('parse')
    parser.set_defaults(func=main)
    parser.add_argument('pdml', type=str, help='PDML file to parse')
    parser.add_argument('--mbytes', action="store_true",
                   help='Outputs the location of missing bytes, this is common. *** DOES NOT WORK IF PDML DOES NOT INCLUDE HEX STREAM ***')
    parser.add_argument('--pbytes', action="store_true",
                   help='Outputs a hex stream for the data if possible ***BUGGY DUE TO BROKEN DISSECTORS***')
    parser.add_argument('--pp', action="store_true",
                   help='Prints out the parsed version of the file.')
