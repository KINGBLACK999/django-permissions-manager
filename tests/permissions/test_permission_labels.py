"""
Tests for the PERMISSIONS_MANAGER_PERMISSION_LABELS setting.

_update_permission_labels is a pure function that receives its dependencies
injected, so tests need no patching — just pass a MagicMock as the model.
"""
from unittest.mock import MagicMock

from django_permissions_manager.infrastructure.django.apps import _update_permission_labels


class TestUpdatePermissionLabels:
    def test_updates_matching_permission(self):
        MockPermission = MagicMock()
        _update_permission_labels(MockPermission, {"change_role": "Puede modificar el rol"})

        MockPermission.objects.filter.assert_called_once_with(
            content_type__app_label="django_permissions_manager",
            codename="change_role",
        )
        MockPermission.objects.filter.return_value.update.assert_called_once_with(
            name="Puede modificar el rol"
        )

    def test_updates_each_label_independently(self):
        MockPermission = MagicMock()
        labels = {
            "change_role": "Puede modificar el rol",
            "assign_role": "Puede asignar roles",
        }
        _update_permission_labels(MockPermission, labels)

        assert MockPermission.objects.filter.call_count == 2

    def test_does_nothing_when_labels_is_empty_dict(self):
        MockPermission = MagicMock()
        _update_permission_labels(MockPermission, {})

        MockPermission.objects.filter.assert_not_called()

    def test_does_nothing_when_labels_is_none(self):
        MockPermission = MagicMock()
        _update_permission_labels(MockPermission, None)

        MockPermission.objects.filter.assert_not_called()
