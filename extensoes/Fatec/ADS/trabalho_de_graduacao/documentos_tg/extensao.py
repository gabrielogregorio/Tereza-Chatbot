from random import choice
from src.Extensao import Extensao
import os
 
class main(Extensao):
    def __init__(self, dict_extensao):
        Extensao.__init__(self, dict_extensao)

    def entrada(self, dados:dict, prox_ponto_referencia:str, chat_id) -> dict:
        self.carregar_variaveis(dados, chat_id)
    
        if prox_ponto_referencia == "principal": # Principal
            resposta = choice(dados['config']["finalizar_interacao"]) # Pergunta
            return self.responder(resposta=resposta, prox_ponto_referencia="", chat_id=chat_id, liberar=True) # Esperar Resposta
