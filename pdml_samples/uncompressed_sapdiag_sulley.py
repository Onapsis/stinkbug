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

##TOP:sapni#-sapni.length
s_static("00000017".decode("hex"))
##-sapni.payload
##-UNSURE WHAT TO DO ==> Payload
##TOP:sapdiag#-
##-Header
## TRUTH value:"",pos:70,size:8
##--sapdiag.header.mode
s_static("00".decode("hex"))
##--0x00
##--Com Flag: 0x00
##---sapdiag.header.comflag.TERM_EOS
s_static("00".decode("hex"))
##---^^^sapdiag.header.comflag.TERM_EOC
##---^^^sapdiag.header.comflag.TERM_NOP
##---^^^sapdiag.header.comflag.TERM_EOP
##---^^^sapdiag.header.comflag.TERM_INI
##---^^^sapdiag.header.comflag.TERM_CAS
##---^^^sapdiag.header.comflag.TERM_NNM
##---^^^sapdiag.header.comflag.TERM_GRA
##--sapdiag.header.modestat
s_static("00".decode("hex"))
##--sapdiag.header.errorflag
s_static("00".decode("hex"))
##--sapdiag.header.msgtype
s_static("00".decode("hex"))
##--sapdiag.header.msginfo
s_static("00".decode("hex"))
##--sapdiag.header.msgrc
s_static("00".decode("hex"))
##--sapdiag.header.compress
s_static("00".decode("hex"))
##-
##-Message
## TRUTH value:"",pos:78,size:15
##--
##--Item: APPL, UI_EVENT, UI_EVENT_SOURCE, Len=65535
##---sapdiag.item.type
s_static("10".decode("hex"))
##---sapdiag.item.id
s_static("0f".decode("hex"))
##---sapdiag.item.sid
s_static("01".decode("hex"))
##---65535
##---Length: 65535
##----None
##----Expert Info (Warn/Malformed): The item length is invalid
s_static("ffff".decode("hex"))
##-----expert.message
##-----UNSURE WHAT TO DO ==> Message: The item length is invalid
##-----expert.severity
##-----UNSURE WHAT TO DO ==> Severity level: Warn
##-----expert.group
##-----UNSURE WHAT TO DO ==> Group: Malformed
##----malformed
##----UNSURE WHAT TO DO ==> Malformed Packet
##---
##---Value, Event Type=Unknown, Control Type=Unknown
##----65
##----UI Event Valid: 65
##-----sapdiag.item.value.uievent.valid.MENU_POS
s_static("41".decode("hex"))
##-----^^^^^sapdiag.item.value.uievent.valid.CONTROL_POS
##-----^^^^^sapdiag.item.value.uievent.valid.NAVIGATION_DATA
##-----^^^^^sapdiag.item.value.uievent.valid.FUNCTIONKEY_DATA
##----sapdiag.item.value.uievent.type
s_static("4141".decode("hex"))
##----sapdiag.item.value.uievent.control
s_static("4141".decode("hex"))
##----sapdiag.item.value.uievent.data
s_static("41".decode("hex"))
##----sapdiag.item.value.uievent.data
s_static("41".decode("hex"))
##----sapdiag.item.value.uievent.data
s_static("41".decode("hex"))
##----sapdiag.item.value.uievent.data
s_static("41".decode("hex"))
##TOP:short

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
