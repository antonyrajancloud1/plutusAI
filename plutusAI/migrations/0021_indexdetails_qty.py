# Generated by Django 5.0 on 2024-01-20 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plutusAI', '0020_configuration_lots'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexdetails',
            name='qty',
            field=models.CharField(default=None, max_length=5),
        ),
    ]
