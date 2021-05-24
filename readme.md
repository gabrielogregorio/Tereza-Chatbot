## Configurando o ambiente pela primeira vez

> O sistema precisa estar sendo executado com o python 3.7 ou superior em uma máquina windows 10.  

A primeira vez que o sistema for instalado, ele precisará ser configurado. Essa configuração irá acontecer somente uma única vez e envolve basicamente a criação, ativação e instalação de pacotes no ambiente virtual. A configuração também envolve a correção de um bug que faz a biblioteca do telegram ser desconectada caso passe mais de 15 minutos sem interação. Tudo isso já está pronto, basta seguir o passo a passo a seguir:

Crie um ambiente com o comando abaixo
```shell
python -m venv ambiente
```

Ative o ambiente virtual
```shell
.\ambiente\Scripts\activate source
```

Instale os requisitos do chatbot
```shell
python -m pip install -r .\\requirements.txt
```

Substitua o arquivo problemático com um com a correção
```shell
cp .\arquivos\request.py .\ambiente\Lib\site-packages\telegram\utils\
```

Crie um arquivo .env na raiz do projeto e informe o token do chatbot
```env
TELEGRAM_TOKEN=
NAME_DATABASE=REGISTROS.db
NAME_TABLE=REGISTROS_TEREZA
```

Execute o bot sempre dentro do ambiente virtual

```sheel
python bot.py
```

Para usar o \ nas respostas das extensões é preciso usar duas barras, \\

# Como adicionar uma extensão
Por definição você precisará o aproveitar uma extrutura de diretórios, seguindo o seguinte padrão:
```
extensoes/escola/curso/disciplina/assunto
```
Dentro da pasta assunto, basta adicionar o arquivo de configuração e o arquivo de extensão:

Arquivo config.json
```
{
    "configuracoes": {
        "precisao": 80,
        "timeout": "00:02:00",
        "tentativas": 3,
        "mensagens_tentativas": [
            "Mensagem caso extrapole o número de tentativas"
        ]
    },
    "variaveis": {},
    "principal": [
        "Frase do usuário que aciona a extensão"
    ],
    "finalizar_interacao": [
        "resposta ao usuário"
    ]
}
```

Arquivo extensao.py
```python
from random import choice
from src.Extensao import Extensao


class main(Extensao):
    def __init__(self, dict_extensao):
        Extensao.__init__(self, dict_extensao)

    def entrada(self, dados:dict, prox_ponto_referencia:str, chat_id) -> dict:
        self.carregar_variaveis(dados, chat_id)
    
        if prox_ponto_referencia == "principal":
            resposta = choice(dados['config']["finalizar_interacao"])
            return self.responder(
              resposta=resposta,
              prox_ponto_referencia="",
              chat_id=chat_id,
              liberar=True)
```
Desta forma, ao iniciar o chatbot novamente esta extensão será carregada.