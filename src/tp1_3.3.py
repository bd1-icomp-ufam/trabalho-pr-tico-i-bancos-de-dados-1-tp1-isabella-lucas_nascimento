# TRABALHO 1 BANCO DE DADOS
# ISABELLA ALMEIDA MACEDO DANIEL - 22250544
# LUCAS DO NASCIMENTO SILVA - 22250552

# Importando classes e funções necessárias
from typing import Iterable, Any
from infobase import DatabaseManager

# Definições das consultas SQL que serão usadas
LISTAR_5_SQL = """((SELECT product.id_product, product.asin, review.id_customer, review.review_date, review.rating, review.helpful 
                    FROM product, review 
                    WHERE product.id_product=%s 
                    ORDER BY rating DESC, helpful DESC LIMIT 5) 
                   UNION ALL 
                   (SELECT product.id_product, product.asin, review.id_customer, review.review_date, review.rating, review.helpful 
                    FROM product, review 
                    WHERE product.id_product=%s 
                    ORDER BY rating ASC, helpful DESC LIMIT 5))"""

LISTAR_SIMILARES_SQL = """SELECT product.title, product.salesrank, psimilar.title, psimilar.salesrank 
                          FROM product 
                          JOIN similar_products ON product.asin=similar_products.product_asin 
                          JOIN product as psimilar ON psimilar.asin=similar_products.similar_asin 
                          WHERE product.id_product=%s AND psimilar.salesrank>product.salesrank"""

LISTAR_EVOLUCAO_SQL = """SELECT product.title, review.review_date, round(avg(review.rating), 2) 
                         FROM product 
                         INNER JOIN review ON product.id_product=review.id_product 
                         WHERE product.id_product=%s 
                         GROUP BY product.title, review.review_date 
                         ORDER BY review_date ASC"""

LISTAR_MAIS_VENDIDOS_SQL = """SELECT title, salesrank, product_group 
                              FROM (SELECT title, salesrank, product_group, Rank() over (Partition BY product_group ORDER BY salesrank DESC ) AS Rank 
                                    FROM product WHERE salesrank > 0) rs 
                              WHERE Rank <= 10"""

LISTAR_PRODUTOS_SQL = """SELECT t2.id_product, t2.title, t2.product_group, t2.avg_helpful, t2.n_rank 
                         FROM (SELECT product.id_product, product.title, product.product_group, t1.avg_helpful, 
                                      ROW_NUMBER() OVER (PARTITION BY product.product_group ORDER BY t1.avg_helpful DESC) AS n_rank 
                               FROM product 
                               JOIN (SELECT review.id_product, round(avg(review.helpful), 2) AS avg_helpful 
                                     FROM review WHERE review.helpful > 0 
                                     GROUP BY review.id_product) t1 ON t1.id_product=product.id_product) as t2 
                         WHERE n_rank <= 10"""

LISTAR_CATEGORIAS_SQL = """SELECT category.name, round(t_avg.avg, 2) 
                           FROM category 
                           INNER JOIN (SELECT product_category.id_category, avg(qtd_pos.count) 
                                       FROM product_category 
                                       INNER JOIN (SELECT review.id_product, count(*) 
                                                   FROM review WHERE review.helpful > 0 
                                                   GROUP BY review.id_product) qtd_pos 
                                       ON qtd_pos.id_product = product_category.id_product 
                                       GROUP BY product_category.id_category 
                                       HAVING avg(qtd_pos.count) > 0 
                                       ORDER BY avg DESC LIMIT 5) t_avg 
                           ON category.id_category = t_avg.id_category"""

LISTAR_CLIENTES_SQL = """SELECT id_customer, n_reviews, review_rank, product_group 
                         FROM (SELECT id_customer, n_reviews, product_group, 
                                      ROW_NUMBER() OVER (PARTITION BY t1.product_group ORDER BY t1.n_reviews DESC) AS review_rank 
                               FROM (SELECT id_customer, count(id_customer) AS n_reviews, product_group 
                                     FROM product 
                                     INNER JOIN review ON product.id_product=review.id_product 
                                     GROUP BY (product_group, id_customer)) AS t1 
                               ORDER BY t1.product_group ASC, t1.n_reviews DESC) AS t2 
                         WHERE review_rank <= 10"""


# Função para imprimir os resultados da consulta formatados
def print_info(header: Iterable[str], cols_size: Iterable[int], info: Iterable[Iterable[Any]]):
    """
    Função para imprimir informações tabulares de forma organizada.
    :param header: Títulos das colunas
    :param cols_size: Tamanho de cada coluna
    :param info: Dados a serem exibidos
    """
    print('-' * sum(cols_size))  # Linha de separação superior
    for col_name, col_size in zip(header, cols_size):
        print(f'{col_name.ljust(col_size)}', end='')  # Cabeçalho
    print('\n' + '-' * sum(cols_size))  # Linha de separação entre cabeçalho e dados
    for row in info:
        for value, col_size in zip(row, cols_size):
            print(f'{str(value).ljust(col_size)}', end='')  # Dados de cada linha
        print('')  # Nova linha após cada linha de dados
    print('-' * sum(cols_size))  # Linha de separação inferior
    print('')


