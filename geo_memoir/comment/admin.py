from django.contrib import admin
from comment.models import Comment


# Register your models here.
class CommentManager(admin.ModelAdmin):
    list_display = ['story_title', 'name_of_commenter', 'created_time', 'updated_time']

    def name_of_commenter(self, obj):
        return obj.commenter.first_name + ' ' + obj.commenter.last_name

    def story_title(self, obj):
        return obj.story.title

admin.site.register(Comment, CommentManager)

