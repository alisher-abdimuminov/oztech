# Generated by Django 5.1.4 on 2025-06-04 04:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_alter_course_students'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='finishers',
            field=models.ManyToManyField(blank=True, related_name='module_finishers', to=settings.AUTH_USER_MODEL, verbose_name='Bitirganlar'),
        ),
    ]
