#automatizações de verificação textual

import requests
from bs4 import BeautifulSoup
from pprint import pprint
from pathlib import Path
import re
p = re.compile(r'(\d+)')  # a pattern for a number

def search_in_file(path,searchstring):
	with open(path, 'r',encoding='utf-8') as file:
		if 'textit{'+searchstring in file.read():
			print('encontrado: ' + searchstring + ' em: '+path.name)

vgm_url = 'https://www12.senado.leg.br/manualdecomunicacao/verbetes-acessorio/estrangeirismos-grafados-sem-italico-ou-aspas'
html_text = requests.get(vgm_url).text
soup = BeautifulSoup(html_text, 'html.parser')

soup = soup.find_all('p')
nova = []
alternativo = []
for i in soup:
	temp = str(i).replace('<p>','').replace('</p>','').replace(')','')
	
	if temp != '\xa0' and 'Não use itálico' not in temp and '<p' not in temp:
		trim = temp.find(' (')
		if trim > 0: 
			alternativo.append(temp.split(' ('))
			temp = temp[:trim]
		nova.append(temp)

dir_content = sorted(Path('.').iterdir())
#pprint(nova)
for searchstring in nova:
	for path in dir_content: 
		if not path.is_dir():
			if '.tex' in str(path):
				search_in_file(path, searchstring)
