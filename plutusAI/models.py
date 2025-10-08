import json

from django.db import models


# Create your models here.

class Configuration(models.Model):
    user_id = models.CharField(max_length=500, default=None)
    levels = models.CharField(max_length=5000, default=None)
    index_name = models.CharField(max_length=50, default='nifty50')
    start_scheduler = models.BooleanField(default=False)
    strike = models.CharField(max_length=5, default='10')
    is_place_sl_required = models.BooleanField(default=True)
    trend_check_points = models.CharField(max_length=10, default='15')
    trailing_points = models.CharField(max_length=10, default='10')
    initial_sl = models.CharField(max_length=10, default='10')
    safe_sl = models.CharField(max_length=10, default='3')
    target_for_safe_sl = models.CharField(max_length=10, default='10')
    status = models.CharField(max_length=250, default='stopped')
    lots = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.index_name

    @classmethod
    def search_by_name(cls, query):
        return cls.objects.filter(name__icontains=query)


class OrderBook(models.Model):
    user_id = models.CharField(max_length=500, default=None)
    entry_time = models.CharField(max_length=500, default=None)
    exit_time = models.CharField(max_length=500, default=None, blank=True, null=True)
    script_name = models.CharField(max_length=250, default=None)
    qty = models.CharField(max_length=250, default=None)
    entry_price = models.CharField(max_length=250, default=None, blank=True)
    exit_price = models.CharField(max_length=250, default=None, blank=True, null=True)
    status = models.CharField(max_length=250, default=None)
    total = models.CharField(max_length=250, default=None, blank=True, null=True)
    strategy = models.CharField(max_length=250, default=None, blank=True, null=True)
    index_name = models.CharField(max_length=50, default=None)
    index_group = models.CharField(max_length=20, default="indian_index", null=True)
    order_id = models.CharField(max_length=20, default=None, null=True)
    position_id = models.CharField(max_length=20, default=None, null=True)
    def __str__(self):
        return "{" + f"user_id:{self.user_id}, script_name:{self.script_name}, entry_time:{self.entry_time}, strategy:{self.strategy} ,exit_time:{self.exit_time},total:{self.total},index_name:{self.index_name}" + "}"

    @classmethod
    def search_by_name(cls, query):
        return cls.objects.filter(name__icontains=query)


class BrokerDetails(models.Model):
    user_id = models.CharField(max_length=500, default=None,null=True)
    broker_name = models.CharField(max_length=250, default=None,null=True)
    broker_user_id = models.CharField(max_length=250, default=None,null=True)
    broker_user_name = models.CharField(max_length=250, default=None, blank=True,null=True)
    broker_mpin = models.CharField(max_length=250, default=None, blank=True ,null=True)
    broker_api_token = models.CharField(max_length=250, default=None,null=True)
    broker_qr = models.CharField(max_length=250, default=None, blank=True,null=True)
    token_status = models.CharField(max_length=250, default=None,null=True)
    is_demo_trading_enabled = models.BooleanField(default=False,null=True)
    index_group = models.CharField(max_length=20, default="indian_index",null=True)
    broker_password = models.CharField(max_length=250, default=None,null=True)
    broker_forex_server = models.CharField(max_length=250, default=None,null=True)

    def __str__(self):
        return self.broker_name

    @classmethod
    def search_by_name(cls, query):
        return cls.objects.filter(name__icontains=query)


class IndexDetails(models.Model):
    index_name = models.CharField(max_length=50, default=None)
    index_group = models.CharField(max_length=20, default="indian_index")
    index_token = models.CharField(max_length=50, default=None)
    ltp = models.CharField(max_length=50, default=None)
    last_updated_time = models.CharField(max_length=250, default=None)
    qty = models.CharField(max_length=5, default=None)
    current_expiry = models.CharField(max_length=50, default=None)
    next_expiry = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.index_name

    @classmethod
    def search_by_name(cls, query):
        return cls.objects.filter(name__icontains=query)


class JobDetails(models.Model):
    user_id = models.CharField(max_length=500, default=None)
    index_name = models.CharField(max_length=50, default=None)
    job_id = models.CharField(max_length=300, default=None)
    strategy = models.CharField(max_length=300, default=None)

    def __str__(self):
        return self.index_name

    @classmethod
    def search_by_name(cls, query):
        return cls.objects.filter(name__icontains=query)


class PaymentDetails(models.Model):
    user_id = models.CharField(max_length=500, default=None)
    registed_date = models.CharField(max_length=200, default=None)
    renew_date = models.CharField(max_length=200, default=None)
    opted_index = models.CharField(max_length=500, default=None)

    @classmethod
    def search_by_name(cls, query):
        return cls.objects.filter(name__icontains=query)


class ScalperDetails(models.Model):
    user_id = models.CharField(max_length=500, default=None)
    index_name = models.CharField(max_length=50, default=None)
    strike = models.CharField(max_length=10, default=None)
    target = models.CharField(max_length=100, default=None)
    is_demo_trading_enabled = models.BooleanField(default=True)
    use_full_capital = models.BooleanField(default=False)
    lots = models.CharField(max_length=10, default=None)
    on_candle_close = models.BooleanField(default=False)
    status = models.CharField(max_length=250, default=None)
    def __str__(self):
        return self.index_name

    @classmethod
    def search_by_name(cls, query):
        return cls.objects.filter(name__icontains=query)


