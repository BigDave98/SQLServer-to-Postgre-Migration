from abc import ABC, abstractmethod
from sqlalchemy import Table

class IRepository(ABC):
    """Interface base para repositórios."""
    
    @abstractmethod
    def get_table_metadata(self, table_name: str) -> Table:
        """Obtém os metadados de uma tabela."""
        pass
    
    @abstractmethod
    def count_records(self, table: Table) -> int:
        """Conta o número de registros em uma tabela."""
        pass
    
    @abstractmethod
    def table_exists(self, table_name: str) -> bool:
        """Verifica se uma tabela existe."""
        pass