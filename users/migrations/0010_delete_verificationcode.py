# Generated by Django 5.1.4 on 2025-07-12 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_is_active'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VerificationCode',
        ),
    ]
