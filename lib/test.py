import sys

# This is meant to hold the different security tests that can be output

# this takes in a file and outputs the data as a sulley configuration file. 
def output_sulley_file(fname,template,outfile):

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
def output_sulley(fname,template):

    temp = open(template, "r" )
    out = open(outfile, "r" )
    
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
            

