from django.contrib import admin
from user.models import UserProfile


# Register your models here.
class UserManager(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'profile_name', 'created_time', 'updated_time']


admin.site.register(UserProfile, UserManager)
