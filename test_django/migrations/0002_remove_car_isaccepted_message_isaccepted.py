# Generated by Django 4.2.6 on 2023-12-22 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_django', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='isAccepted',
        ),
        migrations.AddField(
            model_name='message',
            name='isAccepted',
            field=models.BooleanField(default=False),
        ),
    ]
