# Generated by Django 4.2.6 on 2023-12-22 05:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_django', '0002_remove_car_isaccepted_message_isaccepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='main_mech',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='test_django.mechanic'),
        ),
    ]
