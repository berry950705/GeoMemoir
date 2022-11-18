from django.contrib import admin
from contact.models import Contact


# Register your models here.
class ContactManager(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_time']


admin.site.register(Contact, ContactManager)

