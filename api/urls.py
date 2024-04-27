from django.urls import path
from .views import *

urlpatterns = [
    path('users', getUsers),
    path('user/<str:uname>', getUser),
    path('users/add', setUser),
    path('user/update/<str:uname>', updateUser),
    path('user/delete/<str:uname>', deleteUser),
]
