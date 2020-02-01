# Generated by Django 2.2.5 on 2020-02-01 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_login_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(blank=True, choices=[('english', 'English'), ('korean', 'Korea')], default='korean', max_length=10),
        ),
    ]
