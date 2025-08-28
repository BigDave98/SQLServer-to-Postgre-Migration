from abc import ABC, abstractmethod
from sqlalchemy import Column
from sqlalchemy.types import TypeEngine

class TypeConverterStrategy(ABC):
    """Interface base para estratégias de conversão de tipos."""
    
    @abstractmethod
    def can_convert(self, type_name: str) -> bool:
        """Verifica se esta estratégia pode converter o tipo."""
        pass
    
    @abstractmethod
    def convert(self, column: Column) -> TypeEngine:
        """Converte o tipo da coluna."""
        pass