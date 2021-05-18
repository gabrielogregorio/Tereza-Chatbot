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
        arquivo = '{}\\._config.json'.format(pasta)

        with open(arquivo, 'r', encoding='utf-8') as file:
            programa = str(file.read())

        js = json.loads(programa)
        js['referencia'] = pasta

        return js

    def util_gerar_arquivo_configuracao(self, pasta):
        diretorio = '{}\\'.format(pasta)
        dicionario_dados = self.carregar_json(diretorio + 'config.json')
        dicionario_dados = self.__processar_dicionario(dicionario_dados)
        dicionario_dados = self.escrever_json(diretorio + '._config.json', dicionario_dados)

    def __filtros(self, frase:str) -> str:
        frase = str(frase) #.lower()
        return re.sub('\\s{1,}', ' ', frase)

    def __processar_dicionario(self, dicionario_dados: dict) -> dict:
        variaveis = dicionario_dados['variaveis']

        for k,v in variaveis.items():
            if str(type(v)) == "<class 'list'>":
                lista_nova = []
                for item in v:
                    if str(type(item)) == "<class 'str'>":
                        lista_nova.append(item) #.lower())
                    else:
                        lista_nova.append(item)

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

            regex_final, lista_labels = self.__variavel_para_regex(variaveis)
            possivel = re.sub('(\\$[\\w*\\d*]*)', '', texto_possivel)
            dicionario_dados['frases_tratadas'].append(possivel)

            possivel = re.findall('(\\$[\\w*\\d*]*)', texto_possivel)
            if possivel is not None:
                dicionario_dados['frases_variaveis'].append(possivel)
            else:
                dicionario_dados['frases_variaveis'].append([])
        return dicionario_dados

    def __lista_para_regex(self, lista: list) -> str:
        var = ''
        for item in lista:
            var = var + str(item) + '|'
        return var[:-1]

    def __variavel_para_regex(self, variaveis):
        regex = ".*"
        lista = []
        for k_var, v_var in variaveis.items():
            if str(type(v_var)) == "<class 'list'>":
                regex = regex + "(" + self.__lista_para_regex(v_var) + ").*"
                lista.append(k_var)

            elif str(type(v_var)) == "<class 'str'>":
                regex = regex + "(" + v_var + ").*"
                lista.append(k_var)

            else:
                print("__ERRO__")
        return [regex, lista]
