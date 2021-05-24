import json
import re


class Util():
    def __init__(self):
        pass

    def carregar_json(self, diretorio:str) -> dict:
        with open(diretorio, 'r', encoding='utf-8') as file:
            return json.loads(file.read())

    def escrever_json(self, diretorio:str, dicionario_dados:dict) -> dict:
        with open(diretorio, 'w', encoding='utf-8') as file:
            file.write(str(json.dumps(dicionario_dados, indent=4)))

    def carregar_configuracao(self, pasta: str) -> dict:
        """ Carrega um arquivo de configuração """
        arquivo = '{}\\._config.json'.format(pasta)

        with open(arquivo, 'r', encoding='utf-8') as file:
            js = json.loads(file.read())

        js['referencia'] = pasta
        return js

    def util_gerar_arquivo_configuracao(self, pasta):
        """ Gera um arquivo de configuração especial para a Tereza """
        diretorio = '{}\\'.format(pasta)
        dicionario_dados = self.carregar_json(diretorio + 'config.json')
        dicionario_dados = self.__processar_dicionario(dicionario_dados)
        dicionario_dados = self.escrever_json(diretorio + '._config.json', dicionario_dados)

    def __filtros(self, frase:str) -> str:
        frase = str(frase)
        return re.sub('\\s{1,}', ' ', frase)

    def __processar_dicionario(self, dicionario_dados: dict) -> dict:
        """ Cria uma chave especial com os textos formatados para expressões
        regulares
        """
        variaveis = dicionario_dados['variaveis']

        # Percorrer as chaves e os itens
        for k, v in variaveis.items():
            if isinstance(v, list):
                lista_nova = []
                for item in v:
                    if isinstance(v, str): lista_nova.append(item)
                    else: lista_nova.append(item)

                variaveis[k] = lista_nova

        frases_entrada = dicionario_dados['principal']

        for texto_possivel in frases_entrada:
            if 'frases_tratadas' not in dicionario_dados.keys():
                dicionario_dados['frases_tratadas'] = []

            if 'frases_variaveis' not in dicionario_dados.keys():
                dicionario_dados['frases_variaveis'] = []

            texto_possivel = self.__filtros(texto_possivel)

            if '$' not in texto_possivel:
                dicionario_dados['frases_tratadas'].append(texto_possivel)
                dicionario_dados['frases_variaveis'].append([])
                continue

            possivel = re.sub('(\\$[\\w*\\d*]*)', '', texto_possivel)
            dicionario_dados['frases_tratadas'].append(possivel)

            possivel = re.findall('(\\$[\\w*\\d*]*)', texto_possivel)
            if possivel is not None:
                dicionario_dados['frases_variaveis'].append(possivel)
            else:
                dicionario_dados['frases_variaveis'].append([])
 
        return dicionario_dados
