## Configurando o ambiente pela primeira vez

A primeira vez que o sistema for instalado, ele precisará ser configurado. Essa configuração irá acontecer somente uma única vez e envolve basicamente a criação, ativação e instalação de pacotes no ambiente virtual. A configuração também envolve a correção de um bug que faz a biblioteca do telegram ser desconectada caso passe mais de 15 minutos sem interação. Tudo isso já está pronto, basta seguir o passo a passo a seguir:

Criação de um ambiente com o nome ambiente
```shell
python -m venv ambiente
```

Ativação do ambiente virtual
```shell
.\ambiente\Scripts\activate source
```

Instalação dos requisitos dentro do ambiente virtual
```shell
python -m pip install -r .\\requirements.txt
```

Correção do bug substituindo o arquivo requests do telegram
```shell
cp .\arquivos\request.py .\ambiente\Lib\site-packages\telegram\utils\
```


Crie um arquivo .env e informe o token do chatbot
```env
TELEGRAM_TOKEN=
NAME_DATABASE=REGISTROS.db
NAME_TABLE=REGISTROS_TEREZA
```

Execute o bot

```sheel
python bot.py
```
