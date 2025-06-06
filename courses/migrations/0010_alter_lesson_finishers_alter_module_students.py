# Generated by Django 5.1.4 on 2025-06-04 04:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_alter_module_finishers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='finishers',
            field=models.ManyToManyField(blank=True, related_name='lesson_finishers', to=settings.AUTH_USER_MODEL, verbose_name='Tugatganlar'),
        ),
        migrations.AlterField(
            model_name='module',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='module_students', to=settings.AUTH_USER_MODEL, verbose_name='Talabalar'),
        ),
    ]
