import re
from src.pyanalise import Compare
from src.nlu import SepararFrases


class Processar():
    def __init__(self, ext):
        self.analise = SepararFrases()
        self.compare = Compare()

        self.dic_config_extensoes = ext.dic_recursos

    def filtros(self, frase:str) -> str:
        frase = str(frase) # .lower()
        return re.sub('\\s{1,}', ' ', frase)

    def obter_resposta(self, entrada_original:str, base_instancia, prox_ponto_referencia) -> dict:
        entrada_original = self.filtros(entrada_original)
        maior = {"maior":0}

        for instrucao in self.dic_config_extensoes:
            # Carregamento da instância e do arquivo config_tess.json
            for instance, instrucao in instrucao.items():

                if base_instancia is not None:
                    # Se tem uma instância disponível, tem que analisar somente ela
                    if str(instance) != str(base_instancia):
                        continue

                # Navegar pelas frases de entradas tratadas
                for n in range(len(instrucao[prox_ponto_referencia])):
                    entrada = entrada_original

                    texto_a_testar = instrucao[prox_ponto_referencia][n]
                    # Obter todas as variáveis
                    lista = re.findall( "(\$[\w]{1,})", texto_a_testar)
                    variaveis = {}

                    for item in lista:
                        chave = item[1:]
                        valor = instrucao['variaveis'][chave]
                        variaveis[chave] = valor

                    if lista != []:
                        regex_final, lista_labels = self.analise.converter_variaveis_texto(variaveis)
                        entrada2 = self.analise.retornar_textos_das_variaveis(entrada, regex_final)
                        if entrada2[0] == False:
                            # Não havia nenhum registro
                            # mas o arquivo de config será salvo
                            # para comparar as melhores possibilidades
                            if maior == {"maior":0}:
                                maior['config'] = instrucao
                            continue

                        dic_vars = {}
                        for n_c in range(len(lista_labels)):
                            dic_vars[lista_labels[n_c]] = entrada2[2][n_c]

                        entrada = entrada2[1]

                    # Verificar as frases tratadas e salvar a mais provável
                    base = instrucao[prox_ponto_referencia][n]
                    base = re.sub('(\$[\w]{1,})', '', base)
                    num = self.compare.comparar_palavras(base, entrada)
                    # Salvar dados da mais provável
                    # Se não houver texto restante, o regex pegou tudo
                    # E portanto temos um 100%

                    if maior['maior'] <= num: 
                        
                        maior['maior'] = num # Porcentagem
                        maior['instance'] = instance # instância
                        maior['prox_ponto_referencia'] = prox_ponto_referencia # Salvar o ponto analisado
                        maior['config'] = instrucao # instruções do arquivo ._config.json
                        maior['variaveis'] = {}
                        if lista != []:
                            maior['variaveis'] = dic_vars
                            if entrada2[1] == '':
                                maior['maior'] = 100

        return maior
