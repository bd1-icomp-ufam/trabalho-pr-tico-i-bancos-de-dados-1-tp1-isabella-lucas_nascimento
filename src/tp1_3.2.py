# TRABALHO 1 BANCO DE DADOS
# ISABELLA ALMEIDA MACEDO DANIEL - 22250544
# LUCAS DO NASCIMENTO SILVA - 22250552

# Importando as classes de controle de dados e banco de dados
from infobase import DatabaseManager
from datetime import datetime
from typing import List
from psycopg2 import extras
from infobase import DatabaseManager
import re

class Model:

    # Converte o objeto em uma tupla de seus atributos
    def to_tuple(self):
        pass

    # Retorna uma lista de atributos do modelo
    @staticmethod
    def attr_list():
        pass


# Classe representando um produto
class Product(Model):

    def __init__(self, id_product: int, asin: str, title: str = None, product_group: str = None, salesrank: int = None, review_total: int = None, review_downloaded: int = None, review_avg: float = None):
        """
        Inicializa um objeto Product com os dados fornecidos, incluindo id, ASIN, título, grupo de produto, rank de vendas,
        contadores de reviews, etc.
        """
        self.id_product = id_product
        self.asin = asin
        self.title = title
        self.product_group = product_group
        self.salesrank = salesrank
        self.review_total = review_total
        self.review_downloaded = review_downloaded
        self.review_avg = review_avg

    # Converte o objeto Product para uma tupla de seus valores
    def to_tuple(self):
        values = []
        for attr in self.attr_list():
            values.append(getattr(self, attr))
        return tuple(values)

    # Retorna uma lista de atributos da classe Product
    @staticmethod
    def attr_list():
        return list(Product(-1, "").__dict__)[:]

    # Retorna uma string representando o objeto Product e seus atributos
    def __str__(self):
        list_str = [f'{self.__class__.__name__}']
        for attr in self.attr_list():
            list_str.append(f'{attr}: {getattr(self, attr)}')
        return '\n'.join(list_str)


# Classe representando a relação entre Produto e Categoria
class ProductCategory(Model):

    def __init__(self, id_product: id, id_category: int):
        """
        Inicializa um objeto ProductCategory representando a associação entre um produto e uma categoria.
        """
        self.id_product = id_product
        self.id_category = id_category

    # Converte o objeto ProductCategory para uma tupla de seus valores
    def to_tuple(self):
        values = []
        for attr in self.attr_list():
            values.append(getattr(self, attr))
        return tuple(values)

    # Retorna uma lista de atributos da classe ProductCategory
    @staticmethod
    def attr_list():
        return list(ProductCategory(-1, -1).__dict__)[:]

    # Retorna uma string representando o objeto ProductCategory e seus atributos
    def __str__(self):
        list_str = [f'{self.__class__.__name__}']
        for attr in self.attr_list():
            list_str.append(f'{attr}: {getattr(self, attr)}')
        return '\n'.join(list_str)


# Classe representando uma Categoria de produtos
class Category(Model):

    def __init__(self, id_category: int, name: str, id_parent: int = None):
        """
        Inicializa um objeto Category com o id da categoria, nome e opcionalmente um id de categoria pai.
        """
        self.id_category = id_category
        self.name = name
        self.id_parent = id_parent

    # Converte o objeto Category para uma tupla de seus valores
    def to_tuple(self):
        values = []
        for attr in self.attr_list():
            values.append(getattr(self, attr))
        return tuple(values)

    # Retorna uma lista de atributos da classe Category
    @staticmethod
    def attr_list():
        return list(Category(-1, "").__dict__)[:]

    # Retorna uma string representando o objeto Category e seus atributos
    def __str__(self):
        list_str = [f'{self.__class__.__name__}']
        for attr in self.attr_list():
            list_str.append(f'{attr}: {getattr(self, attr)}')
        return '\n'.join(list_str)


# Classe representando uma Review de produto
class Review(Model):

    def __init__(self, id_product: int, id_customer: str, review_date: str, rating=None, votes=None, helpful=None):
        """
        Inicializa um objeto Review com informações de produto, cliente, data, e dados de avaliação.
        """
        self.id_product = id_product
        self.id_customer = id_customer
        self.review_date = review_date
        self.rating = rating
        self.votes = votes
        self.helpful = helpful

    # Converte o objeto Review para uma tupla de seus valores
    def to_tuple(self):
        values = []
        for attr in self.attr_list():
            values.append(getattr(self, attr))
        return tuple(values)

    # Retorna uma lista de atributos da classe Review
    @staticmethod
    def attr_list():
        return list(Review(-1, "", "").__dict__)[:]

    # Retorna uma string representando o objeto Review e seus atributos
    def __str__(self):
        list_str = [f'{self.__class__.__name__}']
        for attr in self.attr_list():
            list_str.append(f'{attr}: {getattr(self, attr)}')
        return '\n'.join(list_str)


