# Generated by Django 5.1.6 on 2025-06-11 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_background_profile_local_background_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Display Name'),
        ),
    ]
