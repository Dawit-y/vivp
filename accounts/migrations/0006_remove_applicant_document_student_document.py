# Generated by Django 5.0.2 on 2024-06-07 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_applicant_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicant',
            name='document',
        ),
        migrations.AddField(
            model_name='student',
            name='document',
            field=models.FileField(blank=True, help_text='Upload final document when the work is done', null=True, upload_to='final_documents/'),
        ),
    ]
