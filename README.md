# Database Migration Tool - SQL Server to PostgreSQL

A robust and efficient database migration tool designed to seamlessly transfer data from SQL Server to PostgreSQL databases. Built with Python, SQLAlchemy, and following clean architecture principles.

## 🚀 Features

- **Complete Schema Migration**: Automatically converts SQL Server table structures to PostgreSQL-compatible schemas
- **Intelligent Type Mapping**: Smart conversion of data types between different database systems
- **Batch Processing**: Configurable batch sizes for optimal performance on large datasets
- **Data Integrity**: Automatic handling of character encoding issues and NULL byte removal
- **Progress Tracking**: Real-time progress bars and detailed migration statistics
- **Error Recovery**: Resilient error handling with automatic retry mechanisms
- **Foreign Key Management**: Intelligent ordering of table migration based on dependencies
- **Clean Architecture**: Modular design following SOLID principles and repository pattern

## 📋 Prerequisites

- Python 3.8+
- SQL Server database (source)
- PostgreSQL database (target)
- ODBC Driver for SQL Server

## 🔧 Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/database-migration.git
cd database-migration
```

2. **Virtual environment**

```bash
.venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a .env file in the root directory:

```bash
# SQL Server Configuration
SQL_SERVER_HOST=your_sqlserver_host
SQL_SERVER_PORT=1433
SQL_SERVER_DATABASE=your_source_db
SQL_SERVER_USER=your_username
SQL_SERVER_PASSWORD=your_password
SQL_SERVER_DRIVER=ODBC+Driver+17+for+SQL+Server

# PostgreSQL Configuration
POSTGRES_HOST=your_postgres_host
POSTGRES_PORT=5432
POSTGRES_DATABASE=your_target_db
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_SCHEMA=public

# Migration Configuration
BATCH_SIZE=10000
```

## 🚀 Usage

**Basic Migration**
Run the migration with default settings:
```bash
python main.py
```
## Migration Process
The tool performs migration in the following steps:

**Metadata Extraction**: Reads source database schema
**Dependency Analysis**: Determines correct table creation order
**Schema Creation**: Creates tables in PostgreSQL with converted types
**Data Transfer**: Migrates data in optimized batches
**Validation**: Verifies record counts and data integrity

## Example Output
```bash
Retrieving MetaData
Creating 15 tables in PostgreSQL...
✓ Table users created successfully
✓ Table products created successfully
✓ Table orders created successfully

Starting data migration...
[1/15] Processing users...
  → users: 100%|████████████| 50,000/50,000 [00:45<00:00, 1,105 records/s]
✅ users: 50,000 records migrated successfully

Migration completed successfully!

=== Migration Statistics ===
Tables migrated: 15
Total records: 1,250,000
Migration time: 15m 32s
```
## 🏗️ Architecture
The project follows Clean Architecture principles with clear separation of concerns:
```bash
src/
├── domain/           # Business logic and interfaces
├── application/      # Use cases and orchestration
├── infrastructure/   # External dependencies and implementations
└── config/          # Configuration management
```

## Key Components
**Repository Pattern**: Abstracts database operations
**Strategy Pattern**: Flexible type conversion system
**Factory Pattern**: Standardized object creation
**Dependency Injection**: Loose coupling between components

## 🔄 Type Conversion
The tool automatically converts SQL Server types to PostgreSQL equivalents:
```bash
| SQL Server | PostgreSQL |
|------------|------------|
| NVARCHAR   | VARCHAR    |
| DATETIME   | TIMESTAMP  |
| MONEY      | DECIMAL    |
| BIT        | BOOLEAN    |
| NTEXT      | TEXT       |
```