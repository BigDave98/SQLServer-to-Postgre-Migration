from typing import Dict, Type
from src.domain.enums.database_type import DatabaseType
from src.domain.interfaces.database_connection import IDatabaseConnection
from src.infrastructure.database.sql_server_connection import SQLServerConn
from src.infrastructure.database.postgre_connection import PostgreConn

class DatabaseConnectionFactory:
    """Factory para criar conexões de banco de dados."""
    
    # Registro de tipos de conexão
    _connection_types: Dict[DatabaseType, Type[IDatabaseConnection]] = {
        DatabaseType.SQL_SERVER: SQLServerConn,
        DatabaseType.POSTGRESQL: PostgreConn
    }
    
    @classmethod
    def create(cls, db_type: str, uri: str) -> IDatabaseConnection:
        try:
            # Converter string para enum
            database_type = DatabaseType(db_type.lower())
        except ValueError:
            supported_types = [t.value for t in DatabaseType]
            raise ValueError(
                f"Tipo de banco '{db_type}' não suportado. "
                f"Tipos válidos: {supported_types}"
            )
        
        # Obter a classe de conexão
        connection_class = cls._connection_types.get(database_type)
        
        if not connection_class:
            raise ValueError(f"Implementação para {db_type} não encontrada")
        
        # Criar e retornar a instância
        return connection_class(uri)
    
    @classmethod
    def create_from_config(cls, db_type: str) -> IDatabaseConnection:
        from src.config.settings import Config
        
        uri_mapping = {
            DatabaseType.SQL_SERVER.value: Config.SQL_SERVER_URI,
            DatabaseType.POSTGRESQL.value: Config.POSTGRES_URI
        }
        
        uri = uri_mapping.get(db_type.lower())
        
        if not uri:
            raise ValueError(f"URI não configurada para {db_type}")
        
        return cls.create(db_type, uri)