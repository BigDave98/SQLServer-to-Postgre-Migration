from src.infrastructure.database.sql_server_connection import SQLServerConn
from src.infrastructure.database.base_connection import DBServerConn
from src.domain.interfaces.target_repository import ITargetRepository
from src.infrastructure.factories.repository_factory import RepositoryFactory
from src.infrastructure.converters.type_converter import TypeConverter

from typing import List, Tuple, Optional
from sqlalchemy import Table, MetaData, Column

import os

class PostgreConn(DBServerConn):
    def __init__(self, sql_uri: str) -> None:
        super().__init__(sql_uri)
        self.schema: Optional[str] = os.getenv("POSTGRES_SCHEMA")
        self.repository: ITargetRepository = RepositoryFactory.create_target_repository(
            self.engine, 
            self.schema
        )
        self.type_converter = TypeConverter()

    def create_tables(self, SQLMetadata: SQLServerConn, creation_order: List[str]) -> None:
        """Cria tabelas no PostgreSQL usando o repositório."""
        created: List[str] = []
        failed: List[Tuple[str, str]] = []
        
        for table_name in creation_order:
            try:
                source_table = SQLMetadata.tables[table_name]
                
                # Criar metadata para PostgreSQL
                pg_metadata = MetaData(schema=self.schema)
                
                # Criar tabela nova com tipos adaptados
                columns = []
                for col in source_table.columns:
                    new_type = self.type_converter.convert_column_type(col)
                    
                    columns.append(Column(
                        name=col.name,
                        type_=new_type,
                        nullable=col.nullable,
                        primary_key=col.primary_key,
                        autoincrement=col.autoincrement,
                        index=col.index,
                        default=col.default
                    ))
                
                target_table = Table(table_name, pg_metadata, *columns)
                
                # Usar repositório para criar tabela
                if self.repository.create_table(target_table):
                    created.append(table_name)
                    print(f"✓ Tabela {table_name} criada com sucesso")
                else:
                    failed.append((table_name, "Falha ao criar tabela"))
                
            except Exception as e:
                failed.append((table_name, str(e)))
                print(f"✗ Erro ao criar tabela {table_name}: {e}")
        
        print(f"\nResumo: {len(created)} criadas, {len(failed)} falharam")