from lxml import etree
import random 
import string 
from lib import parse as parse
                    
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
        outfile = ""
        
        print "|+| Using /tmp/stinkbug_"+fname+".txt as a temporary file"
        parse.run(fname,pdml,frame.getchildren())
    
        template = "./templates/sulley_fuzz.py" if not args.template else args.template
    
        if args.outfile:
            print "|+| Writing output to "+str(args.outfile)
            parse.output_file("/tmp/stinkbug_"+fname+".txt",template,args.outfile,"s_static(\"===VALUE===\")","#===VALUE===")        
        if args.outdir:
            outfile = str(args.outdir)+"peach_"+str(ofname)+"_"+str(n)+".txt"
            print "|+| Writing output to "+outfile
            parse.output_file("/tmp/stinkbug_"+fname+".txt",template,outfile,"s_static(\"===VALUE===\")","#===VALUE===")        
        else: 
            # the value option is specific to sulley
            parse.output("/tmp/stinkbug_"+fname+".txt",template,"s_static(\"===VALUE===\")","#===VALUE===")
        n = n + 1


# initialize the module here
def load_(subparser):
    parser = subparser.add_parser('sulley')
    parser.set_defaults(func=main)
    parser.add_argument('pdml', type=str, help='PDML file to parse')
    parser.add_argument('--outfile', type=str,
                   help='Output a test to a file')
    parser.add_argument('--template', type=str,
                   help='Template to use')
    parser.add_argument('--outdir', type=str,
                   help='A directory to output the files to.')

