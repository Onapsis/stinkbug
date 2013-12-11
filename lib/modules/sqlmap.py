from lxml import etree
import random 
import string 
from lib import parse as parse

# this takes in a file and outputs the data as a sqlmap configuration file. 
def output_file(fname,template,outfile):
    verb,uri,host = "","",""
    outfile = open(outfile,"w")
    
    # piece together the request
    with open(fname) as f:
        ns = f.readlines()
   
    i = 0
    for line in ns:
        if "http.request.method" in line:
            linex = ns[i+1]
            verb = linex.split("value:")[1].split(",")[0].replace("\"","").decode("hex")
        if "http.request.uri" in line:
            linex = ns[i+1]
            uri = linex.split("value:")[1].split(",")[0].replace("\"","").decode("hex").replace("\r\n","")
        if "http.host" in line:
            linex = ns[i+1]
            host = linex.split("value:")[1].split(",")[0].replace("\"","").decode("hex").replace("Host: ","").replace("\r\n","")
        i = i + 1
    
    if verb == "":
        return

    temp = open(template, "r" )
    if verb == "GET":        
        # write the template file here
        for temp_line in temp:
            if "url =" in temp_line:
                outfile.write("url= http://"+host+uri
                outfile.write("\n")
            else:
                outfile.write(temp_line.replace("\n",""))
                outfile.write("\n")
    else:
        print "|!| Unknown verb used, printing out the info. Good luck."
            
# this takes in a file and outputs the data as a sqlmap configuration file. 
def output(fname,template):
    verb,uri,host = "","",""
    
    # piece together the request
    with open(fname) as f:
        ns = f.readlines()
   
    i = 0
    for line in ns:
        if "http.request.method" in line:
            linex = ns[i+1]
            verb = linex.split("value:")[1].split(",")[0].replace("\"","").decode("hex")
        if "http.request.uri" in line:
            linex = ns[i+1]
            uri = linex.split("value:")[1].split(",")[0].replace("\"","").decode("hex").replace("\r\n","")
        if "http.host" in line:
            linex = ns[i+1]
            host = linex.split("value:")[1].split(",")[0].replace("\"","").decode("hex").replace("Host: ","").replace("\r\n","")
        i = i + 1
    
    if verb == "":
        return

    temp = open(template, "r" )
    if verb == "GET":        
        # write the template file here
        for temp_line in temp:
            if "url =" in temp_line:
                print "url= http://"+host+uri
            else:
                print temp_line.replace("\n","")
    else:
        print "|!| Unknown verb used, printing out the info. Good luck."
    
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
            output_file("/tmp/stinkbug_"+fname+".txt","./templates/sqlmap.conf",args.outfile)        
        else: 
            output("/tmp/stinkbug_"+fname+".txt","./templates/sqlmap.conf")

# initialize the module here
def load_(subparser):
    parser = subparser.add_parser('sqlmap')
    parser.set_defaults(func=main)
    parser.add_argument('pdml', type=str, help='PDML file to parse')
    parser.add_argument('--outfile', type=str,
                   help='Output a test to a file; NOTE: only works on SECURITY_TESTS')
    
