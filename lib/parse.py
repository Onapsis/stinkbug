from lxml import etree
import sys 

unmasked = []

# recurse each packet for the goodness
def recurse_tree(val,i,delim,f):
    
    for child in val:
    
        if len(child.getchildren()) > 0:
            if type(child.get("showname")):
                f.write("#"+i*delim+str(child.get("show"))+"\n")       
            else:
                f.write("#"+i*delim+child.get("showname")+"\n")
            if i == 1:
                f.write("# TRUTH value:"+str(child.get("value"))+"\",pos:"+str(child.get("pos"))+",size:"+str(child.get("size"))+"\n")
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
                        f.write("#"+i*delim+"UNSURE WHAT TO DO ==> "+str(child.get("showname"))+"\n")
                    else:
                        f.write(i*delim+"value:\""+str(child.get("value"))+"\",pos:"+str(child.get("pos"))+",size:"+str(child.get("size"))+"\n")
    
            else:
                f.write("#"+i*delim+child.get("show"))
                
                if str(child.get("value")) == "":
                    # if the value is blank print an error
                    f.write("#"+i*delim+"UNSURE WHAT TO DO ==> "+i*delim+str(child.get("showname"))+"\n")
                else:
                    # else the value is not blank
                    f.write(i*delim+"value:\""+str(child.get("value"))+"\",pos:"+str(child.get("pos"))+",size:"+str(child.get("size"))+"\n")

def run(fname,pdml):
    # import the pdml into tree
    tree = etree.parse(pdml)

    # parse based on protocol
    packets = [e for e in tree.xpath('/pdml/packet/proto')]

    # ignore boring parts of the frame
    consts = ["geninfo","frame","eth","ip","tcp"]

    # contains tuple [position, length, unmasked value]
    unmasked = []

    # create a temporary file
    f = open("/tmp/stinkbug_"+fname+".txt",'w')

    # parse the pdml and write to the file                   
    for i in packets:
        if not i.get("name") in consts:
            
            # Not one of the common fields
            f.write("\n#TOP:"+str(i.get("name")))
            
            #if we have children, call recursion
            if len(i.getchildren()) > 0:
                recurse_tree(i.getchildren(),1,"-",f)
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
    ns = open(fname, "r" )
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
            #print line
            #print line.split("value:")[1].split(",")[0].replace("\"","")
            if old_pos == truth_pos:
                old_pos = int(line.split("pos:")[1].split(",")[0])+int(line.split("size:")[1])
            else:
                pos = int(line.split("pos:")[1].split(",")[0])
                # get the pos and the size
                new_pos = pos+int(line.split("size:")[1])
                
                if not old_pos == pos:
                    print "#|!| bytes missing, check at position "+str(pos)+" for "+str(int(pos-old_pos))+" missing bytes"
                    #print "value:"+str("00"*int(pos-old_pos)) 
                    #sys.stdout.write(str(buff*int(pos-old_pos)))           
                old_pos = new_pos

    print "\n"
    ns.close()

