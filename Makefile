.PHONY: test test-roles test-permissions test-permission-groups test-user-roles test-django

## Run all tests
test:
	pytest

## Run tests for a specific feature
test-roles:
	pytest -m roles -v

test-permissions:
	pytest -m permissions -v

test-permission-groups:
	pytest -m permission_groups -v

test-user-roles:
	pytest -m user_roles -v

test-django:
	pytest -m django_integration -v
