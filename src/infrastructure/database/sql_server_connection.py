from typing import Dict, List, Optional
from sqlalchemy import MetaData
from sqlalchemy.sql.schema import Table as TableType
from src.infrastructure.database.base_connection import DBServerConn
from src.infrastructure.factories.repository_factory import RepositoryFactory
from src.infrastructure.repositories.source_repository import SourceRepository

class SQLServerConn(DBServerConn):
    def __init__(self, sql_uri: str) -> None:
        super().__init__(sql_uri)
        self.repository: SourceRepository = RepositoryFactory.create_source_repository(self.engine)
        self.metadata: MetaData = MetaData()
        self.sorted_tables: Optional[List[TableType]] = None
        self.tables_names: List[str] = []
        self.tables: Dict[str, TableType] = {}
        self.fks_dependencies: List = []

    def get_db_metadata(self) -> None:
        """Carrega metadados do banco usando o repositório."""
        # Forçar carregamento dos metadados
        self.tables = self.repository.get_all_tables_metadata()
        self.tables_names = list(self.tables.keys())
        
        # Obter tabelas ordenadas
        self.sorted_tables = self.repository.get_sorted_tables()
        
        # Atualizar metadata local para compatibilidade
        self.metadata = self.repository.metadata