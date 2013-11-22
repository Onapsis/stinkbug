from lxml import etree
import random 
import string 
from lib import parse as parse

# this takes in a file and outputs the data as a sulley configuration file. 
def output_file(fname,template,outfile):

    temp = open(template, "r" )
    out = open(outfile, "w" )
    
    for temp_line in temp:
        if "# << -------- >>" in temp_line:            
            # check for chars not in the pdml that we missed
            ns = open(fname, "r" )

            for line in ns:
                if "#" in line:
                    out.write(line.replace("\n","")+"\n")
                if "value" in line and not "#" in line:
                    out.write("s_static(\""+line.split("value:")[1].split(",")[0].replace("\"","")+"\".decode(\"hex\"))"+"\n")

            ns.close()
        else:
            out.write(temp_line.replace("\n","")+"\n")
            
# this takes in a file and outputs the data as a sulley configuration file. 
def output(fname,template):

    temp = open(template, "r" )
    
    for temp_line in temp:
        if "# << -------- >>" in temp_line:            
            # check for chars not in the pdml that we missed
            ns = open(fname, "r" )

            for line in ns:
                if "#" in line:
                    print line.replace("\n","")
                if "value" in line and not "#" in line:
                    print "s_static(\""+line.split("value:")[1].split(",")[0].replace("\"","")+"\")"

            ns.close()
        else:
            print temp_line.replace("\n","")
        
# sulley module
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
    if len(frames) > 1 and args.outfile:
            print "|!| More than one frame, but --outfile used. Please use --outdir instead."
            return
            
    for frame in frames:

        fname = ofname+"_"+str(n)
        print "|+| Using /tmp/stinkbug_"+fname+".txt as a temporary file"
        parse.run(fname,pdml,frame.getchildren())
    
        if args.outfile:
            print "|+| Writing output to "+str(args.outfile)
            output_file("/tmp/stinkbug_"+fname+".txt","./templates/sulley_fuzz.py",args.outfile)        
        else: 
            output("/tmp/stinkbug_"+fname+".txt","./templates/sulley_fuzz.py")

# initialize the module here
def load_(subparser):
    parser = subparser.add_parser('sulley')
    parser.set_defaults(func=main)
    parser.add_argument('pdml', type=str, help='PDML file to parse')
    parser.add_argument('--outfile', type=str,
                   help='Output a test to a file; NOTE: only works on SECURITY_TESTS')

