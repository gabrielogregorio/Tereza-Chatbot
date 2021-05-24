# pip install python-dotenv

from re import search as re_search
from telegram.ext import Filters
from telegram.ext import Updater
from telegram import Update
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.utils.request import Request
from json import loads
from os import path as ospath
from src.chatBots import ChatBot
from src.util import *
from dotenv import load_dotenv 
from os import getenv
from api.database import DataBase
from datetime import datetime

load_dotenv(verbose=True)


class Api():
    def __init__(self):
        self.token_telegram = getenv("TELEGRAM_TOKEN")
        self.bot = ChatBot()
        self.database = DataBase(getenv("NAME_DATABASE"), getenv("NAME_TABLE"))

    def __salvar_historico(self, 
            ID_INTERACAO:int,
            CHAT_ID:str,
            STATUS:str,
            PERGUNTA:str,
            RESPOSTA:str,
            EXTENSAO:str,
            DATA_HORA_PERGUNTA:str,
            DATA_HORA_RESPOSTA:str):

        self.database.inserir_dados(
                ID_INTERACAO=ID_INTERACAO,
                CHAT_ID=CHAT_ID,
                STATUS=STATUS,
                PERGUNTA=PERGUNTA,
                RESPOSTA=RESPOSTA,
                EXTENSAO=EXTENSAO,
                DATA_HORA_PERGUNTA=DATA_HORA_PERGUNTA,
                DATA_HORA_RESPOSTA=DATA_HORA_RESPOSTA
        )

    def __interacao(self, update: Update, context: CallbackContext):
        DATA_HORA_PERGUNTA = datetime.now()

        try:
            PERGUNTA = str(update.message.text)
            CHAT_ID = str(update.message.chat_id)
        except Exception as e:
            print(e)
            return ""
        
        PERGUNTA = PERGUNTA.replace('?', '')
        PERGUNTA = PERGUNTA.replace('!', '')

        RESPOSTA = self.bot.interacao_chat(CHAT_ID, PERGUNTA)
        EXTENSAO = RESPOSTA['EXTENSAO']
        ID_INTERACAO = RESPOSTA['ID_INTERACAO']
        lista_respostas = RESPOSTA['RESPOSTA'].split('\n')

        STATUS = RESPOSTA['STATUS']

        resposta = ''
        for linha in lista_respostas:
            teste_especial = re_search('\\!\\[([\\w]{2,})\\]\\((.*)\\s{1,}"(.*)\\"\\)', linha)

            if teste_especial:
                if resposta.strip():
                    update.message.reply_text(text=resposta)
                    resposta = ''

                tipo, file, caption = teste_especial.group(1), teste_especial.group(2), teste_especial.group(3)

                with open(file, 'rb') as binary_file:
                    if tipo == 'documento':
                        update.message.reply_document(binary_file, caption=caption, parse_mode='html')
                    elif tipo == 'imagem':
                        update.message.reply_photo(binary_file, caption=caption, parse_mode='html')
                    elif tipo == 'video':
                        update.message.reply_video(binary_file, caption=caption, parse_mode='html')
            else:
                resposta = resposta + '\n' + linha 

        # Verificar se só tem linhas vazias
        test = resposta.replace('\n', '')

        if test:
            update.message.reply_text(text=resposta)

        DATA_HORA_RESPOSTA = datetime.now()

        self.__salvar_historico(ID_INTERACAO,
                    CHAT_ID,
                    STATUS,
                    PERGUNTA,
                    RESPOSTA['RESPOSTA'],
                    EXTENSAO,
                    DATA_HORA_PERGUNTA,
                    DATA_HORA_RESPOSTA)

    def main(self):
        updater = Updater(self.token_telegram)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(MessageHandler(Filters.text, self.__interacao))

        updater.start_polling()
        updater.idle()


if __name__ == "__main__":
    bot = Api()
    bot.main()
