# Generated by Django 5.0.2 on 2024-05-19 11:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_post_system_coordinator_alter_post_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasksubmission',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tasksubmission',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
