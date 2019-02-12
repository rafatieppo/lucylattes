# LATTES_SCRAPER

## Motivação


## O que faz

Organiza os dados dos currículos da plataforma *Lattes* em arquivos de
texto organizados que proporcionam rapidez para a geração de
informação. 

## Desenvolvimento

- [X ] Salva em arquivos `.csv` os projetos de pesquisa e extensão de
cada pesquisador em arquivos individuais. Para cada tipo de produção foi
criado uma pasta específica.
- [X] Capturar os projetos de pesquisa, e extensão, com seus respectivos
participantes, classificação do tipo de projeto (pesquisa ou extensão)
organizando os dados em um `DataFrame`; 
- [X] Capturar produção técnica de cada pesquisador
- [X] Capturar as atividades de orientação;
- [ ] Capturar produção em periódicos;
- [ ] Associar produção em periódico com capes qualis;
- [ ] Capturar as atividades dos projetos de extensão;
- [ ] Ler o `.xml` direto do `.zip`;
- [ ] Gerar um `.json` file para cada currículo;
- [ ] Realizar um looping para caturar uma série de currículos.

## Histórico

- 20190212: os arquivos `.xlm` são lidos diretamente do arquivo
`.zip`. Foi criado um arquivo **lista** no formato `.csv`, neste arquivo
deve conter o **id** *Lattes* de cada pesquisador e seus respectivo nome.

- 20190126: do arquivo xlm do lattes é possível extrair o nome do
projeto, tipo do projeto, ano de início, e integrantes, etc

## Arquivos

- `parserlattes.py`: contém as funções que extraem as informações
necessárias e geram os `.csv`
- `readidlist.py`: faz a leitura da lista que contém o **id** dos pesquisadores 
- `scriptLattes.py`: funciona como o executável

## Autor

- Rafael Tieppo
- rafaeltieppo@yahoo.com.br
- https://rafatieppo.github.io/



