# Development

## Prerequisites

- Python ≥ 3.11
- Git

---

## Setup

```bash
git clone https://github.com/KINGBLACK999/django-permissions-manager.git
cd django-permissions-manager

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -e ".[dev]"
```

---

## Running tests

### All tests

```bash
make test
# or
pytest
```

### By feature

Each folder under `tests/` is a feature. Run any subset with `make` or the `-m` flag:

```bash
make test-roles
make test-permissions
make test-permission-groups
make test-user-roles
make test-django
```

Equivalent pytest commands:

```bash
pytest -m roles
pytest -m permissions
pytest -m permission_groups
pytest -m user_roles
pytest -m django_integration
```

### Combine markers

```bash
pytest -m "roles or permissions"
pytest -m "not django_integration"
```

---

## Test structure

Tests are organized by **feature** rather than by architectural layer. Every subfolder under `tests/` maps to a feature and its marker is applied automatically by `conftest.py`.

```
tests/
├── conftest.py                    # auto-applies markers from folder names
├── roles/
│   ├── test_role_entity.py
│   ├── test_role_name.py
│   ├── test_role_manager.py
│   ├── test_create_role.py
│   ├── test_update_role_permissions.py
│   ├── test_create_default_roles.py
│   ├── test_role_repository.py
│   └── test_role_mapper.py
├── permissions/
│   ├── test_permission_code.py
│   ├── test_permission_checker.py
│   ├── test_check_user_permission.py
│   ├── test_permission_mapper.py
│   └── test_permission_labels.py
├── permission_groups/
│   ├── test_create_permission_group.py
│   ├── test_assign_permission_group_to_role.py
│   └── test_permission_group_mapper.py
└── user_roles/
    ├── test_user_id.py
    ├── test_entity_reference.py
    ├── test_assign_role_to_user.py
    ├── test_remove_role_from_user.py
    ├── test_user_role_repository.py
    └── test_user_role_mapper.py
```

---

## Documentation

Install the docs dependencies:

```bash
pip install -e ".[docs]"
```

Serve locally with live reload:

```bash
mkdocs serve
# open http://127.0.0.1:8000
```

Build static site:

```bash
mkdocs build
```

The production site is deployed automatically to GitHub Pages on every push to `main` via `.github/workflows/docs.yml`.

---

## Project structure

```
django_permissions_manager/
├── domain/
│   ├── entities/          # Role, Permission, PermissionGroup, UserRole
│   ├── value_objects/     # RoleName, PermissionCode, UserId, EntityReference
│   ├── repositories/      # Abstract port interfaces
│   └── services/          # RoleManager, PermissionChecker
├── application/
│   └── use_cases/         # One class per use case
└── infrastructure/
    └── django/
        ├── models/        # ORM models
        ├── repositories/  # Django ORM adapters (implement domain ports)
        ├── mappers/       # Domain ↔ ORM conversions
        ├── migrations/
        ├── views/         # Mixins and auth backend
        ├── management/    # create_default_roles command
        ├── signals.py
        ├── apps.py
        └── settings.py
```

---

## Making a release

1. Bump `version` in `pyproject.toml`.
2. Update the changelog (if any).
3. Push a tag:

```bash
git tag v0.2.0
git push origin v0.2.0
```

4. Build and upload to PyPI:

```bash
pip install build twine
python -m build
twine upload dist/*
```
