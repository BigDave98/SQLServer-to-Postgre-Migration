from abc import abstractmethod
from typing import List, Dict, Any
from sqlalchemy import Table
from src.domain.interfaces.repository import IRepository

class ISourceRepository(IRepository):
    """Interface para repositórios de origem (leitura)."""
    
    @abstractmethod
    def get_all_tables_metadata(self) -> Dict[str, Table]:
        """Obtém metadados de todas as tabelas."""
        pass
    
    @abstractmethod
    def get_tables_in_order(self) -> List[str]:
        """Obtém lista de tabelas ordenadas por dependências."""
        pass
    
    @abstractmethod
    def fetch_batch(
        self, 
        table: Table, 
        order_column: str, 
        batch_size: int, 
        offset: int
    ) -> List[Any]:
        """Busca um lote de dados."""
        pass
    
    @abstractmethod
    def get_primary_key_columns(self, table: Table) -> List[str]:
        """Obtém colunas de chave primária de uma tabela."""
        pass