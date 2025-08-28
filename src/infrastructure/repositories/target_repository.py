from typing import List, Dict, Any, Optional
from sqlalchemy import Table, MetaData, select, func, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from src.domain.interfaces.target_repository import ITargetRepository

class TargetRepository(ITargetRepository):
    """Repositório para operações de escrita no banco de destino."""
    
    def __init__(self, engine: Engine, schema: Optional[str] = None):
        self.engine = engine
        self.schema = schema
        self.metadata = MetaData(schema=schema)
    
    def get_table_metadata(self, table_name: str) -> Table:
        """Obtém os metadados de uma tabela."""
        metadata = MetaData(schema=self.schema)
        return Table(
            table_name, 
            metadata, 
            autoload_with=self.engine,
            schema=self.schema
        )
    
    def create_table(self, table: Table) -> bool:
        """Cria uma tabela no banco de destino."""
        try:
            table.create(self.engine, checkfirst=True)
            return True
        except SQLAlchemyError as e:
            print(f"Erro ao criar tabela {table.name}: {e}")
            return False
    
    def insert_batch(self, table: Table, data: List[Dict[str, Any]]) -> bool:
        """Insere um lote de dados na tabela."""
        if not data:
            return True
        
        try:
            with self.engine.begin() as conn:
                conn.execute(table.insert(), data)
            return True
        except SQLAlchemyError as e:
            print(f"Erro ao inserir dados em {table.name}: {e}")
            return False
    
    def count_records(self, table: Table) -> int:
        """Conta registros na tabela."""
        try:
            with self.engine.connect() as conn:
                count_query = select(func.count()).select_from(table)
                return conn.execute(count_query).scalar() or 0
        except SQLAlchemyError:
            return 0
    
    def truncate_table(self, table_name: str) -> bool:
        """Limpa todos os dados de uma tabela."""
        try:
            with self.engine.begin() as conn:
                # Para PostgreSQL
                if self.engine.dialect.name == 'postgresql':
                    conn.execute(text(f"TRUNCATE TABLE {table_name} CASCADE"))
                else:
                    conn.execute(text(f"DELETE FROM {table_name}"))
            return True
        except SQLAlchemyError as e:
            print(f"Erro ao truncar tabela {table_name}: {e}")
            return False
    
    def disable_constraints(self) -> None:
        """Desabilita constraints para PostgreSQL."""
        if self.engine.dialect.name == 'postgresql':
            try:
                with self.engine.begin() as conn:
                    conn.execute(text("SET session_replication_role = replica;"))
            except SQLAlchemyError as e:
                print(f"Erro ao desabilitar constraints: {e}")
    
    def enable_constraints(self) -> None:
        """Habilita constraints para PostgreSQL."""
        if self.engine.dialect.name == 'postgresql':
            try:
                with self.engine.begin() as conn:
                    conn.execute(text("SET session_replication_role = origin;"))
            except SQLAlchemyError as e:
                print(f"Erro ao habilitar constraints: {e}")
    
    def table_exists(self, table_name: str) -> bool:
        """Verifica se uma tabela existe."""
        return self.engine.dialect.has_table(
            self.engine, 
            table_name, 
            schema=self.schema
        )