import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from django_permissions_manager.application.use_cases.create_role import CreateRoleUseCase
from django_permissions_manager.domain.exceptions.role_exceptions import RoleAlreadyExistsException
from django_permissions_manager.domain.services.role_factory import RoleFactory
from django_permissions_manager.domain.services.role_manager import RoleManager


class TestCreateRoleUseCase:
    def setup_method(self):
        self.role_repo = MagicMock()
        self.perm_repo = MagicMock()
        self.role_manager = MagicMock()
        self.use_case = CreateRoleUseCase(
            role_repository=self.role_repo,
            permission_repository=self.perm_repo,
            role_manager=self.role_manager,
        )

    def test_creates_global_role_and_returns_dto(self):
        self.role_manager.ensure_role_name_is_unique.return_value = None
        self.perm_repo.get_by_code.return_value = None

        dto = self.use_case.execute(name="Editor", description="Edit content")

        self.role_repo.save.assert_called_once()
        assert dto.name == "Editor"
        assert dto.entity_type is None

    def test_raises_when_role_name_already_taken(self):
        self.role_manager.ensure_role_name_is_unique.side_effect = RoleAlreadyExistsException("exists")

        with pytest.raises(RoleAlreadyExistsException):
            self.use_case.execute(name="Editor")

        self.role_repo.save.assert_not_called()

    def test_validates_entity_when_entity_service_provided(self):
        entity_service = MagicMock()
        entity_service.exists.return_value = False
        use_case = CreateRoleUseCase(
            role_repository=self.role_repo,
            permission_repository=self.perm_repo,
            role_manager=self.role_manager,
            entity_service=entity_service,
        )

        with pytest.raises(ValueError, match="does not exist"):
            use_case.execute(name="Admin", entity_type="Company", entity_id="999")

        self.role_repo.save.assert_not_called()

    def test_skips_entity_validation_when_no_entity_service(self):
        self.role_manager.ensure_role_name_is_unique.return_value = None
        dto = self.use_case.execute(name="Admin", entity_type="Company", entity_id="999")
        assert dto.entity_type == "Company"

    def test_creates_scoped_role(self):
        self.role_manager.ensure_role_name_is_unique.return_value = None
        dto = self.use_case.execute(name="Admin", entity_type="Company", entity_id="1")
        assert dto.entity_type == "Company"
        assert dto.entity_id == "1"


class TestCreateRoleUseCaseModeValidation:
    """Tests that the MODE setting is enforced by the use case."""

    def _make_use_case(self, mode: str):
        role_repo = MagicMock()
        perm_repo = MagicMock()
        role_manager = MagicMock()
        role_manager.ensure_role_name_is_unique.return_value = None
        perm_repo.get_by_code.return_value = None
        return CreateRoleUseCase(
            role_repository=role_repo,
            permission_repository=perm_repo,
            role_manager=role_manager,
            mode=mode,
        )

    # ---- GLOBAL mode ----

    def test_global_mode_allows_global_role(self):
        uc = self._make_use_case("GLOBAL")
        dto = uc.execute(name="GlobalAdmin")
        assert dto.name == "GlobalAdmin"
        assert dto.entity_type is None

    def test_global_mode_rejects_scoped_role(self):
        uc = self._make_use_case("GLOBAL")
        with pytest.raises(ValueError, match="GLOBAL mode"):
            uc.execute(name="ScopedAdmin", entity_type="Company", entity_id="1")

    # ---- ENTITY mode ----

    def test_entity_mode_allows_scoped_role(self):
        uc = self._make_use_case("ENTITY")
        dto = uc.execute(name="ScopedAdmin", entity_type="Company", entity_id="1")
        assert dto.entity_type == "Company"

    def test_entity_mode_rejects_global_role(self):
        uc = self._make_use_case("ENTITY")
        with pytest.raises(ValueError, match="ENTITY mode"):
            uc.execute(name="GlobalAdmin")

    # ---- BOTH mode ----

    def test_both_mode_allows_global_role(self):
        uc = self._make_use_case("BOTH")
        dto = uc.execute(name="GlobalAdmin")
        assert dto.entity_type is None

    def test_both_mode_allows_scoped_role(self):
        uc = self._make_use_case("BOTH")
        dto = uc.execute(name="ScopedAdmin", entity_type="Company", entity_id="1")
        assert dto.entity_type == "Company"

    # ---- Invalid mode ----

    def test_invalid_mode_raises_on_construction(self):
        with pytest.raises(ValueError, match="Invalid mode"):
            CreateRoleUseCase(
                role_repository=MagicMock(),
                permission_repository=MagicMock(),
                role_manager=MagicMock(),
                mode="INVALID",
            )
