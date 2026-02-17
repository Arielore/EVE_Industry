"""
DuckDB connection management for EVE Industry application.
Provides thread-local connections and safe query execution.
"""

import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Union, Tuple

import duckdb


class DatabaseConnection:
    """Thread-local DuckDB connection manager."""
    
    _local = threading.local()
    
    def __init__(self, db_path: Union[str, Path] = None):
        """
        Initialize database connection manager.
        
        Args:
            db_path: Path to DuckDB database file. If None, uses in-memory database.
        """
        self.db_path = Path(db_path) if db_path else None
    
    def get_connection(self) -> duckdb.DuckDBPyConnection:
        """Get thread-local DuckDB connection."""
        if not hasattr(self._local, 'connection') or self._local.connection is None:
            if self.db_path:
                self._local.connection = duckdb.connect(str(self.db_path))
            else:
                self._local.connection = duckdb.connect(':memory:')
        return self._local.connection
    
    def close_connection(self):
        """Close thread-local connection."""
        if hasattr(self._local, 'connection') and self._local.connection is not None:
            self._local.connection.close()
            self._local.connection = None
    
    @contextmanager
    def cursor(self):
        """Context manager for database cursor."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            cursor.close()
        except Exception:
            cursor.close()
            raise
    
    def execute(self, query: str, params: Optional[Tuple] = None):
        """
        Execute SQL query that doesn't return results (INSERT, UPDATE, DELETE).
        
        Args:
            query: SQL query string
            params: Optional query parameters
        """
        conn = self.get_connection()
        if params:
            conn.execute(query, params)
        else:
            conn.execute(query)
    
    def execute_df(self, query: str, params: tuple = None):
        """
        Execute SQL query and return result as pandas DataFrame.
        
        Args:
            query: SQL query string
            params: Optional query parameters
        
        Returns:
            pandas.DataFrame containing query results
        """
        import pandas as pd
        
        with self.cursor() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Get column names
            columns = [desc[0] for desc in cursor.description]
            
            # Fetch all rows
            rows = cursor.fetchall()
            
            return pd.DataFrame(rows, columns=columns) if rows else pd.DataFrame(columns=columns)


# Global database connection instance
_db: Optional[DatabaseConnection] = None


def get_db() -> DatabaseConnection:
    """Get global database connection instance."""
    global _db
    if _db is None:
        # Default to data/database/industry.duckdb
        db_path = Path(__file__).parent.parent.parent.parent / "data" / "database" / "industry.duckdb"
        _db = DatabaseConnection(db_path)
    return _db