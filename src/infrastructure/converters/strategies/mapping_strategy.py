from typing import Dict
from sqlalchemy import Column, String
from sqlalchemy.types import TypeEngine
from src.domain.interfaces.type_converter import TypeConverterStrategy

class MappingStrategy(TypeConverterStrategy):
    """Estratégia que usa um dicionário de mapeamento."""
    
    def __init__(self, type_mapping: Dict[str, TypeEngine]):
        self.type_mapping = type_mapping
    
    def can_convert(self, type_name: str) -> bool:
        return type_name in self.type_mapping
    
    def convert(self, column: Column) -> TypeEngine:
        type_name = str(column.type)
        return self.type_mapping.get(type_name, String())