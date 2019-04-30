# lucyLattes

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2591748.svg)](https://doi.org/10.5281/zenodo.2591748)

## Última atualização

*Tue 2019-04-30 15:01:59 -04*

## Motivação

O CNPq por meio do currículo Lattes agrega dados do registro da vida
profissional de estudantes, professores, e pesquisadores do país,
e tornando-se padrão nacional no meio científico para consulta sobre a
produção científica dos referidos profissionais.

Contudo, após a criação do captcha para o acesso aos currículos Lattes,
extrair dados dos currículos se tornou uma tarefa árdua, pois todas vez
que pretende-se acessar um currículo, torna-se necessário passar pelo
captcha.  Com o intuito de auxiliar na obtenção destes dados, o
`lucyLattes` foi desenvolvido. 

## O que faz

Extração, compilação, e organização dos dados dos currículos da
plataforma *Lattes* em arquivos de texto, e geração de um relátório
simplificado, que proporcionam agilidade para a geração de informação.

## Notas

> O lucyLattes não tem vínculo com o CNPq. Este programa computacional
> é fruto de um esforço (independente) realizado com o objetivo de dar
> suporte às rotinas de análise de dados cadastradas nos Currículos
> Lattes (publicamente disponíveis).

> Este programa é um software livre; você pode redistribui-lo e/ou
> modificá-lo dentro dos termos da Licença Pública Geral
> GNU. **Verifique** o arquivo **LICENSE.txt** . 

> Este programa é distribuído na esperança que possa ser util, mas SEM
> NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
> MERCADO ou APLICAÇÃO EM PARTICULAR. **Verifique** o arquivo
> **LICENSE.txt** . 


## Instalação

- Requerimentos:
    - Sistema operacional Linux;
    - Python 3 ou superior;
    - Navegador para visualizar relatório

- Se não possuir *Python3* ou superior instalado executar no terminal: 

Se vc usar *UBUNTU 18*

```sudo apt-get install python3```

```sudo apt-get install python3-pip```

```sudo apt-get install python3-tk```

- Caso não tenha as bibliotecas *Python* instaladas executar no
terminal:

```
pip3 install pandas
pip3 install numpy
pip3 install requests
pip3 install beautifulsoup4
pip3 install matplotlib
pip3 install networkx
pip3 install lxml
pip3 install tabulate
```

## Como executar o programa

1. Descompacte o arquivo `.zip` obtido em
[https://github.com/rafatieppo/lucyLattes](https://github.com/rafatieppo/lucyLattes)
em um diretório de sua preferência. 

2. Abra o arquivo `list_id_name.txt` com um editor de texto, leias as
instruções no arquivo e faça as alterações necessárias. Salve e feche o
arquivo. 

3. Faça o dowload dos *curriculos Lattes* desejados e copie todos no
diretório `xml_zip`, *NÃO DESCOMPACTE OS ARQUIVOS*.

4. Abra o arquivo `config.txt` com um editor de texto e altere o que for
necessário. Somente edite à direita do símbolo ":" Salve e feche o arquivo.

5. Acesse o diretório `pyLattes-master` pelo terminal e digite:

```python3 lucyLattes.py```

6. Se tudo ocorreu corretamente, um relatório foi gerado no diretório
`relatório`, basta acessar com um navegador (Chrome ou Firefox).

## Observações

Sempre que editar o arquivo `list_id_name.txt` **APAGUE** todos os
arquivos do diretório `csv_producao`.

## Desenvolvimento

- DONE Capturar os projetos de pesquisa, e extensão, com seus
respectivos participantes, classificação do tipo de projeto (pesquisa ou
extensão) organizando os dados em um `DataFrame`; 
- DONE Capturar produção técnica de cada pesquisador
- DONE Capturar as atividades de orientação;
- DONE Ler o `.xml` direto do `.zip`;
- DONE Realizar um looping para caturar uma série de currículos.
- DONE Capturar produção em periódicos;
- DONE Associar produção em periódico com capes qualis;
- DONE Gerar um arquivo `.csv` com o extrato de produção na pasta relatório;

- TODO Salva em pasta específica arquivos `.csv` individuais para cada pesquisador[80%] 
  - [X] os projetos de pesquisa e extensão;
  - [X] cursos de curta duração;
  - [X] publicações em periódico com qualis, revista;
  - [X] publicações de livros e capítulos;
  - [ ] orientações (tcc, ic, mestrado **FALTA DOUTORADO**);

- TODO Grafo de interação entre pesquisadores [33%]
  - [X] realiza interações somente entre artigos
  - [X] como **observação**, deve-se atentar que os integrantes que não possuem interação(s) não aparecem no grafo.
  - [ ] Verificar as interações nos projetos de pesquisa e extensão;
  - [ ] Calcular o peso das interações dos membros no grafo;
  - [ ] Capturar as atividades dos projetos de extensão;
  - [ ] Gerar um `.json` file para cada currículo;

- DONE Relatório em `.html` [85%]
  - [X] Relação de pesquisadores, cidade, estado, link lattes;
  - [X] Lista de projetos de pesquisa e extensão;
  - [X] Síntese de artigos publicados em periódicos;
  - [X] Gráficos dos periódicos por período e por qualis;
  - [X] Extrato de produção por pesquisador;
  - [X] relação de livros
  - [ ] relação de orientações

## Histórico

## Tue 2019-04-02 10:34:17 -04

- No `scrapper.py` para *ppe* os limites de seleção foram melhorados.

## Tue 2019-04-02 10:34:17 -04

- Insirido no relatório publicação de livros e capítulos (gráficos e
listas). Na produção individual também insirido o número de livros e
capítulos. No resumo da produção foi inserido o número de profissionais
que formam a equipe.

## Sat 2019-03-23 18:24:31 -04

- No relatório, caso tenha ocorrência de pesquisadores que não possuam
interação em periódicos, uma lista com o nome dos mesmos é
adicionada. Melhoria na disposição do grafo, relatório aprimorado.

### Mon 2019-03-18 23:49:11 -04

- Melhorias no relatório com indicação do número total de projetos como
coordenador e integrante.

### Fri 2019-03-15 16:45:33 -04
- Problema no ids que inciavam com o zero foram corrigidos. O relatório
foi melhorado com adicao de link lattes na producao individual, um
extrato do grupo foi adicionado no final. Avisos para PPE e PAPERS sem
ano foram adicionados. Corrigido para resumo gerado automaticamente pelo Lattes.

### Mon 2019-03-11 21:30:46 -04
- No relatório as produções foram enumeradas. Avisos foram inseridos após a finalização dos processos.

### Thu 2019-03-07 21:16:25 -04
- o método de verificação da ordem de autoria do paper foi melhorado, a ordem é obtida direto do lattes.

### Thu 2019-02-28  21:16:25 -04
- relatório está implementado, como produto um arquivo `.html` é gerado. Para verificar a interação entre os integrantes um Grafo é gerado, assumindo somente as interações entre publicações em periódicos. 

### Tue 2019-02-19 21:16:25 -04 
- relatório `.html` foi iniciado, mas não foi implementado na função ainda. 

### Sat 2019-02-16 21:16:25 -04 
- foi inserido uma verificação no scraperlattes, caso o comprimento da
lista seja zero é informado. Há um arquivo `.csv` com o nome completo,
sobrenome, e id do pesquisador. Foi iniciado a análise de dados para o
reatório. 

### Thu 2019-02-14 21:16:25 -04
- foi criado um arquivo `config.txt` com objetivos de:
    - especificar o arquivo `.csv` que será utilizado no qualis.

### Wed 2019-02-13 21:16:25 -04 
- função para capturar os periódicos com qualis foi concluída, os
arquivos `.xml` foram movidos para a pasta `xml_zip`. 

### Tue 2019-02-12 21:16:25 -04
- os arquivos `.xml` são lidos diretamente do arquivo `.zip`. Foi criado
um arquivo **lista** no formato `.csv`, neste arquivo deve conter o
**id** *Lattes* de cada pesquisador e seus respectivo nome. 

### Sat 2019-01-26 21:16:25 -03
- do arquivo `.xml` do lattes é possível extrair o nome do projeto, tipo do
projeto, ano de início, e integrantes, etc 

## Arquivos

- `scraperlattes.py`: contém as funções que extraem as informações
necessárias e geram os `.csv`;
- `readidlist.py`: faz a leitura da lista que contém o **id** dos pesquisadores ;
- `lucyLattes.py`: funciona como o executável;
- `config.txt`: configurações para funcionamento do script;
- `tidydf.py`: organiza os `DataFrame`;
- `report.py`: gerador do relatório;
- `grapho.py`: gerador do gráfico com as interações entre os membros.

## Referências

J. P. Mena-Chalco e R. M. Cesar-Jr. scriptLattes: *An open-source
knowledge extraction system from the Lattes platform*. Journal of the
Brazilian Computer Society, vol. 15, n. 4, páginas 31--39, 2009.

## Autor

- Rafael Tieppo
- rafaeltieppo@yahoo.com.br
- https://rafatieppo.github.io/

