from lxml import etree
import sys
import random 

unmasked = []

# recurse each packet for the goodness
def recurse_tree(val,i,delim,f):
    for child in val:
        if len(child.getchildren()) > 0:
            if type(child.get("showname")):
                f.write("#"+i*delim+str(child.get("show"))+"\n")                       
            if child.get("name") == "expert":
                # there was an error, lets grab the value if we can
                if type(child.getparent().get("value")):
                    f.write("#"+i*delim+child.get("showname")+"\n")
                    f.write(i*delim+"value:\""+str(child.getparent().get("value"))+"\",pos:"+str(child.getparent().get("pos"))+",size:"+str(child.getparent().get("size"))+"\n")
            else:
                f.write("#"+i*delim+child.get("showname")+"\n")
            if i == 1:
                f.write("# TRUTH value:\""+str(child.get("value"))+"\",pos:"+str(child.get("pos"))+",size:"+str(child.get("size"))+"\n")
            recurse_tree(child.getchildren(),i+1,delim,f)
    
        else:
            if str(child.get("name")):        
    
                # first check if it has an unmasked value
                if(child.get("unmaskedvalue")):                    
                    # if unmasked value exists in the array, print comment
                    if {child.get("pos"),child.get("size"),child.get("unmaskedvalue")} in unmasked:
                        f.write("#"+i*delim+i*"^"+child.get("name")+"\n") 
                                               
                    # if unmasked value not in array, print and add                            
                    else:
                        unmasked.append({child.get("pos"),child.get("size"),child.get("unmaskedvalue")})
                        f.write("#"+i*delim+child.get("name")+"\n")
                        f.write(i*delim+"value:\""+str(child.get("unmaskedvalue"))+"\",pos:"+str(child.get("pos"))+",size:"+str(child.get("size"))+"\n")
    
                else:
                    f.write("#"+i*delim+child.get("name")+"\n") 
                    if str(child.get("value")) == "" or child.get("value") is None:
                        f.write("#"+i*delim+"UNSURE WHAT TO DO WITH ==> "+str(child.get("showname"))+"\n")
                    else:
                        f.write(i*delim+"value:\""+str(child.get("value"))+"\",pos:"+str(child.get("pos"))+",size:"+str(child.get("size"))+"\n")
    
            else:
                f.write("#"+i*delim+child.get("show")+"\n")
                
                if str(child.get("value")) == "":
                    # if the value is blank print an error
                    f.write("#"+i*delim+"UNSURE WHAT TO DO WITH ==> "+i*delim+str(child.get("showname"))+"\n")
                else:
                    # else the value is not blank
                    f.write(i*delim+"value:\""+str(child.get("value"))+"\",pos:"+str(child.get("pos"))+",size:"+str(child.get("size"))+"\n")

def run(fname,pdml,packets):
    # ignore boring parts of the frame
    consts = ["geninfo","frame","eth","ip","tcp"]

    # contains tuple [position, length, unmasked value]
    unmasked = []

    # create a temporary file
    f = open("/tmp/stinkbug_"+fname+".txt",'w')
   
    for packet in packets:
        if not packet.get("name") in consts:
                    
            # Not one of the common fields
            f.write("\n#TOP:"+str(packet.get("name")))
                    
            #if we have children, call recursion
            if len(packet.getchildren()) > 0:
                recurse_tree(packet.getchildren(),1,"-",f)
            else:
                print "Hrm, no children"

    # close the file
    f.close()

# this takes in a file and pieces the stream back together. 
#   If there are missing hex, it will dumbly add them in as the buffer string
def print_buffer(fname,buff):
    # check for chars not in the pdml that we missed
    ns = open(fname, "r" )
    array = []

    old_pos = 0
    truth_pos = 0

    for line in ns:
        # check for the truth first
        if "TRUTH" in line:
            if "pos:\"" in line:
                old_pos = int(line.split("pos:\"")[1].split(",")[0])
                truth_pos = old_pos
            if "pos:" in line:
                old_pos = int(line.split("pos:")[1].split(",")[0])
                truth_pos = old_pos
            
        if "#" in line:
            #print line
            "ignore"
        if "value" in line and not "#" in line:
            #print line
            sys.stdout.write(line.split("value:")[1].split(",")[0].replace("\"",""))
            if old_pos == truth_pos:
                old_pos = int(line.split("pos:")[1].split(",")[0])+int(line.split("size:")[1])
            else:
                pos = int(line.split("pos:")[1].split(",")[0])
                # get the pos and the size
                new_pos = pos+int(line.split("size:")[1])
                
                if not old_pos == pos:
                    #print "#|!!| bytes missing, adding nulls "+str(int(pos-old_pos))
                    #print "value:"+str("00"*int(pos-old_pos)) 
                    sys.stdout.write(str(buff*int(pos-old_pos)))           
                old_pos = new_pos

    print "\n"
    ns.close()

