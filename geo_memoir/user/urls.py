from django.urls import path

from user import views

urlpatterns = [
    path('login_account', views.show_login_account),
    path('forgot_password', views.forgot_password),
    path('reset_password', views.reset_password),
    path('<str:username>', views.UserViews.as_view()),
    path('<str:username>/edit_profile', views.edit_profile),
    path('<str:username>/get_user_email', views.get_user_email),
    path('<str:username>/send_email_code', views.send_email_code),
    path('<str:username>/change_email', views.change_email),
    path('<str:username>/change_password', views.change_password),
]

