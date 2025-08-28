from sqlalchemy import Table, select, func
from sqlalchemy.engine import Engine

class MigrationValidator:
    def __init__(self, source_engine: Engine, target_engine: Engine) -> None:
        self.source_engine = source_engine
        self.target_engine = target_engine
    
    def validate_migration(self, source_table: Table, target_table: Table, 
                          expected_count: int) -> bool:
        """Verifica se a migração foi bem sucedida."""
        try:
            actual_count = self._count_records(target_table, self.target_engine)
            return actual_count == expected_count
        except Exception as e:
            print(f"Erro na verificação: {e}")
            return False
    
    def _count_records(self, table: Table, engine: Engine) -> int:
        """Conta registros em uma tabela."""
        with engine.connect() as conn:
            count_query = select(func.count()).select_from(table)
            return conn.execute(count_query).scalar() or 0
    
    def validate_table_exists(self, table_name: str, engine: Engine) -> bool:
        """Verifica se a tabela existe no banco de dados."""
        return engine.dialect.has_table(engine, table_name)