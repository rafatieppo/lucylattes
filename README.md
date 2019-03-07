# LATTES_SCRAPER

## Motivação


## O que faz

Organiza os dados dos currículos da plataforma *Lattes* em arquivos de
texto organizados que proporcionam rapidez para a geração de
informação. 

## Instalação

- Requerimentos:
    - Sistema operacional Linux;
    - Python 3 ou superior;
    - Navegador para visualizar relatório

- Se não possuir *Python3* ou superior instalado executar no terminal: 

*UBUNTU 18*

```sudo apt-get install python3```
```sudo apt-get install python3-pip```

- Caso não tenha as bibliotecas *Python* instaladas executar no
terminal:

```
pip3 install pandas
pip3 install numpy
pip3 install os
pip3 install requests
pip3 install BeautifulSoup
pip3 install re
pip3 install zipfile
pip3 install glob
pip3 install matplotlib.pyplot
pip3 install networkx
```

## Como executar o programa

1. Descompacte o arquivo `.zip` obtido em
[https://github.com/rafatieppo/LATTES_SCRAPER](https://github.com/rafatieppo/LATTES_SCRAPER)
em um diretório de sua preferência. 

2. Abra o arquivo `list_id_name.txt` com um editor de texto, leias as
instruções no arquivo e faça as alterações necessárias. Salve e feche o
arquivo. 

3. Faça o dowload dos *curriculos Lattes* desejados e copie todos no
diretório `xlm_zip`, *NÃO DESCOMPACTE OS ARQUIVOS*.

4. Abra o arquivo `config.txt` com um editor de texto e altere o que for
necessário. Somente edite à direita do símbolo ":" Salve e feche o arquivo.

5. Acesse o diretório `LATTES_SCRAPER` pelo terminal e digite:
`python scriptLattes.py`

6. Se tudo ocorreu corretamente, um relatório foi gerado no diretório
`relatório`, basta acessar com um navegador (Chrome ou Firefox).

## Observações

Sempre que editar o arquivo `list_id_name.txt` **APAGUE** todos os
arquivos do diretório `csv_prdoucao`.



## Desenvolvimento

* DONE Capturar os projetos de pesquisa, e extensão, com seus
respectivos participantes, classificação do tipo de projeto (pesquisa ou
extensão) organizando os dados em um `DataFrame`; 
* DONE Capturar produção técnica de cada pesquisador
* DONE Capturar as atividades de orientação;
* DONE Ler o `.xml` direto do `.zip`;
* DONE Realizar um looping para caturar uma série de currículos.
* DONE Capturar produção em periódicos;
* DONE Associar produção em periódico com capes qualis;
* TODO Salva em pasta específica arquivos `.csv` individuais para cada pesquisador[75%] 
- [X] os projetos de pesquisa e extensão;
- [X] cursos de curta duração;
- [X] publicações em periódico com qualis, revista;
- [ ] orientações (tcc, ic, mestrado **FALTA DOUTORADO**);
* DONE Gerar um arquivo `.csv` com o extrato de produção na pasta relatório;
* DONE Relatório em `.html` [100%]
- [X] Relação de pesquisadores, cidade, estado, link lattes;
- [X] Lista de projetos de pesquisa e extensão;
- [X] Síntese de artigos publicados em periódicos;
- [X] Gráficos por período e por qualis;
- [X] Extrato de produção por pesquisador;
* TODO Grafo de interação entre pesquisadores [33%]
- [X] realiza interações somente entre artigos
- [X] como **observação**, deve-se atentar que os integrantes que não possuem interação(s) não aparecem no grafo.
- [ ] Verificar as interações nos projetos de pesquisa e extensão;
- [ ] Calcular o peso das interações dos membros no grafo;
- [ ] Capturar as atividades dos projetos de extensão;
- [ ] Gerar um `.json` file para cada currículo;

## Histórico

- 20190307: o método de verificação da ordem de autoria do paper foi
melhorado, a ordem é obtida direto do lattes.   

- 20190228: relatório está implementado, como produto um arquivo `.html`
é gerado. Para verificar a interação entre os integrantes um Grafo é
gerado, assumindo somente as interações entre publicações em periódicos.

- 20190219: relatório `.html` foi iniciado, mas não foi implementado na
função ainda. 

- 20190216: foi inserido uma verificação no scraperlattes, caso o
comprimento da lista seja zero é informado. Há um arquivo `.csv` com o
nome completo, sobrenome, e id do pesquisador. Foi iniciado a análise de
dados para o reatório.

- 20190214: foi criado um arquivo `config.txt` com objetivos de:
    - especificar o arquivo `.csv` que será utilizado no qualis.

- 20190213: função para capturar os periódicos com qualis foi concluída,
os arquivos `.xlm` foram movidos para a pasta `xlm_zip`.

- 20190212: os arquivos `.xlm` são lidos diretamente do arquivo
`.zip`. Foi criado um arquivo **lista** no formato `.csv`, neste arquivo
deve conter o **id** *Lattes* de cada pesquisador e seus respectivo nome.

- 20190126: do arquivo xlm do lattes é possível extrair o nome do
projeto, tipo do projeto, ano de início, e integrantes, etc

## Arquivos

- `scraperlattes.py`: contém as funções que extraem as informações
necessárias e geram os `.csv`;
- `readidlist.py`: faz a leitura da lista que contém o **id** dos pesquisadores ;
- `scriptLattes.py`: funciona como o executável;
- `config.txt`: configurações para funcionamento do script;
- `tidydf.py`: organiza os `DataFrame`;
- `report.py`: gerador do relatório;
- `grapho.py`: gerador do gráfico com as interações entre os membros.


## Autor

- Rafael Tieppo
- rafaeltieppo@yahoo.com.br
- https://rafatieppo.github.io/



