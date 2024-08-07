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
    stage = models.CharField(max_length=250, default='stopped')
    lots = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.index_name

    @classmethod
    def search_by_name(cls, query):
        return cls.objects.filter(name__icontains=query)


class OrderBook(models.Model):
    user_id = models.CharField(max_length=500, default=None)
    entry_time = models.CharField(max_length=500, default=None)
    exit_time = models.CharField(max_length=500, default=None,blank=True, null=True)
    script_name = models.CharField(max_length=250, default=None)
    qty = models.CharField(max_length=250, default=None)
    entry_price = models.CharField(max_length=250, default=None, blank=True)
    exit_price = models.CharField(max_length=250, default=None, blank=True, null=True)
    status = models.CharField(max_length=250, default=None)
    total = models.CharField(max_length=250, default=None, blank=True, null=True)
    strategy = models.CharField(max_length=250, default=None, blank=True, null=True)

    def __str__(self):
        return "{" + f"user_id:{self.user_id}, script_name:{self.script_name}, entry_time:{self.entry_time}, exit_time:{self.exit_time},total:{self.total}" + "}"

    @classmethod
    def search_by_name(cls, query):
        return cls.objects.filter(name__icontains=query)


class BrokerDetails(models.Model):
    user_id = models.CharField(max_length=500, default=None)
    broker_name = models.CharField(max_length=250, default=None)
    broker_user_id = models.CharField(max_length=250, default=None)
    broker_user_name = models.CharField(max_length=250, default=None, blank=True)
    broker_mpin = models.CharField(max_length=250, default=None, blank=True)
    broker_api_token = models.CharField(max_length=250, default=None)
    broker_qr = models.CharField(max_length=250, default=None, blank=True)
    token_status = models.CharField(max_length=250, default=None)
    is_demo_trading_enabled = models.BooleanField(default=False)
    index_group = models.CharField(max_length=20, default=None)

    def __str__(self):
        return self.index_name

    @classmethod
    def search_by_name(cls, query):
        return cls.objects.filter(name__icontains=query)


class IndexDetails(models.Model):
    index_name = models.CharField(max_length=50, default=None)
    index_group = models.CharField(max_length=50, default=None)
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
