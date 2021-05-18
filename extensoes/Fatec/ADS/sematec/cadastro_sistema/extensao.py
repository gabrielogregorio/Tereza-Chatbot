from random import choice
import re
from src.Extensao import Extensao

class main(Extensao):
    def __init__(self, dict_extensao):
        Extensao.__init__(self, dict_extensao)

    def entrada(self, dados:dict, prox_ponto_referencia:str, chat_id) -> dict:
        self.carregar_variaveis(dados, chat_id)
    
        if prox_ponto_referencia == "principal": # Principal
            resposta = choice(dados['config']["perguntar_nome"]) # Pergunta
            return self.responder(resposta=resposta, prox_ponto_referencia="ref_obter_nome", chat_id=chat_id, liberar=False)

        elif prox_ponto_referencia == "ref_obter_nome": # ponto Referencia
            resposta = choice(dados['config']["perguntar_idade"]) # Pergunta
            return self.responder(resposta=resposta, prox_ponto_referencia="ref_obter_idade", chat_id=chat_id, liberar=False)
 
        elif prox_ponto_referencia == "ref_obter_idade":
            resposta = choice(dados['config']["perguntar_data_nascimento"]) # Pergunta
            return self.responder(resposta=resposta, prox_ponto_referencia="ref_obter_data_nascimento", chat_id=chat_id, liberar=False)

        elif prox_ponto_referencia == "ref_obter_data_nascimento":
            resposta = choice(dados['config']["perguntar_cep"]) # Pergunta
            return self.responder(
                resposta=resposta,
                prox_ponto_referencia="ref_obter_cep",
                chat_id=chat_id,
                liberar=False)

        elif prox_ponto_referencia == "ref_obter_cep":
            resposta = choice(dados['config']["perguntar_cpf"]) # Pergunta
            return self.responder(
                resposta=resposta,
                prox_ponto_referencia="ref_obter_cpf",
                chat_id=chat_id,
                liberar=False)

        elif prox_ponto_referencia == "ref_obter_cpf":
            resposta = choice(dados['config']["perguntar_materia"]) # Pergunta
            return self.responder(
                resposta=resposta,
                prox_ponto_referencia="ref_obter_materia",
                chat_id=chat_id,
                liberar=False)

        elif prox_ponto_referencia == "ref_obter_materia":
            resposta = choice(dados['config']["perguntar_confirma_dados"]) # Pergunta
            return self.responder(
                resposta=resposta,
                prox_ponto_referencia="ref_obter_confirmacao",
                chat_id=chat_id,
                liberar=False)
        
        elif prox_ponto_referencia == "ref_obter_confirmacao":
            resposta = choice(dados['config']["finalizar_interacao"]) # Pergunta
            if (dados['variaveis']['dados_corretos'] == '/sim'):
                return self.responder(
                    resposta=resposta,
                    prox_ponto_referencia="",
                    chat_id=chat_id,
                    liberar=True)
            else:
                resposta = 'Ok, vou perguntar novamente, qual é o seu nome?'
                return self.responder(
                    resposta=resposta,
                    prox_ponto_referencia="ref_obter_nome",
                    chat_id=chat_id,
                    liberar=False)
