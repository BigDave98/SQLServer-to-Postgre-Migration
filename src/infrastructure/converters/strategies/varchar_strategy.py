from sqlalchemy import Column, String
from sqlalchemy.types import TypeEngine
from src.domain.interfaces.type_converter import TypeConverterStrategy

class VarcharStrategy(TypeConverterStrategy):
    """Estratégia para conversão de tipos VARCHAR."""
    
    def can_convert(self, type_name: str) -> bool:
        return "VARCHAR" in type_name
    
    def convert(self, column: Column) -> TypeEngine:
        # Preserva o length se existir
        length = getattr(column.type, 'length', None)
        return String(length=length)