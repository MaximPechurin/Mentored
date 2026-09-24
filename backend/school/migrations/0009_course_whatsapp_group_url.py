from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0008_assignment_is_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='whatsapp_group_url',
            field=models.URLField(
                blank=True,
                help_text='Если заполнено - студент увидит на странице курса блок '
                          '«Группа WhatsApp», клик по которому открывает эту ссылку.',
                verbose_name='Ссылка на группу WhatsApp',
            ),
        ),
    ]
