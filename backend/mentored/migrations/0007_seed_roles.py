from django.db import migrations


ROLES = [
    ('student', 'Студент', 'Учащийся - доступ к купленным курсам, сдача домашних заданий'),
    ('teacher', 'Преподаватель', 'Ментор/куратор - ведёт курсы, проверяет домашние задания'),
]


def seed_roles(apps, schema_editor):
    Role = apps.get_model('mentored', 'Role')
    for codename, name, description in ROLES:
        Role.objects.get_or_create(
            codename=codename,
            defaults={'name': name, 'description': description},
        )


def unseed_roles(apps, schema_editor):
    Role = apps.get_model('mentored', 'Role')
    Role.objects.filter(codename__in=[codename for codename, _, _ in ROLES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mentored', '0006_role_user_roles'),
    ]

    operations = [
        migrations.RunPython(seed_roles, unseed_roles),
    ]
