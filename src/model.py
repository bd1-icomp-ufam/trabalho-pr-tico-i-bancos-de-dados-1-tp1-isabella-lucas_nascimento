# Classe base para entidades do modelo
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
