#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

__author__       = 'Gabriel Gregório da Silva'
__email__        = 'gabriel.gregorio.1@outlook.com'
__description__  = 'Processamento de respostas para chatbots'
__status__       = 'Development'
__date__         = '18/04/2019'
__version__      = '1.4'


class SepararFrases():
    def __init__(self):
        pass

    def lista_para_regex(self, lista:list) -> str:
        var = ''
        for item in lista:
            var += str(item) + '|'
        return var[:-1]
    
    def filtros(self, frase:str) -> str:
        """Remove multiplas strings"""
        return re.sub('\\s{1,}', ' ', str(frase))

    def converter_variaveis_texto(self, variaveis:dict) -> list:
        """ Converte as variáveis textuais ou lista em expressões regulares"""
        regex_final = ".*?"
        lista = []
        for k, v in variaveis.items():

            # Variável é uma lista
            if isinstance(v, list):
                regex_final += "({}).*".format(self.lista_para_regex(lista=v))
                lista.append(k)
    
            # Variável é uma string
            elif isinstance(v, str):
                regex_final += "({}).*".format(v)
                lista.append(k)
    
            else:
                print("Erro, tipo indefinido!")

        return [regex_final, lista]

    def retornar_textos_das_variaveis(self, texto:str, regex:str) -> list:
        """ Extrai informações de um texto baseado na expressão regular"""
        re_resposta = re.search(regex, texto)

        texto_sem_dados = ''
        ponto = 0
        lista_dados = []
    
        # Se extraiu dados
        if re_resposta is not None:

            # Contar a quantidade de dados extraidos
            quantidade = len(list(re_resposta.groups()))
            for n in range(quantidade):
                # Inicio e fim da posição do dado
                xi, xf = re_resposta.span(n + 1)

                # Exclusão do dado no texto
                texto_sem_dados += texto[ponto:xi]

                # Salvamento do dado
                lista_dados.append(texto[xi:xf])

                # Normalizção
                ponto = xf

            # Salvamento final do texto extraido
            texto_sem_dados += texto[ponto:]
    
            return [True, texto_sem_dados, lista_dados]
        return [False, '', lista_dados]
    