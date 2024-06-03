from abc import ABC, abstractmethod
from sqlalchemy import create_engine, text
import pandas as pd
import logging


class Database(ABC):

    def __init__(self, conn_str):
        self.conn_str = conn_str
        self.engine = create_engine(conn_str)
        self.logger = logging.getLogger(__name__)

    def get_engine(self):
        self.validate_connection()
        return self.engine

    def validate_connection(self):
        try:
            conn = self.engine.connect()
            conn.close()
            self.logger.debug("Connection to database validated")
            return True, self.get_connection_info()
        except Exception as e:
            error_message = str(e)
            self.logger.error(f"Failed to validate connection: {error_message}")
            try:
                self.engine = create_engine(self.conn_str)
                self.logger.debug("Created new engine")
                return True, self.get_connection_info()
            except:
                self.logger.error("Could not create new engine")
                return False, None
    
    def execute_query(self, select_, from_, where_="1=1", limit_=None):
        query = self.format_query(select_, from_, where_, limit_)
        self.logger.debug(f"Executing query: {query}")

        try:
            df = pd.read_sql(query, self.get_engine())
            self.logger.debug(f"Query executed successfully")
            return df, True
        except Exception as e:
            error_message = str(e)
            self.logger.error(f"Failed to execute query: {error_message}")
            return error_message, False
        
    def execute_custom_query(self, query):
        self.logger.debug(f"Executing custom query: {query}")

        try:
            df = pd.read_sql(query, self.get_engine())
            self.logger.debug(f"Query executed successfully")
            return df, True
        except Exception as e:
            error_message = str(e)
            self.logger.error(f"Failed to execute query: {error_message}")
            return error_message, False
        
    @abstractmethod
    def format_query(self, select_, from_, where_="1=1", limit_=None):
        pass

    @abstractmethod
    def get_connection_info(self):
        pass


class OracleDatabase(Database):
    def __init__(self, user, password, host, port, service_name):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.service_name = service_name

        self.conn_str = f"oracle+cx_oracle://{user}:{password}@{host}:{port}/{service_name}"
        super().__init__(self.conn_str)

    def format_query(self, select_, from_, where_="1=1", limit_=None):

        if not where_ or where_.strip() == "":
            where_ = "1=1"

        query = f"SELECT {select_} FROM {from_} WHERE {where_}"
        if limit_ is not None:
            query = query + f" FETCH FIRST {limit_} ROWS ONLY "

        return text(query)
    
    def get_connection_info(self):
        return {
            "username": self.user,
            "hostname": self.host,
            "port": self.port,
            "sid": self.service_name
        }


class PostgresDatabase(Database):
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

        self.conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        super().__init__(self.conn_str)

    def format_query(self, select_, from_, where_="1=1", limit_=None):

        if not where_ or where_.strip() == "":
            where_ = "1=1"

        query = f"SELECT {select_} FROM {from_} WHERE {where_}"
        if limit_ is not None:
            query = query + f" LIMIT {limit_}"

        return text(query)
    
    def get_connection_info(self):
        return {
            "username": self.user,
            "hostname": self.host,
            "port": self.port,
            "database": self.database
        }
        

class MysqlDatabase(Database):
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

        self.conn_str = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
        super().__init__(self.conn_str)

    def format_query(self, select_, from_, where_="1=1", limit_=None):

        if not where_ or where_.strip() == "":
            where_ = "1=1"

        query = f"SELECT {select_} FROM {from_} WHERE {where_}"
        if limit_ is not None:
            query = query + f" LIMIT {limit_}"

        return text(query)
    
    def get_connection_info(self):
        return {
            "username": self.user,
            "hostname": self.host,
            "port": self.port,
            "database": self.database
        }

class DatabaseFactory:
    supported_dbs = {
        "oracle": OracleDatabase,
        "mysql": MysqlDatabase,
        "postgres": PostgresDatabase
    }

    @classmethod
    def get_database(cls, config):
        
        hostname = config.get('REMOTE', 'hostname')
        port = config.get('REMOTE', 'port')
        database = config.get('REMOTE', 'sid')
        username = config.get('REMOTE', 'username')
        password = config.get('REMOTE', 'password')
        db_type = config.get('REMOTE', 'db_type')
        
        if db_type in cls.supported_dbs:
            logging.debug("Connecting to Oracle database")
            return cls.supported_dbs[db_type](username, password, hostname, port, database)
        else:
            logging.error("Chosen database is not supported")
            return None
        
    @classmethod
    def get_supported_dbs(cls):
        return list(cls.supported_dbs.keys())
