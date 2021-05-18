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
            return self.responder(resposta=resposta, chat_id=chat_id, prox_ponto_referencia="ref_obter_nome", liberar=False) # Esperar Resposta

        elif prox_ponto_referencia == "ref_obter_nome": # ponto Referencia
            resposta = choice(dados['config']["finalizar_interacao"]) # Pergunta
            return self.responder(resposta=resposta, prox_ponto_referencia="", chat_id=chat_id, liberar=True) # Esperar Resposta
 