class CandleData(models.Model):
    index_name = models.CharField(max_length=50, default=None)
    token = models.CharField(max_length=50, default=None)
    time = models.CharField(max_length=50, default=None)
    open = models.CharField(max_length=50, default=None)
    high = models.CharField(max_length=50, default=None)
    low = models.CharField(max_length=50, default=None)
    close = models.CharField(max_length=50, default=None)

    def __str__(self):
        return f"{self.index_name} - {self.token} - {self.time} - {self.open} - {self.high} - {self.low} - {self.close}"

    @classmethod
    def search_by_name(cls, query):
        return cls.objects.filter(name__icontains=query)


class UserAuthTokens(models.Model):
    user_id = models.CharField(max_length=500, default=None)
    refreshToken = models.CharField(max_length=2000, default=None)
    jwtToken = models.CharField(max_length=2000, default=None)
    feedToken = models.CharField(max_length=2000, default=None)
    last_updated_time = models.CharField(max_length=500, default=None)
    index_group = models.CharField(max_length=20, default="indian_index")
    def __str__(self):
        # return str({"user_id": self.user_id,"jwtToken": self.jwtToken,"feedToken": self.feedToken})
        return json.dumps({
            "user_id": self.user_id,
            "jwtToken": self.jwtToken,
            "feedToken": self.feedToken
        })
    @classmethod
    def search_by_name(cls, query):
        return cls.objects.filter(name__icontains=query)


class ManualOrders(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('INTRADAY', 'INTRADAY'),
        ('CARRYFORWARD', 'CARRYFORWARD'),
    ]
    TIMEFRAME_CHOICES = [
        ('ONE_MINUTE', 'ONE_MINUTE'),
        ('THREE_MINUTE', 'THREE_MINUTE'),
        ('FIVE_MINUTE', 'FIVE_MINUTE'),
        ('TEN_MINUTE', 'TEN_MINUTE'),
        ('FIFTEEN_MINUTE', 'FIFTEEN_MINUTE'),
        ('THIRTY_MINUTE', 'THIRTY_MINUTE'),
        ('ONE_HOUR', 'ONE_HOUR'),
        ('ONE_DAY', 'ONE_DAY'),
    ]
    user_id = models.CharField(max_length=100, default=None)
    index_name = models.CharField(max_length=100, default=None)
    target = models.CharField(max_length=100, default=None,blank=True, null=True)
    stop_loss = models.CharField(max_length=100, default=None,blank=True, null=True)
    order_status = models.CharField(max_length=100, default=None,blank=True, null=True)
    strike = models.CharField(max_length=100, default=None)
    lots = models.CharField(max_length=100, default=None,)
    trigger = models.CharField(max_length=100, default=None,blank=True, null=True)
    time = models.CharField(max_length=100, default=None,blank=True, null=True)
    order_id = models.CharField(max_length=100, default=None ,blank=True, null=True)
    unique_order_id = models.CharField(max_length=100, default=None,blank=True, null=True)
    current_premium = models.CharField(max_length=100, default=None,blank=True, null=True)
    on_candle_close = models.BooleanField(default=False)
    producttype = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default='INTRADAY')
    timeframe = models.CharField(max_length=20, choices=TIMEFRAME_CHOICES, default='FIVE_MINUTE')
    index_group = models.CharField(max_length=20, default="indian_index")
    strategy_name = models.CharField(max_length=225, default=None, blank=True, null=True,unique=True)
    strategy_type = models.CharField(max_length=100, default="default", blank=True, null=True)

    def __str__(self):
        return f"{self.user_id} - {self.index_name} - {self.target} - {self.stop_loss} - {self.order_status} - {self.time}"

    @classmethod
    def search_by_name(cls, query):
        return cls.objects.filter(name__icontains=query)


class WebhookDetails(models.Model):
    user_id = models.CharField(max_length=100, default=None)
    index_name = models.CharField(max_length=100, default=None)
    target = models.CharField(max_length=100, default=None , null=True)
    order_status = models.CharField(max_length=100, default=None)
    time = models.CharField(max_length=100, default=None)
    is_demo_trading_enabled = models.BooleanField(default=True)
    strategy = models.CharField(max_length=100, default=None)
    order_id = models.CharField(max_length=100, default=None)
    unique_order_id = models.CharField(max_length=100, default=None)
    current_premium = models.CharField(max_length=100, default=None)
    def __str__(self):
        return f"{self.user_id} - {self.index_name} - {self.target} -  {self.order_status} - {self.time} - {self.is_demo_trading_enabled}"

    @classmethod
    def search_by_name(cls, query):
        return cls.objects.filter(name__icontains=query)


class FlashDetails(models.Model):
    user_id = models.CharField(max_length=100, default=None)
    index_name = models.CharField(max_length=20, default=None)
    strike = models.CharField(max_length=10, default=None)
    max_profit = models.CharField(max_length=20, default=None)
    max_loss = models.CharField(max_length=20, default=None)
    trend_check_points = models.CharField(max_length=10, default='15')
    trailing_points = models.CharField(max_length=10, default='10')
    is_demo_trading_enabled = models.BooleanField(default=True)
    lots = models.CharField(max_length=10, default=None)
    status = models.CharField(max_length=20, default=None)
    average_points = models.CharField(max_length=20, default=None)

    def __str__(self):
        return self.index_name

    @classmethod
    def search_by_name(cls, query):
        return cls.objects.filter(name__icontains=query)

class LogDetails(models.Model):
    user_id = models.CharField(max_length=100, default=None)
    index_name = models.CharField(max_length=100, default=None)
    log = models.CharField(max_length=500, default=None , null=True)
    log_type = models.CharField(max_length=10, default="trigger" , null=True)
    time = models.CharField(max_length=100, default=None, null=True)

    def __str__(self):
        return f"{self.user_id} - {self.index_name} - {self.log_type} -  {self.log} "

    @classmethod
    def search_by_name(cls, query):
        return cls.objects.filter(name__icontains=query)