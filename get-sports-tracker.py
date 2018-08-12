#!/usr/bin/env python
# coding=utf-8

import requests
import os
from datetime import datetime

def get_my_gpx():
	my_gpx_list = []
	proc = Popen("ls", shell=True, stdout=PIPE, )
	output = proc.communicate()[0]
	lista = output.split("\n")
	lista.remove('')

	for x in lista:
		x = x.split('-')
		x = x[2].split('.')
		my_gpx_list.append(x[0])

	return my_gpx_list

def get_gpx_files(ids_treino):
	for y, identificador in enumerate(ids_treino):
		print "Treino: ", y+1 , " de ", len(ids_treino)
		url = 'http://www.sports-tracker.com/apiserver/v1/workout/exportGpx/'+identificador+'?token='+TOKEN

		os.system('wget '+url+' -O '+USER+'-'+str(y)+'-'+identificador+'.gpx')

def get_gpx_ids(STTAuthorization):
	s = requests.Session()
	resumo_treinos = s.get('http://www.sports-tracker.com/apiserver/v1/workouts?limited=true&limit=1000000', headers=STTAuthorization).json()
	resumo_treinos = resumo_treinos['payload']

	ids_treino = []

	for x in resumo_treinos:
		ids_treino.append(x['workoutKey'])

	return ids_treino

if __name__ == '__main__':

	i = datetime.now()
	USER = 'jan'
	SENHA = 'x'
	NOME_DA_PASTA = 'sports-tracker'
	DATA = i.strftime('%Y-%m-%d')

	s = requests.Session()
	login = s.post('http://www.sports-tracker.com/apiserver/v1/login?source=javascript', data={'l': USER, 'p': SENHA})

	TOKEN = login.json()['sessionkey']
	STTAuthorization = {'STTAuthorization': TOKEN}

	ids = get_gpx_ids(STTAuthorization)
	get_gpx_files(ids)
