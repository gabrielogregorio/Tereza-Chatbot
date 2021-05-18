from json import loads
from src.util import Util


class Seguranca():
    """ Gerencia requisitos de segurança e conexão do chatbot """
    def __init__(self):
        self.util = Util()
        self.config = self.util.carregar_json('config.json')
        self.config_temp = []

    def verificar_permissao(self, chat_id:str) -> list:
        """ Verifica se um usuário está permitido"""
        permitidos = [item['chat_id'] for item in self.config['autorizados']]

        # Usuário está permanentemente permitido
        if chat_id in permitidos: 
            return ['permitido', True]

        # Chat_id já está no temporário
        if chat_id in self.config_temp:
            return ['obter_nome', True]

        self.config_temp.append(chat_id)
        return ['cadastrar', True]

    def remover_registro_temporario(self, chat_id:str) -> bool:
        try:
            self.config_temp.remove(chat_id)
        except ValueError:
            return False
        return True
    
    def salvar_registro_permanente(self, chat_id:str, nome:str) -> bool:
        self.config = self.util.carregar_json('config.json')

        self.config['autorizados'].append(
            {
                "chat_id":str(chat_id),
                "e-mail": nome
            }
        )

        self.util.escrever_json('config.json', self.config)

        return True
