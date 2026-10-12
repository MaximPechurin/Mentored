from rest_framework.permissions import BasePermission


class IsCrmUser(BasePermission):
    """
    Доступ к CRM: суперюзер ИЛИ пользователь с флагом crm_access.
    Раньше был только is_superuser — теперь можно дать доступ
    руководителю без прав Django-админа.
    """
    message = 'Acceso solo para el equipo de MENTORED.'

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        return bool(user.is_superuser or getattr(user, 'crm_access', False))