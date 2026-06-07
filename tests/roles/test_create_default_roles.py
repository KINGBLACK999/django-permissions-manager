import pytest
from unittest.mock import MagicMock

from django_permissions_manager.application.use_cases.create_default_roles import CreateDefaultRolesUseCase


class TestCreateDefaultRolesUseCase:
    def setup_method(self):
        self.role_repo = MagicMock()
        self.use_case = CreateDefaultRolesUseCase(role_repository=self.role_repo)

    def test_creates_role_when_it_does_not_exist(self):
        self.role_repo.get_by_name.return_value = None

        self.use_case.execute([{"name": "Administrator", "description": "Full access"}])

        self.role_repo.save.assert_called_once()

    def test_skips_role_when_it_already_exists(self):
        self.role_repo.get_by_name.return_value = MagicMock()

        self.use_case.execute([{"name": "Administrator", "description": "Full access"}])

        self.role_repo.save.assert_not_called()

    def test_empty_list_makes_no_repository_calls(self):
        self.use_case.execute([])

        self.role_repo.get_by_name.assert_not_called()
        self.role_repo.save.assert_not_called()

    def test_creates_only_missing_roles_from_mixed_list(self):
        self.role_repo.get_by_name.side_effect = lambda name, _: (
            MagicMock() if name == "Administrator" else None
        )

        self.use_case.execute([
            {"name": "Administrator", "description": "Full access"},
            {"name": "Editor", "description": "Edit content"},
        ])

        assert self.role_repo.save.call_count == 1
        saved = self.role_repo.save.call_args[0][0]
        assert saved.name.value == "Editor"

    def test_saved_role_is_a_system_role(self):
        self.role_repo.get_by_name.return_value = None

        self.use_case.execute([{"name": "Viewer", "description": "Read only"}])

        saved = self.role_repo.save.call_args[0][0]
        assert saved.is_system_role is True

    def test_description_defaults_to_empty_when_not_provided(self):
        self.role_repo.get_by_name.return_value = None

        self.use_case.execute([{"name": "Viewer"}])

        saved = self.role_repo.save.call_args[0][0]
        assert saved.description == ""

    def test_checks_global_scope_for_existing_role(self):
        self.role_repo.get_by_name.return_value = None

        self.use_case.execute([{"name": "Admin", "description": ""}])

        self.role_repo.get_by_name.assert_called_once_with("Admin", None)

    def test_processes_multiple_new_roles(self):
        self.role_repo.get_by_name.return_value = None

        self.use_case.execute([
            {"name": "Admin", "description": ""},
            {"name": "Editor", "description": ""},
            {"name": "Viewer", "description": ""},
        ])

        assert self.role_repo.save.call_count == 3
