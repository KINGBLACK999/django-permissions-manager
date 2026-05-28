from typing import Callable, Optional

from ...domain.repositories.user_role_repository import UserRoleRepository


class RemoveRoleFromUserUseCase:
    """Application use case for removing a role assignment from a user.

    Attributes:
        on_revoked (Callable, optional): Callback invoked after a role is removed.
            Receives keyword arguments ``user_id`` and ``role_id``.
            Injected by the infrastructure layer (e.g. a Django signal).
    """

    def __init__(
        self,
        user_role_repository: UserRoleRepository,
        on_revoked: Optional[Callable[..., None]] = None,
    ):
        self.user_role_repository = user_role_repository
        self.on_revoked = on_revoked

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

        # Notify via callback (injected by infrastructure layer)
        if self.on_revoked:
            self.on_revoked(user_id=user_id, role_id=role_id)
