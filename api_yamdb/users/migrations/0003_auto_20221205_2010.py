# Generated by Django 2.2.16 on 2022-12-05 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('moderator', 'Moderator'), ('user', 'User')], default='user', max_length=9),
        ),
    ]