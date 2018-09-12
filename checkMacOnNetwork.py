#!/usr/bin/env python
# coding=utf-8

from subprocess import Popen,PIPE,STDOUT,call
from time import strftime
from datetime import datetime, timedelta
import sys

DIARIO = "/home/jean/diario.txt"
STRANGE = "home/jean/strange.txt"

STATUS_CHEGADA = "conectou"
STATUS_SAIDA = "desconectou"

def now_on_network():
	now_in_network = "sudo arp-scan --interface=wlp2s0 --localnet | grep -o -E \'([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}\'"

	proc=Popen(now_in_network, shell=True, stdout=PIPE, )
	output=proc.communicate()[0]

	now_in_network = output.split("\n")
	now_in_network = [x.lower() for x in now_in_network]

	return now_in_network

def not_authorized(network_now):
	MACS_OK = ["e8:89:2c:45:79:31","00:1e:58:2a:3a:9a","a4:77:33:fe:77:a8","80:d2:1d:42:27:fc","54:60:09:bc:61:a0","bc:6e:64:aa:37:2c"]
	MACS_OK = [x.lower() for x in MACS_OK]
	not_authorized = list(set(network_now) - set(MACS_OK))
	if '' in not_authorized:
		not_authorized.remove('')

	return ','.join(not_authorized)

def check(mac_address, network_now):
	return mac_address.lower() in network_now

def bate_ponto(mac_address):
	network_now = now_on_network()
	status = ultimo_status(DIARIO)

	if not check(mac_address, network_now):
		if status == STATUS_CHEGADA:
			escreve(STATUS_SAIDA, mac_address, DIARIO)
	elif status == STATUS_SAIDA:
		escreve(STATUS_CHEGADA, mac_address, DIARIO)

def escreve(status, mac_address, arquivo):
	hora_agora = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	text_file = open(arquivo, "a")
	text_file.write("\n"+mac_address+" > "+hora_agora+" -"+status)
	text_file.close()

def ultimo_status(arquivo):
	text_file = open(arquivo, "r")
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