import commands
import os

ip = commands.getoutput('wget http://ipinfo.io/ip -qO -')
ip = ip.split('.')

ip_mais_um = ""

for x in ip:
	ip = int(x)+1
	ip_mais_um = ip_mais_um +" "+ str(ip)

os.system("echo $(date) "+ip_mais_um+" > teste")

os.system("git add teste")
os.system("git commit -m 'bla bla'")
os.system("")
