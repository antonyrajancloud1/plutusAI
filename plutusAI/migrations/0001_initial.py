# Generated by Django 5.1.5 on 2025-04-11 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BrokerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=None, max_length=500)),
                ('broker_name', models.CharField(default=None, max_length=250)),
                ('broker_user_id', models.CharField(default=None, max_length=250)),
                ('broker_user_name', models.CharField(blank=True, default=None, max_length=250)),
                ('broker_mpin', models.CharField(blank=True, default=None, max_length=250)),
                    ('broker_api_token', models.CharField(default=None, max_length=250)),
                ('broker_qr', models.CharField(blank=True, default=None, max_length=250)),
                ('token_status', models.CharField(default=None, max_length=250)),
                ('is_demo_trading_enabled', models.BooleanField(default=False)),
                ('index_group', models.CharField(default=None, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='CandleData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index_name', models.CharField(default=None, max_length=50)),
                ('token', models.CharField(default=None, max_length=50)),
                ('time', models.CharField(default=None, max_length=50)),
                ('open', models.CharField(default=None, max_length=50)),
                ('high', models.CharField(default=None, max_length=50)),
                ('low', models.CharField(default=None, max_length=50)),
                ('close', models.CharField(default=None, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=None, max_length=500)),
                ('levels', models.CharField(default=None, max_length=5000)),
                ('index_name', models.CharField(default='nifty50', max_length=50)),
                ('start_scheduler', models.BooleanField(default=False)),
                ('strike', models.CharField(default='10', max_length=5)),
                ('is_place_sl_required', models.BooleanField(default=True)),
                ('trend_check_points', models.CharField(default='15', max_length=10)),
                ('trailing_points', models.CharField(default='10', max_length=10)),
                ('initial_sl', models.CharField(default='10', max_length=10)),
                ('safe_sl', models.CharField(default='3', max_length=10)),
                ('target_for_safe_sl', models.CharField(default='10', max_length=10)),
                ('status', models.CharField(default='stopped', max_length=250)),
                ('lots', models.CharField(default=None, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='FlashDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=None, max_length=100)),
                ('index_name', models.CharField(default=None, max_length=20)),
                ('strike', models.CharField(default=None, max_length=10)),
                ('max_profit', models.CharField(default=None, max_length=20)),
                ('max_loss', models.CharField(default=None, max_length=20)),
                ('trend_check_points', models.CharField(default='15', max_length=10)),
                ('trailing_points', models.CharField(default='10', max_length=10)),
                ('is_demo_trading_enabled', models.BooleanField(default=True)),
                ('lots', models.CharField(default=None, max_length=10)),
                ('status', models.CharField(default=None, max_length=20)),
                ('average_points', models.CharField(default=None, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='IndexDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index_name', models.CharField(default=None, max_length=50)),
                ('index_group', models.CharField(default=None, max_length=50)),
                ('index_token', models.CharField(default=None, max_length=50)),
                ('ltp', models.CharField(default=None, max_length=50)),
                ('last_updated_time', models.CharField(default=None, max_length=250)),
                ('qty', models.CharField(default=None, max_length=5)),
                ('current_expiry', models.CharField(default=None, max_length=50)),
                ('next_expiry', models.CharField(default=None, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='JobDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=None, max_length=500)),
                ('index_name', models.CharField(default=None, max_length=50)),
                ('job_id', models.CharField(default=None, max_length=300)),
                ('strategy', models.CharField(default=None, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='ManualOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=None, max_length=100)),
                ('index_name', models.CharField(default=None, max_length=100)),
                ('target', models.CharField(default=None, max_length=100)),
                ('stop_loss', models.CharField(default=None, max_length=100)),
                ('order_status', models.CharField(default=None, max_length=100)),
                ('strike', models.CharField(default=None, max_length=100)),
                ('lots', models.CharField(default=None, max_length=100)),
                ('trigger', models.CharField(default=None, max_length=100)),
                ('time', models.CharField(default=None, max_length=100)),
                ('order_id', models.CharField(default=None, max_length=100)),
                ('unique_order_id', models.CharField(default=None, max_length=100)),
                ('current_premium', models.CharField(default=None, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OrderBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=None, max_length=500)),
                ('entry_time', models.CharField(default=None, max_length=500)),
                ('exit_time', models.CharField(blank=True, default=None, max_length=500, null=True)),
                ('script_name', models.CharField(default=None, max_length=250)),
                ('qty', models.CharField(default=None, max_length=250)),
                ('entry_price', models.CharField(blank=True, default=None, max_length=250)),
                ('exit_price', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('status', models.CharField(default=None, max_length=250)),
                ('total', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('strategy', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('index_name', models.CharField(default=None, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=None, max_length=500)),
                ('registed_date', models.CharField(default=None, max_length=200)),
                ('renew_date', models.CharField(default=None, max_length=200)),
                ('opted_index', models.CharField(default=None, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ScalperDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=None, max_length=500)),
                ('index_name', models.CharField(default=None, max_length=50)),
                ('strike', models.CharField(default=None, max_length=10)),
                ('target', models.CharField(default=None, max_length=100)),
                ('is_demo_trading_enabled', models.BooleanField(default=True)),
                ('use_full_capital', models.BooleanField(default=False)),
                ('lots', models.CharField(default=None, max_length=10)),
                ('on_candle_close', models.BooleanField(default=False)),
                ('status', models.CharField(default=None, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='UserAuthTokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=None, max_length=500)),
                ('refreshToken', models.CharField(default=None, max_length=2000)),
                ('jwtToken', models.CharField(default=None, max_length=2000)),
                ('feedToken', models.CharField(default=None, max_length=2000)),
                ('last_updated_time', models.CharField(default=None, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='WebhookDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=None, max_length=100)),
                ('index_name', models.CharField(default=None, max_length=100)),
                ('target', models.CharField(default=None, max_length=100, null=True)),
                ('order_status', models.CharField(default=None, max_length=100)),
                ('time', models.CharField(default=None, max_length=100)),
                ('is_demo_trading_enabled', models.BooleanField(default=True)),
                ('strategy', models.CharField(default=None, max_length=100)),
                ('order_id', models.CharField(default=None, max_length=100)),
                ('unique_order_id', models.CharField(default=None, max_length=100)),
                ('current_premium', models.CharField(default=None, max_length=100)),
            ],
        ),
    ]
