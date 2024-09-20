# TRABALHO PRÁTICO 1 - BANCO DE DADOS I (ICC200)
### Contribuidores
-Isabella Almeida Macedo Daniel 22250544 \
-Lucas do Nascimento Silva 22250552


## Objetivo
Objetivo deste trabalho prático é projetar e implementar um banco de dados sobre produtos vendidos em uma loja de comércio eletrônico, incluindo avaliações e comentários de usuários sobre estes produtos. O trabalho consiste na criação de um Banco de Dados Relacional contendo dados sobre compras de produtos e elaboração de um Dashboard, um painel para monitoramento dos dados de compra, gerando uma série de relatórios.


## Ambiente de desenvolvimento

Os códigos fontes foram desenvolvidos em linguagem Python e o SGBD relacional usado foi o PostgreSQL.\
Os scripts Python fazem acesso direto ao SGDB usando comandos SQL.

## Arquivos

**tp1_3.3.py:** Script main, implementado um menu interativo para que o usuário possa escolher as opções desejadas de consulta no banco de dados.

**tp1_3.2.py:** Script main, realiza as extrações dos dados do arquivo, conexão com o SGBD, criação das tabelas do banco e inserção dos dados. Possui as definições de classes de modelos relacionadas às entidades do sistema, como Product, Category, Review e SimilarProducts. Cada classe mapeia as tabelas do banco de dados e possui métodos para converter os dados em tuplas adequadas para inserção no banco. 

**tp1_3.1.PDF:** Arquivo PDF com o esquema, dicionario e diagrama do banco de dados.

**infobase.ini:** Arquivo de configuração que contém as informações de conexão com o SGBD

**db_create.sql:** Arquivo que contém as instruções SQL para criar as tabelas do banco de dados necessárias para o sistema. Ele define as estruturas de dados para entidades como products, categories, reviews, entre outras.


## Arquivo de Entrada

O arquivo de entrada de onde foram extraídos os dados de entrada foi o “[Amazon product co-purchasing network metadata](https://snap.stanford.edu/data/bigdata/amazon/amazon-meta.txt.gz)” que faz parte do Stanford Network Analysis Project (SNAP). Os dados foram coletados em 2006 do site Amazon.com e contém informações sobre produtos e comentários de clientes sobre 548.552 produtos diferentes (livros, CDs de música, DVDs e fitas de vídeo VHS). Para cada produto, a seguinte informação está disponível:

Título\
Posição no ranking de vendas (Salesrank)\
Lista de produtos ``similares’’ (que foram adquiridos junto com o produto)\
Informação de categorização do produto – Categorias e subcategorias ao qual o produto pertence\
Comentários sobre os produtos: Informação data, id do cliente, classificação, número de votos, o número de pessoas que acharam a avaliação útil\

## Scripty do código

Caso não possua o psycopg2 instalado no computador, digite o seguinte comando no terminal
  
```sh
pip install psycopg2-binary==2.9.5
```

Após baixar os arquivos disponibilizados no github, entre no diretorio que foram baixados e execute o script tp1_3.2.py para extração dos metadados e criação e inserção do banco de dados
```sh
python3 tp1_3.2.py
```
O script solicitará o local do arquivo que se encontra os metadados\
ex: /home/NomeUsuario/Downloads/amazon-meta.txt

Espere a extração dos dados e a inserção deles, após terminarem, inicialize o script tp1_3.3 para realizar as consultar conforme o dashboard especificado
```sh
python3 tp1_3.3.py
```
Será apresentado um menu com as opções de consulta


[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zixaop7v)
