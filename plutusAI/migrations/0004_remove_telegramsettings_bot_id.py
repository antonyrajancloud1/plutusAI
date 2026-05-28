from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("plutusAI", "0003_logdetails_telegrambotconfig_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="telegramsettings",
            name="bot_id",
        ),
    ]
