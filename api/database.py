import sqlite3
import os

class DataBase():
    def __init__(self, NAME_DATABASE, NAME_TABLE):
        self.NAME_DATABASE = NAME_DATABASE
        self.NAME_TABLE = NAME_TABLE

        #self.__criar_tabela()

    def __criar_tabela(self):
        """ Só é para ser usado uma vez"""
        conn = sqlite3.connect(self.NAME_DATABASE)
        cursor = conn.cursor()

        # criando a tabela (schema)
        cursor.execute("""
        CREATE TABLE {} (
                ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                ID_INTERACAO INTEGER NOT NULL,
                CHAT_ID INTEGER NOT NULL,
                STATUS TEXT NOT NULL,
                PERGUNTA TEXT NOT NULL,
                RESPOSTA TEXT NOT NULL,
                EXTENSAO TEXT NOT NULL,
                DATA_HORA_PERGUNTA DATE not null,
                DATA_HORA_RESPOSTA DATE not null
    
        );
        """.format(self.NAME_TABLE))

        print('Tabela criada com sucesso.')
        conn.close()

    def inserir_dados(self,
        ID_INTERACAO:int,
        CHAT_ID:str,
        STATUS:str,
        PERGUNTA:str,
        RESPOSTA:str,
        EXTENSAO:str,
        DATA_HORA_PERGUNTA:str,
        DATA_HORA_RESPOSTA:str
        ) -> int: # ID

        conn = sqlite3.connect(self.NAME_DATABASE)
        cursor = conn.cursor()

        # inserindo dados na tabela
        cursor.execute("""
        INSERT INTO {} (ID_INTERACAO, CHAT_ID, STATUS, PERGUNTA, RESPOSTA, EXTENSAO, DATA_HORA_PERGUNTA, DATA_HORA_RESPOSTA)
        VALUES (?,?,?,?,?,?,?,?)
        """.format(self.NAME_TABLE),
            (ID_INTERACAO, CHAT_ID, STATUS, PERGUNTA, RESPOSTA, EXTENSAO, DATA_HORA_PERGUNTA, DATA_HORA_RESPOSTA)
        )

        conn.commit()

        print('Dados inseridos com sucesso, id=', ID_INTERACAO)

        conn.close()

        return True

    def atualizar_dados(self, ID:int, STATUS:str) -> bool:
        ID = int(ID)
        STATUS = str(STATUS)

        conn = sqlite3.connect(self.NAME_DATABASE)
        cursor = conn.cursor()

        # alterando os dados da tabela
        cursor.execute("""
        UPDATE {}
        SET STATUS = ?
        WHERE id = ?
        """.format(self.NAME_TABLE), (STATUS, ID))

        conn.commit()

        print('Dados atualizados com sucesso, id={}, status={}'.format(STATUS, ID))

        conn.close()

        return True


    def deletar_dados(self, ID:int):
        ID = int(ID)

        conn = sqlite3.connect(self.NAME_DATABASE)
        cursor = conn.cursor()

        # excluindo um registro da tabela
        cursor.execute(
            """ DELETE FROM {} WHERE ID = ?""".format(self.NAME_TABLE), (ID,))

        conn.commit()

        print('Registro excluido com sucesso, id=', ID)

        conn.close()

    def ler_dados(self):
        conn = sqlite3.connect(self.NAME_DATABASE)
        cursor = conn.cursor()

        # lendo os dados
        cursor.execute("""SELECT * FROM {}; """.format(self.NAME_TABLE))
        dict_dados = {}

        n = 0;
        data = cursor.fetchall()
        data.reverse()

        for linha in data:
            dict_dados[linha[0]] = {
                'ID_INTERACAO': linha[1],
                'CHAT_ID': linha[2],
                'STATUS': linha[3],
                'PERGUNTA': linha[4],
                'RESPOSTA': linha[5],
                'EXTENSAO': linha[6],
                'DATA_HORA_PERGUNTA': linha[7],
                'DATA_HORA_RESPOSTA': linha[8]
            }
            n += 1
            if (n == 10):
                break

        conn.close()
        return dict_dados



    def ler_dados_id(self, _id):
        conn = sqlite3.connect(self.NAME_DATABASE)
        cursor = conn.cursor()

        # lendo os dados
        cursor.execute("""SELECT * FROM {} where id = {}; """.format(self.NAME_TABLE, _id))

        data = cursor.fetchone()

        conn.close()
        return data


if __name__ == '__main__':
    database = DataBase('REGISTROS.db', 'REGISTROS_TEREZA')
    database.__criar_tabela()




    '''

    database.inserir_dados(
            ID_INTERACAO=123123,
            CHAT_ID="113541341",
            STATUS="RESPOSTA_DINAMICA",
            PERGUNTA="Qual é o e-mail do Saulo",
            RESPOSTA="O e-mail do saulo é o xx@xx.com",
            EXTENSAO='PERGUNTAR_EMAIL',
            DATA_HORA_PERGUNTA = '2021-04-11 17:47:00',
            DATA_HORA_RESPOSTA = '2021-04-11 17:47:03'
    )
    '''
    #database.ler_dados()
    #database.atualizar_dados(
    #    ID=1,
    #    STATUS="RESPOSTA_POR_EXTENSAO")
    #database.ler_dados()

    #database.deletar_dados(1)
