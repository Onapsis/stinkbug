#!/usr/bin/env python
# Fuzzing the initial 4-byte packet from client to CMS with aps request.
import time
import sys
from sulley import *

# Time to wait between mutations
SLEEP_TIME=10
# Time to wait before claiming a host is unresponsive
TIMEOUT=1
# number of crashes to observe before skipping the remainder of a group
CRASH_THRESHOLD=300

# Initialize the Sulley mutation descriptor
# TODO ------- THIS PACKET NAME SHOULD BE UNIQUE
s_initialize("UNIQUE_packet")

#TOP:giop#-Magic number: GIOP
s_static("47494f50".decode("hex"))
#-Version: 1.1
s_static("0101".decode("hex"))
#-0x01
# TRUTH value:"01",pos:72,size:1
#--^^giop.flags.ziop_enabled
#--^^giop.flags.ziop_supported
#--^^giop.flags.fragment
#--^^giop.flags.little_endian
#-giop.type
s_static("05".decode("hex"))
#-giop.len
s_static("00000000".decode("hex"))

print "Total mutations: " + str(s_num_mutations()) + "\n"
print "Minimum time for execution: " + str(round(((s_num_mutations() * (SLEEP_TIME))/3600),2)) + " hours."

sess = sessions.session(session_filename="cs32_packet.sess", sleep_time=SLEEP_TIME, timeout=TIMEOUT, crash_threshold=CRASH_THRESHOLD)

# Tie this session to the unique packet name fuzzing case
sess.connect(s_get("UNIQUE_packet"))

# # TODO ------- Add in the target info
target = sessions.target("<IP>", <PORT>)
target.procmon   = pedrpc.client("<IP>",  <SULLEY_PORT>)
target.procmon_options = \
{
    "proc_name"      : "<PROCESS_NAME>",
}
# Add the target to the session (can be repeated for multiple targets)
sess.add_target(target)

# Kick off the fuzzer, monitoring with WebUI on localhost:26000
sess.fuzz()
