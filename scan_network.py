#!/usr/bin/env python
# coding=utf-8

from subprocess import Popen,PIPE,STDOUT,call

macs_ok = ["e8:89:2c:45:79:31","00:1e:58:2a:3a:9a",
"a4:77:33:fe:77:a8","80:d2:1d:42:27:fc","54:60:09:bc:61:a0","bc:6e:64:aa:37:2c", "50:92:B9:4B:19:12"]

now_in_network = "sudo arp-scan --interface=wlp2s0 --localnet | grep -o -E \'([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}\'"

proc=Popen(now_in_network, shell=True, stdout=PIPE, )
output=proc.communicate()[0]

now_in_network = output.split("\n")

not_authorized = list(set(now_in_network) - set(macs_ok))
not_authorized.remove('')

print not_authorized
