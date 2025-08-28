from sqlalchemy import Column, String
from sqlalchemy.types import TypeEngine
from src.domain.interfaces.type_converter import TypeConverterStrategy

class DefaultStrategy(TypeConverterStrategy):
    """Estratégia padrão quando nenhuma outra se aplica."""
    
    def can_convert(self, type_name: str) -> bool:
        return True  
    
    def convert(self, column: Column) -> TypeEngine:
        return String() 