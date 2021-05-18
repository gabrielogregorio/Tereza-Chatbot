from bs4 import BeautifulSoup
import unidecode
import requests
import json
import re

menus_site = []
dict_textos = {}
dict_menus = {}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class EncontrarRespostaAlternativa():
    def __init__(self):
        req = requests.get('https://www.fatecaracatuba.edu.br/', headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        table = soup.find(id='fatec-menu')
        all_itens = table.find_all('li')

        # Obter o menu completo
        for item in all_itens:
            list_a = item.find_all('a')
            for a in list_a:
                texto, link = a.text, a['href']
                if link not in ['#', '']:
                    if link.startswith('http'):
                        link2 = link
                    else:
                        link2 = 'https://www.fatecaracatuba.edu.br/' + link

                    dict_menus[texto.strip()] = link2

        # Obter os textos
        for texto, link in dict_menus.items():
            if 'docs.google' in link or link.endswith('.pdf') or link.endswith('.docx'):
                continue
            else:
                req = requests.get(link, headers=headers)
                html = str(req.text)
                html2 = html.replace('\n', '')



                regex = '<div class="collapse navbar-collapse" id="fatec-menu"\\>.*<\\/div>'
                html2 = re.sub(regex, '', html2)
                

                soup = BeautifulSoup(html, 'html.parser')
                soup2 = BeautifulSoup(html2, 'html.parser')

                texto_novo = ""
                lista = soup2.get_text().split('\n')
                for item in lista:
                    valor = item.strip()
                    if valor:
                        texto_novo = texto_novo + valor + '\n'
                
                dict_textos[str(link)] = [str(texto_novo), html]

        js = json.dumps(dict_textos, indent=4)
        js_menus = json.dumps(dict_menus, indent=4)

        # Salvar um backup dos arquivos
        with open('src/arquivos/textos.json', 'w', encoding='utf-8') as f:
            f.write(str(js))

        with open('src/arquivos/menus.json', 'w', encoding='utf-8') as f:
            f.write(str(js_menus))

        # Pega-los novamente. Talvez seha desnecessário
        with open('src/arquivos/textos.json', 'r', encoding='utf-8') as f:
            self.js_textos = json.loads(f.read())

        with open('src/arquivos/menus.json', 'r', encoding='utf-8') as f:
            self.js_menu = json.loads(f.read())


    def __filtrar_texto(self, texto):
        texto = texto.strip()
        texto = unidecode.unidecode(texto)
        texto = texto.lower()

        texto = ' ' + texto + ' '
        for i in ['.', ',', '\n', ';', ':']:
            texto = texto.replace(i, ' ')

        return ' ' + texto + ' '


    def __dict_menu_data(self, entrada:str):
        dict_titulos = {}
        lista = []

        entrada = self.__filtrar_texto(entrada).split(' ')
        entrada2 = []
        for e in entrada:
            if e != '':
                entrada2.append(e)

        for titulo_link, link in self.js_menu.items():
            titulo_link2 = self.__filtrar_texto(titulo_link).split(' ')
            counts = 0
            for doc in entrada2:
                if doc != '':
                    ct = titulo_link2.count(doc)
                    counts = counts + ct
            
            if counts != 0:
                lista.append([counts, titulo_link, link])
        
        return lista


    def __dicionario_para_texto(self, entrada:str):
        dict_titulos = {}
        lista = []

        entrada = self.__filtrar_texto(entrada).split(' ')
        entrada2 = []
        for e in entrada:
            if e != '':
                entrada2.append(e)

        for link, titulo_html in self.js_textos.items():
            titulo_link = titulo_html[0].replace('\n', ' ')
            titulo_link2 = self.__filtrar_texto(titulo_link).split(' ')
            counts = 0
            for doc in entrada2:
                if doc != '':
                    ct = titulo_link2.count(doc)
                    counts = counts + ct
            
            if counts != 0:
                lista.append([counts, titulo_link, titulo_html[1], link])
        
        return lista

    def __obter_titulo(self, html:str):
        reh1 = '<h1.*?>(.*)?<\\/h1>'
        reh2 = '<h2.*?>(.*)?<\\/h2>'

        h1 = re.search(reh1, html)
        if not h1:
            h2 = re.search(reh2, html)
            if h2:
                return h2.group(1)
        else:
            return h1.group(1)
        
        return ""

    def __obter_referencias(self, entrada:str):
        entrada = entrada.strip()
        entrada = ' ' + entrada + ' '
        for i in ['posso', 'qual', 'fatec', 'que', 'qual', 'é', 'o', 'atua', 'nos', 'de', 'me', 'no', 'da', '.', ',', '\n']:
            entrada = entrada.replace(' {} '.format(i), ' ')
        entrada = entrada.strip()

        lista2 = self.__dict_menu_data(entrada)
        lista_dados = []

        for item in lista2:
            counts, titulo, link = item
            lista_dados.append(['menu', counts, titulo, link])
            
        lista = self.__dicionario_para_texto(entrada)
        for item in lista:
            counts, texto, html, link = item
            titulo = self.__obter_titulo(html)
            lista_dados.append(['html', counts, titulo, link])

        lista = []
        melhor = {'maior':0}
        for tipo, count, titulo, link in lista_dados:
            if count >= melhor['maior']:
                melhor = {
                    "tipo": tipo,
                    'maior': count,
                    "titulo": titulo,
                    "link": link
                }
                lista.append(melhor)

        return lista

    def localizar_uma_referencia(self, entrada:str) -> list:
        lista = self.__obter_referencias(entrada)
        return lista

