# Generated by Django 2.2.5 on 2019-09-27 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_auto_20190927_1333'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='room',
            new_name='room_type',
        ),
    ]
