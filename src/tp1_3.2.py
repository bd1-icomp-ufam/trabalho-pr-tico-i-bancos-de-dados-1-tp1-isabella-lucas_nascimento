# TRABALHO 1 BANCO DE DADOS
# ISABELLA ALMEIDA MACEDO DANIEL - 22250544
# LUCAS DO NASCIMENTO SILVA - 22250552

# Importando as classes de controle de dados e banco de dados
from controller import DatasetController, ProductController, CategoryController, ProductCategoryController, SimilarProductsController, ReviewController
from infobase import DatabaseManager
from datetime import datetime

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