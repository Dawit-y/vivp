# Generated by Django 5.0.2 on 2024-03-31 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_alter_application_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='default_text',
        ),
        migrations.AddField(
            model_name='certificate',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='certificates/'),
        ),
    ]