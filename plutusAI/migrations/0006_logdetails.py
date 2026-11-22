# LogDetails was created on the live DB outside migrations (SQL dump), so this
# migration only creates the table where it is missing (fresh / test databases).

from django.db import migrations, models


def create_if_missing(apps, schema_editor):
    model = apps.get_model("plutusAI", "LogDetails")
    if model._meta.db_table not in schema_editor.connection.introspection.table_names():
        schema_editor.create_model(model)


class Migration(migrations.Migration):
    # MySQL can't run DDL (create_model) inside a transaction, which would make a
    # fresh MySQL database fail here. Nothing to roll back, so run non-atomically.
    atomic = False

    dependencies = [
        ("plutusAI", "0005_telegrambotconfig_admin_bot_id"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name="LogDetails",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("user_id", models.CharField(default=None, max_length=100)),
                        ("index_name", models.CharField(default=None, max_length=100)),
                        ("log", models.CharField(default=None, max_length=500, null=True)),
                        ("log_type", models.CharField(default="trigger", max_length=10, null=True)),
                        ("time", models.CharField(default=None, max_length=100, null=True)),
                    ],
                ),
            ],
        ),
        # Runs after the state change above so the model is available here.
        migrations.RunPython(create_if_missing, migrations.RunPython.noop),
    ]
