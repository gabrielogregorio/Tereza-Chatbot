from random import choice
from src.util import Util
import re
import os


class Extensao:
    def __init__(self, dict_extensao):
        self.util = Util()
        self.dic_var = {}
        self.dict_extensao = dict_extensao
        self.dados = {}
        
        # Carrega os regex ou lista com os padrões
        # para serem usados com o ., exemplo: $.nome
        self.tipo_variaveis = {}
        for k, v in self.dict_extensao['variaveis'].items():
            self.tipo_variaveis[ '.' + k] = v
    
    def carregar_variaveis(self, dados, chat_id):
        self.dados[chat_id] = dados
        for k, v in dados['variaveis'].items():
            print('UPDATE VAR')
            try:
                self.dic_var[chat_id][k] = v
            except:
                self.dic_var[chat_id] = {}
                self.dic_var[chat_id][k] = v

    def formatar_resposta(self, resposta, chat_id):
        resposta = self.__atualizar_diretorios(resposta)

        config_chaves = self.util.carregar_json('config.json')['chaves_acesso']
        textoX = ""
        for k, v in config_chaves.items():
            k = k.replace('_', ' ')
            textoX = textoX + k + '\n'

            for item in v:
                textoX = textoX + '- ' + item + '\n'
            
            textoX = textoX + '\n'
        
        resposta = resposta.replace('$_g_chaves_acesso', textoX)

        if self.dic_var.get(chat_id):
            for k, v in self.dic_var[chat_id].items():
                resposta = resposta.replace('${}'.format(k), str(v))

        for k, v in self.tipo_variaveis.items():
            base = '${}'.format(k)

            if isinstance(v, list):
                texto = ""
                for item in v:
                    texto = texto + '\n' + item

                resposta = resposta.replace(base, texto)
            else:
                resposta = resposta.replace(base, str(v))
        resposta = resposta.replace('\\n', '\n')
        return resposta

    def __atualizar_diretorios(self, resposta):
        qualquer_id = list(self.dados.keys())[0]
        dir_ref = self.dados[qualquer_id]['config']['referencia']
        regex = '\\!\\[([\\w]{2,})\\]\\((.*)\\s{1,}"(.*)\\"\\)'
        lista = resposta.split('\\n')
        texto = ''
        for linha in lista:
            linha = linha.strip()
            resp = re.search(regex, linha)
            if resp:
                tipo = resp.group(1) 
                dir = resp.group(2)# diretório
                desc = resp.group(3)# nome

                texto = texto + '![{}]({} "{}")'.format(tipo, os.path.join(dir_ref, dir), desc) + '\n'
            else:
                texto = texto + linha + '\n'
            
        return texto

    def responder(self, resposta, prox_ponto_referencia, chat_id, liberar=False):
            return {'resposta': self.formatar_resposta(resposta, chat_id),
        		'prox_ponto_referencia': prox_ponto_referencia,
                'finished': liberar}
