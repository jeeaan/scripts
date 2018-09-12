#!/usr/bin/env python
# coding=utf-8

from subprocess import Popen,PIPE,STDOUT,call
from time import strftime
from datetime import datetime, timedelta
import sys

ARQUIVO = "/home/jean/diario.txt"
STATUS_CHEGADA = "chegou"
STATUS_SAIDA = "saiu"

macs_ok = ["e8:89:2c:45:79:31","00:1e:58:2a:3a:9a",
"a4:77:33:fe:77:a8","80:d2:1d:42:27:fc","54:60:09:bc:61:a0","bc:6e:64:aa:37:2c", "50:92:B9:4B:19:12"]

def not_authorized():
	now_in_network = "sudo arp-scan --interface=wlp2s0 --localnet | grep -o -E \'([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}\'"

	proc=Popen(now_in_network, shell=True, stdout=PIPE, )
	output=proc.communicate()[0]

	now_in_network = output.split("\n")

	not_authorized = list(set(now_in_network) - set(macs_ok))
	not_authorized.remove('')

	return not_authorized

def check(mac_address):
	now_in_network = "sudo arp-scan --interface=wlp2s0 --localnet | grep -o -E \'([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}\'"
	proc=Popen(now_in_network, shell=True, stdout=PIPE, )
	output=proc.communicate()[0]

	now_in_network = output.split("\n")

	return mac_address in now_in_network

def bate_ponto(mac_address):
	status = ultimo_status()
	if not check(mac_address):
		if status == STATUS_CHEGADA:
			escreve(STATUS_SAIDA)
	elif status == STATUS_SAIDA:
		escreve(STATUS_CHEGADA)
	else:
		escreve("Vamos começar!")

def escreve(status):
	hora_agora = datetime.today()
	hora_agora = hora_agora.strftime("%Y-%m-%d %H:%M:%S")
	text_file = open(ARQUIVO, "a")
	text_file.write("\n"+hora_agora+" -"+status)
	text_file.close()

def ultimo_status():
	text_file = open(ARQUIVO, "r")
	diario = text_file.read()
	try:
		ultimo_status = diario.split("-")
		ultimo_status = ultimo_status[len(ultimo_status)-1]
		if ultimo_status.startswith(STATUS_CHEGADA):
			return STATUS_CHEGADA
		elif ultimo_status.startswith(STATUS_SAIDA):
			return STATUS_SAIDA
		else:
			return ""
	except:
		return ""

if __name__ == '__main__':
	if len(sys.argv) < 2:
		sys.exit(1)

	mac_address = sys.argv[1]
	bate_ponto(mac_address)