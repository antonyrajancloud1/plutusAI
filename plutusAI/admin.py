from django.contrib import admin
from .models import Configuration, TelegramSettings

# Register your models here.
admin.site.register(Configuration)
admin.site.register(TelegramSettings)
