from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from projects.models import Project


class Command(BaseCommand):
    help = "Delete existing project/request records and non-staff users so only new live data remains."

    def add_arguments(self, parser):
        parser.add_argument(
            "--yes",
            action="store_true",
            help="Confirm destructive cleanup.",
        )
        parser.add_argument(
            "--keep-users",
            action="store_true",
            help="Keep existing users and only delete project/request data.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if not options["yes"]:
            raise CommandError("This command is destructive. Re-run with --yes to proceed.")

        User = get_user_model()

        project_qs = Project.objects.all()
        project_count = project_qs.count()
        # Project-related records are cascade-deleted through FK relations.
        deleted_project_rows, _ = project_qs.delete()

        users_deleted = 0
        if not options["keep_users"]:
            removable_users = User.objects.filter(is_superuser=False, is_staff=False)
            users_deleted = removable_users.count()
            removable_users.delete()

        self.stdout.write(self.style.SUCCESS("Live cleanup completed."))
        self.stdout.write(f"Projects removed: {project_count}")
        self.stdout.write(f"Project-related rows removed (total): {deleted_project_rows}")
        self.stdout.write(f"Users removed (non-staff/non-superuser): {users_deleted}")
