from random import choice
from src.Extensao import Extensao
import requests
from bs4 import BeautifulSoup
import re
import unidecode


class main(Extensao):
    def __init__(self, dict_extensao):
        Extensao.__init__(self, dict_extensao)
        self.dict_emails = {}

        try:
            self.dict_emails = self.carrega_emails()
        except Exception as e:
            print(e)

    def entrada(self, dados:dict, prox_ponto_referencia:str, chat_id) -> dict:
        self.carregar_variaveis(dados, chat_id)
    
        if prox_ponto_referencia == "principal": # Principal
            # Se tem listinha de e-mail disponível
            # Se o nome do professor foi obtido
            texto = ""
            if self.dict_emails != {} and dados['variaveis'].get('nome_professor'):
                nome_professor = dados['variaveis']['nome_professor'].lower().strip()
                for nome, email in self.dict_emails.items():

                    unic_nome_professor = unidecode.unidecode(nome_professor)
                    unic_nome = unidecode.unidecode(nome)
                    
                    # Verifica se o nome contém o nome sugerido
                    if unic_nome_professor in unic_nome.lower().strip():
                        texto = texto + '\n' + '{}\n{}\n'.format(nome, email)
            
            if texto:
                resposta = texto
            else:
                resposta = choice(dados['config']["finalizar_interacao"]) # Pergunta

            return self.responder(
                resposta=resposta,
                chat_id=chat_id,
                prox_ponto_referencia="",
                liberar=True)

    def carrega_emails(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        urls = [
            'https://www.fatecaracatuba.edu.br/curso_bio.php#docentes',
            'https://www.fatecaracatuba.edu.br/curso_ads.php#docentes'
        ]
        dict_emails = {}
        for url in urls:
            req = requests.get(url=url, headers=headers, timeout=15)
            html = req.text

            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find(id='docentes')
            rows = table.find_all('tr')

            for row in rows:
                if row:
                    regex = '<td>(.*)?\\<\\/td>\n\\s*<td>([a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+)\\<\\/td>'

                    emails = re.search(regex, str(row))
                    if emails:
                        nome_professor, email = emails.group(1), emails.group(2)
                        dict_emails[nome_professor] = email

        return dict_emails