# Classe representando produtos similares
class SimilarProducts(Model):

    def __init__(self, product_asin: str, similar_asin: str):
        """
        Inicializa um objeto SimilarProducts que representa a relação de produtos similares com base no ASIN.
        """
        self.product_asin = product_asin
        self.similar_asin = similar_asin

    # Converte o objeto SimilarProducts para uma tupla de seus valores
    def to_tuple(self):
        values = []
        for attr in self.attr_list():
            values.append(getattr(self, attr))
        return tuple(values)

    # Retorna uma lista de atributos da classe SimilarProducts
    @staticmethod
    def attr_list():
        return list(SimilarProducts("", "").__dict__)[:]

    # Retorna uma string representando o objeto SimilarProducts e seus atributos
    def __str__(self):
        list_str = [f'{self.__class__.__name__}']
        for attr in self.attr_list():
            list_str.append(f'{attr}: {getattr(self, attr)}')
        return '\n'.join(list_str)


class DatasetController:
    # Expressões regulares para capturar categorias, reviews e análises
    categoria_regex = re.compile(r'(.*)\[(\d+)\]')
    review_regex = re.compile(r'reviews:\s+total:\s+(\d+)\s+downloaded:\s+(\d+)\s+avg\srating:\s+([\d.]+)')
    analise_regex = re.compile(
        r'(\d{4}-\d{1,2}-\d{1,2})\s+cutomer:\s+([A-Z0-9]+)\s+rating:\s+(\d+)\s+votes:\s+(\d+)\s+helpful:\s+(\d+)')

    @staticmethod
    def extract_data(path: str):
        # Primeira passagem para contar o número total de produtos
        total_products = 0
        with open(path, 'r', encoding="utf8") as arquivo:
            for _ in range(3):
                next(arquivo)
            for line in arquivo:
                if line.strip() == '':
                    total_products += 1
        print(f"Total de produtos a serem processados: {total_products}")

        # Inicializa as listas de dados
        list_products, list_categories = [], {}
        list_prod_cat, list_similars, list_reviews = [], [], []

        # Variáveis para rastrear o progresso
        processed_products = 0
        progress_percentage = 0

        with open(path, 'r', encoding="utf8") as arquivo:
            for _ in range(3):
                next(arquivo)

            section = []
            for line in arquivo:
                if line.strip():
                    section.append(line)
                else:
                    result = DatasetController.__parse_section(section)
                    if result:
                        produto, categorias, prod_cat, similares, reviews = result
                        list_products.append(produto)
                        list_categories.update(categorias)
                        list_prod_cat.extend(prod_cat)
                        list_similars.extend(similares)
                        list_reviews.extend(reviews)

                        processed_products += 1
                        # Calcula a porcentagem concluída
                        new_percentage = int((processed_products / total_products) * 100)
                        if new_percentage > progress_percentage:
                            progress_percentage = new_percentage
                            print(f"Progresso: {progress_percentage}% concluído.")
                    section = []

            # Processa a última seção se o arquivo não terminar com uma linha em branco
            if section:
                result = DatasetController.__parse_section(section)
                if result:
                    produto, categorias, prod_cat, similares, reviews = result
                    list_products.append(produto)
                    list_categories.update(categorias)
                    list_prod_cat.extend(prod_cat)
                    list_similars.extend(similares)
                    list_reviews.extend(reviews)

                    processed_products += 1
                    # Atualiza a porcentagem para 100% no final
                    progress_percentage = 100
                    print(f"Progresso: {progress_percentage}% concluído.")

        print("Extração de dados concluída.")
        return list_products, list_categories, list_prod_cat, list_similars, list_reviews

    @staticmethod
    def __parse_section(section: List[str]):
        if not section:
            return None

        # Inicializa as listas para armazenar dados
        list_similars, list_reviews, list_prod_cat = [], [], []
        list_categories = {}

        # Extrai o ID do produto e o ASIN
        produto_id = int(section[0][3:].strip())
        asin = section[1][5:].strip().upper()
        produto_obj = Product(produto_id, asin)

        index = 2  # Índice atual na seção

        # Verifica se há título do produto
        if index < len(section) and section[index].startswith('  title:'):
            produto_obj.title = section[index][8:].strip().upper()
            index += 1
        else:
            produto_obj.title = ''

        # Verifica se há grupo do produto
        if index < len(section) and section[index].startswith('  group:'):
            produto_obj.product_group = section[index][8:].strip().upper()
            index += 1
        else:
            produto_obj.product_group = ''

        # Verifica se há salesrank
        if index < len(section) and section[index].startswith('  salesrank:'):
            try:
                produto_obj.salesrank = int(section[index][12:].strip())
            except ValueError:
                produto_obj.salesrank = None
            index += 1
        else:
            produto_obj.salesrank = None

        # Verifica se há produtos similares
        if index < len(section) and section[index].startswith('  similar:'):
            similares_info = section[index][11:].strip().split()
            n_similares = int(similares_info[0])
            if n_similares > 0 and len(similares_info) > 1:
                for asin_similar in similares_info[1:]:
                    similar_obj = SimilarProducts(produto_obj.asin, asin_similar)
                    list_similars.append(similar_obj)
            index += 1

        # Verifica se há categorias
        if index < len(section) and section[index].startswith('  categories:'):
            try:
                n_categories = int(section[index][14:].strip())
            except ValueError:
                n_categories = 0
            index += 1
            for _ in range(n_categories):
                if index < len(section):
                    cat_line = section[index].strip()
                    cat_father_code = None
                    categories_info = []
                    for x in cat_line.split('|'):
                        match = DatasetController.categoria_regex.match(x.strip())
                        if match:
                            cat_name, cat_id = match.groups()
                            cat_id = int(cat_id)
                        else:
                            # Se não corresponder, usa o nome como está e define um ID único negativo
                            cat_name = x.strip().upper()
                            cat_id = -hash(cat_name)  # ID negativo baseado no hash do nome
                        cat_obj = Category(cat_id, cat_name, cat_father_code)
                        list_categories[cat_id] = cat_obj
                        cat_father_code = cat_id
                    list_prod_cat.append(ProductCategory(produto_obj.id_product, cat_father_code))
                    index += 1
                else:
                    break

        # Verifica se há informações de reviews
        if index < len(section) and 'reviews:' in section[index]:
            review_match = DatasetController.review_regex.search(section[index])
            if review_match:
                total, downloaded, avg_rating = review_match.groups()
                produto_obj.review_total = int(total)
                produto_obj.review_downloaded = int(downloaded)
                produto_obj.review_avg = float(avg_rating)
            index += 1

            # Processa cada review individual
            while index < len(section):
                review_match = DatasetController.analise_regex.search(section[index])
                if review_match:
                    date, customer_id, rating, votes, helpful = review_match.groups()
                    review_obj = Review(produto_obj.id_product, customer_id, date)
                    review_obj.rating = int(rating)
                    review_obj.votes = int(votes)
                    review_obj.helpful = int(helpful)
                    list_reviews.append(review_obj)
                index += 1

        return produto_obj, list_categories, list_prod_cat, list_similars, list_reviews


