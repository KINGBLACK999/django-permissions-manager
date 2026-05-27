from django.core.management.base import BaseCommand
from ....application.use_cases.create_default_roles import CreateDefaultRolesUseCase
from ..repositories.django_role_repository import DjangoRoleRepository
from ...django.settings import app_settings


class Command(BaseCommand):
    help = 'Creates default system roles defined in PERMISSIONS_MANAGER_DEFAULT_ROLES'

    def handle(self, *args, **options):
        self.stdout.write('Initializing default roles...')

        default_roles = app_settings.DEFAULT_ROLES
        if not default_roles:
            self.stdout.write(self.style.WARNING('No default roles configured. Set PERMISSIONS_MANAGER_DEFAULT_ROLES in settings.'))
            return

        use_case = CreateDefaultRolesUseCase(role_repository=DjangoRoleRepository())
        use_case.execute(default_roles)

        self.stdout.write(self.style.SUCCESS(f'Successfully initialized {len(default_roles)} default role(s).'))
