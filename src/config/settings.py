import os
from dotenv import load_dotenv
from sqlalchemy import (
    Integer, String,Text, Boolean, Numeric, Float
)
from sqlalchemy.dialects.postgresql import BYTEA, TIMESTAMP

load_dotenv()

class Config:
    # SQL Server
    SQL_SERVER_URI = (
        f"mssql+pyodbc://{os.getenv('SQL_SERVER_USER')}:{os.getenv('SQL_SERVER_PASSWORD')}"
        f"@{os.getenv('SQL_SERVER_HOST')}:{os.getenv('SQL_SERVER_PORT')}"
        f"/{os.getenv('SQL_SERVER_DATABASE')}"
        f"?driver={os.getenv('SQL_SERVER_DRIVER')}"
        f"&charset=utf8"
        f"&ansi=true"
    )
    
    # PostgreSQL
    POSTGRES_URI = (
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DATABASE')}?client_encoding=utf8"
    )
    
    # Migration Settings
    BATCH_SIZE = int(os.getenv('MIGRATION_BATCH_SIZE', 10000))
    
    @staticmethod
    def get_sql_server_config():
        return {
            'host': os.getenv('SQL_SERVER_HOST'),
            'port': os.getenv('SQL_SERVER_PORT'),
            'database': os.getenv('SQL_SERVER_DATABASE'),
            'user': os.getenv('SQL_SERVER_USER'),
            'password': os.getenv('SQL_SERVER_PASSWORD'),
            'driver': os.getenv('SQL_SERVER_DRIVER')
        }
    
    @staticmethod
    def get_postgres_config():
        return {
            'host': os.getenv('POSTGRES_HOST'),
            'port': os.getenv('POSTGRES_PORT'),
            'database': os.getenv('POSTGRES_DATABASE'),
            'user': os.getenv('POSTGRES_USER'),
            'password': os.getenv('POSTGRES_PASSWORD')
        }
    
# Mapeamento 
TYPE_MAPPING = {
    'INTEGER': Integer,
    'DATETIME': TIMESTAMP(),
    'VARCHAR': String,
    'VARBINARY': BYTEA(), 
    'CHAR': String,
    'TEXT': Text,
    'BIT': Boolean,
    'FLOAT': Float,
    'NUMERIC': Numeric,
    'DECIMAL': Numeric,
}