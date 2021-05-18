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
            item = item
            var = var + str(item) + '|'
        return var[:-1]
    
    def filtros(self, frase:str) -> str:
        frase = str(frase) # .lower()
        return re.sub('\\s{1,}', ' ', frase)

    def converter_variaveis_texto(self, variaveis:dict) -> list:
        """in: {"nome":".*", "escola":["Fatec", "Etec", "Outra"]})
           out: ['.*(.*).*(Fatec|Etec|Outra).*', ['nome', 'escola']]
        """
        regex_final = ".*?"
        lista = []
        for k_var, v_var in variaveis.items():
    
            if str(type(v_var)) == "<class 'list'>":
                regex_final = regex_final + "(" + SepararFrases.lista_para_regex(self, v_var) + ").*"
                lista.append(k_var)
    
            elif str(type(v_var)) == "<class 'str'>":
                regex_final = regex_final + "(" + v_var + ").*"
                lista.append(k_var)
    
            else:
                print("__ERRO__")
        return [regex_final, lista]

    def retornar_textos_das_variaveis(self, texto:str, regex_final:str) -> list:
        #saida: [True, 'Tenho ', ['18']]
        res = re.search(regex_final, texto)
        string = ''
        ponto = 0
        lista = []
    
        if res is not None:
            qtd = len(list(res.groups()))
            for n in range(qtd):
                xi, xf = res.span(n + 1)
                string = string + texto[ponto:xi]
                lista.append(texto[xi:xf])
    
                ponto = xf

            string = string + texto[ponto:]
    
            return [True, string, lista]
        return [False, '', lista]
    