from typing import List
from sqlalchemy import Column, String
from sqlalchemy.types import TypeEngine
from src.domain.interfaces.type_converter import TypeConverterStrategy
from src.infrastructure.converters.strategies.varchar_strategy import VarcharStrategy
from src.infrastructure.converters.strategies.mapping_strategy import MappingStrategy
from src.infrastructure.converters.strategies.default_strategy import DefaultStrategy
from src.config.settings import TYPE_MAPPING

class TypeConverter:
    """Conversor de tipos usando Strategy Pattern."""
    
    def __init__(self):
        self.strategies: List[TypeConverterStrategy] = [
            VarcharStrategy(),
            MappingStrategy(TYPE_MAPPING),
            DefaultStrategy()  
        ]
    
    def convert_column_type(self, column: Column) -> TypeEngine:
        """Converte o tipo de uma coluna do SQL Server para PostgreSQL."""
        type_name = str(column.type)
        
        for strategy in self.strategies:
            if strategy.can_convert(type_name):
                return strategy.convert(column)
        
        return String()

# Função para manter compatibilidade com código existente
def convert_column_type(column: Column) -> TypeEngine:
    converter = TypeConverter()
    return converter.convert_column_type(column)