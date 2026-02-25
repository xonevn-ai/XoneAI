"""
Permissions checks for the Doctor CLI module.

Validates filesystem permissions for XoneAI directories.
"""

import os
import tempfile
from pathlib import Path

from ..models import (
    CheckCategory,
    CheckResult,
    CheckStatus,
    CheckSeverity,
    DoctorConfig,
)
from ..registry import register_check


def _check_dir_writable(path: Path) -> tuple:
    """Check if a directory is writable."""
    try:
        if not path.exists():
            return False, "does not exist"
        
        if not path.is_dir():
            return False, "not a directory"
        
        # Try to create a temp file
        test_file = path / ".xone_write_test"
        try:
            test_file.write_text("test")
            test_file.unlink()
            return True, "writable"
        except PermissionError:
            return False, "permission denied"
        except Exception as e:
            return False, str(e)
    except Exception as e:
        return False, str(e)


@register_check(
    id="permissions_home_xone",
    title="~/.xone Directory",
    description="Check ~/.xone directory permissions",
    category=CheckCategory.PERMISSIONS,
    severity=CheckSeverity.MEDIUM,
)
def check_permissions_home_xone(config: DoctorConfig) -> CheckResult:
    """Check ~/.xone directory permissions."""
    xone_dir = Path.home() / ".xone"
    
    if not xone_dir.exists():
        # Try to create it
        try:
            xone_dir.mkdir(parents=True, exist_ok=True)
            return CheckResult(
                id="permissions_home_xone",
                title="~/.xone Directory",
                category=CheckCategory.PERMISSIONS,
                status=CheckStatus.PASS,
                message="~/.xone created successfully",
                metadata={"path": str(xone_dir)},
            )
        except PermissionError:
            return CheckResult(
                id="permissions_home_xone",
                title="~/.xone Directory",
                category=CheckCategory.PERMISSIONS,
                status=CheckStatus.FAIL,
                message="Cannot create ~/.xone directory",
                remediation="Check home directory permissions",
                severity=CheckSeverity.HIGH,
            )
    
    writable, reason = _check_dir_writable(xone_dir)
    
    if writable:
        return CheckResult(
            id="permissions_home_xone",
            title="~/.xone Directory",
            category=CheckCategory.PERMISSIONS,
            status=CheckStatus.PASS,
            message=f"~/.xone is writable",
            metadata={"path": str(xone_dir)},
        )
    else:
        return CheckResult(
            id="permissions_home_xone",
            title="~/.xone Directory",
            category=CheckCategory.PERMISSIONS,
            status=CheckStatus.FAIL,
            message=f"~/.xone is not writable: {reason}",
            remediation="Fix permissions: chmod 755 ~/.xone",
            severity=CheckSeverity.HIGH,
        )


@register_check(
    id="permissions_project_xone",
    title=".xone Directory (Project)",
    description="Check project .xone directory permissions",
    category=CheckCategory.PERMISSIONS,
    severity=CheckSeverity.LOW,
)
def check_permissions_project_xone(config: DoctorConfig) -> CheckResult:
    """Check project .xone directory permissions."""
    xone_dir = Path.cwd() / ".xone"
    
    if not xone_dir.exists():
        return CheckResult(
            id="permissions_project_xone",
            title=".xone Directory (Project)",
            category=CheckCategory.PERMISSIONS,
            status=CheckStatus.SKIP,
            message="No .xone directory in current project",
        )
    
    writable, reason = _check_dir_writable(xone_dir)
    
    if writable:
        return CheckResult(
            id="permissions_project_xone",
            title=".xone Directory (Project)",
            category=CheckCategory.PERMISSIONS,
            status=CheckStatus.PASS,
            message=".xone is writable",
            metadata={"path": str(xone_dir)},
        )
    else:
        return CheckResult(
            id="permissions_project_xone",
            title=".xone Directory (Project)",
            category=CheckCategory.PERMISSIONS,
            status=CheckStatus.WARN,
            message=f".xone is not writable: {reason}",
            remediation="Fix permissions or use ~/.xone instead",
        )


@register_check(
    id="permissions_temp_dir",
    title="Temp Directory",
    description="Check temp directory permissions",
    category=CheckCategory.PERMISSIONS,
    severity=CheckSeverity.MEDIUM,
)
def check_permissions_temp_dir(config: DoctorConfig) -> CheckResult:
    """Check temp directory permissions."""
    temp_dir = Path(tempfile.gettempdir())
    
    try:
        # Try to create a temp file
        with tempfile.NamedTemporaryFile(delete=True) as f:
            f.write(b"test")
        
        return CheckResult(
            id="permissions_temp_dir",
            title="Temp Directory",
            category=CheckCategory.PERMISSIONS,
            status=CheckStatus.PASS,
            message=f"Temp directory writable: {temp_dir}",
            metadata={"path": str(temp_dir)},
        )
    except Exception as e:
        return CheckResult(
            id="permissions_temp_dir",
            title="Temp Directory",
            category=CheckCategory.PERMISSIONS,
            status=CheckStatus.FAIL,
            message=f"Temp directory not writable: {e}",
            remediation="Check TMPDIR environment variable and permissions",
            severity=CheckSeverity.HIGH,
        )


@register_check(
    id="permissions_cwd",
    title="Current Working Directory",
    description="Check current directory permissions",
    category=CheckCategory.PERMISSIONS,
    severity=CheckSeverity.INFO,
)
def check_permissions_cwd(config: DoctorConfig) -> CheckResult:
    """Check current directory permissions."""
    cwd = Path.cwd()
    
    writable, reason = _check_dir_writable(cwd)
    
    if writable:
        return CheckResult(
            id="permissions_cwd",
            title="Current Working Directory",
            category=CheckCategory.PERMISSIONS,
            status=CheckStatus.PASS,
            message=f"Current directory writable: {cwd}",
        )
    else:
        return CheckResult(
            id="permissions_cwd",
            title="Current Working Directory",
            category=CheckCategory.PERMISSIONS,
            status=CheckStatus.WARN,
            message=f"Current directory not writable: {reason}",
            details="Some features may not work without write access",
        )


@register_check(
    id="permissions_config_dir",
    title="Config Directory",
    description="Check ~/.config/xone directory",
    category=CheckCategory.PERMISSIONS,
    severity=CheckSeverity.LOW,
)
def check_permissions_config_dir(config: DoctorConfig) -> CheckResult:
    """Check ~/.config/xone directory."""
    config_dir = Path.home() / ".config" / "xone"
    
    if not config_dir.exists():
        # Check if we can create it
        try:
            config_dir.mkdir(parents=True, exist_ok=True)
            return CheckResult(
                id="permissions_config_dir",
                title="Config Directory",
                category=CheckCategory.PERMISSIONS,
                status=CheckStatus.PASS,
                message="~/.config/xone created successfully",
            )
        except Exception:
            return CheckResult(
                id="permissions_config_dir",
                title="Config Directory",
                category=CheckCategory.PERMISSIONS,
                status=CheckStatus.SKIP,
                message="~/.config/xone does not exist (will use ~/.xone)",
            )
    
    writable, reason = _check_dir_writable(config_dir)
    
    if writable:
        return CheckResult(
            id="permissions_config_dir",
            title="Config Directory",
            category=CheckCategory.PERMISSIONS,
            status=CheckStatus.PASS,
            message="~/.config/xone is writable",
        )
    else:
        return CheckResult(
            id="permissions_config_dir",
            title="Config Directory",
            category=CheckCategory.PERMISSIONS,
            status=CheckStatus.WARN,
            message=f"~/.config/xone not writable: {reason}",
        )
