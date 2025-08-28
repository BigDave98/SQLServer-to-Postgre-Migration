from typing import Dict, Any, List, Tuple

class DataTransformer:
    def __init__(self) -> None:
        self._transformations_applied: int = 0
    
    def clean_null_characters(self, value: Any) -> Any:
        """Remove caracteres NUL (0x00) de strings."""
        if isinstance(value, str) and '\x00' in value:
            self._transformations_applied += 1
            return value.replace('\x00', '').strip()
        return value
    
    def transform_batch(self, batch_data: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], bool]:
        """Transforma um batch de dados. Retorna (dados_transformados, houve_transformacao)"""
        transformed_batch: List[Dict[str, Any]] = []
        has_transformations: bool = False
        
        for row_dict in batch_data:
            transformed_row: Dict[str, Any] = {}
            for key, value in row_dict.items():
                original_value = value
                transformed_value = self.clean_null_characters(value)
                
                if original_value != transformed_value:
                    has_transformations = True
                    
                transformed_row[key] = transformed_value
            transformed_batch.append(transformed_row)
        
        return transformed_batch, has_transformations
    
    def get_transformations_count(self) -> int:
        return self._transformations_applied