from django.contrib import admin
from subscribe.models import Subscribe


# Register your models here.
class SubscribeManager(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_time']


admin.site.register(Subscribe, SubscribeManager)

