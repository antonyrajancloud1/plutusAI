# Generated by Django 5.0 on 2024-01-16 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plutusAI', '0017_remove_jobdetails_terminate_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexdetails',
            name='index_ltp',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='indexdetails',
            name='index_token',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
