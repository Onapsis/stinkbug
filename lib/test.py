import sys

# This is meant to hold the different security tests that can be output

# this takes in a file and outputs the data as a sulley configuration file. 
def output_sulley(fname,template):

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

