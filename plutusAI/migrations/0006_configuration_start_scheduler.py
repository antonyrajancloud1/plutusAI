# Generated by Django 5.0 on 2023-12-29 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plutusAI', '0005_delete_levels_configuration_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='start_scheduler',
            field=models.BooleanField(default=False),
        ),
    ]
