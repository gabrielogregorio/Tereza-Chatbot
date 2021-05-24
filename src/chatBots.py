from src.Processar import Processar
from src.carregar_extensoes import CarregarExtensoes
from datetime import datetime
from datetime import timedelta
from random import choice
from src.Seguranca import Seguranca
from src.util import Util
from src.encontrar_resposta_alternativa import EncontrarRespostaAlternativa
import uuid

class ChatBot(): 
    def __init__(self):
        self.util = Util()
        ext = CarregarExtensoes()
        # Salvar as variáveis globais no arquivo de configurações
        self.salvar_variaveis_globais(ext.variaveis_gerais['chaves_acesso'])
 
        self.process = Processar(ext)
        self.data = {}
        self.sec = Seguranca()
        self.encontrar_alternativa = EncontrarRespostaAlternativa()
        self.config = self.util.carregar_json('config.json')
        print('extensões carregadas')

    def salvar_variaveis_globais(self, chave_acesso:str):
        self.config = self.util.carregar_json('config.json')
        self.config['chaves_acesso'] = chave_acesso
        self.util.escrever_json('config.json', self.config)

    def __atualizar_tempo_limite(self, timeout:str, chat_id:str):
        time_timeout = datetime.strptime(timeout, '%H:%M:%S')
        self.data[chat_id]['timeout'] = datetime.now() + timedelta(
                minutes=time_timeout.minute,
                hours=time_timeout.hour,
                seconds=time_timeout.second)

    def __limpar_variaveis(self, chat_id:str):
            self.data[chat_id] = {}
            self.data[chat_id]['finished'] = True
            self.data[chat_id]['instance'] = None
            self.data[chat_id]['variaveis'] = {}
            self.data[chat_id]['id_interacao'] = str(uuid.uuid4())

    def registrar_tentativa(self, chat_id:str, maior:dict):
        # Não existe nenuma tentativa registrada
        if not self.data[chat_id].get('tentativas'):
            # Registra o número de tentativas
            self.data[chat_id]['tentativas'] = maior['config']['configuracoes']['tentativas']
            self.data[chat_id]['mensagens_tentativas'] = maior['config']['configuracoes']['mensagens_tentativas']

        # Diminui uma tentativa
        self.data[chat_id]['tentativas'] = self.data[chat_id]['tentativas'] - 1
    
    def __formatar_resposta_padrao(self, resposta:str):
        config_chaves = self.config['chaves_acesso']
        textoX = ""
        for k, v in config_chaves.items():
            k = k.replace('_', ' ')
            textoX = textoX + k + '\n'

            for item in v:
                textoX = textoX + '- ' + item + '\n'
            
            textoX = textoX + '\n'
        
        resposta = resposta.replace('$_g_chaves_acesso', textoX)
        return resposta

    def __resposta_alternativa(self, entrada:str, chat_id:str):
        lista = self.encontrar_alternativa.localizar_uma_referencia(entrada)

        if lista == []:
            return self.__formatar_resposta_padrao(
                "Eu não entendi o que você escreveu, você poderia perguntar de outra forma ou clicar em uma das opções abaixo caso seja a que você esteja procurando?\n\n$_g_chaves_acesso"
            )

        else:
            texto = "Veja se algum destes resultados servem:\n\n"
            for item in lista:
                tipo = item['tipo']
                maior = item['maior']
                titulo = item['titulo']
                link = item['link']
                texto = texto + titulo + '\n' + link + '\n\n'
            self.__limpar_variaveis(chat_id)
            return texto

    def interacao_chat(self, chat_id:str, entrada:str, usuario_nao_registrado:str=''):
        usuario_nao_registrado = ''
        permissao = self.sec.verificar_permissao(chat_id)
        if permissao == ['cadastrar', True]:
            #print('Usuário não cadastrado!')
            usuario_nao_registrado = 'cadastrar'

        # Impede a primeira interação ser registrada de propósito pelo usuário
        if entrada == '/primeiraInteracao':
            entrada = 'primeiraInteracao'
            #print('Texto era a primeira interação')

        # Se é para registrar um usuário
        # configure a entrada para acionar a extensão de registro
        if usuario_nao_registrado == 'cadastrar':
            entrada = "/primeiraInteracao"
            #print('Cadastrar Usuário')

        # Usuário não esta cadastrado no sistema
        if chat_id not in self.data.keys():
            #print('Usuário não esta cadastrado no sistema')
            self.__limpar_variaveis(chat_id)

        nenhum_instancia_definida = True
 
        # Nenhuma instância definida
        if self.data[chat_id]['finished']:
            #print('Nenhuma instância definida')
            maior = self.process.obter_resposta(entrada, base_instancia=None, prox_ponto_referencia='principal')

            if not maior.get('config'): 
                #print('Nenhuma respsota alternativa\n')
                id_interacao = self.data[chat_id]['id_interacao']
                self.__limpar_variaveis(chat_id)
                return {
                    "RESPOSTA": self.__resposta_alternativa(entrada, chat_id),                  
                    "EXTENSAO": "",
                    "ID_INTERACAO": id_interacao,
                    "STATUS": "RESPOSTA_ALTERNATIVA"
                }

        else:
            nenhum_instancia_definida = False
            #print('Continuação de uma interação')
            # Ja existe uma instância definida,
            # Ela não finalizou então continuar execução

            # Se deu timeout
            if datetime.now() > self.data[chat_id]['timeout']:
                #print('Usuário Ficou muito tempo sem interagir\n')
                # Resetar o usuário e retornar resposta
                id_interacao = self.data[chat_id]['id_interacao']
                self.__limpar_variaveis(chat_id)
                # Remover permissao Temporaria se ela existir
                self.sec.remover_registro_temporario(chat_id)

                return {
                    "RESPOSTA": "Você ficou muito tempo sem interagir, por isso eu esqueci o que a gente estava falando. O que você precisa?",
                    "EXTENSAO": "",
                    "ID_INTERACAO": id_interacao,
                    "STATUS": "DESCONECTADO_POR_TEMPO"
                }
                


            # Obter Próxima resposta
            #print('Será buscada uma nova resposta')
            maior = self.process.obter_resposta(entrada, base_instancia=self.data[chat_id]['instance'], prox_ponto_referencia=self.data[chat_id]['prox_ponto_referencia'])

        # Se o arquivo de configurações não veio
        # Não houve nenhuma resposta satisfatória
        if not maior.get('config'):
            #print('Não foi encontrado nenhuma resposta válida')
            # Somar uma tentativa
            self.registrar_tentativa(chat_id, maior)

            # Chegou ao limite de tentativas, finalizar
            if self.data[chat_id]['tentativas'] == 0:
                #print('esgotou as tentativas\n')
                mensagens_tentativas = choice(self.data[chat_id]['mensagens_tentativas'])

                # Remover permissao Temporaria se ela existir
                self.sec.remover_registro_temporario(chat_id)
 


                id_interacao = self.data[chat_id]['id_interacao']
                self.__limpar_variaveis(chat_id)

                return {
                    "RESPOSTA": mensagens_tentativas,
                    "EXTENSAO": "",
                    "ID_INTERACAO": id_interacao,
                    "STATUS": "DESCONECTADO_POR_TENTATIVAS"
                }


            #print('Reposta em caso da resposta não fazer sentido\n')
            id_interacao = self.data[chat_id]['id_interacao']
            return {
                "RESPOSTA": 'Olá, você precisa de escrever de outra forma',
                "EXTENSAO": "",
                "ID_INTERACAO": id_interacao,
                "STATUS": "ESPERANDO_RESPOSTA_CERTA"
            }

        #print('Existiu uma resposta válida')
        # Marcar quando ocorrerá o timeout da interação com o usuário
        timeout = maior['config']['configuracoes']['timeout']
        self.__atualizar_tempo_limite(timeout, chat_id)


        # Resposta < x% de certeza 
        if maior['maior'] < maior['config']['configuracoes']['precisao']:
            #print('Precisão da resposta válida foi insuficiente', maior['maior'])

            # Registrar uma tentativa, porém com precisão
            # insuficiente para a extensão
            self.registrar_tentativa(chat_id, maior)

            # Chegou ao limite de tentativas, finalizar
            if self.data[chat_id]['tentativas'] == 0:
                #print('esgotou as tentativas 2\n')
                mensagens_tentativas = choice(self.data[chat_id]['mensagens_tentativas'])

                # Remover permissao Temporaria se ela existir
                self.sec.remover_registro_temporario(chat_id)
 
                id_interacao = self.data[chat_id]['id_interacao']
                self.__limpar_variaveis(chat_id)
                return {
                    "RESPOSTA": mensagens_tentativas,
                    "EXTENSAO": maior['config']['referencia'],
                    "ID_INTERACAO": id_interacao,
                    "STATUS": "ESPERANDO_RESPOSTA_CERTA"
                } 

            # Resposta Geral ao usuário
            #print('Reposta em caso da resposta não fazer sentido 2')
            if nenhum_instancia_definida:
                #print('Nenhuma respsota alternativa 3\n')
                id_interacao = self.data[chat_id]['id_interacao']
                self.__limpar_variaveis(chat_id)
                
                return {
                    "RESPOSTA": self.__resposta_alternativa(entrada, chat_id),
                    "EXTENSAO": "",
                    "ID_INTERACAO": id_interacao,
                    "STATUS": "RESPOSTA_ALTERNATIVA"
                }

            id_interacao = self.data[chat_id]['id_interacao']
            return {
                "RESPOSTA": 'Eu não entendi, você poderia escrever de outra forma?',
                "EXTENSAO": maior['config']['referencia'],
                "ID_INTERACAO": id_interacao,
                "STATUS": "ESPERANDO_RESPOSTA_CERTA"
            }

        else:
            #print('Resposta faz sentido e está acima da %')
            # Acessa a instância e informa a entrada com os dados tratados
            resposta = maior['instance'].entrada(maior, maior['prox_ponto_referencia'], chat_id)
            
            # Deletar a chave de tentativas (Se precisar)
            try:
                del self.data[chat_id]['tentativas']
                del self.data[chat_id]['mensagens_tentativas']
            except KeyError:
                pass

            #print("Atualização dos dados")
            self.data[chat_id]['instance'] = maior['instance']
            self.data[chat_id]['finished'] = resposta['finished']
            self.data[chat_id]['prox_ponto_referencia'] = resposta['prox_ponto_referencia']

            # Atualizar valor das variáveis
            for var, valor in maior['variaveis'].items():
                #print("Atualizar o valor das variávieis disponíveis")
                self.data[chat_id]['variaveis'][var] = valor

            # Ultima referencia é vazia, programa finalizou!
            if self.data[chat_id]['prox_ponto_referencia'] == "":
                #print("Deu instrução para finalizar a interação com essa extensão")
                self.data[chat_id]['finished'] = True

            if self.data[chat_id]['finished']:
                # Se era para finalizar a extensão, limpe as variáveis
                self.__limpar_variaveis(chat_id)
            
            if permissao == ['obter_nome', True]:
                # Se era apenas para obter o nome
                #print("Salvando usuário permanentemente")
                self.sec.salvar_registro_permanente(chat_id, 'nome')


            #print('Resposta ao usuário\n')
            id_interacao = self.data[chat_id]['id_interacao']
            return {
                "RESPOSTA": resposta['resposta'],
                "EXTENSAO": maior['config']['referencia'],
                "ID_INTERACAO": id_interacao,
                "STATUS": "RESPONDIDO"
            }
