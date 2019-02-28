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

- Se não possuir *Python3* ou superior instaladas executar no terminal: 

```sudo apt-get install python3```

- Caso não tenhas as bibliotecas *Python* instaladas executar no
terminal:

```pip3 install pandas```

## Como executar o programa


## Desenvolvimento

- [X] Capturar os projetos de pesquisa, e extensão, com seus respectivos
participantes, classificação do tipo de projeto (pesquisa ou extensão)
organizando os dados em um `DataFrame`; 
- [X] Capturar produção técnica de cada pesquisador
- [X] Capturar as atividades de orientação;
- [X] Ler o `.xml` direto do `.zip`;
- [X] Realizar um looping para caturar uma série de currículos.
- [X] Capturar produção em periódicos;
- [X] Associar produção em periódico com capes qualis;
- [X] Salva em pasta específica arquivos `.csv` individuais para cada
pesquisador:
    - os projetos de pesquisa e extensão;
    - cursos de curta duração;
    - orientações (tcc, ic, mestrado **FALTA DOUTORADO**);
    - publicações em periódico com qualis, revista;
- [X] Gerar um arquivo `.csv` com o extrato de produção na pasta
relatório;
- [X] Relatório em `.html`:
    - Relação de pesquisadores, cidade, estado, link lattes;
    - Lista de projetos de pesquisa e extensão;
    - Síntese de artigos publicados em periódicos;
    - Gráficos por período e por qualis;
    - Extrato de produção por pesquisador;
- [X] Grafo de interação entre pesquisadores;
    - realiza interações somente entre artigos
    - **o método de verificação deve ser melhorado**
- [ ] Capturar as atividades dos projetos de extensão;
- [ ] Gerar um `.json` file para cada currículo;

## Histórico

- 20190228: relatório está implementado, como produto um arquivo `.html`
é gerado. Para verificar a interação entre os integrantes um Grafo é
gerado, assumindo somente as interações entre os artigos em periódicos.

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
necessárias e geram os `.csv`
- `readidlist.py`: faz a leitura da lista que contém o **id** dos pesquisadores 
- `scriptLattes.py`: funciona como o executável
- `config.txt`: configurações para funcionamento do script

## Autor

- Rafael Tieppo
- rafaeltieppo@yahoo.com.br
- https://rafatieppo.github.io/



