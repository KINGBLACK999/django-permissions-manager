import pytest
from django_permissions_manager.domain.value_objects.entity_reference import EntityReference


class TestEntityReference:
    def test_valid_reference_is_accepted(self):
        ref = EntityReference("Company", "42")
        assert ref.entity_type == "Company"
        assert ref.entity_id == "42"

    def test_empty_entity_type_raises(self):
        with pytest.raises(ValueError, match="entity_type"):
            EntityReference("", "42")

    def test_whitespace_entity_type_raises(self):
        with pytest.raises(ValueError, match="entity_type"):
            EntityReference("   ", "42")

    def test_empty_entity_id_raises(self):
        with pytest.raises(ValueError, match="entity_id"):
            EntityReference("Company", "")

    def test_whitespace_entity_id_raises(self):
        with pytest.raises(ValueError, match="entity_id"):
            EntityReference("Company", "   ")

    def test_equality_based_on_values(self):
        assert EntityReference("Company", "1") == EntityReference("Company", "1")

    def test_different_type_not_equal(self):
        assert EntityReference("Company", "1") != EntityReference("Team", "1")
