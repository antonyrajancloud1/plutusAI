# Generated by Django 5.0 on 2024-01-16 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plutusAI', '0018_indexdetails_index_ltp_indexdetails_index_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='indexdetails',
            old_name='index_ltp',
            new_name='ltp',
        ),
        migrations.AddField(
            model_name='indexdetails',
            name='last_updated_time',
            field=models.CharField(default=None, max_length=250),
        ),
    ]
