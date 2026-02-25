"""
Unit tests for xoneaiagents.paths module.

Tests centralized path utilities for XoneAI data storage.
TDD: These tests define the expected behavior of the paths module.
"""

import os
import warnings
from pathlib import Path
from unittest.mock import patch


class TestGetDataDir:
    """Tests for get_data_dir() function."""
    
    def test_default_returns_xoneai_in_home(self):
        """Default data dir should be ~/.xoneai/"""
        from xoneaiagents.paths import get_data_dir
        
        result = get_data_dir()
        expected = Path.home() / ".xoneai"
        assert result == expected
    
    def test_env_var_override(self):
        """XONEAI_HOME env var should override default."""
        from xoneaiagents.paths import get_data_dir
        
        with patch.dict(os.environ, {"XONEAI_HOME": "/custom/path"}):
            result = get_data_dir()
            assert result == Path("/custom/path")
    
    def test_env_var_expands_tilde(self):
        """XONEAI_HOME should expand ~ to home directory."""
        from xoneaiagents.paths import get_data_dir
        
        with patch.dict(os.environ, {"XONEAI_HOME": "~/custom/xone"}):
            result = get_data_dir()
            assert result == Path.home() / "custom" / "xone"
    
    def test_legacy_fallback_with_warning(self, tmp_path):
        """Should fall back to ~/.xone/ if it exists and ~/.xoneai/ doesn't."""
        from xoneaiagents.paths import get_data_dir, _clear_cache
        
        # Clear cache before test
        _clear_cache()
        
        # Create mock home with only legacy dir
        mock_home = tmp_path / "home"
        legacy_dir = mock_home / ".xone"
        legacy_dir.mkdir(parents=True)
        
        with patch("xoneaiagents.paths.Path.home", return_value=mock_home):
            with patch.dict(os.environ, {}, clear=True):
                # Remove XONEAI_HOME if set
                os.environ.pop("XONEAI_HOME", None)
                
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always")
                    result = get_data_dir()
                    
                    # Should return legacy path
                    assert result == legacy_dir
                    
                    # Should emit deprecation warning
                    assert len(w) == 1
                    assert issubclass(w[0].category, DeprecationWarning)
                    assert ".xone" in str(w[0].message)
        
        # Clear cache after test
        _clear_cache()


class TestGetSessionsDir:
    """Tests for get_sessions_dir() function."""
    
    def test_returns_sessions_subdir(self):
        """Should return sessions subdirectory of data dir."""
        from xoneaiagents.paths import get_sessions_dir
        
        result = get_sessions_dir()
        assert result == Path.home() / ".xoneai" / "sessions"
    
    def test_respects_env_override(self):
        """Should respect XONEAI_HOME override."""
        from xoneaiagents.paths import get_sessions_dir
        
        with patch.dict(os.environ, {"XONEAI_HOME": "/custom"}):
            result = get_sessions_dir()
            assert result == Path("/custom/sessions")


class TestGetSkillsDir:
    """Tests for get_skills_dir() function."""
    
    def test_returns_skills_subdir(self):
        """Should return skills subdirectory of data dir."""
        from xoneaiagents.paths import get_skills_dir
        
        result = get_skills_dir()
        assert result == Path.home() / ".xoneai" / "skills"


class TestGetPluginsDir:
    """Tests for get_plugins_dir() function."""
    
    def test_returns_plugins_subdir(self):
        """Should return plugins subdirectory of data dir."""
        from xoneaiagents.paths import get_plugins_dir
        
        result = get_plugins_dir()
        assert result == Path.home() / ".xoneai" / "plugins"


class TestGetMcpDir:
    """Tests for get_mcp_dir() function."""
    
    def test_returns_mcp_subdir(self):
        """Should return mcp subdirectory of data dir."""
        from xoneaiagents.paths import get_mcp_dir
        
        result = get_mcp_dir()
        assert result == Path.home() / ".xoneai" / "mcp"


class TestGetDocsDir:
    """Tests for get_docs_dir() function."""
    
    def test_returns_docs_subdir(self):
        """Should return docs subdirectory of data dir."""
        from xoneaiagents.paths import get_docs_dir
        
        result = get_docs_dir()
        assert result == Path.home() / ".xoneai" / "docs"


class TestGetRulesDir:
    """Tests for get_rules_dir() function."""
    
    def test_returns_rules_subdir(self):
        """Should return rules subdirectory of data dir."""
        from xoneaiagents.paths import get_rules_dir
        
        result = get_rules_dir()
        assert result == Path.home() / ".xoneai" / "rules"


class TestGetPermissionsDir:
    """Tests for get_permissions_dir() function."""
    
    def test_returns_permissions_subdir(self):
        """Should return permissions subdirectory of data dir."""
        from xoneaiagents.paths import get_permissions_dir
        
        result = get_permissions_dir()
        assert result == Path.home() / ".xoneai" / "permissions"


class TestGetStorageDir:
    """Tests for get_storage_dir() function."""
    
    def test_returns_storage_subdir(self):
        """Should return storage subdirectory of data dir."""
        from xoneaiagents.paths import get_storage_dir
        
        result = get_storage_dir()
        assert result == Path.home() / ".xoneai" / "storage"


class TestGetCheckpointsDir:
    """Tests for get_checkpoints_dir() function."""
    
    def test_returns_checkpoints_subdir(self):
        """Should return checkpoints subdirectory of data dir."""
        from xoneaiagents.paths import get_checkpoints_dir
        
        result = get_checkpoints_dir()
        assert result == Path.home() / ".xoneai" / "checkpoints"


class TestGetSnapshotsDir:
    """Tests for get_snapshots_dir() function."""
    
    def test_returns_snapshots_subdir(self):
        """Should return snapshots subdirectory of data dir."""
        from xoneaiagents.paths import get_snapshots_dir
        
        result = get_snapshots_dir()
        assert result == Path.home() / ".xoneai" / "snapshots"


class TestGetLearnDir:
    """Tests for get_learn_dir() function."""
    
    def test_returns_learn_subdir(self):
        """Should return learn subdirectory of data dir."""
        from xoneaiagents.paths import get_learn_dir
        
        result = get_learn_dir()
        assert result == Path.home() / ".xoneai" / "learn"


class TestGetProjectDataDir:
    """Tests for get_project_data_dir() function."""
    
    def test_returns_xoneai_in_cwd(self):
        """Should return .xoneai/ in current working directory."""
        from xoneaiagents.paths import get_project_data_dir
        
        result = get_project_data_dir()
        assert result == Path.cwd() / ".xoneai"
    
    def test_accepts_custom_project_path(self, tmp_path):
        """Should accept custom project path."""
        from xoneaiagents.paths import get_project_data_dir
        
        result = get_project_data_dir(tmp_path)
        assert result == tmp_path / ".xoneai"


class TestEnsureDir:
    """Tests for ensure_dir() function."""
    
    def test_creates_directory(self, tmp_path):
        """Should create directory if it doesn't exist."""
        from xoneaiagents.paths import ensure_dir
        
        test_dir = tmp_path / "test" / "nested" / "dir"
        assert not test_dir.exists()
        
        result = ensure_dir(test_dir)
        
        assert test_dir.exists()
        assert test_dir.is_dir()
        assert result == test_dir
    
    def test_returns_existing_directory(self, tmp_path):
        """Should return existing directory without error."""
        from xoneaiagents.paths import ensure_dir
        
        test_dir = tmp_path / "existing"
        test_dir.mkdir()
        
        result = ensure_dir(test_dir)
        
        assert result == test_dir


class TestGetMcpAuthPath:
    """Tests for get_mcp_auth_path() function."""
    
    def test_returns_mcp_auth_json(self):
        """Should return path to mcp-auth.json."""
        from xoneaiagents.paths import get_mcp_auth_path
        
        result = get_mcp_auth_path()
        assert result == Path.home() / ".xoneai" / "mcp-auth.json"


class TestConstants:
    """Tests for module constants."""
    
    def test_env_var_name(self):
        """ENV_VAR should be XONEAI_HOME."""
        from xoneaiagents.paths import ENV_VAR
        
        assert ENV_VAR == "XONEAI_HOME"
    
    def test_default_dir_name(self):
        """DEFAULT_DIR_NAME should be .xoneai."""
        from xoneaiagents.paths import DEFAULT_DIR_NAME
        
        assert DEFAULT_DIR_NAME == ".xoneai"
    
    def test_legacy_dir_name(self):
        """LEGACY_DIR_NAME should be .xone."""
        from xoneaiagents.paths import LEGACY_DIR_NAME
        
        assert LEGACY_DIR_NAME == ".xone"


class TestGetAllPaths:
    """Tests for get_all_paths() function."""
    
    def test_returns_dict_of_all_paths(self):
        """Should return dictionary with all path locations."""
        from xoneaiagents.paths import get_all_paths
        
        result = get_all_paths()
        
        assert isinstance(result, dict)
        assert "data_dir" in result
        assert "sessions" in result
        assert "skills" in result
        assert "plugins" in result
        assert "mcp" in result
        assert "docs" in result
        assert "rules" in result
        assert "permissions" in result
        assert "storage" in result
        assert "checkpoints" in result
        assert "snapshots" in result
        assert "learn" in result
        assert "mcp_auth" in result


class TestImportPerformance:
    """Tests for import performance."""
    
    def test_import_time_under_10ms(self):
        """Module import should be fast (no heavy deps)."""
        import time as time_module
        import sys as sys_module
        
        # Remove from cache if present
        if "xoneaiagents.paths" in sys_module.modules:
            del sys_module.modules["xoneaiagents.paths"]
        
        start = time_module.perf_counter()
        import xoneaiagents.paths as paths_module  # noqa: F401
        elapsed = time_module.perf_counter() - start
        
        # Should import in under 10ms (no heavy deps)
        assert elapsed < 0.01, f"Import took {elapsed*1000:.2f}ms, expected < 10ms"
