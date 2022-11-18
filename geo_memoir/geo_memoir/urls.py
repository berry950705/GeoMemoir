"""geo_memoir URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf.urls.static import static

import user.views as user_views
import comment.views as comment_views
import gallery.views as gallery_views
import contact.views as contact_views
import subscribe.views as subscribe_views
from . import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/<str:lang_code>/v1/tokens/', include('gtoken.urls')),
    path('api/<str:lang_code>/v1/users', user_views.UserViews.as_view()),
    path('api/<str:lang_code>/v1/users/', include('user.urls')),
    path('api/<str:lang_code>/v1/stories/', include('story.urls')),
    path('api/<str:lang_code>/v1/comments', comment_views.CommentViews.as_view()),
    path('api/<str:lang_code>/v1/gallery', gallery_views.get_photos),
    path('api/<str:lang_code>/v1/weather/', include('weather.urls')),
    path('api/<str:lang_code>/v1/contact', contact_views.contact_info),
    path('api/<str:lang_code>/v1/subscribe', subscribe_views.subscribe_info)
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

