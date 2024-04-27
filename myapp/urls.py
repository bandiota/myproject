from django.urls import path
from.views import *


urlpatterns = [
    path('', dashboard),
    path('profile/<str:uname>', profile),
    path('profile-delete/<str:uname>', profile_delete),
    path('register', register),
    path('login', login),
    path('logout', logout),
    path('notification/<str:uname>', send_notifications),
    path('read-notification', read_notification),
]