# Função para executar uma query SQL no banco de dados
def executar_query(sql_query: str, params: Iterable = None) -> Iterable:
    """
    Executa uma consulta SQL no banco de dados e retorna os resultados.
    :param sql_query: A consulta SQL a ser executada
    :param params: Parâmetros opcionais para a consulta
    :return: Resultados da consulta
    """
    conn = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)  # Obter a conexão
    cursor = conn.cursor()  # Criar o cursor para executar a consulta
    cursor.execute(sql_query, params)  # Executar a consulta com parâmetros
    return cursor.fetchall()  # Retornar os resultados


# Funções específicas para cada tipo de listagem

# Listar os 5 comentários mais úteis com maior e menor avaliação
def listar_5():
    id = input('Insira o Id do produto: ')  # Solicita o ID do produto
    rows = executar_query(LISTAR_5_SQL, (id, id))  # Executa a consulta
    print_info(['ID', 'ASIN', 'CUSTOMER ID', 'REVIEW DATE', 'RATING', 'HELPFUL'], [8, 15, 18, 13, 10, 5], rows)  # Exibe os resultados

# Listar produtos similares com maior vendas
def listar_similares():
    id = input('Insira o Id do produto: ')  # Solicita o ID do produto
    rows = executar_query(LISTAR_SIMILARES_SQL, (id, ))  # Executa a consulta
    print_info(['TITULO PRODUTO', 'SALESRANK', 'TITULO SIMILAR', 'SALESRANK'], [80, 12, 80, 12], rows)  # Exibe os resultados

# Mostrar evolução diária das avaliações de um produto
def listar_evolucao():
    """Esta função exibe a evolução diária das médias de avaliação de um produto."""
    id = input('Insira o Id do produto: ')  # Solicita o ID do produto
    rows = executar_query(LISTAR_EVOLUCAO_SQL, (id, ))  # Executa a consulta
    print_info(['TITULO', 'DATA', 'MÉDIA DE AVALIAÇÕES'], [150, 14, 10], rows)  # Exibe os resultados

# Listar os 10 produtos mais vendidos em cada grupo de produtos
def listar_mvendidos():
    rows = executar_query(LISTAR_MAIS_VENDIDOS_SQL)  # Executa a consulta
    print_info(['TITULO', 'RANK VENDAS', 'GRUPO'], [150, 15, 13], rows)  # Exibe os resultados

# Listar os 10 produtos com a maior média de avaliações úteis positivas por grupo de produtos
def listar_avaliacoes_produtos():
    rows = executar_query(LISTAR_PRODUTOS_SQL)  # Executa a consulta
    print_info(['ID PRODUTO', 'TITULO', 'GRUPO', 'MEDIA AV', 'RANK'], [12, 150, 15, 12, 5], rows)  # Exibe os resultados

# Listar as 5 categorias com maior média de avaliações úteis positivas
def listar_avaliacoes_categorias():
    rows = executar_query(LISTAR_CATEGORIAS_SQL)  # Executa a consulta
    print_info(['NOME CATEGORIA', 'MEDIA AV'], [50, 12], rows)  # Exibe os resultados

# Listar os 10 clientes que mais comentaram por grupo de produtos
def listar_clientes():
    rows = executar_query(LISTAR_CLIENTES_SQL)  # Executa a consulta
    print_info(['ID CLIENTE', 'N COMENTARIOS', 'RANK', 'GRUPO'], [16, 18, 10, 15], rows)  # Exibe os resultados


# Função principal que exibe o menu e chama as funções com base na escolha do usuário
def exibir_menu():
    print("\nSelecione uma opção:")
    print("1 - Listar os 5 comentários mais úteis com maior avaliação e menor avaliação")
    print("2 - Listar os produtos similares com maior venda")
    print("3 - Mostrar a evolução diária das médias de avaliação")
    print("4 - Listar os 10 produtos mais vendidos em cada grupo de produtos")
    print("5 - Listar os 10 produtos com a maior média de avaliações úteis positivas por produto")
    print("6 - Listar as 5 categorias de produto com a maior média de avaliações úteis positivas por produto")
    print("7 - Listar os 10 clientes que mais fizeram comentários por grupo de produto")
    print("0 - SAIR\n")

def processar_opcao(opcao):
    match opcao:
        case 1:
            listar_5()
        case 2:
            listar_similares()
        case 3:
            listar_evolucao()
        case 4:
            listar_mvendidos()
        case 5:
            listar_avaliacoes_produtos()
        case 6:
            listar_avaliacoes_categorias()
        case 7:
            listar_clientes()
        case 0:
            print("Saindo do sistema...")
        case _:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    opcao = -1
    while opcao != 0:
        exibir_menu()
        try:
            opcao = int(input('Digite uma das opções: ').strip())
            processar_opcao(opcao)
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")
