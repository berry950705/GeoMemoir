from django.contrib import admin
from story.models import Story, LikeStatus


# Register your models here.
class StoryManager(admin.ModelAdmin):
    list_display = ['title', 'area', 'category', 'country', 'view', 'name_of_author']

    def name_of_author(self, obj):
        return obj.author.first_name + ' ' + obj.author.last_name


class LikeStatusManager(admin.ModelAdmin):
    list_display = ['story_title', 'name_of_user', 'is_clicked']

    def story_title(self, obj):
        return obj.story.title

    def name_of_user(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name


admin.site.register(Story, StoryManager)
admin.site.register(LikeStatus, LikeStatusManager)

