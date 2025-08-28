from typing import Dict, Any
from datetime import datetime

class MigrationStats:
    def __init__(self) -> None:
        self._stats: Dict[str, Any] = {
            'tables_migrated': 0,
            'total_records': 0,
            'failed_tables': [],
            'start_time': None,
            'end_time': None,
            'tables_with_issues': []
        }
    
    def start_migration(self) -> None:
        self._stats['start_time'] = datetime.now()
    
    def end_migration(self) -> None:
        self._stats['end_time'] = datetime.now()
    
    def add_successful_table(self, table_name: str, records: int) -> None:
        self._stats['tables_migrated'] += 1
        self._stats['total_records'] += records
    
    def add_failed_table(self, table_name: str) -> None:
        self._stats['failed_tables'].append(table_name)
    
    def add_table_with_issues(self, table_name: str, issue_type: str) -> None:
        self._stats['tables_with_issues'].append({
            'table': table_name,
            'issue': issue_type
        })
    
    def get_stats(self) -> Dict[str, Any]:
        return self._stats.copy()