# Classe responsável pelo controle de operações de banco de dados
class ModelController:

    @classmethod
    def _inserir(cls, rows, tab_name: str, attr_list):
        attr_names = ','.join(attr_list)
        sql_query = f'INSERT INTO {tab_name} ({attr_names}) VALUES %s'
        connection = DatabaseManager.get_connection(DatabaseManager.POSTGRESQL_DB)
        cursor = connection.cursor()
        extras.execute_values(cursor, sql_query, rows)
        connection.commit()
        return cursor.rowcount


# Controlador para o modelo de produto
class ProductController(ModelController):
    TAB_NAME = 'product'

    @classmethod
    def inserir(cls, elements: List[Product]):
        return ModelController._inserir([x.to_tuple() for x in elements], cls.TAB_NAME, Product.attr_list())


# Controlador para o relacionamento Produto e Categoria
class ProductCategoryController(ModelController):
    TAB_NAME = 'product_category'

    @classmethod
    def inserir(cls, elements: List[ProductCategory]):
        return ModelController._inserir([x.to_tuple() for x in elements], cls.TAB_NAME, ProductCategory.attr_list())


# Controlador para a entidade Categoria
class CategoryController(ModelController):
    TAB_NAME = 'category'

    @classmethod
    def inserir(cls, elements: List[Category]):
        return ModelController._inserir([x.to_tuple() for x in elements], cls.TAB_NAME, Category.attr_list())



# Controlador para a entidade Review
class ReviewController(ModelController):
    TAB_NAME = 'review'

    @classmethod
    def inserir(cls, elements: List[Review]):
        return ModelController._inserir([x.to_tuple() for x in elements], cls.TAB_NAME, Review.attr_list())


# Controlador para a entidade SimilarProducts
class SimilarProductsController(ModelController):
    TAB_NAME = 'similar_products'

    @classmethod
    def inserir(cls, elements: List[SimilarProducts]):
        return ModelController._inserir([x.to_tuple() for x in elements], cls.TAB_NAME, SimilarProducts.attr_list())



# Ponto de entrada do script
if __name__ == '__main__':
    # Marcando o início do tempo de execução para medir a performance
    start_time = datetime.now()
    
    # Criando o banco de dados com o nome definido no DatabaseManager
    DatabaseManager.database_create(DatabaseManager.DATABASE_NAME)
    
    infoset_path = input('Informe o local do arquivo: ')
    
    # Extraindo os dados do arquivo de metadados usando a classe DatasetController
    products, categories, prod_cats, similars, reviews = DatasetController().extract_data(infoset_path)
    ProductController.inserir(products)
    print(f'{len(products)} Product inserido no DataBase')
    CategoryController.inserir(categories.values())
    print(f'{len(categories.values())} Category inserido no DataBase')
    ProductCategoryController.inserir(prod_cats)
    print(f'{len(prod_cats)} Product_Category inserido no DataBase')
    SimilarProductsController.inserir(similars)
    print(f'{len(similars)} Similar_products inserido no Database')
    ReviewController.inserir(reviews)
    print(f'{len(reviews)} Review inserido no DataBase')
    
    # Fechando a conexão com o banco de dados após a inserção dos dados
    DatabaseManager.close_connection()
    
    # Calculando e exibindo o tempo total de execução do script
    print(f'Tempo: {datetime.now() - start_time}')