# this takes in a file and outputs the missing bytes
def missing_bytes(fname):
    # check for chars not in the pdml that we missed
    ns = open(fname, "rw" )
    array = []

    old_pos = 0
    truth_pos = 0

    for line in ns:
        # check for the truth first
        if "TRUTH" in line:
            old_pos = int(line.split("pos:")[1].split(",")[0])
            truth_pos = old_pos
            
        if "#" in line:
            #print line
            "ignore"
        if "value" in line and not "#" in line:
            if truth_pos == 0:
                print "|!| There was no top level value (i.e. TRUTH), check the dissector for correctness"
                ns.close()
                break
                 
            #print line
            #print line.split("value:")[1].split(",")[0].replace("\"","")
            if old_pos == truth_pos:
                old_pos = int(line.split("pos:")[1].split(",")[0])+int(line.split("size:")[1])
            else:
                pos = int(line.split("pos:")[1].split(",")[0])
                # get the pos and the size
                new_pos = pos+int(line.split("size:")[1])
                
                if not old_pos == pos:
                    print "#|!| bytes missing, check starting at position "+str(pos)+" for "+str(int(pos-old_pos))+" missing bytes"
                    #print "value:"+str("00"*int(pos-old_pos)) 
                    #sys.stdout.write(str(buff*int(pos-old_pos)))           
                old_pos = new_pos

    print "\n"
    ns.close()

# this takes in a file and outputs the data given the inp string
#   For example for peach inp will be "s_static(===VALUE===)"
def output(fname,template,inp, comment):
    temp = open(template, "r" )
    
    for temp_line in temp:
        if "<< -------- >>" in temp_line:            
            # check for chars not in the pdml that we missed
            ns = open(fname, "r" )
    
            num = 0
            for line in ns:
                if "#" in line:
                    v = line.replace("\n","")
                    print comment.replace("===VALUE===",v)
                if "value" in line and not "#" in line:
                    # peach uses space between hex value, value needs to be parsed
                    s = line.split("value:")[1].split(",")[0].replace("\"","")
                    p_value = "".join(s[i:i+2] + " " for i in xrange(0,len(s),2)) 
                    val = line.split("value:")[1].split(",")[0].replace("\"","")
                    print inp.replace("===VALUE===",val).replace("===RAND===",str(random.randrange(0,1000)))
                    num = num + 1
         
            ns.close()
        else:
            print temp_line.replace("\n","")

# this takes in a file and writes a file from a template 
def output_file(fname,template,outfile,inp,comment):
    temp = open(template, "r" )
    outfile = open(outfile,"w")
    
    for temp_line in temp:
        if "<< -------- >>" in temp_line:            
            # check for chars not in the pdml that we missed
            ns = open(fname, "r" )
    
            num = 0
            for line in ns:
                if "#" in line:
                    v = line.replace("\n","")
                    outfile.write(comment.replace("===VALUE===",v))
                    outfile.write("\n")
                if "value" in line and not "#" in line:
                    # peach uses space between hex value, value needs to be parsed
                    s = line.split("value:")[1].split(",")[0].replace("\"","")
                    p_value = "".join(s[i:i+2] + " " for i in xrange(0,len(s),2)) 
                    
                    val = line.split("value:")[1].split(",")[0].replace("\"","")
                    outfile.write(inp.replace("===VALUE===",val).replace("===RAND===",str(random.randrange(0,1000))))
                    outfile.write("\n")
                    num = num + 1
         
            ns.close()
        else:
            outfile.write(temp_line.replace("\n","")+"\n")
    outfile.close()
            
