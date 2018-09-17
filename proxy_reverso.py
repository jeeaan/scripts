import commands
import pprint
import time
import simplejson as json

def conexao(ip, porta):
    conexao = commands.getoutput("timeout 10 nc -zv "+ip+" "+porta+"")

    if conexao.endswith("succeeded!"):
        return True
    else:
        return False

def dns_por_ip(lista_dns):

	dict_ips = {}

	for dns in lista_dns:
		output_lookup = commands.getoutput("nslookup "+dns+"")
		ip = output_lookup.split( )[-1]

		if dict_ips.get(ip) is None:
			dict_ips[ip] = []
			dict_ips[ip].append(dns)
		else:
			dict_ips[ip].append(dns)

	return dict_ips

def faz_login(usuario, senha, dns):

	response = commands.getoutput("curl -m 40 -k -X POST https://"+dns+":8090/api/login/?username="+usuario+"\&password="+senha+"\&phone_id=666 -ssl3")

	if "Couldn\'t resolve host" in response:
		return False
	elif "502 Bad Gateway" in response:
		return False
	elif "The requested URL could not be retrieved" in response:
		return False
	elif "timed out" in response:
		return False

	response_to_string = response[response.find("\n{\"")+1:]
	try:
		response = json.loads(response_to_string)
	except ValueError, e:
		return False

	if "access_token" in response:
		return True
	elif "error" in response:
		return False

def funfa_ou_nao_funfa(lista_dns, usuario, senha):
	print "\nfunfa_ou_nao_funfa:"

	funfa = {}
	nao_funfa = {}

	print "\nSeparando DNS por IP:"
	dnss = dns_por_ip(lista_dns)
	#dnss = {'200.198.213.118': ['bsb2.host2.com.br'], '177.15.66.3': ['ct1.host2.com.br'], '177.15.64.138': ['bh2.host2.com.br'], '177.15.72.153': ['bsb3.host2.com.br']}
	print dnss

	print "\nTeste Proxy Reverso:\n"
	for ip in dnss:
		print "->", ip
		if conexao(ip, "8090"):
			for dns in dnss[ip]:
				start = time.time()
				print dns,
				if faz_login(usuario, senha, dns):
					print "-> logou!",
					end = time.time()
					total = end - start
					print ("%.2f" % total), "s"
					if funfa.get(ip) is None:
						funfa[ip] = []
						funfa[ip].append(dns)
					else:
						funfa[ip].append(dns)
				else:
					print "\n",
					if nao_funfa.get(ip) is None:
						nao_funfa[ip] = []
						nao_funfa[ip].append(dns)
					else:
						nao_funfa[ip].append(dns)
		else:
			for dns in dnss[ip]:
				if nao_funfa.get(ip) is None:
					nao_funfa[ip] = []
					nao_funfa[ip].append(dns)
				else:
					nao_funfa[ip].append(dns)

	print "\nFuncionando:\n"
	pprint.pprint(funfa)

	print "\nNao funciona:\n"
	pprint.pprint(nao_funfa)

if __name__ == '__main__':
#	proxy_reverso = ["host.com.br", "h2.host.com.br", "bh1.host2.com.br","bh2.host2.com.br","bh3.host2.com.br","bh4.host2.com.br","bsb1.host2.com.br","bsb2.host2.com.br","bsb3.host2.com.br","bsb4.host2.com.br","cb1.host2.com.br","cb2.host2.com.br","cb3.host2.com.br","cb4.host2.com.br","ct1.host2.com.br","ct2.host2.com.br","ct3.host2.com.br","ct4.host2.com.br","fort1.host2.com.br","fort2.host2.com.br","fort3.host2.com.br","fort4.host2.com.br","mn1.host2.com.br","mn2.host2.com.br","mn3.host2.com.br","mn4.host2.com.br","nt1.host2.com.br","nt2.host2.com.br","nt3.host2.com.br","nt4.host2.com.br","pa2.host2.com.br","pa3.host2.com.br","pa4.host2.com.br","rec1.host2.com.br","rec2.host2.com.br","rec3.host2.com.br","rec4.host2.com.br","rj1.host2.com.br","rj2.host2.com.br","rj3.host2.com.br","rj4.host2.com.br","salv1.host2.com.br","salv2.host2.com.br","salv3.host2.com.br","salv4.host2.com.br","sp1.host2.com.br","sp2.host2.com.br","sp3.host2.com.br","sp4.host2.com.br"]
	proxy_reverso = ["host.com.br", "2cta.host.com.br"]
	start = time.time()
	USUARIO = "root"
	SENHA = ""

	funfa_ou_nao_funfa(proxy_reverso, USUARIO, SENHA)
	end = time.time()
	total = end - start
	print "Tempo total: ", ("%.2f" % total), "s\n"