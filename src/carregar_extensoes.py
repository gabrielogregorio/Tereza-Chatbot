#!/usr/bin/python

from importlib import import_module
from pkgutil import iter_modules
from inspect import isclass
from pathlib import Path
from src.util import Util
import re
import os
import json

util = Util()

'''Caminhar pelas extensões e importa-las'''
dic_recursos = []
for root, dirs, files in os.walk("extensoes"):
    
    path = root.split(os.sep)
    # Verificar se está dentro de uma possível extensão
    if len(path) == 5:
        # Verificar se o diretório, o arquivo de config e a classe extensão existe
        directory = path[0] + '\\\\' + path[1] + '\\\\' + path[2] + '\\\\' + path[3] + '\\\\' +  path[4]
        file_py = directory + '\\\\extensao.py'
        file_config = directory + '\\\\config.json'

        # Se o arquivo Python e o Config existirem.
        if os.path.exists(file_py):
            if os.path.exists(file_config):

                # Obter apenas o nome do módulo sem o .py
                # transformar o caminho em caminho importável
                modulo = file_py[0:-3].replace(r'\\', '.')

                # Gerar o arquivo de configuração "._config.json"
                util.util_gerar_arquivo_configuracao(directory)
                
                # Importar o módulo
                module = import_module(modulo)

                # Instanciar a classe
                func = module.main(util.carregar_configuracao(directory))
                
                # Adicionar no dicionário de recursos
                dic_recursos.append({
                    func: util.carregar_configuracao(directory)
                })

                # Adicionar a classe as variáveis
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)

                    if isclass(attribute):            
                        globals()[attribute_name] = attribute


class CarregarExtensoes():
    def __init__(self):
        self.dic_recursos = {}
        self.dic_recursos = dic_recursos
        self.variaveis_gerais = {'chaves_acesso': {}}

        # Percorrer pela função e pelo arquivo de configuração:
        for item in self.dic_recursos:

            # função, arquivo de configuração
            for k, v in item.items():

                # Percorrer pelos textos de entrada
                for texto_entrada in v['principal']:

                    # Se começa com barra é um comando instanciável
                    if texto_entrada.startswith('/'):

                        # Ignore o comando de primeira interação
                        if texto_entrada == '/primeiraInteracao':
                            continue

                        # percorrer pelos caminhos
                        ref = re.search('.*\\\\(.{1,})\\\\', v['referencia'])
                        ref = ref.group(1)
                        ref = ref.replace('/', '')
                        ref = ref.replace('\\', '')
                        ref = ref.replace('materia_', '')
                        ref = ref.replace('_', ' ')
 
                        # Indexar a chave de acesso
                        try:
                            self.variaveis_gerais['chaves_acesso'][ref.capitalize()].append(texto_entrada)
                        except:
                            self.variaveis_gerais['chaves_acesso'][ref.capitalize()] = [texto_entrada]