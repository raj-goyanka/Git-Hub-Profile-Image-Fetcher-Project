# Generated by Django 3.2.4 on 2021-07-02 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('img', '0002_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='varify',
            new_name='verify',
        ),
    ]