from django.contrib.auth.models import User


def is_admin_user(user: User) -> bool:
    return user.is_staff or user.is_superuser


def can_access_project(user: User, project) -> bool:
    if is_admin_user(user):
        return True
    return project.customer_id == user.id
