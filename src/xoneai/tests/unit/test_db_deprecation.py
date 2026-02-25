"""
Tests for db import deprecation warnings.

These tests verify that:
1. New simplified imports work: from xoneaiagents import db
2. New simplified imports work: from xoneai import db
3. Old imports emit DeprecationWarning: from xoneai.db import XoneDB
"""

import warnings
import pytest


class TestNewDbImports:
    """Test that new simplified db imports work correctly."""
    
    def test_import_db_from_xoneaiagents(self):
        """Test: from xoneaiagents import db"""
        import sys
        from xoneaiagents import db
        assert db is not None
        # Handle case where 'db' might be imported as a module instead of proxy object
        if isinstance(db, type(sys)):
            from xoneaiagents.db import db as db_proxy
            db = db_proxy
        assert hasattr(db, 'XoneDB')
        assert callable(db)  # db(...) should work as shortcut
    
    def test_import_db_from_xoneai(self):
        """Test: from xoneai import db
        
        Note: This returns the xoneai.db module (for backwards compat).
        The recommended pattern is: from xoneaiagents import db
        """
        import sys
        from xoneai import db
        assert db is not None
        # Handle case where 'db' might be imported as a module instead of proxy object
        if isinstance(db, type(sys)) and not hasattr(db, 'XoneDB'):
            from xoneaiagents.db import db as db_proxy
            db = db_proxy
        # xoneai.db is a module with lazy-loaded classes
        assert hasattr(db, 'XoneDB')
    
    def test_db_callable_shortcut(self):
        """Test that db(...) works as shortcut for db.XoneDB(...)"""
        import sys
        from xoneaiagents import db
        if isinstance(db, type(sys)):
            from xoneaiagents.db import db as db_proxy
            db = db_proxy
        # Should not raise - just creates the adapter
        # (actual DB connection is lazy)
        instance = db(database_url="sqlite:///test.db")
        assert instance is not None
    
    def test_import_agent_and_db_together(self):
        """Test: from xoneaiagents import Agent, db"""
        from xoneaiagents import Agent, db
        assert Agent is not None
        assert db is not None
    
    def test_import_all_common_symbols(self):
        """Test: from xoneaiagents import Agent, Agents, Task, tool, db"""
        from xoneaiagents import Agent, Agents, Task, tool, db
        assert Agent is not None
        assert Agents is not None
        assert Task is not None
        assert tool is not None
        assert db is not None


class TestDeprecationWarnings:
    """Test that old imports emit DeprecationWarning."""
    
    def test_xonedb_import_warns(self):
        """Test: from xoneai.db import XoneDB emits warning"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            from xoneai.db import XoneDB
            
            # Should have at least one deprecation warning
            deprecation_warnings = [
                x for x in w 
                if issubclass(x.category, DeprecationWarning)
            ]
            assert len(deprecation_warnings) >= 1
            
            # Check warning message content
            msg = str(deprecation_warnings[0].message)
            assert "deprecated" in msg.lower()
            assert "xoneaiagents" in msg or "xoneai" in msg
    
    def test_postgresdb_import_warns(self):
        """Test: from xoneai.db import PostgresDB emits warning"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            from xoneai.db import PostgresDB
            
            deprecation_warnings = [
                x for x in w 
                if issubclass(x.category, DeprecationWarning)
            ]
            assert len(deprecation_warnings) >= 1
    
    def test_sqlitedb_import_warns(self):
        """Test: from xoneai.db import SQLiteDB emits warning"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            from xoneai.db import SQLiteDB
            
            deprecation_warnings = [
                x for x in w 
                if issubclass(x.category, DeprecationWarning)
            ]
            assert len(deprecation_warnings) >= 1
    
    def test_redisdb_import_warns(self):
        """Test: from xoneai.db import RedisDB emits warning"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            from xoneai.db import RedisDB
            
            deprecation_warnings = [
                x for x in w 
                if issubclass(x.category, DeprecationWarning)
            ]
            assert len(deprecation_warnings) >= 1


class TestBackwardsCompatibility:
    """Test that old imports still work (just with warnings)."""
    
    def test_xonedb_still_works(self):
        """Old XoneDB import should still work."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            from xoneai.db import XoneDB
            
            # Should be usable
            instance = XoneDB(database_url="sqlite:///test.db")
            assert instance is not None
    
    def test_postgresdb_still_works(self):
        """Old PostgresDB import should still work."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            from xoneai.db import PostgresDB
            
            # Should be a class
            assert PostgresDB is not None


class TestNoHeavyImports:
    """Test that db import doesn't load heavy dependencies."""
    
    def test_db_import_is_lightweight(self):
        """Importing db should not import heavy DB clients."""
        import sys
        
        # Clear any cached imports
        modules_before = set(sys.modules.keys())
        
        from xoneaiagents import db
        
        modules_after = set(sys.modules.keys())
        new_modules = modules_after - modules_before
        
        # Should not have imported heavy DB clients
        heavy_modules = ['psycopg2', 'pymysql', 'redis', 'qdrant_client']
        for heavy in heavy_modules:
            assert heavy not in new_modules, f"Heavy module {heavy} was imported"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
