# Generated by Django 5.0 on 2024-06-15 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plutusAI', '0035_alter_orderbook_entry_time_alter_orderbook_exit_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderbook',
            name='strategy',
            field=models.CharField(blank=True, default=None, max_length=250, null=True),
        ),
    ]