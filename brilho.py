#!/usr/bin/env python
# coding=utf-8

# Uso: 
# ./brilho.py diurno
# ./brilho.py noturno
# ./brilho.py red

import os
import sys
from subprocess import Popen,PIPE,STDOUT,call

ARQUIVO="/tmp/.intensidade"
DIURNO="--brightness 0.99"
NOTURNO="--brightness 0.15"
RED="--gamma 11.1:1:1"

def tela():
	tela = "xrandr | grep \" connected\" | cut -f1 -d \" \""
	proc=Popen(tela, shell=True, stdout=PIPE, )
	output=proc.communicate()[0]
	if "\n" in output:
		output = output.replace("\n", "")

	return output

def screen(modo, tela):
	os.system("xrandr --output " +tela+ " " +modo+ "")

def brilha(intensidade, modo, tela):
	try:
		atual = le()

		if modo == "mais":
			nova = float(atual)+float(intensidade)
			if(nova <= 0.99):
				os.system("xrandr --output " +tela+ " --brightness " +str(nova)+ "")
				escreve(str(nova))
		if modo == "menos":
			nova = float(atual)-float(intensidade)
			if(nova >= 0.10):
				os.system("xrandr --output " +tela+ " --brightness " +str(nova)+ "")
				escreve(str(nova))
	except:
		return ""

def escreve(intensidade):
	try:
		text_file = open(ARQUIVO, "w")
		text_file.write(intensidade)
		text_file.close()
	except:
		os.system("echo 0.99 > "+ARQUIVO)

def le():
	try:
		text_file = open(ARQUIVO, "r")
		intensidade = text_file.read()
		text_file.close()
	except:
		escreve("0.99")

	return intensidade

if __name__ == '__main__':
	if len(sys.argv) < 2:
		sys.exit(1)

	MODO = sys.argv[1]
	tela = tela()

	if MODO == "diurno":
		screen(DIURNO, tela)
	elif MODO == "noturno":
		screen(NOTURNO, tela)
	elif MODO == "red":
		screen(RED, tela)
	elif MODO == "mais":
		brilha(0.09, MODO, tela)
	elif MODO == "menos":
		brilha(0.09, MODO, tela)