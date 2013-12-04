#!/usr/bin/env python
# Fuzzing the initial 4-byte packet from client to CMS with aps request.
import time
import sys
from sulley import *

# Time to wait between mutations
SLEEP_TIME=1
# Time to wait before claiming a host is unresponsive
TIMEOUT=1
# number of crashes to observe before skipping the remainder of a group
CRASH_THRESHOLD=300

# Initialize the Sulley mutation descriptor
# TODO ------- THIS PACKET NAME SHOULD BE UNIQUE
s_initialize("UNIQUE_packet")

# define a group primitive listing the various HTTP verbs we wish to fuzz.
s_group("verbs", values=["OPTIONS","GET","HEAD","POST","PUT","DELETE","TRACE","CONNECT","PROPFIND","PROPPATCH","MKCOL","COPY","MOVE","LOCK","UNLOCK","VERSION-CONTROL","REPORT","CHECKOUT","CHECKIN","UNCHECKOUT","MKWORKSPACE","UPDATE","LABEL","MERGE","BASELINE-CONTROL","MKACTIVITY","ORDERPATCH","ACL","PATCH","SEARCH","ARBITRARY"])

if s_block_start("body", group="verbs"):
# << -------- >>
s_block_end("body")

print "Total mutations: " + str(s_num_mutations()) + "\n"
print "Minimum time for execution: " + str(round(((s_num_mutations() * (SLEEP_TIME))/3600),2)) + " hours."

sess = sessions.session(session_filename="UNIQUE_packet.sess", sleep_time=SLEEP_TIME, timeout=TIMEOUT, crash_threshold=CRASH_THRESHOLD) # TODO ------- THIS PACKET NAME SHOULD BE UNIQUE


# Tie this session to the unique packet name fuzzing case
sess.connect(s_get("UNIQUE_packet")) # TODO ------- THIS PACKET NAME SHOULD BE UNIQUE

# # TODO ------- Add in the target info
target = sessions.target("<IP>", <PORT>)
# Add the target to the session (can be repeated for multiple targets)
sess.add_target(target)

# Kick off the fuzzer, monitoring with WebUI on localhost:26000
sess.fuzz()
