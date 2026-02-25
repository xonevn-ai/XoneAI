# Package Manager Example

This example demonstrates how to use the XoneAI package manager for installing and managing Python packages with security defaults.

## Features Demonstrated

- Installing packages with version constraints
- Listing installed packages
- Searching for packages on PyPI
- Managing package index configuration
- Security features (dependency confusion prevention)

## Quick Start

```bash
# Run the example
python package_manager_example.py
```

## CLI Commands

### Install Packages

```bash
# Install a package
xoneai install requests

# Install with version constraint
xoneai install "requests>=2.28"

# Install multiple packages
xoneai install requests httpx aiohttp

# Upgrade existing package
xoneai install requests --upgrade

# JSON output
xoneai install requests --json
```

### Uninstall Packages

```bash
# Uninstall a package
xoneai uninstall requests

# Uninstall without confirmation
xoneai uninstall requests --yes
```

### List Packages

```bash
# List all installed packages
xoneai package list

# JSON output
xoneai package list --json
```

### Search Packages

```bash
# Search PyPI
xoneai package search langchain

# JSON output
xoneai package search langchain --json
```

### Index Configuration

```bash
# Show current index settings
xoneai package index show --json

# Set custom index
xoneai package index set https://pypi.mycompany.com/simple

# Reset to PyPI default
xoneai package index set https://pypi.org/simple
```

## Security Features

By default, only the primary index (PyPI) is used. Extra indexes are blocked to prevent dependency confusion attacks.

```bash
# This will FAIL (extra index not allowed by default)
xoneai install mypackage --extra-index-url https://other.index.com/simple

# Explicitly allow extra index (shows security warning)
xoneai install mypackage \
  --extra-index-url https://other.index.com/simple \
  --allow-extra-index
```

## Environment Variables

- `XONEAI_PACKAGE_INDEX_URL` - Override primary index URL
- `PIP_INDEX_URL` - Fallback to pip's index URL
