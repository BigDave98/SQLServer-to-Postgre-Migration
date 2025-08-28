from typing import Optional
from sqlalchemy.engine import Engine
from src.domain.interfaces.source_repository import ISourceRepository
from src.domain.interfaces.target_repository import ITargetRepository
from src.infrastructure.repositories.source_repository import SourceRepository
from src.infrastructure.repositories.target_repository import TargetRepository

class RepositoryFactory:
    """Factory para criar repositórios."""
    
    @staticmethod
    def create_source_repository(engine: Engine) -> ISourceRepository:
        """Cria um repositório de origem."""
        return SourceRepository(engine)
    
    @staticmethod
    def create_target_repository(
        engine: Engine, 
        schema: Optional[str] = None
    ) -> ITargetRepository:
        """Cria um repositório de destino."""
        return TargetRepository(engine, schema)