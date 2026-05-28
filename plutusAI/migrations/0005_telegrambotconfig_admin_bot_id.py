from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plutusAI", "0004_remove_telegramsettings_bot_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="telegrambotconfig",
            name="admin_bot_id",
            field=models.CharField(default="", max_length=200),
        ),
    ]
