#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__       = 'Gabriel Gregório da Silva'
__email__        = 'gabriel.gregorio.1@outlook.com'
__description__  = 'Compara duas palavras'
__status__       = 'Development'
__last_update__  = '09/04/2021'
__version__      = '0.3'

import unidecode
import json


class Compare():
    def __init__(self):
        # Carrega dados na memória
        self.dict_de_palavras = {}

        with open('classes.json', 'r', encoding='utf-8') as f:
            self.dict_classes = json.loads(f.read())

        # Percorre as classes e a lista de palavras
        # correspondente a uma classe
        for classe, palavras in self.dict_classes.items():
            lista = []
            for palavra in palavras:
                lista.append(unidecode.unidecode(palavra))
            
            self.dict_classes[classe] = lista

        # Percorre as classes e a lista de palavras
        # correspondente a uma classe
        for classe, palavras in self.dict_classes.items():
            for palavra in palavras:
                # unicode remove acentos
                self.dict_de_palavras[unidecode.unidecode(palavra)] = classe

    def __verificar_semelhanca(self, palavra1:str, palavra2:str) -> bool:
        palavra1 = unidecode.unidecode(palavra1)
        palavra2 = unidecode.unidecode(palavra2)
        
        # Verifica se a palavra existe no
        # contexto do dicionário de palavras
        if self.dict_de_palavras.get(palavra1):
            # Lista de palavras similares
            if palavra2 in self.dict_classes[self.dict_de_palavras[palavra1]]:
                # palavra é sinônimo
                return True
        return False

    def __reconstruir_frases(self, lista:list) -> list:
        frase = ""
        for palavra in lista:
            frase = frase + ' ' + palavra
        return frase.strip()

    def __normalizar_frase(self, frase1:str, frase2:str) -> tuple:
        frase1 = frase1.strip().lower()
        frase2 = frase2.strip().lower()

        l_frase1 = frase1.split(' ')
        l_frase2 = frase2.split(' ')
        
        if len(l_frase2) > len(l_frase1):
            l_maior_frase = l_frase2
            l_menor_frase = l_frase1
        else:
            l_maior_frase = l_frase1
            l_menor_frase = l_frase2

        for palavra_maior_frase in l_maior_frase:
            for n_menor_frase in range(len(l_menor_frase)):
                palavra_menor_frase = l_menor_frase[n_menor_frase]
                
                if self.__verificar_semelhanca(palavra_maior_frase, palavra_menor_frase):
                    l_menor_frase[n_menor_frase] = palavra_maior_frase

        return (self.__reconstruir_frases(l_menor_frase), self.__reconstruir_frases(l_maior_frase)) 

    # Inicia a comparação
    def comparar_palavras(self, menor:str, maior:str) -> int: 
        lista_remover = ['?', '!', ',']

        for item in lista_remover:
            menor = menor.replace(item, ' ')
            maior = maior.replace(item, ' ')

        menor = menor.replace('@', 'a')
        maior = maior.replace('@', 'a')

        menor = menor.strip().lower()
        maior = maior.strip().lower()

        menor = menor.replace('  ', ' ')
        maior = maior.replace('  ', ' ')

        # Dados inválidos
        if menor == '' or menor == '' or menor.isspace() or menor.isspace():
            return 0
        
        # o 'b' tem que ser maior que o 'a' ou no minimo igual!
        if len(menor) > len(maior):
            c = maior
            maior = menor
            menor = c
        
        # Normalizar Frase

        menor, maior = self.__normalizar_frase(menor, maior)
        # o 'b' tem que ser maior que o 'a' ou no minimo igual!
        if len(menor) > len(maior):
            c = maior
            maior = menor
            menor = c

        # Remoção de espaços | Todos para minisculos | Adição de espaços | Para lista
        menor = menor.replace(' ','').lower()
        maior = maior.replace(' ','').lower()

        # Retorna a soma entre a análise por __letras e a análise por duas silabas
        __letras, bissilabas = int(self.__letras(menor, maior)), int(self.__bisilabas(menor, maior))
        return __letras+bissilabas


    def __letras(self, a:str, b:str) -> int:
        # Isolamento das variáveis 'a' e 'b'
        a_1 = a
        b_1 = b

        # Adição de espaços nas variáveis isoladas e tranformação em lista
        a_1 = a_1.replace('',' ').split(" ")
        b_1 = b_1.replace('',' ').split(" ")

        # Corte dos espaços no começo e no fim
        a = str(a[1:len(a)-1])
        b = str(b[1:len(b)-1])

        # Salva o total de posições na maior variável isolada (b)
        total_b = len(b_1)

        # Processamento de __letras
        for x in a_1:
            for y in b_1:
                if x == y:
                    b_1.remove(y)
                    break
        # Retorna um valor de 0 a 50!
        try:
            return ((50/total_b)*(total_b-len(b_1)))
        except:
            print("Erro na saida da definição __letras")
            return 0

    def __bisilabas(self, a:str, b:str) -> int:
        # Isolamento das variáveis 'a' e 'b'
        ab = a
        bb = b

        # Criação das listas
        c = []
        d = []

        # Declaração dos andantes
        x = 0
        y = 0

        # Loops de 2 em 2 para criar uma lista de __bisilabas
        while y < len(ab):
            c.append(ab[y:y+2])
            y=y+1

        while x < len(bb):
            d.append(bb[x:x+2])
            x=x+1

        # Registra o valor da maior variável isolada (b)
        b_salva = len(d)

        # Processamento de silabas
        for p in c:
            for l in d:
                if p == l:
                    d.remove(l)
                    break
        # Retorna um valor de 0 a 50!
        try:
            return ((50*(b_salva - len(d)) )/b_salva)
        except:
            print("Erro na saida da definição bissilabas")
            return 0
