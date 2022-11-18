# from django.urls import path
from django.urls import path
from story import views
urlpatterns = [
    path('<str:username>/get_story', views.get_story),
    path('<str:username>/post_story', views.post_story),
    path('<str:username>/update_story', views.update_story),
    path('<str:username>/delete_story', views.delete_story),
    path('<str:username>/story_list', views.stories_list),
    path('<str:username>/like_story', views.like_story),
    path('destinations', views.destination_stories)
]










