from ...domain.repositories.user_role_repository import UserRoleRepository
from ...infrastructure.django.signals import role_revoked


class RemoveRoleFromUserUseCase:
    """Application use case for removing a role assignment from a user."""

    def __init__(self, user_role_repository: UserRoleRepository):
        self.user_role_repository = user_role_repository

    def execute(self, user_role_id: str) -> None:
        """Removes a user-role assignment.

        Args:
            user_role_id: The UUID of the assignment to remove.

        Raises:
            ValueError: If the assignment does not exist.
        """
        assignment = self.user_role_repository.get_by_id(user_role_id)
        if not assignment:
            raise ValueError(f"Assignment '{user_role_id}' does not exist.")

        user_id = assignment.user_id.value
        role_id = assignment.role.id

        self.user_role_repository.delete(user_role_id)

        role_revoked.send(
            sender=self.__class__,
            user_id=user_id,
            role_id=role_id,
        )
