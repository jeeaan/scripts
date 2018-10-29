# coding=utf-8
import string, unicodedata, PyPDF2, sys, itertools

from collections import Counter

PDFS = ["2018-01-02_O_001_boletim_interno.pdf",
"2018-01-04_O_002_boletim_interno.pdf",
"2018-01-09_O_003_boletim_interno.pdf",
"2018-01-11_O_004_boletim_interno.pdf",
"2018-01-16_O_005_boletim_interno.pdf",
"2018-01-18_O_006_boletim_interno.pdf",
"2018-01-23_O_007_boletim_interno.pdf",
"2018-01-25_O_008_boletim_interno.pdf",
"2018-01-30_O_009_boletim_interno.pdf",
"2018-02-01_O_010_boletim_interno.pdf",
"2018-02-06_O_011_boletim_interno.pdf",
"2018-02-08_O_012_boletim_interno.pdf",
"2018-02-15_O_013_boletim_interno.pdf",
"2018-02-20_O_014_boletim_interno.pdf",
"2018-02-22_O_015_boletim_interno.pdf",
"2018-02-27_O_016_boletim_interno.pdf",
"2018-03-01_O_017_boletim_interno.pdf",
"2018-03-06_O_018_boletim_interno.pdf",
"2018-03-08_O_019_boletim_interno.pdf",
"2018-03-13_O_020_boletim_interno.pdf",
"2018-03-15_O_021_boletim_interno.pdf",
"2018-03-20_O_022_boletim_interno.pdf",
"2018-03-22_O_023_boletim_interno.pdf",
"2018-03-27_O_024_boletim_interno.pdf",
"2018-03-29_O_025_boletim_interno.pdf",
"2018-04-03_O_026_boletim_interno.pdf",
"2018-04-05_O_027_boletim_interno.pdf",
"2018-04-10_O_028_boletim_interno.pdf",
"2018-04-12_O_029_boletim_interno.pdf",
"2018-04-17_O_030_boletim_interno.pdf",
"2018-04-24_O_031_boletim_interno.pdf",
"2018-04-26_O_032_boletim_interno.pdf",
"2018-05-03_O_033_boletim_interno.pdf",
"2018-05-08_O_034_boletim_interno.pdf",
"2018-05-10_O_035_boletim_interno.pdf",
"2018-05-15_O_036_boletim_interno.pdf",
"2018-05-17_O_037_boletim_interno.pdf",
"2018-05-22_O_038_boletim_interno.pdf",
"2018-05-24_O_039_boletim_interno.pdf",
"2018-05-29_O_040_boletim_interno.pdf",
"2018-06-05_O_041_boletim_interno.pdf",
"2018-06-07_O_042_boletim_interno.pdf",
"2018-06-12_O_043_boletim_interno.pdf",
"2018-06-14_O_044_boletim_interno.pdf",
"2018-06-19_O_045_boletim_interno.pdf",
"2018-06-21_O_046_boletim_interno.pdf",
"2018-06-26_O_047_boletim_interno.pdf",
"2018-06-28_O_048_boletim_interno.pdf",
"2018-07-03_O_049_boletim_interno.pdf",
"2018-07-05_O_050_boletim_interno.pdf",
"2018-07-10_O_051_boletim_interno.pdf",
"2018-07-12_O_052_boletim_interno.pdf",
"2018-07-17_O_053_boletim_interno.pdf",
"2018-07-19_O_054_boletim_interno.pdf",
"2018-07-24_O_055_boletim_interno.pdf",
"2018-07-26_O_056_boletim_interno.pdf",
"2018-07-31_O_057_boletim_interno.pdf",
"2018-08-02_O_058_boletim_interno.pdf",
"2018-08-07_O_059_boletim_interno.pdf",
"2018-08-09_O_060_boletim_interno.pdf",
"2018-08-14_O_061_boletim_interno.pdf",
"2018-08-16_O_062_boletim_interno.pdf",
"2018-08-21_O_063_boletim_interno.pdf",
"2018-08-23_O_064_boletim_interno.pdf",
"2018-08-28_O_065_boletim_interno.pdf",
"2018-08-30_O_066_boletim_interno.pdf",
"2018-09-04_O_067_boletim_interno.pdf",
"2018-09-06_O_068_boletim_interno.pdf",
"2018-09-11_O_069_boletim_interno.pdf",
"2018-09-13_O_070_boletim_interno.pdf",
"2018-09-18_O_071_boletim_interno.pdf",
"2018-09-20_O_072_boletim_interno.pdf",
"2018-09-25_O_073_boletim_interno.pdf",
"2018-09-27_O_074_boletim_interno.pdf",
"2018-10-02_O_075_boletim_interno.pdf",
"2018-10-04_O_076_boletim_interno.pdf",
"2018-10-09_O_077_boletim_interno.pdf",
"2018-10-11_O_078_boletim_interno.pdf",
"2018-10-16_O_079_boletim_interno.pdf",
"2018-10-18_O_080_boletim_interno.pdf",
"2018-10-23_O_081_boletim_interno.pdf",
"2018-10-25_O_082_boletim_interno.pdf"]

