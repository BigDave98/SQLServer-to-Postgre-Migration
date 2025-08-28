from typing import List, Dict, Any, Tuple
from sqlalchemy import Table, select, text
from sqlalchemy.engine import Engine
from sqlalchemy.engine.row import Row
from src.infrastructure.transformers.data_transformer import DataTransformer

class BatchProcessor:
    def __init__(self, batch_size: int, transformer: DataTransformer) -> None:
        self.batch_size = batch_size
        self.transformer = transformer
    
    def fetch_batch(self, table: Table, engine: Engine, order_column: str, 
                   offset: int) -> List[Row]:
        """Busca um batch de dados da origem."""
        with engine.connect() as conn:
            query = (
                select(table)
                .order_by(text(order_column))
                .limit(self.batch_size)
                .offset(offset)
            )
            result = conn.execute(query)
            return result.fetchall()
    
    def prepare_batch_data(self, batch: List[Row], column_names: List[str]) -> List[Dict[str, Any]]:
        """Converte batch para lista de dicionários."""
        return [dict(zip(column_names, row)) for row in batch]
    
    def insert_batch(self, table: Table, batch_data: List[Dict[str, Any]], 
                    engine: Engine) -> Tuple[bool, str]:
        """Insere batch com tratamento de erros e transformação se necessário."""
        try:
            # Primeira tentativa sem transformação
            with engine.begin() as conn:
                conn.execute(table.insert(), batch_data)
            return True, "success"
            
        except ValueError as e:
            if "NUL (0x00)" in str(e):
                # Aplicar transformação e tentar novamente
                transformed_data, _ = self.transformer.transform_batch(batch_data)
                
                try:
                    with engine.begin() as conn:
                        conn.execute(table.insert(), transformed_data)
                    return True, "transformed"
                except Exception as retry_error:
                    raise retry_error
            else:
                raise e