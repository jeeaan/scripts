#!/usr/bin/env python
# coding=utf-8

from subprocess import Popen,PIPE,STDOUT,call
from time import strftime
from datetime import datetime, timedelta
import sys

DIARIO = "/home/jean/diario.txt"
STRANGE = "/home/jean/stranges.txt"

STATUS_CHEGADA = "conectou"
STATUS_SAIDA = "desconectou"

MACS_MAP =	{
  "A4:77:33:FE:77:A8": "Chromecast_Audio",
  "54:60:09:BC:61:A0": "Chromecast_1",
  "80:D2:1D:42:27:FC": "Chromecast_2",
  "94:39:E5:F4:12:B9": "SonyZ3",
  "40:88:05:22:91:6A": "MotoG3Turbo",
  "e8:89:2c:45:79:31": "ArrisTG",
  "94:39:E5:F4:12:B9": "Itautec",
  "50:92:b9:4b:19:12": "SamsungA5"
}

def tem_estranho(network_now, authorized):
	mac_address = not_authorized(network_now, authorized)
	if mac_address:
		escreve(STATUS_CHEGADA, mac_address, STRANGE)

def now_on_network():
	now_in_network = "sudo arp-scan --interface=wlp2s0 --localnet | grep -o -E \'([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}\'"

	proc=Popen(now_in_network, shell=True, stdout=PIPE, )
	output=proc.communicate()[0]

	now_in_network = output.split("\n")
	now_in_network = [x.lower() for x in now_in_network]

	return now_in_network

def not_authorized(network_now, authorized):

	not_authorized = list(set(network_now) - set(authorized))
	if '' in not_authorized:
		not_authorized.remove('')

	return ','.join(not_authorized)

def check(mac_address, network_now):
	return mac_address.lower() in network_now

def bate_ponto(mac_address, network_now):
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

	network_now = now_on_network()
	authorized = [mac.lower() for mac in MACS_MAP]

	bate_ponto(mac_address, network_now)
	tem_estranho(network_now, authorized)