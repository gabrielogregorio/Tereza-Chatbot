import unittest
from src.chatBots import ChatBot


# Classe de teste
class TestCadastro(unittest.TestCase):
    def test_cadastro(self):
        e1 = "obrigado mesmo"
        s1 = "Foi um prazer ajudar\n"

        e2 = "Grato"
        s2 = "Foi um prazer ajudar\n"

        e3 = "oi linda"
        s3 = "Se toca, sou um programa de computador, acabei de reportar a diretoria da Fatec. Melhor você não fazer isso novamente, pois está marcado!\n"

        e4 = "manda nuds"
        s4 = "Se toca, sou um programa de computador, acabei de reportar a diretoria da Fatec. Melhor você não fazer isso novamente, pois está marcado!\n"

        e5 = "Me desculpe"
        s5 = "Melhor não fazer isso de novo!\n"

        e6 = "eae"
        s6 = "Olá, do que você precisa?\n"

        e7 = "oi robô"
        s7 = "Olá, do que você precisa?\n"

        e8 = "Qual a carga horária do  obrigatório estágio"
        s8 = "A carga horária total do estágio é de 240 horas. Estas horas devem ser cumpridas em até seis horas diárias totalizando no máximo 30 horas semanais.\n"

        e9 = "Todo estágio deve ter um professor orientador"
        s9 = "Sim, todo o estágio precisa ter um professor orientador, ele precisa ser da mesma área em que você vai estagiar. Você deve indicar o nome do professor na hora da formalização do contrato.\n"

        e10 = "O estagio e obrigatorio?"
        s10 = "Sim, o estágio é obrigatório, inclusive é previsto na grade curricular dos cursos. O estudante que não cumpre 240 horas, não pode colar grau. (Se formar)\n"

        e11 = "De que parte a iniciativa para iniciar o estágio"
        s11 = "Para iniciar o estágio você deve tomar a iniciativa. Você deve observar o mercado para perceber as empresas que se enquadram no seu desejo profissional. Após isso, deve buscar o contato da pessoa responsável pelo Recursos Humanos para o iniciar o diálogo sobre o estágio. Você também deve conversar com um professor responsável, pois precisa se cadastrar na disciplina de estágio no Siga no início do Semestre.\n"

        e12 = "Em quais empresas posso fazer estágio?"
        s12 = "Você pode fazer o estágio em empresas que possuem afinidade com sua área de formação profissional. Ou seja, se você está cursando Análise e desenvolvimento de sistemas, precisa fazer estágio em uma área que engloba ADS\n\n"

        e13 = "Ja escolhi a empresa em que desejo estagiar e obtive resposta positiva do Recursos Humanos da organizacao. O que devo fazer agora"
        s13 = "Agora que você já recebeu uma resposta positiva do RH da empresa, você precisa seguir com estes passos em relação ao seu estágio:\n\nEntre em contato com o\(a\) Coordenador\(a\) de Estágio do seu curso:\n\nProfa. Me. Lucilena de Lima - luma.delima@gmail.com - Coordenadora de estágio do Curso de Análise e Desenvolvimento de Sistemas\n\nProfa. Me. Agatha S. de Morais - agatha-morais@hotmail.com - Coordenadora de estágio do Curso de Biocombustíveis \(tarde\)\n\nProf. Dr. Wesley Pontes - wesley.pontes@gmail.com Coordenador de estágio do Curso de Biocombustíveis \(noite\\)\n\n"

        e14 = "Preciso dos documentos do estagio"
        s14 = "Acesse o site:\n\nFatec Araçatuba: https://www.fatecaracatuba.edu.br/estagio.php#arquivos\n\nSe você não conseguir baixar os documentos, clique com o botão esquerdo do mouse e abra o documento em uma nova página!\n\n"

        e15 = "qual é o site da Fatec?"
        s15 = "O site da Fatec é o https://www.fatecaracatuba.edu.br/\n"

        e16 = "qual é o site do Ronnie"
        s16 = "O site do Ronnie é o http://auladehoje.com.br/home/\n"

        e17 = "quais aulas eu tenho hoje?"
        s17 = "Segue o site com um PDF com os horários.\n\nHorário ADS\nhttps://www.fatecaracatuba.edu.br/curso_ads.php#horarios\n\nHorário Biocombustíveis\nhttps://www.fatecaracatuba.edu.br/curso_bio.php#horarios\n\nHorário Gestão Empresarial\nhttps://www.fatecaracatuba.edu.br/curso_gestao.php\n\n"

        e18 = "teste"
        s18 = "Por favor, escolha um curso que você deseja fazer:\n\n/curso_ads\n/curso_biocombustiveis\n"

        e19 = "/curso_ads"
        s19 = "Você escolheu o curso de /curso_ads\n"

        id1 = '222'

        self.bt = ChatBot()

        # Simula duas interações simultâneas na mesma extensão de cadastro na sematec.
        self.assertEqual(self.bt.interacao_chat(id1, e1)['RESPOSTA'], s1)
        self.assertEqual(self.bt.interacao_chat(id1, e2)['RESPOSTA'], s2)
        self.assertEqual(self.bt.interacao_chat(id1, e3)['RESPOSTA'], s3)
        self.assertEqual(self.bt.interacao_chat(id1, e4)['RESPOSTA'], s4)
        self.assertEqual(self.bt.interacao_chat(id1, e5)['RESPOSTA'], s5)
        self.assertEqual(self.bt.interacao_chat(id1, e6)['RESPOSTA'], s6)
        self.assertEqual(self.bt.interacao_chat(id1, e7)['RESPOSTA'], s7)
        self.assertEqual(self.bt.interacao_chat(id1, e8)['RESPOSTA'], s8)
        self.assertEqual(self.bt.interacao_chat(id1, e9)['RESPOSTA'], s9)
        self.assertEqual(self.bt.interacao_chat(id1, e10)['RESPOSTA'], s10)
        self.assertEqual(self.bt.interacao_chat(id1, e11)['RESPOSTA'], s11)
        self.assertEqual(self.bt.interacao_chat(id1, e12)['RESPOSTA'], s12)
        self.assertEqual(self.bt.interacao_chat(id1, e13)['RESPOSTA'], s13)
        self.assertEqual(self.bt.interacao_chat(id1, e14)['RESPOSTA'], s14)
        self.assertEqual(self.bt.interacao_chat(id1, e15)['RESPOSTA'], s15)
        self.assertEqual(self.bt.interacao_chat(id1, e16)['RESPOSTA'], s16)
        self.assertEqual(self.bt.interacao_chat(id1, e17)['RESPOSTA'], s17)
        self.assertEqual(self.bt.interacao_chat(id1, e18)['RESPOSTA'], s18)
        self.assertEqual(self.bt.interacao_chat(id1, e19)['RESPOSTA'], s19)

if __name__ == '__main__':
    unittest.main()

# python -m unittest -v
