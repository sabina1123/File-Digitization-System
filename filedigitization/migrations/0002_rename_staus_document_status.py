# Generated by Django 5.1.4 on 2024-12-23 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filedigitization', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='staus',
            new_name='status',
        ),
    ]
