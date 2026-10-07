from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    """
    Доступ только суперюзерам. Используется для всех эндпоинтов CRM.
    По ТЗ 'руководитель проекта' решено принимать is_superuser, без отдельной роли.
    """
    message = 'CRM доступна только руководителю проекта.'

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )