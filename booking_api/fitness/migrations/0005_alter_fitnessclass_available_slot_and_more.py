# Generated by Django 5.2.3 on 2025-06-11 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0004_remove_booking_user_booking_client_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitnessclass',
            name='available_slot',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='fitnessclass',
            name='max_capacity',
            field=models.IntegerField(default=5),
        ),
    ]