def abre_pdf(pdfDoc):
	pdfFileObj = open(pdfDoc, 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	return pdfReader

def get_escala(pdfReader):
	texto = pdfReader.getPage(0).extractText() + pdfReader.getPage(1).extractText()
	escala = texto.split("arte INSTRU")[0]
	return escala

def get_bi_number(escala):
	x = escala.split("Para conhecimento")
	nro = x[0].split("BOLETIM INTERNO")
	nro = nro[1].replace(" ","")
	return nro

def get_bi_month(escala):
	x = escala.split("BOLETIM INTERNO")
	x = x[0].split(" de ")
	return x[1]

def liberta_senhor(nome):
	nome = ''.join([i for i in nome if not i.isdigit()])
	nome = ''.join(x for x in nome if not x.islower())
	nome = nome.replace(".", "")
	nome = nome.replace(",", "")
	nome = nome.replace(" - SERVI", "")
	nome = nome.replace("(C", "")
	nome = nome.replace("JEFERSON", "JEFFERSON")
	nome = nome.replace("EMILY", "EMILLY")
	nome = nome.replace("ALVES", "PATRICIA")
	if type(nome) is not str:
		nome = unicodedata.normalize('NFKD', nome).encode('ascii', 'ignore')

	return nome

def get_fiscais(escala):
	fiscais = []
	fiscal = escala.split("FISCAL DE ")
	for linha in fiscal:
		case1 = linha.startswith("DIA")
		if case1:
			linha = linha.split("Sgt ")[1]
			linha = linha.split(" ")[0]
			nome = linha
			nome = liberta_senhor(nome)
			if len(nome) > 0: fiscais.append(nome)

	return fiscais

def get_sv_qgex(escala):
	sgt_sv = escala.split(u"SARGENTO DE SERVIÇO ")
	lista_qgex = []

	for linha in sgt_sv:
		if not linha.startswith("AO QGEX") and linha.find("AO QGEX") != -1:
			linha = linha[linha.find(u"AO QGE"):]
		case1 = linha.startswith("AO QGEX")
		case2 = linha.startswith("AO QGEx")
		if (case1 or case2) and linha.find("Sgt ") != -1:
			if "Sgt" in linha[:100]:
				linha = linha.split("Sgt ")[1]
				linha = linha.split(" ")[0]
				nome = linha
				nome = liberta_senhor(nome)
				if len(nome) > 0: lista_qgex.append(nome)
	return lista_qgex

def get_sv_garagem(escala):
	sgt_sv = []
	sgt_sv = escala.split(u"GARAGENS")
	lista_garagem = []

	for linha in sgt_sv:
		if linha.startswith("..."):
			linha = linha[0:100]
			if "Sgt" in linha:
				linha = linha.split("Sgt ")[1]
				linha = linha.split(" ")[0]
				nome = linha
				nome = liberta_senhor(nome)
				if len(nome) > 0: lista_garagem.append(nome)
	return lista_garagem

def get_substituidos(escala):
	substituidos = {}
	substituidos["GARAGENS"] = []
	substituidos["QGEX"] = []
	substituidos["FISCAL"] = []
	
	escala = escala.split("2. ESCALA DE SERVI")[0]
	escala = escala[:1000]
	if u"substitui\xe7\xe3o" in escala:
		escala = escala.split(u"SGT")
		for linha in escala:
			nome = linha[linha.find(u"substituição")+15:]
			nome = nome[nome.find("Sgt")+4:]
			nome = nome.split(" ")
			nome = nome[0]
			nome = liberta_senhor(nome)
			if "GARAGENS" in linha:
				substituidos["GARAGENS"].append(nome)
			if "QGE" in linha:
				substituidos["QGEX"].append(nome)
			if "FISCAL" in linha:
				substituidos["FISCAL"].append(nome)

	return substituidos

if __name__ == '__main__':

	lista_fiscal = []
	lista_garagem = []
	lista_qgex = []
	lista_subs = []
	bis_substituicoes = []
	meses = {}

	for boletim in PDFS:
		pdfReader = abre_pdf(boletim)
		escala = get_escala(pdfReader)
		bi_number = get_bi_number(escala)
		fiscais = get_fiscais(escala)
		lista_fiscal = lista_fiscal + fiscais

		qgex = get_sv_qgex(escala)
		lista_qgex = lista_qgex + qgex

		garagem = get_sv_garagem(escala)
		lista_garagem = lista_garagem + garagem

		subs = get_substituidos(escala)
		lista_subs.append(subs)

		if subs:
			bis_substituicoes.append(bi_number)

		mes = get_bi_month(escala)

		if mes in meses:
			meses[mes].append(qgex+garagem)
		else:
			meses[mes] = []

		print "\n", bi_number, "\nQGEX: ", qgex, "\nGARAGEM: ", garagem, "\nFISCAL: ", fiscais, "\nSubstituição:", subs

	for mes in meses:
		print "\n-", mes, Counter(list(itertools.chain.from_iterable(meses[mes])))

	for substituidos in lista_subs:
		for nome in substituidos["FISCAL"]:
			if nome in lista_fiscal:
				lista_fiscal.remove(nome)

		for nome in substituidos["QGEX"]:
			if nome in lista_qgex:
				lista_qgex.remove(nome)

		for nome in substituidos["GARAGENS"]:
			if nome in lista_garagem:
				lista_garagem.remove(nome)

	externa = lista_qgex+lista_garagem
	tudao = externa+lista_fiscal

	print "\nFiscal: ", Counter(lista_fiscal)
	print "\nGaragem: ", Counter(lista_garagem)
	print "\nQgex: ", Counter(lista_qgex)
	print "\nEXTERNA: ", Counter(externa)
	print "\nTOTAL: ", Counter(tudao)