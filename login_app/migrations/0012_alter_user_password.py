# Generated by Django 5.0 on 2024-01-07 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0011_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=200),
        ),
    ]
