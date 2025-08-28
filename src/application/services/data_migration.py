from src.domain.services.migration_stats import MigrationStats
from src.infrastructure.validators.migration_validator import MigrationValidator
from src.infrastructure.transformers.data_transformer import DataTransformer
from src.infrastructure.processors.batch_processor import BatchProcessor
from src.infrastructure.database.sql_server_connection import SQLServerConn
from src.infrastructure.database.postgre_connection import PostgreConn
from src.config.settings import Config

from typing import Dict,Tuple, Any
from tqdm import tqdm
from sqlalchemy import Table

class DataMigration:
    def __init__(self, src: SQLServerConn, tgt: PostgreConn) -> None:
        self.source_conn = src
        self.target_conn = tgt
        
        # Usar repositórios ao invés de engines diretos
        self.source_repository = src.repository
        self.target_repository = tgt.repository
        
        # Injeção de dependências
        self.stats = MigrationStats()
        self.validator = MigrationValidator(src.engine, tgt.engine)
        self.transformer = DataTransformer()
        self.batch_processor = BatchProcessor(Config.BATCH_SIZE, self.transformer)
    
    def migrate_data(self) -> Dict[str, Any]:
        """Orquestra o processo de migração usando repositórios."""
        try:
            self.stats.start_migration()
            
            # Usar repositório para obter ordem de migração
            migration_order = self.source_repository.get_tables_in_order()
            
            if not migration_order:
                print("Nenhuma tabela para migrar")
                return self.stats.get_stats()
            
            # Usar repositório para controlar constraints
            self.target_repository.disable_constraints()
            
            for idx, table_name in enumerate(migration_order, 1):
                print(f"\n[{idx}/{len(migration_order)}] Processando {table_name}...")
                success, records = self._migrate_table(table_name)
                
                if success:
                    self.stats.add_successful_table(table_name, records)
                else:
                    self.stats.add_failed_table(table_name)
            
            self.target_repository.enable_constraints()
            
        except Exception as e:
            print(f"Erro na migração: {e}")
            raise
        finally:
            self.stats.end_migration()
            
        return self.stats.get_stats()
    
    def _migrate_table(self, table_name: str) -> Tuple[bool, int]:
        """Migra uma única tabela usando repositórios."""
        try:
            # Usar repositórios para obter metadados
            source_table = self.source_repository.get_table_metadata(table_name)
            target_table = self.target_repository.get_table_metadata(table_name)
            
            # Usar repositório para contar registros
            total_records = self.source_repository.count_records(source_table)
            
            if total_records == 0:
                print(f"Tabela {table_name} está vazia. Pulando.")
                return True, 0
            
            print(f"Migrando {table_name}: {total_records:,} registros")

            migrated = self._migrate_table_data(source_table, target_table, total_records)
            
            # Validar usando repositório
            target_count = self.target_repository.count_records(target_table)
            if target_count == migrated:
                print(f"{table_name}: {migrated:,} registros migrados com sucesso")
                return True, migrated
            else:
                print(f"{table_name}: Falha na validação")
                return False, 0
                
        except Exception as e:
            print(f"Erro ao migrar {table_name}: {str(e)}")
            return False, 0
    
    def _migrate_table_data(self, source_table: Table, target_table: Table,
                           total_records: int) -> int:
        """Coordena a migração de dados de uma tabela usando repositórios."""
        # Usar repositório para obter chaves primárias
        pk_columns = self.source_repository.get_primary_key_columns(source_table)
        order_column = pk_columns[0] if pk_columns else source_table.columns.keys()[0]
        column_names = [col.name for col in target_table.columns]
        
        migrated = 0
        
        with tqdm(total=total_records, desc=f"  → {source_table.name}", 
                 unit="registros") as pbar:
            
            offset = 0
            while offset < total_records:
                try:
                    # Usar repositório para buscar batch
                    batch = self.source_repository.fetch_batch(
                        source_table, order_column, 
                        self.batch_processor.batch_size, offset
                    )
                    
                    if not batch:
                        break
                    
                    # Preparar dados
                    batch_data = self.batch_processor.prepare_batch_data(batch, column_names)
                    
                    # Tentar inserir primeiro sem transformação
                    try:
                        success = self.target_repository.insert_batch(target_table, batch_data)
                        if success:
                            status = "success"
                        else:
                            raise Exception("Falha na inserção")
                    except ValueError as e:
                        if "NUL (0x00)" in str(e):
                            # Aplicar transformação e tentar novamente
                            transformed_data, _ = self.transformer.transform_batch(batch_data)
                            success = self.target_repository.insert_batch(
                                target_table, transformed_data
                            )
                            status = "transformed" if success else "failed"
                        else:
                            raise
                    
                    if status == "transformed":
                        self.stats.add_table_with_issues(source_table.name, "null_chars")
                    
                    batch_size = len(batch)
                    migrated += batch_size
                    offset += batch_size
                    pbar.update(batch_size)
                    
                except Exception as e:
                    print(f"Erro no batch {offset}-{offset+self.batch_processor.batch_size}: {e}")
                    offset += self.batch_processor.batch_size
                    continue
        
        return migrated