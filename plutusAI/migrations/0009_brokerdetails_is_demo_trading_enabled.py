# Generated by Django 5.0 on 2023-12-30 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plutusAI', '0008_brokerdetails_orderbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='brokerdetails',
            name='is_demo_trading_enabled',
            field=models.BooleanField(default=False),
        ),
    ]
