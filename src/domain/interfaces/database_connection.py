from abc import ABC, abstractmethod
from sqlalchemy import Engine, MetaData

class IDatabaseConnection(ABC):
    """Interface para conexões de banco de dados."""
    
    @abstractmethod
    def get_engine(self) -> Engine:
        """Retorna a engine do SQLAlchemy."""
        pass
    
    @abstractmethod
    def get_metadata(self) -> MetaData:
        """Retorna os metadados do banco."""
        pass
    
    @abstractmethod
    def dispose(self) -> None:
        """Fecha a conexão e limpa recursos."""
        pass