from src.infrastructure.factories.database_connection_factory import DatabaseConnectionFactory
from src.infrastructure.database.sql_server_connection import SQLServerConn
from src.infrastructure.database.postgre_connection import PostgreConn
from src.infrastructure.factories.database_connection_factory import DatabaseConnectionFactory
from src.application.services.data_migration import DataMigration 

import logging

def main() -> None:
    try:
        # Criar conexões usando factory
        src_connection: SQLServerConn = DatabaseConnectionFactory.create_from_config('sql_server')
        tgt_connection: PostgreConn = DatabaseConnectionFactory.create_from_config('postgresql')
        
        print("Retrieving MetaData")
        # Carregar metadados
        src_connection.get_db_metadata()

        # Obter ordem de criação usando repositório
        creation_order = src_connection.repository.get_tables_in_order()
        # Reverter ordem para criação (pais primeiro)
        creation_order.reverse()
        
        # Criar tabelas
        tgt_connection.create_tables(src_connection, creation_order)

        print("Iniciando migração de dados...")
        data_migration = DataMigration(src_connection, tgt_connection)
        stats = data_migration.migrate_data()

        #data_migration.validator.validate_migration() 
    
    except Exception as e:
        logging.exception("Falha catastrófica na migração", e)

    finally:
        # Garantir que conexões sejam fechadas
        if 'src_engine' in locals():
            src_connection.engine.dispose()
        if 'tgt_engine' in locals():
            tgt_connection.engine.dispose()
    
if __name__ == "__main__":
    main()