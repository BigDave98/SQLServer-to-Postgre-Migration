from typing import List, Dict, Any, Optional
from sqlalchemy import Table, MetaData, select, text, func
from sqlalchemy.engine import Engine
from src.domain.interfaces.source_repository import ISourceRepository

class SourceRepository(ISourceRepository):
    """Repositório para operações de leitura no banco de origem."""
    
    def __init__(self, engine: Engine):
        self.engine = engine
        self.metadata = MetaData()
        self._tables_cache: Optional[Dict[str, Table]] = None
        self._sorted_tables_cache: Optional[List[Table]] = None
        self._reflected: bool = False
    
    def _ensure_metadata_reflected(self) -> None:
        """Garante que os metadados foram refletidos do banco."""
        if not self._reflected:
            self.metadata.reflect(self.engine)
            self._tables_cache = dict(self.metadata.tables)
            self._sorted_tables_cache = list(self.metadata.sorted_tables)
            self._reflected = True
    
    def get_table_metadata(self, table_name: str) -> Table:
        """Obtém os metadados de uma tabela específica."""
        self._ensure_metadata_reflected()
        
        table = self._tables_cache.get(table_name)
        if table == None:
            raise ValueError(f"Tabela '{table_name}' não encontrada")
        
        return table
    
    def get_all_tables_metadata(self) -> Dict[str, Table]:
        """Obtém metadados de todas as tabelas."""
        self._ensure_metadata_reflected()
        return self._tables_cache.copy()
    
    def get_tables_in_order(self) -> List[str]:
        """Obtém lista de tabelas ordenadas por dependências."""
        self._ensure_metadata_reflected()
        
        # Retorna em ordem reversa para migração (filhas primeiro)
        return [table.name for table in reversed(self._sorted_tables_cache)]
    
    def count_records(self, table: Table) -> int:
        """Conta o número de registros em uma tabela."""
        with self.engine.connect() as conn:
            count_query = select(func.count()).select_from(table)
            return conn.execute(count_query).scalar() or 0
    
    def fetch_batch(
        self, 
        table: Table, 
        order_column: str, 
        batch_size: int, 
        offset: int
    ) -> List[Any]:
        """Busca um lote de dados da tabela."""
        with self.engine.connect() as conn:
            query = (
                select(table)
                .order_by(text(order_column))
                .limit(batch_size)
                .offset(offset)
            )
            result = conn.execute(query)
            return result.fetchall()
    
    def get_primary_key_columns(self, table: Table) -> List[str]:
        """Obtém colunas de chave primária."""
        return [col.name for col in table.primary_key]
    
    def table_exists(self, table_name: str) -> bool:
        """Verifica se uma tabela existe."""
        return self.engine.dialect.has_table(self.engine, table_name)
    
    def get_sorted_tables(self) -> List[Table]:
        """Obtém lista de tabelas ordenadas por dependências."""
        self._ensure_metadata_reflected()
        return list(self._sorted_tables_cache)