# Generated by Django 4.1.5 on 2023-01-13 23:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('image', models.ImageField(default='person.png', upload_to=users.models.PathRename('images/users'))),
                ('birthday', models.DateField(blank=True, null=True)),
                ('join_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('roles', models.CharField(blank=True, choices=[('user', 'User'), ('manager', 'Manager'), ('support', 'Support'), ('admin', 'Admin')], default='user', max_length=30, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
            },
        ),
    ]
