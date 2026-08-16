from django.contrib.admin.apps import AdminConfig


class MentoredAdminConfig(AdminConfig):
    """ Подключает кастомный AdminSite (группировка + гайд). """
    default_site = 'config.admin.MentoredAdminSite'
