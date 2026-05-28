# Generated manually to only add TelegramSettings model
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plutusAI", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TelegramSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user_id",
                    models.CharField(default=None, max_length=500, unique=True),
                ),
                (
                    "chat_id",
                    models.CharField(
                        blank=True, default=None, max_length=100, null=True
                    ),
                ),
                ("notify_on_error", models.BooleanField(default=False)),
            ],
        ),
    ]
