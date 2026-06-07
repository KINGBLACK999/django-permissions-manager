"""
Auto-applies pytest markers based on the feature folder name.

Each test under tests/<feature>/ is automatically tagged with @pytest.mark.<feature>,
so you can run a single feature with:

    pytest -m roles
    pytest -m permissions
    pytest -m permission_groups
    pytest -m user_roles
    pytest -m django_integration
"""
import pytest
from pathlib import Path


def pytest_collection_modifyitems(config, items):
    tests_root = Path(config.rootdir) / "tests"
    for item in items:
        try:
            feature = Path(item.fspath).relative_to(tests_root).parts[0]
            item.add_marker(getattr(pytest.mark, feature))
        except (ValueError, IndexError):
            pass
