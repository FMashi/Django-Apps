# Generated by Django 4.1.5 on 2023-01-15 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_user_user_profile_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_profile',
            old_name='User',
            new_name='user',
        ),
    ]
