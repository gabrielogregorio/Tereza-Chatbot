import unittest
from src.chatBots import ChatBot


# Classe de teste
class TestCadastro(unittest.TestCase):
    def test_cadastro(self):
        e1 = "quero me cadastrar no novo semestre"
        s1 = "Qual é o seu nome? (Digite apenas o seu nome)\n"

        e2 = "Gabriel Gregório"
        e2_ = "Julian Riberio"
        s2 = "Qual é a sua idade\n"

        e3 = "tenho 18 anos"
        e3_ = "tenho 25 anos"
        s3 = "Você nasceu em qual ano? Exemplo: 03/12/1996\n"

        e4 = "Eu nasci em 11"
        e4_ = "Eu nasci em 25"
        s4 = "Eu não entendi, você poderia escrever de outra forma?"

        e5 = "Eu nasci em 12/03/1992"
        e5_ = "Eu nasci em 03/01/2005"
        s5 = "Qual o seu CEP?\n"

        e6 = "Meu cep é 16140-970"
        e6_ = "Meu cep é 12344-000"
        s6 = "Qual o seu CPF?\n"

        e7 = "72452644136"
        e7_ = "36489435434"
        s7 = "Clique na matéria que você quer se inscrever?\n\n/analiseDesenvolvimentoDeSistemas\n/biocombustiveis\n"

        e8 = "/biocombustiveis"
        e8_ = "/analiseDesenvolvimentoDeSistemas"
        s8 = "Ok, Os dados estão corretos?\n\n- nome = 'Gabriel Gregório'\n- idade = '18'\n- data de nascimento = '12/03/1992'\n- cep = '16140-970'\n- cpf = '72452644136'\n- materia = '/biocombustiveis'\n \n/sim\n/nao\n"
        s8_ = "Ok, Os dados estão corretos?\n\n- nome = 'Julian Riberio'\n- idade = '25'\n- data de nascimento = '03/01/2005'\n- cep = '12344-000'\n- cpf = '36489435434'\n- materia = '/analiseDesenvolvimentoDeSistemas'\n \n/sim\n/nao\n"

        e9 = "/sim"
        s9 = "Ok, muito obrigado, seu cadastro na Fatec está realizado. Bem-vindo!\n"

        id1 = '792445887'
        id2 = '1079590751'

        e10 = '/nao'
        s10 = 'Ok, vou perguntar novamente, qual é o seu nome?\n'


        self.bt = ChatBot()

        # Simula duas interações simultâneas na mesma extensão de cadastro na sematec.

        self.assertEqual(self.bt.interacao_chat(id1, e1), s1)
        self.assertEqual(self.bt.interacao_chat(id2, e1), s1)
        self.assertEqual(self.bt.interacao_chat(id1, e2), s2)
        self.assertEqual(self.bt.interacao_chat(id1, e3), s3)
        self.assertEqual(self.bt.interacao_chat(id2, e2_), s2)
        self.assertEqual(self.bt.interacao_chat(id2, e3_), s3)
        self.assertEqual(self.bt.interacao_chat(id1, e4), s4)
        self.assertEqual(self.bt.interacao_chat(id1, e5), s5)
        self.assertEqual(self.bt.interacao_chat(id1, e6), s6)
        self.assertEqual(self.bt.interacao_chat(id2, e4_), s4)
        self.assertEqual(self.bt.interacao_chat(id2, e5_), s5)
        self.assertEqual(self.bt.interacao_chat(id2, e6_), s6)
        self.assertEqual(self.bt.interacao_chat(id1, e7), s7)
        self.assertEqual(self.bt.interacao_chat(id1, e8), s8)
        self.assertEqual(self.bt.interacao_chat(id2, e7_), s7)
        self.assertEqual(self.bt.interacao_chat(id2, e8_), s8_)
        self.assertEqual(self.bt.interacao_chat(id2, e9), s9)

        self.assertEqual(self.bt.interacao_chat(id1, e10), s10)
        self.assertEqual(self.bt.interacao_chat(id1, e2), s2)
        self.assertEqual(self.bt.interacao_chat(id1, e3), s3)
        self.assertEqual(self.bt.interacao_chat(id1, e4), s4)
        self.assertEqual(self.bt.interacao_chat(id1, e5), s5)
        self.assertEqual(self.bt.interacao_chat(id1, e6), s6)
        self.assertEqual(self.bt.interacao_chat(id1, e7), s7)
        self.assertEqual(self.bt.interacao_chat(id1, e8), s8)
        self.assertEqual(self.bt.interacao_chat(id1, e9), s9)

if __name__ == '__main__':
    unittest.main()

# python -m unittest -v
