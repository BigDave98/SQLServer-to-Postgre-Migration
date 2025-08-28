from abc import abstractmethod
from typing import List, Dict, Any
from sqlalchemy import Table
from src.domain.interfaces.repository import IRepository

class ITargetRepository(IRepository):
    """Interface para repositórios de destino (escrita)."""
    
    @abstractmethod
    def create_table(self, table: Table) -> bool:
        """Cria uma tabela no banco de destino."""
        pass
    
    @abstractmethod
    def insert_batch(self, table: Table, data: List[Dict[str, Any]]) -> bool:
        """Insere um lote de dados."""
        pass
    
    @abstractmethod
    def truncate_table(self, table_name: str) -> bool:
        """Limpa todos os dados de uma tabela."""
        pass
    
    @abstractmethod
    def disable_constraints(self) -> None:
        """Desabilita constraints temporariamente."""
        pass
    
    @abstractmethod
    def enable_constraints(self) -> None:
        """Habilita constraints."""
        pass