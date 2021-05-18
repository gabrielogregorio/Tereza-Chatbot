from random import choice
import re
from src.Extensao import Extensao


class main(Extensao):
    def __init__(self, dict_extensao):
        Extensao.__init__(self, dict_extensao)

    def entrada(self, dados:dict, prox_ponto_referencia:str, chat_id) -> dict:
        self.carregar_variaveis(dados, chat_id)
    
        if prox_ponto_referencia == "principal":
            resposta = choice(dados['config']["teste"])
            return self.responder(
                resposta=resposta,
                prox_ponto_referencia="coletar",
                chat_id=chat_id,
                liberar=False)
 
        if prox_ponto_referencia == "coletar":
            resposta = choice(dados['config']["finalizar_interacao"])
            return self.responder(
                resposta=resposta,
                prox_ponto_referencia="",
                chat_id=chat_id,
                liberar=True)