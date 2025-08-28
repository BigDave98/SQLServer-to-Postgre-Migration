from enum import Enum

class DatabaseType(Enum):
    """Tipos de banco de dados suportados."""
    SQL_SERVER = "sql_server"
    POSTGRESQL = "postgresql"