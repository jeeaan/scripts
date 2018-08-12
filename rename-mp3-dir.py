#coding=utf8
from selenium import webdriver
from selenium.webdriver.support.ui import Select

browser = webdriver.Chrome()

f = open('teste.txt', 'r')

linhas = f.readlines()

lista_novos_nomes = []

for busca in linhas:

	if busca.find('_-_19') < 0:
		if busca.find('_-_2') < 0:
			browser.get('https://www.bing.com/?q='+busca+' release')

			busca = busca.replace("_", " ")

			try:
				div_ano = browser.find_element_by_class_name('b_focusTextLarge')
				ano = div_ano.text

				nome = busca[0:busca.find('-')+2]+ano+' '+busca[busca.find('-'):]

				nome_velho = busca.replace('\n', '')
				nome = nome.replace('\n', '')
				nome = [nome_velho, str(nome)]
				lista_novos_nomes.append(nome)
				print nome

			except:
				try:
					browser.get('https://www.bing.com/?q='+busca+' album release')
					div_wiki = browser.find_element_by_class_name('b_entityTP')
					if div_wiki.text.find("Release year") >= 0:
						ano = div_wiki.text[div_wiki.text.find("Release year")+14:div_wiki.text.find("Release year")+18]
					if div_wiki.text.find("Release date") >= 0:
						ano = div_wiki.text[div_wiki.text.find("Release date")+27:div_wiki.text.find("Release date")+31]
					
					if ano.isnumeric():
						nome = busca[0:busca.find('-')+2]+ano+' '+busca[busca.find('-'):]

						busca = busca.replace('\n', '')
						nome = nome.replace('\n', '')
						nome = [busca, str(nome)]
						lista_novos_nomes.append(nome)
						print nome
					else:
						print busca + "não achei na wiki"

				except:
					pass
					print busca + " não achei porra nenhuma"
ano = ""
nome = ""