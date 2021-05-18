from random import choice
from src.Extensao import Extensao

class main(Extensao):
    def __init__(self, dict_extensao):
        Extensao.__init__(self, dict_extensao)

    def entrada(self, dados:dict, prox_ponto_referencia:str, chat_id) -> dict:
        self.carregar_variaveis(dados, chat_id)

        if prox_ponto_referencia == "principal":
            resposta = choice(dados['config']["finalizar_interacao"])
            return self.responder(resposta=resposta, chat_id=chat_id, prox_ponto_referencia="", liberar=True)
