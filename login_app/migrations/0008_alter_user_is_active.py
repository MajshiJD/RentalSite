# Generated by Django 5.0 on 2024-01-07 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0007_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
