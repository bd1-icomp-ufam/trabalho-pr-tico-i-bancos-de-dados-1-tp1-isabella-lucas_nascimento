from configparser import ConfigParser
import psycopg2
import os

# Classe que gerencia a conexão e a criação do banco de dados
class DatabaseManager:

    # Constantes para o nome do banco de dados e tipo de SGBD (PostgreSQL)
    POSTGRESQL_DB = 'postgresql'
    DATABASE_NAME = 'amazon'
    __db_config_filename = 'infobase.ini'  # Arquivo de configuração do banco de dados
    __connection = None  # Conexão com o banco de dados

    @classmethod
    def __get_connection_params(cls, sgbd_name: str):
        """
        Obtém os parâmetros de conexão do arquivo de configuração (.ini).
        :param sgbd_name: Nome do SGBD para o qual queremos os parâmetros de conexão
        :return: Dicionário com os parâmetros de conexão
        """
        # Verifica se o arquivo de configuração existe
        if os.path.exists(DatabaseManager.__db_config_filename):
            parser = ConfigParser()  # Parser para ler o arquivo de configuração
            parser.read(DatabaseManager.__db_config_filename)  # Lê o arquivo de configuração
            # Verifica se o arquivo contém a seção do SGBD solicitado
            if parser.has_section(sgbd_name):
                params = parser.items(sgbd_name)  # Obtém os parâmetros da seção
                db = dict(params)  # Converte os parâmetros em um dicionário
                return db  # Retorna os parâmetros de conexão
            else:
                raise Exception(f'Section {sgbd_name} not found in the {DatabaseManager.__db_config_filename} file')
        else:
            raise FileNotFoundError(f'O arquivo {DatabaseManager.__db_config_filename} de configurações para o SGBD {sgbd_name} não foi encontrado!')

    @classmethod
    def get_connection(cls, sgbd_name: str):
        """
        Obtém a conexão com o banco de dados. Se já existir uma conexão, a reutiliza.
        :param sgbd_name: Nome do SGBD para o qual queremos a conexão
        :return: Conexão com o banco de dados
        """
        # Verifica se a conexão não existe ou se está fechada
        if not DatabaseManager.__connection or DatabaseManager.__connection.closed:
            # Estabelece uma nova conexão com base nos parâmetros obtidos
            DatabaseManager.__connection = psycopg2.connect(**DatabaseManager.__get_connection_params(sgbd_name))
        return DatabaseManager.__connection

    @classmethod
    def close_connection(cls):
        """
        Fecha a conexão com o banco de dados, se ela estiver aberta.
        """
        if DatabaseManager.__connection and not DatabaseManager.__connection.closed:
            DatabaseManager.__connection.close()  # Fecha a conexão

    @classmethod
    def database_create(cls, sgbd_name: str):
        """
        Cria o banco de dados e executa os scripts SQL iniciais para a criação das tabelas.
        :param sgbd_name: Nome do SGBD onde o banco será criado
        """
        # Obtém os parâmetros de conexão, mas substitui o nome do banco para 'postgres'
        db_params = DatabaseManager.__get_connection_params(sgbd_name)
        db_params['database'] = 'postgres'
        # Conecta-se ao banco de dados 'postgres' para criar o novo banco de dados
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True  # Habilita o modo de autocommit
        cursor = conn.cursor()
        # Executa o comando SQL para criar o banco de dados
        cursor.execute(f"CREATE DATABASE {sgbd_name}")
        conn.close()  # Fecha a conexão com o banco de dados 'postgres'
        
        # Lê o script SQL para criação de tabelas
        with open('db_create.sql', 'r') as db_file:
            sql = ''.join(db_file.readlines())  # Concatena as linhas do arquivo SQL
            conn = DatabaseManager.get_connection(sgbd_name)  # Obtém a conexão com o novo banco
            cursor = conn.cursor()
            cursor.execute(sql)  # Executa o script SQL
            cursor.close()  # Fecha o cursor
            conn.commit()  # Confirma as mudanças no banco de dados
            conn.close()  # Fecha a conexão com o banco